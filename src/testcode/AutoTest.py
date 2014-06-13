#!/usr/bin/python
#from DistroTest import DistroTest
#from RPTest import RPTest
import unittest
import sys

from src.testcode.clusterTest.testCluster import ClusterTest
from src.testcode.simpleTest.testDistro import DistroTest
import HTMLTestRunner


def suite():
   suite = unittest.TestSuite()
   test_cases = [DistroTest]
   for testcase in test_cases:
       tests = unittest.TestLoader().loadTestsFromTestCase(testcase)
       suite.addTests(tests)
   return suite
if __name__ == "__main__":
   unittest.main(defaultTest = 'suite', argv = ['--verbose', '-v'])
   fp = file('resttest_report.html', 'wb')
   runner = HTMLTestRunner.HTMLTestRunner(
                                          stream = fp,verbosity = 2,title = 'REST API TEST RESULT',
                                          description = 'This report is for REST API test status.',
                                          )
   result = runner.run(suite())
   sys.exit(not result.wasSuccessful())