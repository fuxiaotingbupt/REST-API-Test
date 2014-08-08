#!/usr/bin/env python
# testCluster.py -- Cluster related test cases
import unittest
import logging
from src.testcode.common import bde_api_helper, Constants
import os

#Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# initialize API helper
api = bde_api_helper.Connection(Constants.SERENGETI_SERVER_IP, '8443')


class HbaseOnlyTest(unittest.TestCase):
    def setUp(self):
        self.createDefaultHbaseJsonFileList = [
                                   "../../jsonFile/clusterJsonFile/clusterDefaultHbase.json"]
    def testAcreateDefaultHbase(self):
        '''
        Create a default hbase cluster!
        '''
        for createJsonFile in self.createDefaultHbaseJsonFileList:
            createJsonFileToRead = open(createJsonFile)
            try:
                strObject = createJsonFileToRead.read()
                #Generate str to dic
                dicObject = eval(strObject)
                instanceName = dicObject['name']
                api.clusters.create(dicObject)
                #Get this newly created cluster by cluster name.
                clusterCreated = api.clusters.get(instanceName)
                logger.info(clusterCreated)
                self.assertIsNotNone(clusterCreated, 'Cluster has not been created!')
            finally:
                createJsonFileToRead.close()

    def testBcreateHbaseOnly(self):
        '''
        Create a hbase only cluster.
        '''
        masterInstance = ''
        allclusters = api.clusters.getAll()
        allinstances = allclusters[0]['nodeGroups']
        for instance in allinstances:
            if instance['name'] == 'master':
                masterInstance = instance
                break
        else:
            logger.error('There is no master node group!')
        ipAddress = masterInstance['instances'][0]['ipConfigs']['MGT_NETWORK'][0]['ipAddress'].strip()
        logger.info(ipAddress)
        os.system("sed -i 's/hostname-of-namenode/"+ipAddress+"'" + " clusterHbaseOnly.json")
        #create a hbase only cluster.
        createJsonFileToRead = open("clusterHbaseOnly.json")
        try:
            strObject = createJsonFileToRead.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            api.clusters.create(dicObject)
        finally:
            createJsonFileToRead.close()
        clusterCreated = api.clusters.get(instanceName)
        self.assertTrue(clusterCreated['status']=='RUNNING')










