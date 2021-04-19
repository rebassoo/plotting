#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-16-2019
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
        self.data={"A":[],"B":[],"C":[],"D":[]}
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


def plot_number_protons(e,h_signal_protons_eacharm,year,xi_tmp):
    #year="2018"
    #sample="ExclusiveWW"
    #xi_tmp = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[],"weight":[],"multi_arm0":[],"multi_arm1":[]}
    #era=RandomEraFine2018()
    #passPPSMultiRP=passPPSMulti(e,xi_tmp,era)
    if len(xi_tmp["multi_arm0"]) == 0 or len(xi_tmp["multi_arm1"]) == 0:
        h_signal_protons_eacharm.Fill(-1,-1)
        return 0
    #passAperture45=aperture(xi_tmp["multi_arm0"][0],e.crossingAngle,"45",era,year)
    #passAperture56=aperture(xi_tmp["multi_arm1"][0],e.crossingAngle,"56",era,year)
    #if not passAperture45 or not passAperture56:
    #    h_signal_protons_eacharm.Fill(-1,-1)
    #    return 0
    #addPileupProtons(e,xi_tmp,era,sample,year)        
    h_signal_protons_eacharm.Fill(len(xi_tmp["multi_arm0"]),len(xi_tmp["multi_arm1"]))

def plotXYSignal(e,h_y_vs_x_signal):
    x_ = {"3":[],"103":[],"23":[],"123":[]}
    y_ = {"3":[],"103":[],"23":[],"123":[]}
    passPPSNewPixelXY(e,x_,y_)
    #passPPSNewStrip(e,x_,y_)
    selection_det=["3","23","103","123"]
    i=0
    for tex in selection_det:
        if len(x_[tex]) > 0:
            h_y_vs_x_signal[i].Fill(x_[tex][0],y_[tex][0])
        i=i+1

def findEra(run):
    if (run >= 315252 and run <= 316995):
        return "A"
    if (run >= 316998 and run <= 317696):
        return "B1"
    if (run >= 318662 and run <= 319312):
        return "B2"
    if (run >= 319313 and run <= 320393):
        return "C"
    if (run >= 320394 and run <= 322633):
        return "D1"
    if (run >= 323363 and run <= 325273):
        return "D2"
        

def RandomEraFine2018():
    r0=r.random()
    era=""
    if r0<0.2172:
        era="A"
    if r0>=0.2172 and r0<0.3318:
        era="B1"
    if r0>=0.3318 and r0<0.3390:
        era="B2"
    if r0>=0.3390 and r0<0.4562:
        era="C"
    if r0>=0.4562 and r0<0.8131:
        era="D1"
    if r0>=0.8131:
        era="D2"
    return era

def RandomEra2018():
    #RunA 12.10 fb-1
    #RunB1 6.38 fb-1
    #RunB2 0.40 fb-1
    #RunC  6.5297 fb-1
    #RunD1 19.88 fb-1
    #RunD2 10.4157 fb-1
    
    #These are based on CMS ratios not PPS json
    r0=r.random()
    era=""
    if r0<0.229:
        era="A"
    if r0>=0.229 and r0<0.344:
        era="B"
    if r0>=0.344 and r0<0.456:
        era="C"
    if r0>=0.456:
        era="D"
    return era


def addPileupProtons(e,xi,era,sample,year,evm,tree=0,entries=0):
    nVerticesCMS=e.nVertices
    if sample != "DATA":
        #if e.muon_pt.size()>0:
        #    f=TFile("xiEventsRun{0}-2018.root".format(era[0]))
        #if e.electron_pt.size()>0:
        #    f=TFile("xiEventsRun{0}-2018-e.root".format(era[0]))
        f=TFile("inputfiles/xiEventsRun{0}-2018.root".format(era))
        #f=TFile("inputfiles/xiEventsRun{0}-2018.root".format(era))
        tree=f.Get("SlimmedNtuple")
        entries=tree.GetEntries()

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
        #nVerticesPPS=tree.nVertices
        #if (abs(nVerticesPPS-nVerticesCMS)<5 and i < 150) or (abs(nVerticesPPS-nVerticesCMS)<100 and i > 149):
        #if abs(nVerticesPPS-nVerticesCMS)<100 or year == "2018":
        if year == "2018":
            getMatch=True
            if sample != "MC":
                if evm.already_mixed(era,entry): 
                    continue
                else:
                    evm.add_event(era,entry)
            passPPSMulti(tree,xi,era_mixed)
            break
    if not getMatch:
        print "Don't get a match,era: ",era
    return 0

def aperture(xi,xangle,arm,era,year):
    aperturelimit=0.0
    if year == "2017":
        if era == "B" or era == "C" or era =="D":
            era = "2017preTS2"
        if era == "E" or era == "F":
            era = "2017postTS2"
    #print era
    if era == "2016preTS2":
        if arm == "45":
            aperturelimit = 0.111
        if arm == "56":
            aperturelimit = 0.138
    if era == "2016postTS2":
        if arm == "45":
            aperturelimit = 0.104
        if arm == "56":#Note - 1 strip RP was not in, so no aperture cuts derieved
            aperturelimit = 999.9
    if era == "2017preTS2":
        if arm == "45":
            aperturelimit = 0.066 + (3.54e-4 * xangle)
            #print "AP: ",aperturelimit
        if arm == "56":
            aperturelimit = 0.062 + (5.96e-4 * xangle)
    if era == "2017postTS2":
        if arm == "45":
            aperturelimit = 0.073 + (4.11e-4 * xangle)
        if arm == "56":
            aperturelimit = 0.067 + (6.87e-4 * xangle)
    if year == "2018":
        if arm == "45":
            aperturelimit = 0.079 + (4.21e-4 * xangle);
        if arm == "56":
            aperturelimit = 0.074 + (6.6e-4 * xangle);
    #print "xi:", xi
    #print "aperturelimit: ",aperturelimit
    if xi<aperturelimit:
        return True
    else:
        return False

def pixelLimits2018(x,y,era,rpid):
    xmin=0.
    xmax=1000.
    ymin=0.
    ymax=1000.
    dic={}
    #print "era", era
    if era == "A":
        #[xmin,xmax,ymin,ymax]
        dic={"3":[2.850,17.927,-11.598,3.698],"23":[2.421,24.62,-10.898,4.398],"103":[3.275,18.498,-11.298,3.298],"123":[2.421,20.045,-10.398,5.098]}
    if era == "B1":
        dic={"3":[2.850,17.927,-11.598,3.698],"23":[2.421,24.620,-10.898,4.198],"103":[3.275,18.070,-11.198,4.098],"123":[2.564,20.045,-10.398,5.098]}
    if era == "B2":
        dic={"3":[2.564,17.640,-11.598,4.198],"23":[2.140,24.479,-11.398,3.798],"103":[3.275,17.931,-10.498,4.098],"123":[2.279,24.760,-10.598,4.498]}
    if era == "C":
        dic={"3":[2.564,17.930,-11.098,4.198],"23":[2.421,24.620,-11.398,3.698],"103":[3.275,17.931,-10.498,4.698],"123":[2.279,24.760,-10.598,4.398]}
    if era == "D1":
        dic={"3":[2.850,17.931,-11.098,4.098],"23":[2.421,24.620,-11.398,3.698],"103":[3.275,17.931,-10.498,4.698],"123":[2.279,24.760,-10.598,4.398]}
    if era == "D2":
        dic={"3":[2.850,17.931,-10.598,4.498],"23":[2.421,24,620,-11.698,3.298],"103":[3.275,17.931,-9.998,4.698],"123":[2.279,24.760,-10.598,3.898]}
    #print dic
    list_xy=dic[rpid]
    if rpid == "3" or rpid =="103":
        x=x*m.cos((-8/180.)*m.pi)-y*m.sin((-8/180.)*m.pi)
        y=x*m.sin((-8/180.)*m.pi)+y*m.cos((-8/180.)*m.pi)
        
    if x>list_xy[0] and x<list_xy[1] and y>list_xy[2] and y<list_xy[3]:
        return True
    else:
        return False

def passYcutFunc2(Yvalue_,signal_bin):
    #print Yvalue_
    #print signal_bin
    passYcut_=False
    #if signal_bin=="multiPixel" and Yvalue_<0.6:
    if signal_bin=="multiPixel" and Yvalue_<0.4:
        passYcut_=True
    if signal_bin=="pixel-pixel" and Yvalue_<0.4:
        passYcut_=True
    if signal_bin=="multiRP" and Yvalue_<0.25:
        passYcut_=True
    #print passYcut_
    return passYcut_

def muonScaleFactor(pt,eta,year,batch_prefix):
    #currently not doing anything for pt>120 GeV
    #Also not doing anything for isolation
    #f=TFile("RunBCDEF_SF_ISO.root")
    h=TH2F()
    if year == "2017":
        f=TFile("{0}RunBCDEF_SF_MuID.root".format(batch_prefix))
        h=f.Get("NUM_TightID_DEN_genTracks_pt_abseta")
    if year == "2018":
        f=TFile("{0}RunABCD_SF_ID.root".format(batch_prefix))
        h=f.Get("NUM_TightID_DEN_TrackerMuons_pt_abseta")
    sf=1.
    if pt<120:
        bin_x=h.GetXaxis().FindBin(pt)
        bin_y=h.GetYaxis().FindBin(abs(eta))
        sf=h.GetBinContent(bin_x,bin_y)
    return sf

def electronScaleFactor(pt,eta,year,batch_prefix):
    h=TH2F()
    if year == "2017":
        f=TFile("{0}2017_ElectronTight.root".format(batch_prefix))
        h=f.Get("EGamma_SF2D")
    if year == "2018":
        f=TFile("{0}2018_ElectronTight.root".format(batch_prefix))
        h=f.Get("EGamma_SF2D")
    sf=1.
    if pt < 500:
        bin_y=h.GetYaxis().FindBin(pt)
        bin_x=h.GetXaxis().FindBin(eta)
        sf=h.GetBinContent(bin_x,bin_y)
    return sf

def calculatePixelRadEffic2018(x_pixel,y_pixel,era,rp):
    f=TFile("pixelEfficiencies_radiation.root")
    effic45=1.
    effic56=1.
    #print era
    r1=0.
    r2=0.
    if rp == "3":
        r1=r.random()
        h45=f.Get("Pixel/2018/2018{0}/h45_210_2018{1}_all_2D".format(era,era))
        effic45=h45.GetBinContent(h45.FindBin(x_pixel,y_pixel))
        if r1 < effic45: 
            return True
        else: return False
    if rp == "103":
        r2=r.random()
        h56=f.Get("Pixel/2018/2018{0}/h56_210_2018{1}_all_2D".format(era,era))
        effic56=h56.GetBinContent(h56.FindBin(x_pixel,y_pixel))
        if r2 < effic56:
            return True
        else: return False
    print "Rp number is not 3 or 103, something is incorrect in pixel radiation correctoin"
    return False

def passPPSGeneralData(e,xi,era,sample,year):
    passPPSMultiRP=False
    era=findEra(e.run)
    passPPSMultiRP=passPPSMulti(e,xi,era)
    passMultiRP=False
    passMultiPixel=False
    if passPPSMultiRP and len(xi["multi_arm0"]) == 1 and len(xi["multi_arm1"]) == 1:
        xi["23"]=xi["multi_arm0"]
        xi["123"]=xi["multi_arm1"]
        passMultiRP=True
    else: 
        passMultiRP=False
        if (len(xi["multi_arm0"]) == 1 and len(xi["multi_arm1"]) == 2) \
           or (len(xi["multi_arm0"]) == 2 and len(xi["multi_arm1"]) == 1):
            xi["23"]=xi["multi_arm0"]
            xi["123"]=xi["multi_arm1"]
            passMultiPixel=True

    passPPS=[passMultiRP,False,passMultiPixel]
    #print passPPS
    return passPPS

def passPPSGeneralMixDataMC(e,xi,sample,era,year,tree,entries,evm):
    if sample != "Data":
        era=RandomEraFine2018()
    else:
        era=findEra(e.run)
    addPileupProtons(e,xi,era,sample,year,evm,tree,entries)    
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
        if year=="2018":
            if (len(xi["multi_arm0"])==1 and len(xi["multi_arm1"])==2) \
               or (len(xi["multi_arm0"])==2 and len(xi["multi_arm1"])==1):
                xi["23"]=xi["multi_arm0"]
                xi["123"]=xi["multi_arm1"]
                passMultiPixel=True
    passPPS=[passMultiRP,passPixelPixel,passMultiPixel]
    return passPPS


def passPPSGeneralSignal(e,xi,sample,year,era,evm):
    #print "Regular Signal"
    nVerticesCMS=e.nVertices
    era=RandomEraFine2018()
    if year != "2018":
        print "Wrong year to use passPPSGeneraSignal"

    passPPSMultiRP=passPPSMulti(e,xi,era,True,True)
    ns_multiRP_arm0=len(xi["multi_arm0"])
    ns_multiRP_arm1=len(xi["multi_arm1"])
    #print "xi before: ",xi
    addPileupProtons(e,xi,era,sample,year,evm)
    passPixelPixel=False
    passMultiPixel=False
    xi["23"]=xi["multi_arm0"]
    xi["123"]=xi["multi_arm1"]
    ismisreco=False
    #output is [[bool],[bool,bool,bool]], where the first list denotes if misreco,
    #and the second list denotes if passes each of the signal regions
    if (len(xi["multi_arm0"])==1 and len(xi["multi_arm1"])==1):
        if ns_multiRP_arm0 == 1  and ns_multiRP_arm1 == 1:
            return [False,[True,False,False]]
        else:
            return [True,[True,False,False]]

    if (len(xi["multi_arm0"])==1 and len(xi["multi_arm1"])==2):
        if ns_multiRP_arm0 == 1  and ns_multiRP_arm1 == 1:
            return [False,[False,False,True]]
        else:
            return [True,[False,False,True]]
    if (len(xi["multi_arm0"])==2 and len(xi["multi_arm1"])==1):
        if ns_multiRP_arm0 == 1  and ns_multiRP_arm1 == 1:
            return [False,[False,False,True]]
        else:
            return [True,[False,False,True]]
    return [False,[False,False,False]]
    #return [False,False,False]



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


def protonYWWMixing(batch_prefix,year):
    file_xi=TFile("{0}xi{1}.root".format(batch_prefix,year))
    h_YWW=file_xi.Get("h_YCMS_5_up_all")
    YWW=h_YWW.GetRandom()
    return YWW

def protonMWWMixing(batch_prefix,year):
    file_xi=TFile("{0}xi{1}.root".format(batch_prefix,year))
    h_MWW=file_xi.Get("h_MWW_5_up_all")
    MWW=h_MWW.GetRandom()
    return MWW

def passPPSMulti(e,xi,era="99",fiducialpxl=True,signal=False):
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
                    if aperture(xi_,e.crossingAngle,"45",era[0],"2018"):
                        xi["multi_arm0"].append(xi_)
                        left=True
                elif aperture(xi_,e.crossingAngle,"45",era[0],"2018"):
                    #if stripLimits(e.proton_trackx1[ii],e.proton_tracky1[ii],era,e.proton_arm[ii]):
                    if e.proton_rpid2[ii_multi] != 23:
                        print "There is an issue with multiRP in sector 45"
                    if pixelLimits2018(e.proton_trackx1[ii_multi],e.proton_tracky1[ii_multi],era,"3"):
                        if pixelLimits2018(e.proton_trackx2[ii_multi],e.proton_tracky2[ii_multi],era,"23"):
                            passrad=calculatePixelRadEffic2018(e.proton_trackx1[ii_multi],e.proton_tracky1[ii_multi],era,"3")
                            if signal and passrad:
                                xi["multi_arm0"].append(xi_)
                                left=True
                            if not signal:
                                xi["multi_arm0"].append(xi_)
                                left=True
        if e.proton_arm[ii]==1 and e.proton_ismultirp_[ii]==1:
            if e.proton_trackpixshift1[ii]==0 and e.proton_trackpixshift2[ii_multi]==0:
                #print "aperature 56: ",aperature(xi_,e.crossingAngle,"56",era[0])
                if not fiducialpxl:
                    if aperture(xi_,e.crossingAngle,"56",era[0],"2018"):
                        xi["multi_arm1"].append(xi_)
                        right=True                    
                elif aperture(xi_,e.crossingAngle,"56",era[0],"2018"):
                    if e.proton_rpid2[ii_multi] != 123:
                        print "There is an issue with multiRP in sector 56"
                    #if stripLimits(e.proton_trackx1[ii],e.proton_tracky1[ii],era,e.proton_arm[ii]):
                    if pixelLimits2018(e.proton_trackx1[ii_multi],e.proton_tracky1[ii_multi],era,"103"):
                        if pixelLimits2018(e.proton_trackx2[ii_multi],e.proton_tracky2[ii_multi],era,"123"):
                            passrad=calculatePixelRadEffic2018(e.proton_trackx1[ii_multi],e.proton_tracky1[ii_multi],era,"103")
                            if signal and passrad:
                                xi["multi_arm1"].append(xi_)
                                right=True
                            if not signal:
                                xi["multi_arm1"].append(xi_)
                                right=True

        if e.proton_ismultirp_[ii]==1: ii_multi=ii_multi+1
        ii=ii+1
    if left and right: passesPPS=True
    return passesPPS

def passPPSNewPixelXY(e,x_pixel,y_pixel):
    ii=0
    for detId_rp in e.pps_track_rpid:
        #pixel
        if detId_rp == 3:
            x_pixel["3"].append(e.pps_track_x[ii])
            y_pixel["3"].append(e.pps_track_y[ii])
        if detId_rp == 23:
            x_pixel["23"].append(e.pps_track_x[ii])
            y_pixel["23"].append(e.pps_track_y[ii])
        #pixel
        if detId_rp == 103:
            x_pixel["103"].append(e.pps_track_x[ii])
            y_pixel["103"].append(e.pps_track_y[ii])
        if detId_rp == 123:
            x_pixel["123"].append(e.pps_track_x[ii])
            y_pixel["123"].append(e.pps_track_y[ii])
        ii=ii+1
    return True


def passPPSNewPixelMixSignal(e,xi,year,tree,entries):
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
    era=RandomEra2018()
    addPileupProtons(e,xi,era,"ExclusiveMC",year,evm,tree,entries)
    if len(xi["123"])==1 and len(xi["23"])==1:
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
    verbose=False
    if verbose: print "Is is Data: ",DATA
    mypath_prefix='/hadoop/cms/store/user/rebassoo/'
    #mypath_prefix='/eos/uscms/store/user/rebassoo/'
    #print os.listdir('/hadoop/cms/store/user/rebassoo/{0}/{1}'.format(sample_name,file_dir))
    print("directory_type: ",directory_type)
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
            if verbose: print di
            d=di.split("/")[8]
            if verbose: print d
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

        if verbose:
            print m_date
            print m_time        
        if m_time > 0:
            sub_dir=str(m_date_string)+"_"+str(m_time_string)
        else:
            sub_dir=str(m_date_string)
        if verbose: print sub_dir
        itt = 0
        print mypath_prefix+'{0}/{1}/{2}'.format(sample_name,file_dir,sub_dir)
        for i in os.listdir(mypath_prefix+'{0}/{1}/{2}'.format(sample_name,file_dir,sub_dir)):
            mypath=mypath_prefix+'{0}/{1}/{2}/{3}/'.format(sample_name,file_dir,sub_dir,i)
            ListOfFiles += [mypath_prefix+'{0}/{1}/{2}/{3}/{4}'.format(sample_name,file_dir,sub_dir,i,f) for f in listdir(mypath) if isfile(join(mypath, f))]

    if directory_type == 'specific':
        mypath=mypath_prefix+'{0}/{1}/'.format(sample_name,file_dir)
        ListOfFiles = [mypath_prefix+'{0}/{1}/{2}'.format(sample_name,file_dir,f) for f in listdir(mypath) if isfile(join(mypath, f))]
        output_name=sample_name+'_'+file_dir.split('_')[1].split('/')[0]+'_'+file_dir.split('/')[2]

    return ListOfFiles,output_name


def GetListOfFilesOLD(sample_name,file_dir,DATA,directory_type):
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


def writeoutTree(outTree,output_name,i):
    outTree.SetBranchStatus("*",0)
    outTree.SetBranchStatus("crossingAngle",1)
    outTree.SetBranchStatus("run",1)
    outTree.SetBranchStatus("event",1)
    outTree.SetBranchStatus("lumiblock",1)
    outTree.SetBranchStatus("proton_xi",1)
    outTree.SetBranchStatus("proton_ismultirp_",1)
    outTree.SetBranchStatus("proton_rpid",1)
    outTree.SetBranchStatus("proton_arm",1)
    outTree.SetBranchStatus("proton_trackpixshift1",1)
    outTree.SetBranchStatus("proton_trackpixshift2",1)
    outTree.SetBranchStatus("proton_thx",1)
    outTree.SetBranchStatus("proton_trackx1",1)
    outTree.SetBranchStatus("proton_tracky1",1)
    outTree.SetBranchStatus("proton_trackx2",1)
    outTree.SetBranchStatus("proton_tracky2",1)
    outTree.SetBranchStatus("proton_rpid1",1)
    outTree.SetBranchStatus("proton_rpid2",1)
    outTree.SetBranchStatus("nVertices",1)
    fout = TFile('{0}_{1}.root'.format(output_name,i),'recreate')
    fout.cd()
    outTree2 = outTree.CloneTree(0)

    nEntries = outTree.GetEntries()
    for ita in range(nEntries):
        #it=it+1
        outTree.GetEntry(ita+1)
        outTree2.Fill()

    fout.Write()
    fout.Close()
    return 0

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
