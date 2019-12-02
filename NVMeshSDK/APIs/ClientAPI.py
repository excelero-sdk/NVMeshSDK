from NVMeshSDK.Entities.Client import Client
from NVMeshSDK.Entities.Volume import Volume
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes, ControlJobs


class ClientAPI(BaseClassAPI):

    endpointRoute = EndpointRoutes.CLIENTS
    controlJobsPayload = {
        '_id': '',
        'controlJobs': []
    }

    # # entity or id
    # def attach(self, volumes, client):
    #     return self.__setControlJobs(volumes, client, ControlJobs.ATTACH)
    #
    # # entity or id
    # def detach(self, volumes, client):
    #     return self.__setControlJobs(volumes, client, ControlJobs.DETACH)

    # entity or id
    def delete(self, clients):
        return self.makePost(routes=['delete'], objects={'Ids': self.getEntityIds(clients)})

    def save(self, entitiesList):
        raise NotImplemented

    def update(self, entitiesList):
        raise NotImplemented

    def __setControlJobs(self, volumes, client, controlJob):
        self.controlJobsPayload['_id'] = client._id if isinstance(client, Client) else client
        for volume in volumes:
            if isinstance(volume, Volume):
                uuid = volume._id
            else:
                uuid = volume
            self.controlJobsPayload['controlJobs'].append({'uuid': uuid, 'control': controlJob})

        err, out = self.makePost(routes=['setControlJobs'], objects=self.controlJobsPayload)
        self.controlJobsPayload['controlJobs'] = []
        return err, out

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return Client


