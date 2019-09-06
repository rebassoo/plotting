#!/usr/bin/env python                                                                                   
#Finn Rebassoo, LLNL 04-30-2019 
import math as m
from ptools import *
from ROOT import *



directory="histos_electron"
_file0 = TFile("{0}/SingleElectronTotal.root".format(directory))

#h_MWW_extra_tracks_0_4_notPPS->GetEntries()
#h_MWW_extra_tracks_9_up_notPPS->GetEntries()
#h_MWW_MX_10_up.Rebin(10)
#h_MWW_MX_10_up.Scale(0.012282431)
#h_MWW_MX_10_up.Draw("e")


num=h_MWW_extra_tracks_0_4_notPPS.GetEntries()
deno=h_MWW_extra_tracks_5_15_notPPS.GetEntries()
#deno=h_MWW_900_extra_tracks_5_15_notPPS.GetEntries()
print "num: ",num
print "deno: ",deno
histo_name_control="h_MWW_MX_control_Ycut"
#histo_name_control="h_MWW_MX_control"
h1=_file0.Get(histo_name_control)
h1.Rebin(10)
print "h_MWW_MX_control.GetEntries(): ",h1.GetEntries()
#h_MWW_MX_10_up.Scale(0.012282431)
h1.Sumw2()
nbins=h1.GetNbinsX()
scale_factor=num/deno
scale_factor_error=scale_factor*(m.sqrt(1/num+1/deno))
for i in range(0,nbins+1):
    entry=h1.GetBinContent(i)
    entry_error=h1.GetBinError(i)
    if scale_factor > 0 and entry > 0:
        total_bin_error=m.sqrt( m.pow((scale_factor_error/scale_factor),2) + m.pow(entry_error/entry,2)  )
    else:
        total_bin_error=0
    h1.SetBinContent(i,entry*scale_factor)
    h1.SetBinError(i,entry*scale_factor*total_bin_error)
    #h1.SetBinError(i,0)
#h1.Scale(num/deno)
h1.SetStats(0)
h1.GetYaxis().SetRangeUser(0,5)
print "Data total prediction: ",h1.Integral(0,1001) 
h1.Draw("e")

#h_MWW_MX_0_4_tracks_notPPS.Scale(0.098)
#h_MWW_MX_0_4_tracks_notPPS.Rebin(10)
#h_MWW_MX_0_4_tracks_notPPS.SetLineColor(2)
#h_MWW_MX_0_4_tracks_notPPS.Draw("esamehist")

histo_name="h_MWW_MX_0_4_tracks_Ycut"
#histo_name="h_MWW_MX_0_4_tracks"
#histo_name="h_Y_CMS_minus_RP_0_4_extratracks"


#_file1 = TFile("histos_electron/ExclusiveWW_a0w1e-6-SingleLepton-2017.root")
_file1 = TFile("{0}/GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6.root".format(directory))
##This is luminosity factor
h2=_file1.Get(histo_name)
print h2.Integral(0,1001)
#h2.Scale(0.166)
#ModifyHisto(h2,"ExclusiveWW_a0w1e-6-SingleLepton-2017")
ModifyHisto(h2,"GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6")
print h2.Integral(0,1001)
h2.SetLineColor(6)
h2.SetFillColor(0)
##h_MWW_MX_0_4_tracks->GetNbinsX()
h2.Rebin(10)
#h2.SetLineColor(6)
h2.Draw("histsame")
#h2.Draw()


#_file2 = TFile("{0}/GGToWWToJJMuNu_PtL-15_13TeV-fpmc-herwig6.root".format(directory))
_file2 = TFile("{0}/GGToWWToJJENu_PtL-15_13TeV-fpmc-herwig6.root".format(directory))
#_file2 = TFile("histos_muon/ExclusiveWW_a0w1e-6-SingleLepton-2017.root")
h3=_file2.Get(histo_name)
#ModifyHisto(h3,"GGToWWToJJMuNu_PtL-15_13TeV-fpmc-herwig6")
ModifyHisto(h3,"GGToWWToJJENu_PtL-15_13TeV-fpmc-herwig6")
#ModifyHisto(h3,"ExclusiveWW_a0w1e-6-SingleLepton-2017")
h3.SetFillColor(0)
h3.Rebin(10)
h3.SetLineColor(1)
h3.Draw("histsame")

