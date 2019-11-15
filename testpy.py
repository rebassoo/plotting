#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-30-2019
import subprocess

mypath_prefix='/hadoop/cms/store/user/rebassoo/'
sample_name="SingleMuon"
file_dir="crab_Run2017B"
print 'ls {0}{1}/{2}'.format(mypath_prefix,sample_name,file_dir)
#list2 = subprocess.check_output(['ls {0}{1}/{2}'.format(mypath_prefix,sample_name,file_dir), '-l']).splitlines()
#list2 = subprocess.check_output(['ls /hadoop/cms/store/user/rebassoo/SingleMuon/crab_Run2017B', '-l']).splitlines()
subprocess.call(['ls /hadoop/cms/store/user/rebassoo/SingleMuon/crab_Run2017B', '-l'])
