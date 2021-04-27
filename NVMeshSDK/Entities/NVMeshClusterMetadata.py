#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity
from NVMeshSDK.Entities.AttributeRepresentation import AttributeRepresentation


class NVMeshClusterMetadata(Entity):
    """
    Static class attributes to use with MongoObj
        * Id
        * NeedReconfirm
        * UUID
    """
    Id = AttributeRepresentation(display='Cluster ID', dbKey='id')
    ClusterId = AttributeRepresentation(display='Cluster ID', dbKey='clusterID')
    NeedReconfirm = AttributeRepresentation(display='Reconfirm', dbKey='needReconfirm')
    UUID = AttributeRepresentation(display='UUID', dbKey='uuid')

    @Utils.initializer
    def __init__(self, _id=None, id=None, uuid=None, needReconfirm=None):
        """**Initializes NVMesh cluster metadata entity**

                :param _id: cluster mongo id, defaults to None
                :type _id: str, optional
                :param id: cluster id, defaults to None
                :type id: str, optional
                :param uuid: cluster uuid, defaults to None
                :type uuid: str, optional
        """
        pass
