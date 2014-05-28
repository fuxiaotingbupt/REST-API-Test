__author__ = 'xfu'
#!/usr/bin/env python
# testDistro.py -- Distro related test cases
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

class DistroTest(unittest.TestCase):
    def testAgetAllDistros(self):
        '''
        Get all distros' information
        '''
        distros = api.distros.getAll()
        logger.info(distros)
        self.assertTrue(len(distros) != 0)
    def testBgetDistroByName(self):
        '''
        Get one distro's detail information by its name.
        '''
        distroGeted = api.distros.get('apache')
        logger.info(distroGeted)
        self.assertIsNotNone(distroGeted,'There is no distro named with apache')