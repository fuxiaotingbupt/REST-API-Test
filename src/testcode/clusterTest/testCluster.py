#!/usr/bin/env python
# testCluster.py -- Cluster related test cases
import unittest
import logging

#Configure logging
from src.testcode.common import bde_api_helper, Constants

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

# initialize API helper
api = bde_api_helper.Connection(Constants.SERENGETI_SERVER_IP, '8443')


class ClusterTest(unittest.TestCase):
    def testAcreate(self):
        '''
        This is json file for default cluster creation!
        '''
        postFields = {
            "name": "clusterName1",
            "type": "HDFS_MAPRED",
            "rpNames": ["xfu"],
            "networkConfig": {"MGT_NETWORK": ["dhcpNetwork"]},
            "nodeGroups":
                [
                    {
                        "name": "master",
                        "roles":
                            [
                                "hadoop_namenode",
                                "hadoop_jobtracker"
                            ],
                        "instanceNum": 1,
                        "instanceType": "MEDIUM",
                        "storage":
                            {
                                "type": "shared",
                                "sizeGB": 50
                            },
                        "cpuNum": 2,
                        "memCapacityMB": 7500,
                        "swapRatio": 1,
                        "haFlag": "on",
                    },
                    {
                        "name": "worker",
                        "roles":
                            [
                                "hadoop_datanode",
                                "hadoop_tasktracker"
                            ],
                        "instanceNum": 4,
                        "instanceType": "SMALL",
                        "storage":
                            {
                                "type": "local",
                                "sizeGB": 50
                            },
                        "cpuNum": 2,
                        "memCapacityMB": 5000,
                        "swapRatio": 1,
                        "haFlag": "off",
                    },
                    {
                        "name": "client",
                        "roles":
                            [
                                "hadoop_client",
                                "pig",
                                "hive",
                                "hive_server"
                            ],
                        "instanceNum": 1,
                        "instanceType": "SMALL",
                        "storage":
                            {
                                "type": "shared",
                                "sizeGB": 50
                            },
                        "cpuNum": 1,
                        "memCapacityMB": 3748,
                        "swapRatio": 1,
                        "haFlag": "off"
                    }
                ],
            "distro": "apache"
        }
        clusterCreated = api.clusters.create(postFields)
        '''myfile = open("clusterCreate.json")
        clusterCreated = api.clusters.create(myfile)
        myfile.close()
        '''

    def testBGetCluster(self):
        clusterName = 'clusterName1'
        clusterGet = api.clusters.get(clusterName)
        print clusterGet
        assert clusterGet['distro'] == 'apache'

    def testCGetClusters(self):
        clusters = api.clusters.getAll()
        print clusters
        assert clusters.length > 0


if __name__ == '__main__': unittest.main()