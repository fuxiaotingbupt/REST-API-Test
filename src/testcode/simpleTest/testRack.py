
#!/usr/bin/env python
# testRack.py -- Rack related test cases
from src.testcode.common import bde_api_helper
from src.testcode.common import Constants
import logging
import unittest


#Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
# initialize API helper
api = bde_api_helper.Connection(Constants.SERENGETI_SERVER_IP, '8443')

class RackTest(unittest.TestCase):
    '''
    Store rack list information into BDE for rack related support, such as hadoop rack awareness and node placement policies.
    '''
    def testAputRacks(self):
        putJsonFile = open("../jsonFile/rackJsonFile/rackPut.json")
        try:
            strObject = putJsonFile.read()
            #Generate str to dic
            dicObject = eval(strObject)
            api.racks.put(dicObject)
        finally:
            putJsonFile.close()
    def testBgetRacks(self):
        racks = api.racks.getAll()
        logger.info(racks)
        self.assertTrue(len(racks) != 0)
        logger.info(len(racks))


