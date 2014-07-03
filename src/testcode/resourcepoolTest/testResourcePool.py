__author__ = 'xfu'
#!/usr/bin/env python
# testResourcePool.py -- ResourcePool related test cases
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


class ResourcePoolTest(unittest.TestCase):

    def testAcreateResourcePool(self):
        '''
        Create a resourcepool. And get this resourcepool information by its name.
        '''
        createJsonFile= open("../../jsonFile/resourcepoolJsonFile/rpCreate.json")
        try:

            strObject = createJsonFile.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            rpCreated = api.resourcepools.create(dicObject)
        finally:
            createJsonFile.close()
        # Get a resourcepool information by its name.
        rpGet = api.resourcepools.get(instanceName)
        self.assertIsNotNone(rpGet, "rpCreate does not create successfully! ")
        logger.info(rpGet)

    def testBgetResourcePools(self):
        '''
        Get all rps.
        '''
        rps = api.resourcepools.getAll()
        logger.info(rps)
        assert len(rps) > 0

    def testCdeleteResourcePool(self):
        '''
        Delete a resourcepool.
        '''
        #Delete rp created at case A.
        api.resourcepools.delete('rpCreate')
        #Try to get this network by its name, and check whether it's none or not.
        try:
            api.resourcepools.get('rpCreate')
        except Exception:
            True
        else:
            False
    @classmethod
    def tearDownClass(self):
        '''
        Create a resourcepool for other test.
        '''
        createJsonFile= open("../../jsonFile/resourcepoolJsonFile/rpCreate.json")
        try:

            strObject = createJsonFile.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            rpCreated = api.resourcepools.create(dicObject)
        finally:
            createJsonFile.close()
        # Get a resourcepool information by its name.
        rpGet = api.resourcepools.get(instanceName)
        logger.info(rpGet)
        assert rpGet is not None




