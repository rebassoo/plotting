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
fout = TFile('histos/quick/{0}.root'.format(output_name),'recreate')
fout.cd()


#Chain Together List Of Files
chain = TChain('demo/SlimmedNtuple')
AddFilesToChain(chain,ListOfFiles,DATA)

fout.cd()

print("--- %s seconds ---" % (time.time() - start_time))

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

h_muon_pt_passingPPS=TH1F("h_muon_pt_passingPPS",";p_{T} (#mu) [GeV];",100,0,1000)
h_jet_pt_passingPPS=TH1F("h_jet_pt_passingPPS",";p_{T} (jet) [GeV];",120,0,1200)
h_tau21_passingPPS=TH1F("h_tau21_passingPPS",";tau21;",100,0,2)
h_prunedMass_passingPPS=TH1F("h_prunedMass_passingPPS",";prunedMass [GeV];",200,0,1000)
h_WLeptonicPt_passingPPS=TH1F("h_WLeptonicPt_passingPPS",";W Leptonic Pt [GeV];",100,0,1000)
h_recoMWW_passingPPS=TH1F("h_recoMWW_passingPPS",";M_{WW} [GeV];",100,0,2000)
h_MET_passingPPS=TH1F("h_MET_passingPPS",";MET [GeV];",80,0,400)
h_MX_passingPPS=TH1F("h_MX_passingPPS",";Mass RP [GeV];",100,0,3000)
h_Y_CMS_minus_RP_passingPPS=TH1F("h_Y_CMS_minus_RP_passingPPS",";Y RP;",60,-3,3)
h_MWW_MX_passingPPS=TH1F("h_MWW_MX_passingPPS",";MWW/MX;",100,0,2)

h_xi_1_0_4_extratracks=TH1F("h_xi_1_0_4_extratracks",";#xi_{1};",128,0,0.32)
h_xi_2_0_4_extratracks=TH1F("h_xi_2_0_4_extratracks",";#xi_{2};",128,0,0.32)
h_Y_RP_0_4_extratracks=TH1F("h_Y_RP_0_4_extratracks",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_0_4_extratracks=TH1F("h_Y_CMS_minus_RP_0_4_extratracks",";Y RP;",60,-3,3)
h_MX_0_4_extratracks=TH1F("h_MX_0_4_extratracks",";Mass RP [GeV];",100,0,3000)
h_MWW_0_4_extratracks=TH1F("h_MWW_0_4_extratracks",";M_{WW} [GeV];",100,0,3000)
h_MWW_MX_0_4_tracks=TH1F("h_MWW_MX_0_4_tracks",";MWW/MX;",100,0,2)
h_recoMWhad_0_4_tracks=TH1F("h_recoMWhad_0_4_tracks",";M_{W_{had}} [GeV];",100,0,200)
h_tau21_0_4_tracks=TH1F("h_tau21_0_4_tracks",";tau21;",100,0,2)
h_prunedMass_0_4_tracks=TH1F("h_prunedMass_0_4_tracks",";prunedMass [GeV];",200,0,1000)
h_MWW_MX_0_4_tracks_Ycut=TH1F("h_MWW_MX_0_4_tracks_Ycut",";MWW/MX;",100,0,2)

h_xi_1_0_4_extratracks_notPPS=TH1F("h_xi_1_0_4_extratracks_notPPS",";#xi_{1};",128,0,0.32)
h_xi_2_0_4_extratracks_notPPS=TH1F("h_xi_2_0_4_extratracks_notPPS",";#xi_{2};",128,0,0.32)
h_Y_RP_0_4_extratracks_notPPS=TH1F("h_Y_RP_0_4_extratracks_notPPS",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_0_4_extratracks_notPPS=TH1F("h_Y_CMS_minus_RP_0_4_extratracks_notPPS",";Y RP;",60,-3,3)
h_MX_0_4_extratracks_notPPS=TH1F("h_MX_0_4_extratracks_notPPS",";Mass RP [GeV];",100,0,3000)
h_MWW_0_4_extratracks_notPPS=TH1F("h_MWW_0_4_extratracks_notPPS",";M_{WW} [GeV];",100,0,3000)
h_MWW_MX_0_4_tracks_notPPS=TH1F("h_MWW_MX_0_4_tracks_notPPS",";MWW/MX;",100,0,2)
h_recoMWhad_0_4_tracks_notPPS=TH1F("h_recoMWhad_0_4_tracks_notPPS",";M_{W_{had}} [GeV];",100,0,200)
h_tau21_0_4_tracks_notPPS=TH1F("h_tau21_0_4_tracks_notPPS",";tau21;",100,0,2)
h_prunedMass_0_4_tracks_notPPS=TH1F("h_prunedMass_0_4_tracks_notPPS",";prunedMass [GeV];",200,0,1000)
h_MWW_MX_0_4_tracks_notPPS_Ycut=TH1F("h_MWW_MX_0_4_tracks_notPPS_Ycut",";MWW/MX;",100,0,2)

h_xi_1_control=TH1F("h_xi_1_control",";#xi_{1};",128,0,0.32)
h_xi_2_control=TH1F("h_xi_2_control",";#xi_{2};",128,0,0.32)
h_Y_RP_control=TH1F("h_Y_RP_control",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_control=TH1F("h_Y_CMS_minus_RP_control",";Y RP;",60,-3,3)
h_MX_control=TH1F("h_MX_control",";Mass RP [GeV];",100,0,3000)
h_MWW_control=TH1F("h_MWW_control",";M_{WW} [GeV];",100,0,3000)
h_MWW_MX_control=TH1F("h_MWW_MX_control",";MWW/MX;",100,0,2)
#h_MWW_minus_MX_control=TH1F("h_MWW_minus_MX",";MWW - MX;",1000,-1000,200)
h_recoMWhad_control_control=TH1F("h_recoMWhad_control_control",";M_{W_{had}} [GeV];",100,0,200)
h_tau21_control_control=TH1F("h_tau21_control_control",";tau21;",100,0,2)
h_prunedMass_control_control=TH1F("h_prunedMass_control_control",";prunedMass [GeV];",200,0,1000)
h_MWW_MX_control_Ycut=TH1F("h_MWW_MX_control_Ycut",";MWW/MX;",100,0,2)

h_xi_1_control_notPPS=TH1F("h_xi_1_control_notPPS",";#xi_{1};",128,0,0.32)
h_xi_2_control_notPPS=TH1F("h_xi_2_control_notPPS",";#xi_{2};",128,0,0.32)
h_Y_RP_control_notPPS=TH1F("h_Y_RP_control_notPPS",";Y RP;",60,-3,3)
h_Y_CMS_minus_RP_control_notPPS=TH1F("h_Y_CMS_minus_RP_control_notPPS",";Y RP;",60,-3,3)
h_MX_control_notPPS=TH1F("h_MX_control_notPPS",";Mass RP [GeV];",100,0,3000)
h_MWW_control_notPPS=TH1F("h_MWW_control_notPPS",";M_{WW} [GeV];",100,0,3000)
h_MWW_MX_control_notPPS=TH1F("h_MWW_MX_control_notPPS",";MWW/MX;",100,0,2)
#h_MWW_minus_MX_control_notPPS=TH1F("h_MWW_minus_MX",";MWW - MX;",1000,-1000,200)
h_recoMWhad_control_control_notPPS=TH1F("h_recoMWhad_control_control_notPPS",";M_{W_{had}} [GeV];",100,0,200)
h_tau21_control_control_notPPS=TH1F("h_tau21_control_control_notPPS",";tau21;",100,0,2)
h_prunedMass_control_control_notPPS=TH1F("h_prunedMass_control_control_notPPS",";prunedMass [GeV];",200,0,1000)
h_MWW_MX_control_Ycut_notPPS=TH1F("h_MWW_MX_control_Ycut_notPPS",";MWW/MX;",100,0,2)

h_MWW_MX_control_5_up=TH1F("h_MWW_MX_control_5_up",";MWW/MX;",100,0,2)
h_MWW_MX_control_5_up_Ycut=TH1F("h_MWW_MX_control_5_up_Ycut",";MWW/MX;",100,0,2)
h_MWW_MX_control_15_30=TH1F("h_MWW_MX_control_15_30",";MWW/MX;",100,0,2)
h_MWW_MX_control_30_50=TH1F("h_MWW_MX_control_30_50",";MWW/MX;",100,0,2)
h_MWW_MX_control_50_70=TH1F("h_MWW_MX_control_50_70",";MWW/MX;",100,0,2)
h_MWW_MX_control_70_100=TH1F("h_MWW_MX_control_70_100",";MWW/MX;",100,0,2)

h_num_extra_tracks_nominal=TH1F("h_num_extra_tracks_nominal",";Number of extra tracks;",100,-0.5,99.5)
#h_num_extra_tracks_PPS=TH1F("h_num_extra_tracks_PPS",";Number of extra tracks;",100,-0.5,99.5)
h_num_extra_tracks_PPS=TH1F("h_num_extra_tracks_PPS",";Number of extra tracks;",20,-0.5,99.5)
h_num_extra_tracks_PPS_reweight_extra_tracks=TH1F("h_num_extra_tracks_PPS_reweight_extra_tracks",";Number of extra tracks;",20,-0.5,99.5)
#h_num_extra_tracks_notPPS=TH1F("h_num_extra_tracks_notPPS",";Number of extra tracks;",100,-0.5,99.5)
h_num_extra_tracks_notPPS=TH1F("h_num_extra_tracks_notPPS",";Number of extra tracks;",20,-0.5,99.5)
h_num_extra_tracks_notPPS_reweight_extra_tracks=TH1F("h_num_extra_tracks_notPPS_reweight_extra_tracks",";Number of extra tracks;",20,-0.5,99.5)
h_num_extra_tracks_PPS_noDRl=TH1F("h_num_extra_tracks_PPS_noDRl",";Number of extra tracks;",20,-0.5,99.5)
h_num_extra_tracks_notPPS_noDRl=TH1F("h_num_extra_tracks_notPPS_noDRl",";Number of extra tracks;",20,-0.5,99.5)

h_extra_tracks_vs_MWW_notPPS=TH2F("h_extra_tracks_vs_MWW_notPPS",";;",100,0,2000,100,-0.5,99.5)
h_extra_tracks_vs_MWW_PPS=TH2F("h_extra_tracks_vs_MWW_PPS",";;",100,0,2000,100,-0.5,99.5)
h_extra_tracks_vs_MX_PPS=TH2F("h_extra_tracks_vs_MX_PPS",";;",100,0,2000,100,-0.5,99.5)

h_MWW_notPPS=TH1F("h_MWW_notPPS",";;",100,0,2000)
h_MWW_extra_tracks_0_4_notPPS=TH1F("h_MWW_extra_tracks_0_4_notPPS",";;",100,0,2000)
h_MWW_extra_tracks_5_15_notPPS=TH1F("h_MWW_extra_tracks_5_15_notPPS",";;",100,0,2000)
h_MWW_extra_tracks_5_up_notPPS=TH1F("h_MWW_extra_tracks_5_up_notPPS",";;",100,0,2000)

h_xi_23=TH1F("h_xi_23",";Xi;",128,0,0.32)
h_xi_123=TH1F("h_xi_123",";Xi;",128,0,0.32)

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

    #if DATA:
    #    xi_trigger = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[]}
    #    if passPPSNewPixel(e,xi_trigger):
    #        if len(xi_trigger["23"]) == 1:
    #            h_xi_23.Fill(xi_trigger["23"][0])
    #        if len(xi_trigger["123"]) == 1:
    #           h_xi_123.Fill(xi_trigger["123"][0])

    jet_veto=False
    mjet_veto=False
    #Look at events passing preselection and jet veto
    if e.num_jets_ak4<1 and e.num_bjets_ak8 < 1:
        jet_veto=True
    if e.num_bjets_ak4<1:
        mjet_veto=True

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

    #Plots after jet pruning requirements.
    jet_pruning=False
    #if tau21<0.6 and prunedMass>40 and prunedMass<120:
    #if tau21<0.6 and prunedMass>50 and prunedMass<110:
    if prunedMass>50 and prunedMass<110:
        jet_pruning=True

    passesBoosted=False
    if dphiWW>2.5 and recoMWW>500 and MET>40 and WLeptonicPt>200:
        passesBoosted=True

    #Looking at Mauricio jet veto with W leptonic cuts
    if e.num_bjets_ak4<1 and passesBoosted and MET > 40:
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



    ######################################################################
    #Now Add PPS requirements
    ######################################################################
    #Look to see if passing PPS
    xi = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[]}
    passesPPS=False
    passesPPSSignalMixing=False
    rw_extrk=1.
    rw_prt_mix=1.

    #If data get protons from PPS reco
    if mjet_veto and passesBoosted and jet_pruning and DATA:
        passesPPS=passPPSNew(e,xi)
    if mjet_veto and passesBoosted and jet_pruning and DATA and not passesPPS:
        xi_data=protonDataMixing()
        xi["23"].append(xi_data[0])
        xi["123"].append(xi_data[1])
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
        #    rw_extrk=ratio[int(pfcand_nextracks/5)]
        rw_prt_mix=0.086319
        passesPPS,xi_sim=passPPSSimMixing()
        if passesPPS:
            xi["23"].append(xi_sim[0])
            xi["123"].append(xi_sim[1])

    M_RP=-999.
    Rapidity_RP=-999.
    #Calculate M_RP and Rapidity_RP
    #if mjet_veto and passesBoosted and jet_pruning and passesPPS:
    if mjet_veto and passesBoosted and jet_pruning and passesPPS:
        M_RP=m.sqrt(169000000*xi["23"][0]*xi["123"][0])
        if xi["23"][0] > 0 and xi["123"][0] > 0:
            Rapidity_RP=0.5*m.log(xi["23"][0]/xi["123"][0])

    if mjet_veto and passesBoosted and jet_pruning and DATA and not passesPPS:
        M_RP=m.sqrt(169000000*xi["23"][0]*xi["123"][0])
        if xi["23"][0] > 0 and xi["123"][0] > 0:
            Rapidity_RP=0.5*m.log(xi["23"][0]/xi["123"][0])



    ######################################################################
    #Start of looking at only MC passing PPS for signal region, this is to keep things blind
    ######################################################################
    if mjet_veto and passesBoosted and jet_pruning and passesPPS:
        h_muon_pt_passingPPS.Fill(e.muon_pt[0],pileupw)
        h_jet_pt_passingPPS.Fill(e.jet_pt[0],pileupw)
        h_tau21_passingPPS.Fill(tau21,pileupw)
        h_prunedMass_passingPPS.Fill(prunedMass,pileupw)
        h_WLeptonicPt_passingPPS.Fill(WLeptonicPt,pileupw)
        h_recoMWW_passingPPS.Fill(recoMWW,pileupw)
        h_MET_passingPPS.Fill(MET,pileupw)
        h_MX_passingPPS.Fill(M_RP,pileupw)
        #h_MWW_passingPPS.Fill(recoMWW,pileupw)
        #h_Y_RP_passingPPS.Fill(Rapidity_RP,pileupw)
        h_Y_CMS_minus_RP_passingPPS.Fill(recoYCMS-Rapidity_RP,pileupw)
        h_MWW_MX_passingPPS.Fill(recoMWW/M_RP,pileupw)

    if mjet_veto and passesBoosted and jet_pruning and passesPPS:
        if DATA and pfcand_nextracks>4:
            h_num_extra_tracks_PPS.Fill(pfcand_nextracks,pileupw)
            h_num_extra_tracks_PPS_noDRl.Fill(pfcand_nextracks_noDRl,pileupw)
            h_num_extra_tracks_PPS_reweight_extra_tracks.Fill(pfcand_nextracks,pileupw*rw_extrk)
            h_extra_tracks_vs_MWW_PPS.Fill(recoMWW,pfcand_nextracks,pileupw)
            h_extra_tracks_vs_MX_PPS.Fill(M_RP,pfcand_nextracks,pileupw)
            
        if not DATA:
            h_num_extra_tracks_PPS.Fill(pfcand_nextracks,pileupw)
            h_num_extra_tracks_PPS_reweight_extra_tracks.Fill(pfcand_nextracks,pileupw*rw_extrk*rw_prt_mix)
            h_num_extra_tracks_PPS_noDRl.Fill(pfcand_nextracks_noDRl,pileupw)


    if mjet_veto and passesBoosted and jet_pruning and passesPPS and not DATA:    
        if pfcand_nextracks<5:
            h_xi_1_0_4_extratracks.Fill(xi["23"][0],pileupw*rw_extrk*rw_prt_mix)
            h_xi_2_0_4_extratracks.Fill(xi["123"][0],pileupw*rw_extrk*rw_prt_mix)
            h_MX_0_4_extratracks.Fill(M_RP,pileupw*rw_extrk*rw_prt_mix)
            h_MWW_0_4_extratracks.Fill(recoMWW,pileupw*rw_extrk*rw_prt_mix)
            h_Y_RP_0_4_extratracks.Fill(Rapidity_RP,pileupw*rw_extrk*rw_prt_mix)
            h_Y_CMS_minus_RP_0_4_extratracks.Fill(recoYCMS-Rapidity_RP,pileupw*rw_extrk*rw_prt_mix)                        
            h_MWW_MX_0_4_tracks.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)
            h_recoMWhad_0_4_tracks.Fill(recoMWhad,pileupw*rw_extrk*rw_prt_mix)
            h_tau21_0_4_tracks.Fill(tau21,pileupw)
            h_prunedMass_0_4_tracks.Fill(prunedMass,pileupw)


    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and DATA:    
        if pfcand_nextracks<5:
            h_xi_1_0_4_extratracks_notPPS.Fill(xi["23"][0],pileupw*rw_extrk)
            h_xi_2_0_4_extratracks_notPPS.Fill(xi["123"][0],pileupw*rw_extrk)
            h_MX_0_4_extratracks_notPPS.Fill(M_RP,pileupw*rw_extrk)
            h_MWW_0_4_extratracks_notPPS.Fill(recoMWW,pileupw*rw_extrk)
            h_Y_RP_0_4_extratracks_notPPS.Fill(Rapidity_RP,pileupw*rw_extrk)
            h_Y_CMS_minus_RP_0_4_extratracks_notPPS.Fill(recoYCMS-Rapidity_RP,pileupw*rw_extrk)                        
            h_MWW_MX_0_4_tracks_notPPS.Fill(recoMWW/M_RP,pileupw*rw_extrk)
            h_recoMWhad_0_4_tracks_notPPS.Fill(recoMWhad,pileupw*rw_extrk)
            h_tau21_0_4_tracks_notPPS.Fill(tau21,pileupw*rw_extrk)
            h_prunedMass_0_4_tracks_notPPS.Fill(prunedMass,pileupw*rw_extrk)


    if mjet_veto and passesBoosted and jet_pruning and passesPPS and not DATA and pfcand_nextracks<5 and abs(recoYCMS-Rapidity_RP) < 0.6:
        h_MWW_MX_0_4_tracks_Ycut.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)

    ###########################################################
    #Start of looking at control regions
    ###########################################################
    
    #Looking large extra tracks passing PPS, this is conrol region for W+jets and ttbar
    if mjet_veto and passesBoosted and jet_pruning and passesPPS and pfcand_nextracks<16 and pfcand_nextracks>4:
        h_xi_1_control.Fill(xi["23"][0],pileupw*rw_extrk*rw_prt_mix)
        h_xi_2_control.Fill(xi["123"][0],pileupw*rw_extrk*rw_prt_mix)
        h_Y_RP_control.Fill(M_RP,pileupw*rw_extrk*rw_prt_mix)
        h_Y_CMS_minus_RP_control.Fill(recoYCMS-Rapidity_RP,pileupw*rw_extrk*rw_prt_mix)
        h_MX_control.Fill(M_RP,pileupw*rw_extrk*rw_prt_mix)
        h_MWW_control.Fill(recoMWW,pileupw*rw_extrk*rw_prt_mix)
        h_MWW_MX_control.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)
        h_recoMWhad_control_control.Fill(recoMWhad,pileupw*rw_extrk*rw_prt_mix)
        h_tau21_control_control.Fill(tau21,pileupw*rw_extrk*rw_prt_mix)
        h_prunedMass_control_control.Fill(prunedMass,pileupw*rw_extrk*rw_prt_mix)
        if abs(recoYCMS-Rapidity_RP) < 0.6:
            h_MWW_MX_control_Ycut.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)

    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks<16 and pfcand_nextracks>4 and DATA:
        h_xi_1_control_notPPS.Fill(xi["23"][0],pileupw*rw_extrk*rw_prt_mix)
        h_xi_2_control_notPPS.Fill(xi["123"][0],pileupw*rw_extrk*rw_prt_mix)
        h_Y_RP_control_notPPS.Fill(M_RP,pileupw*rw_extrk*rw_prt_mix)
        h_Y_CMS_minus_RP_control_notPPS.Fill(recoYCMS-Rapidity_RP,pileupw*rw_extrk*rw_prt_mix)
        h_MX_control_notPPS.Fill(M_RP,pileupw*rw_extrk*rw_prt_mix)
        h_MWW_control_notPPS.Fill(recoMWW,pileupw*rw_extrk*rw_prt_mix)
        h_MWW_MX_control_notPPS.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)
        h_recoMWhad_control_control_notPPS.Fill(recoMWhad,pileupw*rw_extrk*rw_prt_mix)
        h_tau21_control_control_notPPS.Fill(tau21,pileupw*rw_extrk*rw_prt_mix)
        h_prunedMass_control_control_notPPS.Fill(prunedMass,pileupw*rw_extrk*rw_prt_mix)
        if abs(recoYCMS-Rapidity_RP) < 0.6:
            h_MWW_MX_control_Ycut_notPPS.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)



    if mjet_veto and passesBoosted and jet_pruning and passesPPS and pfcand_nextracks>4:
        h_MWW_MX_control_5_up.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)
        if abs(recoYCMS-Rapidity_RP) < 0.6:
            h_MWW_MX_control_5_up_Ycut.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)

    if mjet_veto and passesBoosted and jet_pruning and passesPPS and pfcand_nextracks>14 and pfcand_nextracks<31:
        h_MWW_MX_control_15_30.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)
    if mjet_veto and passesBoosted and jet_pruning and passesPPS and pfcand_nextracks>30 and pfcand_nextracks<51:
        h_MWW_MX_control_30_50.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)
    if mjet_veto and passesBoosted and jet_pruning and passesPPS and pfcand_nextracks>50 and pfcand_nextracks<71:
        h_MWW_MX_control_50_70.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)
    if mjet_veto and passesBoosted and jet_pruning and passesPPS and pfcand_nextracks>70 and pfcand_nextracks<101:
        h_MWW_MX_control_70_100.Fill(recoMWW/M_RP,pileupw*rw_extrk*rw_prt_mix)

    #Looking at control region not passing PPS to get ratio of high to low for MWW.
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS:
        h_MWW_notPPS.Fill(recoMWW,pileupw)        
        h_extra_tracks_vs_MWW_notPPS.Fill(recoMWW,pfcand_nextracks,pileupw)
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks<5:
        h_MWW_extra_tracks_0_4_notPPS.Fill(recoMWW,pileupw)        
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks>4 and pfcand_nextracks<16:
        h_MWW_extra_tracks_5_15_notPPS.Fill(recoMWW,pileupw)
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS and pfcand_nextracks>4:
        h_MWW_extra_tracks_5_up_notPPS.Fill(recoMWW,pileupw)

    #Looking at control region not passing PPS, this is for EXTRA TRACKS reweighting
    if mjet_veto and passesBoosted and jet_pruning and not passesPPS:
        h_num_extra_tracks_notPPS.Fill(pfcand_nextracks,pileupw)
        h_num_extra_tracks_notPPS_noDRl.Fill(pfcand_nextracks_noDRl,pileupw)
        if DATA:
            h_num_extra_tracks_notPPS_reweight_extra_tracks.Fill(pfcand_nextracks,pileupw)
        else:
            h_num_extra_tracks_notPPS_reweight_extra_tracks.Fill(pfcand_nextracks,pileupw*rw_extrk)




fout.Write()
fout.Close()
print fout
print("--- %s seconds ---" % (time.time() - start_time))
