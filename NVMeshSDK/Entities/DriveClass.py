#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity
from NVMeshSDK.Entities.Drive import Drive
from NVMeshSDK.Entities.AttributeRepresentation import AttributeRepresentation


class DriveClass(Entity):
    Id = AttributeRepresentation(display='Name', dbKey='_id')
    Description = AttributeRepresentation(display='Description', dbKey='description')
    Drives = AttributeRepresentation(display='Drives', dbKey='disks', type=Drive)
    DateModified = AttributeRepresentation(display='Date Modified', dbKey='dateModified')
    ModifiedBy = AttributeRepresentation(display='Modified By', dbKey='modifiedBy')
    Domains = AttributeRepresentation(display='Domains', dbKey='domains')
    __objectsToInstantiate = ['Drives']

    @Utils.initializer
    def __init__(self, _id, disks, description=None, tags=None, modifiedBy=None, createdBy=None, dateModified=None, dateCreated=None, domains=None):
        pass

    def getObjectsToInstantiate(self):
        return DriveClass.__objectsToInstantiate
