from NVMeshSDK.Entities.Target import Target
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes


class TargetAPI(BaseClassAPI):
    """**All the functions of the Target API are defined here**"""
    endpointRoute = EndpointRoutes.SERVERS

    def get(self, page=0, count=0, filter=None, sort=None, projection=None):
        """**Get targets by page and count, limit the result using filter, sort and projection**

        :param page: The page to fetch, defaults to 0
        :type page: int, optional
        :param count: Number of records per page, defaults to 0
        :type count: int, optional
        :param filter: Filter before fetching using MongoDB filter objects, defaults to None
        :type filter: list, optional
        :param sort: Sort before fetching using MongoDB filter objects, defaults to None
        :type sort: list, optional
        :param projection: Project before fetching using MongoDB filter objects, defaults to None
        :type projection: list, optional
        :return: tuple (err, out)

            **err**: HTTP error details or None if there were no errors

            **out**: list of Target entities
        :rtype: (dict, list)

        - Example::

                from NVMeshSDK.APIs.TargetAPI import TargetAPI

                # fetching all the targets
                targetAPI = TargetAPI()
                err, out = targetAPI.get()

                >>> err
                None
                >>> for target in out: print target
                {
                    "_id": "nvme71_00000000000000000",
                    "dateModified": "2019-07-07T12:03:57.454Z",
                    "disks": [
                        {
                            "diskID": "S3HCNX0K800805.1"
                        },
                        {
                            "diskID": "S3HCNX0K800807.1"
                        },
                        {
                            "diskID": "S3P8NY0J700135.1"
                        },
                        {
                            "diskID": "S3HCNX0K800137.1"
                        }
                    ],
                    "health": "healthy",
                    "nics": [
                        {
                            "nicID": "0x00000000000000000000ffff0a016447"
                        },
                        {
                            "nicID": "0x00000000000000000000ffff0a019647"
                        }
                    ],
                    "node_id": "nvme71",
                    "node_status": 1,
                    "tomaStatus": "up",
                    "version": "1.3.1-659",
                    "wsStatus": "connected"
                }
                {
                    "_id": "nvme77_00000000000000000",
                    "dateModified": "2019-07-07T12:04:01.458Z",
                    "disks": [
                        {
                            "diskID": "S3P8NY0J800090.1"
                        },
                        {
                            "diskID": "S3HCNX0JC02023.1"
                        },
                        {
                            "diskID": "S3HCNX0K800875.1"
                        },
                        {
                            "diskID": "S3HCNX0K800811.1"
                        }
                    ],
                    "health": "healthy",
                    "nics": [
                        {
                            "nicID": "0x00000000000000000000ffff0a01644d"
                        },
                        {
                            "nicID": "0x00000000000000000000ffff0a01964d"
                        }
                    ],
                    "node_id": "nvme77",
                    "node_status": 1,
                    "tomaStatus": "up",
                    "version": "1.3.1-659",
                    "wsStatus": "connected"
                }

                # fetching all targets and projecting only the id of each target using MongoObj and Target's class attribute
                from NVMeshSDK.Entities.Target import Target
                from NVMeshSDK.MongoObj import MongoObj
                err, out = targetAPI.get(projection=[MongoObj(field=Target.Id, value=1)])

                >>> err
                None
                >>> for target in out: print target
                {
                    "_id": "nvme77"
                }
                {
                    "_id": "nvme71"
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
        return super(TargetAPI, self).get(page=page, count=count, filter=filter, sort=sort, projection=projection)

    def deleteNicByIds(self, nicIds):
        """**Delete specific NICs by IDs. --NIC can only be deleted if its status is Missing**

        :param nicIds: list of nic ids
        :type nicIds: list
        :return: tuple (err, out)

            **err**: HTTP error details or None if there were no errors

            **out**: operation success details per entity or None if there was an HTTP error
        :rtype: (dict, list)

        - Example::

                from NVMeshSDK.APIs.TargetAPI import TargetAPI

                # deleting 2 NICs using their ids
                targetAPI = TargetAPI()
                err, out = targetAPI.deleteNicByIds(["0x00000000000000000000ffffc0a8640a", "0x00000000000000000000ffffc0a8c80a"])

            - Expected Success Response::

                >>> err
                None

                >>> out
                [
                    {
                        u'_id': u'0x00000000000000000000ffffc0a8640a',
                        u'error': None,
                        u'payload': None,
                        u'success': True
                    },
                    {
                        u'_id': u'0x00000000000000000000ffffc0a8c80a',
                        u'error': None,
                        u'payload': None,
                        u'success': True
                    }
                ]

            - Expected Operation Fail Response::

                >>> err
                None

                >>> out
                [
                    {
                        u'_id': u'0x00000000000000000000ffffc0a8640a',
                        u'error': <Failure Reason>,
                        u'payload': None,
                        u'success': False
                    },
                    {
                        u'_id': u'0x00000000000000000000ffffc0a8c80a',
                        u'error': <Failure Reason>,
                        u'payload': None,
                        u'success': False
                    }
                ]

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
        return [self.makePost(routes=['deleteNIC'], objects={'nicID': nicId}) for nicId in nicIds]

    # entity or id
    def delete(self, targets):
        """**Delete targets. --Target won't be deleted if a volume is dependent on it.**

        :param targets: list of targets ids or Target entities
        :type targets: list
        :return: tuple (err, out)

            **err**: HTTP error details or None if there were no errors

            **out**: operation success details per entity or None if there was an HTTP error
        :rtype: (dict, list)

        - Example::

                from NVMeshSDK.APIs.TargetAPI import TargetAPI

                # deleting 2 targets using their ids
                targetAPI = TargetAPI()
                err, out = targetAPI.delete(['nvme77','nvme71'])

                # deleting all targets, first using the 'get' method to get all the targets
                # as target entities list then passing it to the 'delete' method
                err, currentTargets = targetAPI.get()
                err, out = targetAPI.delete(currentTargets)

            - Expected Success Response::

                >>> err
                None

                >>> out
                [
                    {
                        u'_id': u'nvme77',
                        u'error': None,
                        u'payload': None,
                        u'success': True
                    },
                    {
                        u'_id': u'nvme71',
                        u'error': None,
                        u'payload': None,
                        u'success': True
                    }
                ]

            - Expected Operation Fail Response::

                >>> err
                None

                >>> out
                [
                    {
                        u'_id': u'nvme77',
                        u'error': <Failure Reason>,
                        u'payload': None,
                        u'success': False
                    },
                    {
                        u'_id': u'nvme71',
                        u'error': <Failure Reason>,
                        u'payload': None,
                        u'success': False
                    }
                ]

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
        return self.makePost(routes=['delete'], objects={'Ids': self.getEntityIds(targets, idAttr='node_id')})

    def count(self):
        """**Get total targets count.**

        :return: targets count
        :rtype: int

            - Example::

                from NVMeshSDK.APIs.TargetAPI import TargetAPI

                targetAPI = TargetAPI()
                err, out = targetAPI.count()

                >>> err
                None
                >>> out
                2

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
        return super(TargetAPI, self).count()

    def save(self, entitiesList):
        raise NotImplemented

    def update(self, entitiesList):
        raise NotImplemented

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return Target