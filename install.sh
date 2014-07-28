#!/bin/bash
#FileName: install.sh
#Usage:./install.sh distroName testsuite
set -e
WORKSPACE=/var/lib/jenkins/workspace/SmokeN-RESTAPI-CDH
QE_UNTAR_NAME="aurora-qe-test"
PYTHON_CODE_PATH="${WORKSPACE}/src/testcode"
CONSTANTSFILE="$PYTHON_CODE_PATH/common/Constants.py"

#Get serengeti server ip and vc username/password from aurora-bdc-connection.json
cd ${WORKSPACE}/${QE_UNTAR_NAME}

SERENGETI_SERVER_IP=`cat aurora-bdc-connection.json |grep systemUrl |cut -d '"' -f4 |cut -d ':' -f1`
cd $PYTHON_CODE_PATH/common/
sed -i "s/SERENGETI_SERVER_IP=.*/SERENGETI_SERVER_IP='${SERENGETI_SERVER_IP}'/g" $CONSTANTSFILE
#change all distro in clusterCreate json files.
if [ "$1" != "Mapr" ];
then
   for file in ${WORKSPACE}/src/jsonFile/clusterJsonFile/*;
     do
       sed -i "s/\"distro\":.*/\"distro\":\"$1\"/g" $file
     done
else
   echo 'Need add jsonfiles for mapr creation'
fi

#VC_USERNAME should be base64 encoded.
#VC_USERNAME =
#VC_PASSWORD =

#Execute rest api test cases
cd $PYTHON_CODE_PATH
#Set python path
export PYTHONPATH="${WORKSPACE}/"
#Run smoketest or whole test suite
if [ "$2" = "SmokeTest" ];
then
   echo 'Execute smoke test!'
   python smoketest.py
else
   echo 'Execute whole test suite!'
   python AutoTest.py
fi
