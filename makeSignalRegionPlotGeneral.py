#!/usr/bin/env python                                                                                   
#Finn Rebassoo, LLNL 04-30-2019 
import math as m
import sys
from ptools import *
from ROOT import *
from htools import *

def main(direc,Ycut,channel,background_method):

    backgroundMC=True
    rebin=5
    maximum=4

    fout=TFile("combined_shapes_{0}_{1}.root".format(channel,direc.split("-")[4]),"recreate")
    fout.cd()

    #signal_1e6=TH1F()
    #signal_2e6=TH1F()
    #signal_5e6=TH1F()
    #background=TH1F()
    #background_up=TH1F()
    #background_down=TH1F()
    #data_obs=TH1F()


    c=TCanvas("c","",800,800)
    c.cd()
    #directory="2019-11-05-Pixel-Pixel"
    #print directory
    directory=direc
    _file0=TFile()
    if channel=="muon":
        _file0 = TFile("{0}/SingleMuonTotal.root".format(directory))
    if channel=="electron":
        _file0 = TFile("{0}/SingleElectronTotal.root".format(directory))

    num=_file0.Get("h_MWW_extra_tracks_0_4_notPPS").GetEntries()
    print "Num of events in 0-4 extra tracks not PPS: ",num
    h1=TH1F()
    h0=TH1F()
    if background_method=="5_up" or background_method=="template_5up":
        deno=_file0.Get("h_MWW_extra_tracks_5_up_notPPS").GetEntries()
        histo_name_control="h_MWW_MX_5_up"
        if Ycut=="Ycut":     histo_name_control="h_MWW_MX_control_5_up_Ycut"
        h1=_file0.Get(histo_name_control)
        h1.Rebin(rebin)
        #print "h_MWW_MX_control.GetEntries(): ",h1.Integral(0,1001)
        h1.Sumw2()
        nbins=h1.GetNbinsX()
        scale_factor=num/deno
        print "Scale factor for high to low extra tracks for ABCD is: ",scale_factor
        scale_factor_error=scale_factor*(m.sqrt(1/num+1/deno))
        for i in range(0,nbins+2):
            entry=h1.GetBinContent(i)
            entry_error=h1.GetBinError(i)
            if scale_factor > 0 and entry > 0:
                total_bin_error=m.sqrt( m.pow((scale_factor_error/scale_factor),2) + m.pow(entry_error/entry,2)  )
            else:
                total_bin_error=0
            h1.SetBinContent(i,entry*scale_factor)
            h1.SetBinError(i,entry*scale_factor*total_bin_error)
        h1.SetStats(0)
        h1.GetYaxis().SetRangeUser(0,maximum)
        h1.GetXaxis().SetTitle("M_{WW}/M_{X}")
        h1.GetYaxis().SetTitle("Events")
        print "Data total prediction: ",h1.Integral(0,1001) 
        h1.Draw("e")
        h0=h1.Clone()
        h0.SetLineColor(2)
        h0.SetLineWidth(2)
        h_control=_file0.Get("h_MWW_5_up")
        h_control_notPPS=_file0.Get("h_MWW_extra_tracks_5_up_notPPS")
        ratio=h_control.GetEntries()/h_control_notPPS.GetEntries()
        ratioMC=h_control.GetEntries()/(h_control.GetEntries()+h_control_notPPS.GetEntries())
        print "Ratio: ",ratio


    if background_method=="template":
        deno=_file0.Get("h_MWW_extra_tracks_5_15_notPPS").GetEntries()
        h1=_file0.Get("h_MWW_MX_control_notPPS")
        if Ycut=="Ycut": h1=_file0.Get("h_MWW_MX_control_Ycut_notPPS")
        h1.Scale(num/deno)

        h_control_temp=_file0.Get("h_MX_control")
        h_control_notPPS_temp=_file0.Get("h_MX_control_notPPS")
        ratio=h_control_temp.GetEntries()/h_control_notPPS_temp.GetEntries()
        ratioMC=h_control_temp.GetEntries()/(h_control_temp.GetEntries()+h_control_notPPS_temp.GetEntries())
        print "Ratio: ",ratio

        h1.Scale(ratio)
        h1.Rebin(rebin)
        h1.Sumw2()
        h1.SetStats(0)
        h1.GetYaxis().SetRangeUser(0,10)
        h1.GetXaxis().SetTitle("MWW/MX")
        h1.GetYaxis().SetTitle("Events")
        print "Data total prediction: ",h1.Integral(0,1001) 
        h1.SetMaximum(maximum)
        h1.Draw("e")

    if background_method=="template_5up":
        deno=_file0.Get("h_MWW_extra_tracks_5_up_notPPS").GetEntries()
        h1=_file0.Get("h_MWW_MX_5_up_notPPS")
        if Ycut=="Ycut": h1=_file0.Get("h_MWW_MX_5_up_Ycut_notPPS")
        h1.Scale(num/deno)
        print "Scale factor for high to low extra tracks for template_5up is: ",scale_factor
        h_control_temp=_file0.Get("h_MWW_5_up")
        #h_control_notPPS_temp=_file0.Get("h_MX_control_notPPS")
        h_control_notPPS_temp=_file0.Get("h_MWW_extra_tracks_5_up_notPPS")
        ratio=h_control_temp.GetEntries()/h_control_notPPS_temp.GetEntries()
        ratioMC=h_control_temp.GetEntries()/(h_control_temp.GetEntries()+h_control_notPPS_temp.GetEntries())
        print "Ratio: ",ratio

        h1.Scale(ratio)
        h1.Rebin(rebin)
        h1.Sumw2()
        h1.SetStats(0)
        h1.GetYaxis().SetRangeUser(0,10)
        h1.GetXaxis().SetTitle("MWW/MX")
        h1.GetYaxis().SetTitle("Events")
        print "Data total prediction: ",h1.Integral(0,1001) 
        h1.SetMaximum(maximum)
        h1.Draw("e")


    #h0.Draw()
    #h1.Draw("same")
    #sys.exit(1)
    h1.SetLineColor(1)
    h1.SetLineWidth(2)
    h1.SetMarkerStyle(22)

    #######################################################################################
    #Make Signal plots
    #######################################################################################
    histo_name="h_MWW_MX_0_4_tracks"
    if Ycut=="Ycut":     histo_name="h_MWW_MX_0_4_tracks_Ycut"
    #_file1 = TFile("histos_electron/ExclusiveWW_a0w1e-6-SingleLepton-2017.root")
    _file1 = TFile("{0}/GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6.root".format(directory))
    h2=_file1.Get(histo_name)
    print h2.Integral(0,1001)
    ModifyHisto(h2,"GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6",directory)
    print h2.Integral(0,1001)
    h2.SetLineColor(6)
    h2.SetFillColor(0)
    h2.Rebin(rebin)
    h2.Draw("histsame")

    _file2=TFile()
    h3=TH1F()
    if channel=="muon":
        _file2 = TFile("{0}/GGToWWToJJMuNu_PtL-15_13TeV-fpmc-herwig6.root".format(directory))
        h3=_file2.Get(histo_name)
        ModifyHisto(h3,"GGToWWToJJMuNu_PtL-15_13TeV-fpmc-herwig6",directory)
    if channel=="electron":
        _file2 = TFile("{0}/GGToWWToJJENu_PtL-15_13TeV-fpmc-herwig6.root".format(directory))       
        h3=_file2.Get(histo_name)
        ModifyHisto(h3,"GGToWWToJJENu_PtL-15_13TeV-fpmc-herwig6",directory)

    h3.SetFillColor(0)
    h3.Rebin(rebin)
    h3.SetLineColor(1)
    h3.Draw("histsame")

    _file3 = TFile("{0}/GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6.root".format(directory))
    h4=_file3.Get(histo_name)
    print h4.Integral(0,1001)
    ModifyHisto(h4,"GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6",directory)
    print h4.Integral(0,1001)
    h4.SetLineColor(7)
    h4.SetFillColor(0)
    h4.Rebin(rebin)
    h4.Draw("histsame")

    _file5 = TFile("{0}/GGToWW_bSM-A0W5e-6_13TeV-fpmc-herwig6.root".format(directory))
    h5=_file5.Get(histo_name)
    print h5.Integral(0,1001)
    ModifyHisto(h5,"GGToWW_bSM-A0W5e-6_13TeV-fpmc-herwig6",directory)
    print h5.Integral(0,1001)
    h5.SetLineColor(40)
    h5.SetFillColor(0)
    h5.Rebin(rebin)
    h5.Draw("histsame")


    #sys.exit(1)

    #######################################################################################
    #Make Background plots
    #######################################################################################

    MCsamples=[#"WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8","WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8","WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
        "W1JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8", "W1JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8","W1JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8","W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8","W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8","W2JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8","W2JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8","W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8",
        #"DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",#"DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",#"DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
        "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8",
        #"QCD_Pt_170to300_TuneCP5_13TeV_pythia8",
        #"QCD_Pt_300to470_TuneCP5_13TeV_pythia8",
        #"QCD_Pt_470to600_TuneCP5_13TeV_pythia8",
        #"QCD_Pt_600to800_TuneCP5_13TeV_pythia8",
        #"QCD_Pt_800to1000_TuneCP5_13TeV_pythia8",
        #"QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8",
        #"QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8",
        #"QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8",
        #"QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8",
        #"QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8",
        "ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8",
        "ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8",
        "ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8",
        "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
        "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
        "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8",
        "WW_TuneCP5_13TeV-pythia8",
        "WZ_TuneCP5_13TeV-pythia8",
        "ZZ_TuneCP5_13TeV-pythia8"
    ]

    leg=TLegend(0.61,0.402,0.81,0.892)
    leg.SetFillColor(0)
    leg.SetLineColor(0)
    leg.SetTextSize(0.022)
    leg.SetTextFont(42)
    leg.AddEntry(h0,"ABCD prediction","lep")
    leg.AddEntry(h1,"Template prediction","lep")

    if backgroundMC:
        histo_name="h_MWW_MX_0_4_tracks_100events"
        if Ycut=="Ycut":     histo_name="h_MWW_MX_0_4_tracks_100events_Ycut"
        hstack=THStack()
        hMC=[]
        fMC=[]
        it=0
        u=histo_name
        digits=False
        apply_extra_tracks_weight=True
        if channel=="muon":
            extra_tracks_weight=2.2*ratioMC
        if channel=="electron":
            extra_tracks_weight=1.6835*ratioMC
        for sample in MCsamples:
            fMC.append(TFile(directory+"/"+sample+".root"))
            fMC[it].cd()
            #This is if specified a range of histos
            if digits:
                hMC.append(fMC[it].Get(histo_list[i-1]))
            else: hMC.append(fMC[it].Get(u))
            ModifyHisto(hMC[it],sample,directory)
            if apply_extra_tracks_weight:
                hMC[it].Scale(extra_tracks_weight)
            hMC[it].Rebin(rebin)
            hstack.Add(hMC[it])
            it=it+1

        leg.AddEntry(h2,legend_name("ExclusiveWW_a0w1e-6-SingleLepton-2017"),"l")
        leg.AddEntry(h4,legend_name("ExclusiveWW_a0w2e-6-SingleLepton-2017"),"l")
        leg.AddEntry(h5,legend_name("ExclusiveWW_a0w5e-6-SingleLepton-2017"),"l")
        leg.AddEntry(h3,legend_name("ExclusiveWW_SM_FPMC-SingleLepton-2017"),"l")

        len_a=len(hMC)
        for sample in reversed(MCsamples):
            if sample =="WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8" or sample=="WW_TuneCP5_13TeV-pythia8" or sample=="TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8" or sample =="ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8" or sample =="QCD_Pt_170to300_TuneCP5_13TeV_pythia8" or sample=="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8" or sample =="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8" or sample=="WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8" or sample =="DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8" or sample =="DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8" or sample == "W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8" or sample =="ExclusiveWW_SM_FPMC-SingleLepton-2017":
                leg.AddEntry(hMC[len_a-1],legend_name(sample),"f")
            len_a=len_a-1


        hstack.SetMaximum(maximum)
        hstack.Draw("hist same")
        h_mc_errors=hstack.GetStack().Last().Clone()
        h_mc_errors.SetLineColor(1)
        h_mc_errors.SetFillStyle(2)
        h_mc_errors.SetFillColor(1)
        h_mc_errors.SetFillStyle(3005)
        h_mc_errors.Draw("e2 same")

    h0.Draw("esame")
    h1.Draw("esame")
    h2.Draw("histsame")
    h3.Draw("histsame")
    h4.Draw("histsame")
    h5.Draw("histsame")

    diff_up=h1.Clone()
    diff_down=h1.Clone()
    bins_x=h0.GetNbinsX()
    for i in range(0,bins_x+1):
        h0_bc=h0.GetBinContent(i)
        h1_bc=h1.GetBinContent(i)
        diff=abs(h0_bc-h1_bc)
        print diff
        diff_up.SetBinContent(i,h1_bc+diff)
        diff_down.SetBinContent(i,h1_bc-diff)

    fout.cd()
    h1.Write("background")
    diff_up.Write("background_alphaUp")
    diff_down.Write("background_alphaDown")
    #h1.Scale(2)
    data_obs=h1.Clone()
    data_obs.Add(h1,h3)
    data_obs.Write("data_obs")
    #h1.Write("data_obs")
    h2.Write("signal_1e6")
    h3.Write("background_ExclWW")
    h4.Write("signal_2e6")
    h5.Write("signal_5e6")
    fout.Write()
    fout.Close()

    leg.Draw("same")
    latex=TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(11)
    #latex.DrawLatex(0.12,0.96,"CMS")
    ycut_str=""
    if Ycut=="Ycut":
        ycut_str="_ycut"
    if channel=="muon":
        latex.DrawLatex(0.17,0.80,"{0}".format(directory[11:]))
    if channel=="electron":
        latex.DrawLatex(0.17,0.80,"{0}".format(directory[11:]))
    c.Print("BackgroundPrediction_{0}_{1}{2}.pdf".format(directory[11:],background_method,ycut_str))

if __name__=="__main__":
    #main(sys.argv[1],"h_MWW_MX_0_4_tracks","h_MWW_MX_5_up","muon")
    #if len(sys.argv)==5:
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
