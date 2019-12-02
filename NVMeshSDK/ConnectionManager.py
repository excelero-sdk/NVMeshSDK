import json
import requests
import urllib3
import urlparse
import random
import datetime
import time
from logging import DEBUG, INFO

from NVMeshSDK import LoggerUtils
from NVMeshSDK.Utils import Utils

urllib3.disable_warnings()


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


class ConnectionManager:
    DEFAULT_USERNAME = "app@excelero.com"
    DEFAULT_PASSWORD = "admin"
    DEFAULT_NVMESH_CONFIG_FILE = '/etc/opt/NVMesh/nvmesh.conf'

    __instance = None

    @staticmethod
    def getInstance(managementServer=None, user=DEFAULT_USERNAME, password=DEFAULT_PASSWORD,
                 configFile=DEFAULT_NVMESH_CONFIG_FILE):
        if ConnectionManager.__instance is None:
            ConnectionManager(managementServer, user, password, configFile)
        return ConnectionManager.__instance

    def __init__(self, managementServer=None, user=DEFAULT_USERNAME, password=DEFAULT_PASSWORD,
                 configFile=DEFAULT_NVMESH_CONFIG_FILE):
        if ConnectionManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ConnectionManager.__instance = self
            self.managementServer = None
            self.httpRequestTimeout = 5
            self.requestOperationTimeout = 30
            self.maxRetries = 3
            self.logLevel = INFO
            self.configFile = configFile
            self.setManagementServer(managementServer)
            self.currentMgmtIndex = self.getRandomMgmtIndex() if len(self.managementServers) != 1 else 0
            self.user = user
            self.password = password
            self.logger = LoggerUtils.getInfraClientLogger('ConnectionManager', logLevel=self.logLevel)
            self.session = requests.session()
            self.isAlive()

    def getRandomMgmtIndex(self):
        return random.randint(0, len(self.managementServers) - 1)

    def setManagementServer(self, managementServers=None):
        if managementServers:
            if isinstance(managementServers, list):
                self.managementServers = managementServers
            else:
                self.managementServers = [managementServers]
        else:
            self.managementSetConfigs()

    def managementSetConfigs(self):
        configs = Utils.readConfFile(self.configFile)
        if not configs:
            self.managementServers = ['https://localhost:4000']
        else:
            if 'MANAGEMENT_PROTOCOL' in configs:
                protocol = configs['MANAGEMENT_PROTOCOL']
            else:
                raise Exception('MANAGEMENT_PROTOCOL variable could not be found in: {0}'.format(self.configFile))

            if 'MANAGEMENT_SERVERS' in configs:
                servers = configs['MANAGEMENT_SERVERS'].replace('4001', '4000').split(',')
            else:
                raise Exception('MANAGEMENT_SERVERS variable could not be found in: {0}'.format(self.configFile))

            if 'HTTP_REQUEST_TIMEOUT' in configs:
                self.httpRequestTimeout = configs['HTTP_REQUEST_TIMEOUT']

            if 'REQUEST_OPERATION_TIMEOUT' in configs:
                self.requestOperationTimeout = configs['REQUEST_OPERATION_TIMEOUT']

            if 'CONNECTION_MANAGER_DEBUG' in configs:
                if configs['CONNECTION_MANAGER_DEBUG'] == 'Yes':
                    self.logLevel = DEBUG

            self.managementServers = [protocol + '://' + server for server in servers]

        return self.managementServers

    def isAlive(self):
        endTime = Utils.getTimeoutEndTime(self.requestOperationTimeout)
        sleepTime = 0.01
        reachedTimeout = False

        while not reachedTimeout:
            self.logger.debug("doing isAlive the end time is: {0}".format(endTime))
            nowTime = datetime.datetime.now()
            if endTime <= nowTime:
                reachedTimeout = True
                break

            try:
                err, out = self.get('/isAlive')
                return True if not err else False
            except ManagementTimeout as ex:
                self.logger.debug(
                    "failed isAlive to: {0}, exception: {1}, waiting for: {2}s before next request".format(self.managementServer, ex, sleepTime))
                time.sleep(sleepTime)

                self.getNextMgmtIndex()

        if reachedTimeout:
            raise ManagementTimeout("Tried isAlive on all Management Servers in rotation for: {}s and all failed".format(
                                        self.requestOperationTimeout))

    def getNextMgmtIndex(self):
        if len(self.managementServers) != 1:
            self.currentMgmtIndex = (self.currentMgmtIndex + 1) % len(self.managementServers)

    def post(self, route, payload=None, postTimeout=None):
        return self.request('post', route, payload, postTimeout)

    def get(self, route, payload=None):
        return self.request('get', route, payload)

    def request(self, method, route, payload=None, postTimeout=None, numberOfRetries=0):
            self.logger.debug('In request method={0} route={1} payload={2} postTimeout={3}, numberOfRetries={4}'.
                    format(method, route, payload, postTimeout, numberOfRetries))

            self.managementServer = self.managementServers[self.currentMgmtIndex]

            try:
                return self.do_request(method, route, payload, postTimeout, numberOfRetries)
            except ManagementTimeout as ex:
                raise ex

    def do_request(self, method, route, payload=None, postTimeout=None, numberOfRetries=0):
        if '/save' in route:
            volName = payload[0]['name']
        startTime = None

        res = None
        if route != '/isAlive':
            self.logger.debug(
                'In do_request method={0} route={1} payload={2} postTimeout={3}, numberOfRetries={4}'.
                    format(method, route, payload, postTimeout, numberOfRetries))
        url = ''
        try:
            url = urlparse.urljoin(self.managementServer, route)
            if method == 'post':
                startTime = time.time()
                res = self.session.post(url, json=payload, verify=False, timeout=self.httpRequestTimeout if not postTimeout else postTimeout)
                if '/save' in route:
                    execTime = time.time() - startTime
                    execTime *= 1000
                    err, jsonObject = self.handleResponse(res)
                    self.logger.debug("VolumeID: {0}, err: {1}, res: {2}, time: {3}".format(volName, err, json.dumps(jsonObject), execTime))
            elif method == 'get':
                res = self.session.get(url, params=payload, verify=False, timeout=self.httpRequestTimeout)

            if '/login' in res.text:
                res = self.login()

                if '/save' in route:
                    self.logger.debug("VolumeID: {0}, res: {1}".format(volName, res.content))

                success = json.loads(res.content)['success']
                if success:
                    return self.request(method, route, payload, postTimeout)

            if route != '/isAlive' and method == 'post':
                self.logger.debug('route {0} got response: {1}'.format(route, res.content))

            err, jsonObj = self.handleResponse(res)
            return err, jsonObj

        except Exception as ex:
            if '/save' in route:
                execTime = None
                if startTime:
                    execTime = time.time() - startTime
                    execTime *= 1000

                self.logger.debug("ex:volumeID {0}, Request to {1} failed, ex: {2}, time: {3}, type: {4}, name: {5}".format(
                    volName, route, ex, execTime, type(ex), type(ex).__name__))
            else:
                self.logger.debug("Request to {0} failed, ex: {1}".format(route, ex))

            if numberOfRetries < self.maxRetries:
                numberOfRetries += 1
                self.logger.debug("Got exception: {0}, retrying route: {1}".format(ex, route))
                return self.request(method, route, payload, postTimeout, numberOfRetries)
            else:
                raise ManagementTimeout(url, ex.message)




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
                    "message": ex.message,
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

            raise ManagementTimeout(self.managementServer, ex.message)
