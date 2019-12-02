from NVMeshSDK.Entities.ClusterStatus import ClusterStatus
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes


class StatusAPI(BaseClassAPI):

    endpointRoute = EndpointRoutes.INDEX

    def status(self):
        routes = ['status']

        err, out = self.makeGet(routes)

        if out is not None:
            status = self.getType()(**out)
            status.deserialize()
            return None, status
        else:
            return err, None

    def get(self, page=0, count=0, filter=None, sort=None, projection=None):
        raise NotImplemented

    def delete(self, clients):
        raise NotImplemented

    def save(self, entitiesList):
        raise NotImplemented

    def update(self, entitiesList):
        raise NotImplemented

    def count(self):
        raise NotImplemented

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return ClusterStatus