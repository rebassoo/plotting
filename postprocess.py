#!/usr/bin/env python                                                                                   
#Finn Rebassoo, LLNL 11-11-2019 
import os
import subprocess
import sys
import json
import glob
#Finn Rebassoo
#python postprocess.py 2019-11-08-Electron-MultiRP electron
#To do in this file
#First check that all data and Wjets files present before doing combine
#Add together data files
#Add together Wjets samples
#Add together samples.json file, to do this see https://stackoverflow.com/questions/23520542/issue-with-merging-multiple-json-files-in-python
#possibly remove individaul data file and json files after combine
#Clean things up, putting all log files and run files in a directory called run
#Add a json file which has the extra tracks reweighting factor


#directory="./histos_muon_withSimPUDataMixing"
#directory="./histos_muon_withDataProtonMixedIn_bugFix2"
#directory="2019-10-30-MultiPixel"
#directory="2019-10-31-MultiPixel-Correct"
#directory="2019-10-31-MultiRP"
#directory="2019-10-31-Pixel-Pixel"
directory=sys.argv[1]
channel=sys.argv[2]
#directory="2019-11-08-Electron-MultiRP"
#directory="./histos_muon2"

os.chdir(directory)
print os.system("pwd")

i=0
for f in glob.glob("*.json"):
    i=i+1
print "Number of json files is: ",i
ii=0
mc_it=0
for f in glob.glob("*.root"):
    ii=ii+1
    if "Single" not in f:
        mc_it=mc_it+1
print "Number of total root files is: ",ii
print "Number of mc root files is: ",mc_it
print "Number of data root files is: ",(ii-mc_it)
#sys.exit(1)

#Combine data files
if channel=="muon":
    subprocess.call("hadd SingleMuonTotal.root SingleMuon_*root",shell=True)
if channel=="electron":
    #subprocess.call("hadd SingleElectronTotal.root SingleElectron_*root",shell=True)
    subprocess.call("hadd SingleElectronTotal.root EGamma_*root",shell=True)


#
for f in glob.glob("W1Jets*_ext1.root"):
    subprocess.call("mv {0}.root {1}-original.root".format(f[:-10],f[:-10]),shell=True)
    #subprocess.call("mv {0}.root tmp.root".format(f[:-10]),shell=True)
    #subprocess.call("ls {0}.root".format(f[:-10]),shell=True)
    subprocess.call("hadd {0}.root {1}-original.root {2}".format(f[:-10],f[:-10],f),shell=True)
    print f
for f in glob.glob("W2Jets*_ext1.root"):
    subprocess.call("mv {0}.root {1}-original.root".format(f[:-10],f[:-10]),shell=True)
    subprocess.call("hadd {0}.root {1}-original.root {2}".format(f[:-10],f[:-10],f),shell=True)


#sys.exit(1)

#Here want to add number of events from ext1 Wjets files to events from nominal files
#Below to get sample name have to remove samples_info_, this is the 13, and .json is the 5
print "Add number of events from Wjets pt binned ext to nominal Wjets pt binned"
for f in glob.glob("*_ext1.json"):
    num_events_ext1=0
    #if "ext1" in f:
    subprocess.call("cp {0}.json {1}-original.json".format(f[:-10],f[:-10]),shell=True)
    with open(f, "r") as infile:
        data_ext=json.load(infile)
        num_events_ext1=data_ext[f[13:-5]][0]
        #result.append(json.load(infile))
    with open(f[:-10]+".json","r") as infile:
        data=json.load(infile)
        num_events=data[f[13:-10]][0]
    total_events=num_events_ext1+num_events
    data[f[13:-10]][0]=total_events
    with open(f[:-10]+".json","w") as jsonFile:
        json.dump(data,jsonFile)

os.mkdir("run")
subprocess.call("mv *-original.json ./run/",shell=True)

#Now combine all the individual json files into a master json file
print "Combine all individual json files into master json file"
result = {}
for f in glob.glob("*.json"):
    if "Run" in f: continue
    if "ext1" in f: continue
    if "samples_info.json" in f: continue
    with open(f, "r") as infile:
        result.update(json.load(infile))
with open("merged_file.json", "w") as outfile:
    json.dump(result, outfile)

#Now do some cleanup
print "Perform Cleanup"

#subprocess.call("mv sample_info.json samples_info_forSubmit.json",shell=True)
subprocess.call("mv samples_info_*json run/",shell=True)
subprocess.call("mv test* run/",shell=True)
subprocess.call("mv log run/",shell=True)
subprocess.call("mv makeBashScript.sh run/",shell=True)
if channel=="muon":
    subprocess.call("mv produceHistosSingleMu.txt run/",shell=True)
if channel=="electron":
    subprocess.call("mv produceHistosSingleE.txt run/",shell=True)
subprocess.call("mv base.jdl run/",shell=True)
subprocess.call("mv merged_file.json samples_info.json",shell=True)

