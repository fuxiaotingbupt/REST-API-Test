__author__ = 'xfu'
#!/usr/bin/env python
#Filename:testAppmanager.py
import unittest
from src.testcode.common.testBase import TestBase
from src.testcode.common import Constants
class AppmanagerTest(unittest.TestCase,TestBase):
    '''
    Configure logging and Initialize API connection
    '''
    testBaseInstance = TestBase()
    logger = testBaseInstance.setLogger()
    api = testBaseInstance.initializeAPI()
    def test_B_appAll(self):
        appmanagerLists = self.api.appManagers.getAll()
        self.logger.info(appmanagerLists)
    def test_C_appTypes(self):
        appmanagerType = self.api.appManagers.getAppmangerTypes()
        self.logger.info(appmanagerType)
        self.assertIn('ClouderaManager',appmanagerType,'ClouderaManager is in appmanagerType.')
        self.assertIn('Ambari',appmanagerType,'Ambari is in appmanagerType.')
    def test_D_defaultAppDistros(self):
        appmanagerName = 'Default'
        defaultDistros = self.api.appManagers.getAppmanagerDistros(appmanagerName)
        self.logger.info(defaultDistros)
    def test_E_distroConf(self):
        distroConf = self.api.appManagers.getAppmanagerDistroConf('Default',Constants.DistroName)
        self.logger.info(distroConf)
    def test_F_distroRoles(self):
        distroRoles = self.api.appManagers.getAppmanagerDistroRoles('Default',Constants.DistroName)
        self.logger.info(distroRoles)
if __name__=='__main__':
    unittest.main()