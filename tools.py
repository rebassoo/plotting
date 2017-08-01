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
    luminosity_fb=35.8
    #This is luminosity without runD
    #luminosity_fb=32.8
    print sample
    #https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
    cross_section_pb=0
    numevents=0
    linecolor=0
    if sample =="ExclusiveWW":
        #This cross section is from Doug's notes 92.83+/-0.10 for Madgraph 5.2.4.2. But this sample is only leptons so smaller cross section. Used %10.61 from Doug's notes. Should be 10.71% from 2014 PDG. 
        numevents=5000
        #0.0098903 is value calculated in Madgraph and is in the file unweighted_events.lhe
        cross_section_pb=4.1*0.0098903
        linecolor=7
    if sample =="WWTo2L2Nu_13TeV-powheg":
        #numevents=1999000
        #numevents=1236906
        #numevents=1162658
        numevents=1206070
        #From website above
        cross_section_pb=12.178
        linecolor=5
    if sample =="TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":
        #numevents=6105137.
        #numevents=5865278
        #numevents=5997301
        numevents=6055403
        #From UCSB table (3*0.108)^2*815.96
        cross_section_pb=85.66
        linecolor=4
    if sample =="DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":
        #Differs slightly from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#DY_Z. Where is 1.23 factor from that is in UCSB table?
        numevents=49748967
        #numevents=47943922
        cross_section_pb=4895*1.23
        linecolor=2
    if sample =="DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":
        #Differs slightly from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#DY_Z. Where is 1.23 factor from?
        #numevents=35293682
        numevents=35167868
        cross_section_pb=18610*1.23
        linecolor=2
    #From UCBS table, NNLO from Lesya's summary table
    if sample=="WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":
        numevents=24120319
        #numevents=23183722
        cross_section_pb=61526.7
        linecolor=6
    h.Scale((luminosity_fb*cross_section_pb*1000.)/numevents)
    h.SetFillColor(linecolor)


def legend_name(sample):
    name="No legend name yet"
    if sample=="WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8":name="W+Jets"
    if sample=="TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8":name="t#bar{t}"
    if sample=="WWTo2L2Nu_13TeV-powheg":name="WW"
    if sample=="DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": name="Drell-Yan 10-50 GeV"
    if sample=="DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8": name="Drell-Yan 50+ GeV"
    if sample=="ExclusiveWW": name="SM Exclusive WW"
    return name

