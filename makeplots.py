#!/usr/bin/env python
#Finn Rebassoo, LLNL 05-05-2017
#Plot all the MC samples
from tools import *
from ROOT import *
import datetime

#MCsamples=["WWTo2L2Nu_13TeV-powheg","TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]
MCsamples=["WWTo2L2Nu_13TeV-powheg","TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8","ExclusiveWW"]
#MCsamples=["WWTo2L2Nu_13TeV-powheg","TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"]

gStyle.SetOptStat(0)

#List all the histograms in the root file
f0=TFile("histos/"+MCsamples[0]+".root")
#f=TFile.Open("histos/WWTo2L2Nu_13TeV-powheg.root")
f0.cd()
List=f0.GetListOfKeys()
it=0
histo_list=[]
for k1 in List:
    h1 = k1.ReadObj()
    it=it+1
    print "Histo {0}: {1}".format(it,h1.GetName())
    histo_list.append(h1.GetName())
print histo_list

#User inputs histograms to draw
user_input = raw_input("Input histogram or range of histos (1-5): ")
print(user_input)

u="h_fvtx_numtracks_Leptons"
u=user_input

#Here loop over all the plots we want to make
min=0
max=0
digits=False
if u[0].isdigit():
    min=int(u.split('-')[0])
    max=int(u.split('-')[1])
    digits=True
    print "True"
else:
    print "False"

#Need to set up the canvases
#for i in range(min,max+1):

c1=TCanvas()
udate=str(datetime.datetime.now())
pdffile="Plots-{0}-{1}-{2}.pdf".format(udate.split(' ')[0],udate.split(' ')[1].split(':')[0],udate.split(' ')[1].split(':')[1])
c1.Print(pdffile+'[')
#Loop over all the histos the user wants to plot. If the user chooses one name the min will be 0, max will be 1 (see above)
maxhisto=0
for i in range(min,max+1):

    c1.cd()
    leg=TLegend(0.45,0.56,0.623,0.886)
    print i
    print histo_list[i-1]
    #Plot MC
    hstack=THStack()
    hMC=[]
    fMC=[]
    it=0

    #Plot Data
    f_data=TFile("histos/MuonEG_total.root")
    #f_data=TFile("histos/MuonEG_runBCG.root")
    f_data.cd()
    if digits:
        h_data=f_data.Get(histo_list[i-1])
    else:    h_data=f_data.Get(u)
    h_data.SetMarkerStyle(8)
    h_data.SetMarkerColor(1)
    h_data.SetLineColor(1)
    #h_data.Scale(0.5)
    maxhisto_data=h_data.GetMaximum()
    print maxhisto_data
    #hstack.GetYaxis().SetRangeUser(0,maxhisto_data*1.15)
    #hstack.GetYaxis().SetRangeUser(0,4000)
    #hstack.Draw()
    #maxhisto=hstack.GetMaximum()
    print maxhisto
    #h_data.Draw("e")
    leg.AddEntry(f_data,"Data","p")
    print "Get out of data samples"

    PPSMCScale=1.
    if u == "h_fvtx_numtracks_Leptons_PPS":
        u="h_fvtx_numtracks_Leptons"
        PPSMCScale=(64./2111)

    for sample in MCsamples:
        print "Get to beginning of MC samples"
        fMC.append(TFile("histos/"+sample+".root"))
        fMC[it].cd()
        #This is if specified a range of histos
        if digits:
            hMC.append(fMC[it].Get(histo_list[i-1]))
        else: hMC.append(fMC[it].Get(u))
        ModifyHisto(hMC[it],sample)
        #Scale MC to data for PPS numextra tracks plot
        hMC[it].Scale(PPSMCScale)
        leg.AddEntry(hMC[it],legend_name(sample),"f")
        hstack.Add(hMC[it])
        it=it+1

    hstack.Draw()
    #f_data.Draw("samee")
    maxhisto=hstack.GetMaximum()
    if maxhisto > maxhisto_data:
        #hstack.Draw()
        h_data.GetYaxis().SetRangeUser(0,maxhisto*1.1)
        #h_data.Draw("e")
    h_data.Draw("e")
    hstack.Draw("same")
    h_data.Draw("esame")

    print maxhisto

    leg.Draw("same")

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(11)
    latex.DrawLatex(0.12,0.92,"CMS")
    #latex.DrawLatex(0.67,0.92,"37.2 fb^{-1} (13 TeV)")
    #All runs
    latex.DrawLatex(0.67,0.92,"35.8 fb^{-1} (13 TeV)")
    #RunBCG
    #latex.DrawLatex(0.67,0.92,"15.9 fb^{-1} (13 TeV)")
    #latex.DrawLatex(0.67,0.92,"4.39 fb^{-1} (13 TeV)")
    #latex.DrawLatex(0.67,0.92,"12.19 fb^{-1} (13 TeV)")
    #latex.DrawLatex(0.67,0.92,"7.8 fb^{-1} (13 TeV)")
    c1.Print(pdffile)


c1.Print(pdffile+']')
