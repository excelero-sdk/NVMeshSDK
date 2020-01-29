from NVMeshSDK.Entities.Volume import Volume
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes


class VolumeAPI(BaseClassAPI):
    endpointRoute = EndpointRoutes.VOLUMES

    # entity or id
    def rebuildVolumes(self, volumes):
        return self.makePost(routes=['rebuildVolumes'], objects=self.getEntityIds(volumes))

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return Volume
