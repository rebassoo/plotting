#!/bin/bash                                                      

echo "ls ---"
ls

export SCRAM_ARCH=slc6_amd64_gcc630
#export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh CMSSW_9_4_11
#source /cvmfs/cms.cern.ch/cmsset_default.sh CMSSW_10_6_0
#export SCRAM_ARCH=slc6_amd64_gcc530

scramv1 p -n globe9411 CMSSW CMSSW_9_4_11
#scramv1 p -n globe1060 CMSSW CMSSW_10_6_0

cd globe9411/src/
#cd globe1060/src/

eval `scramv1 ru -sh`

cd -

if [ $# != 3 ]; then
   echo usage: runningOverNtupleDCACHE.sh cluster process initial_seed
   exit 1
fi
seed=$(($2+$3))

echo "ls ---"
ls
which python
python -V
