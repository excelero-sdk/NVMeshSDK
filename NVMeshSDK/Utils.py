#!/usr/bin/env python
from functools import wraps
import inspect
import json


class Utils:

    @staticmethod
    def initializer(func):
        argSpec = inspect.getargspec(func)
        names, varargs, keywords, defaults = argSpec

        @wraps(func)
        def wrapper(self, *args, **kargs):
            for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
                if name in names:
                    setattr(self, name, arg)

            for name, default in zip(reversed(names), reversed(defaults)):
                if not hasattr(self, name):
                    if default is not None:
                        setattr(self, name, default)

            filteredKargs = {k: v for k, v in kargs.iteritems() if k in names}
            func(self, *args, **filteredKargs)

        wrapper.argSpec = argSpec

        return wrapper

    @staticmethod
    def createMongoQueryObj(mongoObects):
        return {mongoObj.field: mongoObj.value for mongoObj in mongoObects}

    @staticmethod
    def buildQueryStr(queryParams):
        query = '?'
        isFirstParam = True

        for paramName, paramValue in queryParams.iteritems():
            if paramValue is not None:
                if not isFirstParam:
                    query += '&'
                else:
                    isFirstParam = False

                query += '{0}={1}'.format(paramName, json.dumps(Utils.createMongoQueryObj(paramValue)))

        if len(query) == 1:
            query = ''

        return query

    @staticmethod
    def convertUnitToBytes(unit):
        if type(unit) != str or unit.lower() == 'max':
            return unit

        unitChar = unit[-1:]
        unit = unit[:-1]

        if unitChar in 'kK':
            factor = 1
        elif unitChar in 'mM':
            factor = 2
        elif unitChar in 'gG':
            factor = 3
        elif unitChar in 'tT':
            factor = 4
        elif unitChar in 'pP':
            factor = 5
        else:
            assert unit, "Invalid capacity unit {}".format(unit)
            raise ValueError

        return int(unit) * 1024 ** factor

    @staticmethod
    def convertBytesToUnit(bytes):
        def getUnitType(multiplier):
            if multiplier == 1:
                unitType = 'KiB'
            elif multiplier == 2:
                unitType = 'MiB'
            elif multiplier == 3:
                unitType = 'GiB'
            else:
                unitType = 'TiB'

            return unitType

        if not isinstance(bytes, (int, long, float)):
            return bytes

        counter = 0
        someUnits = bytes

        while someUnits / 1000 >= 1:
            counter += 1
            someUnits /= 1000

        if counter == 0:
            return str(bytes) + 'B'
        else:
            division = float(bytes) / float(1024 ** counter)

            return str(round(((division * 100) / 100), 2)) + getUnitType(counter)
