#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity
from NVMeshSDK.Entities.AttributeRepresentation import AttributeRepresentation


class TargetClass(Entity):
    Id = AttributeRepresentation(display='Name', dbKey='name')
    Description = AttributeRepresentation(display='Description', dbKey='description')
    TargetNodes = AttributeRepresentation(display='Targets', dbKey='targetNodes')
    DateModified = AttributeRepresentation(display='Date Modified', dbKey='dateModified')
    ModifiedBy = AttributeRepresentation(display='Modified By', dbKey='modifiedBy')
    Domains = AttributeRepresentation(display='Domains', dbKey='domains')

    @Utils.initializer
    def __init__(self, name, targetNodes, _id=None, description=None, domains=None,
                 modifiedBy=None, createdBy=None, dateModified=None, dateCreated=None, servers=None, index=None):
        self._id = self.name


