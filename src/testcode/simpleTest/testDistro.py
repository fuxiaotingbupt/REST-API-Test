__author__ = 'xfu'
#!/usr/bin/env python
# testDistro.py -- Distro related test cases
import unittest
from src.testcode.common.testBase import TestBase


class DistroTest(unittest.TestCase, TestBase):
    '''
    Configure logging and Initialize API connection
    '''
    testBaseInstance = TestBase()
    logger = testBaseInstance.setLogger()
    api = testBaseInstance.initializeAPI()

    def testAgetAllDistros(self):
        '''
        Get all distros' information
        '''
        distros = self.api.distros.getAll()
        self.logger.info(distros)
        self.assertTrue(len(distros) != 0)

    def testBgetDistroByName(self):
        '''
        Get one distro's detail information by its name.
        '''
        distroGeted = self.api.distros.get('apache')
        self.logger.info(distroGeted)
        self.assertIsNotNone(distroGeted, 'There is no distro named with apache')