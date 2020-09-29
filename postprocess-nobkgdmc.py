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
    #subprocess.call("hadd SingleElectronTotal.root EGamma_*root",shell=True)


os.mkdir("run")
subprocess.call("mv *-original.json ./run/",shell=True)

#Now combine all the individual json files into a master json file
print "Combine all individual json files into master json file"
result = {}
for f in glob.glob("samples*GG*.json"):
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

