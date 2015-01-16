'''
NL80211 module
================

TODO
'''

from pyroute2.netlink import genlmsg
from pyroute2.netlink.generic import GenericNetlinkSocket
from pyroute2.netlink.nlsocket import Marshal

# nl80211 commands

NL80211_CMD_UNSPEC = 0
NL80211_CMD_GET_WIPHY = 1
NL80211_CMD_SET_WIPHY = 2
NL80211_CMD_NEW_WIPHY = 3
NL80211_CMD_DEL_WIPHY = 4
NL80211_CMD_GET_INTERFACE = 5
NL80211_CMD_SET_INTERFACE = 6
NL80211_CMD_NEW_INTERFACE = 7
NL80211_CMD_DEL_INTERFACE = 8
NL80211_CMD_GET_KEY = 9
NL80211_CMD_SET_KEY = 10
NL80211_CMD_NEW_KEY = 11
NL80211_CMD_DEL_KEY = 12
NL80211_CMD_GET_BEACON = 13
NL80211_CMD_SET_BEACON = 14
NL80211_CMD_START_AP = 15
NL80211_CMD_NEW_BEACON = NL80211_CMD_START_AP
NL80211_CMD_STOP_AP = 16
NL80211_CMD_DEL_BEACON = NL80211_CMD_STOP_AP
NL80211_CMD_GET_STATION = 17
NL80211_CMD_SET_STATION = 18
NL80211_CMD_NEW_STATION = 19
NL80211_CMD_DEL_STATION = 20
NL80211_CMD_GET_MPATH = 21
NL80211_CMD_SET_MPATH = 22
NL80211_CMD_NEW_MPATH = 23
NL80211_CMD_DEL_MPATH = 24
NL80211_CMD_SET_BSS = 25
NL80211_CMD_SET_REG = 26
NL80211_CMD_REQ_SET_REG = 27
NL80211_CMD_GET_MESH_CONFIG = 28
NL80211_CMD_SET_MESH_CONFIG = 29
NL80211_CMD_SET_MGMT_EXTRA_IE = 30
NL80211_CMD_GET_REG = 31
NL80211_CMD_GET_SCAN = 32
NL80211_CMD_TRIGGER_SCAN = 33
NL80211_CMD_NEW_SCAN_RESULTS = 34
NL80211_CMD_SCAN_ABORTED = 35
NL80211_CMD_REG_CHANGE = 36
NL80211_CMD_AUTHENTICATE = 37
NL80211_CMD_ASSOCIATE = 38
NL80211_CMD_DEAUTHENTICATE = 39
NL80211_CMD_DISASSOCIATE = 40
NL80211_CMD_MICHAEL_MIC_FAILURE = 41
NL80211_CMD_REG_BEACON_HINT = 42
NL80211_CMD_JOIN_IBSS = 43
NL80211_CMD_LEAVE_IBSS = 44
NL80211_CMD_TESTMODE = 45
NL80211_CMD_CONNECT = 46
NL80211_CMD_ROAM = 47
NL80211_CMD_DISCONNECT = 48
NL80211_CMD_SET_WIPHY_NETNS = 49
NL80211_CMD_GET_SURVEY = 50
NL80211_CMD_NEW_SURVEY_RESULTS = 51
NL80211_CMD_SET_PMKSA = 52
NL80211_CMD_DEL_PMKSA = 53
NL80211_CMD_FLUSH_PMKSA = 54
NL80211_CMD_REMAIN_ON_CHANNEL = 55
NL80211_CMD_CANCEL_REMAIN_ON_CHANNEL = 56
NL80211_CMD_SET_TX_BITRATE_MASK = 57
NL80211_CMD_REGISTER_FRAME = 58
NL80211_CMD_REGISTER_ACTION = NL80211_CMD_REGISTER_FRAME
NL80211_CMD_FRAME = 59
NL80211_CMD_ACTION = NL80211_CMD_FRAME
NL80211_CMD_FRAME_TX_STATUS = 60
NL80211_CMD_ACTION_TX_STATUS = NL80211_CMD_FRAME_TX_STATUS
NL80211_CMD_SET_POWER_SAVE = 61
NL80211_CMD_GET_POWER_SAVE = 62
NL80211_CMD_SET_CQM = 63
NL80211_CMD_NOTIFY_CQM = 64
NL80211_CMD_SET_CHANNEL = 65
NL80211_CMD_SET_WDS_PEER = 66
NL80211_CMD_FRAME_WAIT_CANCEL = 67
NL80211_CMD_JOIN_MESH = 68
NL80211_CMD_LEAVE_MESH = 69
NL80211_CMD_UNPROT_DEAUTHENTICATE = 70
NL80211_CMD_UNPROT_DISASSOCIATE = 71
NL80211_CMD_NEW_PEER_CANDIDATE = 72
NL80211_CMD_GET_WOWLAN = 73
NL80211_CMD_SET_WOWLAN = 74
NL80211_CMD_START_SCHED_SCAN = 75
NL80211_CMD_STOP_SCHED_SCAN = 76
NL80211_CMD_SCHED_SCAN_RESULTS = 77
NL80211_CMD_SCHED_SCAN_STOPPED = 78
NL80211_CMD_SET_REKEY_OFFLOAD = 79
NL80211_CMD_PMKSA_CANDIDATE = 80
NL80211_CMD_TDLS_OPER = 81
NL80211_CMD_TDLS_MGMT = 82
NL80211_CMD_UNEXPECTED_FRAME = 83
NL80211_CMD_PROBE_CLIENT = 84
NL80211_CMD_REGISTER_BEACONS = 85
NL80211_CMD_UNEXPECTED_4ADDR_FRAME = 86
NL80211_CMD_SET_NOACK_MAP = 87
NL80211_CMD_CH_SWITCH_NOTIFY = 88
NL80211_CMD_START_P2P_DEVICE = 89
NL80211_CMD_STOP_P2P_DEVICE = 90
NL80211_CMD_CONN_FAILED = 91
NL80211_CMD_SET_MCAST_RATE = 92
NL80211_CMD_SET_MAC_ACL = 93
NL80211_CMD_RADAR_DETECT = 94
NL80211_CMD_GET_PROTOCOL_FEATURES = 95
NL80211_CMD_UPDATE_FT_IES = 96
NL80211_CMD_FT_EVENT = 97
NL80211_CMD_CRIT_PROTOCOL_START = 98
NL80211_CMD_CRIT_PROTOCOL_STOP = 99
NL80211_CMD_GET_COALESCE = 100
NL80211_CMD_SET_COALESCE = 101
NL80211_CMD_CHANNEL_SWITCH = 102
NL80211_CMD_VENDOR = 103
NL80211_CMD_SET_QOS_MAP = 104
NL80211_CMD_ADD_TX_TS = 105
NL80211_CMD_DEL_TX_TS = 106
NL80211_CMD_GET_MPP = 107
NL80211_CMD_JOIN_OCB = 108
NL80211_CMD_LEAVE_OCB = 109
NL80211_CMD_CH_SWITCH_STARTED_NOTIFY = 110
NL80211_CMD_TDLS_CHANNEL_SWITCH = 111
NL80211_CMD_TDLS_CANCEL_CHANNEL_SWITCH = 112
NL80211_CMD_WIPHY_REG_CHANGE = 113
NL80211_CMD_MAX = NL80211_CMD_WIPHY_REG_CHANGE


class nl80211cmd(genlmsg):
    nla_map = (('NL80211_ATTR_UNSPEC', 'none'),
               ('NL80211_ATTR_WIPHY', 'none'),
               ('NL80211_ATTR_WIPHY_NAME', 'none'),
               ('NL80211_ATTR_IFINDEX', 'uint32'),
               ('NL80211_ATTR_IFNAME', 'none'),
               ('NL80211_ATTR_IFTYPE', 'none'),
               ('NL80211_ATTR_MAC', 'none'),
               ('NL80211_ATTR_KEY_DATA', 'none'),
               ('NL80211_ATTR_KEY_IDX', 'none'),
               ('NL80211_ATTR_KEY_CIPHER', 'uint32'),
               ('NL80211_ATTR_KEY_SEQ', 'none'),
               ('NL80211_ATTR_KEY_DEFAULT', 'none'),
               ('NL80211_ATTR_BEACON_INTERVAL', 'none'),
               ('NL80211_ATTR_DTIM_PERIOD', 'none'),
               ('NL80211_ATTR_BEACON_HEAD', 'none'),
               ('NL80211_ATTR_BEACON_TAIL', 'none'),
               ('NL80211_ATTR_STA_AID', 'none'),
               ('NL80211_ATTR_STA_FLAGS', 'none'),
               ('NL80211_ATTR_STA_LISTEN_INTERVAL', 'none'),
               ('NL80211_ATTR_STA_SUPPORTED_RATES', 'none'),
               ('NL80211_ATTR_STA_VLAN', 'none'),
               ('NL80211_ATTR_STA_INFO', 'none'),
               ('NL80211_ATTR_WIPHY_BANDS', 'none'),
               ('NL80211_ATTR_MNTR_FLAGS', 'none'),
               ('NL80211_ATTR_MESH_ID', 'none'),
               ('NL80211_ATTR_STA_PLINK_ACTION', 'none'),
               ('NL80211_ATTR_MPATH_NEXT_HOP', 'none'),
               ('NL80211_ATTR_MPATH_INFO', 'none'),
               ('NL80211_ATTR_BSS_CTS_PROT', 'none'),
               ('NL80211_ATTR_BSS_SHORT_PREAMBLE', 'none'),
               ('NL80211_ATTR_BSS_SHORT_SLOT_TIME', 'none'),
               ('NL80211_ATTR_HT_CAPABILITY', 'none'),
               ('NL80211_ATTR_SUPPORTED_IFTYPES', 'none'),
               ('NL80211_ATTR_REG_ALPHA2', 'none'),
               ('NL80211_ATTR_REG_RULES', 'none'),
               ('NL80211_ATTR_MESH_CONFIG', 'none'),
               ('NL80211_ATTR_BSS_BASIC_RATES', 'none'),
               ('NL80211_ATTR_WIPHY_TXQ_PARAMS', 'none'),
               ('NL80211_ATTR_WIPHY_FREQ', 'none'),
               ('NL80211_ATTR_WIPHY_CHANNEL_TYPE', 'none'),
               ('NL80211_ATTR_KEY_DEFAULT_MGMT', 'none'),
               ('NL80211_ATTR_MGMT_SUBTYPE', 'none'),
               ('NL80211_ATTR_IE', 'none'),
               ('NL80211_ATTR_MAX_NUM_SCAN_SSIDS', 'none'),
               ('NL80211_ATTR_SCAN_FREQUENCIES', 'none'),
               ('NL80211_ATTR_SCAN_SSIDS', 'none'),
               ('NL80211_ATTR_GENERATION', 'none'),
               ('NL80211_ATTR_BSS', 'none'),
               ('NL80211_ATTR_REG_INITIATOR', 'none'),
               ('NL80211_ATTR_REG_TYPE', 'none'),
               ('NL80211_ATTR_SUPPORTED_COMMANDS', 'none'),
               ('NL80211_ATTR_FRAME', 'none'),
               ('NL80211_ATTR_SSID', 'none'),
               ('NL80211_ATTR_AUTH_TYPE', 'none'),
               ('NL80211_ATTR_REASON_CODE', 'none'),
               ('NL80211_ATTR_KEY_TYPE', 'none'),
               ('NL80211_ATTR_MAX_SCAN_IE_LEN', 'none'),
               ('NL80211_ATTR_CIPHER_SUITES', 'none'),
               ('NL80211_ATTR_FREQ_BEFORE', 'none'),
               ('NL80211_ATTR_FREQ_AFTER', 'none'),
               ('NL80211_ATTR_FREQ_FIXED', 'none'),
               ('NL80211_ATTR_WIPHY_RETRY_SHORT', 'none'),
               ('NL80211_ATTR_WIPHY_RETRY_LONG', 'none'),
               ('NL80211_ATTR_WIPHY_FRAG_THRESHOLD', 'none'),
               ('NL80211_ATTR_WIPHY_RTS_THRESHOLD', 'none'),
               ('NL80211_ATTR_TIMED_OUT', 'none'),
               ('NL80211_ATTR_USE_MFP', 'none'),
               ('NL80211_ATTR_STA_FLAGS2', 'none'),
               ('NL80211_ATTR_CONTROL_PORT', 'none'),
               ('NL80211_ATTR_TESTDATA', 'none'),
               ('NL80211_ATTR_PRIVACY', 'none'),
               ('NL80211_ATTR_DISCONNECTED_BY_AP', 'none'),
               ('NL80211_ATTR_STATUS_CODE', 'none'),
               ('NL80211_ATTR_CIPHER_SUITES_PAIRWISE', 'none'),
               ('NL80211_ATTR_CIPHER_SUITE_GROUP', 'none'),
               ('NL80211_ATTR_WPA_VERSIONS', 'none'),
               ('NL80211_ATTR_AKM_SUITES', 'none'),
               ('NL80211_ATTR_REQ_IE', 'none'),
               ('NL80211_ATTR_RESP_IE', 'none'),
               ('NL80211_ATTR_PREV_BSSID', 'none'),
               ('NL80211_ATTR_KEY', 'none'),
               ('NL80211_ATTR_KEYS', 'none'),
               ('NL80211_ATTR_PID', 'none'),
               ('NL80211_ATTR_4ADDR', 'none'),
               ('NL80211_ATTR_SURVEY_INFO', 'none'),
               ('NL80211_ATTR_PMKID', 'none'),
               ('NL80211_ATTR_MAX_NUM_PMKIDS', 'none'),
               ('NL80211_ATTR_DURATION', 'none'),
               ('NL80211_ATTR_COOKIE', 'none'),
               ('NL80211_ATTR_WIPHY_COVERAGE_CLASS', 'none'),
               ('NL80211_ATTR_TX_RATES', 'none'),
               ('NL80211_ATTR_FRAME_MATCH', 'none'),
               ('NL80211_ATTR_ACK', 'none'),
               ('NL80211_ATTR_PS_STATE', 'none'),
               ('NL80211_ATTR_CQM', 'none'),
               ('NL80211_ATTR_LOCAL_STATE_CHANGE', 'none'),
               ('NL80211_ATTR_AP_ISOLATE', 'none'),
               ('NL80211_ATTR_WIPHY_TX_POWER_SETTING', 'none'),
               ('NL80211_ATTR_WIPHY_TX_POWER_LEVEL', 'none'),
               ('NL80211_ATTR_TX_FRAME_TYPES', 'none'),
               ('NL80211_ATTR_RX_FRAME_TYPES', 'none'),
               ('NL80211_ATTR_FRAME_TYPE', 'none'),
               ('NL80211_ATTR_CONTROL_PORT_ETHERTYPE', 'none'),
               ('NL80211_ATTR_CONTROL_PORT_NO_ENCRYPT', 'none'),
               ('NL80211_ATTR_SUPPORT_IBSS_RSN', 'none'),
               ('NL80211_ATTR_WIPHY_ANTENNA_TX', 'none'),
               ('NL80211_ATTR_WIPHY_ANTENNA_RX', 'none'),
               ('NL80211_ATTR_MCAST_RATE', 'none'),
               ('NL80211_ATTR_OFFCHANNEL_TX_OK', 'none'),
               ('NL80211_ATTR_BSS_HT_OPMODE', 'none'),
               ('NL80211_ATTR_KEY_DEFAULT_TYPES', 'none'),
               ('NL80211_ATTR_MAX_REMAIN_ON_CHANNEL_DURATION', 'none'),
               ('NL80211_ATTR_MESH_SETUP', 'none'),
               ('NL80211_ATTR_WIPHY_ANTENNA_AVAIL_TX', 'none'),
               ('NL80211_ATTR_WIPHY_ANTENNA_AVAIL_RX', 'none'),
               ('NL80211_ATTR_SUPPORT_MESH_AUTH', 'none'),
               ('NL80211_ATTR_STA_PLINK_STATE', 'none'),
               ('NL80211_ATTR_WOWLAN_TRIGGERS', 'none'),
               ('NL80211_ATTR_WOWLAN_TRIGGERS_SUPPORTED', 'none'),
               ('NL80211_ATTR_SCHED_SCAN_INTERVAL', 'none'),
               ('NL80211_ATTR_INTERFACE_COMBINATIONS', 'none'),
               ('NL80211_ATTR_SOFTWARE_IFTYPES', 'none'),
               ('NL80211_ATTR_REKEY_DATA', 'none'),
               ('NL80211_ATTR_MAX_NUM_SCHED_SCAN_SSIDS', 'none'),
               ('NL80211_ATTR_MAX_SCHED_SCAN_IE_LEN', 'none'),
               ('NL80211_ATTR_SCAN_SUPP_RATES', 'none'),
               ('NL80211_ATTR_HIDDEN_SSID', 'none'),
               ('NL80211_ATTR_IE_PROBE_RESP', 'none'),
               ('NL80211_ATTR_IE_ASSOC_RESP', 'none'),
               ('NL80211_ATTR_STA_WME', 'none'),
               ('NL80211_ATTR_SUPPORT_AP_UAPSD', 'none'),
               ('NL80211_ATTR_ROAM_SUPPORT', 'none'),
               ('NL80211_ATTR_SCHED_SCAN_MATCH', 'none'),
               ('NL80211_ATTR_MAX_MATCH_SETS', 'none'),
               ('NL80211_ATTR_PMKSA_CANDIDATE', 'none'),
               ('NL80211_ATTR_TX_NO_CCK_RATE', 'none'),
               ('NL80211_ATTR_TDLS_ACTION', 'none'),
               ('NL80211_ATTR_TDLS_DIALOG_TOKEN', 'none'),
               ('NL80211_ATTR_TDLS_OPERATION', 'none'),
               ('NL80211_ATTR_TDLS_SUPPORT', 'none'),
               ('NL80211_ATTR_TDLS_EXTERNAL_SETUP', 'none'),
               ('NL80211_ATTR_DEVICE_AP_SME', 'none'),
               ('NL80211_ATTR_DONT_WAIT_FOR_ACK', 'none'),
               ('NL80211_ATTR_FEATURE_FLAGS', 'none'),
               ('NL80211_ATTR_PROBE_RESP_OFFLOAD', 'none'),
               ('NL80211_ATTR_PROBE_RESP', 'none'),
               ('NL80211_ATTR_DFS_REGION', 'none'),
               ('NL80211_ATTR_DISABLE_HT', 'none'),
               ('NL80211_ATTR_HT_CAPABILITY_MASK', 'none'),
               ('NL80211_ATTR_NOACK_MAP', 'none'),
               ('NL80211_ATTR_INACTIVITY_TIMEOUT', 'none'),
               ('NL80211_ATTR_RX_SIGNAL_DBM', 'none'),
               ('NL80211_ATTR_BG_SCAN_PERIOD', 'none'),
               ('NL80211_ATTR_WDEV', 'uint32'),
               ('NL80211_ATTR_USER_REG_HINT_TYPE', 'none'),
               ('NL80211_ATTR_CONN_FAILED_REASON', 'none'),
               ('NL80211_ATTR_SAE_DATA', 'none'),
               ('NL80211_ATTR_VHT_CAPABILITY', 'none'),
               ('NL80211_ATTR_SCAN_FLAGS', 'none'),
               ('NL80211_ATTR_CHANNEL_WIDTH', 'uint32'),
               ('NL80211_ATTR_CENTER_FREQ1', 'none'),
               ('NL80211_ATTR_CENTER_FREQ2', 'none'),
               ('NL80211_ATTR_P2P_CTWINDOW', 'none'),
               ('NL80211_ATTR_P2P_OPPPS', 'none'),
               ('NL80211_ATTR_LOCAL_MESH_POWER_MODE', 'none'),
               ('NL80211_ATTR_ACL_POLICY', 'none'),
               ('NL80211_ATTR_MAC_ADDRS', 'none'),
               ('NL80211_ATTR_MAC_ACL_MAX', 'none'),
               ('NL80211_ATTR_RADAR_EVENT', 'none'),
               ('NL80211_ATTR_EXT_CAPA', 'none'),
               ('NL80211_ATTR_EXT_CAPA_MASK', 'none'),
               ('NL80211_ATTR_STA_CAPABILITY', 'none'),
               ('NL80211_ATTR_STA_EXT_CAPABILITY', 'none'),
               ('NL80211_ATTR_PROTOCOL_FEATURES', 'none'),
               ('NL80211_ATTR_SPLIT_WIPHY_DUMP', 'none'),
               ('NL80211_ATTR_DISABLE_VHT', 'none'),
               ('NL80211_ATTR_VHT_CAPABILITY_MASK', 'none'),
               ('NL80211_ATTR_MDID', 'none'),
               ('NL80211_ATTR_IE_RIC', 'none'),
               ('NL80211_ATTR_CRIT_PROT_ID', 'none'),
               ('NL80211_ATTR_MAX_CRIT_PROT_DURATION', 'none'),
               ('NL80211_ATTR_PEER_AID', 'none'),
               ('NL80211_ATTR_COALESCE_RULE', 'none'),
               ('NL80211_ATTR_CH_SWITCH_COUNT', 'none'),
               ('NL80211_ATTR_CH_SWITCH_BLOCK_TX', 'none'),
               ('NL80211_ATTR_CSA_IES', 'none'),
               ('NL80211_ATTR_CSA_C_OFF_BEACON', 'none'),
               ('NL80211_ATTR_CSA_C_OFF_PRESP', 'none'),
               ('NL80211_ATTR_RXMGMT_FLAGS', 'none'),
               ('NL80211_ATTR_STA_SUPPORTED_CHANNELS', 'none'),
               ('NL80211_ATTR_STA_SUPPORTED_OPER_CLASSES', 'none'),
               ('NL80211_ATTR_HANDLE_DFS', 'none'),
               ('NL80211_ATTR_SUPPORT_5_MHZ', 'none'),
               ('NL80211_ATTR_SUPPORT_10_MHZ', 'none'),
               ('NL80211_ATTR_OPMODE_NOTIF', 'none'),
               ('NL80211_ATTR_VENDOR_ID', 'none'),
               ('NL80211_ATTR_VENDOR_SUBCMD', 'none'),
               ('NL80211_ATTR_VENDOR_DATA', 'none'),
               ('NL80211_ATTR_VENDOR_EVENTS', 'none'),
               ('NL80211_ATTR_QOS_MAP', 'none'),
               ('NL80211_ATTR_MAC_HINT', 'none'),
               ('NL80211_ATTR_WIPHY_FREQ_HINT', 'none'),
               ('NL80211_ATTR_MAX_AP_ASSOC_STA', 'none'),
               ('NL80211_ATTR_TDLS_PEER_CAPABILITY', 'none'),
               ('NL80211_ATTR_SOCKET_OWNER', 'none'),
               ('NL80211_ATTR_CSA_C_OFFSETS_TX', 'none'),
               ('NL80211_ATTR_MAX_CSA_COUNTERS', 'none'),
               ('NL80211_ATTR_TDLS_INITIATOR', 'none'),
               ('NL80211_ATTR_USE_RRM', 'none'),
               ('NL80211_ATTR_WIPHY_DYN_ACK', 'none'),
               ('NL80211_ATTR_TSID', 'none'),
               ('NL80211_ATTR_USER_PRIO', 'none'),
               ('NL80211_ATTR_ADMITTED_TIME', 'none'),
               ('NL80211_ATTR_SMPS_MODE', 'none'),
               ('NL80211_ATTR_OPER_CLASS', 'none'),
               ('NL80211_ATTR_MAC_MASK', 'none'),
               ('NL80211_ATTR_WIPHY_SELF_MANAGED_REG', 'none'),
               ('NUM_NL80211_ATTR', 'none'))


class MarshalNl80211(Marshal):
    msg_map = {NL80211_CMD_UNSPEC: genlmsg,
               NL80211_CMD_GET_WIPHY: genlmsg,
               NL80211_CMD_SET_WIPHY: genlmsg,
               NL80211_CMD_NEW_WIPHY: genlmsg,
               NL80211_CMD_DEL_WIPHY: genlmsg,
               NL80211_CMD_GET_INTERFACE: genlmsg,
               NL80211_CMD_SET_INTERFACE: genlmsg,
               NL80211_CMD_NEW_INTERFACE: genlmsg,
               NL80211_CMD_DEL_INTERFACE: genlmsg,
               NL80211_CMD_GET_KEY: genlmsg,
               NL80211_CMD_SET_KEY: genlmsg,
               NL80211_CMD_NEW_KEY: genlmsg,
               NL80211_CMD_DEL_KEY: genlmsg,
               NL80211_CMD_GET_BEACON: genlmsg,
               NL80211_CMD_SET_BEACON: genlmsg,
               NL80211_CMD_START_AP: genlmsg,
               NL80211_CMD_NEW_BEACON: genlmsg,
               NL80211_CMD_STOP_AP: genlmsg,
               NL80211_CMD_DEL_BEACON: genlmsg,
               NL80211_CMD_GET_STATION: genlmsg,
               NL80211_CMD_SET_STATION: genlmsg,
               NL80211_CMD_NEW_STATION: genlmsg,
               NL80211_CMD_DEL_STATION: genlmsg,
               NL80211_CMD_GET_MPATH: genlmsg,
               NL80211_CMD_SET_MPATH: genlmsg,
               NL80211_CMD_NEW_MPATH: genlmsg,
               NL80211_CMD_DEL_MPATH: genlmsg,
               NL80211_CMD_SET_BSS: genlmsg,
               NL80211_CMD_SET_REG: genlmsg,
               NL80211_CMD_REQ_SET_REG: genlmsg,
               NL80211_CMD_GET_MESH_CONFIG: genlmsg,
               NL80211_CMD_SET_MESH_CONFIG: genlmsg,
               NL80211_CMD_SET_MGMT_EXTRA_IE: genlmsg,
               NL80211_CMD_GET_REG: genlmsg,
               NL80211_CMD_GET_SCAN: genlmsg,
               NL80211_CMD_TRIGGER_SCAN: genlmsg,
               NL80211_CMD_NEW_SCAN_RESULTS: genlmsg,
               NL80211_CMD_SCAN_ABORTED: genlmsg,
               NL80211_CMD_REG_CHANGE: genlmsg,
               NL80211_CMD_AUTHENTICATE: genlmsg,
               NL80211_CMD_ASSOCIATE: genlmsg,
               NL80211_CMD_DEAUTHENTICATE: genlmsg,
               NL80211_CMD_DISASSOCIATE: genlmsg,
               NL80211_CMD_MICHAEL_MIC_FAILURE: genlmsg,
               NL80211_CMD_REG_BEACON_HINT: genlmsg,
               NL80211_CMD_JOIN_IBSS: genlmsg,
               NL80211_CMD_LEAVE_IBSS: genlmsg,
               NL80211_CMD_TESTMODE: genlmsg,
               NL80211_CMD_CONNECT: genlmsg,
               NL80211_CMD_ROAM: genlmsg,
               NL80211_CMD_DISCONNECT: genlmsg,
               NL80211_CMD_SET_WIPHY_NETNS: genlmsg,
               NL80211_CMD_GET_SURVEY: genlmsg,
               NL80211_CMD_NEW_SURVEY_RESULTS: genlmsg,
               NL80211_CMD_SET_PMKSA: genlmsg,
               NL80211_CMD_DEL_PMKSA: genlmsg,
               NL80211_CMD_FLUSH_PMKSA: genlmsg,
               NL80211_CMD_REMAIN_ON_CHANNEL: genlmsg,
               NL80211_CMD_CANCEL_REMAIN_ON_CHANNEL: genlmsg,
               NL80211_CMD_SET_TX_BITRATE_MASK: genlmsg,
               NL80211_CMD_REGISTER_FRAME: genlmsg,
               NL80211_CMD_REGISTER_ACTION: genlmsg,
               NL80211_CMD_FRAME: genlmsg,
               NL80211_CMD_ACTION: genlmsg,
               NL80211_CMD_FRAME_TX_STATUS: genlmsg,
               NL80211_CMD_ACTION_TX_STATUS: genlmsg,
               NL80211_CMD_SET_POWER_SAVE: genlmsg,
               NL80211_CMD_GET_POWER_SAVE: genlmsg,
               NL80211_CMD_SET_CQM: genlmsg,
               NL80211_CMD_NOTIFY_CQM: genlmsg,
               NL80211_CMD_SET_CHANNEL: genlmsg,
               NL80211_CMD_SET_WDS_PEER: genlmsg,
               NL80211_CMD_FRAME_WAIT_CANCEL: genlmsg,
               NL80211_CMD_JOIN_MESH: genlmsg,
               NL80211_CMD_LEAVE_MESH: genlmsg,
               NL80211_CMD_UNPROT_DEAUTHENTICATE: genlmsg,
               NL80211_CMD_UNPROT_DISASSOCIATE: genlmsg,
               NL80211_CMD_NEW_PEER_CANDIDATE: genlmsg,
               NL80211_CMD_GET_WOWLAN: genlmsg,
               NL80211_CMD_SET_WOWLAN: genlmsg,
               NL80211_CMD_START_SCHED_SCAN: genlmsg,
               NL80211_CMD_STOP_SCHED_SCAN: genlmsg,
               NL80211_CMD_SCHED_SCAN_RESULTS: genlmsg,
               NL80211_CMD_SCHED_SCAN_STOPPED: genlmsg,
               NL80211_CMD_SET_REKEY_OFFLOAD: genlmsg,
               NL80211_CMD_PMKSA_CANDIDATE: genlmsg,
               NL80211_CMD_TDLS_OPER: genlmsg,
               NL80211_CMD_TDLS_MGMT: genlmsg,
               NL80211_CMD_UNEXPECTED_FRAME: genlmsg,
               NL80211_CMD_PROBE_CLIENT: genlmsg,
               NL80211_CMD_REGISTER_BEACONS: genlmsg,
               NL80211_CMD_UNEXPECTED_4ADDR_FRAME: genlmsg,
               NL80211_CMD_SET_NOACK_MAP: genlmsg,
               NL80211_CMD_CH_SWITCH_NOTIFY: genlmsg,
               NL80211_CMD_START_P2P_DEVICE: genlmsg,
               NL80211_CMD_STOP_P2P_DEVICE: genlmsg,
               NL80211_CMD_CONN_FAILED: genlmsg,
               NL80211_CMD_SET_MCAST_RATE: genlmsg,
               NL80211_CMD_SET_MAC_ACL: genlmsg,
               NL80211_CMD_RADAR_DETECT: genlmsg,
               NL80211_CMD_GET_PROTOCOL_FEATURES: genlmsg,
               NL80211_CMD_UPDATE_FT_IES: genlmsg,
               NL80211_CMD_FT_EVENT: genlmsg,
               NL80211_CMD_CRIT_PROTOCOL_START: genlmsg,
               NL80211_CMD_CRIT_PROTOCOL_STOP: genlmsg,
               NL80211_CMD_GET_COALESCE: genlmsg,
               NL80211_CMD_SET_COALESCE: genlmsg,
               NL80211_CMD_CHANNEL_SWITCH: genlmsg,
               NL80211_CMD_VENDOR: genlmsg,
               NL80211_CMD_SET_QOS_MAP: genlmsg,
               NL80211_CMD_ADD_TX_TS: genlmsg,
               NL80211_CMD_DEL_TX_TS: genlmsg,
               NL80211_CMD_GET_MPP: genlmsg,
               NL80211_CMD_JOIN_OCB: genlmsg,
               NL80211_CMD_LEAVE_OCB: genlmsg,
               NL80211_CMD_CH_SWITCH_STARTED_NOTIFY: genlmsg,
               NL80211_CMD_TDLS_CHANNEL_SWITCH: genlmsg,
               NL80211_CMD_TDLS_CANCEL_CHANNEL_SWITCH: genlmsg,
               NL80211_CMD_WIPHY_REG_CHANGE: genlmsg}


class NL80211(GenericNetlinkSocket):

    def __init__(self):
        GenericNetlinkSocket.__init__(self)
        self.marshal = MarshalNl80211()

    def bind(self):
        GenericNetlinkSocket.bind(self, 'nl80211', genlmsg)
