__author__ = 'xfu'
#!/usr/bin/env python
#Filename:testADLDAP.py
import unittest
from src.testcode.common.testBase import TestBase
from src.testcode.common import Constants
from src.testcode.adldapTest.BDEException import BDEException


class ADLDAPTest(unittest.TestCase, TestBase):
    '''
    Configure logging and Initialize API connection
    '''
    testBaseInstance = TestBase()
    logger = testBaseInstance.setLogger()
    api = testBaseInstance.initializeAPI()

    def test_A_addAccountServer(self):
        '''
        Add an account management server (AD/LDAP)
        '''
        createJsonFile = self.testBaseInstance.getJsonFile("../../jsonFile/adldapJsonFile/adServerAdd.json")
        instanceName = createJsonFile['name']
        self.api.accountServers.create(createJsonFile)
        accountServerGet = self.api.accountServers.get(createJsonFile['name'])
        if accountServerGet is not None:
            assert True
        else:
            assert False

    def test_B_getAccountServers(self):
        '''
        Get an account management server
        '''
        accountServer= self.api.accountServers.get('ldapxfu')
        self.assertIsNotNone(accountServer)
        self.logger.info(accountServer)

    def test_C_confGetMgmtVM(self):
        '''
        Configure Management VM and get configurations.
        '''
        putJsonFile = self.testBaseInstance.getJsonFile("../../jsonFile/adldapJsonFile/configuremgmtvm.json")
        self.api.mgmtvm.put(putJsonFile)
        mgmtVMconfGet = self.api.mgmtvm.get()
        self.assertTrue(mgmtVMconfGet['vmconfig.mgmtvm.cum.servername'] == putJsonFile['vmconfig.mgmtvm.cum.servername'])
#Error handling for ad/ldap server adding
    def test_D_duplicatedName(self):
        '''
        Add an another ad/ldap server with a duplicated name.
        '''
        createJsonFile = self.testBaseInstance.getJsonFile("../../jsonFile/adldapJsonFile/adServerAdd.json")
        instanceName = createJsonFile['name']
        try:
            response = self.api.accountServers.create(createJsonFile)
            print response.read()
            print response
        except BDEException, e:
            print e










