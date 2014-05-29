#!/usr/bin/env python
# testCluster.py -- Cluster related test cases
import unittest
import logging
from src.testcode.common import bde_api_helper, Constants

#Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# initialize API helper
api = bde_api_helper.Connection(Constants.SERENGETI_SERVER_IP, '8443')


class ClusterTest(unittest.TestCase):
    def setUp(self):
        self.createJsonFileList = ["../../jsonFile/clusterJsonFile/clusterMRv1Create.json",
                                   "../../jsonFile/clusterJsonFile/clusterMRv2Create.json"]

    def testAcreate(self):
        '''
        Create a default cluster!
        '''
        for createJsonFile in self.createJsonFileList:
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
                self.assertIsNotNone(clusterCreated,'Cluster has not been created!')
            finally:
                createJsonFileToRead.close()

    def testBgetClusters(self):
        '''
        Get all clusters, and the return type should be list and  not be none after test A.
        '''
        allclusters = api.clusters.getAll()
        logger.info(allclusters)
        self.assertTrue(type(allclusters) == list)
        self.assertIsNotNone(allclusters,'There is no clusters.')

    def testCstopCluster(self):
        clusters = api.clusters.getAll()
        if len(clusters) > 0:
            for cluster in clusters:
                if str(cluster['status'])== 'RUNNING':
                    api.clusters.action(cluster['name'],'stop')
                else:
                    logger.info('There is no running cluster to stop!')
        else:
            logger.error('There is no clusters to stop')
  #  def testDstartCluster(self):
