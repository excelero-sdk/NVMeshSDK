from NVMeshSDK.Entities.Drive import Drive
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes


class DriveAPI(BaseClassAPI):
    endpointRoute = EndpointRoutes.DISKS

    # entity or id
    def deleteDrives(self, drives):
        return self.makePost(routes=['delete'], objects={'Ids': self.getEntityIds(drives, idAttr='diskID')})

    # entity or id
    def evictDrives(self, drives):
        return self.makePost(routes=['evictDiskByDiskIds'], objects={'Ids': self.getEntityIds(drives, idAttr='diskID')})

    # entity or id
    def formatDrives(self, drives, formatType=None):
        driveIds = self.getEntityIds(drives, idAttr='diskID')
        payload = {'diskIDs': driveIds}

        if formatType is not None:
            payload.update({'formatType': formatType})

        return self.makePost(routes=['formatDiskByDiskIds'], objects=payload)

    def save(self, entitiesList):
        raise NotImplemented

    def update(self, entitiesList):
        raise NotImplemented

    def count(self):
        raise NotImplemented

    def delete(self, entitiesList):
        raise NotImplemented

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return Drive