__author__ = 'xfu'
#!/usr/bin/env python
#Filename:testAppmanager.py
import unittest
from src.testcode.common.testBase import TestBase
from src.testcode.common import Constants


class AppmanagerTest(unittest.TestCase, TestBase):
    '''
    Configure logging and Initialize API connection
    '''
    testBaseInstance = TestBase()
    logger = testBaseInstance.setLogger()
    api = testBaseInstance.initializeAPI()

    def test_A_addApp(self):
        '''
        Add clourdera manager into serengeti server!
        '''
        createJsonFile = self.testBaseInstance.getJsonFile("../../jsonFile/appManagerJsonFile/cmAdd.json")
        instanceName = createJsonFile['name']
        self.api.appManagers.create(createJsonFile)
        appmanagerLists = self.api.appManagers.getAll()
        for appmanager in appmanagerLists:
            if appmanager['name'] == instanceName:
                assert True
                break
        else:
            assert False
    def test_B_appAll(self):
        '''
        Get all appmanagers.
        '''
        appmanagerLists = self.api.appManagers.getAll()
        self.logger.info(appmanagerLists)

    def test_C_appTypes(self):
        '''
        Get all  types that server can supported.
        '''
        appmanagerType = self.api.appManagers.getAppmangerTypes()
        self.logger.info(appmanagerType)
        self.assertIn('ClouderaManager', appmanagerType, 'ClouderaManager is in appmanagerType.')
        self.assertIn('Ambari', appmanagerType, 'Ambari is in appmanagerType.')

    def test_D_defaultAppDistros(self):
        '''
        Get default appmanager's distros.
        '''
        appmanagerName = 'Default'
        defaultDistros = self.api.appManagers.getAppmanagerDistros(appmanagerName)
        self.logger.info(defaultDistros)

    def test_E_distroConf(self):
        '''
        Get default appmanager's distros' configuration.
        '''
        distroConf = self.api.appManagers.getAppmanagerDistroConf('Default', Constants.DistroName)
        self.logger.info(distroConf)

    def test_F_distroRoles(self):
        '''
        Get default appmanager's distros' roles.
        '''
        distroRoles = self.api.appManagers.getAppmanagerDistroRoles('Default', Constants.DistroName)
        self.logger.info(distroRoles)
    def test_G_deleteAppmanager(self):
        '''
        Delete appmanager.
        '''
        self.api.appManagers.delete('cm')




