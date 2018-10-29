#!/usr/bin/env python
#Finn Rebassoo, LLNL 05-05-2017
#Plot all the MC samples
from ptools import *
from ROOT import *
import datetime
import sys


MCsamples=[
#"WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8",
"WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8",
"WW_TuneCP5_13TeV-pythia8",
"WZ_TuneCP5_13TeV-pythia8",
#"TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8",
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

#c1=TCanvas()

yswidth = 500.
ylwidth = 700.
scaleFacBottomPad = yswidth/float((ylwidth-yswidth))
yBorder = (ylwidth-yswidth)/float(ylwidth)
c1 = TCanvas( 'c', 'Example', 500, 700 )


udate=str(datetime.datetime.now())
pdffile="Plots-{0}-{1}-{2}.pdf".format(udate.split(' ')[0],udate.split(' ')[1].split(':')[0],udate.split(' ')[1].split(':')[1])
c1.Print(pdffile+'[')
#Loop over all the histos the user wants to plot. If the user chooses one name the min will be 0, max will be 1 (see above)
maxhisto=0

thisPad=TCanvas()
thisPad =c1
toppad=TPad()
bottompad=TPad()
thisPad.Divide(1,2,0,0)
toppad = thisPad.cd(1)
    #toppad.SetBottomMargin(0.02)
toppad.SetBottomMargin(0.0375)
toppad.SetTopMargin(0.05)
toppad.SetRightMargin(0.035)
toppad.SetPad(toppad.GetX1(), yBorder, toppad.GetX2(), toppad.GetY2())
bottompad = thisPad.cd(2)
bottompad.SetTopMargin(0)
bottompad.SetRightMargin(0.035);
bottompad.SetBottomMargin(scaleFacBottomPad*0.13);
bottompad.SetPad(bottompad.GetX1(), bottompad.GetY1(), bottompad.GetX2(), yBorder);
c1.cd()

for i in range(min,max+1):

    toppad.cd()
    leg=TLegend(0.72,0.56,0.886,0.886)
    print i
    print histo_list[i-1]
    #Plot MC
    hstack=THStack()
    hMC=[]
    fMC=[]
    it=0

    #Plot Data
    #f_data=TFile("histos/SingleMuon_Run2017C.root")
    #f_data=TFile("histos/SingleElectron_Run2017C.root")
    #f_data=TFile("histos/SingleMuonTotal.root")
    f_data=TFile("histos/SingleElectronTotal.root")
    f_data.cd()
    if digits:
        h_data=f_data.Get(histo_list[i-1])
    else:    h_data=f_data.Get(u)
    h_data.SetMarkerStyle(8)
    h_data.SetMarkerColor(1)
    h_data.SetMarkerSize(0.5)
    h_data.SetLineColor(1)
    #h_data.Sumw2()
    #h_data.Scale(0.5)
    h_data.Rebin(2)
    maxhisto_data=h_data.GetMaximum()
    print maxhisto_data
    #hstack.GetYaxis().SetRangeUser(0,maxhisto_data*1.15)
    #hstack.GetYaxis().SetRangeUser(0,4000)
    #hstack.Draw()
    #maxhisto=hstack.GetMaximum()
    print maxhisto
    h_data.Draw("e")
    leg.AddEntry(f_data,"Data","p")
    print "Get out of data samples"


    for sample in MCsamples:
        fMC.append(TFile("histos/"+sample+".root"))
        fMC[it].cd()
        #This is if specified a range of histos
        if digits:
            hMC.append(fMC[it].Get(histo_list[i-1]))
        else: hMC.append(fMC[it].Get(u))
        ModifyHisto(hMC[it],sample)
        #Scale MC to data for PPS numextra tracks plot
        hMC[it].Rebin(2)
        if sample =="WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8" or sample=="WW_TuneCP5_13TeV-pythia8" or sample=="WZ_TuneCP5_13TeV-pythia8" or sample=="TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8" or sample =="ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8" or sample =="QCD_Pt_170to300_TuneCP5_13TeV_pythia8" or sample=="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8" or sample =="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8":
            leg.AddEntry(hMC[it],legend_name(sample),"f")
        hstack.Add(hMC[it])
        it=it+1

    #hstack.Draw()
    #f_data.Draw("samee")
    maxhisto=hstack.GetMaximum()
    if maxhisto > maxhisto_data:
        #hstack.Draw()
        h_data.GetYaxis().SetRangeUser(0.01,maxhisto*1.1)
        #h_data.Draw("e")
    h_data.Draw("e")
    hstack.Draw("hist same")
    h_mc_errors=hstack.GetStack().Last().Clone()
    #print "Bin content: ",h_mc_errors.GetBinContent(5)
    #print "Bin Error: ",h_mc_errors.GetBinError(5)
    h_mc_errors.SetLineColor(1)
    h_mc_errors.SetFillStyle(2)
    h_mc_errors.SetFillColor(1)
    h_mc_errors.SetFillStyle(3005)
    h_mc_errors.Draw("e2,same")
    
    h_data.Draw("esame")
    gPad.RedrawAxis()

    print maxhisto

    leg.Draw("same")

    latex=TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(11)
    #latex.DrawLatex(0.12,0.92,"CMS")
    latex.DrawLatex(0.12,0.96,"CMS")
    
    #latex.DrawLatex(0.67,0.96,"8.681 fb^{-1} (13 TeV)")
    #latex.DrawLatex(0.67,0.92,"37.5 fb^{-1} (13 TeV)")
    latex.DrawLatex(0.67,0.96,"37.5 fb^{-1} (13 TeV)")



    bottompad.cd()

    h_ratio=TH1F()
    h_ratio = h_data.Clone()
    h_ratio.Divide(h_data,hstack.GetStack().Last())
    h_ratio.GetYaxis().SetRangeUser(0.5,1.5)
    h_ratio.SetStats(0)
    h_ratio.SetLineColor(4)
    h_ratio.GetXaxis().SetTitleSize(2*scaleFacBottomPad*h_ratio.GetXaxis().GetTitleSize())
    h_ratio.SetTitle("")
    h_ratio.GetXaxis().SetLabelSize(scaleFacBottomPad*h_ratio.GetXaxis().GetLabelSize())
    h_ratio.GetXaxis().SetTickLength(scaleFacBottomPad*h_ratio.GetXaxis().GetTickLength())
    h_ratio.GetYaxis().SetTitleSize(0.8*scaleFacBottomPad*h_ratio.GetYaxis().GetTitleSize())
    h_ratio.GetYaxis().SetLabelSize(.8*scaleFacBottomPad*h_ratio.GetYaxis().GetLabelSize())
    h_ratio.GetYaxis().SetTitle("Data / MC")
    h_ratio.GetYaxis().CenterTitle()
    h_ratio.GetXaxis().SetTitle(h_data.GetXaxis().GetTitle())
    h_ratio.GetXaxis().SetTitleOffset(0.75)
    h_ratio.GetXaxis().SetLabelOffset(0.006)
    h_ratio.GetYaxis().SetTitleOffset(1.25 / scaleFacBottomPad)
    h_ratio.GetYaxis().SetNdivisions(505);
    h_ratio.Draw()
    num_bins=h_data.GetNbinsX()
    max_line=h_data.GetBinLowEdge(num_bins+1)
    line=TLine(0,1,max_line,1)
    line.SetLineColor(kBlack);
    line.SetLineStyle(2);
    line.Draw("Same")
    c1.Print(pdffile)

c1.Print(pdffile+']')




