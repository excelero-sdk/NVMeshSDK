from NVMeshSDK.Entities.DriveClass import DriveClass
from NVMeshSDK.Entities.Drive import Drive
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes


class DriveClassAPI(BaseClassAPI):
    endpointRoute = EndpointRoutes.DISK_CLASSES

    def get(self, projection=None, filter=None, sort=None):
        return super(DriveClassAPI, self).get(page=None, count=None, projection=projection, filter=filter, sort=sort)

    def save(self, driveClasses):
        for driveClass in driveClasses:
            if not isinstance(driveClass.disks[0], Drive):
                drives = self.getEntitesFromIds(ids=driveClass.disks, idAttr=Drive.Id.dbKey)
                setattr(driveClass, DriveClass.Drives.dbKey, drives)

        return self.makePost(['save'], driveClasses)

    def count(self):
        raise NotImplemented

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return DriveClass
