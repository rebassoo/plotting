#!/usr/bin/env python
#Finn Rebassoo, LLNL 02-03-2017
import math as m

def calcAco(phi1,phi2):
    result = phi1-phi2
    if result > m.pi : result = result-2*m.pi
    if result < m.pi : result = result+2*m.pi
    aco=1-result/m.pi
    return aco

def ModifyHisto(h,sample):
    #h.Scale(2.)
    #luminosity_fb=37.2
    #luminosity_fb=4.39
    #luminosity_fb=12.19
    #luminosity_fb=7.8
    #Runs BCG
    #luminosity_fb=15.9
    #Full run
    #luminosity_fb=35.8
    #Runs BCG
    #luminosity_fb=37.1
    #luminosity_fb=9.7
    luminosity_fb=37.5
    #Runs BG
    #luminosity_fb=13.8
    #luminosity_fb=13
    #This is luminosity without runD
    #luminosity_fb=32.8
    print sample
    #https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
    cross_section_pb=0
    numevents=0
    linecolor=0
    if sample =="ExclusiveWWNonElastic":
        #This cross section is from Doug's notes 92.83+/-0.10 for Madgraph 5.2.4.2. But this sample is only leptons so smaller cross section. Used %10.61 from Doug's notes. Should be 10.71% from 2014 PDG. 
        #numevents=5000
        numevents=50000
        #0.0098903 is value calculated in Madgraph and is in the file unweighted_events.lhe
        #This does no include elastic
        cross_section_pb=3.11*0.0098903
        #cross_section_pb=0.0098903
        #linecolor=8
        linecolor=429
    if sample =="ExclusiveWW":
        #This cross section is from Doug's notes 92.83+/-0.10 for Madgraph 5.2.4.2. But this sample is only leptons so smaller cross section. Used %10.61 from Doug's notes. Should be 10.71% from 2014 PDG. 
        #numevents=5000
        numevents=50000
        #0.0098903 is value calculated in Madgraph and is in the file unweighted_events.lhe
        #cross_section_pb=4.1*0.0098903
        cross_section_pb=0.0098903
        linecolor=7
    if sample =="WWTo2L2Nu_13TeV-powheg":
        #numevents=1999000
        #numevents=1236906
        #numevents=1162658
        #numevents=1206070
        numevents=1999000.0
        #From website above
        cross_section_pb=12.178
        linecolor=5
    if sample =="TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":
        numevents=6105137.
        #numevents=5865278
        #numevents=5997301
        #numevents=6055403
        #numevents=5967259.0
        #From UCSB table (3*0.108)^2*815.96
        cross_section_pb=85.66
        linecolor=4
#    if sample =="DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":
    if sample =="DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8":
        numevents=45352295
        #numevents=49620546.0
        #cross_section_pb=4895*1.23
        #From https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
        cross_section_pb=5765.4
        linecolor=2
    if sample =="DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        #Differs slightly from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#DY_Z. Where is 1.23 factor from that is in UCSB table?
        #numevents=47943922
        #numevents=49748967
        #numevents=49582723.0
        #numevents=27244008.0
        #numevents=27435948
        #numevents=20270155
        #numevents=27365539
        #numevents=24265115.0
        numevents=27300991.
        #numevents=49620546.0
        #cross_section_pb=4895*1.23
        #From https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeV
        cross_section_pb=5765.4
        linecolor=2
    if sample =="DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":
        #Differs slightly from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#DY_Z. Where is 1.23 factor from?
        #numevents=35293682
        numevents=35167868
        cross_section_pb=18610*1.23
        linecolor=2
    #From UCBS table, NNLO from Lesya's summary table
    if sample=="WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":
        #numevents=24120319
        #numevents=24083399.0
        #numevents=23183722
        numevents=2317615.0
        cross_section_pb=61526.7
        linecolor=6
    if sample=="WW_DoubleScattering_13TeV-pythia8":
        numevents=10000
        cross_section_pb=1.64
        linecolor=7
    if sample=="WpWpJJ_EWK-QCD_TuneCUETP8M1_13TeV-madgraph-pythia8":
        numevents=149681.
        cross_section_pb=0.03711
        linecolor=7
    if sample=="ZZTo4L_13TeV_powheg_pythia8":
        numevents=6669988.
        cross_section_pb=1.256
        linecolor=8
    if sample=="WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":
        numevents=6103817
        cross_section_pb=405.271
        linecolor=9
    if sample=="ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":
        #This samples is for M>30
        numevents=2307158.0
        cross_section_pb=117.864
        linecolor=11
    if sample=="WZ_TuneCUETP8M1_13TeV-pythia8":
        numevents=1000000.0
        cross_section_pb=47.13
        linecolor=12
    if sample=="ZZ_TuneCUETP8M1_13TeV-pythia8":
        numevents=990064.0
        cross_section_pb=16.523
        linecolor=13

        

    print sample
    print luminosity_fb
    print cross_section_pb
    print numevents
    h.Scale((luminosity_fb*cross_section_pb*1000.)/numevents)
    h.SetFillColor(linecolor)
    h.SetLineColor(linecolor)


def legend_name(sample):
    name="No legend name yet"
    if sample=="WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":name="W+Jets"
    if sample=="TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":name="t#bar{t}"
    if sample=="WWTo2L2Nu_13TeV-powheg":name="inclusive WW"
    if sample=="DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": name="Drell-Yan 10-50 GeV"
    if sample=="DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8": name="Drell-Yan 50+ GeV"
    if sample=="DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": name="Drell-Yan 50+ GeV"
    if sample=="ExclusiveWW": name="Elastic SM Exclusive WW"
    if sample=="ExclusiveWWNonElastic": name="Non-Elastic SM Exclusive WW"
    if sample=="WW_DoubleScattering_13TeV-pythia8": name="WW_DoubleScattering"
    if sample=="WpWpJJ_EWK-QCD_TuneCUETP8M1_13TeV-madgraph-pythia8": name="WpWpJJ_EWK-QCD"
    if sample=="ZZTo4L_13TeV_powheg_pythia8": name="ZZTo4L"
    if sample=="ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8": name="ZGTo2LG"
    if sample=="WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": name="WGToLNuG"
    if sample=="ZZ_TuneCUETP8M1_13TeV-pythia8": name="ZZ"
    if sample=="WZ_TuneCUETP8M1_13TeV-pythia8": name="WZ"
    return name


def passPPS(xi):
    left=False
    right=False
    passesPPS=False
    ii=0
    for detId_rp in e.rp_tracks_detId:
                    #print detId_rp
        if detId_rp == 2: 
            left=True
                    #if lessthan6: print "DetId 2, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["2"].append(e.rp_tracks_xi[ii])
        if detId_rp == 3: 
            left=True
                    #if lessthan6: print "DetId 3, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["3"].append(e.rp_tracks_xi[ii])
        if detId_rp == 102: 
            right=True
                    #xi_right.append(float(e.rp_tracks_xi))
                    #if lessthan6: print "DetId 102, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["102"].append(e.rp_tracks_xi[ii])
        if detId_rp == 103: 
            right=True
                    #xi_right.append(float(e.rp_tracks_xi))
                    #if lessthan6: print "DetId 103, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["103"].append(e.rp_tracks_xi[ii])
        ii=ii+1

    if (left == True) and (right == True):
        passesPPS=True
        if fvertex_numtracks < 6 and ptemu > 30:
            print "Run: {0}, Lumi: {1}, Event: {2}".format(run,e.lumiblock,event)
            print "Num extra tracks: {0}, ptemu: {1}".format(fvertex_numtracks,ptemu)
            print "Xi_2:",xi["2"],"Xi_3:",xi["3"],"Xi_102:",xi["102"],"Xi_103:",xi["103"]
            print "Chi2_ndof: {0}".format(e.fvertex_chi2ndof)
            print "Closest track: {0}".format(closest_track)
            print "My vertex fit position x, y, z: {0},{1},{2}".format(e.fvertex_x,e.fvertex_y,e.fvertex_z)
            print "Primary vertex fit position x, y, z: {0},{1},{2}".format(e.vertex_x,e.vertex_y,e.vertex_z)
            print "Primary vertex extra tracks: {0}".format(e.vertex_ntracks-2)

    if len(xi["2"]) > 1 or len(xi["3"]) > 1 or len(xi["102"]) > 1 or len(xi["103"]) > 1:
        print "This event has multiple tracks in a single pot"
        print "Xi_2:",xi["2"],"Xi_3:",xi["3"],"Xi_102:",xi["102"],"Xi_103:",xi["103"]
        passesPPS=False
    return passesPPS


