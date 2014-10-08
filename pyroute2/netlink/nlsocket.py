import io
import os
import time
import struct
import logging
import traceback
import threading

from socket import AF_NETLINK
from socket import SOCK_DGRAM
from socket import MSG_PEEK
from socket import SOL_SOCKET
from socket import SO_RCVBUF
from socket import socket
from socket import error as SocketError

from pyroute2.common import AddrPool
from pyroute2.common import DEFAULT_RCVBUF
from pyroute2.netlink import nlmsg
from pyroute2.netlink import mtypes
from pyroute2.netlink import NetlinkError
from pyroute2.netlink import NetlinkDecodeError
from pyroute2.netlink import NetlinkHeaderDecodeError
from pyroute2.netlink import NLMSG_ERROR
from pyroute2.netlink import NLMSG_DONE
from pyroute2.netlink import NETLINK_GENERIC
from pyroute2.netlink import NLM_F_DUMP
from pyroute2.netlink import NLM_F_MULTI
from pyroute2.netlink import NLM_F_REQUEST


class Marshal(object):
    '''
    Generic marshalling class
    '''

    msg_map = {}
    debug = False

    def __init__(self):
        self.lock = threading.Lock()
        # one marshal instance can be used to parse one
        # message at once
        self.msg_map = self.msg_map or {}
        self.defragmentation = {}

    def parse(self, data, sock=None):
        '''
        Parse the data in the buffer

        If socket is provided, support defragmentation
        '''
        with self.lock:
            data.seek(0)
            offset = 0
            result = []

            if sock in self.defragmentation:
                save = self.defragmentation[sock]
                save.write(data.read())
                save.length += data.length
                # discard save
                data = save
                del self.defragmentation[sock]
                data.seek(0)

            while offset < data.length:
                # pick type and length
                (length, msg_type) = struct.unpack('IH', data.read(6))
                data.seek(offset)
                # if length + offset is greater than
                # remaining size, save the buffer for
                # defragmentation
                if (sock is not None) and (length + offset > data.length):
                    # create save buffer
                    self.defragmentation[sock] = save = io.BytesIO()
                    save.length = save.write(data.read())
                    # truncate data
                    data.truncate(offset)
                    break

                error = None
                if msg_type == NLMSG_ERROR:
                    data.seek(offset + 16)
                    code = abs(struct.unpack('i', data.read(4))[0])
                    if code > 0:
                        error = NetlinkError(code)
                    data.seek(offset)

                msg_class = self.msg_map.get(msg_type, nlmsg)
                msg = msg_class(data, debug=self.debug)
                try:
                    msg.decode()
                    msg['header']['error'] = error
                    # try to decode encapsulated error message
                    if error is not None:
                        enc_type = struct.unpack('H', msg.raw[24:26])[0]
                        enc_class = self.msg_map.get(enc_type, nlmsg)
                        enc = enc_class(msg.raw[20:])
                        enc.decode()
                        msg['header']['errmsg'] = enc
                except NetlinkHeaderDecodeError as e:
                    # in the case of header decoding error,
                    # create an empty message
                    msg = nlmsg()
                    msg['header']['error'] = e
                except NetlinkDecodeError as e:
                    msg['header']['error'] = e
                mtype = msg['header'].get('type', None)
                if mtype in (1, 2, 3, 4):
                    msg['event'] = mtypes.get(mtype, 'none')
                self.fix_message(msg)
                offset += msg.length
                result.append(msg)

            return result

    def fix_message(self, msg):
        pass


# 8<-----------------------------------------------------------
# Singleton, containing possible modifiers to the NetlinkSocket
# bind() call.
#
# Normally, you can open only one netlink connection for one
# process, but there is a hack. Current PID_MAX_LIMIT is 2^22,
# so we can use the rest to midify pid field.
#
# See also libnl library, lib/socket.c:generate_local_port()
sockets = AddrPool(minaddr=0x0,
                   maxaddr=0x3ff,
                   reverse=True)
# 8<-----------------------------------------------------------


class LockProxy(object):

    def __init__(self, factory, key):
        self.factory = factory
        self.refcount = 0
        self.key = key
        self.internal = threading.Lock()
        self.lock = factory.klass()

    def acquire(self, *argv, **kwarg):
        with self.internal:
            self.refcount += 1
            return self.lock.acquire()

    def release(self):
        with self.internal:
            self.refcount -= 1
            if (self.refcount == 0) and (self.key != 0):
                try:
                    del self.factory.locks[self.key]
                except KeyError:
                    pass
            return self.lock.release()

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()


class LockFactory(object):

    def __init__(self, klass=threading.RLock):
        self.klass = klass
        self.locks = {0: LockProxy(self, 0)}

    def __enter__(self):
        self.locks[0].acquire()

    def __exit__(self, exc_type, exc_value, traceback):
        self.locks[0].release()

    def __getitem__(self, key):
        if key is None:
            key = 0
        if key not in self.locks:
            self.locks[key] = LockProxy(self, key)
        return self.locks[key]

    def __delitem__(self, key):
        del self.locks[key]


class NetlinkSocket(socket):
    '''
    Generic netlink socket
    '''

    def __init__(self, family=NETLINK_GENERIC, port=None, pid=None):
        socket.__init__(self, AF_NETLINK, SOCK_DGRAM, family)
        global sockets

        # 8<-----------------------------------------
        # PID init is here only for compatibility,
        # later it will be completely moved to bind()
        self.addr_pool = AddrPool(minaddr=0xff)
        self.epid = None
        self.port = 0
        self.fixed = True
        self.backlog = {0: []}
        self.monitor = False
        self.callbacks = []     # [(predicate, callback, args), ...]
        self.backlog_lock = threading.Lock()
        self.read_lock = threading.Lock()
        self.change_master = threading.Event()
        self.lock = LockFactory()
        self.log = []
        self.get_timeout = 3
        self.get_timeout_exception = None
        if pid is None:
            self.pid = os.getpid() & 0x3fffff
            self.port = port
            self.fixed = self.port is not None
        elif pid == 0:
            self.pid = os.getpid()
        else:
            self.pid = pid
        # 8<-----------------------------------------
        self.groups = 0
        self.marshal = Marshal()

    def release(self):
        logging.warning("The `release()` call is deprecated")
        logging.warning("Use `close()` instead")
        self.close()

    def register_callback(self, callback,
                          predicate=lambda e, x: True, args=None):
        '''
        Register a callback to run on a message arrival.

        Callback is the function that will be called with the
        message as the first argument. Predicate is the optional
        callable object, that returns True or False. Upon True,
        the callback will be called. Upon False it will not.
        Args is a list or tuple of arguments.

        Simplest example, assume ipr is the IPRoute() instance::

            # create a simplest callback that will print messages
            def cb(env, msg):
                print(msg)

            # register callback for any message:
            ipr.register_callback(cb)

        More complex example, with filtering::

            # Set object's attribute after the message key
            def cb(env, msg, obj):
                obj.some_attr = msg["some key"]

            # Register the callback only for the loopback device, index 1:
            ipr.register_callback(cb,
                                  lambda e, x: x.get('index', None) == 1,
                                  (self, ))

        Please note: you do **not** need to register the default 0 queue
        to invoke callbacks on broadcast messages. Callbacks are
        iterated **before** messages get enqueued.
        '''
        if args is None:
            args = []
        self.callbacks.append((predicate, callback, args))

    def unregister_callback(self, callback):
        '''
        Remove the first reference to the function from the callback
        register
        '''
        cb = tuple(self.callbacks)
        for cr in cb:
            if cr[1] == callback:
                self.callbacks.pop(cb.index(cr))
                return

    def register_policy(self, policy, msg_class=None):
        '''
        Register netlink encoding/decoding policy. Can
        be specified in two ways:
        `nlsocket.register_policy(MSG_ID, msg_class)`
        to register one particular rule, or
        `nlsocket.register_policy({MSG_ID1: msg_class})`
        to register several rules at once.
        E.g.::

            policy = {RTM_NEWLINK: ifinfmsg,
                      RTM_DELLINK: ifinfmsg,
                      RTM_NEWADDR: ifaddrmsg,
                      RTM_DELADDR: ifaddrmsg}
            nlsocket.register_policy(policy)

        One can call `register_policy()` as many times,
        as one want to -- it will just extend the current
        policy scheme, not replace it.
        '''
        if isinstance(policy, int) and msg_class is not None:
            policy = {policy: msg_class}

        assert isinstance(policy, dict)
        for key in policy:
            self.marshal.msg_map[key] = policy[key]

        return self.marshal.msg_map

    def unregister_policy(self, policy):
        '''
        Unregister policy. Policy can be:

        * int -- then it will just remove one policy
        * list or tuple of ints -- remove all given
        * dict -- remove policies by keys from dict

        In the last case the routine will ignore dict values,
        it is implemented so just to make it compatible with
        `get_policy_map()` return value.
        '''
        if isinstance(policy, int):
            policy = [policy]
        elif isinstance(policy, dict):
            policy = list(policy)

        assert isinstance(policy, (tuple, list, set))

        for key in policy:
            del self.marshal.msg_map[key]

        return self.marshal.msg_map

    def get_policy_map(self, policy=None):
        '''
        Return policy for a given message type or for all
        message types. Policy parameter can be either int,
        or a list of ints. Always return dictionary.
        '''
        if policy is None:
            return self.marshal.msg_map

        if isinstance(policy, int):
            policy = [policy]

        assert isinstance(policy, (list, tuple, set))

        ret = {}
        for key in policy:
            ret[key] = self.marshal.msg_map[key]

        return ret

    def bind(self, groups=0, pid=None):
        '''
        Bind the socket to given multicast groups, using
        given pid.

        * If pid is None, use automatic port allocation
        * If pid == 0, use process' pid
        * If pid == <int>, use the value instead of pid
        '''
        if pid is not None:
            self.port = 0
            self.fixed = True
            self.pid = pid or os.getpid()

        self.groups = groups
        # if we have pre-defined port, use it strictly
        if self.fixed:
            self.epid = self.pid + (self.port << 22)
            socket.bind(self, (self.epid, self.groups))
            return

        # if we have no pre-defined port, scan all the
        # range till the first available port
        for i in range(1024):
            try:
                self.port = sockets.alloc()
                self.epid = self.pid + (self.port << 22)
                socket.bind(self, (self.epid, self.groups))
                # if we're here, bind() done successfully, just exit
                return
            except SocketError as e:
                # pass occupied sockets, raise other exceptions
                if e.errno != 98:
                    raise
        else:
            # raise "address in use" -- to be compatible
            raise SocketError(98, 'Address already in use')

    def put(self, msg, msg_type,
            msg_flags=NLM_F_REQUEST,
            addr=(0, 0),
            msg_seq=0,
            msg_pid=None):
        '''
        Construct a message from a dictionary and send it to
        the socket. Parameters:

        * msg -- the message in the dictionary format
        * msg_type -- the message type
        * msg_flags -- the message flags to use in the request
        * addr -- `sendto()` addr, default `(0, 0)`
        * msg_seq -- sequence number to use
        * msg_pid -- pid to use, if `None` -- use os.getpid()

        Example::

            s = IPRSocket()
            s.bind()
            s.put({'index': 1}, RTM_GETLINK)
            s.get()
            s.close()

        Please notice, that the return value of `s.get()` can be
        not the result of `s.put()`, but any broadcast message.
        To fix that, use `msg_seq` -- the response must contain the
        same `msg['header']['sequence_number']` value.
        '''
        if msg_seq != 0:
            self.lock[msg_seq].acquire()
        try:
            if msg_seq not in self.backlog:
                self.backlog[msg_seq] = []
            msg_class = self.marshal.msg_map[msg_type]
            if msg_pid is None:
                msg_pid = os.getpid()
            msg = msg_class(msg)
            msg['header']['type'] = msg_type
            msg['header']['flags'] = msg_flags
            msg['header']['sequence_number'] = msg_seq
            msg['header']['pid'] = msg_pid
            msg.encode()
            self.sendto(msg.buf.getvalue(), addr)
        except:
            raise
        finally:
            if msg_seq != 0:
                self.lock[msg_seq].release()

    def get(self, bufsize=DEFAULT_RCVBUF, msg_seq=0, terminate=None):
        '''
        Get parsed messages list. If `msg_seq` is given, return
        only messages with that `msg['header']['sequence_number']`,
        saving all other messages into `self.backlog`.

        The routine is thread-safe.

        The `bufsize` parameter can be:

        * -1: bufsize will be calculated from the first 4 bytes of
              the network data
        * 0: bufsize will be calculated from SO_RCVBUF sockopt
        * int >= 0: just a bufsize
        '''
        ctime = time.time()

        with self.lock[msg_seq]:
            if bufsize == -1:
                # get bufsize from the network data
                bufsize = struct.unpack("I", self.recv(4, MSG_PEEK))[0]
            elif bufsize == 0:
                # get bufsize from SO_RCVBUF
                bufsize = self.getsockopt(SOL_SOCKET, SO_RCVBUF) // 2

            ret = []
            enough = False
            while not enough:
                # 8<-----------------------------------------------------------
                #
                # This stage changes the backlog, so use mutex to
                # prevent side changes
                self.backlog_lock.acquire()
                ##
                # Stage 1. BEGIN
                #
                # 8<-----------------------------------------------------------
                #
                # Check backlog and return already collected
                # messages.
                #
                if msg_seq == 0 and self.backlog[0]:
                    # Zero queue.
                    #
                    # Load the backlog, if there is valid
                    # content in it
                    ret.extend(self.backlog[0])
                    self.backlog[0] = []
                    # And just exit
                    self.backlog_lock.release()
                    break
                elif self.backlog.get(msg_seq, None):
                    # Any other msg_seq.
                    #
                    # Collect messages up to the terminator.
                    # Terminator conditions:
                    #  * NLMSG_ERROR != 0
                    #  * NLMSG_DONE
                    #  * terminate() function (if defined)
                    #  * not NLM_F_MULTI
                    #
                    # Please note, that if terminator not occured,
                    # more `recv()` rounds CAN be required.
                    for msg in tuple(self.backlog[msg_seq]):

                        # Drop the message from the backlog, if any
                        self.backlog[msg_seq].remove(msg)

                        # If there is an error, raise exception
                        if msg['header'].get('error', None) is not None:
                            self.backlog[0].extend(self.backlog[msg_seq])
                            del self.backlog[msg_seq]
                            # The loop is done
                            self.backlog_lock.release()
                            raise msg['header']['error']

                        # If it is the terminator message, say "enough"
                        # and requeue all the rest into Zero queue
                        if (msg['header']['type'] == NLMSG_DONE) or \
                                (terminate is not None and terminate(msg)):
                            # The loop is done
                            enough = True

                        # If it is just a normal message, append it to
                        # the response
                        if not enough:
                            ret.append(msg)
                            # But finish the loop on single messages
                            if not msg['header']['flags'] & NLM_F_MULTI:
                                # but not multi -- so end the loop
                                enough = True

                        # Enough is enough, requeue the rest and delete
                        # our backlog
                        if enough:
                            self.backlog[0].extend(self.backlog[msg_seq])
                            del self.backlog[msg_seq]
                            break

                    # Next iteration
                    self.backlog_lock.release()
                else:
                    # Stage 1. END
                    #
                    # 8<-------------------------------------------------------
                    #
                    # Stage 2. BEGIN
                    #
                    # 8<-------------------------------------------------------
                    #
                    # Receive the data from the socket and put the messages
                    # into the backlog
                    #
                    self.backlog_lock.release()
                    ##
                    #
                    # Control the timeout. We should not be within the
                    # function more than TIMEOUT seconds. All the locks
                    # MUST be released here.
                    #
                    if time.time() - ctime > self.get_timeout:
                        if self.get_timeout_exception:
                            raise self.get_timeout_exception()
                        else:
                            return ret
                    #
                    if self.read_lock.acquire(False):
                        self.change_master.clear()
                        # If the socket is free to read from, occupy
                        # it and wait for the data
                        #
                        # This is a time consuming process, so all the
                        # locks, except the read lock must be released
                        data = io.BytesIO()
                        data.length = data.write(self.recv(bufsize))
                        msgs = self.marshal.parse(data, self)

                        # We've got the data, lock the backlog again
                        self.backlog_lock.acquire()
                        for msg in msgs:
                            seq = msg['header']['sequence_number']
                            if seq not in self.backlog:
                                if msg['header']['type'] == NLMSG_ERROR:
                                    # Drop orphaned NLMSG_ERROR messages
                                    continue
                                seq = 0
                            # 8<-----------------------------------------------
                            # Callbacks section
                            for cr in self.callbacks:
                                try:
                                    if cr[0](msg):
                                        cr[1](msg, *cr[2])
                                except:
                                    logging.warning("Callback fail: %s" % (cr))
                                    logging.warning(traceback.format_exc())
                            # 8<-----------------------------------------------
                            self.backlog[seq].append(msg)
                            # Monitor mode:
                            if self.monitor and seq != 0:
                                self.backlog[0].append(msg)
                        # We finished with the backlog, so release the lock
                        self.backlog_lock.release()

                        # Now wake up other threads
                        self.change_master.set()

                        # Finally, release the read lock: all data processed
                        self.read_lock.release()
                    else:
                        # If the socket is occupied and there is still no
                        # data for us, wait for the next master change or
                        # for a timeout
                        self.change_master.wait(1)
                    # 8<-------------------------------------------------------
                    #
                    # Stage 2. END
                    #
                    # 8<-------------------------------------------------------

            return ret

    def nlm_request(self, msg, msg_type,
                    msg_flags=NLM_F_REQUEST | NLM_F_DUMP,
                    terminate=None):
        msg_seq = self.addr_pool.alloc()
        with self.lock[msg_seq]:
            try:
                self.put(msg, msg_type, msg_flags, msg_seq=msg_seq)
                ret = self.get(msg_seq=msg_seq, terminate=terminate)
                return ret
            except:
                print(msg_type, msg_flags, msg)
                raise
            finally:
                # Ban this msg_seq for 0xff rounds
                #
                # It's a long story. Modern kernels for RTM_SET.* operations
                # always return NLMSG_ERROR(0) == success, even not setting
                # NLM_F_MULTY flag on other response messages and thus w/o
                # any NLMSG_DONE. So, how to detect the response end? One
                # can not rely on NLMSG_ERROR on old kernels, but we have to
                # support them too. Ty, we just ban msg_seq for several rounds,
                # and NLMSG_ERROR, being received, will become orphaned and
                # just dropped.
                #
                # Hack, but true.
                self.addr_pool.free(msg_seq, ban=0xff)

    def close(self):
        '''
        Correctly close the socket and free all resources.
        '''
        global sockets
        if self.epid is not None:
            assert self.port is not None
            if not self.fixed:
                sockets.free(self.port)
            self.epid = None
        socket.close(self)