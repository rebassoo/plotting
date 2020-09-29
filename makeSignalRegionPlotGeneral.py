#!/usr/bin/env python                                                                                   
#Finn Rebassoo, LLNL 04-30-2019 
import math as m
import sys
from ptools import *
from ROOT import *
from htools import *
#python makeSignalRegionPlotGeneral.py directory noYcut channel background_method signal_region

def makeplot(direc,Ycut,channel,background_method,signal_region,year,justSignal=False):
    backgroundMC=True
    #backgroundMC=False
    rebin=5
    if year == "2018":
        maximum=10
    if year == "2017":
        maximum=4
    #print channel
    #print direc.split("-")[4]
    #fout=TFile("combined_shapes_{0}_{1}.root".format(channel,direc.split("-")[4]),"recreate")
    #fout=TFile("combined_shapes_{0}_{1}.root".format(channel,signal_region),"recreate")
    if channel == "muon" : channel_abr=channel[:2]
    if channel == "electron" : channel_abr=channel[:1]
    fout=TFile("combined_shapes_{0}_{1}_{2}.root".format(channel_abr,signal_region.lower(),year),"recreate")
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
        if Ycut=="Ycut":     
            histo_name_control="h_MWW_MX_control_5_up_Ycut"+"_"+signal_region
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
        h1.GetXaxis().SetTitle("M_{WW}/M_{X}")
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
    "GGToWW_SM_13TeV-fpmc-herwig6",    
    "GGToWW_bSM-A0W5e-6_13TeV-fpmc-herwig6",    
    "GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6",    
    "GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6",
    "GGToWW_bSM-A0W5e-7_13TeV-fpmc-herwig6",    
    "GGToWW_bSM-ACW2e-5_13TeV-fpmc-herwig6",
    "GGToWW_bSM-ACW8e-6_13TeV-fpmc-herwig6",
    "GGToWW_bSM-ACW5e-6_13TeV-fpmc-herwig6",
    "GGToWW_bSM-ACW2e-6_13TeV-fpmc-herwig6"
    ]
    if year == "2017":
        if channel == "muon": SignalSamples[0]="GGToWWToJJMuNu_PtL-15_13TeV-fpmc-herwig6"
        if channel == "electron": SignalSamples[0]="GGToWWToJJENu_PtL-15_13TeV-fpmc-herwig6"
    fSig=[]
    hSig=[]
    hSigMisReco=[]
    it=0
    for sig in SignalSamples:
        if year == "2017":
            fSig.append(TFile("{0}/".format(directory)+sig+".root"))
        if year == "2018":
            fSig.append(TFile("{0}/".format(directory)+sig+"-{0}.root".format(year)))
            sig=sig+"-2018"
        fSig[it].cd()
        hSig.append(fSig[it].Get(histo_name))
        hSigMisReco.append(fSig[it].Get(histo_name_misreco))
        #print sig[:-5]
        #ModifyHisto(hSig[it],sig[:-5],directory)
        ModifyHisto(hSig[it],sig,directory)
        hSig[it].Rebin(rebin)
        hSig[it].SetFillColor(0)
        #ModifyHisto(hSigMisReco[it],sig[:-5],directory)
        ModifyHisto(hSigMisReco[it],sig,directory)
        if it == 0:
            hSig[it].SetLineColor(7)
            hSigMisReco[it].SetLineColor(7)
        if it == 1:
            hSig[it].SetLineColor(9)
            hSigMisReco[it].SetLineColor(9)
        if it == 2:
            hSig[it].SetLineColor(8)
            hSigMisReco[it].SetLineColor(8)
        if it == 3:
            hSig[it].SetLineColor(6)
            hSigMisReco[it].SetLineColor(6)
        if it == 4:
            hSig[it].SetLineColor(11)
            hSigMisReco[it].SetLineColor(11)
        if it > 4:
            hSig[it].SetLineColor(42+it)
            hSigMisReco[it].SetLineColor(42+it)


        hSigMisReco[it].Rebin(rebin)
        hSigMisReco[it].SetFillColor(0)
        hSigMisReco[it].SetLineStyle(2)
        print "Line Color: ",hSig[it].GetLineColor()
        if it < 4:
            hSig[it].Draw("histsame")
            hSigMisReco[it].Draw("histsame")
            print "I get here!!!"
        if justSignal and it == 0:
            hSig[it].SetStats(0)
            hSig[it].SetMaximum(maximum)
            hSig[it].GetXaxis().SetTitle("M_{WW}/M_{X}")
            hSig[it].GetYaxis().SetTitle("Events")
            hSig[it].Draw("hist")
            hSigMisReco[it].Draw("histsame")

        it=it+1

    #leg=TLegend(0.61,0.402,0.81,0.892)
    leg=TLegend(0.61,0.402,0.81,0.86)
    if justSignal:
        leg=TLegend(0.63,0.452,0.78,0.86)
    leg.SetFillColor(0)
    leg.SetLineColor(0)
    leg.SetTextSize(0.022)
    leg.SetTextFont(42)
    if not justSignal:
        #leg.AddEntry(0,"Data-driven background prediction")
        #leg.AddEntry(h0,"ABCD prediction","lep")
        leg.AddEntry(h0,"Nominal","lep")
        #leg.AddEntry(h1,"Template prediction","lep")
        leg.AddEntry(h1,"Cross-check","lep")
        hclear=TH1F()
        hclear.SetLineColor(0)
        leg.AddEntry(hclear,"","l")

    #leg.AddEntry(hSig[4],legend_name("ExclusiveWW_aCw5e-6-SingleLepton-2017"),"l")
    #leg.AddEntry(hSig[5],legend_name("ExclusiveWW_aCw8e-6-SingleLepton-2017"),"l")
    #leg.AddEntry(hSig[6],legend_name("ExclusiveWW_aCw2e-5-SingleLepton-2017"),"l")

    
    #leg.AddEntry(hSig[0],"misreco, "+legend_name("ExclusiveWW_a0w1e-6-SingleLepton-2017"),"l")
    #leg.AddEntry(hSig[1],"misreco, "+legend_name("ExclusiveWW_SM_FPMC-SingleLepton-2017"),"l")
    #leg.AddEntry(hSig[2],"misreco, "+legend_name("ExclusiveWW_a0w2e-6-SingleLepton-2017"),"l")
    #leg.AddEntry(hSig[3],"misreco, "+legend_name("ExclusiveWW_a0w5e-6-SingleLepton-2017"),"l")
    
    if justSignal:

        leg.AddEntry(hSig[1],legend_name(SignalSamples[1])[28:],"l")
        leg.AddEntry(hSig[2],legend_name(SignalSamples[2])[28:],"l")
        leg.AddEntry(hSig[3],legend_name(SignalSamples[3])[28:],"l")
        leg.AddEntry(hSig[0],legend_name(SignalSamples[0])[:2],"l")

        leg.AddEntry(hSigMisReco[1],"misreco: "+\
                     legend_name(SignalSamples[1])[28:],"l")
        leg.AddEntry(hSigMisReco[2],"misreco: "+\
                     legend_name(SignalSamples[2:])[28:],"l")
        leg.AddEntry(hSigMisReco[3],"misreco: "+\
                     legend_name(SignalSamples[3])[28:],"l")
        leg.AddEntry(hSigMisReco[0],"misreco: "+\
                     legend_name(SignalSamples[0])[:2],"l")

        leg.Draw("same")
        writePlots(c,Ycut,channel,signal_region,"",year,justSignal)
        _file0.Close()
        fout.Close()
        return 0

    #######################################################################################
    #Make Background plots
    #######################################################################################
    MCsamples=["WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
               "WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
               "WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
               "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8",
               "DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
               "DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
               "DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
               #"TTJets_TuneCP5_13TeV-madgraphMLM-pythia8", 
               "ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8",
               "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
               "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
               "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
               "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
               "WW_TuneCP5_13TeV-pythia8","WZ_TuneCP5_13TeV-pythia8","ZZ_TuneCP5_13TeV-pythia8",
    ]
    if year == "2017":
        MCsamples=[#"WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
            #"WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8"
            #,"WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
            "W1JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8", 
            "W1JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8",
            "W1JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8",
            "W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8",
            "W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8",
            "W2JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8",
            "W2JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8",
            "W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8",
            #"DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
            #"DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
            #"DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8",
            "TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8",
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
        if channel == "muon":
            if year == "2018":
                extra_tracks_weight=2.86
                extra_tracks_weight_error=0.3937
            if year == "2017":
                extra_tracks_weight=2.16
                extra_tracks_weight_error=0.211
        if channel == "electron":
            if year == "2018":
                extra_tracks_weight=2.58
                extra_tracks_weight_error=0.353
            if year == "2017":
                extra_tracks_weight=2.41
                #Need to check this
                extra_tracks_weight_error=0.23
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
            if sample == "WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8" \
               or sample=="WW_TuneCP5_13TeV-pythia8" \
               or sample=="TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8" \
               or sample =="ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8" \
               or sample =="QCD_Pt_170to300_TuneCP5_13TeV_pythia8" \
               or sample=="WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8" \
               or sample =="TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8" \
               or sample=="WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8" \
               or sample =="DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8" \
               or sample =="DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8" \
               or sample == "W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8" \
               or sample =="ExclusiveWW_SM_FPMC-SingleLepton-2017":
                leg.AddEntry(hMC[len_a-1],legend_name(sample),"f")
            len_a=len_a-1


        hstack.SetMaximum(maximum)
        hstack.Draw("hist same")
        h_mc_errors=hstack.GetStack().Last().Clone()
        nbins=h_mc_errors.GetNbinsX()
        for i in range(nbins):
            entry=h_mc_errors.GetBinContent(i)            
            entry_error=h_mc_errors.GetBinError(i)
            if entry > 0:
                total_bin_error=m.sqrt( m.pow((entry_error/entry),2) + m.pow( (extra_tracks_weight_error/extra_tracks_weight),2) )
                h_mc_errors.SetBinError(i,total_bin_error*entry)
        h_mc_errors.SetLineColor(1)
        h_mc_errors.SetFillStyle(2)
        h_mc_errors.SetFillColor(1)
        h_mc_errors.SetFillStyle(3005)
        h_mc_errors.Draw("e2 same")

    leg.AddEntry(hSig[0],legend_name(SignalSamples[0]),"l")
    leg.AddEntry(hclear,"","l")
    leg.AddEntry(hSig[1],legend_name(SignalSamples[1]),"l")
    leg.AddEntry(hSig[2],legend_name(SignalSamples[2]),"l")
    leg.AddEntry(hSig[3],legend_name(SignalSamples[3]),"l")
    #leg.AddEntry(hSig[4],legend_name(SignalSamples[4]),"l")
    #leg.AddEntry(hSig[5],legend_name(SignalSamples[5]),"l")
    #leg.AddEntry(hSig[6],legend_name(SignalSamples[6]),"l")
    #leg.AddEntry(hSig[7],legend_name(SignalSamples[7]),"l")
    #leg.AddEntry(hSig[8],legend_name(SignalSamples[8]),"l")




    h0.Draw("esame")
    h1.Draw("esame")
    hSig[0].Draw("histsame")
    print "LINE COLOR: ",hSig[0].GetLineColor()
    hSig[1].Draw("histsame")
    hSig[2].Draw("histsame")
    hSig[3].Draw("histsame")
    #hSig[4].Draw("histsame")
    hSigMisReco[0].Draw("histsame")
    hSigMisReco[1].Draw("histsame")
    hSigMisReco[2].Draw("histsame")
    hSigMisReco[3].Draw("histsame")
    #hSigMisReco[4].Draw("histsame")

    #hSig[2].Draw("histsame")
    #hSig[3].Draw("histsame")

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
    h0.Write("background")
    diff_up.Write("background_alphaUp")
    diff_down.Write("background_alphaDown")
    data_obs=h1.Clone()
    data_obs.Add(h1,hSig[1])
    data_obs.Write("data_obs")
    hSig[0].Write("background_ExclWW")
    hSig[4].Write("signal_a0w_5e-7")
    hSig[3].Write("signal_a0w_1e-6")
    hSig[2].Write("signal_a0w_2e-6")
    hSig[1].Write("signal_a0w_5e-6")
    hSig[8].Write("signal_acw_2e-6")
    hSig[7].Write("signal_acw_5e-6")
    hSig[6].Write("signal_acw_8e-6")
    hSig[5].Write("signal_acw_2e-5")
    hSigMisReco[0].Write("background_ExclWW_misreco")
    hSigMisReco[4].Write("signal_a0w_5e-7_misreco")
    hSigMisReco[3].Write("signal_a0w_1e-6_misreco")
    hSigMisReco[2].Write("signal_a0w_2e-6_misreco")
    hSigMisReco[1].Write("signal_a0w_5e-6_misreco")
    hSigMisReco[8].Write("signal_acw_2e-6_misreco")
    hSigMisReco[7].Write("signal_acw_5e-6_misreco")
    hSigMisReco[6].Write("signal_acw_8e-6_misreco")
    hSigMisReco[5].Write("signal_acw_2e-5_misreco")


    fout.Write()
    fout.Close()

    leg.Draw("same")
    writePlots(c,Ycut,channel,signal_region,background_method,year,justSignal)
    _file0.Close()
    fout.Close()

if __name__=="__main__":
    #main(sys.argv[1],"h_MWW_MX_0_4_tracks","h_MWW_MX_5_up","muon")
    #if len(sys.argv)==5:
    makePlot(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
