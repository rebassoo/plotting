#!/usr/bin/env python
#Finn Rebassoo, LLNL 05-05-2017
#Plot all the MC samples
from ptools import *
from ROOT import *
#import ROOT
import datetime
import sys

#rebin=128
rebin=2
channel="muon"
#channel="electron"
hdirectory="2020-09-23-ElectronAllDataMC"
#extra_tracks_weight=2.205
#extra_tracks_weight=1.042862
extra_tracks_weight=2.86
#extra_tracks_weight=1.81
#extra_tracks_weight=1.6835
#apply_extra_tracks_weight=True
apply_extra_tracks_weight=False


if channel=="muon": datafile="SingleMuonTotal.root"
if channel=="electron": datafile="SingleElectronTotal.root"

MCsignalsamples=[
#"ExclusiveWW_a0w2p5e-6-SingleLepton-2017",
#"ExclusiveWW_a0w1e-6-SingleLepton-2017",
#"ExclusiveWW_SM_FPMC-SingleLepton-2017"#,
"GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6-2018"
]

MCsamples2=["WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8"]
MCsamples=["WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8","WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
           "WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
           #"W1JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8","W1JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8",
           #"W1JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8","W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8",
           #"W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8","W2JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8",
           #"W2JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8","W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8",
           "DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8","DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
           "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8",
           #"TTJets_TuneCP5_13TeV-madgraphMLM-pythia8", 
           #"QCD_Pt_170to300_TuneCP5_13TeV_pythia8","QCD_Pt_300to470_TuneCP5_13TeV_pythia8",
           #"QCD_Pt_470to600_TuneCP5_13TeV_pythia8","QCD_Pt_600to800_TuneCP5_13TeV_pythia8",
           #"QCD_Pt_800to1000_TuneCP5_13TeV_pythia8","QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8",
           #"QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8","QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8",
           #"QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8","QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8",
           "ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8",
           "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
           "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
           "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
           "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
           #"ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8","ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8",
           #"ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8","ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
           #"ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
           "WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8",
           #"GGToWWToJJMuNu_PtL-15_13TeV-fpmc-herwig6"
           #"TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
           #"QCD_Pt-170to300_MuEnrichedPt5_TuneCP5_13TeV_pythia8",
           #"QCD_Pt-300to470_MuEnrichedPt5_TuneCP5_13TeV_pythia8",
           #"QCD_Pt-470to600_MuEnrichedPt5_TuneCP5_13TeV_pythia8",
           #"QCD_Pt-600to800_MuEnrichedPt5_TuneCP5_13TeV_pythia8",
           #"QCD_Pt-800to1000_MuEnrichedPt5_TuneCP5_13TeV_pythia8",
           #"QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8"
           #"DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8",
]

gStyle.SetOptStat(0)


#ratio=[2.21718335152,2.52607560158,2.46251106262,2.29587388039,2.08750772476,1.96914052963,1.6261909008,1.49893152714,1.33113884926,1.13561844826,0.975487530231,0.83882021904,0.713073134422,0.599662899971,0.545682013035,0.478854328394,0.410977452993,0.370541721582,0.386292546988,0.378802418709]
ratio=[2.42918777466,2.28876924515,2.11150622368,2.1433968544,1.96451759338,1.88715231419,1.53213500977,1.38876831532,1.26254463196,1.09296643734,0.954137682915,0.81217777729,0.688555657864,0.57609641552,0.534466266632,0.479912757874,0.410558223724,0.376152545214,0.379950582981,0.35912322998]



#List all the histograms in the root file
f0=TFile(hdirectory+"/"+MCsamples[0]+".root")
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
#print histo_list

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
toppad.SetLogy()
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
    #leg=TLegend(0.62,0.352,0.92,0.942)
    leg=TLegend(0.72,0.452,0.92,0.942)
    leg.SetFillColor(0)
    leg.SetLineColor(0)
    #leg.SetTextSize(0.035)
    leg.SetTextSize(0.022)
    leg.SetTextFont(42)
    print i
    print histo_list[i-1]

    #Plot Data
    f_data=TFile(hdirectory+"/"+datafile)
    #f_data=TFile("histos/2019-02-05/SingleElectronTotal.root")
    f_data.cd()
    if digits:
        h_data=f_data.Get(histo_list[i-1])
    else:    h_data=f_data.Get(u)
    h_data.SetMarkerStyle(8)
    h_data.SetMarkerColor(1)
    h_data.SetMarkerSize(0.5)
    h_data.SetLineColor(1)
    #h_data.Sumw2()
    #h_data.Scale(2.30522942543)
    h_data.Rebin(rebin)
    maxhisto_data=h_data.GetMaximum()
    print maxhisto_data
    #h_data.GetXaxis().SetRangeUser(0,200)
    h_data.GetYaxis().SetTitleOffset(1.4)
    h_data.GetYaxis().SetTitle("Events")
    #maxhisto=hstack.GetMaximum()
    print maxhisto
    h_data.SetMinimum(0.3)
    h_data.Draw("e")
    leg.AddEntry(h_data,"Data","p")
    print "Get out of data samples"

    hstack=THStack()
    hMC=[]
    fMC=[]
    it=0
    for sample in MCsamples:
        fMC.append(TFile(hdirectory+"/"+sample+".root"))
        #fMC.append(TFile("histos/2019-02-05/"+sample+".root"))
        fMC[it].cd()
        #This is if specified a range of histos
        if digits:
            hMC.append(fMC[it].Get(histo_list[i-1]))
        else: 
            #In this case all MC passes PPS, so need to modify to compare to data
            #if u=="h_num_extra_tracks_notPPS":
            #    u="h_num_extra_tracks_PPS"
            hMC.append(fMC[it].Get(u))
        #else: hMC.append(fMC[it].Get("h_num_extra_tracks_notPPS"))
        ModifyHisto(hMC[it],sample,hdirectory)
        if apply_extra_tracks_weight:
            hMC[it].Scale(extra_tracks_weight)
        #for i in range(0,20):
        #    content=hMC[it].GetBinContent(i+1)
        #    hMC[it].SetBinContent(i+1,content*ratio[i])
        hMC[it].Rebin(rebin)
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

    hsignalMC=[]
    fsignalMC=[]
    itt=0
    max=0
    for sample in MCsignalsamples:
        fsignalMC.append(TFile(hdirectory+"/"+sample+".root"))
        #fsignalMC.append(TFile("histos/2019-02-05/"+sample+".root"))
        fsignalMC[itt].cd()
        #This is if specified a range of histos
        if digits:
            hsignalMC.append(fsignalMC[itt].Get(histo_list[i-1]))
        else: hsignalMC.append(fsignalMC[itt].Get(u))
        ModifyHisto(hsignalMC[itt],sample,hdirectory)
        #Scale MC to data for PPS numextra tracks plot
        hsignalMC[itt].Rebin(rebin)
        hsignalMC[itt].SetFillColor(0)
        hsignalMC[itt].SetLineWidth(2)
        #hsignalMC[itt].SetLineStyle(2)
        maxhisto=hsignalMC[itt].GetMaximum()
        if maxhisto > maxhisto_data and maxhisto>max:
            max=hsignalMC[itt].GetMaximum()
        hsignalMC[itt].Draw("histsame")
        if "GG" in sample:
            leg.AddEntry(hsignalMC[itt],legend_name(sample),"l")            
        itt=itt+1

    #To plot just MC signal
    #h_data.GetYaxis().SetRangeUser(0.01,max*1.1)
    #h_data.Draw("e")
    #ittt=0
    #for sample in MCsignalsamples:
    #    hsignalMC[ittt].Draw("histsame")
    #    ittt=ittt+1

    #len_asignal=len(hsignalMC)
    #for sample in reversed(MCsignalsamples):
    #    if "ExclusiveWW" in sample:
    #        leg.AddEntry(hsignalMC[len_asignal-1],legend_name(sample),"l")            
    #    len_asignal=len_asignal-1

    len_a=len(hMC)
    for sample in reversed(MCsamples):
        if sample =="WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8" or sample=="WW_TuneCP5_13TeV-pythia8" or sample=="TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8" or sample =="ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8" or sample =="QCD_Pt_170to300_TuneCP5_13TeV_pythia8" or sample=="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8" or sample =="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8" or sample=="WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8" or sample =="DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8" or sample =="DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8" or sample == "W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8" or sample =="ExclusiveWW_SM_FPMC-SingleLepton-2017" or sample =="ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8":
            leg.AddEntry(hMC[len_a-1],legend_name(sample),"f")
        len_a=len_a-1

    f_err =TH1F("f_err","",10,0,10);
    f_err.SetFillColor(1);
    f_err.SetLineColor(0);
    f_err.SetFillStyle(3005);
    leg.AddEntry(f_err,"Stat. uncert. in simulation","f");

    leg.Draw("same")
    latex=TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(11)
    #latex.DrawLatex(0.12,0.92,"CMS")
    latex.DrawLatex(0.12,0.96,"CMS")
    latex.DrawLatex(0.67,0.96,"55.7 fb^{-1} (13 TeV)")



    bottompad.cd()

    h_ratio=TH1F()
    h_ratio = h_data.Clone()
    h_ratio.Divide(h_data,hstack.GetStack().Last())
    h_ratio.GetYaxis().SetRangeUser(0,3)
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
    for i in range(0,num_bins):
        print "Ratio, error: ",h_ratio.GetBinContent(i+1),h_ratio.GetBinError(i+1)
    max_line=h_data.GetBinLowEdge(num_bins+1)
    line=TLine(0,1,max_line,1)
    line.SetLineColor(kBlack);
    line.SetLineStyle(2);
    line.Draw("Same")
    c1.Print(pdffile)

c1.Print(pdffile+']')




