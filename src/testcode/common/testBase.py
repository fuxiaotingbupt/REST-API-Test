__author__ = 'xfu'
#!/usr/bin/env python
# testBase.py
from src.testcode.common import bde_api_helper
from src.testcode.common import Constants
import logging



# initialize API helper
api = bde_api_helper.Connection(Constants.SERENGETI_SERVER_IP, '8443')


class TestBase():
    #Configure logging
    def setLogger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler())
        return logger

    #initialize API helper
    def initializeAPI(self):
        api = bde_api_helper.Connection(Constants.SERENGETI_SERVER_IP, '8443')
        return api

    def getJsonFile(self, jsonFile):
        createJsonFile = open(jsonFile)
        try:
            strObject = createJsonFile.read()
            #Generate str to dic
            dicObject = eval(strObject)
        finally:
            createJsonFile.close()
        return dicObject

