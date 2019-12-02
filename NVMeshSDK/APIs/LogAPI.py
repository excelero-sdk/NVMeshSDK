from NVMeshSDK.Entities.Log import Log
from .BaseClassAPI import BaseClassAPI
from NVMeshSDK.Consts import EndpointRoutes

import json


class LogAPI(BaseClassAPI):
    endpointRoute = EndpointRoutes.LOGS

    def getAlerts(self, page=0, count=0, filterObj={}, sortObj={}):
        routes = ['alerts', '{0}', '{1}?filter={2}&sort={3}'.format(page, count, json.dumps(filterObj), json.dumps(sortObj))]
        err, out = self.makeGet(routes)

        if out is not None:
            return [self.getType()(**result) for result in out]
        else:
            return err

    def acknowledgeAll(self):
        return self.makePost(routes=['acknowledgeAll'], objects={})

    # entity or id
    def acknowledgeLogs(self, logs):
        return [self.makePost(routes=['acknowledge'], objects={'id': logId}) for logId in self.getEntityIds(logs)]

    def countAlerts(self):
        return self.makeGet(routes=['alerts', 'count'])

    def save(self, entitiesList):
        raise NotImplemented

    def update(self, entitiesList):
        raise NotImplemented

    def delete(self, entitiesList):
        raise NotImplemented

    @classmethod
    def getEndpointRoute(cls):
        return cls.endpointRoute

    def getType(self):
        return Log