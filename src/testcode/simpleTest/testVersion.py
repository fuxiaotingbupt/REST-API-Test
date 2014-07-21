__author__ = 'xfu'
#!/usr/bin/env python
# testVersion.py -- Version related test cases
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

class VersionTest(unittest.TestCase):
    def testGetVersion(self):
        '''
        Get rest api version.
        '''
        version = api.versions.getVersion()
        logger.info(version)
        self.assertTrue(version=='2.1.0','REST API version is not 2.0.0')