#!/usr/bin/env python
#Finn Rebassoo, LLNL 12-01-2016
from os import listdir
from os.path import isfile, join
from ROOT import *
import math as m
from tools import *
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

#fout = TFile(dir+set_name+'.root','recreate')
output_name=sample_name
DATA=False
if sample_name == "MuonEG":
    DATA=True
    if file_dir =="crab_runBv3/170703_221255/0001":
        output_name="MuonEG_{0}_2nd".format(file_dir.split('/')[0].split('_')[1])
    else:
        output_name="MuonEG_{0}".format(file_dir.split('/')[0].split('_')[1])
    
fout = TFile('histos/{0}.root'.format(output_name),'recreate')
#fout = TFile('{0}.root'.format(sample_name),'recreate')
fout.cd()

#Chain together root files for data
mypath="/hadoop/cms/store/user/rebassoo/{0}/{1}/".format(sample_name,file_dir)
#mypath="/home/users/rebassoo/work/2017_04_19_LoopOverNtupleEmu/test/"
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
    #if i > 1:
    #    break

#chain.Add("/hadoop/cms/store/user/rebassoo/MuonEG/crab_runG/170627_232652/0000/SlimmedNtuple_599.root")

fout.cd()
print "Number of events: {0}".format(num_events)
#sys.exit()

print("--- %s seconds ---" % (time.time() - start_time))

#c1=TCanvas("c1","",800,600)

#Define all the histos to make
#h=TH2F("h","",200,0,1,200,0,1)
#h_numV=TH1F("h_numV","",100,-0.5,99.5)
#h_pvz=TH1F("h_pvz","",300,-15,15)
h_muon_pt=TH1F("h_muon_pt",";p_{T} (#mu) [GeV];",200,0,200)
h_muon_eta=TH1F("h_muon_eta",";#eta_{#mu};",60,-3,3)
h_e_pt=TH1F("h_e_pt",";p_{T} (e) [GeV];",100,0,200)
h_e_eta=TH1F("h_e_eta",";#eta_{e};",60,-3,3)

h_mass=TH1F("h_mass",";Mass [GeV];",100,0,1000)
h_ptemu=TH1F("h_ptemu",";p_{T} (e#mu) [GeV];",100,0,1000)
h_num_tracks=TH1F("h_num_tracks",";Num Extra Tracks at vertex;",100,-0.5,99.5)
h_num_ftracks=TH1F("h_num_ftracks",";Num Extra Tracks at vertex;",100,-0.5,99.5)
h_num_vertices=TH1F("h_num_vertices",";Num vertices;",100,-0.5,99.5)

h_vtx_numtracks=TH1F("h_vtx_numtracks",";Num Extra Tracks at vertex;",15,-0.5,14.5)
h_fvtx_numtracks_Leptons=TH1F("h_fvtx_numtracks_Leptons",";Num Extra Tracks at vertex;",15,-0.5,14.5)
h_fvtx_numtracks_Leptons_PPS=TH1F("h_fvtx_numtracks_Leptons_PPS",";Num Extra Tracks at vertex;",15,-0.5,14.5)
h_fvtx_numtracks_Leptons_pt_0_30=TH1F("h_fvtx_numtracks_Leptons_pt_0_30",";Num Extra Tracks at vertex;",15,-0.5,14.5)
h_fvtx_mass=TH1F("h_fvtx_mass",";Mass [GeV];",50,0,500)
h_fvtx_ptemu=TH1F("h_fvtx_ptemu",";p_{T}(e#mu) [GeV];",20,0,200)
h_fvtx_mass_pt30=TH1F("h_fvtx_mass_pt30",";Mass [GeV];",50,0,500)
h_fvtx_ptemu_pt30=TH1F("h_fvtx_ptemu_pt30",";p_{T}(e#mu) [GeV];",20,0,200)
h_fvtx_ptemu_0tracks=TH1F("h_fvtx_ptemu_0tracks",";p_{T}(e#mu) [GeV];",20,0,200)

h_tkdist_0tracks=TH1F("h_tkdist_0tracks",";Track distance (cm);",200,0,1)
h_tkpt_0tracks=TH1F("h_tkpt_0tracks",";Track p_{T} [GeV];",200,0,100)
h_tketa_0tracks=TH1F("h_tketa_0tracks",";Track #eta;",60,-3,3)

h_muon_dist=TH1F("h_muon_dist",";#mu distance to vertex (cm);",200,0,5)
h_electron_dist=TH1F("h_electron_dist",";e distance to vertex (cm);",200,0,5)
h_closest_track=TH1F("h_closest_track",";closest track to vertex (cm);",200,0,1)

h_muon_dist_vs_chi2=TH2F("h_muon_dist_vs_chi2","",200,0,20,200,0,5)
h_electron_dist_vs_chi2=TH2F("h_electron_dist_vs_chi2","",200,0,20,200,0,5)

h_muon_dist_0tracks=TH1F("h_muon_dist_0tracks","",200,0,5)
h_electron_dist_0tracks=TH1F("h_electron_dist_0tracks","",200,0,5)

h_muon_pt_0tracks=TH1F("h_muon_pt_0tracks","",200,0,200)
h_electron_pt_0tracks=TH1F("h_electron_pt_0tracks","",200,0,200)
h_electron_pt_0tracks_closeTracks=TH1F("h_electron_pt_0tracks_closeTracks","",200,0,200)
h_electron_pt_vs_dist_0tracks=TH2F("h_electron_pt_vs_dist_0tracks","",200,0,5,200,0,200)

h_xi=TH2F("h_xi","",200,0,1,200,0,1)

runPPSCuts=False

count_zero=0
count_one=0
count_two=0
it=0
run=0.
event=0.
for e in chain:
    it=it+1
    if run == e.run and event == e.event:
        continue
    run=e.run
    event=e.event
    #print "run, event: {0}, {1}".format(run,event)

    #if it > 100:
    #    break
    twoLeptons = False
    iMass = False
    tkdist_pair = False
    oppCharge = False
    vertexing = False
    vertexingNew = False
    numMuHighPt=0
    numEHighPt=0
    mass=0
    ptemu=0
    if e.muon_pt.size()+e.electron_pt.size() > 2:
        #print "Event has 3 good leptons, skip"
        continue
    
    for muon_pt in e.muon_pt:
        #print "Muon pt: {0}".format(muon_pt)
        if muon_pt>40:
            numMuHighPt=numMuHighPt+1

    for e_pt in e.electron_pt:
        #print "Electron pt: {0}".format(muon_pt)
        if e_pt>40:
            numEHighPt=numEHighPt+1

    #if( (numMuHighPt==1 and e.electron_pt.size()==1) or (numEHighPt==1 and e.muon_pt.size()==1)):
    passVertexRequirements=False
    fvertex_numtracks=1000
    numCloseLeptons=0
    if( numMuHighPt==1 and numEHighPt==1 and e.muon_tkdist.size() > 0 and e.electron_tkdist.size() > 0):
        if e.fvertex_chi2ndof < 10 and abs(e.fvertex_z) < 15:
            passVertexRequirements=True
            fvertex_numtracks=0
            numCloseLeptons=e.fvertex_ntracks
            for tkdist in e.fvertex_tkdist:
                if tkdist < 0.05:
                    fvertex_numtracks=fvertex_numtracks+1

        if passVertexRequirements ==True:
            twoLeptons=True
            l1 = TLorentzVector(e.muon_px[0],e.muon_py[0],e.muon_pz[0],e.muon_e[0])
            l2 = TLorentzVector(e.electron_px[0],e.electron_py[0],e.electron_pz[0],e.electron_e[0])
            lcombined=l1+l2
            xi_cms_1=lcombined.M()/m.sqrt(13000.*13000.*m.exp(2*lcombined.Rapidity()))
            xi_cms_2=xi_cms_1*m.exp(2*lcombined.Rapidity())
        #print lcombined.M()
            if lcombined.M() > 50: iMass = True
            h_muon_dist.Fill(e.muon_tkdist[0])
            h_electron_dist.Fill(e.electron_tkdist[0])
            if e.muon_tkdist[0] < 0.05 and e.electron_tkdist[0] < 0.05: tkdist_pair = True
            mass=lcombined.M()
            ptemu=lcombined.Pt()
        #print "Muon charge: {0}".format(e.muon_charge[0])
        #print "Electron charge: {0}".format(e.electron_charge[0])
            if e.muon_charge[0] * e.electron_charge[0] < 0: oppCharge=True
            if iMass and oppCharge:
                h_muon_pt.Fill(e.muon_pt[0])            
                h_muon_eta.Fill(e.muon_eta[0])
                h_e_pt.Fill(e.electron_pt[0])
                h_e_eta.Fill(e.electron_eta[0])
                h_mass.Fill(mass)
                h_ptemu.Fill(ptemu)
                h_num_tracks.Fill(e.vertex_ntracks-2)
                h_num_vertices.Fill(e.vertex_nvtxs)


    vertex_numtracks = e.vertex_ntracks

    if twoLeptons and oppCharge and iMass and vertex_numtracks < 15 and abs(e.vertex_z) < 15 and ptemu > 30:
        h_vtx_numtracks.Fill(e.vertex_ntracks-2)

    if twoLeptons and oppCharge and iMass:
        if (fvertex_numtracks-numCloseLeptons) == 0:
            if numCloseLeptons==0:
                count_zero=count_zero+1
            if numCloseLeptons==1:
                count_one=count_one+1
                for tkdist in e.fvertex_tkdist:
                    h_tkdist_0tracks.Fill(tkdist)
                for tkpt in e.fvertex_tkpt:
                    h_tkpt_0tracks.Fill(tkpt)
                for tketa in e.fvertex_tketa:
                    h_tketa_0tracks.Fill(tketa)
            if numCloseLeptons==2:
                count_two=count_two+1


    #Looking at extra tracks <17
    if twoLeptons and oppCharge and iMass and fvertex_numtracks < 17 and (tkdist_pair == True):
        lessthan6=False
        if fvertex_numtracks-numCloseLeptons < 6:
            lessthan6=True
        #PPS requirements
        left=False
        right=False
        passesPPS=False
        xi_left=[]
        xi_right=[]
        xi_2=[]
        xi_3=[]
        xi_102=[]
        xi_103=[]
        if DATA:
            i=0

            for detId_rp in e.rp_tracks_detId:
                    #print detId_rp
                if detId_rp == 2: 
                    left=True
                    #if lessthan6: print "DetId 2, Xi: {0}".format(e.rp_tracks_xi[i])
                    xi_2=e.rp_tracks_xi[i]
                if detId_rp == 3: 
                    left=True
                    #if lessthan6: print "DetId 3, Xi: {0}".format(e.rp_tracks_xi[i])
                    xi_3=e.rp_tracks_xi[i]
                if detId_rp == 102: 
                    right=True
                    #xi_right.append(float(e.rp_tracks_xi))
                    #if lessthan6: print "DetId 102, Xi: {0}".format(e.rp_tracks_xi[i])
                    xi_102=e.rp_tracks_xi[i]
                if detId_rp == 103: 
                    right=True
                    #xi_right.append(float(e.rp_tracks_xi))
                    #if lessthan6: print "DetId 103, Xi: {0}".format(e.rp_tracks_xi[i])
                    xi_103=e.rp_tracks_xi[i]
                i=i+1

        if (left == True) and (right == True):
            passesPPS=True
            if lessthan6 and ptemu > 30:
                print "Num extra tracks: {0}, ptemu: {1}".format(fvertex_numtracks-numCloseLeptons,ptemu)
                print "Xi_2:",xi_2,"Xi_3:",xi_3,"Xi_102:",xi_102,"Xi_103:",xi_103

        #Plotting zero tracks and no ptemu requirement
        if (fvertex_numtracks-numCloseLeptons) < 1:
            h_fvtx_ptemu_0tracks.Fill(ptemu)
            #if passesPPS:
            #    h_ftx_ptemu_0tracks_PPS.Fill(ptemu)
        
        #Plotting ptem<30 for number tracks <17
        if ptemu < 30:
             h_fvtx_numtracks_Leptons_pt_0_30.Fill(fvertex_numtracks-numCloseLeptons)

        h_fvtx_mass.Fill(mass)
        h_fvtx_ptemu.Fill(ptemu)
        if ptemu > 30:
            #Plot number of tracks
            h_fvtx_numtracks_Leptons.Fill(fvertex_numtracks-numCloseLeptons)
            h_fvtx_mass_pt30.Fill(mass)
            h_fvtx_ptemu_pt30.Fill(ptemu)

            #Plots with PPS requirements
            if passesPPS:
                for l in xi_left:
                    for r in xi_right:
                        #print e.rp_tracks_detId
                        #h_xi.Fill(xi_rp,xi_cms_1)
                        #h_xi.Fill(xi_rp,xi_cms_2)
                        h_xi.Fill(l,r)
                if (fvertex_numtracks-numCloseLeptons) > 0:
                    count_1_15_tracks=count_1_15_tracks+1
                    h_fvtx_numtracks_Leptons_PPS.Fill(fvertex_numtracks-numCloseLeptons)
                else:
                    count_zero_tracks=count_zero_tracks+1
                    h_fvtx_numtracks_Leptons_PPS.Fill(fvertex_numtracks-numCloseLeptons)


            #Looking for closest track to electron/muon
            #There is a problem with this line because tkdist and electron_tkdist not calculated the same
            closest_track=1000
            for tkdist in e.fvertex_tkdist:
                #There is a problem with this line because tkdist and electron_tkdist not calculated the same
                if tkdist < closest_track and tkdist != e.muon_tkdist[0] and tkdist != e.electron_tkdist[0]:
                    closest_track=tkdist
            h_closest_track.Fill(closest_track)

            #Looking at muon and electron track distance
            if e.muon_tkdist.size() > 0  and e.electron_tkdist.size() > 0:
                #h_muon_dist.Fill(e.muon_tkdist[0])
                #h_electron_dist.Fill(e.electron_tkdist[0])
                h_muon_dist_vs_chi2.Fill(e.fvertex_chi2ndof,e.muon_tkdist[0])
                h_electron_dist_vs_chi2.Fill(e.fvertex_chi2ndof,e.electron_tkdist[0])
                if (fvertex_numtracks-numCloseLeptons)==0:
                    h_muon_dist_0tracks.Fill(e.muon_tkdist[0])
                    h_electron_dist_0tracks.Fill(e.electron_tkdist[0])
                    h_muon_pt_0tracks.Fill(e.muon_tkpt[0])
                    h_electron_pt_0tracks.Fill(e.electron_tkpt[0])
                    h_electron_pt_vs_dist_0tracks.Fill(e.electron_tkdist[0],e.electron_tkpt[0])
            else:
                print "There is an issue with this event, tk dist size is 0"
                print "run, event: {0}, {1}".format(run,event)
                print "fvertex_numtracks: {0}".format(fvertex_numtracks)
            if (fvertex_numtracks-numCloseLeptons)==0:
                h_electron_pt_0tracks_closeTracks.Fill(e.electron_tkpt[0])


print "Total number of data in 1-15 extra tracks bin, PPS: {0}".format(count_1_15_tracks)
print "Total number of data in 0 extra tracks bin, PPS: {0}".format(count_zero_tracks)
fout.Write()
fout.Close()
print fout
print("--- %s seconds ---" % (time.time() - start_time))
