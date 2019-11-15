#!/usr/bin/env python
#Finn Rebassoo, LLNL 05-05-2017
#Plot all the MC samples
from ptools import *
from ROOT import *
#import ROOT
import datetime
import sys


isData=True


gStyle.SetOptStat(0)



#List all the histograms in the root file
#f_data=TFile("SingleMuonTotal.root")
#f_data=TFile("JustDataCorrectDistribution/SingleMuonTotal.root")
f_data=TFile("./2019-11-04-MultiRP/SingleMuonTotal.root")
#JustDataCorrectDistributionNoPPSDataMixed/SingleMuonTotal.root")
#f_data=TFile("histos_justDataProperMixing/SingleLeptonTotal.root")
f_data.cd()
List=f_data.GetListOfKeys()
it=0
histo_list=[]
for k1 in List:
    h1 = k1.ReadObj()
    it=it+1
    print "Histo {0}: {1}".format(it,h1.GetName())
    histo_list.append(h1.GetName())
#print histo_list

#User inputs histograms to draw
user_input = raw_input("Input histogram or range of histos (1-5): ")
print(user_input)

u="h_fvtx_numtracks_Leptons"
u=user_input

list1=u.split()
#f_data=TFile("histos/SingleMuonTotal.root")
count=0
leg=TLegend(0.72,0.56,0.886,0.886)
h_leg_list=[]
for i in list1:
    print i
    h_data=f_data.Get(i)
    h_data.Rebin(5)
    integral_1=h_data.Integral(0,1001)
    h_data.Scale(1/integral_1)
    h_data.SetMarkerStyle(8)
    h_data.SetMarkerColor(1)
    h_data.SetMarkerSize(0.5)
    h_data.SetLineColor(count+1)
    h_leg=TH1F()
    h_leg.SetLineColor(count+1)
    h_leg_list.append(h_leg)
    leg.AddEntry(h_leg_list[count],i,"l")
    if count==0:
        h_data.Draw("ehist")
    else: 
        h_data.Draw("ehistsame")
    count=count+1

leg.Draw("same")
#print list1



