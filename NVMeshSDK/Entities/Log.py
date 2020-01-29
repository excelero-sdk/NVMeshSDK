#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity


class Log(Entity):
    @Utils.initializer
    def __init__(self, _id=None, timestamp=None, level=None, message=None, rawMessage=None, meta=None, acknowledgedBy=None, dateModified=None):
        pass
