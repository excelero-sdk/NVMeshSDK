from NVMeshSDK.Entities.TargetClass import TargetClass
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes


class TargetClassAPI(BaseClassAPI):
    endpointRoute = EndpointRoutes.SERVER_CLASSES

    def get(self, filter=None, sort=None, projection=None):
        return super(TargetClassAPI, self).get(count=None, page=None, filter=filter, sort=sort, projection=projection)

    def count(self):
        raise NotImplemented

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return TargetClass
