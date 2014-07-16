#!/usr/bin/python

import unittest
import sys
from src.testcode.simpleTest.testDistro import DistroTest
from src.testcode.simpleTest.testVersion import VersionTest
from src.testcode.simpleTest.testRack import RackTest
from src.testcode.resourcepoolTest.testResourcePool import ResourcePoolTest
from src.testcode.networkTest.testNetwork import NetworkTest
from src.testcode.clusterTest.testResumeDel import ResumeTest
from src.testcode.datastoreTest.testDatastore import DatastoreTest
from src.testcode.clusterTest.testScale import ScaleTest
from src.testcode.paramTest.testParam import ParamTest
from src.testcode.clusterTest.testCluster import ClusterTest
import HTMLTestRunner


def suite():
   suite = unittest.TestSuite()
   test_cases = [DistroTest,VersionTest,RackTest,ResourcePoolTest,NetworkTest,ResumeTest,DatastoreTest,ParamTest,ScaleTest,ClusterTest]
   for testcase in test_cases:
       tests = unittest.TestLoader().loadTestsFromTestCase(testcase)
       suite.addTests(tests)
   return suite
if __name__ == "__main__":
   fp = file('resttest_report.html', 'wb')
   runner = HTMLTestRunner.HTMLTestRunner(
                                          stream = fp,verbosity = 2,title = 'REST API TEST RESULT',
                                          description = 'This report is for REST API test status.',
                                          )
   result = runner.run(suite())
   sys.exit(not result.wasSuccessful())