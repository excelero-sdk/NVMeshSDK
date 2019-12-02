from NVMeshSDK.ConnectionManager import ConnectionManager, ConnectionManagerError
from NVMeshSDK.Entities.Entity import Entity
from NVMeshSDK.Utils import Utils


class BaseClassAPI(object):
    def __init__(self, user=None, password=None):
        try:
            if user is not None and password is not None:
                self.managementConnection = ConnectionManager.getInstance(user=user, password=password)
            else:
                self.managementConnection = ConnectionManager.getInstance()
        except ConnectionManagerError as e:
            raise e

    @classmethod
    def getEndpointRoute(cls):
        pass

    def get(self, page=0, count=0, filter=None, sort=None, projection=None):
        routes = ['all']
        query = Utils.buildQueryStr({'filter': filter, 'sort': sort, 'projection': projection})

        if page is None and count is None:
            routes[0] += query
        else:
            routes += ['{0}'.format(page), '{0}{1}'.format(count, query)]

        err, out = self.makeGet(routes)

        if out is not None:
            enteties = [self.getType()(**result) for result in out]
            for entity in enteties:
                entity.deserialize()
            return None, enteties
        else:
            return err, None

    def count(self):
        return self.makeGet(['count'])

    def save(self, entitiesList):
        return self.makePost(['save'], entitiesList)

    def update(self, entitiesList):
        return self.makePost(['update'], entitiesList)

    # calling delete from here indicates that delete eventually expects a list of id objects
    # if overridden in the child then delete expects a list of string ids
    # either way the sdk method will accept both
    def delete(self, entitiesList):
        if not isinstance(entitiesList[0], self.getType()):
            entitiesList = self.getEntitesFromIds(entitiesList)

        return self.makePost(['delete'], entitiesList)

    def makePost(self, routes, objects):
        isObjects = [issubclass(obj.__class__, Entity) for obj in objects]
        if all(isObjects):
            payload = [obj.serialize() for obj in objects]
        else:
            payload = objects

        try:
            err, out = self.managementConnection.post('/{0}/{1}'.format(self.getEndpointRoute(), '/'.join(routes)), payload)
            return err, out
        except ConnectionManagerError as e:
            raise e


    def makeGet(self, routes):
        try:
            err, out = self.managementConnection.get('/{0}/{1}'.format(self.getEndpointRoute(), '/'.join(routes)))
            return err, out
        except ConnectionManagerError as e:
            raise e

    def getEntityIds(self, entities, idAttr='_id'):
        if isinstance(entities[0], self.getType()):
            entityIds = [getattr(entity, idAttr) for entity in entities]
        else:
            entityIds = entities

        return entityIds

    def getEntitesFromIds(self, ids, idAttr='_id'):
        return [{idAttr: id} for id in ids]

    def getType(self):
        pass
