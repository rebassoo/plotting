#!/usr/bin/env python
#Finn Rebassoo, LLNL 12-01-2016
import os
from os import listdir
from os.path import isfile, join
from ROOT import *
#import ROOT
import math as m
from htools import *
import sys
import time
#python histos_mue.py WWTo2L2Nu_13TeV-powheg crab_WWTo2L2Nu_13TeV-powheg/170428_005406/0000/
#python histos_mue.py WWTo2L2Nu_13TeV-powheg crab_WWTo2L2Nu_13TeV-powheg/170426_181453/0000/


if len(sys.argv) < 4:
    print "Need to specify 4 inputs parameters, i.e.:"
    print "  python histos_mue.py latest MuonEG crab_runBv3"
    print "  or"
    print "  python histos_mue.py specific MuonEG crab_runBv3/171116_215828/0001"
    sys.exit()

start_time = time.time()
sample_name=sys.argv[2]
#sample_name="DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
print sample_name
file_dir=sys.argv[3]

#print os.listdir('/hadoop/cms/store/user/rebassoo/{0}/{1}/{2}'.format(sample_name,file_dir,sub_dir))


DATA=False
if sample_name == "SingleMuon":
    DATA=True

mypath_prefix='/hadoop/cms/store/user/rebassoo/'
print os.listdir('/hadoop/cms/store/user/rebassoo/{0}/{1}'.format(sample_name,file_dir))
#Chain together root files for data
ListOfFiles=[]
if sys.argv[1] == 'latest':
    if DATA: output_name=sample_name+'_'+file_dir.split('_')[1]
    else: output_name=sample_name
    m_date=0.
    m_date_string=0.
    m_time=0.
    m_time_string=0.
    for d in os.listdir('/hadoop/cms/store/user/rebassoo/{0}/{1}'.format(sample_name,file_dir)):
        date=int(d.split('_')[0])
        date_string=d.split('_')[0]
        t=0
        t_string=''
        if '_' in d:
            t=int(d.split('_')[1])
            t_string=d.split('_')[1]
        if date >= m_date: 
            m_date=date
            m_date_string=date_string
            m_time=t
            m_time_string=t_string
            if t > m_time: 
                m_time=t
                m_time_string=t_string

    print m_date
    print m_time        
    if m_time > 0:
        sub_dir=str(m_date_string)+"_"+str(m_time_string)
    else:
        sub_dir=str(m_date_string)
    print sub_dir
    itt = 0
    for i in os.listdir(mypath_prefix+'/{0}/{1}/{2}'.format(sample_name,file_dir,sub_dir)):
        mypath=mypath_prefix+'{0}/{1}/{2}/{3}/'.format(sample_name,file_dir,sub_dir,i)
        ListOfFiles += [mypath_prefix+'{0}/{1}/{2}/{3}/{4}'.format(sample_name,file_dir,sub_dir,i,f) for f in listdir(mypath) if isfile(join(mypath, f))]

if sys.argv[1] == 'specific':
    mypath=mypath_prefix+'{0}/{1}/'.format(sample_name,file_dir)
    ListOfFiles = [mypath_prefix+'{0}/{1}/{2}'.format(sample_name,file_dir,f) for f in listdir(mypath) if isfile(join(mypath, f))]
    output_name=sample_name+'_'+file_dir.split('_')[1].split('/')[0]+'_'+file_dir.split('/')[2]



fout = TFile('histos/{0}.root'.format(output_name),'recreate')
fout.cd()


#print ListOfFiles
chain = TChain('demo/SlimmedNtuple')
i=0

num_events=0
for file in ListOfFiles:
    i=i+1
    #print file
    if not DATA:
        statinfo = os.stat(file)
        if statinfo.st_size > 0:
        #print statinfo.st_size
            chain.Add(file)
            f=TFile(file)
            h=TH1F()
            h=f.Get("totalEvents/h_total_events")
    #print h.GetEntries()
            num_events=num_events+h.GetEntries()
    if DATA:
        chain.Add(file)
    #if i>5:
    #    break

print "Number of total files: ",i

fout.cd()
print "Number of events: {0}".format(num_events)
#sys.exit()

print("--- %s seconds ---" % (time.time() - start_time))

h_muon_pt=TH1F("h_muon_pt",";p_{T} (#mu) [GeV];",100,0,1000)
h_muon_eta=TH1F("h_muon_eta",";#eta_{#mu};",60,-3,3)
h_muon_iso=TH1F("h_muon_iso",";pf-based isolation {#mu};",20,0,0.2)
h_jet_pt=TH1F("h_jet_pt",";p_{T} (jet) [GeV];",120,0,1200)
h_jet_eta=TH1F("h_jet_eta",";#eta_{jet};",60,-3,3)
h_deltaR_lepton_jet=TH1F("h_deltaR_lepton_jet",";#deltaR(#mu,jet);",200,0,10)
h_deltaphi_jet_met=TH1F("h_deltaphi_jet_met",";#delta#Phi(MET,jet);",100,0,5)
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



h_muon_pt_jet_pruned=TH1F("h_muon_pt_jetpruned",";p_{T} (#mu) [GeV];",100,0,1000)
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

h_dphiWW_after_jetVeto=TH1F("h_dphiWW_after_jetVeto",";dphiWW;",100,0,5)
h_pfcand_nextracks_after_jetVeto=TH1F("h_pfcand_nextracks_after_jetVeto",";Number of extra tracks;",100,-0.5,99.5)
h_recoMWW_afterDphi=TH1F("h_recoMWW_afterDphi",";M_{WW} [GeV];",100,0,2000)
h_recoMWhad_afterMWW=TH1F("h_recoMWhad_afterMWW",";M_{W_{had}} [GeV];",100,0,200)
h_MET_afterMWhad=TH1F("h_MET_afterMWhad",";MET [GeV];",80,0,400)
h_WLeptonicPt_afterMET=TH1F("h_WLeptonicPt_afterMET",";W Leptonic Pt [GeV];",100,0,1000)
h_jet_pt_afterMET=TH1F("h_jet_pt_afterMET",";Jet Pt [GeV];",120,0,1200)
h_pfcand_nextracks_afterWLeptonicPt=TH1F("h_pfcand_nextracks_afterWLeptonicPt",";Number of extra tracks;",100,-0.5,99.5)

h_pfcand_nextracks_controlRegion=TH1F("h_pfcand_nextracks_controlRegion",";Number of extra tracks;",100,-0.5,99.5)
h_mcWeight=TH1F("h_mcWeight",";MC Weight;",100,0,2)

h_pfcand_nextracks_after_jet_veto_PPS=TH1F("h_pfcand_nextracks_after_jet_veto_PPS",";Number of extra tracks;",100,-0.5,99.5)
h_pfcand_nextracks_after_jet_veto_jet_pruning_PPS=TH1F("h_pfcand_nextracks_after_jet_veto_jet_pruning_PPS",";Number of extra tracks;",100,-0.5,99.5)
h_pfcand_nextracks_after_jet_veto_jet_pruning_veto_signal_PPS=TH1F("h_pfcand_nextracks_after_jet_veto_jet_pruning_veto_signal_PPS",";Number of extra tracks;",100,-0.5,99.5)

h_mass_cms_vs_rp=TH2F("h_mass_cms_vs_rp","M_{CMS} [GeV]; M_{RP} [GeV];",2500,0,2500,2500,0,2500)
h_tau21_vs_prunedMass=TH2F("h_tau21_vs_prunedMass","tau21;prunedMass [GeV];",200,0,1000,100,0,2)

run=0.
event=0.
print chain.GetEntries()
crossAngleDict=GetCrossingAngles()
it=0
for e in chain:
    it=it+1
    run=e.run
    event=e.event
    lumi=e.lumiblock
    pileupw=e.pileupWeight
    #pileupw=1.
    #c = dict.fromkeys(["twoLeptons","iMass","oppCharge","fittedVertexPassRequirements","fittedVertexTracks15","fittedVertexTracks0","ptemug30","ptemul30","passesPPS"],False)
    if not DATA:
        h_mcWeight.Fill(e.mcWeight)

    if e.muon_pt.size() == 0:
        continue


    h_muon_pt.Fill(e.muon_pt[0],pileupw)
    h_muon_eta.Fill(e.muon_eta[0],pileupw)
    h_muon_iso.Fill(e.muon_iso[0],pileupw)
    h_jet_pt.Fill(e.jet_pt[0],pileupw)
    h_jet_eta.Fill(e.jet_eta[0],pileupw)
    
    dphi_lepton_jet=GetDphi(e.muon_phi[0],e.jet_phi[0])
    deta_lepton_jet=e.muon_eta[0]-e.jet_eta[0]
    deltaR=m.sqrt(dphi_lepton_jet*dphi_lepton_jet+deta_lepton_jet*deta_lepton_jet   )
    h_deltaR_lepton_jet.Fill(deltaR,pileupw)
    h_deltaphi_jet_met.Fill(GetDphi(e.jet_phi[0],e.met_phi),pileupw)
    #h_deltaphi_jet_Wleptonic

    tau21=e.jet_tau2[0]/e.jet_tau1[0]
    prunedMass=e.jet_corrmass[0]
    recoMWhad=e.recoMWhad
    recoMWlep=e.recoMWlep
    dphiWW=abs(e.dphiWW)
    WLeptonicPt=e.WLeptonicPt
    recoMWW=e.recoMWW
    pfcand_nextracks=e.pfcand_nextracks
    MET=e.met

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

    jet_veto=False
    if e.num_jets_ak4<1 and e.num_bjets_ak8 < 1:
    #if e.num_bjets_ak4<1 and e.num_bjets_ak8 < 1:
        h_muon_iso_jetVeto.Fill(e.muon_iso[0],pileupw)
        jet_veto=True
        h_muon_pt_jetVeto.Fill(e.muon_pt[0],pileupw)
        h_muon_eta_jetVeto.Fill(e.muon_eta[0],pileupw)
        h_jet_pt_jetVeto.Fill(e.jet_pt[0],pileupw)
        h_jet_eta_jetVeto.Fill(e.jet_eta[0],pileupw)
        h_deltaR_lepton_jet_jetVeto.Fill(deltaR,pileupw)
        h_deltaphi_jet_met_jetVeto.Fill(GetDphi(e.jet_phi[0],e.met_phi),pileupw)
        #print e.muon_charge
        if e.muon_charge[0]>0:
            h_jet_pt_jetVeto_Wplus.Fill(e.jet_pt[0],pileupw)
        if e.muon_charge[0]<0:
            h_jet_pt_jetVeto_Wminus.Fill(e.jet_pt[0],pileupw)
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

    h_tau21_vs_prunedMass.Fill(prunedMass,tau21)

    jet_pruning=False
    #if tau21<0.6 and prunedMass>68 and prunedMass<88:

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
        

    if tau21<0.6 and prunedMass>40 and prunedMass<150:
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
    if jet_veto:
        #if e.num_jets_ak4<1 and e.num_bjets_ak8 < 1:
        h_dphiWW_after_jetVeto.Fill(dphiWW,pileupw)
        h_pfcand_nextracks_after_jetVeto.Fill(pfcand_nextracks,pileupw)
        if not (dphiWW>2.5 and recoMWW>500 and (recoMWhad>40 and recoMWhad<120) and MET>40 and WLeptonicPt>200):
            h_pfcand_nextracks_controlRegion.Fill(pfcand_nextracks,pileupw)
            
        if dphiWW>2.5:
            h_recoMWW_afterDphi.Fill(recoMWW,pileupw)
            if recoMWW>500:
                h_recoMWhad_afterMWW.Fill(recoMWhad,pileupw)
                if recoMWhad>40 and recoMWhad<120:
                    h_MET_afterMWhad.Fill(MET,pileupw)
                    if MET>40:
                        h_WLeptonicPt_afterMET.Fill(WLeptonicPt,pileupw)
                        h_jet_pt_afterMET.Fill(e.jet_pt[0],pileupw)
                        if WLeptonicPt>200:
                            h_pfcand_nextracks_afterWLeptonicPt.Fill(pfcand_nextracks,pileupw)

    #xi = {"2023227392":[],"1981284352":[],"2070937600":[],"2040004608":[],"1998061568":[],"2054160384":[]}
    xi = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[]}
    passesPPS=False
    if DATA and e.num_jets_ak4<1 and e.num_bjets_ak8 < 1:
        crossingAngle=crossAngleDict['{0}:{1}'.format(run,lumi)]
        passesPPS=passPPS(e,xi,float(crossingAngle))
        if passesPPS:
            h_pfcand_nextracks_after_jet_veto_PPS.Fill(pfcand_nextracks,pileupw)
            if jet_pruning:
                h_pfcand_nextracks_after_jet_veto_jet_pruning_PPS.Fill(pfcand_nextracks,pileupw)
                if not (dphiWW>2.5 and recoMWW>500 and (recoMWhad>40 and recoMWhad<120) and MET>40 and WLeptonicPt>200):
                    h_pfcand_nextracks_after_jet_veto_jet_pruning_veto_signal_PPS.Fill(pfcand_nextracks,pileupw)
                if not (dphiWW>2.5 and (recoMWhad>40 and recoMWhad<120) and MET>40 and WLeptonicPt>200):
                    M_RP=m.sqrt(169000000*xi["23"][0]*xi["123"][0])
                    h_mass_cms_vs_rp.Fill(M_RP,recoMWW)
            #plot extra tracks after jet veto
            #plot extra tracks after jet veto and pruning cuts
            #plot extra tracks after all cuts, blind <10 extra tracks
            #compare Xicms vs. Xi_RP in background region, so 

fout.Write()
fout.Close()
print fout
print("--- %s seconds ---" % (time.time() - start_time))
