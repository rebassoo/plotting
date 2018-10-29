#!/usr/bin/env python
#Finn Rebassoo, LLNL 05-05-2017
#Plot all the MC samples
from ptools import *
from ROOT import *
import datetime
import sys
import math as m

MCsamples=[
"WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
"WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
"WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
#"WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8",
#"WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
#"WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
#"WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",
#"WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",
#"WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",
#"WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",
"WW_TuneCP5_13TeV-pythia8",
"WZ_TuneCP5_13TeV-pythia8",
"TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
"ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8",
"ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8",
"ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8",
"ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
"ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
"QCD_Pt_170to300_TuneCP5_13TeV_pythia8",
"QCD_Pt_300to470_TuneCP5_13TeV_pythia8",
"QCD_Pt_470to600_TuneCP5_13TeV_pythia8",
"QCD_Pt_600to800_TuneCP5_13TeV_pythia8",
"QCD_Pt_800to1000_TuneCP5_13TeV_pythia8",
"QCD_Pt_800to1000_TuneCP5_13TeV_pythia8"
]

CutflowHistoList=[
"h_muon_pt",
"h_muon_pt_jetVeto",
#"h_muon_pt_jetVeto_WleptonicCuts",
"h_muon_pt_jetpruned",
"h_recoMWW_afterDphi",
"h_recoMWhad_afterMWW",
"h_MET_afterMWhad",
"h_WLeptonicPt_afterMET",
"h_pfcand_nextracks_afterWLeptonicPt",
"h_pfcand_nextracks_afterWLeptonicPt_NumTracks4"
]

CutflowNameList=[
"Preselection",
"Jet Veto",
"Jet pruned",
"Delta phi cut",
"MWW cut",
"MWhad cut",
"MET cut",
"W leptonic pt cut",
"Extra tracks cut"
]

numCuts=len(CutflowHistoList)
Wjets=[0]*numCuts
ttbar=[0]*numCuts
SingleTop=[0]*numCuts
Diboson=[0]*numCuts
QCD=[0]*numCuts
total=[0]*numCuts

Wjets_error=[0]*numCuts
ttbar_error=[0]*numCuts
SingleTop_error=[0]*numCuts
Diboson_error=[0]*numCuts
QCD_error=[0]*numCuts
total_error=[0]*numCuts

Wjets_all=[]
ttbar_all=[]
SingleTop_all=[]
Diboson_all=[]
QCD_all=[]
total_all=[]
data_all=[]

justMC=False

i=0
for cut in CutflowHistoList:
    print cut
    it=0
    for sample in MCsamples:
        #fMC=TFile("histos/10-25-2018/"+sample+".root")
        fMC=TFile("histos/"+sample+".root")
        hMC=TH1F()
        integral=0
        error=0
        if "NumTracks4" in cut:
            hMC=fMC.Get("h_pfcand_nextracks_afterWLeptonicPt")
            integral_bscaling=hMC.Integral(0,5)
            ModifyHisto(hMC,sample)
            integral=hMC.Integral(0,5)
            if integral_bscaling>0:
                error=(m.sqrt(integral_bscaling)/integral_bscaling)*integral
        else:
            hMC=fMC.Get(cut)
            integral_bscaling=hMC.Integral(0,1001)
            ModifyHisto(hMC,sample)
            integral=hMC.Integral(0,1001)
            if integral_bscaling>0:
                error=(m.sqrt(integral_bscaling)/integral_bscaling)*integral
        total[i]=integral+total[i]
        total_error[i]=m.sqrt(total_error[i]*total_error[i]+error*error)
        if "WJets" in sample:
            Wjets[i]=integral+Wjets[i]
            Wjets_error[i]=m.sqrt(Wjets_error[i]*Wjets_error[i]+error*error)
        if "ST_" in sample:
            SingleTop[i]=integral+SingleTop[i]
            SingleTop_error[i]=m.sqrt(SingleTop_error[i]*SingleTop_error[i]+error*error)
        if "TTT" in sample:
            ttbar[i]=integral+ttbar[i]
            ttbar_error[i]=m.sqrt(ttbar_error[i]*ttbar_error[i]+error*error)
        if ("WW_" in sample) or ("WZ_" in sample):
            Diboson[i]=integral+Diboson[i]
            Diboson_error[i]=m.sqrt(Diboson_error[i]*Diboson_error[i]+error*error)
        if "QCD_" in sample:
            QCD[i]=integral+QCD[i]
            QCD_error[i]=m.sqrt(QCD_error[i]*QCD_error[i]+error*error)
        it=it+1
    Wjets[i]=round(Wjets[i],1)
    ttbar[i]=round(ttbar[i],1)
    SingleTop[i]=round(SingleTop[i],1)
    Diboson[i]=round(Diboson[i],1)
    QCD[i]=round(QCD[i],1)
    total[i]=round(total[i],1)
    Wjets_error[i]=round(Wjets_error[i],1)
    ttbar_error[i]=round(ttbar_error[i],1)
    SingleTop_error[i]=round(SingleTop_error[i],1)
    Diboson_error[i]=round(Diboson_error[i],1)
    QCD_error[i]=round(QCD_error[i],1)

    total_error[i]=round(total_error[i],1)
    i=i+1

data=[0]*6
if not justMC:
    #fdata=TFile("histos/10-25-2018/SingleMuonTotal.root")
    fdata=TFile("histos/SingleMuonTotal.root")
    idata=0
    for cut in CutflowHistoList:
        if idata<6:
            hData=TH1F()
            #print "Cut: ",cut
            hData=fdata.Get(cut)
            integral=hData.Integral(0,1001)
            data[idata]=int(integral)
        idata=idata+1

#Add errors to values
ait=0
for at in CutflowHistoList:
    Wjets_all.append(str(Wjets[ait])+" +/- "+ str(Wjets_error[ait]))
    ttbar_all.append(str(ttbar[ait])+" +/- "+ str(ttbar_error[ait]))
    SingleTop_all.append(str(SingleTop[ait])+" +/- "+ str(SingleTop_error[ait]))
    Diboson_all.append(str(Diboson[ait])+" +/- "+ str(Diboson_error[ait]))
    QCD_all.append(str(QCD[ait])+" +/- "+ str(QCD_error[ait]))
    total_all.append(str(total[ait])+" +/- "+ str(total_error[ait]))
    if ait<6:
        data_all.append(str(data[ait]))
    ait=ait+1



print CutflowHistoList
print "Cuts:           ",CutflowNameList
#print "WJets:          ",Wjets
#print "WJets error:    ",Wjets_error
print "WJets:          ",Wjets_all
print "ttbar:          ",ttbar_all
print "Single Top:     ",SingleTop_all
print "Diboson:        ",Diboson_all
print "QCD:            ",QCD_all
print "Total MC:       ",total_all
#print "Total MC error: ",total_error
print "Data:           ",data_all


data=[CutflowNameList,Wjets_all,ttbar_all,SingleTop_all,Diboson_all,QCD_all,total_all,data_all]
data_names=["","Wjets:","ttbar:","SingleTop:","Diboson:","QCD:","total MC:","data:"]

dash='_'*200
for i in range(len(data)):
    if i ==0:
        print(dash)
        print('{:<20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}'.format(data_names[i],data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5],data[i][6],data[i][7],data[i][8]))
        print(dash)
    if i == 7:
        print('{:<20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}'.format(data_names[i],data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5]))
    if i!=0 and i!=7:
        print('{:<20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}{:^20s}'.format(data_names[i],data[i][0],data[i][1],data[i][2],data[i][3],data[i][4],data[i][5],data[i][6],data[i][7],data[i][8]))


print(dash)
