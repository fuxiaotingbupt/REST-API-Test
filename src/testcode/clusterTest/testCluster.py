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
        self.createJsonFileList = [
                                   "../jsonFile/clusterJsonFile/clusterMRv2Create.json"]
    @unittest.skipUnless(Constants.MapReduce_Version!='Mapr','Mapr is different from MRv1 and MRv2')
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
                self.assertIsNotNone(clusterCreated, 'Cluster has not been created!')
            finally:
                createJsonFileToRead.close()

    def testBgetClusters(self):
        '''
        Get all clusters, and the return type should be list and not be none after test A.
        '''
        allclusters = api.clusters.getAll()
        logger.info(allclusters)
        self.assertTrue(type(allclusters) == list)
        self.assertIsNotNone(allclusters, 'There is no clusters.')

    def testCstopCluster(self):
        #Stop a cluster.
        clusters = api.clusters.getAll()
        if len(clusters) > 0:
            for cluster in clusters:
                if str(cluster['status']) == 'RUNNING':
                    api.clusters.action(cluster['name'], 'stop')
                    break
                else:
                    logger.error('There is no running cluster to stop!')
        else:
            logger.error('There is no clusters to stop!')

    def testDstartCluster(self):
        #Start a cluster.
        clusters = api.clusters.getAll()
        if len(clusters) > 0:
            for cluster in clusters:
                if str(cluster['status']) == 'STOPPED':
                    api.clusters.action(cluster['name'], 'start')
                    break
                else:
                    logger.error('There is no stopped cluster to start!')
        else:
            logger.error('There is no clusters to start!')

    def testEgetSpecFile(self):
        #Get one cluster's specfile.
        clusters = api.clusters.getAll()
        if len(clusters) > 0:
            clusterGeted = clusters[0]
            clusterSpec = api.clusters.getSpecFile(clusterGeted['name'], 'spec')
            logger.info(clusterSpec)
        else:
            logger.info('There is no clusters!')

    def testFdeleteCluster(self):
        if (api.clusters.get('cdhMRv2cluster') is not None):
            clusterDeleted = api.clusters.get('cdhMRv2cluster')
            api.clusters.delete(clusterDeleted['name'])
        else:
            logger.error('There is no cluster named cdhMRv2cluster!')
         #Try to get this cluster by its name, and check whether it's none or not.
        try:
            api.clusters.get('cdhMRv2cluster')
        except Exception:
            True
        else:
            False




