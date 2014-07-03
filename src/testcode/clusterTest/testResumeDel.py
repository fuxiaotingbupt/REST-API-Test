#!/usr/bin/env python
# testResumeDel.py --Resume a failed cluster and delete it.
import unittest
import logging
from src.testcode.common import bde_api_helper, constants

#Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# initialize API helper
api = bde_api_helper.Connection(constants.SERENGETI_SERVER_IP, '8443')


class ResumeTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        '''
        Create a small datastore
        '''
        datastoreCreatedFile = open("../../jsonFile/datastoreJsonFile/datastoreCreateSmall.json")
        try:
            strObject = datastoreCreatedFile.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            api.datastores.create(dicObject)
            datastoreGet = api.datastores.get(instanceName)
            assert datastoreGet is not None
        finally:
            datastoreCreatedFile.close()

    def testAresume(self):
        '''
        Create a cluster with large local datastore.
        '''
        createJsonFileToRead = open("../../jsonFile/clusterJsonFile/clusterResume.json")
        try:
            strObject = createJsonFileToRead.read()
            #Generate str to dic
            dicObject = eval(strObject)
            instanceName = dicObject['name']
            try:
                api.clusters.create(dicObject)
            except Exception:
                True
            else:
                False
        finally:
            createJsonFileToRead.close()
        #Add more datastores to BDE, then try to resume this cluster.
        dsPostFields = {
            "name": "dsResume",
            "spec": [
                "bdcqe*"
            ],
            "type": "LOCAL"
        }
        api.datastores.create(dsPostFields)
        clusterNeedResume = api.clusters.get(instanceName)
        self.assertTrue(str(clusterNeedResume['status']) == 'PROVISION_ERROR',
                        'Cluster status is ' + str(clusterNeedResume['status']))
        api.clusters.action(instanceName, 'resume')
        clusterResumed = api.clusters.get(instanceName)
        self.assertTrue(str(clusterResumed['status']) == 'RUNNING')

    def testBdelete(self):
        '''
        Delete this resumed cluster.
        '''
        api.clusters.delete('resume')
        try:
            api.clusters.get('resume')
        except Exception:
            True
        else:
            False

    @classmethod
    def tearDownClass(self):
        '''
        Delete  datastores small and dsResume
        '''
        api.datastores.delete('small')
        api.datastores.delete('dsResume')


