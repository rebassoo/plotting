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

    if sample=="GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6":
        numevents=993700.0
        cross_section_pb=0.0453974
        linecolor=6

    if sample=="GGToWW_bSM-A0W5e-6_13TeV-fpmc-herwig6":
        numevents=993000.0
        cross_section_pb=0.148132
        linecolor=6

    if sample=="GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6":
        numevents=880000.
        cross_section_pb=0.0583158
        linecolor=6

    if sample=="GGToWWTo3L3Nu_PtL-20_13TeV-fpmc-herwig6.root":
        numevents=310088.
        cross_section_pb=0.0775
        linecolor=1

    if sample=="ExclusiveWW_SM_FPMC-SingleLepton-2017":
        numevents=19000.
        cross_section_pb=0.0391
        linecolor=1

    if sample=="ExclusiveWW_a0w2p5e-6-SingleLepton-2017":
        #numevents=993
        numevents=19923.0
        cross_section_pb=0.1282
        linecolor=38
        
    if sample=="ExclusiveWW_a0w1e-6-SingleLepton-2017":
        #numevents=14000.
        numevents=15000.
        #cross_section_pb=0.05314
        cross_section_pb=0.062086
        linecolor=6

    if sample=="W1JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8":
        #numevents=71937389.0
        numevents=62744276.0
        cross_section_pb=286.1
        linecolor=862

    if sample=="W1JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8":
        #numevents=125064008.0
        numevents=108576810.0
        cross_section_pb=71.9
        linecolor=862

    if sample=="W1JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8":
        #numevents=20841145.0
        numevents=18410600.0
        cross_section_pb=8.05
        linecolor=862

    if sample=="W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8":
        numevents=4558033.0
        #numevents=4342270.0
        cross_section_pb=0.885
        linecolor=862

    if sample=="W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8":
        #numevents=36719823.0
        numevents=34912677.0
        cross_section_pb=277.7
        linecolor=862

    if sample=="W2JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8":
        #numevents=168794029.0
        #numevents=167260334.0
        #numevents=62296752.0
        numevents=137111043.0
        cross_section_pb=105.9
        linecolor=862

    if sample=="W2JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8":
        #numevents=48900966.0
        #numevents=54074629.0
        numevents=58676428.0
        cross_section_pb=18.67
        linecolor=862

    if sample=="W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8":
        #numevents=30340311.0
        numevents=29956048.0
        cross_section_pb=3.037
        linecolor=862


    #W+Jets and DY cross sections come from David Morses talk on pt and nJet-binned samples.
    if sample=="WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        #numevents=179488932.0
        #numevents=180935349.0
        numevents=157537768.0
        cross_section_pb=50131.983
        linecolor=862

    if sample=="WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        #numevents=131511758.0
        #numevents=119299596.0
        #numevents=126360621.0
        #numevents=129238699.0
        numevents=132817445.0
        cross_section_pb=8426.094
        linecolor=862

    if sample=="WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        #numevents=94564355.0
        #numevents=53492479.0
        #numevents=94281664.0
        numevents=95680017.0
        cross_section_pb=3172.958
        linecolor=862

    if sample=="DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        #numevents=88230653.0
        numevents=83325772.0
        cross_section_pb=4620.52
        linecolor=12

    if sample=="DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        #numevents=95629091.0
        numevents=87036913.0
        cross_section_pb=859.59
        linecolor=12

    if sample=="DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        #numevents=54592285.0
        numevents=46359045.0
        cross_section_pb=338.26
        linecolor=12

    if sample=="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8":
        #numevents=41221873*(122./123.)
        #numevents=41221873*(123./123.)
        #numevents=36833333.0
        #numevents=40257121.0
        numevents=41221873.0
        cross_section_pb=831.76*0.435
        linecolor=800

    if sample=="TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        #numevents=133011159
        #numevents=153531390*(435./461.)
        #numevents=145531853.0
        #numevents=33485568.0
        numevents=33762370.0
        cross_section_pb=831.76
        linecolor=800



    if sample=="QCD_Pt_170to300_TuneCP5_13TeV_pythia8":
        #numevents=29829920. *(65./85.)
        #numevents=29168366.0
        numevents=29829920.0
        cross_section_pb=103500
        linecolor=2
        
    if sample=="QCD_Pt_300to470_TuneCP5_13TeV_pythia8":
        #numevents=53798780. *(173./180.)
        #numevents=53484746.0 
        numevents=53798780.0
        cross_section_pb=6830
        linecolor=2

    if sample=="QCD_Pt_470to600_TuneCP5_13TeV_pythia8":
        #numevents=27881028. *(83./92.)
        #numevents=26403420.0
        numevents=11419908.0
        #Exclusive WW twiki
        #cross_section_pb=642.1
        #xsdb
        cross_section_pb=552.1
        linecolor=2

    if sample=="QCD_Pt_600to800_TuneCP5_13TeV_pythia8":
        #numevents=66134964 *(178./227.)
        #numevents=66134964.0
        numevents=65473240.0
        #Exclusive WW twiki
        #cross_section_pb=185.9
        #xsdb
        cross_section_pb=156.9
        linecolor=2

    if sample=="QCD_Pt_800to1000_TuneCP5_13TeV_pythia8":
        #numevents=39529008*(89./124.)
        #numevents=38582152.0
        numevents=39529008.0
        #Exclusive WW twiki
        #cross_section_pb=32.293
        #xsdb
        cross_section_pb=26.28
        linecolor=2

    if sample=="QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8":
        #numevents=19631814 *(60./124.)
        #numevents=19330844.0
        #numevents=17906272.0
        numevents=18048660.0
        #Exclusive WW twiki
        #cross_section_pb=9.4183
        #xsdb
        cross_section_pb=7.47
        linecolor=2

    if sample=="QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8":
        #numevents=5427060.0
        numevents=3972502.0
        cross_section_pb=0.6484
        linecolor=2

    if sample=="QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8":
        #numevents=2923941.0
        numevents=2594457.0
        cross_section_pb=0.08743
        linecolor=2

    if sample=="QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8":
        #numevents=1910526.
        numevents=861718.0
        cross_section_pb=0.005236
        linecolor=2

    if sample=="QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8":
        #numevents=757837.
        numevents=757837.0
        cross_section_pb=0.0001357
        linecolor=2


    if sample=="QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8":
        numevents=46438676.0
        cross_section_pb=0.07335*117989
        linecolor=2
    if sample=="QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8":
        numevents=15679722.0
        cross_section_pb=0.10196*7820.25
        linecolor=2
    if sample=="QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8":
        cross_section_pb=0.12242*645.528
        linecolor=2
        numevents=23940201.0
    if sample=="QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8":
        cross_section_pb=0.13412*187.109
        linecolor=2
        numevents=16171482.0
    if sample=="QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8":
        cross_section_pb=0.14552*32.3486
        linecolor=2
        numevents=14559081.0
    if sample=="QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8":
        cross_section_pb=0.15544*10.4305
        linecolor=2
        numevents=11208614.0

    if sample =="WW_TuneCP5_13TeV-pythia8":
        #numevents=7319484
        #numevents=7424458.0
        #numevents=7375362.0
        numevents=3002708.0
        #From website above
        #This NNLO from diboson_final
        cross_section_pb=115.0
        linecolor=3

    if sample=="WZ_TuneCP5_13TeV-pythia8":
        #numevents=3928630
        #numevents=3500900.0
        #numevents=3161030.0
        numevents=2770750.0
        cross_section_pb=47.13
        #linecolor=12
        linecolor=3

    if sample=="ZZ_TuneCP5_13TeV-pythia8":
        #numevents=1949768.0
        #numevents=1475796.0
        numevents=1949768.0
        cross_section_pb=16.523
        linecolor=3



    if sample=="ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8":
        #numevents=9568575*(5./27.)
        #numevents=9568575.0
        numevents=4756234.0
        cross_section_pb=3.36
        linecolor=7
 
    if sample=="ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8":
        #This is total number of events in DAS, just submitted crab job
        #numevents=5865875.*(23./23.)
        #numevents=5865875.0
        numevents=4434390.0
        cross_section_pb=136.02       
        linecolor=7

    if sample=="ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8":
        #numevents=3939990*(12./13.)
        #numevents=3939990.0
        numevents=2135040.0
        cross_section_pb=80.945
        linecolor=7

    if sample=="ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8":
        #numevents=7581624.*(12./26.)
        #numevents=7581624
        numevents=4411054.0
        cross_section_pb=35.85
        linecolor=7

    if sample=="ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8":
        #numevents=7780870*(26./26.)
        #numevents=7780870.0
        numevents=7119540.0
        cross_section_pb=35.85
        linecolor=7

    if sample=="DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8":
        #numevents=23777166.0
        numevents=27155790.0
        cross_section_pb=5765.4
        linecolor=12


    if sample=="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=35862893*(103./105.)
        #numevents=35862893*(104./105.)
        #numevents=26462644.0
        numevents=31865784.0
        cross_section_pb=61526.7
        linecolor=862

    if sample=="WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=35862893*(30./148.)
        #numevents=35862893*(31./148.)
        numevents=26345944.0
        #cross_section_pb=1345*1.21
        cross_section_pb=1345*1.26
        linecolor=862

    if sample=="WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=17260723
        #numevents=21250517*(79./80.)
        numevents=19899436.0
        #cross_section_pb=359.7*1.21
        cross_section_pb=359.7*1.48
        linecolor=862

    if sample=="WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=14313274
        #numevents=13970012*(63./63.)
        #numevents=13970012*(62./63.)
        numevents=10697050.0
        #cross_section_pb=48.91*1.21
        cross_section_pb=48.91*1.26
        linecolor=862

    if sample=="WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=20516713
        #numevents=21709087*(79./98.)
        #numevents=21709087*(98./98.)
        numevents=18325085.0
        #cross_section_pb=12.05*1.21
        cross_section_pb=12.05*1.03
        linecolor=862

    if sample=="WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=20466692
        #numevents=20466692*(98./98.)
        numevents=20245897.0
        #cross_section_pb=5.501*1.21
        cross_section_pb=5.501*1.05
        linecolor=862

    if sample=="WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=19464742
        #numevents=20258624*(108./111.)
        numevents=20258624.0
        #cross_section_pb=1.329*1.21
        cross_section_pb=1.329*0.77
        linecolor=862

    if sample=="WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8":
        #numevents=20244084
        #numevents=20244084*(100./118.)
        #numevents=20244084*(113./118.)
        numevents=19426229.0
        #cross_section_pb=0.03216*1.21
        cross_section_pb=0.03216*0.77
        linecolor=862

        

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
    if sample=="ExclusiveWW_a0w1e-6-SingleLepton-2017": name="#gamma#gamma #rightarrow WW #scale[1]{(a_{0}^{W}/#Lambda^{2}=1*10^{-6})}"#, a_{c}^{W}#Lambda^{2}=0)}"
    if sample=="ExclusiveWW_a0w2p5e-6-SingleLepton-2017": name="#gamma#gamma #rightarrow WW #scale[1]{(a_{0}^{W}/#Lambda^{2}=2.5*10^{-6})}"#, a_{c}^{W}#Lambda^{2}=0)}"
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

