#!/usr/bin/env python
#Finn Rebassoo, LLNL 12-2016-01
import os
from ROOT import *
import math as m
from htools import *
import sys
import time

if len(sys.argv) < 5:
    print "Need to specify 5 inputs parameters, i.e.:"
    print "  python histos_mue.py muon latest MuonEG crab_runBv3"
    print "  or"
    print "  python histos_mue.py muon specific MuonEG crab_runBv3/171116_215828/0001"
    sys.exit()

start_time = time.time()
directory_type=sys.argv[1]
channel=sys.argv[2]
sample_name=sys.argv[3]
print sample_name
file_dir=sys.argv[4]
print file_dir
batch=False
if len(sys.argv) > 4:
    if sys.argv[5] == "-b":
        batch=True
#channel="electron"

METCUT=0
pname="l"
if channel=="electron": 
    METCUT=100
    pname="e"
if channel=="muon": 
    METCUT=40
    pname="#mu"

DATA=False
ExclusiveMC=False
if sample_name == "SingleElectron" or sample_name == "SingleMuon":    DATA=True
if sample_name == "ExclusiveWW" or ("GGToWW" in sample_name):   ExclusiveMC=True
print "ExclusiveMC", ExclusiveMC

#Get List Of Files
ListOfFiles=[]
returnedFiles=GetListOfFiles(sample_name,file_dir,DATA,directory_type)
ListOfFiles=returnedFiles[0]
output_name=returnedFiles[1]
if "LHEWpT" in output_name:
    if "ext1" in file_dir:  
        output_name=output_name+"_ext1"
        sample_name=sample_name+"_ext1"
#fout = TFile('histos_{0}/{1}.root'.format(channel,output_name),'recreate')


#Chain Together List Of Files
chain = TChain('demo/SlimmedNtuple')
num_events=AddFilesToChain(chain,ListOfFiles,DATA)
if not DATA and (sample_name != "ExclusiveWW"):
    modifyJson(sample_name,num_events,batch)

print("--- %s seconds ---" % (time.time() - start_time))


Run=0.
event=0.
num_events=chain.GetEntries()
print num_events


it=0

#chain.SetBranchStatus("*",0)
#chain.SetBranchStatus("crossingAngle",1)
#chain.SetBranchStatus("run",1)
#chain.SetBranchStatus("event",1)
#chain.SetBranchStatus("proton_xi",1)
#chain.SetBranchStatus("proton_ismultirp_",1)
#chain.SetBranchStatus("proton_rpid",1)
#chain.SetBranchStatus("proton_arm",1)
#chain.SetBranchStatus("nVertices",1)
#chain.SetBranchStatus("electron_pt",1)
#chain.SetBranchStatus("muon_pt",1)
#fout = TFile('{0}.root'.format(output_name),'recreate')
#fout.cd()
outTree = chain.CloneTree(0)

nEntries = chain.GetEntries()
for e in chain:
#for it in range(nEntries):
    it=it+1
    chain.GetEntry(it+1)
    #continue
    if DATA:
        if channel=="electron" and e.electron_pt.size() == 0:
            continue
        if channel=="muon" and e.muon_pt.size() == 0:
                continue
        if channel=="dimuon" and e.muon_pt.size() < 2:
            continue
        if channel=="dielectron" and e.electron_pt.size() < 2:
            continue
        if channel=="electron":
            l_pt=e.electron_pt[0]
            l_eta=e.electron_eta[0]
            l_phi=e.electron_phi[0]
            if not DATA:
                pileupw=pileupw*electronScaleFactor(l_pt,l_eta)
        if channel=="muon":
            l_pt=e.muon_pt[0]
            l_eta=e.muon_eta[0]
            l_phi=e.muon_phi[0]
            if not DATA:
                pileupw=pileupw*muonScaleFactor(l_pt,l_eta)

        #print "muon_pt 1st method:",muon_pt[0]
        #print "muon_pt 2nd method:",e.muon_pt[0]
         
        dphi_lepton_jet=GetDphi(l_phi,e.jet_phi[0])
        deta_lepton_jet=l_eta-e.jet_eta[0]
        deltaR=m.sqrt(dphi_lepton_jet*dphi_lepton_jet+deta_lepton_jet*deta_lepton_jet   )
        dphi_jet_met=abs(GetDphi(e.jet_phi[0],e.met_phi))
        dphi_jet_Wl=abs(GetDphi(e.jet_phi[0],e.WLeptonicPhi))

        recoMWhad=e.recoMWhad
        recoMWlep=e.recoMWlep
        dphiWW=abs(e.dphiWW)
        recoMWW=e.recoMWW
        MET=e.met
        WLeptonicPt=e.WLeptonicPt
        tau21=e.jet_tau2[0]/e.jet_tau1[0]
        prunedMass=e.jet_corrmass[0]
        passesBoosted=False
        jetPruning=True
        mjet_veto=True
        if dphiWW>2.5 and recoMWW>500 and MET>METCUT and WLeptonicPt>200:
            passesBoosted=False
        if prunedMass>50 and prunedMass<110 and tau21<0.6:
            jetPruning=True
        if e.num_bjets_ak4<1:
            mjet_veto=True
        if mjet_veto and passesBoosted and jetPruning and deltaR>(m.pi/2) and dphi_jet_met>2 and dphi_jet_Wl>2:
            continue

        outTree.Fill()
        

outTree.SetBranchStatus("*",0)
outTree.SetBranchStatus("crossingAngle",1)
outTree.SetBranchStatus("run",1)
outTree.SetBranchStatus("event",1)
outTree.SetBranchStatus("proton_xi",1)
outTree.SetBranchStatus("proton_ismultirp_",1)
outTree.SetBranchStatus("proton_rpid",1)
outTree.SetBranchStatus("proton_arm",1)
outTree.SetBranchStatus("proton_trackpixshift1",1)
outTree.SetBranchStatus("proton_trackpixshift2",1)
outTree.SetBranchStatus("nVertices",1)
outTree.SetBranchStatus("electron_pt",1)
outTree.SetBranchStatus("muon_pt",1)
fout = TFile('{0}.root'.format(output_name),'recreate')
fout.cd()
outTree2 = outTree.CloneTree(0)


nEntries = outTree.GetEntries()
#for e in chain:
for ita in range(nEntries):
    #it=it+1
    outTree.GetEntry(ita+1)
    outTree2.Fill()


#outTree.GetCurrentFile().Write()
#outTree.GetCurrentFile().Close()
fout.Write()
fout.Close()
print fout
print("--- %s seconds ---" % (time.time() - start_time))
#if batch:
#    os.listdir(".")
