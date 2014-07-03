#!/bin/bash
set -e

QE_UNTAR_NAME="aurora-qe-test"
PYTHON_CODE_PATH="${WORKSPACE}/src/testcode
#Set python path
export PYTHONPATH=${WORKSPACE}

#Get serengeti server ip and vc username/password from aurora-bdc-connection.json
cd ${WORKSPACE}/${QE_UNTAR_NAME}
pwd
SERENGETI_SERVER_IP = 'cat aurora-bdc-connection.json |grep systemUrl |cut -d '"' -f4 |cut -d ':' -f1'
cd $PYTHON_CODE_PATH/common/
pwd
sed -i 's/SERENGETI_SERVER_IP=.*/SERENGETI_SERVER_IP=10.111.57.91/g' $PYTHON_CODE_PATH/common/constants.py
#VC_USERNAME should be base64 encoded.
#VC_USERNAME =
#VC_PASSWORD =

#Execute rest api test cases
cd $PYTHON_CODE_PATH
python AutoTest.py
