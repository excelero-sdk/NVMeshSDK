#!/usr/bin/env python
from builtins import object
import logging
import os
from future.utils import with_metaclass


class IterableEnumMeta(type):
    def __getattr__(cls, key):
        return cls.__dict__[key]

    def __setattr__(cls, key, value):
        raise TypeError('Cannot rename const attribute {0}.{1}'.format(cls.__name__, key))

    def __getitem__(cls, key):
        return cls.__dict__[key]

    def __iter__(cls):
        for key in cls.__dict__:
            if not callable(key) and type(cls.__dict__[key]) != staticmethod and not key.startswith('_'):
                yield cls.__dict__[key]

    def values(cls):
        return list(cls)


class StaticClass(object):
    def __new__(cls):
        raise Exception('Cannot instantiate Static Class {0}'.format(cls.__name__))


class Enum(with_metaclass(IterableEnumMeta, StaticClass)):
    pass


SYSLOG_PATH = '/dev/log'
DEFAULT_UNIT_TYPE = 'binary'


class ComponentStatus(Enum):
    UNKNOWN = 'UNKNOWN'
    NOT_INSTALLED = 'NOT_INSTALLED'
    IS_UP = 'IS_UP'
    IS_DOWN = 'IS_DOWN'


class EcSeparationTypes(Enum):
    FULL = 'Full Separation'
    MINIMAL = 'Minimal Separation'
    IGNORE = 'Ignore Separation'



class NVMeshService(Enum):
    NVMESH_TARGET = 'nvmeshtarget'
    NVMESH_TARGET_TOMA_RESTART = 'restart-toma'
    TARGET_KERNEL_MODULE = 'nvmeibs'
    NVMESH_CLIENT = 'nvmeshclient'
    CLIENT_KERNEL_MODULE = 'nvmeibc'
    NVMESH_MANAGEMENT = 'nvmeshmgr'
    INFRA_CLIENT = 'infraclient'


class NVMeshPid(Enum):
    TOMA_PID_PATH = '/var/run/NVMesh/nvmeshtarget/toma.pid'
    MANAGEMENT_CM_PID_PATH = '/var/run/NVMesh/managementCM.pid'
    OLD_MANAGEMENT_AGENT_PID_PATH = '/var/run/NVMesh/nvmeshclient/managementAgent.pid'
    MANAGEMENT_AGENT_PID_PATH = '/var/run/NVMesh/managementAgent.pid'
    MANAGEMENT_AGENT_PATH = '/opt/NVMesh/client-repo/management_cm/managementAgent.py'
    MANAGEMENT_PID_PATH = '/var/run/NVMesh/nvmeshmgr/management.pid'
    # Names used for ProcessManager class to work against the PIDs
    TOMA_PID_NAME = 'nvmeibt_toma'
    MANAGEMENT_AGENT_PID_NAME = '/opt/NVMesh/.*/managementAgent.py'
    MANAGEMENT_CM_PID_NAME = 'management_cm/managementCM.py'
    MANAGEMENT_CM_PATH = '/opt/NVMesh/client-repo/management_cm/managementCM.py'
    MANAGEMENT_PID_NAME = 'management/app.js'


class NVMeshVolume(Enum):
    CLIENT_VOLUMES_PATH = '/proc/nvmeibc/volumes/'
    CLIENT_VOLUMES_DEVPATH = '/dev/nvmesh/'
    NVME_TARGET_BUS_ADDRESS = '/sys/bus/pci/drivers/nvmeibs/'
    NVME_PCI_SCAN = '/sys/bus/pci/rescan'
    CLIENT_BLOCK_DEVICES = '/sys/kernel/config/nvmeibc/blockdevices'


class TomaProc(Enum):
    TOMA_STATUS_ALL = '/proc/nvmeibs/toma_status/all'
    TOMA_STATUS_BDEV = '/proc/nvmeibs/toma_status/bdev'
    TOMA_STATUS_CFG = '/proc/nvmeibs/toma_status/cfg'
    TOMA_STATUS_DISK = '/proc/nvmeibs/toma_status/disk'
    TOMA_STATUS_DSEG = '/proc/nvmeibs/toma_status/dseg'
    TOMA_STATUS_IB = '/proc/nvmeibs/toma_status/ib'
    TOMA_STATUS_RAFT = '/proc/nvmeibs/toma_status/raft'
    TOMA_STATUS_RTM = '/proc/nvmeibs/toma_status/rtm '
    TOMA_STATUS_TOPO = '/proc/nvmeibs/toma_status/topo'


class MonitoredServices(Enum):
    TOMA = 'tomaStatus'
    MANAGEMENT_AGENT = 'managementAgentStatus'
    MANAGEMENT = 'managementStatus'
    HOST_KEEP_ALIVE = 'serverKeepAlive'
    MCS = 'mcsStatus'


class IOEngines(Enum):
    LIBAIO = 'libaio'
    SYNC = 'sync'
    POSIXAIO = 'posixaio'
    MMAP = 'mmap'


class FIOpattern(Enum):
    READ = 'read'
    WRITE = 'write'
    TRIM = 'trim'
    RANDREAD = 'randread'
    RANDWRITE = 'randwrite'
    RANDRW = 'randrw'
    TRIMWRITE = 'trimwrite'


class MessageLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'

    @staticmethod
    def getInt(level):
        mappingToLoggingValues = {
            MessageLevel.DEBUG: logging.DEBUG,
            MessageLevel.WARNING: logging.WARNING,
            MessageLevel.INFO: logging.INFO,
            MessageLevel.ERROR: logging.ERROR,
        }

        return mappingToLoggingValues[level]


class SwitchHandler(Enum):
    SW_ETHERNET = 'eth'
    SW_ETHERNET_FULLNAME = 'ethernet'
    SW_INFINIBAND = 'ib'
    SW_VPI = 'vpi'
    SW_INFINIBAND_FULLNAME = 'infiniband'
    INTERFACE_UP = 'up'
    INTERFACE_DOWN = 'down'
    FLOWCONTROL_ON = 'on'
    FLOWCONTROL_OFF = 'off'
    HCA_INFINIBAND = 'InfiniBand'
    HCA_ETHERNET = 'Ethernet'
    INTERFACE_CX3 = 'cx3'
    INTERFACE_CX4 = 'cx4'
    VLAN_ACCESS = 'access'
    VLAN_ACCESS_DCB = 'access-dcb'
    VLAN_HYBRID = 'hybrid'
    VLAN_TRUNK = 'trunk'
    UNMANAGED_SW = 'unmanaged'


class SwitchVendor(Enum):
    DELL = 'dell'
    MLNX = 'mellanox'
    UNMANAGED_MLNX = 'unmanaged_mlnx'
    CUMULUS = 'cumulus'
    CISCO = 'cisco'


class FiberType(Enum):
    INFINIBAND = SwitchHandler.HCA_INFINIBAND
    ROCE = SwitchHandler.HCA_ETHERNET


class NVMeshDebugLevel(Enum):
    RELEASE = 'Release'
    DELEASE = 'Delease'
    DEBUG = 'Debug'


class NVMeshModuleDebugLevel(Enum):
    NVMEIBC_DBG_LEVEL = '/sys/module/nvmeibc/parameters/debug_level'
    NVMEIBS_DBG_LEVEL = '/sys/module/nvmeibs/parameters/debug_level'
    NVMEIB_COMMON_DBG_LEVEL = '/sys/module/nvmeib_common/parameters/debug_level'
    DEBUG_LEVEL_OFF = 1
    DEBUG_LEVEL_ON = 2


class BlockUniTestCommand(Enum):
    CLEAN = 'clean'
    BUILD = 'build'
    REBUILD = 'rebuild'
    RUN = 'run'
    EXEC = 'exec'
    CI = 'ci'
    DEPEND = 'depend'


class TestType(Enum):
    TEST = 'Test'
    DISASTER = 'Disaster'
    CONTROL_FLOW = 'ControlFlow'


class OsDistName(Enum):
    CENTOS_OS = 'centos'
    REDHAT_OS = 'redhat'
    UBUNTU_OS = 'ubuntu'
    SUSE_OS = 'suse'
    MINT_OS = 'linuxmint'
    FEDORA_OS = 'fedora'


class OsDistInstaller(Enum):
    FEDORA_PKG_INSTALLER = 'dnf'
    REDHAT_PKG_INSTALLER = 'yum'
    UBUNTU_PKG_INSTALLER = 'apt'
    SUSE_PKG_INSTALLER = 'zypper'


class OsDistPackageMgr(Enum):
    REDHAT_PKG_MGR = 'rpm'
    UBUNTU_PKG_MGR = 'dpkg'
    SUSE_PKG_MGR = 'rpm'


class OsDistPackageType(Enum):
    REDHAT_PKG_TYPE = 'rpm'
    UBU8NTU_PKG_TYPE = 'deb'
    SUSE_PKG_TYPE = 'rpm'


class NVMeshConfig(Enum):
    CONFIG_FILE = '/etc/opt/NVMesh/nvmesh.conf'


class TomaTraceConfig(Enum):
    CONFIG_FILE = '/var/log/NVMesh/trace.config'


class VolumeStatuses(Enum):
    PENDING = 'pending'
    ONLINE = 'online'
    OFFLINE = 'offline'
    DEGRADED = 'degraded'
    UNAVAILABLE = 'unavailable'
    QUORUM_FAILED = 'quorumFailed'


class VolumeActions(Enum):
    REBUILDING = 'rebuilding'
    MARKED_FOR_DELETION = 'markedForDeletion'
    MARKED_FOR_REBUILD = 'markedForRebuild'
    REBUILD_REQUIRED = 'rebuildRequired'
    MARKED_FOR_REBUILD_OLD = 'markedForRebuild_old'
    EXTENDING = 'extending'
    INITIALIZING = 'initializing'
    TO_BE_DELETED = 'toBeDeleted'
    NONE = 'none'


class VolumeAttachmentStatus(Enum):
    BUSY = 1
    DETACHED = 2
    DETACH_FAILED = 3
    ATTACHED = 4
    ATTACH_FAILED = 5


class BlockSize(Enum):
    SIZE_4K = '4K'
    SIZE_512 = '512'


class NICSConfig(object):
    KEEP_CURRENT_CONFIG = 'keep_current_configuration'
    AT_LEAST_ONE_INFINIBAND = 'at_least_one_Infiniband'
    ALL_INFINIBAND = 'all_Infiniband'
    AT_LEAST_ONE_ROCE = 'at_least_one_Roce'
    ALL_ROCE = 'all_Roce'


class NVMeshConfFields(Enum):
    MANAGEMENT_PROTOCOL = 'MANAGEMENT_PROTOCOL'
    MANAGEMENT_SERVERS = 'MANAGEMENT_SERVERS'
    CONFIGURED_NICS = 'CONFIGURED_NICS'
    MAX_SM_QUERY_BURST = 'MAX_SM_QUERY_BURST'
    MLX5_RDDA_ENABLED = 'MLX5_RDDA_ENABLED'
    DUMP_FTRACE_ON_OOPS = 'DUMP_FTRACE_ON_OOPS'
    AUTO_ATTACH_VOLUMES = 'AUTO_ATTACH_VOLUMES'
    TOMA_BUILD_TYPE = 'TOMA_BUILD_TYPE'
    TOMA_LOG_SIZE = 'TOMA_LOG_SIZE'
    TOMA_REDIRECT_OUTPUT_TO_FILE = 'TOMA_REDIRECT_OUTPUT_TO_FILE'
    MAX_CLIENT_RSRC = 'MAX_CLIENT_RSRC'
    MCS_LOGGING_LEVEL = 'MCS_LOGGING_LEVEL'
    AGENT_LOGGING_LEVEL = 'AGENT_LOGGING_LEVEL'
    ROCE_IPV4_ONLY = 'ROCE_IPV4_ONLY'


class ManagementLogLevel(Enum):
    VERBOSE = 'VERBOSE'
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'


class KillSignals(Enum):
    SIGKILL = '-9'
    SIGTERM = '-15'


class WakeupTomaOptions(Enum):
    WAKEUP_NONE = 'wakeup_none'
    WAKEUP_ONE = 'wakeup_one'
    WAKEUP_ALL = 'wakeup_all'


class DiskFormats(Enum):
    FORMAT_RAID = 'format_raid'
    FORMAT_EC = 'format_ec'
    NO_FORMAT_TYPE = 'format_none'


class DiskStatuses(Enum):
    OK = 'Ok'
    ERROR = 'Error'
    FORMAT_ERROR = 'Format_Error'
    EXCLUDED = 'Excluded'
    NOT_INITIALIZED = 'Not_Initialized'
    INGESTING = 'Ingesting'
    FROZEN = 'Frozen'
    FORMATTING = 'Formatting'
    INITIALIZING = 'Initializing'
    MISSING = 'Missing'


class FormatMetadataSize(Enum):
    EC_SIZE = 8
    RAID_SIZE = 0


class DiskVendors(Enum):
    HGST = 0x1c58
    Samsung = 0x144d
    Intel = 0x8086
    Micron = 0x1344


class SimulatorStatus(Enum):
    PASSED = 0
    GENERAL_ERROR = 1
    ILLEGAL_TEST_NAME = 2
    FAILING_TESTS = 3


class SimulatorTestStatus(Enum):
    PASSED = 0
    FAILED = 1


class SocketPathes(object):
    SOCKET_FILE_PATH = '/var/run/NVMesh/json_uds'


class ConnectPortStatus(Enum):
    UNRESOLVED = 'UNRESOLVED'
    FAILED = 'FAILED'  # at least one interface failed
    SUCCESS = 'SUCCESS'
    SKIPPED = 'SKIPPED'


class NetworkPortAction(Enum):
    CONNECT = ['Connection', 'connect']
    DISCONNECT = ['Disconnection', 'disconnect']


class NVMeshNodeType(Enum):
    CLIENT = 'clients'
    TARGET = 'servers'


class MongoDefaults(Enum):
    PORT = '27017'
    CONF_FILE = '/etc/mongod.conf'
    SERVICE_NAME = 'mongod'
    PID_FILE = '/var/run/mongodb/mongod.pid'
    LOCK_FILE = '/tmp/mongodb-{}.sock'


class TargetStatuses(Enum):
    OK = 'Ok'


class TargetHealth(Enum):
    HEALTHY = 'healthy'
    CRITICAL = 'critical'
    ALARM = 'alarm'


class CompilatorDefaults(Enum):
    BUILD_SCRIPT_NAME = 'build_client_server_rpms.py'
    COMPILE_SCRIPT_NAME = 'compile_for_kernel_and_ofed.sh'
    BLOCK_SIZE_OPTIONS = ['512B', '4k']


class EndpointRoutes(Enum):
    CLIENTS = 'clients'
    SERVERS = 'servers'
    SERVER_CLASSES = 'serverClasses'
    DISK_CLASSES = 'diskClasses'
    DISKS = 'disks'
    LOGS = 'logs'
    USERS = 'users'
    VOLUMES = 'volumes'
    VPGS = 'volumeProvisioningGroups'
    CONFIGURATION_PROFILE = 'configurationProfiles'
    GENERAL_SETTINGS = 'generalSettings'
    LOGIN = 'login'
    MONGO_DB = 'mongoDB'
    KEYS = 'keys'
    VolumeSecurityGroups = 'volumeSecurityGroups'
    NVMESH_METADATA = 'nvmeshMetadata'
    INDEX = '/'


class CLI(object):
    ITERATOR_THRESHOLD = 50
    RESULTS_ITERATOR_CONT = 'it'
    RESULTS_ITERATOR_QUIT = 'q'
    NVMESH_CLI_FILES_DIR = '~/.nvmesh_cli_files'
    API_SECRETS_FILE = '{}/nvmesh_api_secrets'.format(NVMESH_CLI_FILES_DIR)
    SSH_SECRETS_FILE = '{}/nvmesh_ssh_secrets'.format(NVMESH_CLI_FILES_DIR)
    HISTORY_FILE = '{}/nvmesh_cli_history'.format(NVMESH_CLI_FILES_DIR)
    DEFAULT_TIMEOUT = 60
    PERCENT_FROM_TIMEOUT_TO_VOLUME_POST_REQUEST = 0.8
    ERROR_CODE = 100
    CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class ControlJobs(Enum):
    SHUTDOWN_ALL = 'shutdownAll'
    ATTACH = 'toBeAttached'
    DETACH = 'toBeDetached'


class RAIDLevels(Enum):
    CONCATENATED = 'Concatenated'
    JBOD = 'LVM/JBOD'
    STRIPED_RAID_0 = 'Striped RAID-0'
    MIRRORED_RAID_1 = 'Mirrored RAID-1'
    STRIPED_AND_MIRRORED_RAID_10 = 'Striped & Mirrored RAID-10'
    ERASURE_CODING = 'Erasure Coding'
    ELECT = 'ELECT'

class VolumeTypes(Enum):
    WCV = 'WCV'
    MDV = 'MDV'
    QLC = 'QLC'

class VolumeDefaults(Enum):
    STRIPE_SIZE = 32
    NUMBER_OF_MIRRORS = 1
    EC_STRIPE_WIDTH = 1


class ScriptPaths(Enum):
    ATTACH_VOLUMES = '/usr/bin/nvmesh_attach_volumes'
    DETACH_VOLUMES = '/usr/bin/nvmesh_detach_volumes'
    NVMESH_TARGET = '/usr/bin/nvmesh_target'


class ControlJobsScriptCmds(Enum):
    ATTACH_VOLUMES = 'nvmesh_attach_volumes'
    DETACH_VOLUMES = 'nvmesh_detach_volumes'


class ReservationModes(Enum):
    NONE = 0
    SHARED_READ_ONLY = 1
    SHARED_READ_WRITE = 2
    EXCLUSIVE_READ_WRITE = 3
    INT_TO_MODE = {
        0: 'NONE',
        1: 'SHARED_READ_ONLY',
        2: 'SHARED_READ_WRITE',
        3: 'EXCLUSIVE_READ_WRITE'
    }


class AccessLevels(Enum):
    EXCLUSIVE_READ_WRITE = 'EXCLUSIVE_READ_WRITE'
    SHARED_READ_ONLY = 'SHARED_READ_ONLY'
    SHARED_READ_WRITE = 'SHARED_READ_WRITE'
