#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity
from NVMeshSDK.Entities.AttributeRepresentation import AttributeRepresentation


class VPG(Entity):
    Id = AttributeRepresentation(display='Name', dbKey='name')
    Size = AttributeRepresentation(display='Reserved Space', dbKey='capacity')
    Description = AttributeRepresentation(display='Description', dbKey='description')
    RaidLevel = AttributeRepresentation(display='RAID Level', dbKey='RAIDLevel')

    @Utils.initializer
    def __init__(self, name=None, RAIDLevel=None, capacity=None, VPG=None, _id=None, relativeRebuildPriority=10, description=None, diskClasses=None, serverClasses=None,
                 limitByDisks=None, limitByNodes=None, numberOfMirrors=None, createdBy=None, modifiedBy=None, dateModified=None, dateCreated=None, isReserved=None,
                 status=None, blocks=None, chunks=None, stripeSize=None, stripeWidth=None, dataBlocks=None, parityBlocks=None, protectionLevel=None, domain=None,
                 uuid=None, blockSize=None, version=None, type=None, health=None, lockServer=None, serviceResources='RDDA', isDefault=None):
        if hasattr(self, '_id'):
            self.name = self._id
