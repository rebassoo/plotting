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
    subprocess.call("hadd SingleElectronTotal.root SingleElectron_*root",shell=True)


#
for f in glob.glob("W1Jets*_ext1.root"):
    subprocess.call("mv {0}.root {1}-original.root".format(f[:-10],f[:-10]),shell=True)
    #subprocess.call("mv {0}.root tmp.root".format(f[:-10]),shell=True)
    #subprocess.call("ls {0}.root".format(f[:-10]),shell=True)
    subprocess.call("hadd {0}.root {1}-original.root {2}".format(f[:-10],f[:-10],f),shell=True)
    print f
#Need to add up all non-ext files as well.
for f in glob.glob("W2Jets*pythia8_1.root"):
    subprocess.call("hadd {0}.root {1}_1.root {1}_2.root {1}_3.root {1}_4.root {1}_5.root {1}_6.root {1}_7.root".format(f[:-7],f[:-7]),shell=True)
for f in glob.glob("W2Jets*_ext1_1.root"):
    #subprocess.call("mv {0}.root {1}-original.root".format(f[:-10],f[:-10]),shell=True)
    subprocess.call("mv {0}.root {1}-original.root".format(f[:-12],f[:-12]),shell=True)
    #subprocess.call("hadd {0}.root {1}-original.root {2}".format(f[:-10],f[:-10],f),shell=True)
    subprocess.call("hadd {0}.root {1}-original.root {2}*root".format(f[:-12],f[:-12],f[:-7]),shell=True)


#sys.exit(1)

#Here want to add number of events from ext1 Wjets files to events from nominal files
#Below to get sample name have to remove samples_info_, this is the 13, and .json is the 5
print "Add number of events from Wjets pt binned ext to nominal Wjets pt binned"
#Need to add these for non-ext files as well.

#for f in glob.glob("*pythia8_1.json"):
#    num_events_ext1=0
    #subprocess.call("cp {0}.json {1}-original.json".format(f[:-7],f[:-7]),shell=True)

#Should check that get same entries all 7 jobs

#This is for W1Jets
for f in glob.glob("W1Jets*_ext1.json"):
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


#This is for W2Jets
for f in glob.glob("W2Jets*_ext1_1.json"):
    num_events_ext1=0
    #if "ext1" in f:
    #subprocess.call("cp {0}.json {1}-original.json".format(f[:-10],f[:-10]),shell=True)
    subprocess.call("cp {0}_1.json {1}-original.json".format(f[:-12],f[:-12]),shell=True)
    total_events=0
    cross_section=0
    color=0
    for i in range(1,2,1):
        filename_ext=f[:-7]+"_{0}.json".format(i)
        num_events_ext1=0
        num_events=0
        with open(filename_ext, "r") as infile_ext:
            data_ext=json.load(infile_ext)
            num_events_ext1=data_ext[f[13:-7]+"_{0}".format(i)][0]
            if i==1:
                cross_section=data_ext[f[13:-7]+"_{0}".format(i)][1]
                color=data_ext[f[13:-7]+"_{0}".format(i)][2]
        #result.append(json.load(infile))
        filename=f[:-12]+"_{0}.json".format(i)
        with open(filename,"r") as infile:
            data=json.load(infile)
            num_events=data[f[13:-12]+"_{0}".format(i)][0]
        total_events=num_events_ext1+num_events+total_events
    #data[f[13:-12]][0]=total_events
    #data[f[13:-12]][0]=total_events
    dict1={f[13:-12]:[total_events,cross_section,color]}
    with open(f[:-12]+".json","w") as jsonFile:
        #json.dump(data,jsonFile)
        json.dump(dict1,jsonFile)

os.mkdir("run")
subprocess.call("mv *-original.json ./run/",shell=True)

#Now combine all the individual json files into a master json file
print "Combine all individual json files into master json file"
result = {}
for f in glob.glob("*.json"):
    if "Run" in f: continue
    if "ext1" in f: continue
    if "pythia8_" in f: continue
    if "samples_info.json" in f: continue
    with open(f, "r") as infile:
        result.update(json.load(infile))
with open("merged_file.json", "w") as outfile:
    json.dump(result, outfile)

#Now do some cleanup
print "Perform Cleanup"

#subprocess.call("mv sample_info.json samples_info_forSubmit.json",shell=True)
subprocess.call("mv *pythia8_*root run/",shell=True)
#subprocess.call("mv *pythia8_ext1_*root run/",shell=True)
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

