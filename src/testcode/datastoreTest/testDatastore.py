__author__ = 'xfu'
#!/usr/bin/env python
# testDatastore.py -- Datastore related test cases
from src.testcode.common import bde_api_helper
from src.testcode.common import constants
from src.testcode.common.testBase import TestBase
import unittest

class DatastoreTest(unittest.TestCase):
    '''
    Configure logging and Initialize API connection
    '''
    testBaseInstance = TestBase()
    logger = testBaseInstance.setLogger()
    api = testBaseInstance.initializeAPI()

    def testAcreateLocalDatastore(self):
        '''
        Create a local datastore. And get this datastore information by its name.
        '''
        createJsonFile = self.testBaseInstance.getJsonFile("../../jsonFile/datastoreJsonFile/datastoreCreateLocal.json")
        instanceName = createJsonFile['name']
        dsCreated = self.api.datastores.create(createJsonFile)
        # Get a datastore information by its name.
        dsGet = self.api.datastores.get(instanceName)
        self.assertIsNotNone(dsGet, "dslocalTest does not create successfully! ")
        self.logger.info(dsGet)

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
            dsCreated = self.api.datastores.create(dicObject)
        finally:
            createJsonFile.close()
        # Get a datastore information by its name.
        dsGet = self.api.datastores.get(instanceName)
        self.assertIsNotNone(dsGet, "dssharedTest does not create successfully! ")
        self.logger.info(dsGet)

    def testCgetDatastores(self):
        '''
        Get all datastores.
        '''
        datastores = self.api.datastores.getAll()
        self.logger.info(datastores)
        assert len(datastores) > 0

    def testDdeleteDatastore(self):
        '''
        Delete a datastore.
        '''
        #Delete datastore created at case A.
        self.api.datastores.delete('dslocalTest')
        #Try to get this datastore by its name, and check whether it's none or not.
        try:
            self.api.datastores.get('dslocalTest')
        except Exception:
            True
        else:
            False

    @classmethod
    def tearDownClass(self):
        '''
        Create a datastore for other test.
        '''
        createJsonFile = open("../../jsonFile/datastoreJsonFile/datastoreCreateLocal.json")
        try:

            strObject = createJsonFile.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            dsCreated = self.api.datastores.create(dicObject)
        finally:
            createJsonFile.close()
        # Get a datastore information by its name.
        dsGet = self.api.datastores.get(instanceName)
        self.logger.info(dsGet)
        assert dsGet is not None





