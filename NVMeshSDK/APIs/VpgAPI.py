from NVMeshSDK.Entities.VPG import VPG
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes


class VpgAPI(BaseClassAPI):
    endpointRoute = EndpointRoutes.VPGS

    def get(self, filter=None, sort=None, projection=None):
        return super(VpgAPI, self).get(page=None, count=None, filter=filter, sort=sort, projection=projection)

    def update(self, entitiesList):
        raise NotImplemented

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return VPG
