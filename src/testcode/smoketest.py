__author__ = 'xfu'
#!/usr/bin/env python
import unittest
import HTMLTestRunner
from src.testcode.common.testBase import TestBase
from src.testcode.common import Constants
import sys


class SmokeTest(unittest.TestCase, TestBase):
    '''
    Smoke Test related test cases!
    '''
    #ClusterName
    cluster_name = ''
    @classmethod
    def setUp(self):
        '''
        Configure logging and Initialize API connection
        '''
        testBaseInstance = TestBase()
        self.logger = testBaseInstance.setLogger()
        self.api = testBaseInstance.initializeAPI()

    def testAaddgetRP(self):
        '''
        create a resourcepool and get its information
        '''
        #create a rp.
        rpdicObject = self.getJsonFile("../jsonFile/resourcepoolJsonFile/rpCreate.json")
        self.api.resourcepools.create(rpdicObject)
        #get a resourcepool information by its name.
        rpinstanceName = rpdicObject['name']
        rpGet = self.api.resourcepools.get(rpinstanceName)
        self.assertIsNotNone(rpGet, "rpCreate does not create successfully! ")
        self.logger.info(rpGet)

    def testBaddgetNet(self):
        '''
        create a dhcp network and get its information
        '''
        #create dhcp network
        netdicObject = self.getJsonFile("../jsonFile/networkJsonFile/networkCreateDHCP.json")
        self.api.networks.create(netdicObject)
        #get dhcp network detail information by its name
        netinstanceName = netdicObject['name']
        netGet = self.api.networks.get(netinstanceName)
        self.assertIsNotNone(netGet, "dhcpNetwork does not create successfully! ")
        self.logger.info(netGet)

    def testCaddgetDs(self):
        '''
        create a local and shared datastores, then get their information.
        '''
        #create local and shared datastores.
        dsSpecfiles = ["../jsonFile/datastoreJsonFile/datastoreCreateLocal.json",
                       "../jsonFile/datastoreJsonFile/datastoreCreateShared.json"]
        for file in dsSpecfiles:
            localdsdicObject = self.getJsonFile(file)
            localdsinstanceName = localdsdicObject['name']
            self.api.datastores.create(localdsdicObject)
            # Get a datastore information by its name.
            dsGet = self.api.datastores.get(localdsinstanceName)
            self.assertIsNotNone(dsGet, "dsTest does not create successfully! ")
            self.logger.info(dsGet)
    def testDaddmanagers(self):
        '''
        Add a cloudera manager!
        '''
        createJsonFile = self.getJsonFile("../jsonFile/appManagerJsonFile/cmAdd.json")
        self.api.appManagers.create(createJsonFile)
        appmanagerName = createJsonFile['name']
        appmanagerGet = self.api.appManagers.get(appmanagerName)
        self.assertIsNotNone(appmanagerGet,"Appmanager cm create successfully!")
        self.logger.info(appmanagerGet)

    @unittest.skipUnless(Constants.MapReduce_Version != 'Mapr', 'Mapr is different from MRv1 and MRv2')
    def testDcreateCluster(self):
        '''
        create a default cluster, then get its detail information.
        '''
        #create a cluster
        if Constants.MapReduce_Version == 'mrv1':
            clusterdicObject = self.getJsonFile("../jsonFile/clusterJsonFile/clusterMRv1Create.json")
        elif Constants.MapReduce_Version == 'mrv2':
            clusterdicObject = self.getJsonFile("../jsonFile/clusterJsonFile/clusterMRv2Create.json")
        else:
            self.logger.info("Need add mapr cluster create code!")
        self.api.clusters.create(clusterdicObject)
        #get cluster detail information by its name.
        clusterinstanceName = clusterdicObject['name']
        clusterGet = self.api.clusters.get(clusterinstanceName)
        self.assertIsNotNone(clusterGet, "cluster does not create successfully! ")
        self.assertTrue(clusterGet['status'] == 'RUNNING')
        self.logger.info(clusterGet)

    def testEscaleOut(self):
        '''
        Resize worker nodegroup, instance from 2 to 3.
        '''
        resizeNum = 3
        clusters = self.api.clusters.getAll()
        SmokeTest.cluster_name = clusters[0]['name']
        self.api.clusters.scale(self.cluster_name, 'worker', 'instancenum', resizeNum)
        #Verify whether node group is resized successfully.
        cluster = self.api.clusters.get(self.cluster_name)
        nodegroups = cluster['nodeGroups']
        for nodegroup in nodegroups:
            if nodegroup['name'] == 'worker':
                nodegroupNeeded = nodegroup
                break
            else:
                self.logger.error('There is no nodegroup ' + 'worker')
        self.logger.info(nodegroupNeeded)
        self.assertTrue(nodegroupNeeded['instanceNum'] == resizeNum, 'Resize node failed!')

    def testFscaleUpCPU(self):
        '''
        Scale up worker nodegroup cpu from 2 to 3.
        '''
        cpuNumberUp = 3
        putFields = {
            "clusterName": self.cluster_name,
            "nodeGroupName": 'worker',
            "cpuNumber": cpuNumberUp
        }
        self.api.clusters.scale(self.cluster_name, 'worker', 'scale', putFields)
        #Verify whether cpu is scaled up.
        cluster = self.api.clusters.get(self.cluster_name)
        nodegroups = cluster['nodeGroups']
        for nodegroup in nodegroups:
            if nodegroup['name'] == 'worker':
                nodegroupNeeded = nodegroup
                break
            else:
                self.logger.error('There is no nodegroup ' + 'worker')
        self.logger.info(nodegroupNeeded)
        self.assertTrue(nodegroupNeeded['cpuNum'] == cpuNumberUp, 'Scale up cpu node failed!')

    def testGscaleDownCPU(self):
        '''
        Scale down worker nodegroup cpu from 3 to 1.
        '''
        cpuNumberDown = 1
        putFields = {
            "clusterName": self.cluster_name,
            "nodeGroupName": 'worker',
            "cpuNumber": cpuNumberDown
        }
        self.api.clusters.scale(self.cluster_name, 'worker', 'scale', putFields)
        #Verify whether cpu is scaled down.
        cluster = self.api.clusters.get(self.cluster_name)
        nodegroups = cluster['nodeGroups']
        for nodegroup in nodegroups:
            if nodegroup['name'] == 'worker':
                nodegroupNeeded = nodegroup
                break
            else:
                self.logger.error('There is no nodegroup ' + 'worker')
        self.logger.info(nodegroupNeeded)
        self.assertTrue(nodegroupNeeded['cpuNum'] == cpuNumberDown, 'Scale down cpu node failed!')

    def testHscaleUpMEM(self):
        '''
        Scale up client nodegroup mem from 3748 to 4000.
        '''
        memUp = 4000
        putfields = {
            "clusterName": self.cluster_name,
            "nodeGroupName": 'client',
            "memory": memUp
        }
        self.api.clusters.scale(self.cluster_name, 'client', 'scale', putfields)
        #Verify whether mem is scaled up successfully.
        cluster = self.api.clusters.get(self.cluster_name)
        nodegroups = cluster['nodeGroups']
        for nodegroup in nodegroups:
            if nodegroup['name'] == 'client':
                nodegroupNeeded = nodegroup
                break
            else:
                self.logger.error('There is no nodegroup ' + 'client')
        self.logger.info(nodegroupNeeded)
        self.assertTrue(nodegroupNeeded['memCapacityMB'] == memUp, 'Scale up mem node failed!')

    def testIscaleDownMEM(self):
        '''
        Scale down worker nodegroup mem from 5000 to 4000.
        '''
        memDown = 4000
        putfields = {
            "clusterName": self.cluster_name,
            "nodeGroupName": 'worker',
            "memory": memDown
        }
        self.api.clusters.scale(self.cluster_name, 'worker', 'scale', putfields)
        #Verify whether mem is scaled down successfully.
        cluster = self.api.clusters.get(self.cluster_name)
        nodegroups = cluster['nodeGroups']
        for nodegroup in nodegroups:
            if nodegroup['name'] == 'worker':
                nodegroupNeeded = nodegroup
                break
            else:
                self.logger.error('There is no nodegroup ' + 'worker')
        self.logger.info(nodegroupNeeded)
        self.assertTrue(nodegroupNeeded['memCapacityMB'] == memDown, 'Scale down mem node failed!')

    def testJstopCluster(self):
        '''
        Stop a cluster.
        '''
        clusters = self.api.clusters.getAll()
        if len(clusters) > 0:
            for cluster in clusters:
                if str(cluster['status']) == 'RUNNING':
                    self.api.clusters.action(cluster['name'], 'stop')
                    break
                else:
                    self.logger.error('There is no running cluster to stop!')
        else:
            self.logger.error('There is no clusters to stop!')

    def testKstartCluster(self):
        '''
        Start a cluster.
        '''
        clusters = self.api.clusters.getAll()
        if len(clusters) > 0:
            for cluster in clusters:
                if str(cluster['status']) == 'STOPPED':
                    self.api.clusters.action(cluster['name'], 'start')
                    break
                else:
                    self.logger.error('There is no stopped cluster to start!')
        else:
            self.logger.error('There is no clusters to start!')

    def testLdeleteCluster(self):
        '''
        Delete a cluster.
        '''
        clusters = self.api.clusters.getAll()
        for cluster in clusters:
            self.api.clusters.delete(cluster['name'])
            #Try to get this cluster by its name, and check whether it's none or not.
        clustersAll = self.api.clusters.getAll()
        self.assertTrue(len(clustersAll) == 0)

    def testMdeleteDS(self):
        '''
        Delete all datastores.
        '''
        datastores = self.api.datastores.getAll()
        for datastore in datastores:
            self.api.datastores.delete(datastore['name'])
        datastoresAll = self.api.datastores.getAll()
        self.assertTrue(len(datastoresAll) == 0)

    def testNdeleteNet(self):
        '''
        Delete all networks.
        '''
        networks = self.api.networks.getAll()
        for network in networks:
            self.api.networks.delete(network['name'])
        networksAll = self.api.networks.getAll()
        self.assertTrue(len(networksAll) == 0)

    def testOdeleteRP(self):
        '''
        Delete all rp.
        '''
        rps = self.api.resourcepools.getAll()
        for rp in rps:
            self.api.resourcepools.delete(rp['rpName'])
        rpsAll = self.api.resourcepools.getAll()
        self.assertTrue(len(rpsAll) == 0)


def suite():
    suite = unittest.TestSuite()
    test_cases = [SmokeTest]
    for testcase in test_cases:
        tests = unittest.TestLoader().loadTestsFromTestCase(testcase)
        suite.addTests(tests)
    return suite


if __name__ == '__main__':
    fp = file('resttest_report.html', 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp, verbosity=2, title='REST API TEST RESULT',
        description='This report is for REST API test status.',
    )
    result = runner.run(suite())
    sys.exit(not result.wasSuccessful())

