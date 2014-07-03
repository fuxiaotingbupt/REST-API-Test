#!/usr/bin/env python
# testNetwork.py -- Network related test cases
from src.testcode.common import bde_api_helper
from src.testcode.common import constants
import unittest
import logging
import json

#Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
# initialize API helper
api = bde_api_helper.Connection(constants.SERENGETI_SERVER_IP, '8443')


class NetworkTest(unittest.TestCase):
    def testAcreateDHCPNetwork(self):
        '''
        Create a dhcp network. And get this network information by its name.
        '''
        createJsonFileDHCP = open("../../jsonFile/networkJsonFile/networkCreateDHCP.json")
        try:

            strObject = createJsonFileDHCP.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            networkCreated = api.networks.create(dicObject)
        finally:
            createJsonFileDHCP.close()
        # Get a network information by its name.
        networkGet = api.networks.get(instanceName)
        self.assertIsNotNone(networkGet, "dhcpNetwork does not create successfully! ")
        logger.info(networkGet)

    def testBcreateStaticNetork(self):
        '''
        Create a  static network.
        '''
        createJsonFileStatic = open("../../jsonFile/networkJsonFile/networkCreateStatic.json")
        try:

            strObject = createJsonFileStatic.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            networkCreated = api.networks.create(dicObject)
        finally:
            createJsonFileStatic.close()
        # Get a network information by its name.
        networkGet = api.networks.get(instanceName)
        self.assertIsNotNone(networkGet, "staticNetwork does not create successfully! ")
        logger.info(networkGet)

    def testCgetNetworks(self):
        '''
        Get all networks.
        '''
        networks = api.networks.getAll()
        logger.info(networks)
        assert len(networks) > 0

    def testDputNetwork(self):
        '''
        Add ips into an existing BDE network.
        '''
        updateJsonFile = open("../../jsonFile/networkJsonFile/networkUpdate.json")
        try:

            strObject = updateJsonFile.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            ipBlocks = dicObject['ipBlocks']
            logger.info(ipBlocks)
            #add a new sub network ip range.
            api.networks.put(instanceName, dicObject)
        finally:
            updateJsonFile.close()
        # Get this updated network information
        networkUpdated = api.networks.get(instanceName)
        logger.info(networkUpdated)
        ipBlocksUpdated = networkUpdated['allIpBlocks']
        logger.info(ipBlocksUpdated)
        #Delete 'u' from list to str
        ipBlocksUpdatedlist = eval(json.dumps(ipBlocksUpdated))
        for i in ipBlocks:
            self.assertTrue(i in ipBlocksUpdatedlist, 'Network has not been updated successfully!')


    def testEdeleteNetwork(self):
        '''
        Delete a network
        '''
        #Create a dhcp network and delete it
        createJsonFileDHCP = open("../../jsonFile/networkJsonFile/networkCreateForDelete.json")
        try:

            strObject = createJsonFileDHCP.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            networkCreated = api.networks.create(dicObject)
        finally:
            createJsonFileDHCP.close()
        #Delete this newly added network.
        api.networks.delete(instanceName)
        #Try to get this network by its name, and check whether it's none or not.
        try:
            api.networks.get(instanceName)
        except Exception:
            True
        else:
            False


