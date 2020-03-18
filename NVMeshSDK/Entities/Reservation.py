#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity
from NVMeshSDK.Entities.AttributeRepresentation import AttributeRepresentation


class Reservation(Entity):
    Mode = AttributeRepresentation(display='Mode', dbKey='mode')
    Version = AttributeRepresentation(display='Version', dbKey='version')
    ReservedBy = AttributeRepresentation(display='ReservedBy', dbKey='reservedBy')

    @Utils.initializer
    def __init__(self, mode=None, version=None, reservedBy=None):
        pass
