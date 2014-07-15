#!/usr/bin/env python
# testParam.py -- Change elasticity mode, IO priority, and maximum or minimum number of powered on compute nodes under auto mode.
import unittest
import logging
from src.testcode.common import bde_api_helper, Constants

#Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# initialize API helper
api = bde_api_helper.Connection(Constants.SERENGETI_SERVER_IP, '8443')
clusterName = 'cdhMRv1cluster'


class ParamTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''
        Create a default cluster!
        '''
        createJsonFile = "../jsonFile/clusterJsonFile/clusterMRv1Create.json"
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
            assert clusterCreated is not None
        finally:
            createJsonFileToRead.close()

    def testAParam(self):
        '''
        Change elasticity mode, IO priority, and maximum or minimum number of powered on compute nodes under auto mode.
        '''
        putFields = {
            "minComputeNodeNum": 1,
            "activeComputeNodeNum": 1,
            "enableAuto": "true",
            "ioPriority": "HIGH"
        }
        api.clusters.param(clusterName, 'param', putFields)

    def testBasyncSetParam(self):
        '''
        Turn on or off some compute nodes.
        '''
        putFields = {
            "minComputeNodeNum": 1,
            "activeComputeNodeNum": 2,
            "enableAuto": "false",
            "ioPriority": "NORMAL"
        }
        api.clusters.param(clusterName, 'param_wait_for_result', putFields)


    @classmethod
    def tearDownClass(self):
        #Delete clusters
        clusterDeleted = api.clusters.get(clusterName)
        if str(clusterDeleted['status']) in ['RUNNING', 'STOPPED', 'ERROR', 'PROVISION_ERROR',
                                             'CONFIGURE_ERROR' or 'UPGRADE_ERROR']:
            api.clusters.delete(clusterName)
        else:
            logger.error(
                'Cluster ' + clusterName + ' status is ' + str(clusterDeleted['status'] + ' can not been deleted!'))