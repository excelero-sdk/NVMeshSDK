#!/usr/bin/env python
import json
from NVMeshSDK.Utils import Utils
import copy


class Entity(object):

    def __str__(self):
        dictCopy = copy.deepcopy(self.__dict__)
        try:
            del dictCopy['_{0}__objectsToInstantiate'.format(self.__class__.__name__)]
        except KeyError:
            pass
        return json.dumps(dictCopy, sort_keys=True, indent=4, default=lambda x: x.__dict__)

    def __getattribute__(self, item):
        if '.' in item:
            parts = item.split('.')
            array = Entity.__getattribute__(self, parts[0])
            return [getattr(a, parts[1]) for a in array]
        else:
            return object.__getattribute__(self, item)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            selfDict = Entity.myToDict(self)
            otherDict = Entity.myToDict(other)
            return selfDict == otherDict

        return False

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self._id < other._id

        return False

    @staticmethod
    def myToDict(obj):
        return json.loads(json.dumps(obj.__dict__ if not isinstance(obj, dict) else obj, default=lambda x: x.__dict__))

    def serialize(self):
        return Entity.myToDict(self.convertStrToCapacityBytes(self.filterNoneValues()))

    def deserialize(self):
        self.instantiate()

    def instantiate(self):
        for obj in self.getObjectsToInstantiate():
            entityRep = getattr(self, obj)
            if hasattr(self, entityRep.dbKey):
                attrValue = getattr(self, entityRep.dbKey)
                if isinstance(attrValue, list):
                    listOfInstances = []
                    for element in attrValue:
                        element = entityRep.type(**element)
                        listOfInstances.append(element.instantiate() if element.getObjectsToInstantiate() != [] else element)

                    setattr(self, entityRep.dbKey, listOfInstances)
                else:
                    setattr(self, entityRep.dbKey, entityRep.type(**attrValue)) #entityRep.dbKey))
        return self

    def convertStrToCapacityBytes(self, serializedObj):
        if 'capacity' in serializedObj:
            serializedObj['capacity'] = Utils.convertUnitToBytes(serializedObj['capacity'])

        return serializedObj

    def filterNoneValues(self):
        return {k: v for k, v in self.__dict__.iteritems() if v is not None}

    def getObjectsToInstantiate(self):
        return []
