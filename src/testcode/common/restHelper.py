#!/usr/bin/env python

# resthelper.py -- RESTful client helper framework

import copy
import httplib
import json
import logging
import time
import urlparse
import Constants

# configure logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

# convenience constants so clients don't need to depend on httplib module

ACCEPTED = httplib.ACCEPTED
OK = httplib.OK


class RestHelper:
    def __init__(self, hostname, port='8443'):
        self.hostname = hostname
        self.port = port
        self.connectMethod = httplib.HTTPSConnection
        self.perHelperHeaders = {}

    def setLogLevel(self, level):
        logger.setLevel(level)

    def setGlobalHeaders(self, headers):
        self.perHelperHeaders = copy.copy(headers)
    # Log on and save session
    def authenticateBasic(self, username, password):
        url = 'https://' + self.hostname + ':' + self.port + '/serengeti/j_spring_security_check'
        body = 'j_username='+username+'&j_password='+password
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        httpConn = self.connectMethod(self.hostname, self.port)
        httpConn.request('POST', url, body, headers)
        response = httpConn.getresponse()
        headers = response.getheaders()
        self.authheader = dict(headers).get(('set-cookie').split(";")[0])
    # Log out,need to do.
    def logout(self):
        url = 'https://' + self.hostname + ':' + self.port + '/serengeti/j_spring_security_logout'
        logger.info(url)
        headers = {'Content-type': 'application/json'}
        body = None
        httpConn = self.connectMethod(self.hostname, self.port)
        httpConn.request(url, body, headers)

    def transact(self, verb, path, body=None, headers={}):
        # build combined header list
        allHeaders = copy.copy(self.perHelperHeaders)
        #Each operation need log on once, since bug 1290897
        self.authenticateBasic(username=Constants.VC_USERNAME, password=Constants.VC_PASSWORD)
        if hasattr(self, 'authheader'):
            allHeaders['Cookie'] = self.authheader
        for key in headers:
            allHeaders[key] = headers[key]
        # handle both relative and absolute URLs (as long as they're to same scheme://host:port/)
        path = self._relativePath(path)
        httpConn = self.connectMethod(self.hostname, self.port)
        logger.info('request: %s %s' % (verb, path))
        logger.info('Path:' + path)
        if body is not None:
            logger.debug(body)
        httpConn.request(verb, path, body=body, headers=allHeaders)
        response = httpConn.getresponse()
        logger.debug('response: %d %s' % (response.status, response.reason))
        logger.debug(response)
        if response.status in (httplib.ACCEPTED, httplib.CREATED):
            logger.debug('  with location: %s' % self.getLocationHeader(response))
        return response

    def get(self, path, headers={}):
        return self.transact('GET', path, headers=headers)

    def put(self, path, body, headers={}):
        return self.transact('PUT', path, body=body, headers=headers)

    def post(self, path, body, headers={}):
        return self.transact('POST', path, body=body, headers=headers)

    def putAction(self, path, headers={}):
        return self.transact('PUT', path, headers=headers)

    def delete(self, path, headers={}):
        return self.transact('DELETE', path, headers=headers)

    def postActionWithBody(self, path, body, headers={}):
        return self.transact('POST', path, body=body, headers=headers)

    def getLocationHeader(self, response):
        return response.getheader('location')

    def _relativePath(self, path):
        logger.info('path ' + str(path))
        uri = urlparse.urlsplit(path)
        logger.info('uri ' + str(uri))
        if uri.scheme == '':  # was already relative, not absolute, url
            return path
        return uri.path

    def json2prettyjson(self, rawjson):
        obj = json.loads(rawjson)
        return self.obj2prettyjson(obj)

    def obj2prettyjson(self, obj):
        return json.dumps(obj, sort_keys=True, indent=3)


    def waitTaskToSucceed(self, response):
        assert response.status == ACCEPTED
        taskUri = self.getLocationHeader(response)
        taskStatus = None
        taskRead = None
        while True:
            response = self.get(taskUri)
            taskRead = self.readAndDumpJson(response, level=logging.DEBUG)
            taskStatus = taskRead['status']
            if taskStatus not in ('PENDING', 'RUNNING'):
                logger.info('task status: ' + taskStatus + ', task done.')
                break
            logger.info('task status: ' + taskStatus + ', waiting...')
            time.sleep(2)
        assert taskStatus == 'SUCCESS'  # XXX: handle other cases?
        # XXX: return URL which should be embedded in taskRead object

        # (delete won't have this, but async create would)

        # return taskRead['location']

    def readAndDumpJson(self, response, level=logging.INFO):
        data = response.read()
        try:
            obj = json.loads(data)
            logger.log(level, 'response, json format:\n' + self.obj2prettyjson(obj))
            return obj
        except:
            logger.log(level, 'response, non-JSON: %d %s\n%s' % (response.status, response.reason, data))
            return data
