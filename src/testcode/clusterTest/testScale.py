#!/usr/bin/env python
# testScale.py -- Scale out nodegroup and scale up/down cpu/mem.
import unittest
import logging
from src.testcode.common import bde_api_helper, constants

#Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# initialize API helper
api = bde_api_helper.Connection(constants.SERENGETI_SERVER_IP, '8443')
clusterName = 'cdhMRv1cluster'
nodegroupName = 'worker'
clientnodegroupName = 'client'


class ScaleTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''
        Create a default cluster!
        '''
        global clusterTodo
        createJsonFile = "../../jsonFile/clusterJsonFile/clusterMRv1Create.json"
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
        self.clusterTodo = api.clusters.get(instanceName)

    def testAscaleOut(self):
        '''
        Resize worker nodegroup, instance from 2 to 3.
        '''
        resizeNum = 3
        api.clusters.scale(clusterName, nodegroupName, 'instancenum', resizeNum)
        #Verify whether node group is resized successfully.
        cluster = api.clusters.get(clusterName)
        nodegroups = cluster['nodeGroups']
        for nodegroup in nodegroups:
            if nodegroup['name'] == nodegroupName:
                nodegroupNeeded = nodegroup
                break
            else:
                logger.error('There is no nodegroup ' + nodegroupName)
        logger.info(nodegroupNeeded)
        self.assertTrue(nodegroupNeeded['instanceNum'] == resizeNum, 'Resize node failed!')

    def testBscaleUpCPU(self):
        '''
        Scale up worker nodegroup cpu from 2 to 3.
        '''
        cpuNumberUp = 3
        putFields = {
            "clusterName": clusterName,
            "nodeGroupName": nodegroupName,
            "cpuNumber": cpuNumberUp
        }
        api.clusters.scale(clusterName, nodegroupName, 'scale', putFields)
        #Verify whether cpu is scaled up.
        cluster = api.clusters.get(clusterName)
        nodegroups = cluster['nodeGroups']
        for nodegroup in nodegroups:
            if nodegroup['name'] == nodegroupName:
                nodegroupNeeded = nodegroup
                break
            else:
                logger.error('There is no nodegroup ' + nodegroupName)
        logger.info(nodegroupNeeded)
        self.assertTrue(nodegroupNeeded['cpuNum'] == cpuNumberUp, 'Scale up cpu node failed!')

    def testCscaleDownCPU(self):
        '''
        Scale down worker nodegroup cpu from 3 to 1.
        '''
        cpuNumberDown = 1
        putFields = {
            "clusterName": clusterName,
            "nodeGroupName": nodegroupName,
            "cpuNumber": cpuNumberDown
        }
        api.clusters.scale(clusterName, nodegroupName, 'scale', putFields)
        #Verify whether cpu is scaled down.
        cluster = api.clusters.get(clusterName)
        nodegroups = cluster['nodeGroups']
        for nodegroup in nodegroups:
            if nodegroup['name'] == nodegroupName:
                nodegroupNeeded = nodegroup
                break
            else:
                logger.error('There is no nodegroup ' + nodegroupName)
        logger.info(nodegroupNeeded)
        self.assertTrue(nodegroupNeeded['cpuNum'] == cpuNumberDown, 'Scale down cpu node failed!')

    def testDscaleUpMEM(self):
        '''
        Scale up client nodegroup mem from 3748 to 4000.
        '''
        memUp = 4000
        putfields = {
            "clusterName": clusterName,
            "nodeGroupName": clientnodegroupName,
            "memory": memUp
        }
        api.clusters.scale(clusterName, clientnodegroupName, 'scale', putfields)
        #Verify whether mem is scaled up successfully.
        cluster = api.clusters.get(clusterName)
        nodegroups = cluster['nodeGroups']
        for nodegroup in nodegroups:
            if nodegroup['name'] == clientnodegroupName:
                nodegroupNeeded = nodegroup
                break
            else:
                logger.error('There is no nodegroup ' + clientnodegroupName)
        logger.info(nodegroupNeeded)
        self.assertTrue(nodegroupNeeded['memCapacityMB'] == memUp, 'Scale up mem node failed!')

    def testEscaleDownMEM(self):
        '''
        Scale down worker nodegroup mem from 5000 to 4000.
        '''
        memDown = 4000
        putfields = {
            "clusterName": clusterName,
            "nodeGroupName": nodegroupName,
            "memory": memDown
        }
        api.clusters.scale(clusterName, nodegroupName, 'scale', putfields)
        #Verify whether mem is scaled down successfully.
        cluster = api.clusters.get(clusterName)
        nodegroups = cluster['nodeGroups']
        for nodegroup in nodegroups:
            if nodegroup['name'] == nodegroupName:
                nodegroupNeeded = nodegroup
                break
            else:
                logger.error('There is no nodegroup ' + nodegroupName)
        logger.info(nodegroupNeeded)
        self.assertTrue(nodegroupNeeded['memCapacityMB'] == memDown, 'Scale down mem node failed!')

    @classmethod
    def tearDownClass(self):
        #Delete clusters
        clusterDeleted = api.clusters.get(clusterName)
        if str(clusterDeleted['status']) in ['RUNNING', 'STOPPED', 'ERROR', 'PROVISION_ERROR', 'CONFIGURE_ERROR' or 'UPGRADE_ERROR']:
            api.clusters.delete(clusterName)
        else:
            logger.error('Cluster ' + clusterName + ' status is ' + str(clusterDeleted['status'] + ' can not been deleted!'))