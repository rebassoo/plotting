#!/usr/bin/env python                                                                                   
#Finn Rebassoo, LLNL 04-30-2019 
import math as m
import sys
from ptools import *
from ROOT import *
from htools import *
#python makeSignalRegionPlotGeneral.py directory noYcut channel background_method signal_region

def makePlot(direc,Ycut,channel,background_method,signal_region):

    c=TCanvas("c","",800,800)
    c.cd()
 
    rebin=5
    directory=direc
    #######################################################################################
    #Make Signal plots
    #######################################################################################
    histo_name="h_MWW_MX_0_4_tracks"+"_"+signal_region
    if Ycut=="Ycut":     histo_name="h_MWW_MX_0_4_tracks_Ycut"+"_"+signal_region
    #_file1 = TFile("histos_electron/ExclusiveWW_a0w1e-6-SingleLepton-2017.root")
    _file1 = TFile("{0}/GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6.root".format(directory))
    h2=_file1.Get(histo_name)
    print h2.Integral(0,1001)
    ModifyHisto(h2,"GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6",directory)
    print h2.Integral(0,1001)
    h2.SetLineColor(6)
    h2.SetFillColor(0)
    h2.Rebin(rebin)
    h2.GetYaxis().SetRangeUser(0,2)
    h2.Draw("hist")

    histo_name="h_MWW_MX_0_4_tracks_misreco"+"_"+signal_region
    if Ycut=="Ycut":     histo_name="h_MWW_MX_0_4_tracks_misreco_Ycut"+"_"+signal_region
    #_file1 = TFile("histos_electron/ExclusiveWW_a0w1e-6-SingleLepton-2017.root")
    h3=_file1.Get(histo_name)
    print h3.Integral(0,1001)
    ModifyHisto(h3,"GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6",directory)
    print h3.Integral(0,1001)
    h3.SetLineColor(6)
    h3.SetLineStyle(2)
    h3.SetFillColor(0)
    h3.Rebin(rebin)
    h3.Draw("histsame")

    histo_name="h_MWW_MX_0_4_tracks_misreco"+"_"+signal_region
    if Ycut=="Ycut":     histo_name="h_MWW_MX_0_4_tracks_misreco_Ycut"+"_"+signal_region
    _file2 = TFile("{0}/GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6-noXiCut.root".format(directory))
    #histo_name="h_MWW_MX_0_4_tracks"+"_"+signal_region
    #if Ycut=="Ycut":     histo_name="h_MWW_MX_0_4_tracks_Ycut"+"_"+signal_region
    #_file2 = TFile("GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6-noXiCut.root")
    h4=_file2.Get(histo_name)
    print h4.Integral(0,1001)
    ModifyHisto(h4,"GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6-noXiCut",directory)
    print h4.Integral(0,1001)
    h4.SetLineColor(7)
    h4.SetLineStyle(2)
    h4.SetFillColor(0)
    h4.Rebin(rebin)
    h4.Draw("histsame")
    c.Print("test_{0}{1}.pdf".format(Ycut,signal_region))

if __name__=="__main__":
    #main(sys.argv[1],"h_MWW_MX_0_4_tracks","h_MWW_MX_5_up","muon")
    #if len(sys.argv)==5:
    #makePlot(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
    #directory="2020-04-29-MuonJustSignalMC-Dilepton-CMS-XiRequirements"
    directory="2020-04-30-MuonAllDataMC-XiCMSCut"
    makePlot(directory,"","muon","","MultiRP")
    #makePlot(directory,"","muon","","PixelPixel")
    #makePlot(directory,"","muon","","MultiPixel")
    #makePlot(directory,"Ycut","muon","","MultiRP")
    #makePlot(directory,"Ycut","muon","","PixelPixel")
    #makePlot(directory,"Ycut","muon","","MultiPixel")
