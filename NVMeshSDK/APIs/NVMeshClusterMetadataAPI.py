from NVMeshSDK.Entities.NVMeshClusterMetadata import NVMeshClusterMetadata
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes


class NVMeshClusterMetadataAPI(BaseClassAPI):
    endpointRoute = EndpointRoutes.NVMESH_METADATA

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return NVMeshClusterMetadata

    def get(self, page=None, count=None, projection=None, sort=None, filter=None):
        return super(NVMeshClusterMetadataAPI, self).get(route=['clusterID'], page=None, count=None, sort=None, filter=None, projection=projection)

    def updateClusterID(self, clusterID):
        return self.makePost(['updateClusterID'], {'clusterID': clusterID})

    def save(self, entitiesList, postTimeout=None):
        raise NotImplemented

    def count(self):
        return None, 1

    def delete(self, entitiesList, postTimeout=None):
        raise NotImplemented