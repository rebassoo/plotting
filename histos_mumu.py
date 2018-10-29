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
if sample_name == "MuonEG" or sample_name =="DoubleMuon":
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

#files = [f for f in listdir('.') if isfile(f)]
#for f in files:
    #print f

count_1_15_tracks=0
count_zero_tracks=0
num_events=0
Num_event_cut_0=0
Num_event_cut_1=0
Num_event_cut_2=0
Num_event_cut_3=0
for file in ListOfFiles:
    i=i+1
    #print file
    chain.Add(file)
    entries=chain.GetEntries()
    #print entries
    f=TFile(file)
    h=TH1F()
    h=f.Get("demo/h_trueNumInteractions")
    #print h.GetEntries()
    num_events=num_events+h.GetEntries()
    #t=TTree()
    #t=f.Get("demo/SlimmedNtuple")
    #for e in t:
    #    if e.lumiblock == 1700:
    #        if e.run == 279841:
    #            print file
    #if i > 5:
    #    break

fout.cd()
print "Number of events: {0}".format(num_events)
#sys.exit()

print("--- %s seconds ---" % (time.time() - start_time))

h_muon1_pt=TH1F("h_muon1_pt",";p_{T} (#mu) [GeV];",100,0,500)
h_muon2_pt=TH1F("h_muon2_pt",";p_{T} (#mu) [GeV];",100,0,500)

h_muon1_pt_Zmass=TH1F("h_muon1_pt_Zmass",";p_{T} (#mu) [GeV];",100,0,500)
h_muon2_pt_Zmass=TH1F("h_muon2_pt_Zmass",";p_{T} (#mu) [GeV];",100,0,500)

h_muon1_iso_Zmass=TH1F("h_muon1_iso_Zmass",";Iso (#mu) [GeV];",50,0,1)
h_muon2_iso_Zmass=TH1F("h_muon2_iso_Zmass",";Iso (#mu) [GeV];",50,0,1)

h_muon1_dxy_Zmass=TH1F("h_muon1_dxy_Zmass",";dxy [cm];",100,0,5)
h_muon2_dxy_Zmass=TH1F("h_muon2_dxy_Zmass",";dxy [cm];",100,0,5)

h_muon1_dz_Zmass=TH1F("h_muon1_dz_Zmass",";dz [cm];",100,0,5)
h_muon2_dz_Zmass=TH1F("h_muon2_dz_Zmass",";dz [cm];",100,0,5)

h_eta1_minus_eta2=TH1F("h_eta1_minus_eta2",";|#eta_{1}-#eta_{2}|;",100,0,5)
h_phi1_minus_phi2=TH1F("h_phi1_minus_phi2",";|#phi_{1}-#phi_{2}|;",100,0,6.5)

h_muon1_pt_g110=TH1F("h_muon1_pt_g110",";p_{T} (#mu) [GeV];",100,0,500)
h_muon2_pt_g110=TH1F("h_muon2_pt_g110",";p_{T} (#mu) [GeV];",100,0,500)

h_muon_pt=TH1F("h_muon_pt",";p_{T} (#mu) [GeV];",100,0,500)
h_muon_eta=TH1F("h_muon_eta",";#eta_{#mu};",60,-3,3)
h_e_pt=TH1F("h_e_pt",";p_{T} (e) [GeV];",100,0,500)
h_e_eta=TH1F("h_e_eta",";#eta_{e};",60,-3,3)
h_chi2=TH1F("h_chi2",";#chi^{2}/ndof;",100,0,50)

h_mass_nofvtx=TH1F("h_mass_nofvtx",";Mass [GeV];",100,0,1000)
h_mass=TH1F("h_mass",";Mass [GeV];",100,0,1000)
h_ptemu=TH1F("h_ptemu",";p_{T} (e#mu) [GeV];",100,0,1000)
h_num_tracks=TH1F("h_num_tracks",";Num Extra Tracks at vertex;",15,-0.5,14.5)
#h_num_ftracks=TH1F("h_num_ftracks",";Num Extra Tracks at vertex;",100,-0.5,99.5)
h_num_vertices=TH1F("h_num_vertices",";Num vertices;",100,-0.5,99.5)
h_z_vertex=TH1F("h_z_vertex",";z vertex [cm];",120,-15,15)

#h_vtx_numtracks=TH1F("h_vtx_numtracks",";Num Extra Tracks at vertex;",15,-0.5,14.5)
h_fvtx_numtracks_Leptons=TH1F("h_fvtx_numtracks_Leptons",";Num Extra Tracks at vertex;",85,-0.5,84.5)
h_fvtx_numtracks_Leptons_PPS=TH1F("h_fvtx_numtracks_Leptons_PPS",";Num Extra Tracks at vertex;",85,-0.5,84.5)
h_fvtx_numtracks_Leptons_pt_0_30=TH1F("h_fvtx_numtracks_Leptons_pt_0_30",";Num Extra Tracks at vertex;",85,-0.5,84.5)
h_fvtx_numtracks_Leptons_0jets=TH1F("h_fvtx_numtracks_Leptons_0jets",";Num Extra Tracks at vertex;",85,-0.5,84.5)
h_fvtx_numtracks_Leptons_0jets_PPS=TH1F("h_fvtx_numtracks_Leptons_0jets_PPS",";Num Extra Tracks at vertex;",85,-0.5,84.5)
h_fvtx_mass=TH1F("h_fvtx_mass",";Mass [GeV];",50,0,500)
h_fvtx_ptemu=TH1F("h_fvtx_ptemu",";p_{T}(e#mu) [GeV];",20,0,300)
h_fvtx_mass_pt30=TH1F("h_fvtx_mass_pt30",";Mass [GeV];",50,0,500)
h_fvtx_ptemu_pt30=TH1F("h_fvtx_ptemu_pt30",";p_{T}(e#mu) [GeV];",20,0,200)
h_fvtx_ptemu_0tracks=TH1F("h_fvtx_ptemu_0tracks",";p_{T}(e#mu) [GeV];",20,0,300)

#h_tkdist_0tracks=TH1F("h_tkdist_0tracks",";Track distance (cm);",200,0,1)
#h_tkpt_0tracks=TH1F("h_tkpt_0tracks",";Track p_{T} [GeV];",200,0,100)
#h_tketa_0tracks=TH1F("h_tketa_0tracks",";Track #eta;",60,-3,3)

h_muon_dist=TH1F("h_muon_dist",";#mu distance to vertex (cm);",200,0,5)
h_electron_dist=TH1F("h_electron_dist",";e distance to vertex (cm);",200,0,5)
h_closest_track_ts=TH1F("h_closest_track_ts",";closest track to vertex (cm);",100,0,1)
h_closest_track_ts_0jets=TH1F("h_closest_track_ts_0jets",";closest track to vertex (cm);",100,0,1)
h_closest_track_cms=TH1F("h_closest_track_cms",";closest track to vertex (cm);",100,0,1)
#h_closest_track_15tracks=TH1F("h_closest_track_15tracks",";closest track to vertex (cm);",100,0,1)
#h_closest_track_ptemu30=TH1F("h_closest_track_ptemu30",";closest track to vertex (cm);",100,0,1)

h_muon_dist_vs_chi2=TH2F("h_muon_dist_vs_chi2","",200,0,20,200,0,5)
h_electron_dist_vs_chi2=TH2F("h_electron_dist_vs_chi2","",200,0,20,200,0,5)

#h_muon_dist_0tracks=TH1F("h_muon_dist_0tracks","",200,0,5)
#h_electron_dist_0tracks=TH1F("h_electron_dist_0tracks","",200,0,5)

#h_muon_pt_0tracks=TH1F("h_muon_pt_0tracks","",200,0,200)
#h_electron_pt_0tracks=TH1F("h_electron_pt_0tracks","",200,0,200)
#h_electron_pt_0tracks_closeTracks=TH1F("h_electron_pt_0tracks_closeTracks","",200,0,200)
#h_electron_pt_vs_dist_0tracks=TH2F("h_electron_pt_vs_dist_0tracks","",200,0,5,200,0,200)

#h_xi=TH2F("h_xi","",200,0,1,200,0,1)
h_dist_myVertex_pv=TH1F("h_dist_myVertex_pv","",80,0,2)
h_dist_myVertex_0tracks_ptemu30=TH1F("h_dist_myVertex_pv_0tracks_ptemu30","",80,0,2)

h_fvtx_ts_vs_cms_p5mm=TH2F("h_fvtx_ts_vs_cms_p5mm","",100,-0.5,99.5,100,-0.5,99.5)
h_closest_track_ts_vs_cms=TH2F("h_closest_track_ts_vs_cms","",100,0,1,100,0,1)

h_jets_25=TH1F("h_jets_25","Number of jets",15,-0.5,14.5)
h_jets_30=TH1F("h_jets_30","Number of jets",15,-0.5,14.5)
h_jets_30_15extraTracks=TH1F("h_jets_30_15extraTracks","Number of jets",15,-0.5,14.5)

h_jets_30_eta=TH1F("h_jets_30_eta","jet #eta",60,-3,3)
h_jets_30_phi=TH1F("h_jets_30_phi","jet #phi",60,2*3.14,3)
h_jets_30_ptemu30=TH1F("h_jets_30_ptemu30","Number of jets",15,-0.5,14.5)

h_xi_cms_vs_xi_RP_left=TH2F("h_xi_cms_vs_xi_RP_left","",1000,0,1,1000,0,1)
h_xi_cms_vs_xi_RP_right=TH2F("h_xi_cms_vs_xi_RP_right","",1000,0,1,1000,0,1)

h_M_cms_vs_M_RP=TH2F("h_M_cms_vs_M_RP","",9000,0,3000,9000,0,3000)
h_Y_cms_vs_Y_RP=TH2F("h_Y_cms_vs_Y_RP","",640,-4,4,640,-4,4)

h_fvtx_numtracks_Leptons_ptmumu30=TH1F("h_fvtx_numtracks_Leptons_ptmumu30",";Num Extra Tracks at vertex;",85,-0.5,84.5)

h_mass_bare=TH1F("h_mass_bare","",500,0,1000)
h_pt_mumu=TH1F("h_pt_mumu","",50,0,200)
h_mass_pt_mumu_60=TH1F("h_mass_pt_mumu_60","",500,0,1000)
h_pt_mumu_signal=TH1F("h_pt_mumu_signal","",50,0,200)
h_pt_mumu_background=TH1F("h_pt_mumu_background","",50,0,200)
h_missing_mass_background=TH1F("h_missing_mass_background","",120,0,3000)
h_missing_mass_signal=TH1F("h_missing_mass_signal","",120,0,3000)
h_missing_mass_background_noPtMuMuCut=TH1F("h_missing_mass_background_noPtMuMuCut","",120,0,3000)
h_missing_mass_signal_noPtMuMuCut=TH1F("h_missing_mass_signal_noPtMuMuCut","",120,0,3000)
h_missing_mass_background_80=TH1F("h_missing_mass_background_80","",120,0,3000)
h_missing_mass_signal_80=TH1F("h_missing_mass_signal_80","",120,0,3000)

h_missing_mass_background_Mass50=TH1F("h_missing_mass_background_Mass50","",120,0,3000)
h_missing_mass_background_80_Mass50=TH1F("h_missing_mass_background_80_Mass50","",120,0,3000)

h_missing_mass_background_diego=TH1F("h_missing_mass_background_diego","",120,0,3000)
h_missing_mass_signal_diego=TH1F("h_missing_mass_signal_diego","",120,0,3000)

h_xi_background_45=TH1F("h_xi_background_45","",100,0,1)
h_xi_background_56=TH1F("h_xi_background_56","",100,0,1)
h_xi_signal_45=TH1F("h_xi_signal_45","",100,0,1)
h_xi_signal_56=TH1F("h_xi_signal_56","",100,0,1)


runPPSCuts=False

count_zero=0
count_one=0
count_two=0
it=0
run=0.
event=0.
Num_events_cut_0=0
Num_events_cut_1=0
Num_events_cut_2=0
Num_events_cut_3=0
Num_events_cut_4=0
Num_events_cut_5=0
print "Chain get Entries: ",chain.GetEntries()

crossAngleDict=GetCrossingAngles()
#print crossAngleDict

for e in chain:
    it=it+1
    Num_events_cut_0=Num_events_cut_0+1
    #run=300576#, Lumi: 115, Event: 116170160
    #event=506844112
    #if run == e.run and event == e.event:
    #    #continue
    #    print "Got to proper event"
    #else:
    #    continue
    #if e.lumiblock != 1700:
    #    continue
    Num_events_cut_1=Num_events_cut_1+1
    run=e.run
    event=e.event
    lumi=e.lumiblock
    #pileupw=e.pileupWeight
    pileupw=1.
    #print "run, lumi event: {0}, {1}, {2}".format(run,e.lumiblock,event)
    #if e.fvertex_chi2ndof:
    #    print e.fvertex_chi2ndof

    #if it > 100:
    #    break
    c = dict.fromkeys(["twoLeptons","iMass","oppCharge","fittedVertexPassRequirements","fittedVertexTracks15","fittedVertexTracks0","ptemug30","ptemul30","passesPPS"],False)
    numMuHighPt=0
    numEHighPt=0
    mass=0
    rapidity=0
    ptemu=0
    dist_myvtx_pv=0
    closest_track_ts=1000
    closest_track_cms=1000
    acopl=-999.
    xi_cms_1=-999.
    xi_cms_2=-999.
    lcombined=TLorentzVector()
    #if e.muon_pt.size()+e.electron_pt.size() > 2:
    #    #print "Event has 3 good leptons, skip"
    #    continue

    imu=0
    lepton_count=0
    muon_pt_high=0
    muon_pt_low=10000
    if e.muon_pt.size() > 2:
        continue
    for muon_pt in e.muon_pt:
        #print "Muon pt: {0}".format(muon_pt)
        #if e.muon_dxy[imu]<0.2 and e.muon_dz[imu]<0.5:
        lepton_count=lepton_count+1
        if muon_pt>35 and e.muon_iso[imu]<0.15:
            numMuHighPt=numMuHighPt+1
        if muon_pt > muon_pt_high:
            muon_pt_high=muon_pt
        if muon_pt < muon_pt_low:
            muon_pt_low=muon_pt
        imu=imu+1
            
    h_muon1_pt.Fill(muon_pt_high)
    h_muon2_pt.Fill(muon_pt_low)    
    ie=0
    for e_pt in e.electron_pt:
        #print "Electron pt: {0}".format(muon_pt)
        lepton_count=lepton_count+1
        #if e_pt>40 and e.electron_passip[ie]:
        if e_pt>40:
            numEHighPt=numEHighPt+1
        ie=ie+1

    if lepton_count > 2:
        continue

    fvertex_numtracks=1000
    numCloseLeptons=0
    #if( numMuHighPt==1 and numEHighPt==1 ):
    #if( numMuHighPt==2 and numEHighPt==0 ):
    #if( numMuHighPt>1):
    if( numMuHighPt==2):
        Num_events_cut_2=Num_events_cut_2+1
        if e.fvertex_chi2ndof < 10 and abs(e.fvertex_z) < 15:
            c["fittedVertexPassRequirements"]=True
            fvertex_numtracks=0
            #numCloseLeptons=e.fvertex_ntracks
            fvertex_numtracks=e.fvertex_ntracks_ts_p5mm
            #fvertex_numtracks=e.fvertex_ntracks_cms_p5mm
            #for tkdist in e.fvertex_tkdist:
            #    if tkdist < 0.05:
            #        fvertex_numtracks=fvertex_numtracks+1
            if fvertex_numtracks < 15:
                c["fittedVertexTracks15"]=True
            if fvertex_numtracks < 1:
                c["fittedVertexTracks0"]=True

        c["twoLeptons"]=True
        l1 = TLorentzVector(e.muon_px[0],e.muon_py[0],e.muon_pz[0],e.muon_e[0])
        #print "l1 px: {0} py: {1} pz: {2}, E: {3}".format(e.muon_px[0],e.muon_py[0],e.muon_pz[0],e.muon_e[0])
        l2 = TLorentzVector(e.muon_px[1],e.muon_py[1],e.muon_pz[1],e.muon_e[1])
        #print "l2 px: {0} py: {1} pz: {2}, E: {3}".format(e.muon_px[1],e.muon_py[1],e.muon_pz[1],e.muon_e[1])
        lcombined=l1+l2
        #xi_cms_1=lcombined.M()/m.sqrt(13000.*13000.*m.exp(2*lcombined.Rapidity()))
        #xi_cms_2=xi_cms_1*m.exp(2*lcombined.Rapidity())
        #This is towards +45
        xi_cms_1=(e.muon_pt[0]*m.exp(e.muon_eta[0])+e.muon_pt[1]*m.exp(e.muon_eta[1])) / (13000.)
        #print xi_cms_1
        #This is towards +56
        xi_cms_2=(e.muon_pt[0]*m.exp(-e.muon_eta[0])+e.muon_pt[1]*m.exp(-e.muon_eta[1])) / (13000.)
        #print xi_cms_2
        #print "Phi1, Phi2: ",e.muon_phi[0]," ",e.muon_phi[1]
        dphi=GetDphi(e.muon_phi[0],e.muon_phi[1])
        acopl=1. - abs(dphi/m.pi)
        #print lcombined.M()
        rapidity=lcombined.Rapidity()
        if lcombined.M() > 50: 
            c["iMass"] = True
            Num_events_cut_3=Num_events_cut_3+1
        coshf = m.cosh(e.muon_eta[0]-e.muon_eta[1])
        cosf = m.cos(e.muon_phi[0]-e.muon_phi[1])
        mass_squared = 2*e.muon_pt[0]*e.muon_pt[1]*(coshf-cosf)
        if e.muon_charge[0] * e.muon_charge[1] < 0: 
            c["oppCharge"]=True
            Num_events_cut_4=Num_events_cut_4+1
        if c["fittedVertexPassRequirements"]==True:
            Num_events_cut_5=Num_events_cut_5+1
        mass=lcombined.M()
        #print "Mass: ",mass
        #print "Mass squared ",m.sqrt(mass_squared)
        ptemu=lcombined.Pt()
        if ptemu > 30:
            c["ptemug30"]=True
        #for tkdist in e.fvertex_tkdist:
        #    if tkdist < closest_track:
        #        closest_track=tkdist
        closest_track_ts=e.fvertex_closest_trk_ts
        closest_track_cms=e.fvertex_closest_trk_cms

    #Old vertexing plot
    if c["twoLeptons"] and c["iMass"] and c["oppCharge"] and e.vertex_ntracks<17 and abs(e.vertex_z) < 15 and c["ptemug30"]: 
        h_num_tracks.Fill(e.vertex_ntracks-2,pileupw)

    #Plot before chi2 and z requirement of vertex
    if c["twoLeptons"] and c["iMass"] and c["oppCharge"] and abs(e.fvertex_z) < 15: 
        h_chi2.Fill(e.fvertex_chi2ndof,pileupw)

    #Plots with no fitted vertex
    if c["twoLeptons"] and mass > 70 and mass < 110 and c["oppCharge"]:                
        h_muon1_pt_Zmass.Fill(e.muon_pt[0],pileupw)            
        h_muon2_pt_Zmass.Fill(e.muon_pt[1],pileupw)            
        h_muon1_iso_Zmass.Fill(e.muon_iso[0],pileupw)            
        h_muon2_iso_Zmass.Fill(e.muon_iso[1],pileupw)            
        h_muon1_dxy_Zmass.Fill(e.muon_dxy[0],pileupw)                    
        h_muon2_dxy_Zmass.Fill(e.muon_dxy[1],pileupw)                    
        h_muon1_dz_Zmass.Fill(e.muon_dz[0],pileupw)                    
        h_muon2_dz_Zmass.Fill(e.muon_dz[1],pileupw)                    
        h_eta1_minus_eta2.Fill(abs(e.muon_eta[0]-e.muon_eta[1]))
        h_phi1_minus_phi2.Fill(abs(e.muon_phi[0]-e.muon_phi[1]))

    if c["twoLeptons"] and mass > 110 and c["oppCharge"]:                
        h_muon1_pt_g110.Fill(e.muon_pt[0],pileupw)            
        h_muon2_pt_g110.Fill(e.muon_pt[1],pileupw)            


    num_jets_25=0
    num_jets_30=0
    #Plots without any track requirements, but fitted vertex requirements
    if c["twoLeptons"] and c["fittedVertexPassRequirements"] and c["iMass"] and c["oppCharge"]:                
        #h_muon_dist.Fill(e.muon_tkdist[0],pileupw)
        #h_electron_dist.Fill(e.electron_tkdist[0],pileupw)
        #h_muon_dist_vs_chi2.Fill(e.fvertex_chi2ndof,e.muon_tkdist[0],pileupw)
        #h_electron_dist_vs_chi2.Fill(e.fvertex_chi2ndof,e.electron_tkdist[0],pileupw)
        dist_myvtx_pv=m.sqrt( (e.vertex_x-e.fvertex_x)*(e.vertex_x-e.fvertex_x) + (e.vertex_y-e.fvertex_y)*(e.vertex_y-e.fvertex_y) + (e.vertex_z-e.fvertex_z)*(e.vertex_z-e.fvertex_z) )
        h_dist_myVertex_pv.Fill(dist_myvtx_pv,pileupw)
        h_muon_pt.Fill(e.muon_pt[0],pileupw)            
        h_muon_eta.Fill(e.muon_eta[0],pileupw)
        h_e_pt.Fill(e.muon_pt[1],pileupw)
        h_e_eta.Fill(e.muon_eta[1],pileupw)
        h_mass.Fill(mass,pileupw)
        h_ptemu.Fill(ptemu,pileupw)
        h_num_vertices.Fill(e.vertex_nvtxs,pileupw)
        for z in e.allvertices_z:
            h_z_vertex.Fill(z,pileupw)
        h_jets_25.Fill(e.jet_pt.size(),pileupw)
        num_jets_25=e.jet_pt.size()
        jet_i=0
        for jet_pt in e.jet_pt:
            if jet_pt>30 and abs(e.jet_eta[jet_i])<2.4:
                num_jets_30=num_jets_30+1
                h_jets_30_eta.Fill(e.jet_eta[jet_i],pileupw)
                h_jets_30_phi.Fill(e.jet_phi[jet_i],pileupw)
            jet_i=jet_i+1
        h_jets_30.Fill(num_jets_30,pileupw)



    #Plot of closest track for ptemu>30, no tracking requirement
    if c["twoLeptons"] and c["fittedVertexPassRequirements"] and c["iMass"] and c["oppCharge"] and c["ptemug30"]:
        h_closest_track_ts.Fill(closest_track_ts,pileupw)
        h_closest_track_cms.Fill(closest_track_cms,pileupw)
        h_closest_track_ts_vs_cms.Fill(closest_track_cms,closest_track_ts,pileupw)
        h_fvtx_ts_vs_cms_p5mm.Fill(e.fvertex_ntracks_cms_p5mm,e.fvertex_ntracks_ts_p5mm,pileupw)
        if num_jets_30 < 1:
            h_closest_track_ts_0jets.Fill(closest_track_ts,pileupw)
            h_fvtx_numtracks_Leptons_0jets.Fill(fvertex_numtracks,pileupw)
        h_fvtx_numtracks_Leptons_ptmumu30.Fill(fvertex_numtracks,pileupw)
        h_jets_30_ptemu30.Fill(num_jets_30,pileupw)

    if c["twoLeptons"] and c["fittedVertexPassRequirements"] and c["iMass"] and c["oppCharge"]:
        h_fvtx_numtracks_Leptons.Fill(fvertex_numtracks,pileupw)

    #All plots below here have less than 15 extra tracks at the vertex

    #Looking at extra tracks <15, no ptemu requirement. Also, does pass PPS requirements
    xi = {"2023227392":[],"1981284352":[],"2070937600":[],"2040004608":[],"1998061568":[],"2054160384":[]}
    #if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and c["fittedVertexTracks15"]:
    if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"]:
        h_fvtx_mass.Fill(mass,pileupw)
        h_fvtx_ptemu.Fill(ptemu,pileupw)
        if DATA:
            #xi = dict.fromkeys(["2","3","102","103"],[])
            crossingAngle=crossAngleDict['{0}:{1}'.format(run,lumi)]
            #print float(crossingAngle)
            c["passesPPS"]=passPPS(e,xi,float(crossingAngle))

    if c["twoLeptons"] and c["oppCharge"]:
        h_mass_bare.Fill(mass)
        if mass > 50:
            h_pt_mumu.Fill(ptemu)
        if ptemu > 60:
            h_mass_pt_mumu_60.Fill(mass)

    #Plot pixels and signal region
    if c["passesPPS"] and c["twoLeptons"] and c["oppCharge"] and mass < 94 and mass > 88:
        h_pt_mumu_signal.Fill(ptemu)
        if xi["2023227392"][0] > 0 or xi["2040004608"][0] > 0:
            print "One of the xi values is positive"
            print xi["2023227392"][0]
            print xi["2040004608"][0]
        if (xi["2023227392"][0]*xi["2040004608"][0]) > 0:
            proton_pz_45=6500*abs(xi["2023227392"][0])
            proton_pz_56=6500*abs(xi["2040004608"][0])
            h_xi_signal_45.Fill(abs(xi["2023227392"][0]))
            h_xi_signal_56.Fill(abs(xi["2040004608"][0]))
            proton_4vector_45=TLorentzVector(0.,0.,proton_pz_45,proton_pz_45)
            proton_4vector_56=TLorentzVector(0.,0.,-proton_pz_56,proton_pz_56)
            proton_combined=proton_4vector_45+proton_4vector_56
            proton_Z_combined=proton_combined-lcombined
            missing_mass=proton_Z_combined.M()
            h_missing_mass_signal_noPtMuMuCut.Fill(missing_mass)
            if ptemu > 60:
                #proton_4vector_mass=m.sqrt(169000000*xi["2023227392"][0]*xi["2040004608"][0])
                #missing_mass=proton_4vector_mass-lcombined.M()
                h_missing_mass_signal.Fill(missing_mass)
                ECM=13000.0
                #print "Signal"
                proton1_pz=6500-proton_pz_45
                proton2_pz=-6500+proton_pz_56
                #missing_mass_diego=m.sqrt((ECM-(lcombined.M()+abs(proton1_pz)+abs(proton2_pz)))*(ECM-(lcombined.M()+abs(proton1_pz)+abs(proton2_pz)))-(lcombined.Px())*(lcombined.Px())-(lcombined.Py())*(lcombined.Py())- (lcombined.Pz()+proton1_pz+proton2_pz)*(lcombined.Pz()+proton1_pz+proton2_pz));
                #h_missing_mass_signal_diego.Fill(missing_mass_diego)
                if ptemu > 80:
                    h_missing_mass_signal_80.Fill(missing_mass)
        else:
            print "One of the xi values is greater than 0 for signal"
            print "Xi values 2023227392: ",xi["2023227392"][0]
            print "Xi values 2040004608: ",xi["2040004608"][0]

    if c["passesPPS"] and c["twoLeptons"] and c["oppCharge"] and ( mass > 94 or mass < 88) and mass > 20:
        h_pt_mumu_background.Fill(ptemu)
        if xi["2023227392"][0] > 0 or xi["2040004608"][0] > 0:
            print "One of the xi values is positive"
            print xi["2023227392"][0]
            print xi["2040004608"][0]
        
        if (xi["2023227392"][0]*xi["2040004608"][0]) > 0:

            h_xi_background_45.Fill(abs(xi["2023227392"][0]))
            h_xi_background_56.Fill(abs(xi["2040004608"][0]))

                #proton_4vector_mass=m.sqrt(169000000*xi["2023227392"][0]*xi["2040004608"][0])
                #missing_mass=proton_4vector_mass-lcombined.M()
            proton_pz_45=6500-6500*abs(xi["2023227392"][0])
            proton_pz_56=6500-6500*abs(xi["2040004608"][0])
            proton_4vector_45=TLorentzVector(0.,0.,proton_pz_45,proton_pz_45)
            proton_4vector_56=TLorentzVector(0.,0.,-proton_pz_56,proton_pz_56)
            proton_combined=proton_4vector_45+proton_4vector_56
            proton_proton_cms=TLorentzVector(0.,0.,0.,13000)
            proton_Z_combined=proton_proton_cms-proton_combined-lcombined
            missing_mass=proton_Z_combined.M()
            
            proton_pz_45_2=6500*abs(xi["2023227392"][0])
            proton_pz_56_2=6500*abs(xi["2040004608"][0])
            proton_4vector_45_2=TLorentzVector(0.,0.,proton_pz_45_2,proton_pz_45_2)
            proton_4vector_56_2=TLorentzVector(0.,0.,-proton_pz_56_2,proton_pz_56_2)
            proton_combined2=proton_4vector_45_2+proton_4vector_56_2
            proton_Z_combined2=proton_combined2-lcombined
            missing_mass2=proton_Z_combined2.M()
            #print xi["2023227392"][0]
            #print xi["2040004608"][0]
            #print "proton_4vector_45_2, px: {0} py: {1} pz: {2}, E: {3}".format(proton_4vector_45_2.Px(),proton_4vector_45_2.Py(),proton_4vector_45_2.Pz(),proton_4vector_45_2.E())
            #print "proton_4vector_56_2, px: {0} py: {1} pz: {2}, E: {3}".format(proton_4vector_56_2.Px(),proton_4vector_56_2.Py(),proton_4vector_56_2.Pz(),proton_4vector_56_2.E())
            #print "proton_combined2, px: {0} py: {1} pz: {2}, E: {3}".format(proton_combined2.Px(),proton_combined2.Py(),proton_combined2.Pz(),proton_combined2.E())
            #print "proton_Z_combined2, px: {0} py: {1} pz: {2}, E: {3}".format(proton_Z_combined2.Px(),proton_Z_combined2.Py(),proton_Z_combined2.Pz(),proton_Z_combined2.E())
            #print missing_mass
            #print missing_mass2
            h_missing_mass_background_noPtMuMuCut.Fill(missing_mass)
            if ptemu > 60:                
                h_missing_mass_background.Fill(missing_mass)
                ECM=13000.0
                proton1_pz=6500.-proton_pz_45_2
                proton2_pz=-6500.+proton_pz_56_2
                #print proton1_pz
                #print proton2_pz
                #missing_mass_diego=m.sqrt((ECM-(lcombined.E()+abs(proton1_pz)+abs(proton2_pz)))*(ECM-(lcombined.E()+abs(proton1_pz)+abs(proton2_pz)))-(lcombined.Px())*(lcombined.Px())-(lcombined.Py())*(lcombined.Py())- (lcombined.Pz()+proton1_pz+proton2_pz)*(lcombined.Pz()+proton1_pz+proton2_pz));
                #h_missing_mass_background_diego.Fill(missing_mass_diego)
                #print "missing mass background: ",missing_mass
                #print "missing mass background 2: ",missing_mass2
                #print "missing mass background Diego: ",missing_mass_diego
                if mass > 50:
                    h_missing_mass_background_Mass50.Fill(missing_mass)
                if ptemu > 80:
                    h_missing_mass_background_80.Fill(missing_mass)
                    if mass > 50:
                        h_missing_mass_background_80_Mass50.Fill(missing_mass)
        else:
            print "One of the xi values is greater than 0 for background"
            print "Xi values 2023227392: ",xi["2023227392"][0]
            print "Xi values 2040004608: ",xi["2040004608"][0]

    #Plotting zero tracks and no ptemu requirement
    if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and c["fittedVertexTracks0"]:
        h_fvtx_ptemu_0tracks.Fill(ptemu,pileupw)

    #Plotting zero tracks and ptemu>30 requirement
    if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and c["fittedVertexTracks0"] and c["ptemug30"]:
        h_dist_myVertex_0tracks_ptemu30.Fill(dist_myvtx_pv,pileupw)

        
    #Plotting ptem<30 for number tracks less than 15
    if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and c["fittedVertexTracks15"] and c["ptemul30"]:
        h_fvtx_numtracks_Leptons_pt_0_30.Fill(fvertex_numtracks,pileupw)

    #Plotting ptemu>30, number tracks <15
    if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and c["fittedVertexTracks15"] and c["ptemug30"]:
        h_fvtx_mass_pt30.Fill(mass,pileupw)
        h_fvtx_ptemu_pt30.Fill(ptemu,pileupw)
        h_jets_30_15extraTracks.Fill(num_jets_30,pileupw)
    
    #print xi["1981284352"][0]
    #print xi["1998061568"][0]
    #print xi_cms_1
    #print xi_cms_2
    #print mass/m.sqrt(13000.*13000.*m.exp(2*rapidity))  
    #xi_cms_1=mass/m.sqrt(13000.*13000.*m.exp(2*rapidity))  
    #print xi_cms_1*m.exp(2*rapidity)  
    #print fvertex_numtracks
    #print "Acopl: ",acopl
    #print "Mass: ",mass
    #print "c[twoLeptons]",c["twoLeptons"]
    #print "c[fittedVertexPassRequirements]",c["fittedVertexPassRequirements"]
    #print "c[passesPPS]",c["passesPPS"]

    if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and c["passesPPS"]:
        if fvertex_numtracks < 1 and acopl < 0.009 and mass > 110:
            #print "Run: {0}, Lumi: {1}, Event: {2}".format(run,e.lumiblock,event)
            #print xi["1981284352"][0]
            #print xi["1998061568"][0]
            #print xi_cms_1
            #print xi_cms_2
            if len(xi["1981284352"]) > 0:
                h_xi_cms_vs_xi_RP_left.Fill(abs(xi["1981284352"][0]),xi_cms_1)
                #print "Left Run: {0}, Lumi: {1}, Event: {2}".format(run,e.lumiblock,event)
                #print "RP xi: ",xi["1981284352"]
                #print "CMS xi: ",xi_cms_1
            if len(xi["1998061568"]) > 0:
                h_xi_cms_vs_xi_RP_right.Fill(abs(xi["1998061568"][0]),xi_cms_2)
                #print "Right Run: {0}, Lumi: {1}, Event: {2}".format(run,e.lumiblock,event)
                #print "RP xi: ",xi["1998061568"]
                #print "CMS xi: ",xi_cms_2
            #M_RP=m.sqrt(169000000*xi["1981284352"][0]*xi["1998061568"][0])
            #Y_RP=0.5*m.log(xi["1981284352"][0]/xi["1998061568"][0])
            #h_M_cms_vs_M_RP.Fill(M_RP,mass)
            #h_Y_cms_vs_Y_RP.Fill(Y_RP,rapidity)
            #print mass/m.sqrt(13000.*13000.*m.exp(2*rapidity))  
            #xi_cms_2=mass/m.sqrt(13000.*13000.*m.exp(2*rapidity))  
            #print xi_cms_2*m.exp(2*rapidity)  
            #if event == 116170160:
            #    break

    #Plots with PPS requirements, ptemu>30, number of tracks <15
    #if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and c["fittedVertexTracks15"] and c["ptemug30"] and c["passesPPS"]:
    if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and c["ptemug30"] and c["passesPPS"]:
        h_fvtx_numtracks_Leptons_PPS.Fill(fvertex_numtracks,pileupw)
        if num_jets_30 < 1:
            h_fvtx_numtracks_Leptons_0jets_PPS.Fill(fvertex_numtracks,pileupw) 
        if (fvertex_numtracks) > 0:
            count_1_15_tracks=count_1_15_tracks+1
        else:
            count_zero_tracks=count_zero_tracks+1

    #Printing out, ptemu > 30 for number tracks <7 passing PPS
    #if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and fvertex_numtracks < 6 and c["ptemug30"] and c["passesPPS"]:
        #print "Run: {0}, Lumi: {1}, Event: {2}".format(run,e.lumiblock,event)
        #print "Num extra tracks: {0}, ptemu: {1}".format(fvertex_numtracks,ptemu)
        #print "Num jets: ADD THIS"
        #print "Xi_2:",xi["2"],"Xi_3:",xi["3"],"Xi_102:",xi["102"],"Xi_103:",xi["103"]
        #print "Chi2_ndof: {0}".format(e.fvertex_chi2ndof)
        #print "Closest track: {0}".format(closest_track_ts)
        #print "My vertex fit position x, y, z: {0},{1},{2}".format(e.fvertex_x,e.fvertex_y,e.fvertex_z)
        #print "Primary vertex fit position x, y, z: {0},{1},{2}".format(e.vertex_x,e.vertex_y,e.vertex_z)
        #print "Primary vertex extra tracks: {0}".format(e.vertex_ntracks-2)
        #print "Number of vertices in event: {0}".format(e.vertex_nvtxs)
        #print "Muon pt: {0}".format(e.muon_pt[0])
        #print "Electron pt: {0}".format(e.electron_pt[0])
        

print "Num_events_cut_0: ",Num_events_cut_0 
print "Num_events_cut_1: ",Num_events_cut_1 
print "Num_events_cut_2: ",Num_events_cut_2 
print "Num_events_cut_3: ",Num_events_cut_3 
print "Num_events_cut_4: ",Num_events_cut_4 
print "Num_events_cut_5: ",Num_events_cut_5 

print "Total number of data in 1-15 extra tracks bin, PPS: {0}".format(count_1_15_tracks)
print "Total number of data in 0 extra tracks bin, PPS: {0}".format(count_zero_tracks)
fout.Write()
fout.Close()
print fout
print("--- %s seconds ---" % (time.time() - start_time))
