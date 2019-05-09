#!/usr/bin/env python
#Finn Rebassoo, LLNL 12-2016-01
import os
from ROOT import *
import math as m
from htools import *
import sys
import time

if len(sys.argv) < 4:
    print "Need to specify 4 inputs parameters, i.e.:"
    print "  python histos_mue.py latest MuonEG crab_runBv3"
    print "  or"
    print "  python histos_mue.py specific MuonEG crab_runBv3/171116_215828/0001"
    sys.exit()

start_time = time.time()
sample_name=sys.argv[2]
print sample_name
file_dir=sys.argv[3]

DATA=False
ExclusiveMC=False
if sample_name == "SingleMuon":    DATA=True
if sample_name == "ExclusiveWW":   ExclusiveMC=True
print "ExclusiveMC", ExclusiveMC

#Get List Of Files
ListOfFiles=[]
returnedFiles=GetListOfFiles(sample_name,file_dir,DATA)
ListOfFiles=returnedFiles[0]
output_name=returnedFiles[1]
fout = TFile('histos/{0}.root'.format(output_name),'recreate')
fout.cd()


#Chain Together List Of Files
chain = TChain('demo/SlimmedNtuple')
AddFilesToChain(chain,ListOfFiles,DATA)

fout.cd()

print("--- %s seconds ---" % (time.time() - start_time))

h_gen_jetW=TH1F("h_gen_jetW",";;",40,0,2000)
h_reco_jetW=TH1F("h_reco_jetW",";;",40,0,2000)
h_reco_divide_gen_Wpt=TH1F("h_reco_divide_gen_Wpt",";;",40,0,2000)
h_reco_divide_gen_jet=TH2F("h_reco_divide_gen_jet",";;",40,0,2000,100,0,2)
h_gen_Wpt=TH1F("h_gen_Wpt",";gen W Leptonic Pt [GeV];",100,0,1000)
h_gen_Wpt_recopt200=TH1F("h_gen_Wpt_recopt200",";gen W Leptonic Pt [GeV];",100,0,1000)

h_muon_pt=TH1F("h_muon_pt",";p_{T} (#mu) [GeV];",100,0,1000)
h_muon_eta=TH1F("h_muon_eta",";#eta_{#mu};",60,-3,3)
h_muon_iso=TH1F("h_muon_iso",";pf-based isolation {#mu};",20,0,0.2)
h_jet_pt=TH1F("h_jet_pt",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_eta=TH1F("h_jet_eta",";#eta_{jet};",60,-3,3)
h_deltaR_lepton_jet=TH1F("h_deltaR_lepton_jet",";#deltaR(#mu,jet);",200,0,10)
h_deltaphi_jet_met=TH1F("h_deltaphi_jet_met",";#delta#Phi(MET,jet);",100,0,5)
h_deltaphi_jet_Wleptonic=TH1F("h_deltaphi_jet_Wleptonic",";#delta#Phi(MET,jet);",100,0,5)
h_tau21=TH1F("h_tau21",";tau21;",100,0,2)
h_prunedMass=TH1F("h_prunedMass",";prunedMass [GeV];",200,0,1000)
h_recoMWlep=TH1F("h_recoMWlep",";M_{W_{lep}} [GeV];",100,0,200)
h_recoMWhad=TH1F("h_recoMWhad",";M_{W_{had}} [GeV];",100,0,200)
h_dphiWW=TH1F("h_dphiWW",";dphiWW;",100,0,5)
h_WLeptonicPt=TH1F("h_WLeptonicPt",";W Leptonic Pt [GeV];",100,0,1000)
h_recoMWW=TH1F("h_recoMWW",";M_{WW} [GeV];",100,0,2000)
h_MET=TH1F("h_MET",";MET [GeV];",80,0,400)
h_pfcand_nextracks=TH1F("h_pfcand_nextracks",";Number of extra tracks;",100,-0.5,99.5)
h_num_vertices=TH1F("h_num_vertices",";Number of vertices;",100,-0.5,99.5)
h_num_vertices_preweight=TH1F("h_num_vertices_preweight",";Number of vertices;",100,-0.5,99.5)
h_num_jets_ak4=TH1F("h_num_jets_ak4",";Num extra jets (AK4);",10,-0.5,9.5)
h_num_bjets_ak4=TH1F("h_num_bjets_ak4",";Num extra b jets (AK4);",10,-0.5,9.5)
h_num_bjets_ak8=TH1F("h_num_bjets_ak8",";Num extra b jets (AK8);",10,-0.5,9.5)
h_num_jets_ak4_wbjet=TH1F("h_num_jets_ak4_wbjet",";Num extra jets in ttbar control regoin;",10,-0.5,9.5)


h_muon_pt_jetVeto=TH1F("h_muon_pt_jetVeto",";p_{T} (#mu) [GeV];",100,0,1000)
h_muon_eta_jetVeto=TH1F("h_muon_eta_jetVeto",";#eta_{#mu};",60,-3,3)
h_muon_iso_jetVeto=TH1F("h_muon_iso_jetVeto",";pf-based isolation {#mu};",20,0,0.2)
h_jet_pt_jetVeto=TH1F("h_jet_pt_jetVeto",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_eta_jetVeto=TH1F("h_jet_eta_jetVeto",";#eta_{jet};",60,-3,3)
h_jet_pt_jetVeto_Wplus=TH1F("h_jet_pt_jetVeto_Wplus",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_pt_jetVeto_Wminus=TH1F("h_jet_pt_jetVeto_Wminus",";p_{T} (jet) [GeV];",120,0,1200)
h_deltaR_lepton_jet_jetVeto=TH1F("h_deltaR_lepton_jet_jetVeto",";#deltaR(#mu,jet);",200,0,10)
h_deltaphi_jet_met_jetVeto=TH1F("h_deltaphi_jet_met_jetVeto",";#delta#Phi(MET,jet);",100,0,5)
h_tau21_jetVeto=TH1F("h_tau21_jetVeto",";tau21;",100,0,2)
h_prunedMass_jetVeto=TH1F("h_prunedMass_jetVeto",";prunedMass [GeV];",200,0,1000)
h_recoMWlep_jetVeto=TH1F("h_recoMWlep_jetVeto",";M_{W_{lep}} [GeV];",100,0,200)
h_recoMWhad_jetVeto=TH1F("h_recoMWhad_jetVeto",";M_{W_{had}} [GeV];",100,0,200)
h_dphiWW_jetVeto=TH1F("h_dphiWW_jetVeto",";dphiWW;",100,0,5)
h_WLeptonicPt_jetVeto=TH1F("h_WLeptonicPt_jetVeto",";W Leptonic Pt [GeV];",100,0,1000)
h_recoMWW_jetVeto=TH1F("h_recoMWW_jetVeto",";M_{WW} [GeV];",100,0,2000)
h_MET_jetVeto=TH1F("h_MET_jetVeto",";MET [GeV];",80,0,400)
h_pfcand_nextracks_jetVeto=TH1F("h_pfcand_nextracks_jetVeto",";Number of extra tracks;",100,-0.5,99.5)
h_num_vertices_jetVeto=TH1F("h_num_vertices_jetVeto",";Number of vertices;",100,-0.5,99.5)
h_num_vertices_preweight_jetVeto=TH1F("h_num_vertices_preweight_jetVeto",";Number of vertices;",100,-0.5,99.5)

h_recoMWhad_nojetVeto_WleptonicCuts=TH1F("h_recoMWhad_nojetVeto_WleptonicCuts",";M_{W_{had}} [GeV];",100,0,200)
h_prunedMass_nojetVeto_WleptonicCuts=TH1F("h_prunedMass_nojetVeto_WleptonicCuts",";prunedMass [GeV];",40,0,200)

h_muon_pt_jetVeto_WleptonicCuts=TH1F("h_muon_pt_jetVeto_WleptonicCuts",";p_{T} (#mu) [GeV];",100,0,1000)
h_muon_eta_jetVeto_WleptonicCuts=TH1F("h_muon_eta_jetVeto_WleptonicCuts",";#eta_{#mu};",60,-3,3)
h_jet_pt_jetVeto_WleptonicCuts=TH1F("h_jet_pt_jetVeto_WleptonicCuts",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_eta_jetVeto_WleptonicCuts=TH1F("h_jet_eta_jetVeto_WleptonicCuts",";#eta_{jet};",60,-3,3)
h_jet_pt_jetVeto_WleptonicCuts_Wplus=TH1F("h_jet_pt_jetVeto_WleptonicCuts_Wplus",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_pt_jetVeto_WleptonicCuts_Wminus=TH1F("h_jet_pt_jetVeto_WleptonicCuts_Wminus",";p_{T} (jet) [GeV];",120,0,1200)
h_tau21_jetVeto_WleptonicCuts=TH1F("h_tau21_jetVeto_WleptonicCuts",";tau21;",100,0,2)
h_prunedMass_jetVeto_WleptonicCuts=TH1F("h_prunedMass_jetVeto_WleptonicCuts",";prunedMass [GeV];",200,0,1000)
h_recoMWlep_jetVeto_WleptonicCuts=TH1F("h_recoMWlep_jetVeto_WleptonicCuts",";M_{W_{lep}} [GeV];",100,0,200)
h_recoMWhad_jetVeto_WleptonicCuts=TH1F("h_recoMWhad_jetVeto_WleptonicCuts",";M_{W_{had}} [GeV];",100,0,200)
h_dphiWW_jetVeto_WleptonicCuts=TH1F("h_dphiWW_jetVeto_WleptonicCuts",";dphiWW;",100,0,5)
h_WLeptonicPt_jetVeto_WleptonicCuts=TH1F("h_WLeptonicPt_jetVeto_WleptonicCuts",";W Leptonic Pt [GeV];",100,0,1000)
h_recoMWW_jetVeto_WleptonicCuts=TH1F("h_recoMWW_jetVeto_WleptonicCuts",";M_{WW} [GeV];",100,0,2000)
h_MET_jetVeto_WleptonicCuts=TH1F("h_MET_jetVeto_WleptonicCuts",";MET [GeV];",80,0,400)
h_pfcand_nextracks_jetVeto_WleptonicCuts=TH1F("h_pfcand_nextracks_jetVeto_WleptonicCuts",";Number of extra tracks;",100,-0.5,99.5)
h_num_vertices_jetVeto_WleptonicCuts=TH1F("h_num_vertices_jetVeto_WleptonicCuts",";Number of vertices;",100,-0.5,99.5)
h_num_vertices_preweight_jetVeto_WleptonicCuts=TH1F("h_num_vertices_preweight_jetVeto_WleptonicCuts",";Number of vertices;",100,-0.5,99.5)

h_muon_pt_MjetVeto_WleptonicCuts=TH1F("h_muon_pt_MjetVeto_WleptonicCuts",";p_{T} (#mu) [GeV];",100,0,1000)
h_muon_eta_MjetVeto_WleptonicCuts=TH1F("h_muon_eta_MjetVeto_WleptonicCuts",";#eta_{#mu};",60,-3,3)
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

h_muon_pt_jetpruned=TH1F("h_muon_pt_jetpruned",";p_{T} (#mu) [GeV];",100,0,1000)
h_muon_eta_jetpruned=TH1F("h_muon_eta_jetpruned",";#eta_{#mu};",60,-3,3)
h_jet_pt_jetpruned=TH1F("h_jet_pt_jetpruned",";p_{T} (#mu) [GeV];",120,0,1200)
h_jet_eta_jetpruned=TH1F("h_jet_eta_jetpruned",";#eta_{#mu};",60,-3,3)
#h_tau21_jetpruned=TH1F("h_tau21_jetpruned",";tau21;",100,0,2)
#h_prunedMass_jetpruned=TH1F("h_prunedMass_jetpruned",";prunedMass [GeV];",200,0,1000)
h_recoMWlep_jetpruned=TH1F("h_recoMWlep_jetpruned",";M_{W_{lep}} [GeV];",100,0,200)
h_recoMWhad_jetpruned=TH1F("h_recoMWhad_jetpruned",";M_{W_{had}} [GeV];",100,0,200)
h_dphiWW_jetpruned=TH1F("h_dphiWW_jetpruned",";dphiWW;",100,0,5)
h_WLeptonicPt_jetpruned=TH1F("h_WLeptonicPt_jetpruned",";W Leptonic Pt [GeV];",100,0,1000)
h_recoMWW_jetpruned=TH1F("h_recoMWW_jetpruned",";M_{WW} [GeV];",100,0,2000)
h_MET_jetpruned=TH1F("h_MET_jetpruned",";MET [GeV];",80,0,400)
h_pfcand_nextracks_jetpruned=TH1F("h_pfcand_nextracks_jetpruned",";Number of extra tracks;",100,-0.5,99.5)
h_num_jets_ak4_jetpruned=TH1F("h_num_jets_ak4_jetpruned",";Num extra jets (AK4);",10,-0.5,9.5)
h_num_bjets_ak4_jetpruned=TH1F("h_num_bjets_ak4_jetpruned",";Num extra b jets (AK4);",10,-0.5,9.5)
h_num_bjets_ak8_jetpruned=TH1F("h_num_bjets_ak8_jetpruned",";Num extra b jets (AK8);",10,-0.5,9.5)

h_muon_pt_veryBoosted_noExtraJets=TH1F("h_muon_pt_veryBoosted_noExtraJets",";p_{T} (#mu) [GeV];",100,0,1000)
h_muon_eta_veryBoosted_noExtraJets=TH1F("h_muon_eta_veryBoosted_noExtraJets",";#eta_{#mu};",60,-3,3)
h_jet_pt_veryBoosted_noExtraJets=TH1F("h_jet_pt_veryBoosted_noExtraJets",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_eta_veryBoosted_noExtraJets=TH1F("h_jet_eta_veryBoosted_noExtraJets",";#eta_{jet};",60,-3,3)
h_jet_pt_veryBoosted_noExtraJets_Wplus=TH1F("h_jet_pt_veryBoosted_noExtraJets_Wplus",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_pt_veryBoosted_noExtraJets_Wminus=TH1F("h_jet_pt_veryBoosted_noExtraJets_Wminus",";p_{T} (jet) [GeV];",120,0,1200)
h_tau21_veryBoosted_noExtraJets=TH1F("h_tau21_veryBoosted_noExtraJets",";tau21;",100,0,2)
h_prunedMass_veryBoosted_noExtraJets=TH1F("h_prunedMass_veryBoosted_noExtraJets",";prunedMass [GeV];",200,0,1000)
h_recoMWlep_veryBoosted_noExtraJets=TH1F("h_recoMWlep_veryBoosted_noExtraJets",";M_{W_{lep}} [GeV];",100,0,200)
h_recoMWhad_veryBoosted_noExtraJets=TH1F("h_recoMWhad_veryBoosted_noExtraJets",";M_{W_{had}} [GeV];",100,0,200)
h_dphiWW_veryBoosted_noExtraJets=TH1F("h_dphiWW_veryBoosted_noExtraJets",";dphiWW;",100,0,5)
h_WLeptonicPt_veryBoosted_noExtraJets=TH1F("h_WLeptonicPt_veryBoosted_noExtraJets",";W Leptonic Pt [GeV];",100,0,1000)
h_recoMWW_veryBoosted_noExtraJets=TH1F("h_recoMWW_veryBoosted_noExtraJets",";M_{WW} [GeV];",100,0,2000)
h_MET_veryBoosted_noExtraJets=TH1F("h_MET_veryBoosted_noExtraJets",";MET [GeV];",80,0,400)
h_pfcand_nextracks_veryBoosted_noExtraJets=TH1F("h_pfcand_nextracks_veryBoosted_noExtraJets",";Number of extra tracks;",100,-0.5,99.5)
h_num_vertices_veryBoosted_noExtraJets=TH1F("h_num_vertices_veryBoosted_noExtraJets",";Number of vertices;",100,-0.5,99.5)
h_num_vertices_preweight_veryBoosted_noExtraJets=TH1F("h_num_vertices_preweight_veryBoosted_noExtraJets",";Number of vertices;",100,-0.5,99.5)

h_muon_pt_veryBoosted_MjetVeto=TH1F("h_muon_pt_veryBoosted_MjetVeto",";p_{T} (#mu) [GeV];",100,0,1000)
h_muon_eta_veryBoosted_MjetVeto=TH1F("h_muon_eta_veryBoosted_MjetVeto",";#eta_{#mu};",60,-3,3)
h_jet_pt_veryBoosted_MjetVeto=TH1F("h_jet_pt_veryBoosted_MjetVeto",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_eta_veryBoosted_MjetVeto=TH1F("h_jet_eta_veryBoosted_MjetVeto",";#eta_{jet};",60,-3,3)
h_jet_pt_veryBoosted_MjetVeto_Wplus=TH1F("h_jet_pt_veryBoosted_MjetVeto_Wplus",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_pt_veryBoosted_MjetVeto_Wminus=TH1F("h_jet_pt_veryBoosted_MjetVeto_Wminus",";p_{T} (jet) [GeV];",120,0,1200)
h_tau21_veryBoosted_MjetVeto=TH1F("h_tau21_veryBoosted_MjetVeto",";tau21;",100,0,2)
h_prunedMass_veryBoosted_MjetVeto=TH1F("h_prunedMass_veryBoosted_MjetVeto",";prunedMass [GeV];",200,0,1000)
h_recoMWlep_veryBoosted_MjetVeto=TH1F("h_recoMWlep_veryBoosted_MjetVeto",";M_{W_{lep}} [GeV];",100,0,200)
h_recoMWhad_veryBoosted_MjetVeto=TH1F("h_recoMWhad_veryBoosted_MjetVeto",";M_{W_{had}} [GeV];",100,0,200)
h_dphiWW_veryBoosted_MjetVeto=TH1F("h_dphiWW_veryBoosted_MjetVeto",";dphiWW;",100,0,5)
h_WLeptonicPt_veryBoosted_MjetVeto=TH1F("h_WLeptonicPt_veryBoosted_MjetVeto",";W Leptonic Pt [GeV];",100,0,1000)
h_recoMWW_veryBoosted_MjetVeto=TH1F("h_recoMWW_veryBoosted_MjetVeto",";M_{WW} [GeV];",100,0,2000)
h_MET_veryBoosted_MjetVeto=TH1F("h_MET_veryBoosted_MjetVeto",";MET [GeV];",80,0,400)
h_pfcand_nextracks_veryBoosted_MjetVeto=TH1F("h_pfcand_nextracks_veryBoosted_MjetVeto",";Number of extra tracks;",100,-0.5,99.5)
h_num_vertices_veryBoosted_MjetVeto=TH1F("h_num_vertices_veryBoosted_MjetVeto",";Number of vertices;",100,-0.5,99.5)
h_num_vertices_preweight_veryBoosted_MjetVeto=TH1F("h_num_vertices_preweight_veryBoosted_MjetVeto",";Number of vertices;",100,-0.5,99.5)

h_dphiWW_after_jetVeto=TH1F("h_dphiWW_after_jetVeto",";dphiWW;",100,0,5)
h_pfcand_nextracks_after_jetVeto=TH1F("h_pfcand_nextracks_after_jetVeto",";Number of extra tracks;",100,-0.5,99.5)
h_recoMWW_afterDphi=TH1F("h_recoMWW_afterDphi",";M_{WW} [GeV];",100,0,2000)
h_recoMWhad_afterMWW=TH1F("h_recoMWhad_afterMWW",";M_{W_{had}} [GeV];",100,0,200)
h_MET_afterMWhad=TH1F("h_MET_afterMWhad",";MET [GeV];",80,0,400)
h_WLeptonicPt_afterMET=TH1F("h_WLeptonicPt_afterMET",";W Leptonic Pt [GeV];",100,0,1000)
h_jet_pt_afterMET=TH1F("h_jet_pt_afterMET",";Jet Pt [GeV];",120,0,1200)
h_pfcand_nextracks_afterWLeptonicPt=TH1F("h_pfcand_nextracks_afterWLeptonicPt",";Number of extra tracks;",100,-0.5,99.5)
#h_pfcand_nextracks_afterWLeptonicPt=TH1F("h_pfcand_nextracks_afterWLeptonicPt",";Number of extra tracks;",20,-0.5,99.5)
h_pfcand_nextracks_afterWLeptonicPt_0_20_vertices=TH1F("h_pfcand_nextracks_afterWLeptonicPt_0_20_vertices",";Number of extra tracks;",100,-0.5,99.5)
h_pfcand_nextracks_afterWLeptonicPt_20_35_vertices=TH1F("h_pfcand_nextracks_afterWLeptonicPt_20_35_vertices",";Number of extra tracks;",100,-0.5,99.5)
h_pfcand_nextracks_afterWLeptonicPt_35_up_vertices=TH1F("h_pfcand_nextracks_afterWLeptonicPt_35_up_vertices",";Number of extra tracks;",100,-0.5,99.5)
h_num_vertices_pfcand_nextracks_afterWLeptonicPt=TH1F("h_num_vertices_pfcand_nextracks_afterWLeptonicPt",";Number of vertices;",100,-0.5,99.5)

h_xi_1_0_4_extratracks=TH1F("h_xi_1_0_4_extratracks",";#xi_{1};",128,0,0.32)
h_xi_2_0_4_extratracks=TH1F("h_xi_2_0_4_extratracks",";#xi_{2};",128,0,0.32)
h_Y_RP_0_4_extratracks=TH1F("h_Y_RP_0_4_extratracks",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_0_4_extratracks=TH1F("h_Y_CMS_minus_RP_0_4_extratracks",";Y RP;",60,-3,3)
h_MX_0_4_extratracks=TH1F("h_MX_0_4_extratracks",";Mass RP [GeV];",100,0,3000)
h_MWW_MX_0_4_tracks=TH1F("h_MWW_MX_0_4_tracks",";MWW/MX;",100,0,2)
h_recoMWhad_0_4_tracks=TH1F("h_recoMWhad_0_4_tracks",";M_{W_{had}} [GeV];",100,0,200)
h_tau21_0_4_tracks=TH1F("h_tau21_0_4_tracks",";tau21;",100,0,2)
h_prunedMass_0_4_tracks=TH1F("h_prunedMass_0_4_tracks",";prunedMass [GeV];",200,0,1000)
h_MWW_MX_0_4_tracks_Ycut=TH1F("h_MWW_MX_0_4_tracks_Ycut",";MWW/MX;",100,0,2)

h_xi_1_0_4_extratracks_Mhad=TH1F("h_xi_1_0_4_extratracks_Mhad",";#xi_{1};",128,0,0.32)
h_xi_2_0_4_extratracks_Mhad=TH1F("h_xi_2_0_4_extratracks_Mhad",";#xi_{2};",128,0,0.32)
h_Y_RP_0_4_extratracks_Mhad=TH1F("h_Y_RP_0_4_extratracks_Mhad",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_0_4_extratracks_Mhad=TH1F("h_Y_CMS_minus_RP_0_4_extratracks_Mhad",";Y RP;",60,-3,3)
h_MX_0_4_extratracks_Mhad=TH1F("h_MX_0_4_extratracks_Mhad",";Mass RP [GeV];",100,0,3000)
h_MWW_MX_0_4_tracks_Mhad=TH1F("h_MWW_MX_0_4_tracks_Mhad",";MWW/MX;",100,0,2)
h_MWW_MX_0_4_tracks_Mhad_Ycut=TH1F("h_MWW_MX_0_4_tracks_Mhad_Ycut",";MWW/MX;",100,0,2)

h_pfcand_nextracks_after_jet_veto_jet_pruning_PPS=TH1F("h_pfcand_nextracks_after_jet_veto_jet_pruning_PPS",";Number of extra tracks;",100,-0.5,99.5)
h_pfcand_nextracks_after_jet_veto_jet_pruning_veto_signal_PPS=TH1F("h_pfcand_nextracks_after_jet_veto_jet_pruning_veto_signal_PPS",";Number of extra tracks;",100,-0.5,99.5)

h_xi_1_10_up=TH1F("h_xi_1_10_up",";#xi_{1};",128,0,0.32)
h_xi_2_10_up=TH1F("h_xi_2_10_up",";#xi_{2};",128,0,0.32)
h_Y_RP_10_up=TH1F("h_Y_RP_10_up",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_10_up=TH1F("h_Y_CMS_minus_RP_10_up",";Y RP;",60,-3,3)
h_MX_10_up=TH1F("h_MX_10_up",";Mass RP [GeV];",100,0,3000)
h_MWW_MX_10_up=TH1F("h_MWW_MX_10_up",";MWW/MX;",100,0,2)
#h_MWW_minus_MX_10_up=TH1F("h_MWW_minus_MX",";MWW - MX;",1000,-1000,200)
h_recoMWhad_control_10_up=TH1F("h_recoMWhad_control_10_up",";M_{W_{had}} [GeV];",100,0,200)
h_tau21_control_10_up=TH1F("h_tau21_control_10_up",";tau21;",100,0,2)
h_prunedMass_control_10_up=TH1F("h_prunedMass_control_10_up",";prunedMass [GeV];",200,0,1000)


h_MWW_MX_0_4_tracks_Data_Mwhad_0_50=TH1F("h_MWW_MX_0_4_tracks_Data_Mwhad_0_50",";MWW/MX;",100,0,2)
h_MWW_MX_0_9_tracks_Data_Mwhad_0_50=TH1F("h_MWW_MX_0_9_tracks_Data_Mwhad_0_50",";MWW/MX;",100,0,2)
h_MWW_MX_10_up_tracks_Data_Mwhad_0_50=TH1F("h_MWW_MX_10_up_tracks_Data_Mwhad_0_50",";MWW/MX;",100,0,2)
h_MWW_MX_Data_Mwhad_0_50=TH1F("h_MWW_MX_Data_Mwhad_0_50",";MWW/MX;",100,0,2)

h_Y_CMS_minus_RP_0_4_extratracks_Data_Mwhad_0_50=TH1F("h_Y_CMS_minus_RP_0_4_extratracks_Data_Mwhad_0_50",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_0_9_extratracks_Data_Mwhad_0_50=TH1F("h_Y_CMS_minus_RP_0_9_extratracks_Data_Mwhad_0_50",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_10_up_extratracks_Data_Mwhad_0_50=TH1F("h_Y_CMS_minus_RP_10_up_extratracks_Data_Mwhad_0_50",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_Data_Mwhad_0_50=TH1F("h_Y_CMS_minus_RP_Data_Mwhad_0_50",";Y RP;",60,-3,3)

h_MWW_MX_0_4_tracks_Data_Mwhad_50_up_b=TH1F("h_MWW_MX_0_4_tracks_Data_Mwhad_50_up_b",";MWW/MX;",100,0,2)
h_MWW_MX_0_19_tracks_Data_Mwhad_50_up_b=TH1F("h_MWW_MX_0_19_tracks_Data_Mwhad_50_up_b",";MWW/MX;",100,0,2)
h_MWW_MX_20_up_tracks_Data_Mwhad_50_up_b=TH1F("h_MWW_MX_20_up_tracks_Data_Mwhad_50_up_b",";MWW/MX;",100,0,2)
h_MWW_MX_Data_Mwhad_50_up_b=TH1F("h_MWW_MX_Data_Mwhad_50_up_b",";MWW/MX;",100,0,2)

h_Y_CMS_minus_RP_0_4_extratracks_Data_Mwhad_50_up_b=TH1F("h_Y_CMS_minus_RP_0_4_extratracks_Data_Mwhad_50_up_b",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_0_19_extratracks_Data_Mwhad_50_up_b=TH1F("h_Y_CMS_minus_RP_0_19_extratracks_Data_Mwhad_50_up_b",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_20_up_extratracks_Data_Mwhad_50_up_b=TH1F("h_Y_CMS_minus_RP_20_up_extratracks_Data_Mwhad_50_up_b",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_Data_Mwhad_50_up_b=TH1F("h_Y_CMS_minus_RP_Data_Mwhad_50_up_b",";Y RP;",60,-3,3)


h_xi_1_0_9_extratracks=TH1F("h_xi_1_0_9_extratracks",";#xi_{1};",128,0,0.32)
h_xi_2_0_9_extratracks=TH1F("h_xi_2_0_9_extratracks",";#xi_{2};",128,0,0.32)
h_Y_RP_0_9_extratracks=TH1F("h_Y_RP_0_9_extratracks",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_0_9_extratracks=TH1F("h_Y_CMS_minus_RP_0_9_extratracks",";Y RP;",60,-3,3)
h_MX_0_9_extratracks=TH1F("h_MX_0_9_extratracks",";Mass RP [GeV];",100,0,3000)
h_MWW_MX_0_9_extratracks=TH1F("h_MWW_MX_0_9_extratracks",";MWW/MX;",100,0,2)

h_num_extra_tracks_0jets=TH1F("h_num_extra_tracks_0jets",";Number of extra tracks;",100,-0.5,99.5)
h_num_extra_tracks_0jets_boosted=TH1F("h_num_extra_tracks_0jets_boosted",";Number of extra tracks;",100,-0.5,99.5)
h_num_extra_tracks_1plusjets=TH1F("h_num_extra_tracks_1plusjets",";Number of extra tracks;",100,-0.5,99.5)

h_num_extra_tracks_1plusjets_boosted=TH1F("h_num_extra_tracks_1plusjets_boosted",";Number of extra tracks;",100,-0.5,99.5)
h_num_extra_tracks_1plusjets_nobjets=TH1F("h_num_extra_tracks_1plusjets_nobjets",";Number of extra tracks;",100,-0.5,99.5)
h_num_extra_tracks_1plusjets_nobjets_boosted=TH1F("h_num_extra_tracks_1plusjets_nobjets_boosted",";Number of extra tracks;",100,-0.5,99.5)
h_num_extra_tracks_nobjets=TH1F("h_num_extra_tracks_nobjets",";Number of extra tracks;",100,-0.5,99.5)
h_num_extra_tracks_nobjets_boosted=TH1F("h_num_extra_tracks_nobjets_boosted",";Number of extra tracks;",100,-0.5,99.5)

h_recoMWhad_ttbar_centralControlRegion=TH1F("h_recoMWhad_ttbar_centralControlRegion",";M_{W_{had}} [GeV];",100,0,200)
h_recoMWW_ttbar_centralControlRegion=TH1F("h_recoMWW_ttbar_centralControlRegion",";M_{WW} [GeV];",100,0,2000)
h_recoMWW_ttbar_centralControlRegion_0_5=TH1F("h_recoMWW_ttbar_centralControlRegion_0_5",";M_{WW} [GeV];",100,0,2000)
h_recoMWW_ttbar_centralControlRegion_0_9=TH1F("h_recoMWW_ttbar_centralControlRegion_0_9",";M_{WW} [GeV];",100,0,2000)
h_recoMWW_ttbar_centralControlRegion_10_up=TH1F("h_recoMWW_ttbar_centralControlRegion_10_up",";M_{WW} [GeV];",100,0,2000)
h_recoMWhad_ttbar_centralControlRegion_PPS=TH1F("h_recoMWhad_ttbar_centralControlRegion_PPS",";M_{W_{had}} [GeV];",100,0,200)
h_recoMWhad_nominal=TH1F("h_recoMWhad_nominal",";M_{W_{had}} [GeV];",100,0,200)

h_recoMWhad_Wjets_centralControlRegion=TH1F("h_recoMWhad_Wjets_centralControlRegion",";M_{W_{had}} [GeV];",100,0,200)
h_recoMWW_Wjets_centralControlRegion=TH1F("h_recoMWW_Wjets_centralControlRegion",";M_{WW} [GeV];",100,0,2000)
h_recoMWW_Wjets_centralControlRegion_0_5=TH1F("h_recoMWW_Wjets_centralControlRegion_0_5",";M_{WW} [GeV];",100,0,2000)
h_recoMWW_Wjets_centralControlRegion_0_9=TH1F("h_recoMWW_Wjets_centralControlRegion_0_9",";M_{WW} [GeV];",100,0,2000)
h_recoMWW_Wjets_centralControlRegion_10_up=TH1F("h_recoMWW_Wjets_centralControlRegion_10_up",";M_{WW} [GeV];",100,0,2000)
h_recoMWW_Wjets_centralControlRegion_10_up_Mwhad=TH1F("h_recoMWW_Wjets_centralControlRegion_10_up_Mwhad",";M_{WW} [GeV];",100,0,2000)

h_recoMWW_Wjets_centralControlRegion_0_5_Mwhad_noPPS=TH1F("h_recoMWW_Wjets_centralControlRegion_0_5_Mwhad_noPPS",";M_{WW} [GeV];",100,0,2000)
h_recoMWW_Wjets_centralControlRegion_0_9_Mwhad_noPPS=TH1F("h_recoMWW_Wjets_centralControlRegion_0_9_Mwhad_noPPS",";M_{WW} [GeV];",100,0,2000)
h_recoMWW_Wjets_centralControlRegion_10_up_Mwhad_noPPS=TH1F("h_recoMWW_Wjets_centralControlRegion_10_up_Mwhad_noPPS",";M_{WW} [GeV];",100,0,2000)

h_num_extra_tracks_nominal=TH1F("h_num_extra_tracks_nominal",";Number of extra tracks;",100,-0.5,99.5)
#h_num_extra_tracks_PPS=TH1F("h_num_extra_tracks_PPS",";Number of extra tracks;",100,-0.5,99.5)
h_num_extra_tracks_PPS=TH1F("h_num_extra_tracks_PPS",";Number of extra tracks;",20,-0.5,99.5)
h_num_extra_tracks_PPS_reweight_extra_tracks=TH1F("h_num_extra_tracks_PPS_reweight_extra_tracks",";Number of extra tracks;",20,-0.5,99.5)
#h_num_extra_tracks_notPPS=TH1F("h_num_extra_tracks_notPPS",";Number of extra tracks;",100,-0.5,99.5)
h_num_extra_tracks_notPPS=TH1F("h_num_extra_tracks_notPPS",";Number of extra tracks;",20,-0.5,99.5)
h_num_extra_tracks_notPPS_reweight_extra_tracks=TH1F("h_num_extra_tracks_notPPS_reweight_extra_tracks",";Number of extra tracks;",20,-0.5,99.5)
h_num_extra_tracks_PPS_noDRl=TH1F("h_num_extra_tracks_PPS_noDRl",";Number of extra tracks;",20,-0.5,99.5)
h_num_extra_tracks_notPPS_noDRl=TH1F("h_num_extra_tracks_notPPS_noDRl",";Number of extra tracks;",20,-0.5,99.5)

h_num_extra_tracks_notPPS_recoMWW900=TH1F("h_num_extra_tracks_notPPS_recoMWW900",";Number of extra tracks;",20,-0.5,99.5)
h_num_extra_tracks_notPPS_reweight_extra_tracks_recoMWW900=TH1F("h_num_extra_tracks_notPPS_reweight_extra_tracks_recoMWW900",";Number of extra tracks;",20,-0.5,99.5)


h_mass_cms_vs_rp=TH2F("h_mass_cms_vs_rp","M_{CMS} [GeV]; M_{RP} [GeV];",2500,0,2500,2500,0,2500)
h_mass_cms_vs_rp_WjetsControlRegion=TH2F("h_mass_cms_vs_rp_WjetsControlRegion","M_{CMS} [GeV]; M_{RP} [GeV];",2500,0,2500,2500,0,2500)
h_mass_cms_vs_rp_TTbarControlRegion=TH2F("h_mass_cms_vs_rp_TTbarControlRegion","M_{CMS} [GeV]; M_{RP} [GeV];",2500,0,2500,2500,0,2500)
h_tau21_vs_prunedMass=TH2F("h_tau21_vs_prunedMass","tau21;prunedMass [GeV];",200,0,1000,100,0,2)

#Plots to see if jet veto even matters after extra tracks cut
h_num_jets_not_PPS_0_4_extra_tracks=TH1F("h_num_jets_not_PPS_0_4_extra_tracks",";Num extra jets (AK4);",10,-0.5,9.5)
h_recoMWhad_not_PPS_0_4_extra_tracks=TH1F("h_recoMWhad_not_PPS_0_4_extra_tracks",";M_{W_{had}} [GeV];",100,0,200)
h_num_jets_not_PPS_0_4_extra_tracks_recoMWhad=TH1F("h_num_jets_not_PPS_0_4_extra_tracks_recoMWhad",";Num extra jets (AK4);",10,-0.5,9.5)

h_num_jets_not_PPS_0_4_extra_tracks_noDRl=TH1F("h_num_jets_not_PPS_0_4_extra_tracks_noDRl",";Num extra jets (AK4);",10,-0.5,9.5)
h_recoMWhad_not_PPS_0_4_extra_tracks_noDRl=TH1F("h_recoMWhad_not_PPS_0_4_extra_tracks_noDRl",";M_{W_{had}} [GeV];",100,0,200)
h_num_jets_not_PPS_0_4_extra_tracks_recoMWhad_noDRl=TH1F("h_num_jets_not_PPS_0_4_extra_tracks_recoMWhad_noDRl",";Num extra jets (AK4);",10,-0.5,9.5)

h_num_jets_ttbar=TH1F("h_num_jets_ttbar",";Num extra jets (AK4);",10,-0.5,9.5)
h_num_jets_ttbar_0_4_extra_tracks=TH1F("h_num_jets_ttbar_0_4_extra_tracks",";Num extra jets (AK4);",10,-0.5,9.5)
h_recoMWhad_ttbar_0_4_extra_tracks=TH1F("h_recoMWhad_ttbar_0_4_extra_tracks",";M_{W_{had}} [GeV];",100,0,200)
h_num_jets_ttbar_0_4_extra_tracks_recoMWhad=TH1F("h_num_jets_ttbar_0_4_extra_tracks_recoMWhad",";Num extra jets (AK4);",10,-0.5,9.5)

h_num_jets_ttbar_0_4_extra_tracks_noDRl=TH1F("h_num_jets_ttbar_0_4_extra_tracks_noDRl",";Num extra jets (AK4);",10,-0.5,9.5)
h_recoMWhad_ttbar_0_4_extra_tracks_noDRl=TH1F("h_recoMWhad_ttbar_0_4_extra_tracks_noDRl",";M_{W_{had}} [GeV];",100,0,200)
h_num_jets_ttbar_0_4_extra_tracks_recoMWhad_noDRl=TH1F("h_num_jets_ttbar_0_4_extra_tracks_recoMWhad_noDRl",";Num extra jets (AK4);",10,-0.5,9.5)

h_pfcand_nextracks_controlRegion=TH1F("h_pfcand_nextracks_controlRegion",";Number of extra tracks;",100,-0.5,99.5)

#Plots to check gen xi distribution between different aqgc samples
h_gen_proton_xi_pos=TH1F("h_gen_proton_xi_pos",";Xi;",128,0,0.32)
h_gen_proton_xi_neg=TH1F("h_gen_proton_xi_neg",";Xi;",128,0,0.32)

h_gen_proton_xi_pos_PPS=TH1F("h_gen_proton_xi_pos_PPS",";Xi;",128,0,0.32)
h_gen_proton_xi_neg_PPS=TH1F("h_gen_proton_xi_neg_PPS",";Xi;",128,0,0.32)

h_extra_tracks_vs_vertices=TH2F("h_extra_tracks_vs_vertices",";;",100,0,100,100,0,100)
h_extra_tracks_vs_vertices_boosted=TH2F("h_extra_tracks_vs_vertices_boosted",";;",100,0,100,100,0,100)

h_extra_tracks_vs_MWW_notPPS=TH2F("h_extra_tracks_vs_MWW_notPPS",";;",100,0,2000,100,-0.5,99.5)
h_extra_tracks_vs_MWW_PPS=TH2F("h_extra_tracks_vs_MWW_PPS",";;",100,0,2000,100,-0.5,99.5)
h_extra_tracks_vs_MX_PPS=TH2F("h_extra_tracks_vs_MX_PPS",";;",100,0,2000,100,-0.5,99.5)

h_MWW_extra_tracks_notPPS=TH1F("h_MWW_extra_tracks_notPPS",";;",100,0,2000)
h_MWW_extra_tracks_0_4_notPPS=TH1F("h_MWW_extra_tracks_0_4_notPPS",";;",100,0,2000)
h_MWW_extra_tracks_0_9_notPPS=TH1F("h_MWW_extra_tracks_0_9_notPPS",";;",100,0,2000)
h_MWW_extra_tracks_9_up_notPPS=TH1F("h_MWW_extra_tracks_9_up_notPPS",";;",100,0,2000)

h_MWW_900_extra_tracks_0_4_notPPS=TH1F("h_MWW_900_extra_tracks_0_4_notPPS",";;",100,0,2000)
h_MWW_900_extra_tracks_5_15_notPPS=TH1F("h_MWW_900_extra_tracks_5_15_notPPS",";;",100,0,2000)
h_MWW_900_extra_tracks_5_up_notPPS=TH1F("h_MWW_900_extra_tracks_5_up_notPPS",";;",100,0,2000)
h_MWW_MX_5_15_recoMWW900=TH1F("h_MWW_MX_5_15_recoMWW900",";MWW/MX;",100,0,2)
h_MWW_MX_5_up_recoMWW900=TH1F("h_MWW_MX_5_up_recoMWW900",";MWW/MX;",100,0,2)
h_Y_CMS_minus_RP_5_up_recoMWW=TH1F("h_Y_CMS_minus_RP_10_up_recoMWW",";Y RP;",60,-3,3)
h_MWW_MX_5_up_recoMWW900_Ycut=TH1F("h_MWW_MX_5_up_recoMWW900_Ycut",";MWW/MX;",100,0,2)
#h_MWW_MX_10_up_recoMWW900_Ycut=TH1F("h_MWW_MX_10_up_recoMWW900_Ycut",";MWW/MX;",100,0,2)
h_MWW_MX_0_4_tracks_recoMWW900=TH1F("h_MWW_MX_0_4_tracks_recoMWW900",";MWW/MX;",100,0,2)

h_MWW_MX_9_up_extratracks_dY_l0p6=TH1F("h_MWW_MX_9_up_extratracks_dY_l0p6",";MWW/MX;",100,0,2)
h_MWW_MX_9_up_extratracks_dY_g0p6=TH1F("h_MWW_MX_9_up_extratracks_dY_g0p6",";MWW/MX;",100,0,2)

ratio=[1.59918951988,1.68628513813,1.73210585117,1.69695830345,1.60702228546,1.55586051941,1.40359997749,1.24094235897,1.06528007984,0.911292850971,0.805232226849,0.690045535564,0.588334977627,0.506649911404,0.442807376385,0.419169098139,0.373487889767,0.327817767859,0.318366676569,0.320016086102]

Run=0.
event=0.
print chain.GetEntries()
it=0
for e in chain:
    it=it+1
    run=e.run
    event=e.event
    lumi=e.lumiblock
    pileupw=e.pileupWeight

    jet_veto=False
    mjet_veto=False
    #Look at events passing preselection and jet veto
    if e.num_jets_ak4<1 and e.num_bjets_ak8 < 1:
        jet_veto=True
    if e.num_bjets_ak4<1:
        mjet_veto=True
    ##########################################
    #Gen Plots
    ##########################################
    #This is to look at gen pt vs. reco pt for jet as a function of gen jet pt
    count_gen=0
    for gen_jet_pt in e.gen_jet_pt:
        dphi_gen_reco=GetDphi(e.gen_jet_phi[count_gen],e.jet_phi[0])
        deta_gen_reco=e.gen_jet_eta[count_gen]-e.jet_eta[0]
        deltaR=m.sqrt(dphi_gen_reco*dphi_gen_reco+deta_gen_reco*deta_gen_reco   )
        if deltaR < 0.4:
            h_gen_jetW.Fill(gen_jet_pt)
            h_reco_jetW.Fill(e.jet_pt[0])
            h_reco_divide_gen_jet.Fill(gen_jet_pt,e.jet_pt[0]/gen_jet_pt)
        count_gen=count_gen+1

    #This is to look at gen proton xi
    ita=0
    for gen_proton_pz in e.gen_proton_pz:
        if gen_proton_pz > 0:
            h_gen_proton_xi_pos.Fill(e.gen_proton_xi[ita])
        else:
            h_gen_proton_xi_neg.Fill(e.gen_proton_xi[ita])
        ita=ita+1
    #This is to look at gen W pt
    if not DATA and len(e.gen_W_pt)>0:
        h_gen_Wpt.Fill(e.gen_W_pt[0])
    if not DATA and len(e.gen_W_pt)>0 and jet_veto and e.WLeptonicPt>200 and e.met > 40:
        h_gen_Wpt_recopt200.Fill(e.gen_W_pt[0])        
    ##########################################


    if e.muon_pt.size() == 0:
        continue
    
    dphi_lepton_jet=GetDphi(e.muon_phi[0],e.jet_phi[0])
    deta_lepton_jet=e.muon_eta[0]-e.jet_eta[0]
    deltaR=m.sqrt(dphi_lepton_jet*dphi_lepton_jet+deta_lepton_jet*deta_lepton_jet   )
    h_deltaR_lepton_jet.Fill(deltaR,pileupw)
    dphi_jet_met=abs(GetDphi(e.jet_phi[0],e.met_phi))
    h_deltaphi_jet_met.Fill(dphi_jet_met,pileupw)
    dphi_jet_Wl=abs(GetDphi(e.jet_phi[0],e.WLeptonicPhi))
    h_deltaphi_jet_Wleptonic.Fill(dphi_jet_Wl,pileupw)

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
    h_extra_tracks_vs_vertices.Fill(e.nVertices,pfcand_nextracks,pileupw)

    #These are plots with just preselection
    h_muon_pt.Fill(e.muon_pt[0],pileupw)
    h_muon_eta.Fill(e.muon_eta[0],pileupw)
    h_muon_iso.Fill(e.muon_iso[0],pileupw)
    h_jet_pt.Fill(e.jet_pt[0],pileupw)
    h_jet_eta.Fill(e.jet_eta[0],pileupw)
    h_tau21.Fill(tau21,pileupw)
    h_prunedMass.Fill(prunedMass,pileupw)
    h_recoMWhad.Fill(recoMWhad,pileupw)
    h_recoMWlep.Fill(recoMWlep,pileupw)
    h_dphiWW.Fill(dphiWW,pileupw)
    h_WLeptonicPt.Fill(WLeptonicPt,pileupw)
    h_recoMWW.Fill(recoMWW,pileupw)
    h_MET.Fill(MET,pileupw)
    h_pfcand_nextracks.Fill(pfcand_nextracks,pileupw)
    h_num_vertices.Fill(e.nVertices)
    h_num_vertices_preweight.Fill(e.nVertices,pileupw)
    h_num_jets_ak4.Fill(e.num_jets_ak4,pileupw)
    h_num_bjets_ak4.Fill(e.num_bjets_ak4,pileupw)
    h_num_bjets_ak8.Fill(e.num_bjets_ak8,pileupw)

    h_tau21_vs_prunedMass.Fill(prunedMass,tau21)

    if e.num_bjets_ak4>0 or e.num_bjets_ak8>0:
        h_num_jets_ak4_wbjet.Fill(e.num_jets_ak4,pileupw)


    if jet_veto:
        h_muon_pt_jetVeto.Fill(e.muon_pt[0],pileupw)
        h_muon_eta_jetVeto.Fill(e.muon_eta[0],pileupw)
        h_jet_pt_jetVeto.Fill(e.jet_pt[0],pileupw)
        h_jet_eta_jetVeto.Fill(e.jet_eta[0],pileupw)
        h_tau21_jetVeto.Fill(tau21,pileupw)
        h_prunedMass_jetVeto.Fill(prunedMass,pileupw)
        h_recoMWhad_jetVeto.Fill(recoMWhad,pileupw)
        h_recoMWlep_jetVeto.Fill(recoMWlep,pileupw)
        h_dphiWW_jetVeto.Fill(dphiWW,pileupw)
        h_WLeptonicPt_jetVeto.Fill(WLeptonicPt,pileupw)
        h_recoMWW_jetVeto.Fill(recoMWW,pileupw)
        h_MET_jetVeto.Fill(MET,pileupw)
        h_pfcand_nextracks_jetVeto.Fill(pfcand_nextracks,pileupw)
        h_num_vertices_jetVeto.Fill(e.nVertices)
        h_num_vertices_preweight_jetVeto.Fill(e.nVertices,pileupw)
        h_deltaR_lepton_jet_jetVeto.Fill(deltaR,pileupw)
        h_deltaphi_jet_met_jetVeto.Fill(GetDphi(e.jet_phi[0],e.met_phi),pileupw)
        h_muon_iso_jetVeto.Fill(e.muon_iso[0],pileupw)
        #print e.muon_charge
        if e.muon_charge[0]>0:
            h_jet_pt_jetVeto_Wplus.Fill(e.jet_pt[0],pileupw)
        if e.muon_charge[0]<0:
            h_jet_pt_jetVeto_Wminus.Fill(e.jet_pt[0],pileupw)
        h_dphiWW_after_jetVeto.Fill(dphiWW,pileupw)
        h_pfcand_nextracks_after_jetVeto.Fill(pfcand_nextracks,pileupw)

    #Looking W leptonic cuts in addition to preselection cuts
    if WLeptonicPt>200 and MET > 40:
        h_recoMWhad_nojetVeto_WleptonicCuts.Fill(recoMWhad,pileupw)
        h_prunedMass_nojetVeto_WleptonicCuts.Fill(prunedMass,pileupw)

    #Looking W leptonic cuts in addition to preselection cuts with jet veto
    if jet_veto and WLeptonicPt>200 and MET > 40:
        h_muon_pt_jetVeto_WleptonicCuts.Fill(e.muon_pt[0],pileupw)
        h_muon_eta_jetVeto_WleptonicCuts.Fill(e.muon_eta[0],pileupw)
        h_jet_pt_jetVeto_WleptonicCuts.Fill(e.jet_pt[0],pileupw)
        h_jet_eta_jetVeto_WleptonicCuts.Fill(e.jet_eta[0],pileupw)
        h_tau21_jetVeto_WleptonicCuts.Fill(tau21,pileupw)
        h_prunedMass_jetVeto_WleptonicCuts.Fill(prunedMass,pileupw)
        h_recoMWhad_jetVeto_WleptonicCuts.Fill(recoMWhad,pileupw)
        h_recoMWlep_jetVeto_WleptonicCuts.Fill(recoMWlep,pileupw)
        h_dphiWW_jetVeto_WleptonicCuts.Fill(dphiWW,pileupw)
        h_WLeptonicPt_jetVeto_WleptonicCuts.Fill(WLeptonicPt,pileupw)
        h_recoMWW_jetVeto_WleptonicCuts.Fill(recoMWW,pileupw)
        h_MET_jetVeto_WleptonicCuts.Fill(MET,pileupw)
        h_pfcand_nextracks_jetVeto_WleptonicCuts.Fill(pfcand_nextracks,pileupw)
        h_num_vertices_jetVeto_WleptonicCuts.Fill(e.nVertices)
        h_num_vertices_preweight_jetVeto_WleptonicCuts.Fill(e.nVertices,pileupw)

    #Looking at Mauricio jet veto with W leptonic cuts
    if e.num_bjets_ak4<1 and WLeptonicPt>200 and MET > 40:
        h_muon_pt_MjetVeto_WleptonicCuts.Fill(e.muon_pt[0],pileupw)
        h_muon_eta_MjetVeto_WleptonicCuts.Fill(e.muon_eta[0],pileupw)
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


    #Plots after jet pruning requirements.
    jet_pruning=False
    #if tau21<0.6 and prunedMass>40 and prunedMass<120:
    #if tau21<0.6 and prunedMass>50 and prunedMass<110:
    if prunedMass>50 and prunedMass<110:
        jet_pruning=True
    if jet_pruning and jet_veto:
        h_muon_pt_jetpruned.Fill(e.muon_pt[0],pileupw)
        h_muon_eta_jetpruned.Fill(e.muon_eta[0],pileupw)
        h_jet_pt_jetpruned.Fill(e.jet_pt[0],pileupw)
        h_jet_eta_jetpruned.Fill(e.jet_eta[0],pileupw)
        #h_tau21_jetpruned.Fill(tau21)
        #h_prunedMass_jetpruned.Fill(prunedMass)
        h_recoMWhad_jetpruned.Fill(recoMWhad,pileupw)
        h_recoMWlep_jetpruned.Fill(recoMWlep,pileupw)
        h_dphiWW_jetpruned.Fill(dphiWW,pileupw)
        h_WLeptonicPt_jetpruned.Fill(WLeptonicPt,pileupw)
        h_recoMWW_jetpruned.Fill(recoMWW,pileupw)
        h_MET_jetpruned.Fill(MET,pileupw)
        h_pfcand_nextracks_jetpruned.Fill(pfcand_nextracks,pileupw)
        h_num_jets_ak4_jetpruned.Fill(e.num_jets_ak4,pileupw)
        h_num_bjets_ak4_jetpruned.Fill(e.num_bjets_ak4,pileupw)
        h_num_bjets_ak8_jetpruned.Fill(e.num_bjets_ak8,pileupw)


    passesBoosted=False
    if dphiWW>2.5 and recoMWW>500 and MET>40 and WLeptonicPt>200:
        passesBoosted=True

    if jet_veto and passesBoosted:
        h_extra_tracks_vs_vertices_boosted.Fill(e.nVertices,pfcand_nextracks,pileupw)

    #Looking at No jet veto with W leptonic cuts and very boosted
    if jet_veto and passesBoosted and recoMWW> 900:
        h_muon_pt_veryBoosted_noExtraJets.Fill(e.muon_pt[0],pileupw)
        h_muon_eta_veryBoosted_noExtraJets.Fill(e.muon_eta[0],pileupw)
        h_jet_pt_veryBoosted_noExtraJets.Fill(e.jet_pt[0],pileupw)
        h_jet_eta_veryBoosted_noExtraJets.Fill(e.jet_eta[0],pileupw)
        h_tau21_veryBoosted_noExtraJets.Fill(tau21,pileupw)
        h_prunedMass_veryBoosted_noExtraJets.Fill(prunedMass,pileupw)
        h_recoMWhad_veryBoosted_noExtraJets.Fill(recoMWhad,pileupw)
        h_recoMWlep_veryBoosted_noExtraJets.Fill(recoMWlep,pileupw)
        h_dphiWW_veryBoosted_noExtraJets.Fill(dphiWW,pileupw)
        h_WLeptonicPt_veryBoosted_noExtraJets.Fill(WLeptonicPt,pileupw)
        h_recoMWW_veryBoosted_noExtraJets.Fill(recoMWW,pileupw)
        h_MET_veryBoosted_noExtraJets.Fill(MET,pileupw)
        h_pfcand_nextracks_veryBoosted_noExtraJets.Fill(pfcand_nextracks,pileupw)
        h_num_vertices_veryBoosted_noExtraJets.Fill(e.nVertices)
        h_num_vertices_preweight_veryBoosted_noExtraJets.Fill(e.nVertices,pileupw)

    #Looking at Mauricio jet veto with W leptonic cuts and very boosted
    if e.num_bjets_ak4<1 and passesBoosted and recoMWW > 900:
        h_muon_pt_veryBoosted_MjetVeto.Fill(e.muon_pt[0],pileupw)
        h_muon_eta_veryBoosted_MjetVeto.Fill(e.muon_eta[0],pileupw)
        h_jet_pt_veryBoosted_MjetVeto.Fill(e.jet_pt[0],pileupw)
        h_jet_eta_veryBoosted_MjetVeto.Fill(e.jet_eta[0],pileupw)
        h_tau21_veryBoosted_MjetVeto.Fill(tau21,pileupw)
        h_prunedMass_veryBoosted_MjetVeto.Fill(prunedMass,pileupw)
        h_recoMWhad_veryBoosted_MjetVeto.Fill(recoMWhad,pileupw)
        h_recoMWlep_veryBoosted_MjetVeto.Fill(recoMWlep,pileupw)
        h_dphiWW_veryBoosted_MjetVeto.Fill(dphiWW,pileupw)
        h_WLeptonicPt_veryBoosted_MjetVeto.Fill(WLeptonicPt,pileupw)
        h_recoMWW_veryBoosted_MjetVeto.Fill(recoMWW,pileupw)
        h_MET_veryBoosted_MjetVeto.Fill(MET,pileupw)
        h_pfcand_nextracks_veryBoosted_MjetVeto.Fill(pfcand_nextracks,pileupw)
        h_num_vertices_veryBoosted_MjetVeto.Fill(e.nVertices)
        h_num_vertices_preweight_veryBoosted_MjetVeto.Fill(e.nVertices,pileupw)



    #Counting number of events after adding each CMS cut
    if jet_veto and dphiWW>2.5: 
        h_recoMWW_afterDphi.Fill(recoMWW,pileupw)
    if jet_veto and dphiWW>2.5 and recoMWW>500: 
        h_recoMWhad_afterMWW.Fill(recoMWhad,pileupw)
    if jet_veto and dphiWW>2.5 and recoMWW>500 and recoMWhad>40:
        h_MET_afterMWhad.Fill(MET,pileupw)
    if jet_veto and dphiWW>2.5 and recoMWW>500 and recoMWhad>40 and MET>40: 
        h_WLeptonicPt_afterMET.Fill(WLeptonicPt,pileupw)
        h_jet_pt_afterMET.Fill(e.jet_pt[0],pileupw)
    #Looking at number of extra tracks after all CMS cuts, no PPS cuts
    if jet_veto and dphiWW>2.5 and recoMWW>500 and recoMWhad>40 and MET>40 and WLeptonicPt>200:
        if DATA:
            if pfcand_nextracks>9:
                h_pfcand_nextracks_afterWLeptonicPt.Fill(pfcand_nextracks,pileupw)
                h_num_vertices_pfcand_nextracks_afterWLeptonicPt.Fill(e.nVertices,pileupw)
            if e.nVertices < 20:
                h_pfcand_nextracks_afterWLeptonicPt_0_20_vertices.Fill(pfcand_nextracks,pileupw)
            if e.nVertices > 19 and e.nVertices < 36:
                h_pfcand_nextracks_afterWLeptonicPt_20_35_vertices.Fill(pfcand_nextracks,pileupw)
            if e.nVertices > 35:
                h_pfcand_nextracks_afterWLeptonicPt_35_up_vertices.Fill(pfcand_nextracks,pileupw)
        else:
            h_pfcand_nextracks_afterWLeptonicPt.Fill(pfcand_nextracks,pileupw)
            h_num_vertices_pfcand_nextracks_afterWLeptonicPt.Fill(e.nVertices,pileupw)
            if e.nVertices < 20:
                h_pfcand_nextracks_afterWLeptonicPt_0_20_vertices.Fill(pfcand_nextracks,pileupw)
            if e.nVertices > 19 and e.nVertices < 36:
                h_pfcand_nextracks_afterWLeptonicPt_20_35_vertices.Fill(pfcand_nextracks,pileupw)
            if e.nVertices > 35:
                h_pfcand_nextracks_afterWLeptonicPt_35_up_vertices.Fill(pfcand_nextracks,pileupw)



    ######################################################################
    #Now Add PPS requirements
    ######################################################################
    #Look to see if passing PPS
    xi = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[]}
    passesPPS=False
    passesPPSSignalMixing=False
    reweight_extra_tracks=1.


    #If data get protons from PPS reco
    if mjet_veto and passesBoosted and jet_pruning and DATA:
        passesPPS=passPPSNew(e,xi)
    #If exclusive WW MC then see if signal protons produce reco PPS protons. 
    if mjet_veto and passesBoosted and jet_pruning and not DATA and ExclusiveMC:
        #print "Get into Signal Mixing for Signal MC"
        if passPPSNew(e,xi):
            #print "passPPSNew"
            passesPPSSignalMixing=passPPSSimMixingSignal(e.mc_pu_trueinteractions)
            #Then correct for signal efficiency of multiple protons in PPS 
            if passesPPSSignalMixing:
                passesPPS=True
    #All other MC take pileup protons from data distributions
    if mjet_veto and passesBoosted and jet_pruning and not DATA and not ExclusiveMC:
        #if pfcand_nextracks < 100:
        #    reweight_extra_tracks=ratio[int(pfcand_nextracks/5)]
        passesPPS,xi_sim=passPPSSimMixing()
        if passesPPS:
            xi["23"].append(xi_sim[0])
            xi["123"].append(xi_sim[1])

    M_RP=-999.
    Rapidity_RP=-999.
    #Calculate M_RP and Rapidity_RP
    if mjet_veto and passesBoosted and jet_pruning and passesPPS:
        M_RP=m.sqrt(169000000*xi["23"][0]*xi["123"][0])
        if xi["23"][0] > 0 and xi["123"][0] > 0:
            Rapidity_RP=0.5*m.log(xi["23"][0]/xi["123"][0])


    ######################################################################
    #Start of looking at only MC passing PPS for signal region, this is to keep things blind
    ######################################################################
    if mjet_veto and passesBoosted and jet_pruning and passesPPS and not DATA:
        h_num_extra_tracks_PPS.Fill(pfcand_nextracks,pileupw)
        h_num_extra_tracks_PPS_reweight_extra_tracks.Fill(pfcand_nextracks,pileupw*reweight_extra_tracks)
        h_num_extra_tracks_PPS_noDRl.Fill(pfcand_nextracks_noDRl,pileupw)

    if mjet_veto and passesBoosted and jet_pruning and passesPPS and not DATA and pfcand_nextracks<5 and recoMWW>900:      
        h_MWW_MX_0_4_tracks_recoMWW900.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)

    if mjet_veto and passesBoosted and jet_pruning and passesPPS and not DATA:                            
        if pfcand_nextracks<5:
            h_xi_1_0_4_extratracks.Fill(xi["23"][0],pileupw*reweight_extra_tracks)
            h_xi_2_0_4_extratracks.Fill(xi["123"][0],pileupw*reweight_extra_tracks)
            h_MX_0_4_extratracks.Fill(M_RP,pileupw*reweight_extra_tracks)
            h_Y_RP_0_4_extratracks.Fill(Rapidity_RP,pileupw*reweight_extra_tracks)
            h_Y_CMS_minus_RP_0_4_extratracks.Fill(recoYCMS-Rapidity_RP,pileupw*reweight_extra_tracks)                        
            h_MWW_MX_0_4_tracks.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)
            h_recoMWhad_0_4_tracks.Fill(recoMWhad,pileupw*reweight_extra_tracks)
            h_tau21_0_4_tracks.Fill(tau21,pileupw)
            h_prunedMass_0_4_tracks.Fill(prunedMass,pileupw)

        if pfcand_nextracks<10:
            h_xi_1_0_9_extratracks.Fill(xi["23"][0],pileupw*reweight_extra_tracks)
            h_xi_2_0_9_extratracks.Fill(xi["123"][0],pileupw*reweight_extra_tracks)
            h_MX_0_9_extratracks.Fill(M_RP,pileupw*reweight_extra_tracks)
            h_Y_RP_0_9_extratracks.Fill(Rapidity_RP,pileupw*reweight_extra_tracks)
            h_Y_CMS_minus_RP_0_9_extratracks.Fill(recoYCMS-Rapidity_RP,pileupw*reweight_extra_tracks)
            h_MWW_MX_0_9_extratracks.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)


    if mjet_veto and passesBoosted and jet_pruning and passesPPS and not DATA and pfcand_nextracks<5:
        if abs(recoYCMS-Rapidity_RP) < 0.6:
            h_MWW_MX_0_4_tracks_Ycut.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)

    if mjet_veto and passesBoosted and jet_pruning and passesPPS and not DATA and pfcand_nextracks<5 and recoMWhad > 50 and recoMWhad < 140:
        h_xi_1_0_4_extratracks_Mhad.Fill(xi["23"][0],pileupw*reweight_extra_tracks)
        h_xi_2_0_4_extratracks_Mhad.Fill(xi["123"][0],pileupw*reweight_extra_tracks)
        h_MX_0_4_extratracks_Mhad.Fill(M_RP,pileupw*reweight_extra_tracks)
        h_Y_RP_0_4_extratracks_Mhad.Fill(Rapidity_RP,pileupw*reweight_extra_tracks)
        h_Y_CMS_minus_RP_0_4_extratracks_Mhad.Fill(recoYCMS-Rapidity_RP,pileupw*reweight_extra_tracks)                
        h_MWW_MX_0_4_tracks_Mhad.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)
        
        if abs(recoYCMS-Rapidity_RP) < 1:
            h_MWW_MX_0_4_tracks_Mhad_Ycut.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)
    ###########################################################
    #End of looking at only MC passing PPS
    ###########################################################
                    
    if jet_pruning and mjet_veto and passesBoosted and jet_pruning and passesPPS:
        h_pfcand_nextracks_after_jet_veto_jet_pruning_PPS.Fill(pfcand_nextracks,pileupw)
        if not (dphiWW>2.5 and recoMWW>500 and MET>40 and WLeptonicPt>200):
            h_pfcand_nextracks_after_jet_veto_jet_pruning_veto_signal_PPS.Fill(pfcand_nextracks,pileupw)
        if not (dphiWW>2.5 and MET>40 and WLeptonicPt>200):
            #M_RP=m.sqrt(169000000*xi["23"][0]*xi["123"][0])
            h_mass_cms_vs_rp.Fill(M_RP,recoMWW)


    if mjet_veto and passesBoosted and jet_pruning and passesPPS and DATA and pfcand_nextracks>9:
        if abs(recoYCMS-Rapidity_RP) < 0.6:
            h_MWW_MX_9_up_extratracks_dY_l0p6.Fill(recoMWW/M_RP,pileupw)
        else:
            h_MWW_MX_9_up_extratracks_dY_g0p6.Fill(recoMWW/M_RP,pileupw)



    ###########################################################
    #Start of looking at control regions
    ###########################################################
    
    #Looking large extra tracks passing PPS, this is conrol region for W+jets and ttbar
    if mjet_veto and passesBoosted and jet_pruning and passesPPS and pfcand_nextracks >9:
        h_xi_1_10_up.Fill(xi["23"][0],pileupw*reweight_extra_tracks)
        h_xi_2_10_up.Fill(xi["123"][0],pileupw*reweight_extra_tracks)
        h_Y_RP_10_up.Fill(M_RP,pileupw*reweight_extra_tracks)
        h_Y_CMS_minus_RP_10_up.Fill(recoYCMS-Rapidity_RP,pileupw*reweight_extra_tracks)
        h_MX_10_up.Fill(M_RP,pileupw*reweight_extra_tracks)
        h_MWW_MX_10_up.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)
        h_recoMWhad_control_10_up.Fill(recoMWhad,pileupw*reweight_extra_tracks)
        h_tau21_control_10_up.Fill(tau21,pileupw)
        h_prunedMass_control_10_up.Fill(prunedMass,pileupw)
        h_extra_tracks_vs_MX_PPS.Fill(M_RP,pfcand_nextracks,pileupw)
        h_extra_tracks_vs_MWW_PPS.Fill(M_RP,pfcand_nextracks,pileupw)

    if mjet_veto and passesBoosted and jet_pruning and passesPPS and pfcand_nextracks >4 and recoMWW>900:
        h_MWW_MX_5_up_recoMWW900.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)
        h_Y_CMS_minus_RP_5_up_recoMWW.Fill(recoYCMS-Rapidity_RP,pileupw*reweight_extra_tracks)

    if mjet_veto and passesBoosted and jet_pruning and passesPPS and pfcand_nextracks >4 and pfcand_nextracks < 16 and recoMWW>900:
        h_MWW_MX_5_15_recoMWW900.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)

    if mjet_veto and passesBoosted and jet_pruning and passesPPS and pfcand_nextracks >9 and recoMWW>900 and abs(recoYCMS-Rapidity_RP)<0.6:
        h_MWW_MX_5_up_recoMWW900_Ycut.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)

    #Looking at control region not passing PPS, this is for EXTRA TRACKS reweighting
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS:
        h_num_extra_tracks_notPPS.Fill(pfcand_nextracks,pileupw)
        h_num_extra_tracks_notPPS_noDRl.Fill(pfcand_nextracks_noDRl,pileupw)
        if DATA:
            h_num_extra_tracks_notPPS_reweight_extra_tracks.Fill(pfcand_nextracks,pileupw)
        else:
            h_num_extra_tracks_notPPS_reweight_extra_tracks.Fill(pfcand_nextracks,pileupw*reweight_extra_tracks)

    #Looking at control region not passing PPS, this is for EXTRA TRACKS reweighting, recoMWW>900
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and recoMWW>900:
        h_num_extra_tracks_notPPS_recoMWW900.Fill(pfcand_nextracks,pileupw)
        #h_num_extra_tracks_notPPS_noDRl.Fill(pfcand_nextracks_noDRl,pileupw)
        if DATA:
            h_num_extra_tracks_notPPS_reweight_extra_tracks_recoMWW900.Fill(pfcand_nextracks,pileupw)
        else:
            h_num_extra_tracks_notPPS_reweight_extra_tracks_recoMWW900.Fill(pfcand_nextracks,pileupw*reweight_extra_tracks)


    #Looking at control region not passing PPS to get ratio of high to low for MWW.
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS:
        h_MWW_extra_tracks_notPPS.Fill(recoMWW,pileupw)        
        h_extra_tracks_vs_MWW_notPPS.Fill(recoMWW,pfcand_nextracks,pileupw)
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks<10:
        h_MWW_extra_tracks_0_9_notPPS.Fill(recoMWW,pileupw)        
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks>9:
        h_MWW_extra_tracks_9_up_notPPS.Fill(recoMWW,pileupw)

    #Looking at control region not passing PPS and pfcand_nextracks<5
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks<5:
        h_MWW_extra_tracks_0_4_notPPS.Fill(recoMWW,pileupw)
        h_num_jets_not_PPS_0_4_extra_tracks.Fill(e.num_jets_ak4,pileupw)
        h_recoMWhad_not_PPS_0_4_extra_tracks.Fill(recoMWhad,pileupw)
        if recoMWhad > 50:
            h_num_jets_not_PPS_0_4_extra_tracks_recoMWhad.Fill(e.num_jets_ak4,pileupw)

    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks<5 and recoMWW>900:
        h_MWW_900_extra_tracks_0_4_notPPS.Fill(recoMWW,pileupw)
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks>4 and pfcand_nextracks<16 and recoMWW>900:
        h_MWW_900_extra_tracks_5_15_notPPS.Fill(recoMWW,pileupw)
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks>4 and recoMWW>900:
        h_MWW_900_extra_tracks_5_up_notPPS.Fill(recoMWW,pileupw)

    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks<5 and recoMWW>900:
        h_MWW_900_extra_tracks_0_4_notPPS.Fill(recoMWW,pileupw)
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks>4 and pfcand_nextracks<16 and recoMWW>900:
        h_MWW_900_extra_tracks_5_15_notPPS.Fill(recoMWW,pileupw)
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks>4 and pfcand_nextracks<16 and recoMWW>900:
        h_MWW_900_extra_tracks_5_up_notPPS.Fill(recoMWW,pileupw)



    #Looking at control region not passing PPS and pfcand_nextracks_noDRL<5
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks_noDRl<5:
        h_num_jets_not_PPS_0_4_extra_tracks_noDRl.Fill(e.num_jets_ak4,pileupw)
        h_recoMWhad_not_PPS_0_4_extra_tracks_noDRl.Fill(recoMWhad,pileupw)
        if recoMWhad > 50:
            h_num_jets_not_PPS_0_4_extra_tracks_recoMWhad_noDRl.Fill(e.num_jets_ak4,pileupw)

    #Data control region for W+jets passing PPS, DATA
    if mjet_veto and passesBoosted and jet_pruning and passesPPS and recoMWhad<50 and DATA:
        h_mass_cms_vs_rp_WjetsControlRegion.Fill(M_RP,recoMWW)
        h_MWW_MX_Data_Mwhad_0_50.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)
        h_Y_CMS_minus_RP_Data_Mwhad_0_50.Fill(recoYCMS-Rapidity_RP,pileupw*reweight_extra_tracks)
        if pfcand_nextracks<5:
            h_MWW_MX_0_4_tracks_Data_Mwhad_0_50.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)
            h_Y_CMS_minus_RP_0_4_extratracks_Data_Mwhad_0_50.Fill(recoYCMS-Rapidity_RP,pileupw*reweight_extra_tracks) 
        if pfcand_nextracks<10:
            h_MWW_MX_0_9_tracks_Data_Mwhad_0_50.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)
            h_Y_CMS_minus_RP_0_9_extratracks_Data_Mwhad_0_50.Fill(recoYCMS-Rapidity_RP,pileupw*reweight_extra_tracks) 
        if pfcand_nextracks>9:
            h_MWW_MX_10_up_tracks_Data_Mwhad_0_50.Fill(recoMWW/M_RP,pileupw*reweight_extra_tracks)
            h_Y_CMS_minus_RP_10_up_extratracks_Data_Mwhad_0_50.Fill(recoYCMS-Rapidity_RP,pileupw*reweight_extra_tracks)

    #Data control region for W+jets, DATA and MC
    if mjet_veto and passesBoosted and jet_pruning and passesPPS and recoMWhad<50:
        if pfcand_nextracks_noDRl>9:
            h_num_extra_tracks_PPS_noDRl.Fill(pfcand_nextracks_noDRl,pileupw)
        if pfcand_nextracks>9:
            h_num_extra_tracks_PPS.Fill(pfcand_nextracks,pileupw)
            h_num_extra_tracks_PPS_reweight_extra_tracks.Fill(pfcand_nextracks,pileupw*reweight_extra_tracks)


    #W+jets control region, no PPS requirements
    if mjet_veto and passesBoosted and jet_pruning:
        h_recoMWhad_Wjets_centralControlRegion.Fill(recoMWhad,pileupw)
    if mjet_veto and passesBoosted and jet_pruning and recoMWhad < 50:
        h_recoMWW_Wjets_centralControlRegion.Fill(recoMWW,pileupw)
        if pfcand_nextracks>9:
            h_recoMWW_Wjets_centralControlRegion_10_up.Fill(recoMWW,pileupw)
        if pfcand_nextracks<10:
            h_recoMWW_Wjets_centralControlRegion_0_9.Fill(recoMWW,pileupw)
        if pfcand_nextracks<5:
            h_recoMWW_Wjets_centralControlRegion_0_5.Fill(recoMWW,pileupw)

    #Only look at low number of tracks for events not passing PPS, this way keep blind
    if mjet_veto and passesBoosted and jet_pruning and recoMWhad > 50 and pfcand_nextracks>9:
        h_recoMWW_Wjets_centralControlRegion_10_up_Mwhad.Fill(recoMWW,pileupw)
    #W+jets control region, not passing PPS. Can look at low number of extra tracks, because no overlap with signal region
    if mjet_veto and passesBoosted and jet_pruning and recoMWhad > 50 and not passesPPS:
        if pfcand_nextracks<5:
            h_recoMWW_Wjets_centralControlRegion_0_5_Mwhad_noPPS.Fill(recoMWW,pileupw)
        if pfcand_nextracks<10:
            h_recoMWW_Wjets_centralControlRegion_0_9_Mwhad_noPPS.Fill(recoMWW,pileupw)
        if pfcand_nextracks>9:
            h_recoMWW_Wjets_centralControlRegion_10_up_Mwhad_noPPS.Fill(recoMWW,pileupw)


    #Look at ttbar control region with b-requirement and Passing PPS
    xi_b = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[]}
    if (e.num_jets_ak4<1 and e.num_bjets_ak8 >0) and passesBoosted and jet_pruning and DATA:
        reweight_extra_tracks=1.
        passesPPS_b=False
        passesPPS_b=passPPSNew(e,xi_b)
    M_RP_b=-999.
    Rapidity_RP_b=-999.
    if (e.num_jets_ak4<1 and e.num_bjets_ak8 >0) and passesBoosted and jet_pruning and DATA and passesPPS:
        M_RP_b=m.sqrt(169000000*xi_b["23"][0]*xi_b["123"][0])
        if xi_b["23"][0] > 0 and xi_b["123"][0] > 0:
            Rapidity_RP_b=0.5*m.log(xi_b["23"][0]/xi_b["123"][0])
    if (e.num_jets_ak4<1 and e.num_bjets_ak8 >0) and passesBoosted and jet_pruning and DATA and passesPPS and pfcand_nextracks>9:
        h_recoMWhad_ttbar_centralControlRegion_PPS.Fill(recoMWhad,pileupw*reweight_extra_tracks)
    if (e.num_jets_ak4<1 and e.num_bjets_ak8 >0) and passesBoosted and jet_pruning and DATA and passesPPS and recoMWhad > 50:
        h_mass_cms_vs_rp_TTbarControlRegion.Fill(M_RP_b,recoMWW)
        h_MWW_MX_Data_Mwhad_50_up_b.Fill(recoMWW/M_RP_b,pileupw*reweight_extra_tracks)
        h_Y_CMS_minus_RP_Data_Mwhad_50_up_b.Fill(recoYCMS-Rapidity_RP_b,pileupw*reweight_extra_tracks)
        if pfcand_nextracks<5:
            h_MWW_MX_0_4_tracks_Data_Mwhad_50_up_b.Fill(recoMWW/M_RP_b,pileupw*reweight_extra_tracks)
            h_Y_CMS_minus_RP_0_4_extratracks_Data_Mwhad_50_up_b.Fill(recoYCMS-Rapidity_RP_b,pileupw*reweight_extra_tracks) 
        if pfcand_nextracks<20:
            h_MWW_MX_0_19_tracks_Data_Mwhad_50_up_b.Fill(recoMWW/M_RP_b,pileupw*reweight_extra_tracks)
            h_Y_CMS_minus_RP_0_19_extratracks_Data_Mwhad_50_up_b.Fill(recoYCMS-Rapidity_RP_b,pileupw*reweight_extra_tracks) 
        if pfcand_nextracks>19:
            h_MWW_MX_20_up_tracks_Data_Mwhad_50_up_b.Fill(recoMWW/M_RP_b,pileupw*reweight_extra_tracks)
            h_Y_CMS_minus_RP_20_up_extratracks_Data_Mwhad_50_up_b.Fill(recoYCMS-Rapidity_RP_b,pileupw*reweight_extra_tracks)


    #TTbar control region, no PPS requirement
    if (e.num_bjets_ak8 >0) and passesBoosted and jet_pruning:
        h_num_jets_ttbar.Fill(e.num_jets_ak4,pileupw)
        if pfcand_nextracks<5:
            h_num_jets_ttbar_0_4_extra_tracks.Fill(e.num_jets_ak4,pileupw)
            h_recoMWhad_ttbar_0_4_extra_tracks.Fill(recoMWhad,pileupw)
            if recoMWhad > 50:
                h_num_jets_ttbar_0_4_extra_tracks_recoMWhad.Fill(e.num_jets_ak4,pileupw)
        if pfcand_nextracks_noDRl<5:
            h_num_jets_ttbar_0_4_extra_tracks_noDRl.Fill(e.num_jets_ak4,pileupw)
            h_recoMWhad_ttbar_0_4_extra_tracks_noDRl.Fill(recoMWhad,pileupw)
            if recoMWhad > 50:
                h_num_jets_ttbar_0_4_extra_tracks_recoMWhad_noDRl.Fill(e.num_jets_ak4,pileupw)


    #TTBAR control region, no PPS requirement
    if (e.num_jets_ak4>0 or e.num_bjets_ak8 > 0) and dphiWW>2.5 and MET>40 and WLeptonicPt>200:
        h_recoMWhad_ttbar_centralControlRegion.Fill(recoMWhad,pileupw)
    if (e.num_jets_ak4>0 or e.num_bjets_ak8 > 0) and dphiWW>2.5 and MET>40 and WLeptonicPt>200 and recoMWhad>50:
        h_recoMWW_ttbar_centralControlRegion.Fill(recoMWW,pileupw)
        if pfcand_nextracks>9:
            h_recoMWW_ttbar_centralControlRegion_10_up.Fill(recoMWW,pileupw)
        if pfcand_nextracks<10:
            h_recoMWW_ttbar_centralControlRegion_0_9.Fill(recoMWW,pileupw)
        if pfcand_nextracks<5:
            h_recoMWW_ttbar_centralControlRegion_0_5.Fill(recoMWW,pileupw)


    #WJets control region, Looking for number of extra tracks of events with 0 AK4 jets and boosted
    if e.num_jets_ak4<1 and passesBoosted and jet_pruning:
        if DATA and pfcand_nextracks>9:
            h_num_extra_tracks_0jets_boosted.Fill(pfcand_nextracks,pileupw)
        else:
            h_num_extra_tracks_0jets_boosted.Fill(pfcand_nextracks,pileupw)

    #WJets control region, Looking for number of extra tracks of events with 0 AK4 jets
    if e.num_jets_ak4<1:
        if DATA and pfcand_nextracks>9:
            h_num_extra_tracks_0jets.Fill(pfcand_nextracks,pileupw)
        else:
            h_num_extra_tracks_0jets.Fill(pfcand_nextracks,pileupw)

    if mjet_veto and passesBoosted and jet_pruning:
        h_recoMWhad_nominal.Fill(recoMWhad,pileupw)
        h_num_extra_tracks_nominal.Fill(pfcand_nextracks,pileupw)


    #Wjets control region, Mauricio jet veto. Looking for number of extra tracks of events with 0 AK4 jets and boosted
    if e.num_bjets_ak4<1 and passesBoosted and jet_pruning:
        if DATA and pfcand_nextracks>9:
            h_num_extra_tracks_nobjets_boosted.Fill(pfcand_nextracks,pileupw)
        else:
            h_num_extra_tracks_nobjets_boosted.Fill(pfcand_nextracks,pileupw)

    #Wjets control region, Mauricio jet veto. Looking for number of extra tracks of events with 0 AK4 jets
    if e.num_bjets_ak4<1:
        if DATA and pfcand_nextracks>9:
            h_num_extra_tracks_nobjets.Fill(pfcand_nextracks,pileupw)
        else:
            h_num_extra_tracks_nobjets.Fill(pfcand_nextracks,pileupw)


    #TTbar control region
    if e.num_jets_ak4>0:
        if DATA and pfcand_nextracks>9:
            h_num_extra_tracks_1plusjets.Fill(pfcand_nextracks,pileupw)
        else:
            h_num_extra_tracks_1plusjets.Fill(pfcand_nextracks,pileupw)
    if e.num_jets_ak4>0 and passesBoosted and jet_pruning:
        if DATA and pfcand_nextracks>9:
            h_num_extra_tracks_1plusjets_boosted.Fill(pfcand_nextracks,pileupw)
        else:
            h_num_extra_tracks_1plusjets_boosted.Fill(pfcand_nextracks,pileupw)

    #Possibly control region for W
    if e.num_jets_ak4>0 and e.num_bjets_ak4==0:
        if DATA and pfcand_nextracks>9:
            h_num_extra_tracks_1plusjets_nobjets.Fill(pfcand_nextracks,pileupw)
        else:
            h_num_extra_tracks_1plusjets_nobjets.Fill(pfcand_nextracks,pileupw)
    if e.num_jets_ak4>0 and e.num_bjets_ak4==0 and passesBoosted and jet_pruning:
        if DATA and pfcand_nextracks>9:
            h_num_extra_tracks_1plusjets_nobjets_boosted.Fill(pfcand_nextracks,pileupw)
        else:
            h_num_extra_tracks_1plusjets_nobjets_boosted.Fill(pfcand_nextracks,pileupw)

    ###########################################################
    #End of looking at control regions
    ###########################################################


    if mjet_veto and not (dphiWW>2.5 and recoMWW>500 and MET>40 and WLeptonicPt>200):
        h_pfcand_nextracks_controlRegion.Fill(pfcand_nextracks,pileupw)

    #Looking at gen proton distribution after passing PPS, this is meant for signal plots
    if mjet_veto and passesBoosted and jet_pruning and passesPPS:
        ita_p=0
        for gen_proton_pz in e.gen_proton_pz:
            if gen_proton_pz > 0:
                h_gen_proton_xi_pos_PPS.Fill(e.gen_proton_xi[ita_p])
            else:
                h_gen_proton_xi_neg_PPS.Fill(e.gen_proton_xi[ita_p])
            ita_p=ita_p+1







h_reco_jetW.Sumw2()
h_gen_jetW.Sumw2()
#h_reco_divide_gen_Wpt.Divide(h_reco_jetW,h_gen_jetW,1,1,"b")
h_reco_divide_gen_Wpt.Divide(h_reco_jetW,h_gen_jetW,1,1)

fout.Write()
fout.Close()
print fout
print("--- %s seconds ---" % (time.time() - start_time))
