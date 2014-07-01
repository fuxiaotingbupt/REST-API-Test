!#/bin/bash
set -e

#Set python path
export PYTHONPATH=/Users/xfu/PycharmProjects/REST-API-Test

#Get serengeti server ip and vc username/password for aurora-bdc-connection.json
SERENGETI_SERVER_IP = cat aurora-bdc-connection.json |grep systemUrl |cut -d '"' -f4 |cut -d ':' -f1
#VC_USERNAME should be base64 encoded.
#VC_USERNAME =
#VC_PASSWORD =

#Execute rest api test cases
python AutoTest.py
