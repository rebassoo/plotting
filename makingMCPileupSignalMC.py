#!/usr/bin/env python
#Finn Rebassoo, LLNL 12-03-2018
#Obtained recipe for this from: https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookFWLitePython
from ROOT import *
#import ROOT
import math as m
import sys
import time
import os
from DataFormats.FWLite import Events, Handle
import subprocess

#samples=['/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM']
#samples=['/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM']

#samples=['/ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM']
#samples=['/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM']
#samples=['/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM']

#samples=['/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM','/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAOD-PU2017_94X_mc2017_realistic_v11-v1/MINIAODSIM','/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAOD-PU2017_94X_mc2017_realistic_v11-v1/MINIAODSIM','/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM','/WZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/WW_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/ZZ_TuneCP5_13TeV-pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM','/ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt-20toInf_MuEnrichedPt15_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017RECOSIMstep_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM','/QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM','/QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM','/QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM','/QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM','/QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM','/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIFall17MiniAOD-94X_mc2017_realistic_v10-v1/MINIAODSIM']

count=0

fout = TFile('MCPileup.root','recreate')
fout.cd()
h_pileup=TH1F()
sample_name_nodash='a0W2point5e_6_alldecays_xi1to30pct'
h_pileup=TH1F("h_pileup_{0}".format(sample_name_nodash),"",100,0,100)
#for i in samples:
#    sample_name=i.split('/')[1]
#    sample_name_nodash=sample_name.replace("-","_")
#    h_pileup=TH1F("h_pileup_{0}".format(sample_name_nodash),"",100,0,100)
#    #h_pileup=TH1F()
#    print sample_name_nodash
#    #if count>0: continue
#    #list=subprocess.check_output('dasgoclient --query="file dataset=/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAOD-PU2017_94X_mc2017_realistic_v11-v1/MINIAODSIM" --limit=10',shell=True)
#    count=count+1
#    #list=subprocess.check_output('dasgoclient --query="file dataset={0}" --limit=1'.format(i),shell=True)
#    list=subprocess.check_output('dasgoclient --query="file dataset={0}"'.format(i),shell=True)
#    li=list.split("\n")
#    print li[0]

li=['/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_10.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_11.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_12.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_13.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_14.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_15.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_16.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_17.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_18.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_19.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_1.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_20.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_2.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_3.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_4.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_5.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_6.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_7.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_8.root',
    '/hadoop/cms/store/user/rebassoo/2018_12_17_SignalFiles2017Data/MINIAODSIM/step3_fpmc_exclww_a0W2point5e-6_alldecays_xi1to30pct_miniaodv2_9.root']

for ii in li:
    if len(ii)<10: continue
        #events = Events("root://cmsxrootd.fnal.gov/{0}".format(ii))
    events = Events("{0}".format(ii))
    handle  = Handle ('std::vector< PileupSummaryInfo >')
    label = ("slimmedAddPileupInfo")

    for event in events:
        event.getByLabel(label, handle)
        pileups=handle.product()
        h_pileup.Fill(pileups.begin().getTrueNumInteractions())
fout.cd()
h_pileup.Write()
#h_pileup[0].Draw()

#fout.Write()
fout.Close()