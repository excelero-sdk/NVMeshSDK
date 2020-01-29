#!/usr/bin/env python
from NVMeshSDK.Utils import Utils
from NVMeshSDK.Entities.Entity import Entity


class User(Entity):
    @Utils.initializer
    def __init__(self, email, role, notificationLevel, password=None,_id=None, layout=None, relogin=False, modifiedBy=None, createdBy=None,
                 eulaDateOfSignature=None, eulaSignature=None, hasAcceptedEula=None, dateModified=None, dateCreated=None):
        self._id = email
        if hasattr(self, 'password'):
            self.confirmationPassword = self.password

