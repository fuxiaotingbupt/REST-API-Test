__author__ = 'xfu'
#!/usr/bin/env python
# testDatastore.py -- Datastore related test cases
from src.testcode.common import bde_api_helper
from src.testcode.common import Constants
import unittest
import logging

#Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
# initialize API helper
api = bde_api_helper.Connection(Constants.SERENGETI_SERVER_IP, '8443')


class DatastoreTest(unittest.TestCase):
    def testAcreateLocalDatastore(self):
        '''
        Create a local datastore. And get this datastore information by its name.
        '''
        createJsonFile = open("../../jsonFile/datastoreJsonFile/datastoreCreateLocal.json")
        try:

            strObject = createJsonFile.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            dsCreated = api.datastores.create(dicObject)
        finally:
            createJsonFile.close()
        # Get a datastore information by its name.
        dsGet = api.datastores.get(instanceName)
        self.assertIsNotNone(dsGet, "dslocalTest does not create successfully! ")
        logger.info(dsGet)

    def testBcreateSharedDatastore(self):
        '''
        Create a shared datastore.
        '''
        createJsonFile = open("../../jsonFile/datastoreJsonFile/datastoreCreateShared.json")
        try:

            strObject = createJsonFile.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            dsCreated = api.datastores.create(dicObject)
        finally:
            createJsonFile.close()
        # Get a datastore information by its name.
        dsGet = api.datastores.get(instanceName)
        self.assertIsNotNone(dsGet, "dssharedTest does not create successfully! ")
        logger.info(dsGet)

    def testCgetDatastores(self):
        '''
        Get all datastores.
        '''
        datastores = api.datastores.getAll()
        logger.info(datastores)
        assert len(datastores) > 0

    def testDdeleteDatastore(self):
        '''
        Delete a datastore.
        '''
        #Delete datastore created at case A.
        api.datastores.delete('dslocalTest')
        #Try to get this datastore by its name, and check whether it's none or not.
        try:
            api.datastores.get('dslocalTest')
        except Exception:
            True
        else:
            False

    @classmethod
    def tearDownClass(self):
        '''
        Create a resourcepool for other test.
        '''
        createJsonFile = open("../../jsonFile/datastoreJsonFile/datastoreCreateLocal.json")
        try:

            strObject = createJsonFile.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            dsCreated = api.datastores.create(dicObject)
        finally:
            createJsonFile.close()
        # Get a datastore information by its name.
        dsGet = api.datastores.get(instanceName)
        logger.info(dsGet)
        assert dsGet is not None





