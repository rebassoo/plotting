#!/usr/bin/env python                                                                                   
#Finn Rebassoo, LLNL 04-30-2019 
import math as m
import sys
from ptools import *
from ROOT import *
from htools import *
#python makeSignalRegionPlotGeneral.py directory noYcut channel background_method signal_region

def makePlot(direc,Ycut,channel,background_method,signal_region,justSignal=False):

    backgroundMC=True
    rebin=5
    maximum=4

    #print channel
    #print direc.split("-")[4]
    #fout=TFile("combined_shapes_{0}_{1}.root".format(channel,direc.split("-")[4]),"recreate")
    fout=TFile("combined_shapes_{0}_{1}.root".format(channel,signal_region.lower()),"recreate")
    fout.cd()

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
        #histo_name_control="h_MWW_MX_5_up"
        histo_name_control="h_MWW_MX_5_up"+"_"+signal_region
        if Ycut=="Ycut":     histo_name_control="h_MWW_MX_control_5_up_Ycut"+"_"+signal_region
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
        h_control=_file0.Get("h_MWW_5_up"+"_"+signal_region)
        #h_control_notPPS=_file0.Get("h_MWW_extra_tracks_5_up_notPPS")
        h_control_notPPS=_file0.Get("h_MWW_extra_tracks_5_up_notPPS")
        ratio=h_control.GetEntries()/h_control_notPPS.GetEntries()
        ratioMC=h_control.GetEntries()/(h_control.GetEntries()+h_control_notPPS.GetEntries())
        print "Ratio: ",ratio


    if background_method=="template":
        deno=_file0.Get("h_MWW_extra_tracks_5_15_notPPS").GetEntries()
        h1=_file0.Get("h_MWW_MX_control_notPPS"+"_"+signal_region)
        if Ycut=="Ycut": h1=_file0.Get("h_MWW_MX_control_Ycut_notPPS"+"_"+signal_region)
        h1.Scale(num/deno)

        h_control_temp=_file0.Get("h_MX_control"+"_"+signal_region)
        h_control_notPPS_temp=_file0.Get("h_MX_control_notPPS"+"_"+signal_region)
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
        h1=_file0.Get("h_MWW_MX_5_up_notPPS"+"_"+signal_region)
        if Ycut=="Ycut": h1=_file0.Get("h_MWW_MX_5_up_Ycut_notPPS"+"_"+signal_region)
        #h1.Scale(num/deno)
        print "Scale factor for high to low extra tracks for template_5up is: ",scale_factor
        h_control_temp=_file0.Get("h_MWW_5_up"+"_"+signal_region)
        #h_control_notPPS_temp=_file0.Get("h_MX_control_notPPS")
        h_control_notPPS_temp=_file0.Get("h_MWW_extra_tracks_5_up_notPPS")
        ratio=h_control_temp.GetEntries()/h_control_notPPS_temp.GetEntries()
        ratioMC=h_control_temp.GetEntries()/(h_control_temp.GetEntries()+h_control_notPPS_temp.GetEntries())
        print "Ratio: ",ratio
        print "RatioMC: ",ratioMC

        #h1.Scale(num/deno)
        ##This is for the case where take events not Passing PPS and force every event to mix with control region
        ##h1.Scale(ratio)
        scale_factor_1=num/deno
        num2=_file0.Get("h_pfcand_nextracks_MjetVeto_WleptonicCuts_wJetPruning").GetEntries()
        den2=_file0.Get("h_MWW_notPPS").GetEntries()
        #ratio=h_pfcand_nextracks_MjetVeto_WleptonicCuts_wJetPruning.GetEntries()/h_MWW_notPPS.GetEntries()
        ratio=num2/den2
        #ratio=1.
        #h1.Scale(ratio)
        scale_factor_2=ratio
        scale_factor_1_error=scale_factor_1*(m.sqrt(1/num+1/deno))
        #scale_factor_2_error=scale_factor_2*(m.sqrt(1/(h_control_temp.GetEntries())+1/(h_control_notPPS_temp.GetEntries())))
        #scale_factor_2_error=scale_factor_2*(m.sqrt(1/(h_MWW_notPPS.GetEntries())+1/(h_pfcand_nextracks_MjetVeto_WleptonicCuts_wJetPruning.GetEntries())))
        scale_factor_2_error=scale_factor_2*(m.sqrt(1/(num2)+1/(den2) ) )
        #scale_factor_2_error=1.
        nbins=h1.GetNbinsX()
        for i in range(0,nbins+2):
            entry=h1.GetBinContent(i)
            entry_error=h1.GetBinError(i)
            if scale_factor > 0 and entry > 0:
                total_bin_error=m.sqrt( m.pow((scale_factor_1_error/scale_factor_1),2) + m.pow(entry_error/entry,2) +m.pow((scale_factor_2_error/scale_factor_2),2) )
            else:
                total_bin_error=0
            h1.SetBinContent(i,entry*scale_factor_1*scale_factor_2)
            h1.SetBinError(i,entry*scale_factor_1*scale_factor_2*total_bin_error)


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
    histo_name="h_MWW_MX_0_4_tracks"+"_"+signal_region
    if Ycut=="Ycut":     histo_name="h_MWW_MX_0_4_tracks_Ycut"+"_"+signal_region

    histo_name_misreco="h_MWW_MX_0_4_tracks_misreco"+"_"+signal_region
    if Ycut=="Ycut":     histo_name_misreco="h_MWW_MX_0_4_tracks_misreco_Ycut"+"_"+signal_region

    SignalSamples=[
    "GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6.root",
    "GGToWWToJJMuNu_PtL-15_13TeV-fpmc-herwig6.root",
    "GGToWWToJJENu_PtL-15_13TeV-fpmc-herwig6.root",
    "GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6.root",    
    "GGToWW_bSM-A0W5e-6_13TeV-fpmc-herwig6.root",
    "GGToWW_bSM-ACW5e-6_13TeV-fpmc-herwig6.root",
    "GGToWW_bSM-ACW8e-6_13TeV-fpmc-herwig6.root",
    "GGToWW_bSM-ACW2e-5_13TeV-fpmc-herwig6.root"
    ]
    fSig=[]
    hSig=[]
    hSigMisReco=[]
    it=0
    #directory_muon="2020-04-29-MuonJustSignalMC-Dilepton"
    #directory_electron="2020-04-29-ElectronJustSignalMC-Dilepton"
    for sig in SignalSamples:
        if "MuNu" in sig and channel=="electron":
            continue
        if "ENu" in sig and channel=="muon":
            continue
        fSig.append(TFile("{0}/".format(directory)+sig))
        fSig[it].cd()
        hSig.append(fSig[it].Get(histo_name))
        hSigMisReco.append(fSig[it].Get(histo_name_misreco))
        #print sig[:-5]
        ModifyHisto(hSig[it],sig[:-5],directory)
        hSig[it].Rebin(rebin)
        hSig[it].SetLineColor(6+it)
        if it > 3:
            hSig[it].SetLineColor(42+it)
        hSig[it].SetFillColor(0)
        if justSignal and it==0:
            hSig[it].SetStats(0)
            hSig[it].SetMaximum(maximum)
            hSig[it].GetXaxis().SetTitle("MWW/MX")
            hSig[it].GetYaxis().SetTitle("Events")
            hSig[it].Draw("hist")
        hSig[it].Draw("histsame")
        #ModifyHisto(hSigMisReco[it],sig[:-5],directory_muon)
        ModifyHisto(hSigMisReco[it],sig[:-5],directory)
        hSigMisReco[it].Rebin(rebin)
        hSigMisReco[it].SetLineColor(6+it)
        hSigMisReco[it].SetFillColor(0)
        hSigMisReco[it].SetLineStyle(2)
        hSigMisReco[it].Draw("histsame")
        it=it+1

    leg=TLegend(0.61,0.402,0.81,0.892)
    leg.SetFillColor(0)
    leg.SetLineColor(0)
    leg.SetTextSize(0.022)
    leg.SetTextFont(42)
    if not justSignal:
        leg.AddEntry(h0,"ABCD prediction","lep")
        leg.AddEntry(h1,"Template prediction","lep")

    leg.AddEntry(hSig[0],legend_name("ExclusiveWW_a0w1e-6-SingleLepton-2017"),"l")
    leg.AddEntry(hSig[2],legend_name("ExclusiveWW_a0w2e-6-SingleLepton-2017"),"l")
    leg.AddEntry(hSig[3],legend_name("ExclusiveWW_a0w5e-6-SingleLepton-2017"),"l")
    leg.AddEntry(hSig[4],legend_name("ExclusiveWW_aCw5e-6-SingleLepton-2017"),"l")
    leg.AddEntry(hSig[5],legend_name("ExclusiveWW_aCw8e-6-SingleLepton-2017"),"l")
    leg.AddEntry(hSig[6],legend_name("ExclusiveWW_aCw2e-5-SingleLepton-2017"),"l")
    leg.AddEntry(hSig[1],legend_name("ExclusiveWW_SM_FPMC-SingleLepton-2017"),"l")

    #leg.AddEntry(hSig[0],"misreco, "+legend_name("ExclusiveWW_a0w1e-6-SingleLepton-2017"),"l")
    #leg.AddEntry(hSig[1],"misreco, "+legend_name("ExclusiveWW_SM_FPMC-SingleLepton-2017"),"l")
    #leg.AddEntry(hSig[2],"misreco, "+legend_name("ExclusiveWW_a0w2e-6-SingleLepton-2017"),"l")
    #leg.AddEntry(hSig[3],"misreco, "+legend_name("ExclusiveWW_a0w5e-6-SingleLepton-2017"),"l")
    
    if justSignal:
        leg.Draw("same")
        writePlots(c,Ycut,channel,signal_region,"",justSignal)
        _file0.Close()
        fout.Close()
        return 0

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

    if backgroundMC:
        #directory="2020-04-24-MuonAllSignalRegions"
        histo_name="h_MWW_MX_0_4_tracks_100events"+"_"+signal_region
        #histo_name="h_MWW_MX_0_4_tracks_100events_jet_eta_0_1p5"
        if Ycut=="Ycut":     histo_name="h_MWW_MX_0_4_tracks_100events_Ycut"+"_"+signal_region
        #if Ycut=="Ycut":     histo_name="h_MWW_MX_0_4_tracks_100events_Ycut_jet_eta_0_1p5"
        hstack=THStack()
        hMC=[]
        fMC=[]
        it=0
        u=histo_name
        digits=False
        apply_extra_tracks_weight=True
        if channel=="muon":
            #extra_tracks_weight=2.2*ratioMC
            #extra_tracks_weight=2.2
            #extra_tracks_weight=2.3
            #extra_tracks_weight=2.58
            extra_tracks_weight=2.16
        if channel=="electron":
            #extra_tracks_weight=1.6835*ratioMC
            #extra_tracks_weight=1.6835
            #extra_tracks_weight=1.9
            extra_tracks_weight=2.41
        for sample in MCsamples:
            fMC.append(TFile(directory+"/"+sample+".root"))
            fMC[it].cd()
            #This is if specified a range of histos
            if digits:
                hMC.append(fMC[it].Get(histo_list[i-1]))
            else: hMC.append(fMC[it].Get(u))
            ModifyHisto(hMC[it],sample,directory)
            if apply_extra_tracks_weight:
                hMC[it].Sumw2()
                #hMC[it].Scale(extra_tracks_weight*10.)
                hMC[it].Scale(extra_tracks_weight)
            hMC[it].Rebin(rebin)
            hstack.Add(hMC[it])
            it=it+1


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
    hSig[0].Draw("histsame")
    hSig[1].Draw("histsame")
    hSig[2].Draw("histsame")
    hSig[3].Draw("histsame")
    #h2.Draw("histsame")
    #h3.Draw("histsame")
    #h4.Draw("histsame")
    #h5.Draw("histsame")

    diff_up=h1.Clone()
    diff_down=h1.Clone()
    bins_x=h0.GetNbinsX()
    for i in range(0,bins_x+1):
        h0_bc=h0.GetBinContent(i)
        h1_bc=h1.GetBinContent(i)
        diff=abs(h0_bc-h1_bc)
        print diff
        #diff_up.SetBinContent(i,h1_bc+diff)
        #diff_down.SetBinContent(i,h1_bc-diff)
        diff_up.SetBinContent(i,h0_bc+diff)
        diff_down.SetBinContent(i,h0_bc-diff)

    fout.cd()
    #h1.Write("background")
    #This uses ABCD as default
    h0.Write("background")
    diff_up.Write("background_alphaUp")
    diff_down.Write("background_alphaDown")
    data_obs=h1.Clone()
    data_obs.Add(h1,hSig[1])
    data_obs.Write("data_obs")
    hSig[1].Write("background_ExclWW")
    hSig[0].Write("signal_a0w_1e-6")
    hSig[2].Write("signal_a0w_2e-6")
    hSig[3].Write("signal_a0w_5e-6")
    hSig[4].Write("signal_acw_5e-6")
    hSig[5].Write("signal_acw_8e-6")
    hSig[6].Write("signal_acw_2e-5")
    hSigMisReco[1].Write("background_ExclWW_misreco")
    hSigMisReco[0].Write("signal_a0w_1e-6_misreco")
    hSigMisReco[2].Write("signal_a0w_2e-6_misreco")
    hSigMisReco[3].Write("signal_a0w_5e-6_misreco")
    hSigMisReco[4].Write("signal_acw_5e-6_misreco")
    hSigMisReco[5].Write("signal_acw_8e-6_misreco")
    hSigMisReco[6].Write("signal_acw_2e-5_misreco")

    fout.Write()
    fout.Close()

    leg.Draw("same")
    writePlots(c,Ycut,channel,signal_region,background_method,justSignal)
    _file0.Close()
    fout.Close()

if __name__=="__main__":
    #main(sys.argv[1],"h_MWW_MX_0_4_tracks","h_MWW_MX_5_up","muon")
    #if len(sys.argv)==5:
    makePlot(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
