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

def addPileupProtons(e,xi,era,sample):
    nVerticesCMS=e.nVertices
    f=TFile("xiEventsRun{0}.root".format(era))
    #f=TFile("xiEvents.root")
    tree=f.Get("SlimmedNtuple")
    entries=tree.GetEntries()
    passBothArms=False
    for i in range(200):
        if i > 199:
            print "Taking many samples of data to get proper nvertex matching between CMS and PPS"
        r5=r.random()
        #entry=int(r5*2146214)
        entry=int(r5*entries)
        #print entry
        tree.GetEntry(entry)
        nVerticesPPS=tree.nVertices
        if abs(nVerticesPPS-nVerticesCMS)<5:
        #if abs(nVerticesPPS-nVerticesCMS)<100:
            p_rpid=tree.proton_rpid
            p_xi=tree.proton_xi
            p_ismultirp=tree.proton_ismultirp_
            p_arm=tree.proton_arm
            p_trackpixshift1=tree.proton_trackpixshift1
            p_trackpixshift2=tree.proton_trackpixshift2
            passBothArms=True
            count_45_pixel=0
            count_56_pixel=0
            ii=0
            ii_multi=0
            for detId in p_rpid:
                if p_ismultirp[ii]==1:
                    if sample=="ExclusiveMC": continue
                    if p_arm[ii]==0:
                        if p_trackpixshift1[ii]==0 and p_trackpixshift2[ii_multi]==0:
                            xi["multi_arm0"].append(p_xi[ii])
                    if p_arm[ii]==1:
                        if p_trackpixshift1[ii]==0 and p_trackpixshift2[ii_multi]==0:
                            xi["multi_arm1"].append(p_xi[ii])
                    ii_multi=ii_multi+1
                if detId==3:
                    #passBothArms=False
                    xi["3"].append(p_xi[ii])
                if detId==23 and p_ismultirp[ii]==0:
                    if p_trackpixshift1[ii]==0:
                    #count_45_pixel=count_45_pixel+1
                        xi["23"].append(p_xi[ii])
                if detId==103:
                    xi["103"].append(p_xi[ii])
                    #passBothArms=False
                if detId == 123 and p_ismultirp[ii]==0: 
                    if p_trackpixshift1[ii]==0:
                    #count_56_pixel=count_56_pixel+1
                        xi["123"].append(p_xi[ii])
                #print "i before break is: ",i
                #if count_56_pixel > 1 or count_45_pixel > 1:
                #    passBothArms=False
                ii=ii+1
            break

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
    if era == "C":
        if r.random<0.6179316777:
            era = "C1"
        else:
            era = "C2"
    if era == "F":
        if r.random<0.128651:
            era = "F1"
        elif ran1>0.128651 and ran1<0.7252057066:
            era = "F2"
        else:
            era = "F3"
    if era == "B" or era == "C1":
        if arm == "45":
            x_min=1.995
            if era == "C1": x_min=1.860
            x_max=24.479
            y_min=-11.098
            y_max=4.298
        if arm == "56":
            x_min=2.422
            x_max=24.620
            y_min=-10.698
            y_max=4.698
    #print arm
    if era == "E" or era == "F1":
        if arm == "45":
            x_min=1.995
            x_max=24.479
            y_min=-10.098
            y_max=4.998
        if arm == "56":
            x_min=2.422
            x_max=24.620
            y_min=-9.698
            if era == "F1": y_min=-9.798
            y_max=5.498
            if era == "F1": y_max=5.398
    #print "x, y: ",x,y
    #print "x_min: ",x_min
    #print "x_max: ",x_max
    #print "y_min: ",y_min
    #print "y_max: ",y_max
    if x>x_min and x<x_max and y>y_min and y<y_max:
        return True
    else:
        #print "x, y: ",x,y
        #print "x_min: ",x_min
        #print "x_max: ",x_max
        #print "y_min: ",y_min
        #print "y_max: ",y_max
        return False

def calculateMultiMultiRPEffic(x_strip,y_strip,era,arm):
    f=TFile("pixelEfficiencies_multiRP.root")
    effic45=1.
    effic56=1.
    r1=0.
    r2=0.
    if era == "C":
        if r.random<0.6179316777:
            era = "C1"
        else:
            era = "C2"
    if era == "F":
        ran1=r.random
        if ran1<0.128651:
            era = "F1"
        elif ran1>0.128651 and ran1<0.7252057066:
            era = "F2"
        else:
            era = "F3"
    #print era
    if len(x_strip["3"])>0:
        x45=x_strip["3"][0]
        y45=y_strip["3"][0]
        #print "x45: ",x45
        #print "y45: ",y45
        #if not pixelLimits(x45,y45,era,"45"):
        #    return 0.
        #r1=r.random()
        h45=f.Get("Pixel/2017/2017{0}/h45_220_2017{1}_all_2D".format(era,era))
        #h45=f.Get("Pixels/2017/2017{0}/h45_220_2017{1}_all_2D".format("all",""))
        effic45=h45.GetBinContent(h45.FindBin(x45,y45))
        #print effic45
        if arm == "45":
            return effic45
    if len(x_strip["103"])>0:
        x56=x_strip["103"][0]
        y56=y_strip["103"][0]
        #print "x56: ",x56
        #print "y56: ",y56
        #if not pixelLimits(x56,y56,era,"56"):
        #    return 0.
        #r2=r.random()
        h56=f.Get("Pixel/2017/2017{0}/h56_220_2017{1}_all_2D".format(era,era))
        #h56=f.Get("Pixels/2017/2017{0}/h56_220_2017{1}_all_2D".format("all",""))
        effic56=h56.GetBinContent(h56.FindBin(x56,y56))
        #print effic56
        if arm == "56":
            return effic56

    weight=effic45*effic56
    return weight




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
    effic45=1.
    effic56=1.
    #print era
    r1=0.
    r2=0.
    if era == "C":
        if r.random<0.6179316777:
            era == "C1"
        else:
            era == "C2"
    if era == "F":
        if r.random<0.128651:
            era == "F1"
    if era != "B" and era != "E" or era != "C1" or era !="C2":
        return 1.
    if len(x_pixel["23"])>0:
        #print "x_pixel: ",x_pixel["23"][0]
        #print "y_pixel: ",y_pixel["23"][0]
        x45=x_pixel["23"][0]
        y45=y_pixel["23"][0]
        if not pixelLimits(x45,y45,era,"45"):
            print "Outside pixel min,max 45, era: ",era
            return 0.
        r1=r.random()
        h45=f.Get("Pixel/2017/2017{0}/h45_220_2017{1}_all_2D".format(era,era))
        #h45=f.Get("Pixels/2017/2017{0}/h45_220_2017{1}_all_2D".format("all",""))
        effic45=h45.GetBinContent(h45.FindBin(x45,y45))
    if len(x_pixel["123"])>0:
        #print "x_pixel: ",x_pixel["123"][0]
        #print "y_pixel: ",y_pixel["123"][0]
        x56=x_pixel["123"][0]
        y56=y_pixel["123"][0]
        if not pixelLimits(x56,y56,era,"56"):
            print "Outside pixel min,max 56, era: ",era
            return 0.
        r2=r.random()
        h56=f.Get("Pixel/2017/2017{0}/h56_220_2017{1}_all_2D".format(era,era))
        #h56=f.Get("Pixels/2017/2017{0}/h56_220_2017{1}_all_2D".format("all",""))
        effic56=h56.GetBinContent(h56.FindBin(x56,y56))
    if sector == "45":
        if r1<effic45: 
            return True
        else: return False
    if sector == "56":
        if r2<effic56:
            return True
        else: return False
    weight=effic45*effic56
    #print weight
    return weight
    if r1<effic45 and r2<effic56:
        return True
    else:
        return False



def calculateSiRadEffic(x_strip,y_strip,era,sector):
    #if len(x_strip["3"])*len(x_strip["103"])*len(y_strip["3"])*len(y_strip["103"])!=1:
    #    print "Not exactly 1 strip in each arm even though passing multiRP"
    f=TFile("PreliminaryEfficiencies_October92019_1D2DMultiTrack.root")
    effic45=1.
    effic56=1.
    if len(x_strip["3"])>0:
        x45=x_strip["3"][0]
        y45=y_strip["3"][0]
        r1=r.random()
        #h45=f.Get("Strips/2017/2017{0}/h45_2017{1}_all_2D".format(era,era))
        h45=f.Get("Strips/2017/2017{0}/h45_2017{1}_all_2D".format("all",""))
        effic45=h45.GetBinContent(h45.FindBin(x45,y45))
    if len(x_strip["103"])>0:
        x56=x_strip["103"][0]
        y56=y_strip["103"][0]
        r2=r.random()
        #h56=f.Get("Strips/2017/2017{0}/h56_2017{1}_all_2D".format(era,era))
        h56=f.Get("Strips/2017/2017{0}/h56_2017{1}_all_2D".format("all",""))
        effic56=h56.GetBinContent(h56.FindBin(x56,y56))

    if sector == "45":
        return effic45
    if sector == "56":
        return effic56
    weight=effic45*effic56
    return weight
    if r1<effic45 and r2<effic56:
        return True
    else:
        return False

def passPPSGeneralData(e,xi,era,sample):

    passPPSMultiRP=False
    #passPPSNewPixel=False
    if sample=="SingleElectron":
        f2=TFile("ElectronDataProtonsRun{0}.root".format(era))
        tree2=f2.Get("SlimmedNtuple")
        #entry=getProtonsElectrons(e,era)
        i=0
        for ev in tree2:
            if ev.run == e.run and ev.event ==e.event and ev.lumiblock==e.lumiblock:
                passPPSMultiRP=passPPSMulti(ev,xi)    
                passPPSNewPixel(ev,xi)
                i=1
        if i==0:
            print "Couldn't find a match"
    else:
        passPPSMultiRP=passPPSMulti(e,xi)    
    passMultiRP=False
    passPixelPixel=False
    passMultiPixel=False
    if passPPSMultiRP: 
        xi["23"]=xi["multi_arm0"]
        xi["123"]=xi["multi_arm1"]
        passMultiRP=True
    else: 
        passMultiRP=False
        if sample!="SingleElectron":
            passPPSNewPixel(e,xi)
        if len(xi["123"])==1 and len(xi["23"])==1:
            passPixelPixel=True
        else: 
            passPixelPixel=False
            if (len(xi["123"])==1 and len(xi["23"])==2) or (len(xi["123"])==2 and len(xi["23"])==1):
                passMultiPixel=True
            else:
                passMultiPixel=False
    passPPS=[passMultiRP,passPixelPixel,passMultiPixel]
    return passPPS


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


def passPPSGeneralMixDataMC(e,xi,sample,era):
    if sample!="Data":
        era=RandomEra()
    addPileupProtons(e,xi,era,sample)    
    passMRP=False
    if len(xi["multi_arm0"])==1 and len(xi["multi_arm1"])==1: 
        passMRP=True
    passMultiRP=False
    passPixelPixel=False
    passMultiPixel=False
    if passMRP:
        xi["23"]=xi["multi_arm0"]
        xi["123"]=xi["multi_arm1"]
        passMultiRP=True
    else: 
        passMultiRP=False
        if len(xi["123"])==1 and len(xi["23"])==1:
            passPixelPixel=True
        else: 
            passPixelPixel=False
            if (len(xi["123"])==1 and len(xi["23"])==2) or (len(xi["123"])==2 and len(xi["23"])==1):
                passMultiPixel=True
            else:
                passMultiPixel=False
    passPPS=[passMultiRP,passPixelPixel,passMultiPixel]
    return passPPS


def passPPSGeneralSignal(e,xi,sample):
    #print "Regular Signal"
    nVerticesCMS=e.nVertices
    era=""
    era=RandomEra()
    #r0=r.random()
    #era=""
    #if r0<0.1146:
    #    era="B"
    #if r0>0.1146 and r0<0.348:
    #    era="C"
    #if r0>0.348 and r0<0.4514:
    #    era="D"
    #if r0>0.4514 and r0<0.67695:
    #    era="E"
    #if r0>0.67695:
    #    era="F"

    #Randomly Select era based on lumi differences
    #Then input that into calculateSiRadEffic and xiEvents below.
    #First see if have multiRP for signal
    passPPSMultiRP=passPPSMulti(e,xi)    
    #print 'xi["multi_arm0"],xi["multi_arm1"]',xi["multi_arm0"],xi["multi_arm1"]
    #See if have just pixels
    passPixel=passPPSNewPixel(e,xi)
    #print e.crossingAngle
    #print 'xi["23"],xi["123"]',xi["23"],xi["123"]
    passPPSStripXi(e,xi)
    #print 'xi["3"],xi["103"]',xi["3"],xi["103"]
    if not passPixel:
        return [False,False,False]
    x_pixel = {"23":[],"123":[]}
    y_pixel = {"23":[],"123":[]}
    passPPSNewPixelXY(e,x_pixel,y_pixel)
    passAperature45=aperature(xi["23"][0],e.crossingAngle,"45",era)
    passAperature56=aperature(xi["123"][0],e.crossingAngle,"56",era)
    #print passAperature45
    #print passAperature56
    if not passAperature45 or not passAperature56:
        return [False,False,False]
    #print xi
    #passPixEffic=calculatePixelRadEffic(x_pixel,y_pixel,era,"-99")
    passPixEffic45=calculatePixelRadEffic(x_pixel,y_pixel,era,"45")
    passPixEffic56=calculatePixelRadEffic(x_pixel,y_pixel,era,"56")
    passSiEffic=1.
    xi["weight"].append(passSiEffic)
    #return True
    x_strip = {"3":[],"103":[]}
    y_strip = {"3":[],"103":[]}
    if passPPSMultiRP:
        pass2Strip=passPPSNewStrip(e,x_strip,y_strip)
        if pass2Strip:
            passSiEffic=calculateSiRadEffic(x_strip,y_strip,era,"-99")
            rnum=r.random()
            #print rnum
            if rnum<passSiEffic:
                passPPSMultiRP=True
            else:
                passPPSMultiRP=False
        else:
            #xi["weight"].append(1-passSiEffic)
            print "For some reason have 2 multiRP but not 2 strip tracks"

    #This adds strips and pixels
    #print xi
    addPileupProtons(e,xi,era,sample)
    passPixelPixel=False
    passMultiPixel=False

    #Should only be mixing in data where there is strips.
    if passPPSMultiRP and (len(xi["23"])==1 and len(xi["123"])==1):
        #print 'xi["23"],xi["123"]',xi["23"],xi["123"]
        #print 'xi["3"],xi["103"]',xi["3"],xi["103"]
        #print 'xi["multi_arm0"],xi["multi_arm1"]',xi["multi_arm0"],xi["multi_arm1"]
        multiMultiRPEffic=calculateMultiMultiRPEffic(x_strip,y_strip,era,"-99")
        ##print multiMultiRPEffic
        #print "multiMultiRPEffic: ",multiMultiRPEffic
        if multiMultiRPEffic < 0.001:
            print "multiMultiRPEffic is close to or zero: ",multiMultiRPEffic
        if r.random()>multiMultiRPEffic:
            passPPSMultiRP=False
        else:
            xi["23"]=xi["multi_arm0"]
            xi["123"]=xi["multi_arm1"]
    else:
        passPPSMultiRP=False

    if (len(xi["23"])>1 or len(xi["123"])>1) or not passPPSMultiRP: #then multi-pixel or pixel-pixel
        passPPSMultiRP=False
        #pixel-pixel
        if not passPixEffic45 or not passPixEffic56:
            return [False,False,False]
        if (len(xi["23"])==1 and len(xi["123"])==1):
                passPixelPixel=True
        #MultiPixel
        if (len(xi["23"])==2 and len(xi["123"])==1) or (len(xi["23"])==1 and len(xi["123"])==2):
            passMultiPixel=True
    
    return [passPPSMultiRP,passPixelPixel,passMultiPixel]


def passPPSGeneralSignalMisReco(e,xi,sample):
    #print "Misreco Signal"
    nVerticesCMS=e.nVertices
    era=""
    #era=RandomEra()
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

    #Randomly Select era based on lumi differences
    #Then input that into calculateSiRadEffic and xiEvents below.
    #First see if have multiRP for signal
    passPPSMultiRP=passPPSMulti(e,xi)    
    #See if have just pixels
    passPixel=passPPSNewPixel(e,xi)
    x_pixel = {"23":[],"123":[]}
    y_pixel = {"23":[],"123":[]}
    passPPSNewPixelXY(e,x_pixel,y_pixel)
    if (len(xi["23"])>0 and  len(xi["123"])>0):
        return [False,False,False]

    passPixEffic45=True
    passPixEffic56=True
    if len(xi["23"]) == 1 and len(xi["123"]) == 0:
        failAperature45=aperature(xi["23"][0],e.crossingAngle,"45",era)
        if failAperature45: return [False,False,False]
        passPixEffic45=calculatePixelRadEffic(x_pixel,y_pixel,era,"45")
        #if not calculatePixelRadEffic(x_pixel,y_pixel,era,"45"): return [False,False,False]
    if len(xi["23"]) == 0 and len(xi["123"]) == 1:
        failAperature56=aperature(xi["123"][0],e.crossingAngle,"56",era)
        if failAperature56: return [False,False,False]
        #if not calculatePixelRadEffic(x_pixel,y_pixel,era,"56"): return [False,False,False]
        passPixEffic56=calculatePixelRadEffic(x_pixel,y_pixel,era,"56")
        
    passSiEffic=1.
    xi["weight"].append(passSiEffic)
    #return True
    x_strip = {"3":[],"103":[]}
    y_strip = {"3":[],"103":[]}
    pass2Strip=passPPSNewStrip(e,x_strip,y_strip)
    passSiEffic=False
    multiMultiRPEffic=1.
    if len(xi["multi_arm0"])>0:
        passSiEffic=calculateSiRadEffic(x_strip,y_strip,era,45)
        xi["arm_mr"].append("56")
        multiMultiRPEffic=calculateMultiMultiRPEffic(x_strip,y_strip,era,"45")
        
    if len(xi["multi_arm1"])>0:
        passSiEffic=calculateSiRadEffic(x_strip,y_strip,era,56)
        xi["arm_mr"].append("45")
        multiMultiRPEffic=calculateMultiMultiRPEffic(x_strip,y_strip,era,"56")

    rnum=r.random()
    passPPSMultiRP1=False
    if rnum<passSiEffic:
        passPPSMultiRP1=True

    sampleMisReco=sample+"MisReco"
    addPileupProtons(e,xi,era,sampleMisReco)
    passPixelPixel=False
    passMultiPixel=False
    passPPSMultiRP=False

    #Should only be mixing in data where there is strips.
    if passPPSMultiRP1 and len(xi["multi_arm0"])>0 and len(xi["multi_arm1"])>0 and (len(xi["23"])==1 and len(xi["123"])==1):
        passPPSMultiRP=True
        if r.random()>multiMultiRPEffic:
            passPPSMultiRP=False
            xi["23"]=[xi["multi_arm0"][0]]
            xi["123"]=[xi["multi_arm1"][0]]
    else:
        passPPSMultiRP=False
    #if len(xi["3"])==0 and len(xi["103"])==0 then multi-pixel

    if (len(xi["23"])>1 or len(xi["123"])>1) or not passPPSMultiRP: #then multi-pixel or pixel-pixel
        passPPSMultiRP=False
        if not passPixEffic45 or not passPixEffic56:
            return [False,False,False]
        #pixel-pixel
        if (len(xi["23"])==1 and len(xi["123"])==1):
            passPixelPixel=True
        #MultiPixel
        if (len(xi["23"])==2 and len(xi["123"])==1) or (len(xi["23"])==1 and len(xi["123"])==2):
            passMultiPixel=True
    
    return [passPPSMultiRP,passPixelPixel,passMultiPixel]



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


def passPPSMulti(e,xi):
    left=False
    right=False
    passesPPS=False
    ii=0
    ii_multi=0
    for xi_ in e.proton_xi:
        if e.proton_arm[ii]==0 and e.proton_ismultirp_[ii]==1:
            if e.proton_trackpixshift1[ii]==0 and e.proton_trackpixshift2[ii_multi]==0:
                xi["multi_arm0"].append(xi_)
                left=True
        if e.proton_arm[ii]==1 and e.proton_ismultirp_[ii]==1:
            if e.proton_trackpixshift1[ii]==0 and e.proton_trackpixshift2[ii_multi]==0:
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


def passPPSNewPixel(e,xi):
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
    if len(xi["123"])==1 and len(xi["23"])==1:
        return True
    else:
        return False

def passPPSNewPixelXY(e,x_pixel,y_pixel):
    ii=0
    for detId_rp in e.pps_track_rpid:
        #pixel
        if detId_rp == 23:
            x_pixel["23"].append(e.pps_track_x[ii])
            y_pixel["23"].append(e.pps_track_y[ii])
        #pixel
        if detId_rp == 123:
            x_pixel["123"].append(e.pps_track_x[ii])
            y_pixel["123"].append(e.pps_track_y[ii])
        ii=ii+1
    return True


def passPPSNewPixelMixSignal(e,xi):
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
    addPileupProtons(e,xi,era,"ExclusiveMC")
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
