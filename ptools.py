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

    #luminosity_fb=8.681
    luminosity_fb=37.5
    print sample
    #https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
    cross_section_pb=0
    numevents=0
    linecolor=0

    if sample=="WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        numevents=180935349.0
        cross_section_pb=50131.983
        linecolor=3

    if sample=="WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        numevents=129940921.0
        cross_section_pb=8426.094
        linecolor=3

    if sample=="WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        numevents=80285191.0
        cross_section_pb=3172.958
        linecolor=3

    if sample=="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=35862893*(103./105.)
        #numevents=35862893*(104./105.)
        #numevents=26462644.0
        numevents=31865784.0
        cross_section_pb=61526.7
        linecolor=3

    if sample=="WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=35862893*(30./148.)
        #numevents=35862893*(31./148.)
        numevents=26345944.0
        #cross_section_pb=1345*1.21
        cross_section_pb=1345*1.26
        linecolor=3

    if sample=="WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=17260723
        #numevents=21250517*(79./80.)
        numevents=19899436.0
        #cross_section_pb=359.7*1.21
        cross_section_pb=359.7*1.48
        linecolor=3

    if sample=="WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=14313274
        #numevents=13970012*(63./63.)
        #numevents=13970012*(62./63.)
        numevents=10697050.0
        #cross_section_pb=48.91*1.21
        cross_section_pb=48.91*1.26
        linecolor=3

    if sample=="WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=20516713
        #numevents=21709087*(79./98.)
        #numevents=21709087*(98./98.)
        numevents=18325085.0
        #cross_section_pb=12.05*1.21
        cross_section_pb=12.05*1.03
        linecolor=3

    if sample=="WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=20466692
        #numevents=20466692*(98./98.)
        numevents=20245897.0
        #cross_section_pb=5.501*1.21
        cross_section_pb=5.501*1.05
        linecolor=3

    if sample=="WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=19464742
        #numevents=20258624*(108./111.)
        numevents=20258624.0
        #cross_section_pb=1.329*1.21
        cross_section_pb=1.329*0.77
        linecolor=3

    if sample=="WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=20244084
        #numevents=20244084*(100./118.)
        #numevents=20244084*(113./118.)
        numevents=19426229.0
        #cross_section_pb=0.03216*1.21
        cross_section_pb=0.03216*0.77
        linecolor=3

    if sample=="QCD_Pt_170to300_TuneCP5_13TeV_pythia8":
        #numevents=29829920. *(65./85.)
        numevents=26298316.0
        cross_section_pb=103500
        linecolor=2

    if sample=="QCD_Pt_300to470_TuneCP5_13TeV_pythia8":
        #numevents=53798780. *(173./180.)
        numevents=50543662.0
        cross_section_pb=6830
        linecolor=2

    if sample=="QCD_Pt_470to600_TuneCP5_13TeV_pythia8":
        #numevents=27881028. *(83./92.)
        numevents= 27881028.0
        cross_section_pb=642.1
        linecolor=2

    if sample=="QCD_Pt_600to800_TuneCP5_13TeV_pythia8":
        #numevents=66134964 *(178./227.)
        numevents=56760138.0
        cross_section_pb=185.9
        linecolor=2

    if sample=="QCD_Pt_800to1000_TuneCP5_13TeV_pythia8":
        #numevents=39529008*(89./124.)
        numevents=37594720.0
        cross_section_pb=32.293
        linecolor=2

    if sample=="QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8":
        #numevents=19631814 *(60./124.)
        numevents=19631814.0
        cross_section_pb=9.4183
        linecolor=2

    if sample =="WW_TuneCP5_13TeV-pythia8":
        #numevents=7319484
        numevents=7791498
        #From website above
        #This NNLO from diboson_final
        cross_section_pb=115.0
        linecolor=5

    if sample=="WZ_TuneCP5_13TeV-pythia8":
        #numevents=3928630
        numevents=2775960.0
        cross_section_pb=47.13
        linecolor=12

    if sample=="TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        #numevents=133011159
        numevents=153531390*(435./461.)
        #numevents=135461679
        cross_section_pb=831.76
        linecolor=4

    if sample=="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8":
        #numevents=41221873*(122./123.)
        #numevents=41221873*(123./123.)
        #numevents=36833333.0
        numevents=37238173.0
        cross_section_pb=831.76*0.435
        linecolor=4

    if sample=="ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8":
        #numevents=9568575*(5./27.)
        numevents=6860482.0
        cross_section_pb=3.36
        linecolor=7
 
    if sample=="ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8":
        #This is total number of events in DAS, just submitted crab job
        #numevents=5865875.*(23./23.)
        numevents=5865875.0
        cross_section_pb=136.02       
        linecolor=7

    if sample=="ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8":
        #numevents=3939990*(12./13.)
        numevents=3350290.0
        cross_section_pb=80.945
        linecolor=7

    if sample=="ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8":
        #numevents=7581624.*(12./26.)
        numevents=6135926.0
        cross_section_pb=35.85
        linecolor=7

    if sample=="ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8":
        #numevents=7780870*(26./26.)
        numevents=7516910.0
        cross_section_pb=35.85
        linecolor=7


    print sample
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
    if sample=="WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8":name="W+Jets"
    if sample=="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8":name="W+Jets"
    if sample=="WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8":name="W+Jets, HT binned madgraph"
    if sample=="TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8":name="t#bar{t} amcatnloFXFX-pythia8"
    if sample=="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8":name="t#bar{t} powheg"
    if sample=="WW_TuneCP5_13TeV-pythia8":name="WW pythia8"
    if sample=="WZ_TuneCP5_13TeV-pythia8": name="WZ pythia8"
    if sample=="ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8": name="Single top"
    if sample=="QCD_Pt_170to300_TuneCP5_13TeV_pythia8": name="QCD Pt binned"
    return name

