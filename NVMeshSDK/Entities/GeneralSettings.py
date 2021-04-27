#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity
from NVMeshSDK.Entities.AttributeRepresentation import AttributeRepresentation


class GeneralSettings(Entity):
    """
    Static class attributes to use with MongoObj
        * Id
        * ClusterName
        * MaxJsonSize
        * ReservedBlocks
        * AutoLogOutThreshold
        * CacheUpdateInterval
        * CompatibilityMode
        * DateModified
        * DaysBeforeLogEntryExpires
        * DebugComponents
        * Domain
        * EnableDistributedRAID
        * EnableLegacyFormatting
        * EnableZones
        * FullClientReportInterval
        * KeepaliveGracePeriod
        * LoggingLevel
        * RequestStatsInterval
        * sendStatsInterval
        * StatsCollectionSettings
        * EnableNVMf
        * EnableMultiTenancy
        * DefaultUnitType

    """
    Id = AttributeRepresentation(display='ID', dbKey='_id')
    ClusterName = AttributeRepresentation(display='Cluster Name', dbKey='clusterName')
    MaxJsonSize = AttributeRepresentation(display='Max JSON Size', dbKey='MAX_JSON_SIZE')
    ReservedBlocks = AttributeRepresentation(display='Reserved Blocks', dbKey='RESERVED_BLOCKS')
    AutoLogOutThreshold = AttributeRepresentation(display='Auto Log Out Threshold', dbKey='autoLogOutThreshold')
    CacheUpdateInterval = AttributeRepresentation(display='Cache Update Interval', dbKey='cacheUpdateInterval')
    CompatibilityMode = AttributeRepresentation(display='Compatibility Mode', dbKey='compatibilityMode')
    DateModified = AttributeRepresentation(display='Date Modified', dbKey='dateModified')
    DaysBeforeLogEntryExpires = AttributeRepresentation(display='Days Before Log Entry Expires', dbKey='daysBeforeLogEntryExpires')
    DebugComponents = AttributeRepresentation(display='Debug Components', dbKey='debugComponents')
    Domain = AttributeRepresentation(display='Domain', dbKey='domain')
    EnableDistributedRAID = AttributeRepresentation(display='Enable Distributed RAID', dbKey='enableDistributedRAID')
    EnableLegacyFormatting = AttributeRepresentation(display='Enable Legacy Formatting', dbKey='enableLegacyFormatting')
    EnableZones = AttributeRepresentation(display='Enable Zones', dbKey='enableZones')
    FullClientReportInterval = AttributeRepresentation(display='Full Client Report Interval', dbKey='fullClientReportInterval')
    FullTomaReportInterval = AttributeRepresentation(display='Full Toma Report Interval', dbKey='fullTomaReportInterval')
    KeepaliveGracePeriod = AttributeRepresentation(display='Keepalive Grace Period', dbKey='keepaliveGracePeriod')
    LoggingLevel = AttributeRepresentation(display='Logging Level', dbKey='loggingLevel')
    RequestStatsInterval = AttributeRepresentation(display='Request Statistics Interval', dbKey='requestStatsInterval')
    sendStatsInterval = AttributeRepresentation(display='Send Statistics Interval', dbKey='sendStatsInterval')
    StatsCollectionSettings = AttributeRepresentation(display='Statistics Collection Settings', dbKey='statsCollectionSettings')
    EnableNVMf = AttributeRepresentation(display='Enable NVMf', dbKey='enableNVMf')
    EnableMultiTenancy = AttributeRepresentation(display='Enable Multi Tenancy', dbKey='enableMultiTenancy')
    DefaultUnitType = AttributeRepresentation(display='Default Unit Type', dbKey='defaultUnitType')

    @Utils.initializer
    def __init__(self, _id=None, clusterName=None, MAX_JSON_SIZE=None, RESERVED_BLOCKS=None, autoLogOutThreshold=None,
                 cacheUpdateInterval=None, compatibilityMode=None, dateModified=None, daysBeforeLogEntryExpires=None,
                 debugComponents=None, domain=None, enableDistributedRAID=None, enableLegacyFormatting=None, enableZones=None,
                 fullClientReportInterval=None, fullTomaReportInterval=None, keepaliveGracePeriod=None, loggingLevel=None, requestStatsInterval=None,
                 sendStatsInterval=None, statsCollectionSettings=None, enableNVMf=None, enableMultiTenancy=None, defaultUnitType=None):
        """**Initializes volume entity**

                :param _id: general setting's id, defaults to None
                :type _id: str, optional
                :param clusterName: the name of the cluster
                :type clusterName: str, optional
                :param MAX_JSON_SIZE: The size of the largest JSON message supported by the Management Server
                :type MAX_JSON_SIZE: int, optional
                :param RESERVED_BLOCKS: The percentage of reserved blocks at the start of a managed NVMe device
                :type RESERVED_BLOCKS: int, optional
                :param autoLogOutThreshold: The timeout of the GUI and API access (in milliseconds). After the timeout expires the GUI and API will automatically logout all logged in users
                :type autoLogOutThreshold: int, optional
                :param cacheUpdateInterval: The grace period, in milliseconds, since the last message from every component. When the grace period is over, the management server will declare that component as timedOut
                :type cacheUpdateInterval: int, optional
                :param compatibilityMode: Use the NVMesh version of dynamic libraries instead of the operating system versions to avoid compatibility issues
                :type compatibilityMode: bool, optional
                :param daysBeforeLogEntryExpires: The number of days the management logs are kept before rotation
                :type daysBeforeLogEntryExpires: int, optional
                :param debugComponents: List of debugComponents to turn in in logs
                :type debugComponents: dict, optional
                :param domain: The default domain
                :type domain: str, optional
                :param enableDistributedRAID: This option only affects the creation of EC volumes via the GUI, it does not affect creating EC volumes via RESTful API
                :type enableDistributedRAID: bool, optional
                :param enableLegacyFormatting: Determines whether to allow legacy formatting on metadata supported drives via the RESTful API
                :type enableLegacyFormatting: bool, optional
                :param enableZones: Enable zones
                :type enableZones: bool, optional
                :param fullClientReportInterval: The frequency of a full client report from the node machines to the management server
                :type fullClientReportInterval: int, optional
                :param keepaliveGracePeriod: The grace period, in milliseconds, since the last message from every component. When the grace period is over, the management server will declare that component as timedOut
                :type keepaliveGracePeriod: int, optional
                :param loggingLevel: The logging level of the Management Server, options: NONE, INFO, VERBOSE, DEBUG, ERROR, WARNING.
                :type loggingLevel: str, optional
                :param requestStatsInterval: The frequency of statistics updates from the node machines to the management server
                :type requestStatsInterval: int, optional
                :param sendStatsInterval: The interval of time passing after which the "phone home" statistics should be sent to excelero in ms
                :type sendStatsInterval: int, optional
                :param statsCollectionSettings: Cluster statistics
                :type statsCollectionSettings: dict, optional
                :param enableNVMf: Set default value of Enable NVMf for volume creation
                :type enableNVMf: bool, optional
                :param enableMultiTenancy: Set default value of Enable NVMf for volume creation
                :type enableMultiTenancy: bool, optional
                :param defaultUnitType: Set default unit type value (binary/decimal)
                :type defaultUnitType: str, optional
        """
        pass
