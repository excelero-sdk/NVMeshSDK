from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
from builtins import object
import json
import requests
import urllib3
import urllib.parse
import random
import time
from logging import DEBUG, INFO, WARNING

from NVMeshSDK import LoggerUtils
from NVMeshSDK.Utils import Utils

urllib3.disable_warnings()


class RandomSleepTime(object):
    def __init__(self, start, stop, precision=2):
        self.start = start
        self.stop = stop
        self.precision = precision

    def getValue(self):
        return round(random.uniform(self.start, self.stop), self.precision)


class ConnectionManagerError(Exception):
    pass


class ManagementTimeout(ConnectionManagerError):
    def __init__(self, iport, msg=''):
        ConnectionManagerError.__init__(self, 'Could not connect to Management at {0}'.format(iport), msg)


class ManagementLoginFailed(ConnectionManagerError):
    def __init__(self, iport, msg=''):
        ConnectionManagerError.__init__(self, 'Could not login to Management at {0}'.format(iport), msg)


class ManagementHTTPError(ConnectionManagerError):
    def __init__(self, res):
        self.status_code = res.status_code
        self.message = "Reason:{0} Content:{1}".format(res.reason, res.content)


class ConnectionManager(object):
    DEFAULT_USERNAME = "app@excelero.com"
    DEFAULT_PASSWORD = "admin"
    DEFAULT_NVMESH_CONFIG_FILE = '/etc/opt/NVMesh/nvmesh.conf'
    __instance = None

    @staticmethod
    def getInstance(managementServers=None, user=DEFAULT_USERNAME, password=DEFAULT_PASSWORD,
                 configFile=DEFAULT_NVMESH_CONFIG_FILE, logger=None):
        if ConnectionManager.__instance is None:
            ConnectionManager(managementServers, user, password, configFile, logger)
        return ConnectionManager.__instance

    def __init__(self, managementServers=None, user=DEFAULT_USERNAME, password=DEFAULT_PASSWORD,
                 configFile=DEFAULT_NVMESH_CONFIG_FILE, logger=None):
        if ConnectionManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ConnectionManager.__instance = self
            self.logLevel = INFO
            self.managementServer = None
            self.managementServers = None
            self.httpRequestTimeout = 200
            self.randomSleepBetweenRequests = RandomSleepTime(start=0.5, stop=1)
            self.randomSleepBeforeChangingMgmt = RandomSleepTime(start=0, stop=0.2)
            self.maxHttpRequestRetries = 3
            self.maxManagementsRotations = 1
            self.configFile = configFile

            if managementServers:
                self.setManagementServers(managementServers)

            self.managementSetConfigs()
            self.managementServers = [str(server) for server in self.managementServers]

            self.logger = (logger if logger else self.setLogger()).getLogger('ConnectionManager')
            self.currentMgmtIndex = self.getInititalMgmtIndex()
            self.user = user
            self.password = password
            self.session = requests.session()
            self.isAlive()

    def setLogger(self):
        logger = LoggerUtils.Logger()
        logger.setOptions(logLevel=self.logLevel)
        return logger

    def getInititalMgmtIndex(self):
        isHA = len(self.managementServers) != 1
        return self.getRandomMgmtIndex() if isHA else 0

    def getRandomMgmtIndex(self):
        return random.randint(0, len(self.managementServers) - 1)

    def setManagementServers(self, managementServers=None):
        if managementServers:
            if isinstance(managementServers, list):
                self.managementServers = managementServers
            else:
                self.managementServers = [managementServers]

    def managementSetConfigs(self):
        configs = Utils.readConfFile(self.configFile)

        if not configs:
            print('Failed to open the configuration file: {}, all configuration are set to the default.'.format(self.configFile))
            if not self.managementServers:
                self.managementServers = ['https://localhost:4000']
        else:
            if not self.managementServers:
                self.setManagementServersFromConfigs(configs)

            if 'HTTP_REQUEST_TIMEOUT' in configs:
                self.httpRequestTimeout = configs['HTTP_REQUEST_TIMEOUT']

            if 'MAX_MANAGEMENT_ROTATIONS' in configs:
                self.maxManagementsRotations = configs['MAX_MANAGEMENT_ROTATIONS']

            if 'CONNECTION_MANAGER_DEBUG' in configs and configs['CONNECTION_MANAGER_DEBUG'] == 'Yes':
                self.logLevel = DEBUG

    def setManagementServersFromConfigs(self, configs):
        if 'ALTERNATIVE_MGMT' in configs:
            self.managementServers = (configs['ALTERNATIVE_MGMT']).split(',')
        else:
            if 'MANAGEMENT_PROTOCOL' in configs:
                protocol = configs['MANAGEMENT_PROTOCOL']
            else:
                msg = 'MANAGEMENT_PROTOCOL variable could not be found in: {0}'.format(self.configFile)
                self.logAndThrow(msg)
            if 'MANAGEMENT_SERVERS' in configs:
                servers = configs['MANAGEMENT_SERVERS'].replace('4001', '4000').split(',')
            else:
                msg = 'MANAGEMENT_SERVERS variable could not be found in: {0}'.format(self.configFile)
                self.logAndThrow(msg)

            self.managementServers = [protocol + '://' + server for server in servers]

    def logAndThrow(self, msg):
        self.logger.error(msg)
        raise Exception(msg)

    def isAlive(self):
        index = 0
        currentRotation = 0

        while currentRotation < self.maxManagementsRotations:
            try:
                err, out = self.get('/isAlive')
                return True if not err else False
            except ManagementTimeout as ex:
                self.getNextMgmtIndex()
                index += 1
                currentRotation += 1 if index % len(self.managementServers) == 0 else 0
                sleepBeforeChangingMgmt = self.randomSleepBeforeChangingMgmt.getValue()
                self.logger.debug(
                    "failed isAlive to: {0}, exception: {1}, waiting for: {2}s before next request".format(self.managementServer, ex, sleepBeforeChangingMgmt))
                time.sleep(sleepBeforeChangingMgmt)

        raise ManagementTimeout(msg="Tried isAlive on all Management Servers in rotation for {} rotations and all failed".format(
                                        self.maxManagementsRotations), iport=', '.join(self.managementServers))

    def getNextMgmtIndex(self):
        if len(self.managementServers) != 1:
            self.currentMgmtIndex = (self.currentMgmtIndex + 1) % len(self.managementServers)

    def post(self, route, payload=None, postTimeout=None):
        return self.request('post', route, payload, postTimeout)

    def get(self, route, payload=None):
        return self.request('get', route, payload)

    def request(self, method, route, payload=None, postTimeout=None, numberOfRetries=0):
        if numberOfRetries == 0:
            route = Utils.encodePlusInRoute(route)
            
        self.managementServer = self.managementServers[self.currentMgmtIndex]
        self.logger.debug('Doing request to: {}'.format(self.managementServer))
        try:
            return self.doRequest(method, route, payload, postTimeout, numberOfRetries)
        except ManagementTimeout as ex:
            raise ex

    def doRequest(self, method, route, payload=None, postTimeout=None, numberOfRetries=0):
        IS_ALIVE_TIMEOUT = 1
        isAliveRoute = route == '/isAlive'
        volumeSaveRoute = 'volumes/save' in route
        isDebug = self.logLevel == 'DEBUG'

        if volumeSaveRoute:
            volName = payload[0]['name']
        startTime = None

        res = None
        if not isAliveRoute:
            self.logger.debug(
                'In doRequest method={0} route={1} payload={2} postTimeout={3}, numberOfRetries={4}'.
                    format(method, route, payload, postTimeout, numberOfRetries))
        url = ''
        try:
            url = urllib.parse.urljoin(self.managementServer, route)
            if method == 'post':
                if isDebug and volumeSaveRoute:
                    startTime = time.time()

                res = self.session.post(url, json=payload, verify=False, timeout=self.httpRequestTimeout if not postTimeout else postTimeout)
                if isDebug and volumeSaveRoute:
                    execTime = (time.time() - startTime) * 1000
                    err, jsonObject = self.handleResponse(res)
                    self.logger.debug("id: {0}, err: {1}, res: {2}, it took me: {3}ms to save".format(volName, err, json.dumps(jsonObject), execTime))
            elif method == 'get':
                res = self.session.get(url, params=payload, verify=False, timeout=IS_ALIVE_TIMEOUT if isAliveRoute else self.httpRequestTimeout)

            if '/login' in res.text:
                res = self.login()

                if volumeSaveRoute:
                    self.logger.debug("after login, id: {0}, res: {1}".format(volName, res.content))

                success = json.loads(res.content)['success']
                if success:
                    return self.request(method, route, payload, postTimeout)

            if not isAliveRoute and method == 'post':
                self.logger.debug('route {0} got response: {1}'.format(route, res.content))

            err, jsonObj = self.handleResponse(res)
            return err, jsonObj

        except Exception as ex:
            if isDebug and volumeSaveRoute:
                execTime = None
                if startTime:
                    execTime = (time.time() - startTime) * 1000

                self.logger.debug("ex:id {0}, Request to {1} failed, ex: {2}, it took me: {3}ms, ex type: {4}, ex name: {5}".format(
                    volName, route, ex, execTime, type(ex), type(ex).__name__))
            else:
                self.logger.debug("Request to {0} failed, ex: {1}".format(route, ex))

            if isAliveRoute:
                raise ManagementTimeout(url, str(ex))
            elif numberOfRetries < self.maxHttpRequestRetries:
                numberOfRetries += 1
                sleepTimeBetweenRequestRetry = self.randomSleepBetweenRequests.getValue()
                self.logger.debug("Got exception: {0}, sleeping for: {1}s then retrying route: {2}".format(ex,
                                                                                                           sleepTimeBetweenRequestRetry,
                                                                                                           route))
                time.sleep(sleepTimeBetweenRequestRetry)
                return self.request(method, route, payload, postTimeout, numberOfRetries)
            else:
                self.logger.debug("Request to {0}, failed {1} times. Trying to change management server.".format(route, self.maxHttpRequestRetries))
                isAlive = self.isAlive()
                if not isAlive:
                    raise ManagementTimeout(url, str(ex))
                else:
                    return self.request(method, route, payload, postTimeout, numberOfRetries=0)

    @staticmethod
    def handleResponse(res):
        jsonObj = None
        err = None

        if res.status_code in [200, 304]:
            try:
                if res.content:
                    jsonObj = json.loads(res.content)
            except Exception as ex:
                err = {
                    "code": res.status_code,
                    "message": str(ex),
                    "content": res.content
                }
        else:
            err = {
                "code": res.status_code,
                "message": res.reason,
                "content": res.content
            }

        return err, jsonObj

    def login(self):
        try:
            out = self.session.post("{}/login".format(self.managementServer),
                              data={"username": self.user, "password": self.password}, verify=False, timeout=self.httpRequestTimeout)
            return out
        except requests.ConnectionError as ex:
            raise ManagementTimeout(self.managementServer, str(ex))
