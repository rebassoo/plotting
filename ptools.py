#!/usr/bin/env python
#Finn Rebassoo, LLNL 02-03-2017
import math as m
import json
from ROOT import *

def writePlots(c,Ycut,channel,signal_region,background_method,year,justSignal=False):
    latex=TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(11)
    latex.DrawLatex(0.12,0.92,"CMS")
    signal_region_simple=""
    if channel == "muon":
        channel_plot="\mu"
    else:
        channel_plot="e"
    if year == "2018":
        latex.DrawLatex(0.65,0.92,"55.7 fb^{-1} (13 TeV)")
        if signal_region == "MultiRP":
            signal_region_simple = "High Resolution,"
        if signal_region == "MultiPixel":
            signal_region_simple = "Medium Resolution,"
    if year == "2017":
        latex.DrawLatex(0.65,0.92,"37.5 fb^{-1} (13 TeV)")
        if signal_region == "MultiRP":
            signal_region_simple = "High Resolution"
        if signal_region == "PixelPixel":
            signal_region_simple = "Medium Resolution"
        if signal_region == "MultiPixel":
            signal_region_simple = "High Efficiency"
    ycut_str=""
    if Ycut=="Ycut":
        ycut_str="_ycut"
    if channel=="muon":
        #latex.DrawLatex(0.17,0.80,"{0}".format(signal_region))
        latex.DrawLatex(0.17,0.85,"{0}".format(signal_region_simple))
        latex.DrawLatex(0.17,0.80,"\mu channel")
    if channel=="electron":
        #latex.DrawLatex(0.17,0.80,"{0}".format(signal_region))
        latex.DrawLatex(0.17,0.85,"{0}".format(signal_region_simple))
        latex.DrawLatex(0.17,0.80,"e channel")
    #c.Print("BackgroundPrediction_{0}_{1}{2}.pdf".format(directory[11:],background_method,ycut_str))
    latex.SetTextSize(0.02)
    if justSignal:
        c.Print("SignalPrediction_{0}{1}_{2}_{3}.pdf".format(signal_region,ycut_str,channel,year))
    else:
        latex.DrawLatex(0.61,0.852,"#frac{Data-driven background methods}{}")
        latex.DrawLatex(0.61,0.75,"#frac{MC background predictions}{}")
        latex.DrawLatex(0.61,0.52,"#frac{Signal predictions}{}")
        c.Print("BackgroundPrediction_{0}_{1}{2}_{3}_{4}.pdf".format(signal_region,background_method,ycut_str,channel,year))
        #c.Print("BackgroundPrediction_{0}_{1}{2}_{3}_{4}.C".format(signal_region,background_method,ycut_str,channel,year))

def calcAco(phi1,phi2):
    result = phi1-phi2
    if result > m.pi : result = result-2*m.pi
    if result < m.pi : result = result+2*m.pi
    aco=1-result/m.pi
    return aco

def ModifyHisto(h,sample,directory):
    #luminosity_fb=37.5
    luminosity_fb=55.7
    print sample
    #https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
    cross_section_pb=0
    numevents=0
    linecolor=0

    #with open('histos_muon2/run/merged_file.json') as json_file:
    with open('{0}/samples_info.json'.format(directory)) as json_file:
        data=json.load(json_file)
        print sample
        print type(sample)
        numevents=data[sample][0]
        cross_section_pb=data[sample][1]
        linecolor=data[sample][2]
        if "GGToWW" in sample and "2018" in sample:
            cross_section_pb=cross_section_pb*0.14271*(1.174)
            #linecolor=1
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
    if "GGToWW_SM_13TeV-fpmc-herwig6" in sample: 
        name="SM #gamma#gamma #rightarrow WW"
    if "GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6" in sample: 
        name="#gamma#gamma #rightarrow WW #scale[1]{(a_{0}^{W}/#Lambda^{2}=1*10^{-6})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if "GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6" in sample: 
        name="#gamma#gamma #rightarrow WW #scale[1]{(a_{0}^{W}/#Lambda^{2}=1*10^{-6})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if "GGToWW_bSM-A0W5e-7_13TeV-fpmc-herwig6" in sample: 
        name="#gamma#gamma #rightarrow WW #scale[1]{(a_{0}^{W}/#Lambda^{2}=5*10^{-7})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if "GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6" in sample: 
        name="#gamma#gamma #rightarrow WW #scale[1]{(a_{0}^{W}/#Lambda^{2}=2*10^{-6})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if "GGToWW_bSM-A0W5e-6_13TeV-fpmc-herwig6" in sample: 
        name="#gamma#gamma #rightarrow WW #scale[1]{(a_{0}^{W}/#Lambda^{2}=5*10^{-6})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if "GGToWW_bSM-ACW2e-6_13TeV-fpmc-herwig6" in sample: 
        name="#gamma#gamma #rightarrow WW #scale[1]{(a_{C}^{W}/#Lambda^{2}=2*10^{-6})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if "GGToWW_bSM-ACW8e-6_13TeV-fpmc-herwig6" in sample: 
        name="#gamma#gamma #rightarrow WW #scale[1]{(a_{C}^{W}/#Lambda^{2}=8*10^{-6})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if "GGToWW_bSM-ACW2e-5_13TeV-fpmc-herwig6" in sample: 
        name="#gamma#gamma #rightarrow WW #scale[1]{(a_{C}^{W}/#Lambda^{2}=2*10^{-5})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if sample == "QCD_Pt_170to300_TuneCP5_13TeV_pythia8": name="QCD"# Pt binned"
    if sample == "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8":name="t#bar{t}"# amcatnloFXFX-pythia8"
    if sample == "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8":name="t#bar{t} powheg"
    #if sample=="WZ_TuneCP5_13TeV-pythia8": name="WZ pythia8"
    if sample == "ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8": name="Single top"
    if sample == "ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8": name="Single top"
    if sample == "WW_TuneCP5_13TeV-pythia8":name="Inclusive WV"
    if sample == "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8":name="DY+jets"
    if sample == "DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8":name="DY+jets"
    if sample == "WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8":name="W+Jets"
    if sample == "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8":name="W+Jets"
    if sample == "WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8":name="W+Jets, HT binned madgraph"
    if sample == "W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8":name="W+Jets, pt binned"
    return name

