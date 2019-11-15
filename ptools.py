#!/usr/bin/env python
#Finn Rebassoo, LLNL 02-03-2017
import math as m
import json

def calcAco(phi1,phi2):
    result = phi1-phi2
    if result > m.pi : result = result-2*m.pi
    if result < m.pi : result = result+2*m.pi
    aco=1-result/m.pi
    return aco

def ModifyHisto(h,sample,directory):

    luminosity_fb=37.5
    print sample
    #https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
    cross_section_pb=0
    numevents=0
    linecolor=0

    #with open('histos_muon2/run/merged_file.json') as json_file:
    with open('{0}/samples_info.json'.format(directory)) as json_file:
        data=json.load(json_file)
        #print sample
        #print type(sample)
        numevents=data[sample][0]
        cross_section_pb=data[sample][1]
        linecolor=data[sample][2]
    print luminosity_fb
    print cross_section_pb
    print numevents
    h.Sumw2()
    h.Scale((luminosity_fb*cross_section_pb*1000.)/numevents)
    h.SetFillColor(linecolor)
    h.SetLineColor(linecolor)
    #h.SetLineStyle(2)


def legend_name(sample):
    name="No legend name yet"
    if sample=="ExclusiveWW_a0w1e-6-SingleLepton-2017": name="#gamma#gamma #rightarrow WW #scale[1]{(a_{0}^{W}/#Lambda^{2}=1*10^{-6})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if sample=="ExclusiveWW_a0w2e-6-SingleLepton-2017": name="#gamma#gamma #rightarrow WW #scale[1]{(a_{0}^{W}/#Lambda^{2}=2*10^{-6})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if sample=="ExclusiveWW_a0w5e-6-SingleLepton-2017": name="#gamma#gamma #rightarrow WW #scale[1]{(a_{0}^{W}/#Lambda^{2}=5*10^{-6})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if sample=="ExclusiveWW_SM_FPMC-SingleLepton-2017": name="SM #gamma#gamma #rightarrow WW"
    if sample=="QCD_Pt_170to300_TuneCP5_13TeV_pythia8": name="QCD"# Pt binned"
    if sample=="TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8":name="t#bar{t}"# amcatnloFXFX-pythia8"
    if sample=="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8":name="t#bar{t} powheg"
    #if sample=="WZ_TuneCP5_13TeV-pythia8": name="WZ pythia8"
    if sample=="ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8": name="Single top"
    if sample=="WW_TuneCP5_13TeV-pythia8":name="Inclusive WV"
    if sample=="DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8":name="DY+jets"
    if sample=="DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8":name="DY+jets"
    if sample=="WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8":name="W+Jets"
    if sample=="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8":name="W+Jets"
    if sample=="WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8":name="W+Jets, HT binned madgraph"
    if sample=="W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8":name="W+Jets, pt binned"
    return name

