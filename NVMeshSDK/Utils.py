#!/usr/bin/env python

from __future__ import division, unicode_literals
from past.builtins import execfile
from future import standard_library
standard_library.install_aliases()
from builtins import zip, object
from past.utils import old_div
from functools import wraps
import inspect
import json
import datetime
import re
import subprocess
import os
import urllib.request, urllib.parse, urllib.error


class Utils(object):

    @staticmethod
    def initializer(func):
        argSpec = inspect.getargspec(func)
        names, varargs, keywords, defaults = argSpec

        @wraps(func)
        def wrapper(self, *args, **kargs):
            for name, arg in list(zip(names[1:], args)) + list(kargs.items()):
                setattr(self, name, arg)

            for name, default in zip(reversed(names), reversed(defaults)):
                if not hasattr(self, name):
                    if default is not None:
                        setattr(self, name, default)

            filteredKargs = {k: v for k, v in kargs.items() if k in names}
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

        for paramName, paramValue in queryParams.items():
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
    def isStr(s):
        try:
            basestring  # attempt to evaluate basestring -> PY2
            return isinstance(s, basestring)
        except NameError: # PY3
            return isinstance(s, str)

    @staticmethod
    def convertUnitCapacityToBytes(unitCapacity):
        def getMultipleOfBytesType(unitCapacity):
            binary = 1024
            decimal = 1000
            return binary if 'i' in unitCapacity else decimal

        def getFactor(termFirstLetter):
            return {'k': 1, 'm': 2, 'g': 3, 't': 4, 'p': 5}[termFirstLetter]

        if not Utils.isStr(unitCapacity) or unitCapacity.lower() == 'max':
            return unitCapacity

        unitCapacity = unitCapacity.lower()
        multipleOfBytesType = getMultipleOfBytesType(unitCapacity)

        search = re.search(r"([0-9]*\.?[0-9]+)(\w+)", unitCapacity)
        value = search.group(1)
        term = search.group(2)
        factor = getFactor(term[:1])

        return float(value) * multipleOfBytesType ** factor

    @staticmethod
    def convertBytesToUnit(bytes, isBinary=True):
        def getUnitType(multiplier, isBinary):
            if multiplier == 1:
                unitType = 'KiB'
            elif multiplier == 2:
                unitType = 'MiB'
            elif multiplier == 3:
                unitType = 'GiB'
            elif multiplier == 4:
                unitType = 'TiB'
            else:
                unitType = 'PiB'

            return unitType.replace('i', '') if not isBinary else unitType

        if not isinstance(bytes, (int, int, float)):
            return bytes

        counter = 0
        someUnits = bytes

        while old_div(someUnits, 1000) >= 1:
            counter += 1
            someUnits /= 1000

        if counter == 0:
            return str(bytes) + 'B'
        else:
            unitFactor = 1024 if isBinary else 1000
            division = float(bytes) / float(unitFactor ** counter)

            return str(round((old_div((division * 100), 100)), 2)) + getUnitType(counter, isBinary)

    @staticmethod
    def executeLocalCommand(command):
        try:
            out = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout, stderr = out.communicate()
            return stdout, stderr
        except OSError as e:
            return None, e

    @staticmethod
    def readConfFile(confFile):
        g = {}
        l = {}

        try:
            if not os.path.exists(confFile):
                return False
            else:
                execfile(confFile, g, l)
                return l
        except Exception:
            return False

    @staticmethod
    def getTimeoutEndTime(timeout):
        def addSecs(time, secs):
            fullDate = datetime.datetime(time.year, time.month, time.day, time.hour, time.minute, time.second)
            fullDate = fullDate + datetime.timedelta(seconds=secs)
            return fullDate

        startTime = datetime.datetime.now()
        endTime = addSecs(startTime, timeout)

        return endTime

    @staticmethod
    def createDirIfNotExsits(path):
        path = os.path.expanduser(path)
        if not os.path.isdir(path):
            os.makedirs(path)

    @staticmethod
    def encodePlusInRoute(route):
        return ''.join([urllib.parse.quote('+') if c == '+' else c for c in list(route)]) if '+' in route else route