#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity
from NVMeshSDK.Entities.Chunk import Chunk
from NVMeshSDK.Entities.AttributeRepresentation import AttributeRepresentation


class Volume(Entity):
    Id = AttributeRepresentation(display='Name', dbKey='name')
    Health = AttributeRepresentation(display='Health', dbKey='health')
    Description = AttributeRepresentation(display='Description', dbKey='description')
    Status = AttributeRepresentation(display='Status', dbKey='status')
    RaidLevel = AttributeRepresentation(display='RAID Level', dbKey='RAIDLevel')
    ParityBlocks = AttributeRepresentation(display='Parity', dbKey='parityBlocks')
    DataBlocks = AttributeRepresentation(display='Data', dbKey='dataBlocks')
    Protection = AttributeRepresentation(display='Protection Level', dbKey='protectionLevel')
    Size = AttributeRepresentation(display='Size', dbKey='capacity')
    StripeWidth = AttributeRepresentation(display='Stripe Width', dbKey='stripeWidth')
    TargetClasses = AttributeRepresentation(display='Target Classes', dbKey='serverClasses')
    DriveClasses = AttributeRepresentation(display='Drive Classes', dbKey='diskClasses')
    Domain = AttributeRepresentation(display='Domain', dbKey='domain')
    RelativeRebuildPriority = AttributeRepresentation(display='Relative Rebuild Priority', dbKey='relativeRebuildPriority')
    Chunks = AttributeRepresentation(display='Chunks', dbKey='chunks', type=Chunk)
    __objectsToInstantiate = ['Chunks']

    @Utils.initializer
    def __init__(self, name=None, RAIDLevel=None, capacity=None, VPG=None, _id=None, relativeRebuildPriority=None, description=None, diskClasses=None, serverClasses=None,
                 limitByDisks=None, limitByNodes=None, numberOfMirrors=None, createdBy=None, modifiedBy=None, dateModified=None, dateCreated=None, isReserved=None,
                 status=None, blocks=None, chunks=None, stripeSize=None, stripeWidth=None, dataBlocks=None, parityBlocks=None, protectionLevel=None, domain=None,
                 uuid=None, blockSize=None, version=None, type=None, health=None, lockServer=None):
        if hasattr(self, 'name'):
            self._id = self.name

    def getObjectsToInstantiate(self):
        return Volume.__objectsToInstantiate