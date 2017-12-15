#!/usr/bin/env python
#Finn Rebassoo, LLNL 12-01-2016
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


start_time = time.time()
sample_name=sys.argv[1]
#sample_name="DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
print sample_name
file_dir=sys.argv[2]
#file_dir="crab_DY-50-up/170220_225226/0000/"
print file_dir

output_name=sample_name
DATA=False
if sample_name == "MuonEG":
    DATA=True
    if file_dir =="crab_runBv3/171116_215828/0001":
        output_name="MuonEG_{0}_2nd".format(file_dir.split('/')[0].split('_')[1])
    else:
        output_name="MuonEG_{0}".format(file_dir.split('/')[0].split('_')[1])
    
fout = TFile('histos/{0}.root'.format(output_name),'recreate')
fout.cd()

#Chain together root files for data
mypath="/hadoop/cms/store/user/rebassoo/{0}/{1}/".format(sample_name,file_dir)
ListOfFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
chain = TChain('demo/SlimmedNtuple')
i=0

files = [f for f in listdir('.') if isfile(f)]
#for f in files:
    #print f

count_1_15_tracks=0
count_zero_tracks=0
num_events=0
for file in ListOfFiles:
    i=i+1
    #print file
    chain.Add(mypath+file)
    entries=chain.GetEntries()
    f=TFile(mypath+file)
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
    #if i > 1:
    #    break

fout.cd()
print "Number of events: {0}".format(num_events)
#sys.exit()

print("--- %s seconds ---" % (time.time() - start_time))

h_muon_pt=TH1F("h_muon_pt",";p_{T} (#mu) [GeV];",100,0,500)
h_muon_eta=TH1F("h_muon_eta",";#eta_{#mu};",60,-3,3)
h_e_pt=TH1F("h_e_pt",";p_{T} (e) [GeV];",100,0,500)
h_e_eta=TH1F("h_e_eta",";#eta_{e};",60,-3,3)
h_chi2=TH1F("h_chi2",";#chi^{2}/ndof;",100,0,50)

h_mass=TH1F("h_mass",";Mass [GeV];",100,0,1000)
h_ptemu=TH1F("h_ptemu",";p_{T} (e#mu) [GeV];",100,0,1000)
h_num_tracks=TH1F("h_num_tracks",";Num Extra Tracks at vertex;",15,-0.5,14.5)
#h_num_ftracks=TH1F("h_num_ftracks",";Num Extra Tracks at vertex;",100,-0.5,99.5)
h_num_vertices=TH1F("h_num_vertices",";Num vertices;",100,-0.5,99.5)

#h_vtx_numtracks=TH1F("h_vtx_numtracks",";Num Extra Tracks at vertex;",15,-0.5,14.5)
h_fvtx_numtracks_Leptons=TH1F("h_fvtx_numtracks_Leptons",";Num Extra Tracks at vertex;",15,-0.5,14.5)
h_fvtx_numtracks_Leptons_PPS=TH1F("h_fvtx_numtracks_Leptons_PPS",";Num Extra Tracks at vertex;",15,-0.5,14.5)
h_fvtx_numtracks_Leptons_pt_0_30=TH1F("h_fvtx_numtracks_Leptons_pt_0_30",";Num Extra Tracks at vertex;",15,-0.5,14.5)
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

runPPSCuts=False

count_zero=0
count_one=0
count_two=0
it=0
run=0.
event=0.
print chain.GetEntries()
for e in chain:
    it=it+1
    if run == e.run and event == e.event:
        continue
    #if e.lumiblock != 1700:
    #    continue
    run=e.run
    event=e.event
    lumi=e.lumiblock
    pileupw=e.pileupWeight
    #print "run, lumi event: {0}, {1}, {2}".format(run,e.lumiblock,event)
    #if e.fvertex_chi2ndof:
    #    print e.fvertex_chi2ndof

    #if it > 100:
    #    break
    c = dict.fromkeys(["twoLeptons","iMass","oppCharge","fittedVertexPassRequirements","fittedVertexTracks15","fittedVertexTracks0","ptemug30","ptemul30","passesPPS"],False)
    numMuHighPt=0
    numEHighPt=0
    mass=0
    ptemu=0
    dist_myvtx_pv=0
    closest_track_ts=1000
    closest_track_cms=1000
    #if e.muon_pt.size()+e.electron_pt.size() > 2:
    #    #print "Event has 3 good leptons, skip"
    #    continue

    imu=0
    lepton_count=0
    for muon_pt in e.muon_pt:
        #print "Muon pt: {0}".format(muon_pt)
        #if e.muon_dxy[imu]<0.2 and e.muon_dz[imu]<0.5:
        lepton_count=lepton_count+1
        if muon_pt>40:
            numMuHighPt=numMuHighPt+1
        imu=imu+1
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
    if( numMuHighPt==1 and numEHighPt==1 ):
        if e.fvertex_chi2ndof < 10 and abs(e.fvertex_z) < 15:
            c["fittedVertexPassRequirements"]=True
            fvertex_numtracks=0
            #numCloseLeptons=e.fvertex_ntracks
            #This does count muon and electron
            fvertex_numtracks=e.fvertex_ntracks_ts_p5mm
            #for tkdist in e.fvertex_tkdist:
            #    if tkdist < 0.05:
            #        fvertex_numtracks=fvertex_numtracks+1
            if fvertex_numtracks < 15:
                c["fittedVertexTracks15"]=True
            if fvertex_numtracks < 1:
                c["fittedVertexTracks0"]=True

        c["twoLeptons"]=True
        l1 = TLorentzVector(e.muon_px[0],e.muon_py[0],e.muon_pz[0],e.muon_e[0])
        l2 = TLorentzVector(e.electron_px[0],e.electron_py[0],e.electron_pz[0],e.electron_e[0])
        lcombined=l1+l2
        xi_cms_1=lcombined.M()/m.sqrt(13000.*13000.*m.exp(2*lcombined.Rapidity()))
        xi_cms_2=xi_cms_1*m.exp(2*lcombined.Rapidity())
        #print lcombined.M()
        if lcombined.M() > 50: c["iMass"] = True
        if e.muon_charge[0] * e.electron_charge[0] < 0: c["oppCharge"]=True
        mass=lcombined.M()
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

    #Plots without any track requirements, but fitted vertex requirements
    if c["twoLeptons"] and c["fittedVertexPassRequirements"] and c["iMass"] and c["oppCharge"]:                
        h_muon_dist.Fill(e.muon_tkdist[0],pileupw)
        h_electron_dist.Fill(e.electron_tkdist[0],pileupw)
        h_muon_dist_vs_chi2.Fill(e.fvertex_chi2ndof,e.muon_tkdist[0],pileupw)
        h_electron_dist_vs_chi2.Fill(e.fvertex_chi2ndof,e.electron_tkdist[0],pileupw)
        dist_myvtx_pv=m.sqrt( (e.vertex_x-e.fvertex_x)*(e.vertex_x-e.fvertex_x) + (e.vertex_y-e.fvertex_y)*(e.vertex_y-e.fvertex_y) + (e.vertex_z-e.fvertex_z)*(e.vertex_z-e.fvertex_z) )
        h_dist_myVertex_pv.Fill(dist_myvtx_pv,pileupw)
        h_muon_pt.Fill(e.muon_pt[0],pileupw)            
        h_muon_eta.Fill(e.muon_eta[0],pileupw)
        h_e_pt.Fill(e.electron_pt[0],pileupw)
        h_e_eta.Fill(e.electron_eta[0],pileupw)
        h_mass.Fill(mass,pileupw)
        h_ptemu.Fill(ptemu,pileupw)
        h_num_vertices.Fill(e.vertex_nvtxs,pileupw)

    #Plot of closest track for ptemu>30, no tracking requirement
    if c["twoLeptons"] and c["fittedVertexPassRequirements"] and c["iMass"] and c["oppCharge"] and c["ptemug30"]:
        h_closest_track_ts.Fill(closest_track_ts,pileupw)
        h_closest_track_cms.Fill(closest_track_cms,pileupw)
        h_closest_track_ts_vs_cms.Fill(closest_track_cms,closest_track_ts,pileupw)
        h_fvtx_ts_vs_cms_p5mm.Fill(e.fvertex_ntracks_cms_p5mm,e.fvertex_ntracks_ts_p5mm,pileupw)
        
    #All plots below here have less than 15 extra tracks at the vertex

    #Looking at extra tracks <15, no ptemu requirement. Also, does pass PPS requirements
    xi = {"2":[],"3":[],"102":[],"103":[]}
    if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and c["fittedVertexTracks15"]:
        h_fvtx_mass.Fill(mass,pileupw)
        h_fvtx_ptemu.Fill(ptemu,pileupw)
        if DATA:
            #xi = dict.fromkeys(["2","3","102","103"],[])
            c["passesPPS"]=passPPS(e,xi)


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
        h_fvtx_numtracks_Leptons.Fill(fvertex_numtracks,pileupw)
        h_fvtx_mass_pt30.Fill(mass,pileupw)
        h_fvtx_ptemu_pt30.Fill(ptemu,pileupw)

    #Plots with PPS requirements, ptemu>30, number of tracks <15
    if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and c["fittedVertexTracks15"] and c["ptemug30"] and c["passesPPS"]:
        h_fvtx_numtracks_Leptons_PPS.Fill(fvertex_numtracks,pileupw)
        if (fvertex_numtracks) > 0:
            count_1_15_tracks=count_1_15_tracks+1
        else:
            count_zero_tracks=count_zero_tracks+1

    #Printing out, ptemu > 30 for number tracks <7 passing PPS
    if c["twoLeptons"] and c["oppCharge"] and c["iMass"] and c["fittedVertexPassRequirements"] and fvertex_numtracks < 6 and c["ptemug30"] and c["passesPPS"]:
        print "Run: {0}, Lumi: {1}, Event: {2}".format(run,e.lumiblock,event)
        print "Num extra tracks: {0}, ptemu: {1}".format(fvertex_numtracks,ptemu)
        print "Xi_2:",xi["2"],"Xi_3:",xi["3"],"Xi_102:",xi["102"],"Xi_103:",xi["103"]
        print "Chi2_ndof: {0}".format(e.fvertex_chi2ndof)
        print "Closest track: {0}".format(closest_track_ts)
        print "My vertex fit position x, y, z: {0},{1},{2}".format(e.fvertex_x,e.fvertex_y,e.fvertex_z)
        print "Primary vertex fit position x, y, z: {0},{1},{2}".format(e.vertex_x,e.vertex_y,e.vertex_z)
        print "Primary vertex extra tracks: {0}".format(e.vertex_ntracks-2)
        print "Number of vertices in event: {0}".format(e.vertex_nvtxs)
        print "Muon pt: {0}".format(e.muon_pt[0])
        print "Electron pt: {0}".format(e.electron_pt[0])
        

print "Total number of data in 1-15 extra tracks bin, PPS: {0}".format(count_1_15_tracks)
print "Total number of data in 0 extra tracks bin, PPS: {0}".format(count_zero_tracks)
fout.Write()
fout.Close()
print fout
print("--- %s seconds ---" % (time.time() - start_time))
