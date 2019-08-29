#!/usr/bin/env python                                                                                   
#Finn Rebassoo, LLNL 04-30-2019 
from ptools import *
from ROOT import *


_file0 = TFile("histos/quick/SingleMuonTotal.root")

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
h1=_file0.Get(histo_name_control)
h1.Rebin(10)
print "h_MWW_MX_control.GetEntries(): ",h1.GetEntries()
#h_MWW_MX_10_up.Scale(0.012282431)
h1.Sumw2()
h1.Scale(num/deno)
h1.SetStats(0)
h1.GetYaxis().SetRangeUser(0,10)
h1.Draw("e")

#h_MWW_MX_0_4_tracks_notPPS.Scale(0.098)
#h_MWW_MX_0_4_tracks_notPPS.Rebin(10)
#h_MWW_MX_0_4_tracks_notPPS.SetLineColor(2)
#h_MWW_MX_0_4_tracks_notPPS.Draw("esamehist")

histo_name="h_MWW_MX_0_4_tracks_Ycut"
#histo_name="h_MWW_MX_0_4_tracks"
#histo_name="h_Y_CMS_minus_RP_0_4_extratracks"


_file1 = TFile("histos/quick/ExclusiveWW_a0w1e-6-SingleLepton-2017.root")
##This is luminosity factor
h2=_file1.Get(histo_name)
print h2.Integral(0,1001)
#h2.Scale(0.166)
ModifyHisto(h2,"ExclusiveWW_a0w1e-6-SingleLepton-2017")
print h2.Integral(0,1001)
h2.SetLineColor(6)
h2.SetFillColor(0)
##h_MWW_MX_0_4_tracks->GetNbinsX()
h2.Rebin(10)
#h2.SetLineColor(6)
h2.Draw("histsame")
#h2.Draw()

