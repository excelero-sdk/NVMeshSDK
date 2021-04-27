from NVMeshSDK.Entities.GeneralSettings import GeneralSettings
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes
from NVMeshSDK.MongoObj import MongoObj


class GeneralSettingsAPI(BaseClassAPI):
    endpointRoute = EndpointRoutes.GENERAL_SETTINGS

    def getClusterName(self):
        """**Get Cluster Name**

            :return: tuple (err,out)

                **err**: HTTP error details or None if there were no errors

                **out**: list of cluster names
            :rtype: (dict, list)

            - Example::

                    from NVMeshSDK.APIs.GeneralSettingsAPI import GeneralSettingsAPI

                    generalSettingsAPI = GeneralSettingsAPI()

                    err, out = generalSettingsAPI.getClusterName()

                    >>> err
                    None
                    >>> for name in out: print name
                    {
                        "_id": "5f75d76e7a2828b50c08b76d",
                        "clusterName": "My cluster"
                    }

            - Expected HTTP Fail Response::

                >>> err
                {
                    'code': <Return Code>,
                    'content': <Failure Details>,
                    'message': <Failure Reason>
                }

                >>> out
                None
        """
        return self.get(projection=[MongoObj(field=GeneralSettings.ClusterName, value=1)])

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return GeneralSettings

    def get(self, page=None, count=None, projection=None, sort=None, filter=None):
        """**Get General Settings by projection**

        :param projection: Project before fetching using MongoDB filter objects, defaults to None
        :type projection: list, optional
        :return: tuple (err, out)

            **err**: HTTP error details or None if there were no errors

            **out**: list of generalSettings entities
        :rtype: (dict, list)

        - Example::

                from NVMeshSDK.APIs.GeneralSettingsAPI import GeneralSettingsAPI

                generalSettingsAPI = GeneralSettingsAPI()

                err, out = generalSettingsAPI.get()

                >>> err
                None
                >>> for generalSetting in out: print generalSetting
                {
                    {
                    "MAX_JSON_SIZE": 2,
                    "RESERVED_BLOCKS": 0.5,
                    "_id": "5fc79f5c33a875670367464f",
                    "autoLogOutThreshold": 3600,
                    "cacheUpdateInterval": 60,
                    "compatibilityMode": false,
                    "dateModified": "2021-01-11T15:12:44.614Z",
                    "daysBeforeLogEntryExpires": 30,
                    "debugComponents": {
                        "HA": true,
                        "client": false,
                        "counters": false,
                        "diskSegments": false,
                        "events": true,
                        "lock": true,
                        "statistics": false,
                        "updatePRaidStatus": false
                    },
                    "defaultDomain": "excelero.com",
                    "defaultUnitType": "decimal",
                    "domain": "@excelero.com",
                    "enableDistributedRAID": true,
                    "enableLegacyFormatting": false,
                    "enableMultiTenancy": false,
                    "enableNVMf": false,
                    "enableZones": false,
                    "fullClientReportInterval": 300,
                    "keepaliveGracePeriod": 300,
                    "loggingLevel": "VERBOSE",
                    "requestStatsInterval": 8,
                    "sendStatsInterval": 604800,
                    "statsCollectionSettings": {
                        "collectStatistics": false,
                        "limitToMachines": []
                    }
                }


            - Expected HTTP Fail Response::

                >>> err
                {
                    'code': <Return Code>,
                    'content': <Failure Details>,
                    'message': <Failure Reason>
                }

                >>> out
                None
        """
        return super(GeneralSettingsAPI, self).get(page=None, count=None, sort=None, filter=None, projection=projection)

    def update(self, generalSettings):
        """**Update general settings**

        :param generalSettings: GeneralSettings entity
        :type generalSettings: GeneralSettings
        :return: tuple (err, out)

            **err**: HTTP error details or None if there were no errors

            **out**: operation success details or None if there was an HTTP error
        :rtype: (dict, dict)

        - Example::

                from NVMeshSDK.APIs.GeneralSettingsAPI import GeneralSettingsAPI

                # updating the cluster name in general settings
                from NVMeshSDK.Entities.GeneralSettings import GeneralSettings
                from NVMeshSDK.MongoObj import MongoObj

                generalSettingsAPI = GeneralSettingsAPI()
                err, generalSettings = generalSettingsAPI.get(projection=[MongoObj(field=GeneralSettings.ClusterName, value=1)])
                generalSettings = generalSettings[0]
                >>> print generalSettings
                {
                    "_id": "6006e7c6f916fbe09845ddc1",
                    "clusterName": "a"
                }


                generalSettings.clusterName = "My Cluster"
                >>> print generalSettings
                {
                    "_id": "6006e7c6f916fbe09845ddc1",
                    "clusterName": "My Cluster"
                }

                err, out = generalSettingsAPI.update(generalSettings)

            - Expected Success Response::

                >>> err
                None

                >>> out
                {
                    u'_id': u'6006e7c6f916fbe09845ddc1',
                    u'error': None,
                    u'payload': {u'updated': {u'clusterName': u'My Cluster'}},
                    u'success': True
                }

            - Expected Operation Fail Response::

                >>> err
                None

                >>> out
                {
                    u'_id': u'6006e7c6f916fbe09845ddc1',
                    u'error': <Failure Reason>,
                    u'payload': None,
                    u'success': False
                }

            - Expected HTTP Fail Response::

                >>> err
                {
                    'code': <Return Code>,
                    'content': <Failure Details>,
                    'message': <Failure Reason>
                }

                >>> out
                None
        """
        return super(GeneralSettingsAPI, self).update(entitiesList=[generalSettings])

    def save(self, entitiesList, postTimeout=None):
        raise NotImplemented

    def count(self):
        return None, 1

    def delete(self, entitiesList, postTimeout=None):
        raise NotImplemented