#! /usr/bin/env python

import json
import logging
import urlparse
import httplib
import time

import restHelper


#Configure logging
from src.testcode.common import Constants

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class Connection():
    def __init__(self, hostname, port, username=Constants.VC_USERNAME, password=Constants.VC_PASSWORD):
        '''
        Initialize connection to REST API
        '''
        self.rest = restHelper.RestHelper(hostname, port)
        #self.rest.authenticateBasic(username, password)
        self.rest.setGlobalHeaders({
            'Accept': 'application/json',
            'Content-type': 'application/json',
        })
        self.rest.setLogLevel(logging.DEBUG)
        #Child objects for API sub-areas

        self.clusters = Cluster(self)
        self.tasks = Task(self)
        self.networks = Network(self)
        self.resourcepools = ResourcePool(self)
        self.datastores = Datastore(self)
        self.distros = Distro(self)
        self.versions = Version(self)
        self.racks = Rack(self)
        self.appManagers = AppManager(self)
        self.accountServers = Vmusermgmtserver(self)
        self.mgmtvm = Vmmgmtvm(self)


class BasicAPI(object):
    def __init__(self, connection):
        self.connection = connection
        self.rest = connection.rest

    def _create(self, url, obj):
        return self._createJson(self._apiUrl(url), obj)

    def _put(self, url, obj):
        return self._putJson(self._apiUrl(url), obj)

    def _get(self, url):
        return self._getJson(self._apiUrl(url))

    def _delete(self, url):
        '''
         Return a response with Accepted status and put task uri in the Location of header that can be used to monitor the progress
        '''
        response = self.rest.delete(self._apiUrl(url))
        self._checkResponse(response)
        if response.status == httplib.ACCEPTED:
            location = self.rest.getLocationHeader(response)
            task = self._getJson(location)
            logger.info('Task information ' + str(task))
            task = self.connection.tasks.wait(task, 'COMPLETED')
            return self._getJson(location)
        else:
            msg = response.read()
            logger.error(msg)
            return msg

    def _action(self, url):
        '''
         Return a response with Accepted status and put task uri in the Location of header that can be used to monitor the progress
        '''
        response = self.rest.putAction(self._apiUrl(url))
        self._checkResponse(response)
        if response.status == httplib.ACCEPTED:
            location = self.rest.getLocationHeader(response)
            task = self._getJson(location)
            logger.info('Task information ' + str(task))
            task = self.connection.tasks.wait(task, 'COMPLETED')
            return self._getJson(location)
        else:
            msg = response.read()
            logger.error(msg)
            return msg

    def _createJson(self, url, obj):
        data = json.dumps(obj)
        response = self.rest.post(url, body=data)
        self._checkResponse(response)
        if response.status == httplib.OK:
            # Ok has no locationHeader
            return response
        if response.status == httplib.ACCEPTED:
            location = self.rest.getLocationHeader(response)
            task = self._getJson(location)
            logger.info('Task information ' + str(task))
            task = self.connection.tasks.wait(task, 'COMPLETED')
            return self._getJson(location)
        else:
            msg = response.read()
            logger.error(msg)
            return response

    def _putJson(self, url, obj):
        data = json.dumps(obj)
        response = self.rest.put(url, body=data)
        self._checkResponse(response)
        if response.status == httplib.ACCEPTED:
            location = self.rest.getLocationHeader(response)
            task = self._getJson(location)
            logger.info('Task information ' + str(task))
            task = self.connection.tasks.wait(task, 'COMPLETED')
            return self._getJson(location)
        else:
            msg = response.read()
            logger.error(msg)
            return msg

    def _getJson(self, url):
        response = self.rest.get(url)
        self._checkResponse(response)
        return json.loads(response.read())

    def _checkResponse(self, response):
        if response.status / 100 != 2:
            logger.error(response.status)
            msg = response.read()
            print msg
        else:
            logger.info(response.status)

    def _apiUrl(self, url):
        if url[0] != '/' and urlparse.urlsplit(url).scheme == '':
            url = '/serengeti/api/' + url
            logger.info(url)
        return url


class CommonAPI(BasicAPI):
    '''
    Clients just need to override create and put.
    '''

    def __init__(self, connection, urlbase):
        super(CommonAPI, self).__init__(connection)
        self.urlbase = urlbase

    def _create(self, postfields):
        return super(CommonAPI, self)._create(self._collectionURL(), postfields)

    def _put(self, instanceName, putfields):
        return super(CommonAPI, self)._put(self._instanceUrl(instanceName), putfields)

    def _putRack(self, putfields):
        return super(CommonAPI, self)._put(self._collectionURL(), putfields)

    def _action(self, instanceName, action):
        return super(CommonAPI, self)._action(self._instanceUrl(instanceName) + '?state=' + action)

    def _scale(self, instanceName, groupName, scale, putfields):
        return super(CommonAPI, self)._put(self._scaleUrl(instanceName, groupName, scale), putfields)

    def _param(self, instanceName, param, putfields):
        return super(CommonAPI, self)._put(self._paramUrl(instanceName, param), putfields)

    def get(self, instanceName):
        return self._get(self._instanceUrl(instanceName))

    def getByID(self, instanceID):
        return self._get(self._instanceUrlByID(instanceID))

    def getAll(self):
        return self._get(self._collectionURL())

    def getVersion(self):
        return self._get(self.urlbase)

    def getSpecFile(self, instanceName, spec):
        return self._get(self._specfileUrl(instanceName, spec))

    def delete(self, instanceName):
        return self._delete(self._instanceUrl(instanceName))

    #Appmanager related operations
    def getAppmangerTypes(self):
        return self._get(self._appmanagerTypesUrl())

    def getAppmanagerDistros(self, instanceName):
        return self._get(self._appmanagerDistrosUrl(instanceName))

    def getAppmanagerDistroConf(self, instanceName, distroName):
        return self._get(self._appmanagerDistroConfUrl(instanceName, distroName))

    def getAppmanagerDistroRoles(self, instanceName, distroName):
        return self._get(self._appmanagerDistroRoleUrl(instanceName, distroName))

    #Construct all special URLs
    # for usermgmt server , its post url is special
    def _collectionURL(self):
        if 'usermgmtserver' in self.urlbase:
            return self.urlbase + 's' + '?forceTrustCert=true'
        else:
            return self.urlbase + 's'

    def _instanceUrl(self, instanceName):
       if 'mgmtvm' in self.urlbase:
           return self.urlbase
       elif 'usermgmt' in self.urlbase:
           return self.urlbase + 's' + '/' + instanceName
       else:
        return self.urlbase + '/' + instanceName

    def _instanceUrlByID(self, instanceID):
        return self.urlbase + '/' + str(instanceID)

    def _specfileUrl(self, instanceName, spec):
        return self.urlbase + '/' + instanceName + '/' + spec

    def _scaleUrl(self, instanceName, groupName, scale):
        return self.urlbase + '/' + instanceName + '/' + 'nodegroup' + '/' + groupName + '/' + scale

    def _paramUrl(self, instanceName, param):
        return self.urlbase + '/' + instanceName + '/' + param

    def _appmanagerTypesUrl(self):
        return self.urlbase + 's' + '/' + 'types'

    def _appmanagerDistrosUrl(self, instanceName):
        return self.urlbase + '/' + instanceName + '/' + 'distros'

    def _appmanagerDistroConfUrl(self, instanceName, distroName):
        return self.urlbase + '/' + instanceName + '/' + 'distro' + '/' + distroName + '/' + 'configurations'

    def _appmanagerDistroRoleUrl(self, instanceName, distroName):
        return self.urlbase + '/' + instanceName + '/' + 'distro' + '/' + distroName + '/' + 'roles'


class Task(CommonAPI):
    def __init__(self, connection):
        super(Task, self).__init__(connection, 'task')

    def wait(self, task, expStatus):
        if (str(task['status']) in ('STARTED', 'STARTING')):
            logger.info('|' + self._taskUrl(task['id']) + '|' + task['target'] + '|progress: ' + str(
                task['progress']) + ', waiting...')
        else:
            logger.error('Task is under abnormal status ' + str(task['status']))
        while str(task['status']) in ('STARTED', 'STARTING'):
            time.sleep(60)
            task = self.getByID(task['id'])
            logger.info('|' + self._taskUrl(task['id']) + '|' + task['target'] + '|progress: ' + str(
                task['progress']) + ', waiting...')
        if str(task['status']) == expStatus:
            logger.info('|' + self._taskUrl(task['id']) + '|' + task['target'] + '|progress: ' + str(
                task['status']) + ', task done.')
        else:
            logger.error('Task status is abnormal ' + task['status'])
        return task

    def _taskUrl(self, taskId):
        return 'task/' + str(taskId)


class Cluster(CommonAPI):
    def __init__(self, connection):
        super(Cluster, self).__init__(connection, 'cluster')

    def create(self, postfields):
        return self._create(postfields)

    def put(self, clusterName, putfields):
        return self._put(clusterName, putfields)

    #Stop, start and resume a cluster.
    def action(self, clusterName, action):
        return self._action(clusterName, action)

    #Scale up/down cpu and mem, scale out nodegroup.
    def scale(self, instanceName, groupName, scale, putfields):
        return self._scale(instanceName, groupName, scale, putfields)

    #Change elasticity mode, IO priority, and maximum or minimum number of powered on compute nodes under auto mode.
    #Turn on or off some compute nodes
    def param(self, instanceName, param, putfields):
        return self._param(instanceName, param, putfields)


class Network(CommonAPI):
    def __init__(self, connection):
        super(Network, self).__init__(connection, 'network')

    def create(self, postfields):
        return self._create(postfields)

    def put(self, networkName, putfields):
        return self._put(networkName, putfields)


class ResourcePool(CommonAPI):
    def __init__(self, connection):
        super(ResourcePool, self).__init__(connection, 'resourcepool')

    def create(self, postfields):
        return self._create(postfields)


class Datastore(CommonAPI):
    def __init__(self, connection):
        super(Datastore, self).__init__(connection, 'datastore')

    def create(self, postfields):
        return self._create(postfields)


class Distro(CommonAPI):
    def __init__(self, connection):
        super(Distro, self).__init__(connection, 'distro')


class Version(CommonAPI):
    def __init__(self, connection):
        super(Version, self).__init__(connection, 'hello')


class Rack(CommonAPI):
    def __init__(self, connection):
        super(Rack, self).__init__(connection, 'rack')

    def put(self, putfields):
        return self._putRack(putfields)


class AppManager(CommonAPI):
    def __init__(self, connection):
        super(AppManager, self).__init__(connection, 'appmanager')

    def create(self, postfields):
        return self._create(postfields)

#account management server (AD/LDAP)
class Vmusermgmtserver(CommonAPI):
    def __init__(self,connection):
        super(Vmusermgmtserver,self).__init__(connection,'vmconfig/usermgmtserver')
    def create(self,postfields):
        return self._create(postfields)

class Vmmgmtvm(CommonAPI):
    def __init__(self,connection):
        super(Vmmgmtvm,self).__init__(connection,'vmconfig')
#Configure Management VM
    def put(self,putfields,instanceName = 'mgmtvm'):
        'PUT to /serengeti/api/vmconfig/mgmtvm'
        return self.put(instanceName,putfields)
    def get(self,instanceName = 'mgmtvm'):
        'GET from /serengeti/api/vmconfig/mgmtvm'
        return self.get(instanceName)



