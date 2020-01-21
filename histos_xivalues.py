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
fout = TFile('{0}.root'.format(output_name),'recreate')
fout.cd()


#Chain Together List Of Files
chain = TChain('demo/SlimmedNtuple')
num_events=AddFilesToChain(chain,ListOfFiles,DATA)
if not DATA and (sample_name != "ExclusiveWW"):
    modifyJson(sample_name,num_events,batch)

fout.cd()

print("--- %s seconds ---" % (time.time() - start_time))

h_xi_23=TH1F("h_xi_23",";Xi;",128,0,0.32)
h_xi_23_2nd=TH1F("h_xi_23_2nd",";Xi;",128,0,0.32)
h_xi_123=TH1F("h_xi_123",";Xi;",128,0,0.32)
h_xi_123_2nd=TH1F("h_xi_123_2nd",";Xi;",128,0,0.32)
h_xangle=TH1F("h_xangle","",100,99.5,199.5)

h_xi_23_noMultiRP=TH1F("h_xi_23_noMultiRP",";Xi;",128,0,0.32)
h_xi_23_noMultiRP_2nd=TH1F("h_xi_23_noMultiRP_2nd",";Xi;",128,0,0.32)
h_xi_123_noMultiRP=TH1F("h_xi_123_noMultiRP",";Xi;",128,0,0.32)
h_xi_123_noMultiRP_2nd=TH1F("h_xi_123_noMultiRP_2nd",";Xi;",128,0,0.32)

h_xi_23_noMultiRP_doubletag=TH1F("h_xi_23_noMultiRP_doubletag",";Xi;",128,0,0.32)
h_xi_23_noMultiRP_2nd_doubletag=TH1F("h_xi_23_noMultiRP_2nd_doubletag",";Xi;",128,0,0.32)
h_xi_123_noMultiRP_doubletag=TH1F("h_xi_123_noMultiRP_doubletag",";Xi;",128,0,0.32)
h_xi_123_noMultiRP_2nd_doubletag=TH1F("h_xi_123_noMultiRP_2nd_doubletag",";Xi;",128,0,0.32)

h_xi_23_noMultiRP_doubletag_2pxl=TH1F("h_xi_23_noMultiRP_doubletag_2pxl",";Xi;",128,0,0.32)
h_xi_123_noMultiRP_doubletag_2pxl=TH1F("h_xi_123_noMultiRP_doubletag_2pxl",";Xi;",128,0,0.32)
h_xi_23_noMultiRP_2nd_doubletag_2pxl=TH1F("h_xi_23_noMultiRP_2nd_doubletag_2pxl",";Xi;",128,0,0.32)
h_xi_123_noMultiRP_2nd_doubletag_2pxl=TH1F("h_xi_123_noMultiRP_2nd_doubletag_2pxl",";Xi;",128,0,0.32)

h_nvertices_all=TH1F("h_nvertices_all","Num Vertices",100,-0.5,99.5)
h_nvertices_45_0=TH1F("h_nvertices_45_0","Num Vertices",100,-0.5,99.5)
h_nvertices_45_1=TH1F("h_nvertices_45_1","Num Vertices",100,-0.5,99.5)
h_nvertices_45_2up=TH1F("h_nvertices_45_2up","Num Vertices",100,-0.5,99.5)
h_nvertices_45_1_xi0p07=TH1F("h_nvertices_45_1_xi0p07","Num Vertices",100,-0.5,99.5)

h_nvertices_56_0=TH1F("h_nvertices_56_0","Num Vertices",100,-0.5,99.5)
h_nvertices_56_1=TH1F("h_nvertices_56_1","Num Vertices",100,-0.5,99.5)
h_nvertices_56_2up=TH1F("h_nvertices_56_2up","Num Vertices",100,-0.5,99.5)
h_nvertices_56_1_xi0p07=TH1F("h_nvertices_56_1_xi0p07","Num Vertices",100,-0.5,99.5)

h_nvertices_45_0_56_0=TH1F("h_nvertices_45_0_56_0","Num Vertices",100,-0.5,99.5)
h_nvertices_45_1_56_0=TH1F("h_nvertices_45_1_56_0","Num Vertices",100,-0.5,99.5)
h_nvertices_45_0_56_1=TH1F("h_nvertices_45_0_56_1","Num Vertices",100,-0.5,99.5)

h_nvertices_45_0_strips=TH1F("h_nvertices_45_0_strips","Num Vertices",100,-0.5,99.5)
h_nvertices_45_1_strips=TH1F("h_nvertices_45_1_strips","Num Vertices",100,-0.5,99.5)

h_nvertices_56_0_strips=TH1F("h_nvertices_56_0_strips","Num Vertices",100,-0.5,99.5)
h_nvertices_56_1_strips=TH1F("h_nvertices_56_1_strips","Num Vertices",100,-0.5,99.5)

h_nvertices_45_0_56_0_strips=TH1F("h_nvertices_45_0_56_0_strips","Num Vertices",100,-0.5,99.5)
h_nvertices_45_1_56_0_strips=TH1F("h_nvertices_45_1_56_0_strips","Num Vertices",100,-0.5,99.5)
h_nvertices_45_0_56_1_strips=TH1F("h_nvertices_45_0_56_1_strips","Num Vertices",100,-0.5,99.5)


h_xi_23_multi=TH1F("h_xi_23_multi",";Xi;",128,0,0.32)
h_xi_23_multi_2nd=TH1F("h_xi_23_multi_2nd",";Xi;",128,0,0.32)
h_xi_123_multi=TH1F("h_xi_123_multi",";Xi;",128,0,0.32)
h_xi_123_multi_2nd=TH1F("h_xi_123_2nd_multi",";Xi;",128,0,0.32)
h_xi_23_multi_doubletag=TH1F("h_xi_23_multi_doubletag",";Xi;",128,0,0.32)
h_xi_123_multi_doubletag=TH1F("h_xi_123_multi_doubletag",";Xi;",128,0,0.32)

h_nvertices_multi_all=TH1F("h_nvertices_multi_all","Num Vertices",100,-0.5,99.5)
h_nvertices_multi_45_0=TH1F("h_nvertices_multi_45_0","Num Vertices",100,-0.5,99.5)
h_nvertices_multi_45_1=TH1F("h_nvertices_multi_45_1","Num Vertices",100,-0.5,99.5)
h_nvertices_multi_45_2up_pixels=TH1F("h_nvertices_multi_45_2up_pixels","Num Vertices",100,-0.5,99.5)
h_nvertices_multi_45_2up=TH1F("h_nvertices_multi_45_2up","Num Vertices",100,-0.5,99.5)

h_nvertices_multi_56_0=TH1F("h_nvertices_multi_56_0","Num Vertices",100,-0.5,99.5)
h_nvertices_multi_56_1=TH1F("h_nvertices_multi_56_1","Num Vertices",100,-0.5,99.5)
h_nvertices_multi_56_2up=TH1F("h_nvertices_multi_56_2up","Num Vertices",100,-0.5,99.5)

h_nvertices_multi_45_0_56_0=TH1F("h_nvertices_multi_45_0_56_0","Num Vertices",100,-0.5,99.5)
h_nvertices_multi_45_1_56_0=TH1F("h_nvertices_multi_45_1_56_0","Num Vertices",100,-0.5,99.5)
h_nvertices_multi_45_0_56_1=TH1F("h_nvertices_multi_45_0_56_1","Num Vertices",100,-0.5,99.5)

h_nvertices_45_1pixel_1strip=TH1F("h_nvertices_45_1pixel_1strip","Num Vertices",100,-0.5,99.5)
h_nvertices_45_2pixel_1strip=TH1F("h_nvertices_45_2pixel_1strip","Num Vertices",100,-0.5,99.5)
h_nvertices_56_1pixel_1strip=TH1F("h_nvertices_56_1pixel_1strip","Num Vertices",100,-0.5,99.5)
h_nvertices_56_2pixel_1strip=TH1F("h_nvertices_56_2pixel_1strip","Num Vertices",100,-0.5,99.5)

h_nvertices_45_1pixel_1strip_xi0p07=TH1F("h_nvertices_45_1pixel_1strip_xi0p07","Num Vertices",100,-0.5,99.5)
h_nvertices_56_1pixel_1strip_xi0p07=TH1F("h_nvertices_56_1pixel_1strip_xi0p07","Num Vertices",100,-0.5,99.5)

h_pixel_vs_multi_45=TH2F("h_pixel_vs_multi_45",";Xi;",128,0,0.32,128,0,0.32)

Run=0.
event=0.
num_events=chain.GetEntries()
print num_events

#SetBranchAddress(chain)

it=0
for e in chain:
    it=it+1
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

        xi_trigger = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[]}
        xi_trigger_multi = {"23":[],"123":[]}
        xi_trigger_strip = {"3":[],"103":[]}
        h_xangle.Fill(e.crossingAngle)
        passPPS=passPPSMulti(e,xi_trigger_multi)
        passPPSstrip=passPPSNewStrip(e,xi_trigger_strip)
        passPPSpixel=passPPSNewPixel(e,xi_trigger)
        h_nvertices_multi_all.Fill(e.nVertices)
        if len(xi_trigger_multi["23"]) == 0 and len(xi_trigger_strip["3"])==0:
            h_nvertices_multi_45_0.Fill(e.nVertices)
        if len(xi_trigger_multi["23"]) == 1 and len(xi_trigger_multi["123"]):
            h_xi_23_multi_doubletag.Fill(xi_trigger_multi["23"][0])
            h_xi_123_multi_doubletag.Fill(xi_trigger_multi["123"][0])
        if len(xi_trigger_multi["23"]) == 1:
            h_xi_23_multi.Fill(xi_trigger_multi["23"][0])
            h_nvertices_multi_45_1.Fill(e.nVertices)
            if len(xi_trigger["23"])==1:
                h_pixel_vs_multi_45.Fill(xi_trigger_multi["23"][0],xi_trigger["23"][0])
            if len(xi_trigger["23"])>1:
                h_nvertices_multi_45_2up_pixels.Fill(e.nVertices)
        if len(xi_trigger_multi["23"]) == 2:
            h_xi_23_2nd_multi.Fill(xi_trigger_multi["23"][1])
        if len(xi_trigger_multi["23"]) > 1:
            h_nvertices_multi_45_2up.Fill(e.nVertices)
        if len(xi_trigger_multi["123"]) == 0 and len(xi_trigger_strip["103"]):
            h_nvertices_multi_56_0.Fill(e.nVertices)
        if len(xi_trigger_multi["123"]) == 1:
            h_xi_123_multi.Fill(xi_trigger_multi["123"][0])
            h_nvertices_multi_56_1.Fill(e.nVertices)
        if len(xi_trigger_multi["123"]) == 2:
            h_xi_123_2nd_multi.Fill(xi_trigger_multi["123"][1])
        if len(xi_trigger_multi["123"]) > 1:
            h_nvertices_multi_45_2up.Fill(e.nVertices)
        if len(xi_trigger_multi["23"]) == 0 and len(xi_trigger_multi["123"]) == 0 and len(xi_trigger_strip["3"])==0 and len(xi_trigger_strip["103"]) ==0:
            h_nvertices_multi_45_0_56_0.Fill(e.nVertices)
        if len(xi_trigger_multi["23"]) == 0 and len(xi_trigger_multi["123"]) == 1 and len(xi_trigger_strip["3"])==0:
            h_nvertices_multi_45_0_56_1.Fill(e.nVertices)                
        if len(xi_trigger_multi["23"]) == 1 and len(xi_trigger_multi["123"]) == 0 and len(xi_trigger_strip["103"])==0:
            h_nvertices_multi_45_1_56_0.Fill(e.nVertices)                

        if passPPSpixel:
            if len(xi_trigger["23"]) == 1 and len(xi_trigger_multi["23"])==0:
                h_xi_23_noMultiRP.Fill(xi_trigger["23"][0])
            if len(xi_trigger["123"]) == 1 and len(xi_trigger_multi["123"])==0:
                h_xi_123_noMultiRP.Fill(xi_trigger["123"][0])
            if len(xi_trigger["23"]) == 2 and len(xi_trigger_multi["23"])==0:
                h_xi_23_noMultiRP_2nd.Fill(xi_trigger["23"][1])
            if len(xi_trigger["123"]) == 2 and len(xi_trigger_multi["123"])==0:
                h_xi_123_noMultiRP_2nd.Fill(xi_trigger["123"][1])

            if not passPPS:
                if len(xi_trigger["23"]) == 1:
                    h_xi_23_noMultiRP_doubletag.Fill(xi_trigger["23"][0])
                if len(xi_trigger["123"]) == 1:
                    h_xi_123_noMultiRP_doubletag.Fill(xi_trigger["123"][0])
                if len(xi_trigger["23"]) == 2:
                    h_xi_23_noMultiRP_2nd_doubletag.Fill(xi_trigger["23"][1])
                if len(xi_trigger["123"]) == 2:
                    h_xi_123_noMultiRP_2nd_doubletag.Fill(xi_trigger["123"][1])

                if len(xi_trigger["23"]) == 1 and len(xi_trigger["123"]) == 1:
                    h_xi_23_noMultiRP_doubletag_2pxl.Fill(xi_trigger["23"][0])
                    h_xi_123_noMultiRP_doubletag_2pxl.Fill(xi_trigger["123"][0])
                if len(xi_trigger["23"]) == 2 and len(xi_trigger["123"]) == 1:
                    h_xi_23_noMultiRP_2nd_doubletag_2pxl.Fill(xi_trigger["23"][1])
                if len(xi_trigger["123"]) == 2 and len(xi_trigger["23"]) == 1:
                    h_xi_123_noMultiRP_2nd_doubletag_2pxl.Fill(xi_trigger["123"][1])
                
            h_nvertices_all.Fill(e.nVertices)
            if len(xi_trigger["23"]) == 0:
                h_nvertices_45_0.Fill(e.nVertices)
            if len(xi_trigger["23"]) == 1:
                h_xi_23.Fill(xi_trigger["23"][0])
                h_nvertices_45_1.Fill(e.nVertices)
                if xi_trigger["23"][0]>0.07: h_nvertices_45_1_xi0p07.Fill(e.nVertices)
                if len(xi_trigger_strip["3"]) == 1:
                    h_nvertices_45_1pixel_1strip.Fill(e.nVertices)
                    if xi_trigger["23"][0]>0.07:
                        h_nvertices_45_1pixel_1strip_xi0p07.Fill(e.nVertices)
            if len(xi_trigger["23"]) == 2:
                h_xi_23_2nd.Fill(xi_trigger["23"][1])
                if len(xi_trigger_strip["3"]) == 1:
                    h_nvertices_45_2pixel_1strip.Fill(e.nVertices)
            if len(xi_trigger["23"]) > 1:
                h_nvertices_45_2up.Fill(e.nVertices)
            if len(xi_trigger["123"]) == 0:
                h_nvertices_56_0.Fill(e.nVertices)
            if len(xi_trigger["123"]) == 1:
                h_xi_123.Fill(xi_trigger["123"][0])
                h_nvertices_56_1.Fill(e.nVertices)
                if xi_trigger["123"][0]>0.07: h_nvertices_56_1_xi0p07.Fill(e.nVertices)
                if len(xi_trigger_strip["103"]) == 1:
                    h_nvertices_56_1pixel_1strip.Fill(e.nVertices)
                    if xi_trigger["123"][0]>0.07:
                        h_nvertices_56_1pixel_1strip_xi0p07.Fill(e.nVertices)
            if len(xi_trigger["123"]) == 2:
                h_xi_123_2nd.Fill(xi_trigger["123"][1])
                if len(xi_trigger_strip["103"]) == 1:
                    h_nvertices_56_2pixel_1strip.Fill(e.nVertices)
            if len(xi_trigger["123"]) > 1:
                h_nvertices_56_2up.Fill(e.nVertices)
            if len(xi_trigger["23"]) == 0 and len(xi_trigger["123"]) == 0:
                h_nvertices_45_0_56_0.Fill(e.nVertices)
            if len(xi_trigger["23"]) == 0 and len(xi_trigger["123"]) == 1:
                h_nvertices_45_0_56_1.Fill(e.nVertices)                
            if len(xi_trigger["23"]) == 1 and len(xi_trigger["123"]) == 0:
                h_nvertices_45_1_56_0.Fill(e.nVertices)                

        if len(xi_trigger_strip["3"]) == 0:
            h_nvertices_45_0_strips.Fill(e.nVertices)
        if len(xi_trigger_strip["3"]) == 1:
            h_nvertices_45_1_strips.Fill(e.nVertices)
        if len(xi_trigger_strip["103"]) == 0:
            h_nvertices_56_0_strips.Fill(e.nVertices)
        if len(xi_trigger_strip["103"]) == 1:
            h_nvertices_56_1_strips.Fill(e.nVertices)
        if len(xi_trigger_strip["3"]) == 0 and len(xi_trigger_strip["103"]) == 0:
            h_nvertices_45_0_56_0_strips.Fill(e.nVertices)
        if len(xi_trigger_strip["3"]) == 0 and len(xi_trigger_strip["103"]) == 1:
            h_nvertices_45_0_56_1_strips.Fill(e.nVertices)                
        if len(xi_trigger_strip["3"]) == 1 and len(xi_trigger_strip["103"]) == 0:
            h_nvertices_45_1_56_0_strips.Fill(e.nVertices)                




fout.Write()
fout.Close()
print fout
print("--- %s seconds ---" % (time.time() - start_time))
#if batch:
#    os.listdir(".")
