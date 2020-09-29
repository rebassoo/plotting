#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-30-2019
import subprocess
import sys
from htools import *
from ROOT import *
from ptools import *

h=TH1F("h","",10,0,10)
ModifyHisto(h,"GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6-2018","/home/users/rebassoo/work/2020_07_10_2018-PlottingAll")
sys.exit()

era="B"
#fp=open('2020-07-17-RunsABCD-SkimmedProtons-OutputEntriesFixed/log/passingRun{0}.txt'.format(era),'r')
fp=open('inputfiles/passingEventsMuonRunA-WithIndex.txt','r')
long_string=fp.read()
#print long_string.find("319579:2361:3692446389")
#e=long_string.find("320065:359:578431347")
#e=long_string.find("320065:359:578\n")
#e=long_string.find("319579:2361:3692468869\n")
#print "317696:55:45993629"
#print "317696:240:314360781"
#e=long_string.find("317696:55:45993629\n")
#e=long_string.find("315259:109:71741055\n")
e=long_string.find("316114:337:354234678\n")
#e=long_string.find("317641:365:537637407\n")
print e
if e < 10:
    print long_string[:e-1]
sys.exit()
if e > 0:
    print long_string[e-8:e-1]
    if "\n" in long_string[e-8:e-1]:
        print long_string[e-8:e-1].split("\n")[1]
        entry=long_string[e-8:e-1].split("\n")[1]
    else:
        print long_string[e-8:e-1]

print entry
#f2=TFile("xiEventsRun{0}-2018.root".format(era))
f2=TFile("2020-07-17-RunsABCD-AllProtons/SingleMuon_Run2018A-justProtons.root")
tree2=f2.Get("SlimmedNtuple")
tree2.GetEntry(int(entry))
print "Run, etc. :{0}:{1}:{2}".format(tree2.run,tree2.lumiblock,tree2.event)

tree2.GetEntry(int(entry)-1)
print "It -1 Run, etc. :{0}:{1}:{2}".format(tree2.run,tree2.lumiblock,tree2.event)

tree2.GetEntry(int(entry)-2)
print "It -2 Run, etc. :{0}:{1}:{2}".format(tree2.run,tree2.lumiblock,tree2.event)


tree2.GetEntry(int(entry)+1)
print "It +1 Run, etc. :{0}:{1}:{2}".format(tree2.run,tree2.lumiblock,tree2.event)


#if "319579:2361:3692446389" in long_string:
#    
#    print "Yes"

sys.exit()

for i in range(100):
    era="A"
    f2=TFile("SingleMuon_Run2018{0}-justProtons.root".format(era))
    tree2=f2.Get("SlimmedNtuple")
    tree2.GetEntry(i+1000)
    xi = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[],"weight":[],"multi_arm0":[],"multi_arm1":[]}
    passMultiRP=passPPSMulti(tree2,xi)
    print passMultiRP
sys.exit()

mypath_prefix='/hadoop/cms/store/user/rebassoo/'
sample_name="SingleMuon"
file_dir="crab_Run2017B"
print 'ls {0}{1}/{2}'.format(mypath_prefix,sample_name,file_dir)
#list2 = subprocess.check_output(['ls {0}{1}/{2}'.format(mypath_prefix,sample_name,file_dir), '-l']).splitlines()
#list2 = subprocess.check_output(['ls /hadoop/cms/store/user/rebassoo/SingleMuon/crab_Run2017B', '-l']).splitlines()
subprocess.call(['ls /hadoop/cms/store/user/rebassoo/SingleMuon/crab_Run2017B', '-l'])
