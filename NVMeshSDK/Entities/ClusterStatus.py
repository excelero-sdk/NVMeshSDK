#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity
from NVMeshSDK.Entities.TargetsStatus import TargetsStatus
from NVMeshSDK.Entities.ClientsStatus import ClientsStatus
from NVMeshSDK.Entities.AttributeRepresentation import AttributeRepresentation


class ClusterStatus(Entity):
    Targets = AttributeRepresentation(display='Targets', dbKey='servers', type=TargetsStatus)
    Clients = AttributeRepresentation(display='Clients', dbKey='clients', type=ClientsStatus)
    Volumes = AttributeRepresentation(display='Volumes', dbKey='volumes')
    TotalSpace = AttributeRepresentation(display='Total Space', dbKey='totalSpace')
    AllocatedSpace = AttributeRepresentation(display='Allocated Space', dbKey='allocatedSpace')
    FreeSpace = AttributeRepresentation(display='Free Space', dbKey='freeSpace')

    __objectsToInstantiate = ['Targets', 'Clients']

    @Utils.initializer
    def __init__(self, servers=None, clients=None, volumes=None, totalSpace=None, allocatedSpace=None, freeSpace=None,
                 errors=None, warnings=None):
        pass

    def getObjectsToInstantiate(self):
        return ClusterStatus.__objectsToInstantiate
