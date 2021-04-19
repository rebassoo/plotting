#!/usr/bin/env python
#Finn Rebassoo, LLNL 12-2016-01
import os
from ROOT import *
import math as m
from htools import *
import sys
import time

if len(sys.argv) < 6:
    print "Need to specify 6 inputs parameters, i.e.:"
    print "python histos_quick.py latest muon SingleMuon crab_Run2018A-withDilepton -nb"
    print "  or"
    print "python histos_quick.py muon specific SingleMuon crab_Run2018A-withDilepton/200707_182742/0000 -nb"
    print "the input parameter latest looks for most recent ntuple in the directory listed"
    sys.exit()

directory_type=sys.argv[1]
start_time = time.time()
channel=sys.argv[2]
sample_name=sys.argv[3]
print sample_name
file_dir=sys.argv[4]
print file_dir
batch=False
#signal_bin="multiRP"
if len(sys.argv) > 4:
    if sys.argv[5] == "-b":
        batch=True
if len(sys.argv) < 6:
    print "Need to specify if batch submission and if it is multiRP, pixel-pixel, or multiPixel"
#channel="electron"
#if len(sys.argv) > 6:
#    signal_bin=sys.argv[6]
seed_input=0
if len(sys.argv) > 6:
    seed_input=int(sys.argv[6])
job_number=0
if len(sys.argv) > 7:
    job_number=int(sys.argv[7])

METCUT=0
pname="l"
mname=""
if channel=="electron": 
    METCUT=100
    pname="e"
    mname="_e"
if channel=="muon": 
    METCUT=40
    pname="#mu"
year="2017"
if "2018" in file_dir:
    year="2018"

DATA=False
ExclusiveMC=False
sample=""
if sample_name == "SingleElectron" or sample_name == "SingleMuon" or sample_name == "EGamma":    
    DATA=True
    sample="Data"
elif (sample_name == "ExclusiveWW" or ("GGToWW" in sample_name)):   
    ExclusiveMC=True
    sample="ExclusiveMC"
else:
    sample="MC"
print "ExclusiveMC", ExclusiveMC
print "Sample: ",sample

#Get List Of Files
ListOfFiles=[]
returnedFiles=GetListOfFiles(sample_name,file_dir,DATA,directory_type)
ListOfFiles=returnedFiles[0]
output_name=returnedFiles[1]
fout = TFile('{0}.root'.format(output_name),'recreate')
fout.cd()


#Chain Together List Of Files
if DATA:
    chain = TChain('SlimmedNtuple')
else:
    chain = TChain('demo/SlimmedNtuple')

num_events=AddFilesToChain(chain,ListOfFiles,DATA)
if not DATA and (sample_name != "ExclusiveWW"):
    modifyJson(sample_name,num_events,batch)

fout.cd()

print("--- %s seconds ---" % (time.time() - start_time))
#This defines all the histograms
h_deltaR_lepton_jet=TH1F("h_deltaR_lepton_jet",";#deltaR({0},jet);".format(pname),200,0,10)
h_deltaphi_jet_met=TH1F("h_deltaphi_jet_met",";#delta#Phi(MET,jet);",100,0,5)
h_deltaphi_jet_Wleptonic=TH1F("h_deltaphi_jet_Wleptonic",";#delta#Phi(MET,jet);",100,0,5)
h_lepton_pt_MjetVeto_WleptonicCuts=TH1F("h_{0}_pt_MjetVeto_WleptonicCuts".format(channel),";p_{{T}} ({0}) [GeV];".format(pname),100,0,1000)
h_lepton_eta_MjetVeto_WleptonicCuts=TH1F("h_{0}_eta_MjetVeto_WleptonicCuts".format(channel),";#eta_{{0}};".format(pname),60,-3,3)
h_jet_pt_MjetVeto_WleptonicCuts=TH1F("h_jet_pt_MjetVeto_WleptonicCuts",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_eta_MjetVeto_WleptonicCuts=TH1F("h_jet_eta_MjetVeto_WleptonicCuts",";#eta_{jet};",60,-3,3)
h_jet_pt_MjetVeto_WleptonicCuts_Wplus=TH1F("h_jet_pt_MjetVeto_WleptonicCuts_Wplus",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_pt_MjetVeto_WleptonicCuts_Wminus=TH1F("h_jet_pt_MjetVeto_WleptonicCuts_Wminus",";p_{T} (jet) [GeV];",120,0,1200)
h_tau21_MjetVeto_WleptonicCuts=TH1F("h_tau21_MjetVeto_WleptonicCuts",";tau21;",100,0,2)
h_prunedMass_MjetVeto_WleptonicCuts=TH1F("h_prunedMass_MjetVeto_WleptonicCuts",";prunedMass [GeV];",200,0,1000)
h_recoMWlep_MjetVeto_WleptonicCuts=TH1F("h_recoMWlep_MjetVeto_WleptonicCuts",";M_{W_{lep}} [GeV];",100,0,200)
h_recoMWhad_MjetVeto_WleptonicCuts=TH1F("h_recoMWhad_MjetVeto_WleptonicCuts",";M_{W_{had}} [GeV];",100,0,200)
h_dphiWW_MjetVeto_WleptonicCuts=TH1F("h_dphiWW_MjetVeto_WleptonicCuts",";dphiWW;",100,0,5)
h_WLeptonicPt_MjetVeto_WleptonicCuts=TH1F("h_WLeptonicPt_MjetVeto_WleptonicCuts",";W Leptonic Pt [GeV];",100,0,1000)
h_recoMWW_MjetVeto_WleptonicCuts=TH1F("h_recoMWW_MjetVeto_WleptonicCuts",";M_{WW} [GeV];",100,0,2000)
h_MET_MjetVeto_WleptonicCuts=TH1F("h_MET_MjetVeto_WleptonicCuts",";MET [GeV];",80,0,400)
h_pfcand_nextracks_MjetVeto_WleptonicCuts=TH1F("h_pfcand_nextracks_MjetVeto_WleptonicCuts",";Number of extra tracks;",100,-0.5,99.5)
h_num_vertices_MjetVeto_WleptonicCuts=TH1F("h_num_vertices_MjetVeto_WleptonicCuts",";Number of vertices;",100,-0.5,99.5)
h_num_vertices_preweight_MjetVeto_WleptonicCuts=TH1F("h_num_vertices_preweight_MjetVeto_WleptonicCuts",";Number of vertices;",100,-0.5,99.5)

h_lepton_pt_MjetVeto_WleptonicCuts_wJetPruning=TH1F("h_{0}_pt_MjetVeto_WleptonicCuts_wJetPruning".format(channel),";p_{{T}} ({0}) [GeV];".format(pname),100,0,1000)
h_jet_pt_MjetVeto_WleptonicCuts_wJetPruning=TH1F("h_jet_pt_MjetVeto_WleptonicCuts_wJetPruning",";p_{T} (jet) [GeV];",120,0,1200)
h_tau21_MjetVeto_WleptonicCuts_wJetPruning=TH1F("h_tau21_MjetVeto_WleptonicCuts_wJetPruning",";tau21;",100,0,2)
h_WLeptonicPt_MjetVeto_WleptonicCuts_wJetPruning=TH1F("h_WLeptonicPt_MjetVeto_WleptonicCuts_wJetPruning",";W Leptonic Pt [GeV];",100,0,1000)
h_recoMWW_MjetVeto_WleptonicCuts_wJetPruning=TH1F("h_recoMWW_MjetVeto_WleptonicCuts_wJetPruning",";M_{WW} [GeV];",100,0,2000)
h_pfcand_nextracks_MjetVeto_WleptonicCuts_wJetPruning=TH1F("h_pfcand_nextracks_MjetVeto_WleptonicCuts_wJetPruning",";Number of extra tracks;",100,-0.5,99.5)
h_xiCMS_45_wJetPruning=TH1F("h_xiCMS_45_wJetPruning",";xiCMS_45;",100,0,1)
h_xiCMS_56_wJetPruning=TH1F("h_xiCMS_56_wJetPruning",";xiCMS_56;",100,0,1)

h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_200_300=TH1F("h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_200_300",";Number of extra tracks;",100,-0.5,99.5)
h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_300_400=TH1F("h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_300_400",";Number of extra tracks;",100,-0.5,99.5)
h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_400_up=TH1F("h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_400_up",";Number of extra tracks;",100,-0.5,99.5)
h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_600_up=TH1F("h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_600_up",";Number of extra tracks;",100,-0.5,99.5)

h_mww_mx_ratio_et_norm=TH1F("h_mww_mx_ratio_et_norm",";MWW/MX;",100,0,2)
h_pfcand_nextracks_lowMWW_MX_PPStag=TH1F("h_pfcand_nextracks_lowMWW_MX_PPStag",";Number of extra tracks;",100,-0.5,99.5)

h_MWW_5_up_all=TH1F("h_MWW_5_up_all{0}".format(mname),";;",150,0,3000)
h_YCMS_5_up_all=TH1F("h_YCMS_5_up_all{0}".format(mname),";Y RP;",120,-3,3)

h_num_extra_tracks_nominal=TH1F("h_num_extra_tracks_nominal",";Number of extra tracks;",100,-0.5,99.5)

#In this case notPPS should be not passing all criteria
h_MWW_invertPrunedMass_notPPS=TH1F("h_MWW_invertPrunedMass_notPPS",";;",100,0,2000)
h_MWW_invertTau21_notPPS=TH1F("h_MWW_invertTau21_notPPS",";;",100,0,2000)
h_extracks_invertTau21_notPPS=TH1F("h_extracks_invertTau21_notPPS",";Number of extra tracks;",100,-0.5,99.5)
h_MWW_nominalTau21_notPPS=TH1F("h_MWW_nominalTau21_notPPS",";;",100,0,2000)
h_extracks_nominalTau21_notPPS=TH1F("h_extracks_nominalTau21_notPPS",";Number of extra tracks;",100,-0.5,99.5)
h_MWW_notPPS=TH1F("h_MWW_notPPS",";;",100,0,2000)
h_xiCMS_45_notPPS=TH1F("h_xiCMS_45_notPPS",";xiCMS_45;",100,0,1)
h_xiCMS_56_notPPS=TH1F("h_xiCMS_56_notPPS",";xiCMS_56;",100,0,1)
h_MWW_extra_tracks_0_4_notPPS_InvertPrunedMass=TH1F("h_MWW_extra_tracks_0_4_notPPS_InvertPrunedMass",";;",100,0,2000)
h_MWW_extra_tracks_0_4_notPPS=TH1F("h_MWW_extra_tracks_0_4_notPPS",";;",100,0,2000)
h_MWW_extra_tracks_5_15_notPPS=TH1F("h_MWW_extra_tracks_5_15_notPPS",";;",100,0,2000)
h_MWW_extra_tracks_5_up_notPPS_InvertPrunedMass=TH1F("h_MWW_extra_tracks_5_up_notPPS_InvertPrunedMass",";;",100,0,2000)
h_MWW_extra_tracks_5_up_notPPS=TH1F("h_MWW_extra_tracks_5_up_notPPS",";;",100,0,2000)
h_num_extra_tracks_notPPS=TH1F("h_num_extra_tracks_notPPS",";Number of extra tracks;",20,-0.5,99.5)
h_num_extra_tracks_notPPS_reweight_extra_tracks=TH1F("h_num_extra_tracks_notPPS_reweight_extra_tracks",";Number of extra tracks;",20,-0.5,99.5)
h_num_extra_tracks_notPPS_noDRl=TH1F("h_num_extra_tracks_notPPS_noDRl",";Number of extra tracks;",20,-0.5,99.5)

#For 2018 there is only two signal regions, so the PixelPixel will always be zero
selection=["MultiRP","PixelPixel","MultiPixel"]
for i in range(0,3):
    h_extra_tracks_vs_MWW_PPS.append(TH2F("h_extra_tracks_vs_MWW_PPS_{0}".format(selection[i]),";;",100,0,2000,100,-0.5,99.5))
    h_extra_tracks_vs_MX_PPS.append(TH2F("h_extra_tracks_vs_MX_PPS_{0}".format(selection[i]),";;",100,0,2000,100,-0.5,99.5))
    h_Y_CMS_minus_RP_vs_MWW_MX_PPS.append(TH2F("h_Y_CMS_minus_RP_vs_MWW_MX_PPS_{0}".format(selection[i]),"",100,0,2,60,-3,3))
    h_num_extra_tracks_PPS.append(TH1F("h_num_extra_tracks_PPS_{0}".format(selection[i]),";Number of extra tracks;",20,-0.5,99.5))
    h_num_extra_tracks_PPS_noDRl.append(TH1F("h_num_extra_tracks_PPS_noDRl_{0}".format(selection[i]),";Number of extra tracks;",20,-0.5,99.5))
    h_num_extra_tracks_PPS_reweight_extra_tracks.append(TH1F("h_num_extra_tracks_PPS_reweight_extra_tracks_{0}".format(selection[i]),";Number of extra tracks;",20,-0.5,99.5))
    h_xiCMS_45_passPPS.append(TH1F("h_xiCMS_45_passPPS_{0}".format(selection[i]),";xiCMS_45;",100,0,1))
    h_xiCMS_56_passPPS.append(TH1F("h_xiCMS_56_passPPS_{0}".format(selection[i]),";xiCMS_56;",100,0,1))
    h_lepton_pt_passPPS.append(TH1F("h_{0}_pt_passPPS_{1}".format(channel,selection[i]),";p_{T} (#mu) [GeV];",100,0,1000))
    h_jet_pt_passPPS.append(TH1F("h_jet_pt_passPPS_{0}".format(selection[i]),";p_{T} (jet) [GeV];",120,0,1200))
    h_tau21_passPPS.append(TH1F("h_tau21_passPPS_{0}".format(selection[i]),";tau21;",100,0,2))
    h_prunedMass_passPPS.append(TH1F("h_prunedMass_passPPS_{0}".format(selection[i]),";prunedMass [GeV];",200,0,1000))
    h_WLeptonicPt_passPPS.append(TH1F("h_WLeptonicPt_passPPS_{0}".format(selection[i]),";W Leptonic Pt [GeV];",100,0,1000))
    h_recoMWW_passPPS.append(TH1F("h_recoMWW_passPPS_{0}".format(selection[i]),";M_{WW} [GeV];",100,0,2000))
    h_MET_passPPS.append(TH1F("h_MET_passPPS_{0}".format(selection[i]),";MET [GeV];",80,0,400))
    h_MX_passPPS.append(TH1F("h_MX_passPPS_{0}".format(selection[i]),";Mass RP [GeV];",100,0,3000))
    h_MWW_MX_passPPS.append(TH1F("h_MWW_MX_passPPS_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_vs_MX_passPPS.append(TH2F("h_MWW_vs_MX_passPPS_{0}".format(selection[i]),";MWW/MX;",100,0,2000,100,0,2000))
    h_Y_CMS_minus_RP_passPPS.append(TH1F("h_Y_CMS_minus_RP_passPPS_{0}".format(selection[i]),";Y RP;",60,-3,3))
    h_xi_1_0_4_extratracks.append(TH1F("h_xi_1_0_4_extratracks_{0}".format(selection[i]),";#xi_{1};",128,0,0.32))
    h_xi_2_0_4_extratracks.append(TH1F("h_xi_2_0_4_extratracks_{0}".format(selection[i]),";#xi_{2};",128,0,0.32))
    h_Y_RP_0_4_extratracks.append(TH1F("h_Y_RP_0_4_extratracks_{0}".format(selection[i]),";Y RP;",60,-3,3))
    h_Y_CMS_minus_RP_0_4_extratracks.append(TH1F("h_Y_CMS_minus_RP_0_4_extratracks_{0}".format(selection[i]),";Y RP;",60,-3,3))
    h_MX_0_4_extratracks.append(TH1F("h_MX_0_4_extratracks_{0}".format(selection[i]),";Mass RP [GeV];",100,0,3000))
    h_MWW_0_4_extratracks.append(TH1F("h_MWW_0_4_extratracks_{0}".format(selection[i]),";M_{WW} [GeV];",100,0,3000))
    h_MWW_MX_0_4_tracks.append(TH1F("h_MWW_MX_0_4_tracks_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_xi1_0_4_tracks_misreco.append(TH1F("h_xi1_0_4_tracks_misreco_{0}".format(selection[i]),";MWW/MX;",128,0,0.32))
    h_xi2_0_4_tracks_misreco.append(TH1F("h_xi2_0_4_tracks_misreco_{0}".format(selection[i]),";MWW/MX;",128,0,0.32))
    h_MWW_MX_0_4_tracks_misreco.append(TH1F("h_MWW_MX_0_4_tracks_misreco_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_recoMWhad_0_4_tracks.append(TH1F("h_recoMWhad_0_4_tracks_{0}".format(selection[i]),";M_{W_{had}} [GeV];",100,0,200))
    h_tau21_0_4_tracks.append(TH1F("h_tau21_0_4_tracks_{0}".format(selection[i]),";tau21;",100,0,2))
    h_prunedMass_0_4_tracks.append(TH1F("h_prunedMass_0_4_tracks_{0}".format(selection[i]),";prunedMass [GeV];",200,0,1000))
    h_MWW_MX_0_4_tracks_Ycut.append(TH1F("h_MWW_MX_0_4_tracks_Ycut_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_0_4_tracks_misreco_Ycut.append(TH1F("h_MWW_MX_0_4_tracks_misreco_Ycut_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_0_4_tracks_100events.append(TH1F("h_MWW_MX_0_4_tracks_100events_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_0_4_tracks_100events_Ycut.append(TH1F("h_MWW_MX_0_4_tracks_100events_Ycut_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_xi_1_0_4_extratracks_notPPS.append(TH1F("h_xi_1_0_4_extratracks_notPPS_{0}".format(selection[i]),";#xi_{1};",128,0,0.32))
    h_xi_2_0_4_extratracks_notPPS.append(TH1F("h_xi_2_0_4_extratracks_notPPS_{0}".format(selection[i]),";#xi_{2};",128,0,0.32))
    h_Y_RP_0_4_extratracks_notPPS.append(TH1F("h_Y_RP_0_4_extratracks_notPPS_{0}".format(selection[i]),";Y RP;",60,-3,3))
    h_Y_CMS_minus_RP_0_4_extratracks_notPPS.append(TH1F("h_Y_CMS_minus_RP_0_4_extratracks_notPPS_{0}".format(selection[i]),";Y RP;",60,-3,3))
    h_MX_0_4_extratracks_notPPS.append(TH1F("h_MX_0_4_extratracks_notPPS_{0}".format(selection[i]),";Mass RP [GeV];",100,0,3000))
    h_MWW_0_4_extratracks_notPPS.append(TH1F("h_MWW_0_4_extratracks_notPPS_{0}".format(selection[i]),";M_{WW} [GeV];",100,0,3000))
    h_MWW_MX_0_4_tracks_notPPS.append(TH1F("h_MWW_MX_0_4_tracks_notPPS_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_recoMWhad_0_4_tracks_notPPS.append(TH1F("h_recoMWhad_0_4_tracks_notPPS_{0}".format(selection[i]),";M_{W_{had}} [GeV];",100,0,200))
    h_tau21_0_4_tracks_notPPS.append(TH1F("h_tau21_0_4_tracks_notPPS_{0}".format(selection[i]),";tau21;",100,0,2))
    h_prunedMass_0_4_tracks_notPPS.append(TH1F("h_prunedMass_0_4_tracks_notPPS_{0}".format(selection[i]),";prunedMass [GeV];",200,0,1000))
    h_MWW_MX_0_4_tracks_notPPS_Ycut.append(TH1F("h_MWW_MX_0_4_tracks_notPPS_Ycut_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_xi_1_control.append(TH1F("h_xi_1_control_{0}".format(selection[i]),";#xi_{1};",128,0,0.32))
    h_xi_2_control.append(TH1F("h_xi_2_control_{0}".format(selection[i]),";#xi_{2};",128,0,0.32))
    h_Y_RP_control.append(TH1F("h_Y_RP_control_{0}".format(selection[i]),";Y RP;",60,-3,3))
    h_Y_CMS_minus_RP_control.append(TH1F("h_Y_CMS_minus_RP_control_{0}".format(selection[i]),";Y RP;",60,-3,3))
    h_MX_control.append(TH1F("h_MX_control_{0}".format(selection[i]),";Mass RP [GeV];",100,0,3000))
    h_MWW_control.append(TH1F("h_MWW_control_{0}".format(selection[i]),";M_{WW} [GeV];",100,0,3000))
    h_MWW_MX_control.append(TH1F("h_MWW_MX_control_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_recoMWhad_control_control.append(TH1F("h_recoMWhad_control_control_{0}".format(selection[i]),";M_{W_{had}} [GeV];",100,0,200))
    h_tau21_control_control.append(TH1F("h_tau21_control_control_{0}".format(selection[i]),";tau21;",100,0,2))
    h_prunedMass_control_control.append(TH1F("h_prunedMass_control_control_{0}".format(selection[i]),";prunedMass [GeV];",200,0,1000))
    h_MWW_MX_control_Ycut.append(TH1F("h_MWW_MX_control_Ycut_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_5_up_notPPS.append(TH1F("h_MWW_MX_5_up_notPPS_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_5_up_Ycut_notPPS.append(TH1F("h_MWW_MX_5_up_Ycut_notPPS_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_xi_1_control_notPPS.append(TH1F("h_xi_1_control_notPPS_{0}".format(selection[i]),";#xi_{1};",128,0,0.32))
    h_xi_2_control_notPPS.append(TH1F("h_xi_2_control_notPPS_{0}".format(selection[i]),";#xi_{2};",128,0,0.32))
    h_Y_RP_control_notPPS.append(TH1F("h_Y_RP_control_notPPS_{0}".format(selection[i]),";Y RP;",60,-3,3))
    h_Y_CMS_minus_RP_control_notPPS.append(TH1F("h_Y_CMS_minus_RP_control_notPPS_{0}".format(selection[i]),";Y RP;",60,-3,3))
    h_MX_control_notPPS.append(TH1F("h_MX_control_notPPS_{0}".format(selection[i]),";Mass RP [GeV];",100,0,3000))
    h_MWW_control_notPPS.append(TH1F("h_MWW_control_notPPS_{0}".format(selection[i]),";M_{WW} [GeV];",100,0,3000))
    h_MWW_MX_control_notPPS.append(TH1F("h_MWW_MX_control_notPPS_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_recoMWhad_control_control_notPPS.append(TH1F("h_recoMWhad_control_control_notPPS_{0}".format(selection[i]),";M_{W_{had}} [GeV];",100,0,200))
    h_tau21_control_control_notPPS.append(TH1F("h_tau21_control_control_notPPS_{0}".format(selection[i]),";tau21;",100,0,2))
    h_prunedMass_control_control_notPPS.append(TH1F("h_prunedMass_control_control_notPPS_{0}".format(selection[i]),";prunedMass [GeV];",200,0,1000))
    h_MWW_MX_control_Ycut_notPPS.append(TH1F("h_MWW_MX_control_Ycut_notPPS_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_xi_1_5_up.append(TH1F("h_xi_1_5_up_{0}".format(selection[i]),";#xi_{1};",128,0,0.32))
    h_xi_2_5_up.append(TH1F("h_xi_2_5_up_{0}".format(selection[i]),";#xi_{2};",128,0,0.32))
    h_MX_5_up.append(TH1F("h_MX_5_up_{0}".format(selection[i]),";Mass RP [GeV];",100,0,3000))
    h_MWW_5_up.append(TH1F("h_MWW_5_up_{0}".format(selection[i]),";M_{WW} [GeV];",100,0,3000))
    h_Y_RP_5_up.append(TH1F("h_Y_RP_5_up_{0}".format(selection[i]),";Y RP;",60,-3,3))
    h_Y_CMS_minus_RP_5_up.append(TH1F("h_Y_CMS_minus_RP_5_up_{0}".format(selection[i]),";Y RP;",60,-3,3))
    h_MWW_MX_5_up.append(TH1F("h_MWW_MX_5_up_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_5_up_InvertPrunedMass.append(TH1F("h_MWW_MX_5_up_InvertPrunedMass_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_0_4_InvertPrunedMass.append(TH1F("h_MWW_MX_0_4_InvertPrunedMass_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_invertPrunedMass.append(TH1F("h_MWW_invertPrunedMass_{0}".format(selection[i]),";;",100,0,2000))
    h_MWW_MX_invertPrunedMass_Ycut.append(TH1F("h_MWW_MX_invertPrunedMass_Ycut_{0}".format(selection[i]),";;",100,0,2000))
    h_MWW_MX_control_5_up_Ycut.append(TH1F("h_MWW_MX_control_5_up_Ycut_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_control_5_up_Ycut_InvertPrunedMass.append(TH1F("h_MWW_MX_control_5_up_Ycut_InvertPrunedMass_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_control_0_4_Ycut_InvertPrunedMass.append(TH1F("h_MWW_MX_control_0_4_Ycut_InvertPrunedMass_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_control_15_30.append(TH1F("h_MWW_MX_control_15_30_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_control_30_50.append(TH1F("h_MWW_MX_control_30_50_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_control_50_70.append(TH1F("h_MWW_MX_control_50_70_{0}".format(selection[i]),";MWW/MX;",100,0,2))
    h_MWW_MX_control_70_100.append(TH1F("h_MWW_MX_control_70_100_{0}".format(selection[i]),";MWW/MX;",100,0,2))

selection_det=["3","23","103","123"]
for i in range(0,4):
    h_y_vs_x_signal.append(TH2F("h_y_vs_x_signal_{0}".format(selection_det[i]),";x (mm);y (mm)",200,0,27,240,-13,6))


#Plots that I don't look at as much
#Can remove these
h_lepton2_pt_MjetVeto_WleptonicCuts=TH1F("h_lepton2_pt_MjetVeto_WleptonicCuts",";p_{T} (l2) [GeV];",100,0,1000)
h_lepton2_eta_MjetVeto_WleptonicCuts=TH1F("h_lepton2_eta_MjetVeto_WleptonicCuts",";#eta_{l2};",60,-3,3)
h_MassLL_MjetVeto_WleptonicCuts=TH1F("h_MassLL_MjetVeto_WleptonicCuts",";Mass#_{ll};",100,0,200)

h_extra_tracks_vs_MWW_notPPS=TH2F("h_extra_tracks_vs_MWW_notPPS",";;",100,0,2000,100,-0.5,99.5)
h_pt_lepton_vs_Mass=TH2F("h_pt_lepton_vs_Mass","",100,0,2000,120,0,1200)
h_pt_jet_vs_Mass=TH2F("h_pt_jet_vs_Mass","",100,0,2000,120,0,1200)
h_xiCMS_vs_xiPPS_45=TH2F("h_xiCMS_vs_xiPPS_45",";;",200,0,1,200,0,1)
h_xiCMS_vs_xiPPS_56=TH2F("h_xiCMS_vs_xiPPS_56",";;",200,0,1,200,0,1)
h_signal_protons_eacharm=TH2F("h_signal_protons_eacharm",";;",10,-0.5,9.5,10,-0.5,9.5)

Run=0.
event=0.
num_events=chain.GetEntries()
num_dataev_mixed_in=100
print num_events

it=0
#This defines a dictionary that is used to look for any duplicate events.
re_dict={}
era=""
batch_prefix=""
if not batch: batch_prefix="inputfiles/"
if DATA:
    era=file_dir[12]
    #era=findEra(e.run)
else:
    if year == "2018":
        era=RandomEraFine2018()
    if year == "2017":
        era=RandomEra()

#Obtain ntuple for protons to mix in for data/MC and with proper corrections for data
f2=TFile()
print "era: ",era
if year=="2018":
    #f2=TFile("SingleMuon_Run2018{0}-justProtons.root".format(era))
    if channel == "muon":
        f2=TFile("{0}xiEventsRun{1}-2018.root".format(batch_prefix,era[0]))
    if channel == "electron":
        f2=TFile("{0}xiEventsRun{1}-2018-e.root".format(batch_prefix,era[0]))
    #f2=TFile("2020-07-17-RunsABCD-AllProtons/SingleMuon_Run2018A-justProtons.root")
elif year == "2017" and channel == "electron":
    f2=TFile("{0}ElectronDataProtonsRun{0}.root".format(batch_prefix,era))
treeProtons=f2.Get("SlimmedNtuple")
treeProtonsEntries=treeProtons.GetEntries()
evm=eventListMixing()

print("Just before loop --- %s seconds ---" % (time.time() - start_time))
for e in chain:
    #print("Start of loop --- %s seconds ---" % (time.time() - start_time))
    #For events with no Xi cut remove the overlap with centrally produced samples
    #if "GG" in sample_name:

    #print e.crossingAngle

    if "GGToWW" in sample_name:
        #if e.gen_proton_xi[0]<0.2 and e.gen_proton_xi[1]<0.2:
        if e.gen_proton_xi[0]>0.2 or e.gen_proton_xi[1]>0.2:
            if e.gen_proton_xi[0]<0.01 or e.gen_proton_xi[1]<0.01:
                continue
    if it == 0:
        print "Get to first event in loop"
    it=it+1
    event_itt=5e6
    if job_number>0 and job_number<7:
        if not (it>=(job_number-1)*event_itt and it<(job_number*event_itt)):
            continue
    if job_number==7:
        if not (it>=(job_number-1)*event_itt):
            continue
    #if it>500:
    #    break
    run=e.run
    #print run
    event=e.event
    #print event
    lumi=e.lumiblock
    runstring=str(run)+":"+str(lumi)
    if DATA:
        if runstring in re_dict:
            list0=re_dict[runstring]
            #Skip event if it is a duplicate
            if int(event) in list0:
                continue
                print "Duplicate event"
            else:
                list0.append(int(event))
        else:
            re_dict[runstring]=[int(event)]
    #print re_dict
    if event==241461846:
        print "event 241461846"
    pileupw=e.pileupWeight

    jet_veto=False
    mjet_veto=False
    #Look at events passing preselection and jet veto
    if e.num_jets_ak4<1 and e.num_bjets_ak8 < 1:
        jet_veto=True
    if e.num_bjets_ak4<1:
        mjet_veto=True

    #Make sure there is the correct number of leptons in sample or continue
    if channel=="electron" and e.electron_pt.size() == 0:
        continue
    if channel=="electron" and e.electron_pt.size() > 1:
        continue
    if channel=="muon" and e.muon_pt.size() == 0:
        continue
    if channel=="muon" and e.muon_pt.size() > 1:
        continue
    if channel=="dimuon" and e.muon_pt.size() < 2:
        continue
    if channel=="dielectron" and e.electron_pt.size() < 2:
        continue
    if channel=="electron":
        l_pt=e.electron_pt[0]
        if l_pt<50:
            continue
        l_eta=e.electron_eta[0]
        l_phi=e.electron_phi[0]
        if not DATA:
            pileupw=pileupw*electronScaleFactor(l_pt,l_eta,year,batch_prefix)
    if channel=="muon":
        l_pt=e.muon_pt[0]
        if l_pt<50:
            continue
        l_eta=e.muon_eta[0]
        l_phi=e.muon_phi[0]
        if not DATA:
            pileupw=pileupw*muonScaleFactor(l_pt,l_eta,year,batch_prefix)
    
    dphi_lepton_jet=GetDphi(l_phi,e.jet_phi[0])
    deta_lepton_jet=l_eta-e.jet_eta[0]
    deltaR=m.sqrt(dphi_lepton_jet*dphi_lepton_jet+deta_lepton_jet*deta_lepton_jet   )
    dphi_jet_met=abs(GetDphi(e.jet_phi[0],e.met_phi))
    dphi_jet_Wl=abs(GetDphi(e.jet_phi[0],e.WLeptonicPhi))
    h_deltaR_lepton_jet.Fill(deltaR,pileupw)
    h_deltaphi_jet_met.Fill(dphi_jet_met,pileupw)
    h_deltaphi_jet_Wleptonic.Fill(dphi_jet_Wl,pileupw)

    if channel=="electron" or channel=="muon":
        if deltaR<= (m.pi/2):
            continue
        if dphi_jet_met<=2:
            continue
        if dphi_jet_Wl<=2:
            continue


    recoMWhad=-999.
    recoMWhad=e.recoMWhad
    recoMWlep=e.recoMWlep
    dphiWW=abs(e.dphiWW)
    recoMWW=e.recoMWW
    MET=e.met
    WLeptonicPt=e.WLeptonicPt

    recoYCMS=e.recoRapidityWW
    pfcand_nextracks=e.pfcand_nextracks
    pfcand_nextracks_noDRl=e.pfcand_nextracks_noDRl
    tau21=e.jet_tau2[0]/e.jet_tau1[0]
    prunedMass=e.jet_corrmass[0]
    #xiCMS_45=0.
    #xiCMS_56=0.
    #if not (DATA and channel=="electron"):
    WLeptonicEta=e.WLeptonicEta
    xiCMS_45=(1/13000.)*(WLeptonicPt*m.exp(WLeptonicEta)+e.jet_pt[0]*m.exp(e.jet_eta[0]))
    xiCMS_56=(1/13000.)*(WLeptonicPt*m.exp(-WLeptonicEta)+e.jet_pt[0]*m.exp(-e.jet_eta[0]))

    #Plots after jet pruning requirements.
    jet_pruning=False
    #if tau21<0.6 and prunedMass>40 and prunedMass<120:
    #if tau21<0.6 and prunedMass>50 and prunedMass<110:
    if prunedMass>50 and prunedMass<110 and tau21<0.6:
    #if prunedMass>50 and prunedMass<110:
        jet_pruning=True

    passesBoosted=False
    if dphiWW>2.5 and recoMWW>500 and MET>METCUT and WLeptonicPt>200:
        passesBoosted=True

    #Looking at Mauricio jet veto with W leptonic cuts
    if e.num_bjets_ak4<1 and passesBoosted:
        h_pt_lepton_vs_Mass.Fill(recoMWW,l_pt)
        h_pt_jet_vs_Mass.Fill(recoMWW,e.jet_pt[0])
        h_lepton_pt_MjetVeto_WleptonicCuts.Fill(l_pt,pileupw)
        h_lepton_eta_MjetVeto_WleptonicCuts.Fill(l_eta,pileupw)
        h_jet_pt_MjetVeto_WleptonicCuts.Fill(e.jet_pt[0],pileupw)
        h_jet_eta_MjetVeto_WleptonicCuts.Fill(e.jet_eta[0],pileupw)
        h_tau21_MjetVeto_WleptonicCuts.Fill(tau21,pileupw)
        h_prunedMass_MjetVeto_WleptonicCuts.Fill(prunedMass,pileupw)
        h_recoMWhad_MjetVeto_WleptonicCuts.Fill(recoMWhad,pileupw)
        h_recoMWlep_MjetVeto_WleptonicCuts.Fill(recoMWlep,pileupw)
        h_dphiWW_MjetVeto_WleptonicCuts.Fill(dphiWW,pileupw)
        h_WLeptonicPt_MjetVeto_WleptonicCuts.Fill(WLeptonicPt,pileupw)
        h_recoMWW_MjetVeto_WleptonicCuts.Fill(recoMWW,pileupw)
        h_MET_MjetVeto_WleptonicCuts.Fill(MET,pileupw)
        h_pfcand_nextracks_MjetVeto_WleptonicCuts.Fill(pfcand_nextracks,pileupw)
        h_num_vertices_MjetVeto_WleptonicCuts.Fill(e.nVertices)
        h_num_vertices_preweight_MjetVeto_WleptonicCuts.Fill(e.nVertices,pileupw)
        #print "{}:{}:{}".format(run,e.lumiblock,event)
        #additionalDileptonPlots(e)
        if channel=="dimuon":
            l1 = TLorentzVector(e.muon_px[0],e.muon_py[0],e.muon_pz[0],e.muon_e[0])
            l2 = TLorentzVector(e.muon_px[1],e.muon_py[1],e.muon_pz[1],e.muon_e[1])
            lCombined = l1+l2
            h_lepton2_pt_MjetVeto_WleptonicCuts.Fill(e.muon_pt[1],pileupw)
            h_lepton2_eta_MjetVeto_WleptonicCuts.Fill(e.muon_eta[1],pileupw)
            h_MassLL_MjetVeto_WleptonicCuts.Fill(lCombined.M(),pileupw)
        if channel=="dielectron":
            l1 = TLorentzVector(e.electron_px[0],e.electron_py[0],e.electron_pz[0],e.electron_e[0])
            l2 = TLorentzVector(e.electron_px[1],e.electron_py[1],e.electron_pz[1],e.electron_e[1])
            lCombined = l1+l2
            h_lepton2_pt_MjetVeto_WleptonicCuts.Fill(e.electron_pt[1],pileupw)
            h_lepton2_eta_MjetVeto_WleptonicCuts.Fill(e.electron_eta[1],pileupw)
            h_MassLL_MjetVeto_WleptonicCuts.Fill(lCombined.M(),pileupw)

    if e.num_bjets_ak4<1 and passesBoosted and jet_pruning:
        h_lepton_pt_MjetVeto_WleptonicCuts_wJetPruning.Fill(l_pt,pileupw)
        h_jet_pt_MjetVeto_WleptonicCuts_wJetPruning.Fill(e.jet_pt[0],pileupw)
        h_tau21_MjetVeto_WleptonicCuts_wJetPruning.Fill(tau21,pileupw)
        h_WLeptonicPt_MjetVeto_WleptonicCuts_wJetPruning.Fill(WLeptonicPt,pileupw)
        h_recoMWW_MjetVeto_WleptonicCuts_wJetPruning.Fill(recoMWW,pileupw)
        h_pfcand_nextracks_MjetVeto_WleptonicCuts_wJetPruning.Fill(pfcand_nextracks,pileupw)
        h_xiCMS_45_wJetPruning.Fill(xiCMS_45,pileupw)
        h_xiCMS_56_wJetPruning.Fill(xiCMS_56,pileupw)
        #if xiCMS_45>0.2 or xiCMS_56>0.2:
        #    continue
        if pfcand_nextracks>4:
            h_MWW_5_up_all.Fill(recoMWW,pileupw)
            h_YCMS_5_up_all.Fill(recoYCMS,pileupw)

    if xiCMS_45 > 0.2 or xiCMS_56 > 0.2:
        continue

    #Looking at extra tracks as a function of W pt
    if e.num_bjets_ak4<1 and passesBoosted and ( (DATA and pfcand_nextracks >4) or not DATA):
        if WLeptonicPt > 200 and WLeptonicPt < 300:
            h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_200_300.Fill(pfcand_nextracks,pileupw)
        if WLeptonicPt > 300 and WLeptonicPt < 400:
            h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_300_400.Fill(pfcand_nextracks,pileupw)
        if WLeptonicPt > 400:
            h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_400_up.Fill(pfcand_nextracks,pileupw)
        if WLeptonicPt > 600:
            h_pfcand_nextracks_MjetVeto_WleptonicCuts_Wpt_600_up.Fill(pfcand_nextracks,pileupw)

    #Up until now have only looked at CMS information, no PPS information
    #Only look at CMS stuff
    #continue

    ######################################################################
    #Now Add PPS requirements
    ######################################################################
    #Look to see if passing PPS
    xi = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[],"weight":[],"multi_arm0":[],"multi_arm1":[]}
    xi_data_mix = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[],"weight":[],"multi_arm0":[],"multi_arm1":[]}
    #passesPPS=[]
    rw_extrk=1.
    rw_passPPS=1.
    rw_failPPS=1.
    
    #Better way to get protons. For MC will mix in data protons
    #Here need to submit for 3 different signal regions
    passesPPS=[False,False,False]
    passesPPSMisReco=[False,False,False]
    ismisreco=False
    if mjet_veto and passesBoosted and tau21<0.6:
        #passesPPS=passPPSGeneral(e,xi,signal_bin,sample)
        if sample == "ExclusiveMC":
            #passesPPS=passPPSGeneralSignal(e,xi,sample)
            output=passPPSGeneralSignal(e,xi,sample,year,era,evm)
            #print output
            if output[0] == False:
                ismisreco=False
                passesPPS=output[1]
                #print "ismisreco: ",ismisreco
            else:
                ismisreco=True
                passesPPSMisReco=output[1]
            plotXYSignal(e,h_y_vs_x_signal)
            plot_number_protons(e,h_signal_protons_eacharm,year,xi)
            #passPPSMulti(e,xi_det)
            #passPPSNewPixel(e,xi_det)
            #passPPSNewStrip(e,xi_det)
        if sample == "Data":
            passesPPS=passPPSGeneralData(e,xi,era,sample_name,year)
        if sample == "MC":
            passesPPS=passPPSGeneralMixDataMC(e,xi,sample,era,year,treeProtons,treeProtonsEntries,evm)

    #Mixing in protons with data events not passing PPS, currently there is overlap between control regions.
    failsAllPPS=False
    if passesPPS[0] == 0 and passesPPS[1] == 0 and passesPPS[2] == 0:
        failsAllPPS=True

    passPPS2=[False,False,False]
    #if mjet_veto and passesBoosted and jet_pruning and DATA and not passesPPS:
    if mjet_veto and passesBoosted and jet_pruning and DATA and failsAllPPS:
        #print("Write before passPPSGeneralMixDataMC --- %s seconds ---" % (time.time() - start_time))
        passPPS2=passPPSGeneralMixDataMC(e,xi_data_mix,sample,era,year,treeProtons,treeProtonsEntries,evm)
        #print("Write after passPPSGeneralMixDataMC --- %s seconds ---" % (time.time() - start_time))

    #Inverting the pruned mass cut to get MWW/MX distribution.
    if mjet_veto and passesBoosted and tau21<0.6 and prunedMass<50 and failsAllPPS:    
        h_MWW_invertPrunedMass_notPPS.Fill(recoMWW,pileupw*rw_extrk*rw_passPPS)

    if mjet_veto and passesBoosted and prunedMass>50 and prunedMass<110 and tau21>0.6 and failsAllPPS:    
        h_MWW_invertTau21_notPPS.Fill(recoMWW,pileupw*rw_extrk*rw_passPPS)
        h_extracks_invertTau21_notPPS.Fill(pfcand_nextracks,pileupw)

    if mjet_veto and passesBoosted and jet_pruning and failsAllPPS:    
        h_MWW_nominalTau21_notPPS.Fill(recoMWW,pileupw*rw_extrk*rw_passPPS)
        h_extracks_nominalTau21_notPPS.Fill(pfcand_nextracks,pileupw)

    #Looking at control region not passing PPS to get ratio of high to low for MWW.
    if mjet_veto and passesBoosted and jet_pruning and failsAllPPS:
        h_xiCMS_45_notPPS.Fill(xiCMS_45,pileupw)
        h_xiCMS_56_notPPS.Fill(xiCMS_56,pileupw)
        h_MWW_notPPS.Fill(recoMWW,pileupw*rw_failPPS)        
        h_extra_tracks_vs_MWW_notPPS.Fill(recoMWW,pfcand_nextracks,pileupw*rw_failPPS)
    if mjet_veto and passesBoosted and jet_pruning and failsAllPPS and pfcand_nextracks<5:
        h_MWW_extra_tracks_0_4_notPPS.Fill(recoMWW,pileupw*rw_failPPS)        
    if mjet_veto and prunedMass<50 and tau21<0.6 and failsAllPPS and pfcand_nextracks<5:    
        h_MWW_extra_tracks_0_4_notPPS_InvertPrunedMass.Fill(recoMWW,pileupw*rw_failPPS)        
    if mjet_veto and passesBoosted and jet_pruning and failsAllPPS and pfcand_nextracks>4 and pfcand_nextracks<16:
        h_MWW_extra_tracks_5_15_notPPS.Fill(recoMWW,pileupw*rw_failPPS)
    if mjet_veto and passesBoosted and jet_pruning and failsAllPPS and pfcand_nextracks>4:
        h_MWW_extra_tracks_5_up_notPPS.Fill(recoMWW,pileupw*rw_failPPS)
    if mjet_veto and prunedMass<50 and tau21<0.6 and failsAllPPS and pfcand_nextracks>4:    
        h_MWW_extra_tracks_5_up_notPPS_InvertPrunedMass.Fill(recoMWW,pileupw*rw_failPPS)        


    #Looking at control region not passing PPS, this is for EXTRA TRACKS reweighting
    if mjet_veto and passesBoosted and jet_pruning and failsAllPPS:
        h_num_extra_tracks_notPPS.Fill(pfcand_nextracks,pileupw*rw_failPPS)
        h_num_extra_tracks_notPPS_noDRl.Fill(pfcand_nextracks_noDRl,pileupw*rw_failPPS)
        if DATA:
            h_num_extra_tracks_notPPS_reweight_extra_tracks.Fill(pfcand_nextracks,pileupw*rw_failPPS)
        else:
            h_num_extra_tracks_notPPS_reweight_extra_tracks.Fill(pfcand_nextracks,pileupw*rw_extrk*rw_failPPS)

    #This block is for misreconstructed signal, one proton from signal, one from pileup
    signal_samples=["multiRP","pixel-pixel","multiPixel"]
    for i in range(0,3):
        if mjet_veto and passesBoosted and jet_pruning and failsAllPPS and \
           passesPPSMisReco[i] and sample == "ExclusiveMC" and pfcand_nextracks < 5:
            #print xi_misreco["23"]
            xi_misreco_1=max(xi["23"])
            xi_misreco_2=max(xi["123"])
            rapidity_misreco=0.5*m.log(xi_misreco_1/xi_misreco_2)
            mrp_misreco=m.sqrt(169000000*xi_misreco_1*xi_misreco_2)
            Yvalue_misreco=abs(recoYCMS-rapidity_misreco)
            #passYcut_misreco=[passYcutFunc2(Yvalue_misreco,"multiRP"),passYcutFunc2(Yvalue_misreco,"pixel-pixel"),passYcutFunc2(Yvalue_misreco,"multiPixel")]
            passYcut_misreco=passYcutFunc2(Yvalue_misreco,signal_samples[i])
            #print signal_samples[i]
            if i < 0:
                if xi["arm_mr"][0] == "45":
                    #h_xi1_0_4_tracks_misreco[i].Fill(e.gen_proton_xi[0])
                    h_xi1_0_4_tracks_misreco[i].Fill(xi_misreco_1)
                if xi["arm_mr"][0] == "56":
                    #h_xi2_0_4_tracks_misreco[i].Fill(e.gen_proton_xi[1])
                    h_xi2_0_4_tracks_misreco[i].Fill(xi_misreco_2)
            if xi_misreco_1>0.04 and xi_misreco_2>0.04:
                h_MWW_MX_0_4_tracks_misreco[i].Fill(recoMWW/mrp_misreco,pileupw)
                if passYcut_misreco:
                    h_MWW_MX_0_4_tracks_misreco_Ycut[i].Fill(recoMWW/mrp_misreco,pileupw)
    if ismisreco:
        continue

    #This is to produce background prediction from MC mixed with data protons
    if not ExclusiveMC and not DATA and mjet_veto and passesBoosted and \
       jet_pruning and pfcand_nextracks < 5:
        for i in range(1,num_dataev_mixed_in):
            xi_signal = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[],"weight":[],"multi_arm0":[],"multi_arm1":[]}
            #xi_signal = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[]}
            #protonDataMixing(xi_signal,signal_bin)
            passPPS_100=passPPSGeneralMixDataMC(e,xi_signal,sample,era,year,treeProtons,treeProtonsEntries,evm)
            
            if not passPPS_100[0] and not passPPS_100[1] and not passPPS_100[2]: continue
            #print "xi_signal",xi_signal
            mww_100=protonMWWMixing(batch_prefix,year)
            yww_100=protonYWWMixing(batch_prefix,year)
            xi_1=max(xi_signal["23"])
            xi_2=max(xi_signal["123"])
            if xi_1<0.04 or xi_2<0.04:
                continue
            rapidity_100=0.5*m.log(xi_1/xi_2)
            mrp_100=m.sqrt(169000000*xi_1*xi_2)
            for i in range(0,3):
                if passPPS_100[i]: h_MWW_MX_0_4_tracks_100events[i].Fill(mww_100/mrp_100,0.01)
            Yvalue_100=abs(yww_100-rapidity_100)
            passYcut_100=[passYcutFunc2(Yvalue_100,"multiRP"),passYcutFunc2(Yvalue_100,"pixel-pixel"),passYcutFunc2(Yvalue_100,"multiPixel")]
            for i in range(0,3):
                if passYcut_100[i] and passPPS_100[i]:
                    h_MWW_MX_0_4_tracks_100events_Ycut[i].Fill(mww_100/mrp_100,0.01)


    passYcut=[False,False,False]
    for i in range(0,3):
        M_RP=-999.
        Rapidity_RP=-999.
        xi_mult_45=-999.
        xi_mult_56=-999.
        if passesPPS[i]:
            #if mjet_veto and passesBoosted and jet_pruning:
            if mjet_veto and passesBoosted and tau21<0.6:
                if len(xi["23"])>0 and len(xi["123"])>0:
                    xi_mult_45=max(xi["23"])
                    xi_mult_56=max(xi["123"])
                    #M_RP=m.sqrt(169000000*xi["23"][0]*xi["123"][0])
                    M_RP=m.sqrt(169000000*xi_mult_45*xi_mult_56)
                    if xi["23"][0] > 0 and xi["123"][0] > 0:
                        Rapidity_RP=0.5*m.log(xi_mult_45/xi_mult_56)

        elif passPPS2[i]:
            #if mjet_veto and passesBoosted and jet_pruning:
            if mjet_veto and passesBoosted and tau21<0.6:
                xi["23"]=xi_data_mix["23"]
                xi["123"]=xi_data_mix["123"]
                if len(xi["23"])>0 and len(xi["123"])>0:
                    xi_mult_45=max(xi["23"])
                    xi_mult_56=max(xi["123"])
                    #M_RP=m.sqrt(169000000*xi["23"][0]*xi["123"][0])
                    M_RP=m.sqrt(169000000*xi_mult_45*xi_mult_56)
                    if xi["23"][0] > 0 and xi["123"][0] > 0:
                        Rapidity_RP=0.5*m.log(xi_mult_45/xi_mult_56)

        Yvalue=abs(recoYCMS-Rapidity_RP)
        passYcut[i]=passYcutFunc2(Yvalue,signal_samples[i])
        if len(xi["23"])<1 or len(xi["123"])<1:
            continue
        if xi_mult_45<0.04 or xi_mult_56<0.04:
            continue

        if mjet_veto and passesBoosted and jet_pruning and passesPPS[i]:
            h_xiCMS_45_passPPS[i].Fill(xiCMS_45,pileupw)
            h_xiCMS_56_passPPS[i].Fill(xiCMS_56,pileupw)
            h_lepton_pt_passPPS[i].Fill(l_pt,pileupw)
            h_jet_pt_passPPS[i].Fill(e.jet_pt[0],pileupw)
            h_tau21_passPPS[i].Fill(tau21,pileupw)
            h_prunedMass_passPPS[i].Fill(prunedMass,pileupw)
            h_WLeptonicPt_passPPS[i].Fill(WLeptonicPt,pileupw)
            h_recoMWW_passPPS[i].Fill(recoMWW,pileupw)
            h_MET_passPPS[i].Fill(MET,pileupw)
            h_MX_passPPS[i].Fill(M_RP,pileupw)
            #if i==0:
            #    print "Run: {0}, Event: {1}".format(run,event)
            h_Y_CMS_minus_RP_passPPS[i].Fill(recoYCMS-Rapidity_RP,pileupw)
            h_MWW_MX_passPPS[i].Fill(recoMWW/M_RP,pileupw)
            h_MWW_vs_MX_passPPS[i].Fill(M_RP,recoMWW)

        if mjet_veto and passesBoosted and jet_pruning and passesPPS[i]:
            if DATA and pfcand_nextracks>4:
                h_Y_CMS_minus_RP_vs_MWW_MX_PPS[i].Fill(recoMWW/M_RP,recoYCMS-Rapidity_RP)
                h_num_extra_tracks_PPS[i].Fill(pfcand_nextracks,pileupw*rw_passPPS)
                h_num_extra_tracks_PPS_noDRl[i].Fill(pfcand_nextracks_noDRl,pileupw*rw_passPPS)
                h_num_extra_tracks_PPS_reweight_extra_tracks[i].Fill(pfcand_nextracks,pileupw*rw_extrk*rw_passPPS)
                h_extra_tracks_vs_MWW_PPS[i].Fill(recoMWW,pfcand_nextracks,pileupw*rw_passPPS)
                h_extra_tracks_vs_MX_PPS[i].Fill(M_RP,pfcand_nextracks,pileupw*rw_passPPS)
            if not DATA:
                h_num_extra_tracks_PPS[i].Fill(pfcand_nextracks,pileupw*rw_passPPS)
                h_num_extra_tracks_PPS_reweight_extra_tracks[i].Fill(pfcand_nextracks,pileupw*rw_extrk*rw_passPPS)
                h_num_extra_tracks_PPS_noDRl[i].Fill(pfcand_nextracks_noDRl,pileupw*rw_passPPS)


        if mjet_veto and passesBoosted and jet_pruning and passesPPS[i] and not DATA:    
            if pfcand_nextracks<5:
                h_xi_1_0_4_extratracks[i].Fill(xi["23"][0],pileupw*rw_extrk*rw_passPPS)
                h_xi_2_0_4_extratracks[i].Fill(xi["123"][0],pileupw*rw_extrk*rw_passPPS)
                h_MX_0_4_extratracks[i].Fill(M_RP,pileupw*rw_extrk*rw_passPPS)
                h_MWW_0_4_extratracks[i].Fill(recoMWW,pileupw*rw_extrk*rw_passPPS)
                h_Y_RP_0_4_extratracks[i].Fill(Rapidity_RP,pileupw*rw_extrk*rw_passPPS)
                h_Y_CMS_minus_RP_0_4_extratracks[i].Fill(recoYCMS-Rapidity_RP,pileupw*rw_extrk*rw_passPPS) 
                if ExclusiveMC:
                    #h_MWW_MX_0_4_tracks[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS*xi["weight"][0])
                    #print "Get to fill: h_MWW_MX_0_4_tracks[i]"
                    h_MWW_MX_0_4_tracks[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)
                else:h_MWW_MX_0_4_tracks[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)
                h_recoMWhad_0_4_tracks[i].Fill(recoMWhad,pileupw*rw_extrk*rw_passPPS)
                h_tau21_0_4_tracks[i].Fill(tau21,pileupw)
                h_prunedMass_0_4_tracks[i].Fill(prunedMass,pileupw)
                if passYcut[i]:
                    if ExclusiveMC:
                        #h_MWW_MX_0_4_tracks_Ycut[i].Fill(recoMWW/M_RP,pileupw*xi["weight"][0])
                        #print "Get to fill: h_MWW_MX_0_4_tracks_Ycut[i]"
                        h_MWW_MX_0_4_tracks_Ycut[i].Fill(recoMWW/M_RP,pileupw)
                    else:h_MWW_MX_0_4_tracks_Ycut[i].Fill(recoMWW/M_RP,pileupw)

        #Signal plots in data, only looking at MWW/MX<0.8
        if mjet_veto and passesBoosted and jet_pruning and passesPPS[i] and DATA:    
            if pfcand_nextracks<5 and (recoMWW/M_RP)<0.8:
                h_xi_1_0_4_extratracks[i].Fill(xi["23"][0],pileupw*rw_extrk*rw_passPPS)
                h_xi_2_0_4_extratracks[i].Fill(xi["123"][0],pileupw*rw_extrk*rw_passPPS)
                h_MX_0_4_extratracks[i].Fill(M_RP,pileupw*rw_extrk*rw_passPPS)
                h_MWW_0_4_extratracks[i].Fill(recoMWW,pileupw*rw_extrk*rw_passPPS)
                h_Y_RP_0_4_extratracks[i].Fill(Rapidity_RP,pileupw*rw_extrk*rw_passPPS)
                h_Y_CMS_minus_RP_0_4_extratracks[i].Fill(recoYCMS-Rapidity_RP,pileupw*rw_extrk*rw_passPPS) 
                h_MWW_MX_0_4_tracks[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)
                h_tau21_0_4_tracks[i].Fill(tau21,pileupw)
                h_prunedMass_0_4_tracks[i].Fill(prunedMass,pileupw)
                if passYcut[i]:
                    h_MWW_MX_0_4_tracks_Ycut[i].Fill(recoMWW/M_RP,pileupw)

        if mjet_veto and passesBoosted and jet_pruning and failsAllPPS and passPPS2[i] and DATA:    
            if pfcand_nextracks<5:
                h_xi_1_0_4_extratracks_notPPS[i].Fill(xi["23"][0],pileupw*rw_extrk)
                h_xi_2_0_4_extratracks_notPPS[i].Fill(xi["123"][0],pileupw*rw_extrk)
                h_MX_0_4_extratracks_notPPS[i].Fill(M_RP,pileupw*rw_extrk)
                h_MWW_0_4_extratracks_notPPS[i].Fill(recoMWW,pileupw*rw_extrk)
                h_Y_RP_0_4_extratracks_notPPS[i].Fill(Rapidity_RP,pileupw*rw_extrk)
                h_Y_CMS_minus_RP_0_4_extratracks_notPPS[i].Fill(recoYCMS-Rapidity_RP,pileupw*rw_extrk)   
                h_MWW_MX_0_4_tracks_notPPS[i].Fill(recoMWW/M_RP,pileupw*rw_extrk)
                h_recoMWhad_0_4_tracks_notPPS[i].Fill(recoMWhad,pileupw*rw_extrk)
                h_tau21_0_4_tracks_notPPS[i].Fill(tau21,pileupw*rw_extrk)
                h_prunedMass_0_4_tracks_notPPS[i].Fill(prunedMass,pileupw*rw_extrk)
                if passYcut[i]:
                    h_MWW_MX_0_4_tracks_notPPS_Ycut[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)


        ###########################################################
        #Start of looking at control regions
        ###########################################################
        #Inverting the pruned mass cut to get MWW/MX distribution.
        if mjet_veto and passesBoosted and tau21<0.6 and prunedMass<50 and passesPPS[i]:    
            h_MWW_invertPrunedMass[i].Fill(recoMWW,pileupw*rw_extrk*rw_passPPS)
            if passYcut[i]:
                h_MWW_MX_invertPrunedMass_Ycut[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)



    #Looking large extra tracks passing PPS, this is conrol region for W+jets and ttbar
        if mjet_veto and passesBoosted and jet_pruning and passesPPS[i] and pfcand_nextracks<16 and pfcand_nextracks>4:
            h_xi_1_control[i].Fill(xi["23"][0],pileupw*rw_extrk*rw_passPPS)
            h_xi_2_control[i].Fill(xi["123"][0],pileupw*rw_extrk*rw_passPPS)
            h_Y_RP_control[i].Fill(M_RP,pileupw*rw_extrk*rw_passPPS)
            h_Y_CMS_minus_RP_control[i].Fill(recoYCMS-Rapidity_RP,pileupw*rw_extrk*rw_passPPS)
            h_MX_control[i].Fill(M_RP,pileupw*rw_extrk*rw_passPPS)
            h_MWW_control[i].Fill(recoMWW,pileupw*rw_extrk*rw_passPPS)
            h_MWW_MX_control[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)
            h_recoMWhad_control_control[i].Fill(recoMWhad,pileupw*rw_extrk*rw_passPPS)
            h_tau21_control_control[i].Fill(tau21,pileupw*rw_extrk*rw_passPPS)
            h_prunedMass_control_control[i].Fill(prunedMass,pileupw*rw_extrk*rw_passPPS)
            if passYcut[i]:
                h_MWW_MX_control_Ycut[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)

        if mjet_veto and passesBoosted and jet_pruning and passesPPS[i] and pfcand_nextracks>4:
            h_xi_1_5_up[i].Fill(xi["23"][0],pileupw*rw_extrk*rw_passPPS)
            h_xi_2_5_up[i].Fill(xi["123"][0],pileupw*rw_extrk*rw_passPPS)
            h_MX_5_up[i].Fill(M_RP,pileupw*rw_extrk*rw_passPPS)
            h_MWW_5_up[i].Fill(recoMWW,pileupw*rw_extrk*rw_passPPS)
            h_Y_RP_5_up[i].Fill(Rapidity_RP,pileupw*rw_extrk*rw_passPPS)
            h_Y_CMS_minus_RP_5_up[i].Fill(recoYCMS-Rapidity_RP,pileupw*rw_extrk*rw_passPPS)         
            h_MWW_MX_5_up[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)
            if passYcut[i]:
                h_MWW_MX_control_5_up_Ycut[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)

        if mjet_veto and tau21<0.6 and passesBoosted and prunedMass<50 and passesPPS[i] and pfcand_nextracks>4:
            h_MWW_MX_5_up_InvertPrunedMass[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)
            if passYcut[i]:
                h_MWW_MX_control_5_up_Ycut_InvertPrunedMass[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)

        if mjet_veto and tau21<0.6 and passesBoosted and prunedMass<50 and passesPPS[i] and pfcand_nextracks<5:
            h_MWW_MX_0_4_InvertPrunedMass[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)
            if passYcut[i]:
                h_MWW_MX_control_0_4_Ycut_InvertPrunedMass[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)


        if mjet_veto and passesBoosted and jet_pruning and failsAllPPS and passPPS2[i] and pfcand_nextracks>4 and DATA:
            h_MWW_MX_5_up_notPPS[i].Fill(recoMWW/M_RP,pileupw)
            if passYcut[i]:
                h_MWW_MX_5_up_Ycut_notPPS[i].Fill(recoMWW/M_RP,pileupw)


        if mjet_veto and passesBoosted and jet_pruning and failsAllPPS and passPPS2[i] and pfcand_nextracks<16 and pfcand_nextracks>4 and DATA:
            h_xi_1_control_notPPS[i].Fill(xi["23"][0],pileupw*rw_extrk*rw_failPPS)
            h_xi_2_control_notPPS[i].Fill(xi["123"][0],pileupw*rw_extrk*rw_failPPS)
            h_Y_RP_control_notPPS[i].Fill(M_RP,pileupw*rw_extrk*rw_failPPS)
            h_Y_CMS_minus_RP_control_notPPS[i].Fill(recoYCMS-Rapidity_RP,pileupw*rw_extrk*rw_failPPS)
            h_MX_control_notPPS[i].Fill(M_RP,pileupw*rw_extrk*rw_failPPS)
            h_MWW_control_notPPS[i].Fill(recoMWW,pileupw*rw_extrk*rw_failPPS)
            h_MWW_MX_control_notPPS[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_failPPS)
            h_recoMWhad_control_control_notPPS[i].Fill(recoMWhad,pileupw*rw_extrk*rw_failPPS)
            h_tau21_control_control_notPPS[i].Fill(tau21,pileupw*rw_extrk*rw_failPPS)
            h_prunedMass_control_control_notPPS[i].Fill(prunedMass,pileupw*rw_extrk*rw_failPPS)
            if passYcut[i]:
                h_MWW_MX_control_Ycut_notPPS[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_failPPS)

        #####################################################
        ##Additional plots that I don't look at very often
        #####################################################
        if mjet_veto and passesBoosted and jet_pruning and passesPPS[i] and pfcand_nextracks>14 and pfcand_nextracks<31:
            h_MWW_MX_control_15_30[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)
        if mjet_veto and passesBoosted and jet_pruning and passesPPS[i] and pfcand_nextracks>30 and pfcand_nextracks<51:
            h_MWW_MX_control_30_50[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)
        if mjet_veto and passesBoosted and jet_pruning and passesPPS[i] and pfcand_nextracks>50 and pfcand_nextracks<71:
            h_MWW_MX_control_50_70[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)
        if mjet_veto and passesBoosted and jet_pruning and passesPPS[i] and pfcand_nextracks>70 and pfcand_nextracks<101:
            h_MWW_MX_control_70_100[i].Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_passPPS)


fout.Write()
fout.Close()
print fout
print("--- %s seconds ---" % (time.time() - start_time))
#if batch:
#    os.listdir(".")
