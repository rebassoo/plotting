#!/usr/bin/env python
#Finn Rebassoo, LLNL 05-05-2017
#Plot all the MC samples
#from ptools import *
from ROOT import *
#import ROOT
import datetime
import sys


isData=True


gStyle.SetOptStat(0)



#List all the histograms in the root file
#f_data=TFile("SingleMuonTotal.root")
#f_data=TFile("JustDataCorrectDistribution/SingleMuonTotal.root")
f_data=TFile("2019-10-14-AllData-AddingStripsUpdated/SingleMuonTotal.root")
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
digits=False
min=0
max=0
if u[0].isdigit():
    min=int(u.split('-')[0])
    max=int(u.split('-')[1])
    digits=True
    print "True"
else:
    print "False"


list1=u.split()
#f_data=TFile("histos/SingleMuonTotal.root")
count=0
c1 = TCanvas( 'c', 'Example', 500, 700 )
udate=str(datetime.datetime.now())
pdffile="Plots-{0}-{1}-{2}.pdf".format(udate.split(' ')[0],udate.split(' ')[1].split(':')[0],udate.split(' ')[1].split(':')[1])
#c1.Print(pdffile+'[')
count=0
peff=[]
for i in range(min,max+1):
#for i in list1:

    if digits:
        h_pass=f_data.Get(histo_list[i-1])
    else:
        h_pass=f_data.Get(u)
    total="h_nvertices_multi_all"
    if "nvertices_all" in histo_list[i-1]:
        total="h_nvertices_all"
    #total="h_nvertices_45_1"
    #total="h_nvertices_56_1"
    h_total=f_data.Get(total)

    peff.append(TEfficiency(h_pass,h_total))
    peff[count].SetLineColor(count+1)
    if count==0:
        if digits:
            peff[0].SetTitle(histo_list[i-1])
        else:
            peff[0].SetTitle(u)
        peff[0].Draw()

    else:
        peff[count].Draw("same")
    #c1.Print(pdffile)
    count=count+1
#leg.Draw("same")
#print list1
#c1.Print(pdffile+']')
c1.Print(pdffile)


