from NVMeshSDK.Entities.User import User
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes


class UserAPI(BaseClassAPI):
    endpointRoute = EndpointRoutes.USERS

    def get(self, filter=None, sort=None):
        return super(UserAPI, self).get(page=None, count=None, filter=filter, sort=sort)

    def resetPassword(self, users):
        for user in users:
            user.resetPassword = True

        return self.makePost(['update'], users)

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return User