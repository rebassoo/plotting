#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-16-2017
import math as m
import random as r
import os
import sys
import json
import subprocess
import glob
from ROOT import *
from os import listdir
from os.path import isfile, join

class eventListMixing:
    def __init__(self):
        self.data={"B":[],"C":[],"D":[],"E":[],"F":[]}
    def add_event(self,era,number):
        self.data.setdefault(era,[]).append(number)
    def already_mixed(self,era,number):
        #print number
        #self.data.setdefault(era,[]).append(number)
        #print self.data
        #print self.data[era]
        if number in self.data[era[0]]:
            return True
        else:
            return False
        #if era, number is already in list than return false, otherwise true

def get0tr_insuff(xangle,period,arm="-999"):
    prob=1.
    if period == "E":
        period="E2"
        #if r.random()<0.5:
        #    period = "E1"
        #else:
        #    period = "E2"

    #This is for 45
    if xangle == 120:
        if period == "B": prob = 0.8605
        if period == "C": prob = 0.8687
        if period == "D": prob = 0.8665
        if period == "E1": prob = 1.0000*0
        if period == "E2": prob = 0.6945
        if period == "F": prob = 0.6803
    if xangle == 130:
        if period == "B": prob = 0.7749
        if period == "C": prob = 0.7888
        if period == "D": prob = 0.7920
        if period == "E1": prob = 1.0000*0
        if period == "E2": prob = 0.4680
        if period == "F": prob = 0.4667
    if xangle == 140:
        if period == "B": prob = 0.7137
        if period == "C": prob = 0.7181
        if period == "D": prob = 0.7353
        if period == "E1": prob = 1.0000*0
        if period == "E2": prob = 0.3556
        if period == "F": prob = 0.3878
    if xangle == 150:
        if period == "B": prob = 0.6359
        if period == "C": prob = 0.6510
        if period == "D": prob = 0.6713
        if period == "E1": prob = 1.0000*0
        if period == "E2": prob = 0.3493
        if period == "F": prob = 0.3593

    if arm == "45":
        if r.random() < prob: 
            return True
        else: 
            return False
    if arm == "56":
        prob=1.
    #This is for 56
    if xangle == 120:
        if period == "B": prob = 0.8412*prob
        if period == "C": prob = 0.8370*prob
        if period == "D": prob = 0.8273*prob
        if period == "E1": prob = 0.6572*prob
        if period == "E2": prob = 0.6307*prob
        if period == "F": prob = 0.6053*prob
    if xangle == 130:
        if period == "B": prob = 0.7409*prob
        if period == "C": prob = 0.7400*prob
        if period == "D": prob = 0.7376*prob
        if period == "E1": prob = 0.4822*prob
        if period == "E2": prob =  0.3976*prob
        if period == "F": prob =  0.3813*prob
    if xangle == 140:
        if period == "B": prob = 0.6752*prob
        if period == "C": prob = 0.6607*prob
        if period == "D": prob = 0.6729*prob
        if period == "E1": prob = 0.3791*prob
        if period == "E2": prob = 0.2982*prob
        if period == "F": prob = 0.3100*prob
    if xangle == 150:
        if period == "B": prob = 0.5948*prob
        if period == "C": prob = 0.5896*prob
        if period == "D": prob = 0.6010*prob
        if period == "E1": prob = 0.3467*prob
        if period == "E2": prob = 0.2904*prob
        if period == "F": prob = 0.2862*prob

    if arm == "56":
        if r.random() < prob: 
            return True
        else: 
            return False

    if r.random() < prob:
        return True
    else:
        return False
    #return prob

def plotXYSignal(e,h_y_vs_x_signal):
    x_ = {"3":[],"103":[],"23":[],"123":[]}
    y_ = {"3":[],"103":[],"23":[],"123":[]}
    passPPSNewPixelXY(e,x_,y_)
    passPPSNewStrip(e,x_,y_)
    selection_det=["3","23","103","123"]
    i=0
    for tex in selection_det:
        if len(x_[tex]) > 0:
            h_y_vs_x_signal[i].Fill(x_[tex][0],y_[tex][0])
        i=i+1


def findEra(run):
    if (run >= 297020 and run <= 299329):
        return "B"
    if (run >= 299337 and run <= 300785):
        return "C1"
    if (run >= 300806 and run <= 302029):
        return "C2"
    if (run >= 302030 and run <= 303434):
        return "D"
    if (run >= 303435 and run <= 304826):
        return "E"
    if (run >= 304911 and run <= 305114):
        return "F1"
    if (run >= 305178 and run <= 305902):
        return "F2"
    if (run >= 305965 and run <= 306462):
        return "F3"

def RandomEra():
    r0=r.random()
    era=""
    if r0<0.1146:
        era="B"
    if r0>0.1146 and r0<0.348:
        era="C"
    if r0>0.348 and r0<0.4514:
        era="D"
    if r0>0.4514 and r0<0.67695:
        era="E"
    if r0>0.67695:
        era="F"
    return era

def RandomEraFine():
    r0=r.random()
    era=""
    if r0<0.1146:
        era="B"
    if r0>0.1146 and r0<0.348:
        era="C1"
        if r0>0.2588252536:
            era="C2"
    if r0>0.348 and r0<0.4514:
        era="D"
    if r0>0.4514 and r0<0.67695:
        era="E"
    if r0>0.67695:
        era="F1"
        if r0>0.71851 and r0<0.9112277035:
            era="F2"
        else:
            era="F3"
    return era


def addPileupProtons(e,xi,era,sample,evm):
    #print "era: ",era
    nVerticesCMS=e.nVertices
    f=TFile("xiEventsRun{0}.root".format(era[0]))
    #f=TFile("xiEvents.root")
    tree=f.Get("SlimmedNtuple")
    entries=tree.GetEntries()
    #print "entries: ",entries
    getMatch=False
    for i in range(300):
        if i > 199:
            print "Taking many samples of data to get proper nvertex matching between CMS and PPS"
        r5=r.random()
        #print r5
        #entry=int(r5*2146214)
        entry=int(r5*entries)
        #print entry
        tree.GetEntry(entry)
        #These come from this twiki: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TaggedProtonsPixelEfficiencies#Run_periods
        #print "tree.run: ",tree.run
        #This is so that in case of mixing data protons with data won't subdivide eras
        #Could find the subdivided era from the data event based on findEra and then mix in with same sub-era
        era_mixed=era
        if len(era)>1:
            era_mixed=findEra(tree.run)
            if era != era_mixed:
            #print era
                continue
        nVerticesPPS=tree.nVertices
        #if (abs(nVerticesPPS-nVerticesCMS)<5 and i < 150) or (abs(nVerticesPPS-nVerticesCMS)<100 and i > 149):
        if abs(nVerticesPPS-nVerticesCMS)<100:
            getMatch=True
            if sample != "MC":
                if evm.already_mixed(era,entry): 
                    continue
                else:
                    evm.add_event(era,entry)
            if sample == "ExclusiveMC":
                passPPSMulti(tree,xi,era_mixed,False,False)
                #print "I get here"
                passPPSMulti(tree,xi,era_mixed,True,False,True)
            else:
                passPPSMulti(tree,xi,era_mixed)
            #passPPSMulti(tree,xi,era_mixed)
            #passPPSNewPixel(tree,xi,era_mixed)
            passPPSNewPixel(tree,xi,era_mixed)
            break
    if not getMatch:
        print "Don't get a match,era: ",era
    return 0

def calcmisreco(num_arm0,num_arm1):
    if num_arm0 == 1 and num_arm1 == 1:
        return False
    else:
        return True

def aperature(xi,xangle,arm,era):
    aperaturelimit=0.0
    if era == "B" or era == "C" or era =="D":
        era = "2017preTS2"
    if era == "E" or era == "F":
        era = "2017postTS2"
    #print era
    if era == "2016preTS2":
        if arm == "45":
            aperaturelimit = 0.111
        if arm == "56":
            aperaturelimit = 0.138
    if era == "2016postTS2":
        if arm == "45":
            aperaturelimit = 0.104
        if arm == "56":#Note - 1 strip RP was not in, so no aperature cuts derieved
            aperaturelimit = 999.9
    if era == "2017preTS2":
        #print "AP: ",aperaturelimit
        #print "xangle: ",xangle
        if arm == "45":
            aperaturelimit = 0.066 + (3.54e-4 * xangle)
            #print "AP: ",aperaturelimit
        if arm == "56":
            aperaturelimit = 0.062 + (5.96e-4 * xangle)
    if era == "2017postTS2":
        if arm == "45":
            aperaturelimit = 0.073 + (4.11e-4 * xangle)
        if arm == "56":
            aperaturelimit = 0.067 + (6.87e-4 * xangle)
    if era == "2018":
        if arm == "45":
            aperaturelimit = 0.079 + (4.21e-4 * xangle);
        if arm == "56":
            aperaturelimit = 0.074 + (6.6e-4 * xangle);
    #print "xi:", xi
    #print "aperaturelimit: ",aperaturelimit
    if xi<aperaturelimit:
        return True
    else:
        return False

def pixelLimits(x,y,era,arm):
    x_min=0.
    x_max=1000.
    y_min=-1000.
    y_max=1000.
    if era == "B" or era[0] == "C" or era == "D":
        if arm == "45":
            x_min=1.995
            if era[0] == "C" or era == "D": x_min=1.860
            x_max=24.479
            if era[0] == "C" or era == "D": x_max=24.334
            y_min=-11.098
            y_max=4.298
        if arm == "56":
            x_min=2.422
            x_max=24.620
            y_min=-10.698
            y_max=4.698
    #print arm
    if era == "E" or era[0] == "F":
        if arm == "45":
            x_min=1.995
            x_max=24.479
            y_min=-10.098
            y_max=4.998
        if arm == "56":
            x_min=2.422
            x_max=24.620
            y_min=-9.698
            if era[0] == "F": y_min=-9.798
            y_max=5.498
            if era[0] == "F": y_max=5.398
    if x>x_min and x<x_max and y>y_min and y<y_max:
        return True
    else:
        return False

def calculateMultiRPEffic(x_strip,y_strip,era,arm):
    f=TFile("pixelEfficiencies_multiRP.root")
    #effic45=1.
    #effic56=1.
    #r1=0.
    #r2=0.
    if arm == "45":
        h45=f.Get("Pixel/2017/2017{0}/h45_220_2017{1}_all_2D".format(era,era))
        #h45=f.Get("Pixels/2017/2017{0}/h45_220_2017{1}_all_2D".format("all",""))
        effic45=h45.GetBinContent(h45.FindBin(x_strip,y_strip))
        #print "effic45: ",effic45
        if r.random() < effic45:
            return True
        else:
            return False
    if arm == "56":
        h56=f.Get("Pixel/2017/2017{0}/h56_220_2017{1}_all_2D".format(era,era))
        #h56=f.Get("Pixels/2017/2017{0}/h56_220_2017{1}_all_2D".format("all",""))
        effic56=h56.GetBinContent(h56.FindBin(x_strip,y_strip))
        if r.random() < effic56:
            return True
        else:
            return False
    print "Something is wrong with silicon rad calc."

def passYcutFunc2(Yvalue_,signal_bin):
    #print Yvalue_
    #print signal_bin
    passYcut_=False
    if signal_bin=="multiPixel" and Yvalue_<0.6:
        passYcut_=True
    if signal_bin=="pixel-pixel" and Yvalue_<0.4:
        passYcut_=True
    if signal_bin=="multiRP" and Yvalue_<0.25:
        passYcut_=True
    #print passYcut_
    return passYcut_

def muonScaleFactor(pt,eta):
    #currently not doing anything for pt>120 GeV
    #Also not doing anything for isolation
    #f=TFile("RunBCDEF_SF_ISO.root")
    f=TFile("RunBCDEF_SF_MuID.root")
    h=f.Get("NUM_TightID_DEN_genTracks_pt_abseta")
    sf=1.
    if pt<120:
        bin_x=h.GetXaxis().FindBin(pt)
        bin_y=h.GetYaxis().FindBin(abs(eta))
        sf=h.GetBinContent(bin_x,bin_y)
    return sf

def electronScaleFactor(pt,eta):
    f=TFile("2017_ElectronTight.root")
    h=f.Get("EGamma_SF2D")
    sf=1.
    if pt<500:
        bin_y=h.GetYaxis().FindBin(pt)
        bin_x=h.GetXaxis().FindBin(eta)
        sf=h.GetBinContent(bin_x,bin_y)
    return sf

def calculatePixelRadEffic(x_pixel,y_pixel,era,sector):
    f=TFile("pixelEfficiencies_radiation.root")
    #print era
    if era == "C2" or era == "F2" or era == "D" or era == "F3":
        return False
    if sector == "45":
        r1=r.random()
        h45=f.Get("Pixel/2017/2017{0}/h45_220_2017{1}_all_2D".format(era,era))
        effic45=h45.GetBinContent(h45.FindBin(x_pixel,y_pixel))
        if r1<effic45: 
            return True
        else: return False
    if sector == "56":
        r2=r.random()
        h56=f.Get("Pixel/2017/2017{0}/h56_220_2017{1}_all_2D".format(era,era))
        effic56=h56.GetBinContent(h56.FindBin(x_pixel,y_pixel))
        if r2<effic56:
            return True
        else: return False
    print "Something wrong with Pixel Radiation efficiency"

def calculateSiRadEffic(x_strip,y_strip,era,sector):
    f=TFile("PreliminaryEfficiencies_October92019_1D2DMultiTrack.root")
    effic45=1.
    effic56=1.
    #multitrack45=1.
    #multitrack56=1.
    if sector == "45":
        r1=r.random()
        h45=f.Get("Strips/2017/2017{0}/h45_2017{1}_all_2D".format(era,era))
        #h45=f.Get("Strips/2017/2017{0}/h45_2017{1}_all_2D".format("all",""))
        #h45_multitrack=TH1F()
        #h45_multitrack=f.Get("Strips/2017/2017{0}/h45multitrackeff_2017{1}_avg_RP3".format(era,era))
        #multitrack_45=h45_multitrack.GetBinContent(1)
        effic45=h45.GetBinContent(h45.FindBin(x_strip,y_strip))
        if r1<effic45:
            return True
        else:
            return False
    if sector == "56":
        r2=r.random()
        h56=f.Get("Strips/2017/2017{0}/h56_2017{1}_all_2D".format(era,era))
        #h56=f.Get("Strips/2017/2017{0}/h56_2017{1}_all_2D".format("all",""))
        #h56_multitrack=TH1F()
        #h56_multitrack=f.Get("Strips/2017/2017{0}/h56multitrackeff_2017{1}_avg_RP103".format(era,era))
        #multitrack_56=h56_multitrack.GetBinContent(1)
        effic56=h56.GetBinContent(h56.FindBin(x_strip,y_strip))
        if r2<effic56:
            return True
        else:
            return False
    print "Something is wrong with silicon rad calc."

def passPPSGeneralData(e,xi,era,sample):
    era=findEra(e.run)
    passPPSMultiRP=False
    #passPPSNewPixel=False
    if sample == "SingleElectron":
        f2=TFile("ElectronDataProtonsRun{0}.root".format(era[0]))
        tree2=f2.Get("SlimmedNtuple")
        #entry=getProtonsElectrons(e,era)
        i=0
        for ev in tree2:
            if ev.run == e.run and ev.event ==e.event and ev.lumiblock==e.lumiblock:
                passPPSMultiRP=passPPSMulti(ev,xi,era)    
                passPPSNewPixel(ev,xi,era)
                i=1
        if i == 0:
            print "Couldn't find a match"
    else:
        passPPSMultiRP=passPPSMulti(e,xi,era)    
    passMultiRP=False
    passPixelPixel=False
    passMultiPixel=False
    if passPPSMultiRP: 
        xi["23"]=xi["multi_arm0"]
        xi["123"]=xi["multi_arm1"]
        passMultiRP=True
    else: 
        passMultiRP=False
        if sample != "SingleElectron":
            passPPSNewPixel(e,xi,era)
        if era == "C2" or era == "F2" or era == "D" or era == "F3":
            return [False,False,False]

        if len(xi["123"]) == 1 and len(xi["23"]) == 1:
            passPixelPixel=True
        if (len(xi["123"]) == 1 and len(xi["23"]) == 2) \
           or (len(xi["123"]) == 2 and len(xi["23"]) == 1):
            passMultiPixel=True

    passPPS=[passMultiRP,passPixelPixel,passMultiPixel]
    return passPPS

def passPPSGeneralMixDataMC(e,xi,sample,era,evm):
    #print "era: ",era
    #print "run: ",e.run
    if sample != "Data":
        era=RandomEraFine()
    if sample == "Data":
        era=findEra(e.run)
    #print era
    addPileupProtons(e,xi,era,sample,evm)    
    passMRP=False
    if len(xi["multi_arm0"]) == 1 and len(xi["multi_arm1"]) == 1: 
        passMRP=True
    passMultiRP=False
    passPixelPixel=False
    passMultiPixel=False
    if passMRP:
        xi["23"]=xi["multi_arm0"]
        xi["123"]=xi["multi_arm1"]
        passMultiRP=True
    else: 
        if era == "C2" or era == "F2" or era == "D" or era == "F3":
            return [False,False,False]
        passMultiRP=False
        if (len(xi["123"])==1 and len(xi["23"])==1):
            passPixelPixel=True
        if (len(xi["123"])==1 and len(xi["23"])==2) \
           or (len(xi["123"])==2 and len(xi["23"])==1):
            passMultiPixel=True

    passPPS=[passMultiRP,passPixelPixel,passMultiPixel]
    return passPPS


def passPPSGeneralSignal(e,xi,sample,evm,time):
    #print("1--- %s seconds ---" % (time.time() - start_time))
    #print "Regular Signal"
    nVerticesCMS=e.nVertices
    #Randomly Select era based on lumi differences
    era=""
    era=RandomEraFine()

    #First see if have multiRP for signal, this has aperture and pixel limits in it
    #print "Get before signal multiRP"
    passPPSMultiRP=passPPSMulti(e,xi,era,True,True)    
    #print "Get after signal multiRP"
    #See if have just pixels, this has pixel limits in it (but no pixel aperture cuts)
    passPixel=passPPSNewPixel(e,xi,era,True,True)
    
    #ns stands for number of signal
    ns_multiRP_arm0=len(xi["multi_arm0"])
    ns_multiRP_arm1=len(xi["multi_arm1"])
    ns_pixel_arm0=len(xi["23"])
    ns_pixel_arm1=len(xi["123"])
    addPileupProtons(e,xi,era,sample,evm)
    passPPSMultiRP=False
    passPixelPixel=False
    passMultiPixel=False
    #if passPPSMultiRP and pass_0tr_insuff:
    ismisreco=False
    #if len(xi["multi_arm0"])==1 and len(xi["multi_arm1"])==1:
    if len(xi["multi_arm0"])==1 and len(xi["multi_arm1"])==1 and ns_multiRP_arm0 == 1 \
       and ns_multiRP_arm1 == 1:
        passPPSMultiRP=True
        ismisreco=False
        xi["23"]=xi["multi_arm0"]
        xi["123"]=xi["multi_arm1"]
    elif len(xi["multi_arm0"])==1 and len(xi["multi_arm1"])==1 and ns_multiRP_arm0 == 1 \
         and ns_multiRP_arm1 == 0 and len(xi["marm1_tight"]) == 1:
        passPPSMultiRP=True
        ismisreco=True
        xi["23"]=xi["multi_arm0"]
        xi["123"]=xi["marm1_tight"]
    elif len(xi["multi_arm0"]) == 1 and len(xi["multi_arm1"]) == 1 and ns_multiRP_arm0 == 0 \
         and ns_multiRP_arm1 == 1 and len(xi["marm0_tight"]) == 1:
        passPPSMultiRP=True
        ismisreco=True
        xi["23"]=xi["marm0_tight"]
        xi["123"]=xi["multi_arm1"]
    elif len(xi["multi_arm0"]) == 1 and len(xi["multi_arm1"]) == 1 and ns_multiRP_arm0 == 0 \
         and ns_multiRP_arm1 == 0 and len(xi["marm0_tight"]) == 1 and len(xi["marm1_tight"]) == 1:
        passPPSMultiRP=True
        ismisreco=True
        xi["23"]=xi["marm0_tight"]
        xi["123"]=xi["marm1_tight"]
    else:
        passPPSMultiRP=False
    if not passPPSMultiRP:
        #if ns_pixel_arm0 == 0 and ns_pixel_arm1 == 0:
        #    return [ismisreco,[False,False,False]]
        ismisreco=calcmisreco(ns_pixel_arm0,ns_pixel_arm1)
        if (len(xi["23"]) == 1 and len(xi["123"]) == 1):
            passPixelPixel=True
        #MultiPixel
        if (len(xi["123"]) == 1 and len(xi["23"]) == 2) or (len(xi["123"]) == 2 and len(xi["23"]) == 1):
            passMultiPixel=True
    #print("4--- %s seconds ---" % (time.time() - start_time))
    return [ismisreco,[passPPSMultiRP,passPixelPixel,passMultiPixel]]


def modifyJson(sample,num_events,batch):
    if "ext1_" in sample:
        sample_tmp=sample[:-7]
    elif "ext1" in sample: 
        sample_tmp=sample[:-5]
    elif "pythia8_" in sample:
        sample_tmp=sample[:-2]
    else: sample_tmp = sample
    changeNumEvents=False
    with open('samples_info.json') as json_file:
        data=json.load(json_file)
        print num_events
        print data[sample_tmp][0]
        if num_events != data[sample_tmp][0]:
            changeNumEvents=True
    #In case where not running batch job and number of events has changed modify json file
    if changeNumEvents and not batch:
        data[sample_tmp][0]=num_events
        with open("samples_info.json","w") as jsonFile:
            json.dump(data,jsonFile)
    #In case of batch job output json file with only one entry for that sample
    if batch:
        data[sample_tmp][0]=num_events
        data_tmp={sample: data[sample_tmp]}
        with open("samples_info_{0}.json".format(sample),"w") as jsonFile:
            json.dump(data_tmp,jsonFile)
                

def GetDphi(phi1,phi2):
    result = phi1-phi2
    #print result
    while result > m.pi: result = 2*m.pi - result
    while result < -m.pi: result = 2*m.pi + result
    return result


def protonYWWMixing():
    file_xi=TFile("xi.root")
    h_YWW=file_xi.Get("h_YCMS_5_up_all")
    YWW=h_YWW.GetRandom()
    return YWW

def protonMWWMixing():
    file_xi=TFile("xi.root")
    h_MWW=file_xi.Get("h_MWW_5_up_all")
    MWW=h_MWW.GetRandom()
    return MWW


def passPPSMulti(e,xi,era="99",fiducialpxl=True,signal=False,tightproton=False):
    #print "tight proton: ",tightproton
    left=False
    right=False
    passesPPS=False
    ii=0
    ii_multi=0
    for xi_ in e.proton_xi:
        if e.proton_arm[ii]==0 and e.proton_ismultirp_[ii]==1:
            if e.proton_trackpixshift1[ii]==0 and e.proton_trackpixshift2[ii_multi]==0:
                #print "aperature 45: ",aperature(xi_,e.crossingAngle,"45",era[0])
                if not fiducialpxl:
                    #if aperature(xi_,e.crossingAngle,"45",era[0]):
                    xi["multi_arm0"].append(xi_)
                    left=True
                elif aperature(xi_,e.crossingAngle,"45",era[0]):
                    #if stripLimits(e.proton_trackx1[ii],e.proton_tracky1[ii],era,e.proton_arm[ii]):
                    if e.proton_rpid2[ii_multi] != 23:
                        print "There is an issue with multiRP in sector 45"
                    if pixelLimits(e.proton_trackx2[ii_multi],e.proton_tracky2[ii_multi],era,"45"):
                        if signal:
                            #print "I get here 0:"
                            if calculateSiRadEffic(e.proton_trackx1[ii_multi],e.proton_tracky1[ii_multi],era,"45"):
                                #print "I get here 1:"
                                if get0tr_insuff(e.crossingAngle,era[0],"45"):
                                    #print "I get here 2:"
                                    if calculateMultiRPEffic(e.proton_trackx1[ii_multi],e.proton_tracky1[ii_multi],era,"45"):
                                        #print "I get here 3:"
                                        xi["multi_arm0"].append(xi_)
                                        left=True
                        if not signal:
                            #print "I am not signal, tight proton: ",tightproton
                            if tightproton:
                                xi["marm0_tight"].append(xi_)
                                #print "I get in tight proton"
                            else:
                                xi["multi_arm0"].append(xi_)
                                left=True
                            
        if e.proton_arm[ii]==1 and e.proton_ismultirp_[ii]==1:
            if e.proton_trackpixshift1[ii]==0 and e.proton_trackpixshift2[ii_multi]==0:
                #print "aperature 56: ",aperature(xi_,e.crossingAngle,"56",era[0])
                if not fiducialpxl:
                    #if aperature(xi_,e.crossingAngle,"56",era[0]):
                    xi["multi_arm1"].append(xi_)
                    right=True                    
                elif aperature(xi_,e.crossingAngle,"56",era[0]):
                    if e.proton_rpid2[ii_multi] != 123:
                        print "There is an issue with multiRP in sector 56"
                    #if stripLimits(e.proton_trackx1[ii],e.proton_tracky1[ii],era,e.proton_arm[ii]):
                    if pixelLimits(e.proton_trackx2[ii_multi],e.proton_tracky2[ii_multi],era,"56"):
                        if signal:
                            if calculateSiRadEffic(e.proton_trackx1[ii_multi],e.proton_tracky1[ii_multi],era,"56"):
                                if get0tr_insuff(e.crossingAngle,era[0],"56"):
                                    if calculateMultiRPEffic(e.proton_trackx1[ii_multi],e.proton_tracky1[ii_multi],era,"56"):
                                        xi["multi_arm1"].append(xi_)
                                        right=True
                        if not signal:
                            if tightproton:
                                xi["marm1_tight"].append(xi_)
                            else:
                                xi["multi_arm1"].append(xi_)
                                right=True
        if e.proton_ismultirp_[ii]==1: ii_multi=ii_multi+1
        ii=ii+1
    if left and right: passesPPS=True
    return passesPPS

def passPPSNewStrip(e,x_strip,y_strip):
    ii=0
    for detId_rp in e.pps_track_rpid:
        #pixel
        if detId_rp == 3:
            x_strip["3"].append(e.pps_track_x[ii])
            y_strip["3"].append(e.pps_track_y[ii])
        #pixel
        if detId_rp == 103:
            x_strip["103"].append(e.pps_track_x[ii])
            y_strip["103"].append(e.pps_track_y[ii])
        ii=ii+1
    return True


def passPPSNewPixel(e,xi,era="99",fiducialpxl=True,signal=False):
    ii=0
    for detId_rp in e.proton_rpid:
        #pixel
        if detId_rp == 23 and e.proton_ismultirp_[ii]==0: 
            if e.proton_trackpixshift1[ii]==0:
                if not fiducialpxl:
                    #if aperature(e.proton_xi[ii],e.crossingAngle,"45",era[0]):
                    xi["23"].append(e.proton_xi[ii])
                elif aperature(e.proton_xi[ii],e.crossingAngle,"45",era[0]):
                    if e.proton_rpid[ii] != 23:
                        print "There is an issue with multiRP in sector 45"
                    if pixelLimits(e.proton_trackx1[ii],e.proton_tracky1[ii],era,"45"):
                        if signal and calculatePixelRadEffic(e.proton_trackx1[ii],e.proton_tracky1[ii],era,"45"):
                            xi["23"].append(e.proton_xi[ii])
                        if not signal:                            
                            xi["23"].append(e.proton_xi[ii])
        #pixel
        if detId_rp == 123 and e.proton_ismultirp_[ii]==0: 
            if e.proton_trackpixshift1[ii]==0:
                if not fiducialpxl:
                    #if aperature(e.proton_xi[ii],e.crossingAngle,"56",era[0]):
                    xi["123"].append(e.proton_xi[ii])
                elif aperature(e.proton_xi[ii],e.crossingAngle,"56",era[0]):
                    if e.proton_rpid[ii] != 123:
                        print "There is an issue with multiRP in sector 56"
                    if pixelLimits(e.proton_trackx1[ii],e.proton_tracky1[ii],era,"56"):
                        if signal and calculatePixelRadEffic(e.proton_trackx1[ii],e.proton_tracky1[ii],era,"56"):
                            xi["123"].append(e.proton_xi[ii])
                        if not signal:                            
                            xi["123"].append(e.proton_xi[ii])
        ii=ii+1
    if len(xi["123"])==1 and len(xi["23"])==1:
        return True
    else:
        return False

def passPPSNewPixelXY(e,x_pixel,y_pixel,era="-99"):
    ii=0
    for detId_rp in e.proton_rpid:
        #pixel
        if detId_rp == "23" and e.proton_ismultirp_[ii]==0: 
            if e.proton_trackpixshift1[ii]==0:
                if e.proton_rpid[ii] != 23:
                    print "There is an issue with multiRP in sector 45, XY"
                if aperature(e.proton_xi[ii],e.crossingAngle,"45",era[0]):
                    if pixelLimits(e.proton_trackx1[ii],e.proton_tracky1[ii],era,"45"):
                        x_pixel["23"].append(e.proton_trackx1[ii])
                        y_pixel["23"].append(e.proton_tracky1[ii])
        #pixel
        if detId_rp == "123" and e.proton_ismultirp_[ii]==0: 
            if e.proton_trackpixshift1[ii]==0:
                if e.proton_rpid[ii] != 123:
                    print "There is an issue with multiRP in sector 56, XY"
                if aperature(e.proton_xi[ii],e.crossingAngle,"56",era[0]):
                    if pixelLimits(e.proton_trackx1[ii],e.proton_tracky1[ii],era,"56"):
                        x_pixel["123"].append(e.proton_trackx1[ii])
                        y_pixel["123"].append(e.proton_tracky1[ii])
        ii=ii+1
    if len(x_pixel["123"])==1 and len(x_pixel["23"])==1:
        return True
    else:
        return False

    
def passPPSNewPixelMixSignal(e,xi,evm):
    ii=0
    for detId_rp in e.proton_rpid:
        #pixel
        if detId_rp == 23 and e.proton_ismultirp_[ii]==0: 
            if e.proton_trackpixshift1[ii]==0:
                xi["23"].append(e.proton_xi[ii])
        #pixel
        if detId_rp == 123 and e.proton_ismultirp_[ii]==0: 
            if e.proton_trackpixshift1[ii]==0:
                xi["123"].append(e.proton_xi[ii])
        ii=ii+1
    era=RandomEra()
    addPileupProtons(e,xi,era,"ExclusiveMC",evm)
    if len(xi["123"])==1 and len(xi["23"])==1:
        return True
    else:
        return False

def passPPSStripXi(e,xi):
    ii=0
    for detId_rp in e.proton_rpid:
        if detId_rp == 3 and e.proton_ismultirp_[ii]==0: 
            xi["3"].append(e.proton_xi[ii])
        if detId_rp == 103 and e.proton_ismultirp_[ii]==0: 
            xi["103"].append(e.proton_xi[ii])
        ii=ii+1
    if len(xi["103"])==1 and len(xi["3"])==1:
        return True
    else:
        return False


def AddFilesToChain(chain,ListOfFiles,DATA):
    i=0
    num_events=0
    for file in ListOfFiles:
        i=i+1
        ftest=TFile.Open(file)
        if not ftest:
            continue
        if not DATA:
            statinfo = os.stat(file)
            if statinfo.st_size > 0:
                chain.Add(file)
                f=TFile(file)
                h=TH1F()
                h=f.Get("totalEvents/h_total_events")
                num_events=num_events+h.GetEntries()
        if DATA:
            #if i>10: break
            chain.Add(file)

    print "Number of total files: ",i
    print "Number of events: {0}".format(num_events)
    return num_events

def GetListOfFiles(sample_name,file_dir,DATA,directory_type):
    print "Is is Data: ",DATA
    mypath_prefix='/hadoop/cms/store/user/rebassoo/'
    #mypath_prefix='/eos/uscms/store/user/rebassoo/'
    #print os.listdir('/hadoop/cms/store/user/rebassoo/{0}/{1}'.format(sample_name,file_dir))
    ListOfFiles=[]
    if directory_type == 'latest':
        if DATA: output_name=sample_name+'_'+file_dir.split('_')[1]
        else: output_name=sample_name
        m_date=0.
        m_date_string=0.
        m_time=0.
        m_time_string=0.
        dirs=glob.glob(mypath_prefix+'{0}/{1}/*/'.format(sample_name,file_dir))
        for di in dirs:
            print di
            d=di.split("/")[8]
            print d
        #for d in os.listdir(mypath_prefix+'{0}/{1}'.format(sample_name,file_dir)):
            date=int(d.split('_')[0])
            date_string=d.split('_')[0]
            t=0
            t_string=''
            if '_' in d:
                t=int(d.split('_')[1])
                t_string=d.split('_')[1]
            if date >= m_date: 
                m_date=date
                m_date_string=date_string
                m_time=t
                m_time_string=t_string
                if t > m_time: 
                    m_time=t
                    m_time_string=t_string

        print m_date
        print m_time        
        if m_time > 0:
            sub_dir=str(m_date_string)+"_"+str(m_time_string)
        else:
            sub_dir=str(m_date_string)
        print sub_dir
        itt = 0
        for i in os.listdir(mypath_prefix+'{0}/{1}/{2}'.format(sample_name,file_dir,sub_dir)):
            mypath=mypath_prefix+'{0}/{1}/{2}/{3}/'.format(sample_name,file_dir,sub_dir,i)
            ListOfFiles += [mypath_prefix+'{0}/{1}/{2}/{3}/{4}'.format(sample_name,file_dir,sub_dir,i,f) for f in listdir(mypath) if isfile(join(mypath, f))]

    if directory_type == 'specific':
        mypath=mypath_prefix+'{0}/{1}/'.format(sample_name,file_dir)
        ListOfFiles = [mypath_prefix+'{0}/{1}/{2}'.format(sample_name,file_dir,f) for f in listdir(mypath) if isfile(join(mypath, f))]
        output_name=sample_name+'_'+file_dir.split('_')[1].split('/')[0]+'_'+file_dir.split('/')[2]

    return ListOfFiles,output_name


h_extra_tracks_vs_MWW_PPS=[]
h_extra_tracks_vs_MX_PPS=[]
h_Y_CMS_minus_RP_vs_MWW_MX_PPS=[]
h_num_extra_tracks_PPS=[]
h_num_extra_tracks_PPS_noDRl=[]
h_num_extra_tracks_PPS_reweight_extra_tracks=[]
h_xiCMS_45_passPPS=[]
h_xiCMS_56_passPPS=[]
h_lepton_pt_passPPS=[]
h_jet_pt_passPPS=[]
h_tau21_passPPS=[]
h_prunedMass_passPPS=[]
h_WLeptonicPt_passPPS=[]
h_recoMWW_passPPS=[]
h_MET_passPPS=[]
h_MX_passPPS=[]
h_MWW_MX_passPPS=[]
h_MWW_vs_MX_passPPS=[]
h_Y_CMS_minus_RP_passPPS=[]
h_xi_1_0_4_extratracks=[]
h_xi_2_0_4_extratracks=[]
h_Y_RP_0_4_extratracks=[]
h_Y_CMS_minus_RP_0_4_extratracks=[]
h_MX_0_4_extratracks=[]
h_MWW_0_4_extratracks=[]
h_MWW_MX_0_4_tracks=[]
h_xi1_0_4_tracks_misreco=[]
h_xi2_0_4_tracks_misreco=[]
h_Y_CMS_minus_RP_0_4_tracks_misreco=[]
h_MWW_MX_0_4_tracks_misreco=[]
h_recoMWhad_0_4_tracks=[]
h_tau21_0_4_tracks=[]
h_prunedMass_0_4_tracks=[]
h_MWW_MX_0_4_tracks_Ycut=[]
h_MWW_MX_0_4_tracks_misreco_Ycut=[]
h_MWW_MX_0_4_tracks_100events=[]
h_MWW_MX_0_4_tracks_100events_Ycut=[]
h_xi_1_0_4_extratracks_notPPS=[]
h_xi_2_0_4_extratracks_notPPS=[]
h_Y_RP_0_4_extratracks_notPPS=[]
h_Y_CMS_minus_RP_0_4_extratracks_notPPS=[]
h_MX_0_4_extratracks_notPPS=[]
h_MWW_0_4_extratracks_notPPS=[]
h_MWW_MX_0_4_tracks_notPPS=[]
h_recoMWhad_0_4_tracks_notPPS=[]
h_tau21_0_4_tracks_notPPS=[]
h_prunedMass_0_4_tracks_notPPS=[]
h_MWW_MX_0_4_tracks_notPPS_Ycut=[]
h_xi_1_control=[]
h_xi_2_control=[]
h_Y_RP_control=[]
h_Y_CMS_minus_RP_control=[]
h_MX_control=[]
h_MWW_control=[]
h_MWW_MX_control=[]
h_recoMWhad_control_control=[]
h_tau21_control_control=[]
h_prunedMass_control_control=[]
h_MWW_MX_control_Ycut=[]
h_MWW_MX_5_up_notPPS=[]
h_MWW_MX_5_up_Ycut_notPPS=[]
h_xi_1_control_notPPS=[]
h_xi_2_control_notPPS=[]
h_Y_RP_control_notPPS=[]
h_Y_CMS_minus_RP_control_notPPS=[]
h_MX_control_notPPS=[]
h_MWW_control_notPPS=[]
h_MWW_MX_control_notPPS=[]
h_recoMWhad_control_control_notPPS=[]
h_tau21_control_control_notPPS=[]
h_prunedMass_control_control_notPPS=[]
h_MWW_MX_control_Ycut_notPPS=[]
h_xi_1_5_up=[]
h_xi_2_5_up=[]
h_MX_5_up=[]
h_MWW_5_up=[]
h_Y_RP_5_up=[]
h_Y_CMS_minus_RP_5_up=[]
h_MWW_MX_5_up=[]
h_MWW_MX_5_up_InvertPrunedMass=[]
h_MWW_MX_0_4_InvertPrunedMass=[]
h_MWW_invertPrunedMass=[]
h_MWW_MX_invertPrunedMass_Ycut=[]
h_MWW_MX_control_5_up_Ycut=[]
h_MWW_MX_control_5_up_Ycut_InvertPrunedMass=[]
h_MWW_MX_control_0_4_Ycut_InvertPrunedMass=[]
h_MWW_MX_control_15_30=[]
h_MWW_MX_control_30_50=[]
h_MWW_MX_control_50_70=[]
h_MWW_MX_control_70_100=[]
h_y_vs_x_signal=[]
