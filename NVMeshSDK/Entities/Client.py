#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity
from NVMeshSDK.Entities.AttributeRepresentation import AttributeRepresentation
from NVMeshSDK.Entities.BlockDevice import BlockDevice


class Client(Entity):
    Id = AttributeRepresentation(display='Name', dbKey='_id')
    Version = AttributeRepresentation(display='Version', dbKey='version')
    Health = AttributeRepresentation(display='Health', dbKey='health')
    BlockDevices = AttributeRepresentation(display='Volume Attachments', dbKey='block_devices', type=BlockDevice)
    __objectsToInstantiate = ['BlockDevices']

    @Utils.initializer
    def __init__(self, _id=None, branch=None, configuration_version=None, client_status=None, block_devices=None, version=None, clientID=None, controlJobs=None,
                 commit=None, messageSequence=None, connectionSequence=None, dateModified=None, health=None, health_old=None, managementAgentStatus=None):
        pass

    def getObjectsToInstantiate(self):
        return Client.__objectsToInstantiate
