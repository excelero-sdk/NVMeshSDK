#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity
from NVMeshSDK.Entities.Drive import Drive
from NVMeshSDK.Entities.NIC import NIC
from NVMeshSDK.Entities.AttributeRepresentation import AttributeRepresentation


class Target(Entity):

    Id = AttributeRepresentation(display='Name', dbKey='node_id')
    Drives = AttributeRepresentation(display='Drives', dbKey='disks', type=Drive)
    Nics = AttributeRepresentation(display='NICs', dbKey='nics', type=NIC)
    Version = AttributeRepresentation(display='Version', dbKey='version')
    Health = AttributeRepresentation(display='Health', dbKey='health')
    TomaStatus = AttributeRepresentation(display='TOMA Status', dbKey='tomaStatus')
    __objectsToInstantiate = ['Drives', 'Nics']

    @Utils.initializer
    def __init__(self, _id=None, branch=None, disks=None, nics=None, node_status=None, version=None, node_id=None,
                 commit=None, messageSequence=None, connectionSequence=None, dateModified=None, health=None,
                 cpu_load=None, cpu_temp=None, uuid=None, tomaStatus=None, wsStatus=None):
        pass

    def getObjectsToInstantiate(self):
        return Target.__objectsToInstantiate


