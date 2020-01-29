from NVMeshSDK.Entities.Target import Target
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes


class TargetAPI(BaseClassAPI):
    endpointRoute = EndpointRoutes.SERVERS

    def deleteNicByIds(self, nicIds):
        return [self.makePost(routes=['deleteNIC'], objects={'nicID': nicId}) for nicId in nicIds]

    # entity or id
    def delete(self, targets):
        return self.makePost(routes=['delete'], objects={'Ids': self.getEntityIds(targets, idAttr='node_id')})

    def save(self, entitiesList):
        raise NotImplemented

    def update(self, entitiesList):
        raise NotImplemented

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return Target