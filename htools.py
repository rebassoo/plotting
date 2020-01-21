#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-16-2017
import math as m
import random as r
import os
import sys
import json
import subprocess
from ROOT import *
from os import listdir
from os.path import isfile, join

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


def passPPSGeneral(e,xi,signal_bin,sample):
    #print "sample: ",sample
    #print "signal bin: ",signal_bin
    passPPS=False
    if sample=="MC":
        passPPS=passPPSSimMixing(xi,signal_bin)
        return passPPS

    #print "I get here"

    passPPS=passPPSMulti(e,xi)    
    if sample=="ExclusiveMC" and passPPS:
        passPPS=passPPSSimMixingSignalMulti(e.nVertices,xi)
    if signal_bin=="multiRP":
        return passPPS

    #print "I get here 2"

    #Only look at other signal bins if don't pass multiRP
    if (signal_bin=="pixel-pixel" or signal_bin=="multiPixel") and not passPPS:
        del xi["23"][:]
        del xi["123"][:]
        #print "I get in here"
        passPPS=passPPSNew(e,xi,signal_bin,sample)
        if sample=="ExclusiveMC" and passPPS:
            passPPS=passPPSSimMixingSignalPixel(e.nVertices,xi,signal_bin)
        return passPPS
    return False

def rateOf1track1track(numI):
    file_xi=TFile("xi.root")
    #return 0.295310*0.292298
    h_pass=file_xi.Get("h_nvertices_45_0_56_0")
    h_total=file_xi.Get("h_nvertices_all")
    num=h_pass.GetBinContent(int(numI)+1)
    den=h_total.GetBinContent(int(numI)+1)
    ratio=num/den
    return ratio

def rateOf1track2track(numI):
    file_xi=TFile("xi.root")
    h_pass=file_xi.Get("h_nvertices_45_1_56_0")
    h_total=file_xi.Get("h_nvertices_all")
    num=h_pass.GetBinContent(int(numI)+1)
    den=h_total.GetBinContent(int(numI)+1)
    ratio=num/den
    h_pass2=file_xi.Get("h_nvertices_45_0_56_1")
    num2=h_pass2.GetBinContent(int(numI)+1)
    ratio2=num2/den
    return ratio+ratio2
    #return 0.295319*0.451321*0.292298+0.295319*0.451321*0.292298

def passYcutFunc(Yvalue,signal_bin):
    passYcut=False
    if signal_bin=="multiPixel" and Yvalue<0.6:
        passYcut=True
    if signal_bin=="pixel-pixel" and Yvalue<0.4:
        passYcut=True
    if signal_bin=="multiRP" and Yvalue<0.25:
        passYcut=True
    return passYcut

def modifyJson(sample,num_events,batch):
    if "ext1" in sample: 
        sample_tmp=sample[:-5]
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


def passPPSSimMixingSignalPixel(numI,xi,signal_bin):
    #return True
    file_xi=TFile("xi.root")
    #h_pass=file_xi.Get("h_nvertices_multi_45_0_56_0")
    h_pass=file_xi.Get("h_nvertices_45_0_56_0")
    h_total=file_xi.Get("h_nvertices_all")
    num=h_pass.GetBinContent(int(numI)+1)
    den=h_total.GetBinContent(int(numI)+1)
    numa=r.random()
    if numI==0 or den==0:
        return True
    ratio=num/den
    h_pass_pix1=file_xi.Get("h_nvertices_45_1_56_0")
    num1=h_pass_pix1.GetBinContent(int(numI)+1)
    ratio1=num1/den
    h_pass_pix2=file_xi.Get("h_nvertices_45_0_56_1")
    num2=h_pass_pix2.GetBinContent(int(numI)+1)
    ratio2=num2/den

    if numa<ratio and signal_bin=="pixel-pixel":
        return True
    if signal_bin=="pixel-pixel":
        return False
    #print "I get here before mixing in 2nd proton for signal"
    if numa>ratio and numa<(ratio+ratio1):
        file_xi=TFile("xi.root")
        h_xi_45=file_xi.Get("h_xi_23")
        xi_45=h_xi_45.GetRandom()
        xi["23"].append(xi_45)
        #print "Mixing in 2nd proton for signal 45"
        return True
    elif numa>ratio and numa<(ratio+ratio1+ratio2):
        file_xi=TFile("xi.root")
        h_xi_56=file_xi.Get("h_xi_123")
        xi_56=h_xi_56.GetRandom()
        xi["123"].append(xi_56)
        #print "Mixing in 2nd proton for signal 56"
        return True



def passPPSSimMixingSignalMulti(numI,xi):
    #return True
    file_xi=TFile("xi.root")
    #h_pass=file_xi.Get("h_nvertices_multi_45_0_56_0")
    h_pass=file_xi.Get("h_nvertices_45_0_56_0")
    h_total=file_xi.Get("h_nvertices_all")
    if numI==0:
        return True
    num=h_pass.GetBinContent(int(numI)+1)
    den=h_total.GetBinContent(int(numI)+1)
    numa=r.random()
    numb=r.random()
    numc=r.random()
    ratio=num/den
    #print "Random number: ",num1
    #print "ratio: ",ratio
    h_pass_strip1=file_xi.Get("h_nvertices_45_1pixel_1strip")
    h_total_strip1=file_xi.Get("h_nvertices_45_1")
    num1=h_pass_strip1.GetBinContent(int(numI)+1)
    den1=h_total_strip1.GetBinContent(int(numI)+1)
    if den1==0: return True
    ratio1=num1/den1
    h_pass_strip2=file_xi.Get("h_nvertices_56_1pixel_1strip")
    h_total_strip2=file_xi.Get("h_nvertices_56_1")
    num2=h_pass_strip2.GetBinContent(int(numI)+1)
    den2=h_total_strip2.GetBinContent(int(numI)+1)
    ratio2=num2/den2
    if numa<ratio and numb<ratio1 and numc<ratio2:
        return True
    else:
        return False

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

def protonDataMixing(xi,signal_bin):
    file_xi=TFile("xi.root")
    #num1=r.random()
    end=""
    if signal_bin=="multiRP": 
        end="_multi"
    else:
        end="_noMultiRP_doubletag_2pxl"
    h_xi_45=file_xi.Get("h_xi_23{0}".format(end))
    h_xi_56=file_xi.Get("h_xi_123{0}".format(end))
    xi_45=h_xi_45.GetRandom()
    xi_56=h_xi_56.GetRandom()
    xi["23"].append(xi_45)
    xi["123"].append(xi_56)
    if signal_bin=="multiPixel":
        numra=r.random()
            #Assuming here that rate of 1 track in pot is symmetric
        if numra<0.5:
            h_xi_45_2nd=file_xi.Get("h_xi_23_noMultiRP_2nd_doubletag_2pxl")
            xi_45_2nd=h_xi_45_2nd.GetRandom()
            xi["23"].append(xi_45_2nd)
        else:
            h_xi_56_2nd=file_xi.Get("h_xi_123_noMultiRP_2nd_doubletag_2pxl")
            xi_56_2nd=h_xi_56_2nd.GetRandom()
            xi["123"].append(xi_56_2nd)
    return True

def passPPSSimMixing(xi,signal_bin):
    end=""
    file_xi=TFile("xi.root")
    if signal_bin=="multiRP":  
        end="_multi"
    else:
        end="_noMultiRP_doubletag_2pxl"
    h_xi_45=file_xi.Get("h_xi_23{0}".format(end))
    h_xi_56=file_xi.Get("h_xi_123{0}".format(end))
    xi_45=h_xi_45.GetRandom()
    xi_56=h_xi_56.GetRandom()
    passPPS=True
    xi["23"].append(xi_45)
    xi["123"].append(xi_56)
    if signal_bin=="multiPixel":
        numra=r.random()
        #Assuming here that rate of 1 track in pot is symmetric, can improve
        if numra<0.5:
            h_xi_45_2nd=file_xi.Get("h_xi_23_noMultiRP_2nd_doubletag")
            xi_45_2nd=h_xi_45_2nd.GetRandom()
            xi["23"].append(xi_45_2nd)
        else:
            h_xi_56_2nd=file_xi.Get("h_xi_123_noMultiRP_2nd_doubletag")
            xi_56_2nd=h_xi_56_2nd.GetRandom()
            xi["123"].append(xi_56_2nd)
    return passPPS


def passPPSMulti(e,xi):
    left=False
    right=False
    passesPPS=False
    ii=0
    ii_multi=0
    for xi_ in e.proton_xi:
        if e.proton_arm[ii]==0 and e.proton_ismultirp_[ii]==1:
            if e.proton_trackpixshift1[ii]==0 and e.proton_trackpixshift2[ii_multi]==0:
                xi["23"].append(xi_)
                left=True
        if e.proton_arm[ii]==1 and e.proton_ismultirp_[ii]==1:
            if e.proton_trackpixshift1[ii]==0 and e.proton_trackpixshift2[ii_multi]==0:
                xi["123"].append(xi_)
                right=True
        if e.proton_ismultirp_[ii]==1: ii_multi=ii_multi+1
        ii=ii+1

    if left and right: passesPPS=True
    return passesPPS

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
    return True


def passPPSNew(e,xi,signal_bin,sample):
    left=False
    right=False
    passesPPS=False
    ii=0
    for detId_rp in e.proton_rpid:
        #pixel
        if detId_rp == 23 and e.proton_ismultirp_[ii]==0: 
            if e.proton_trackpixshift1[ii]==0:
                xi["23"].append(e.proton_xi[ii])
        #strips
        if detId_rp == 3 and e.proton_ismultirp_[ii]==0: 
            xi["3"].append(e.proton_xi[ii])
        #diamond
        if detId_rp == 16 and e.proton_ismultirp_[ii]==0: 
            xi["16"].append(e.proton_xi[ii])
        #pixel
        if detId_rp == 123 and e.proton_ismultirp_[ii]==0: 
            if e.proton_trackpixshift1[ii]==0:
                xi["123"].append(e.proton_xi[ii])
        #strips
        if detId_rp == 103 and e.proton_ismultirp_[ii]==0: 
            xi["103"].append(e.proton_xi[ii])
        #diamond
        if detId_rp == 116 and e.proton_ismultirp_[ii]==0: 
            xi["116"].append(e.proton_xi[ii])
        ii=ii+1

    passesPPS_0_0=False
    passesPPS_0_1=False
    passesPPS_1_0=False
    if len(xi["123"])==1 and len(xi["23"])==1:
        passesPPS_0_0=True
    if len(xi["123"])==1 and len(xi["23"])==2:
        passesPPS_1_0=True
    if len(xi["123"])==2 and len(xi["23"])==1:
        passesPPS_0_1=True
    if signal_bin=="multiPixel" and (passesPPS_0_1 or passesPPS_1_0) and sample!="ExclusiveMC":
        return True
    if signal_bin=="multiPixel" and passesPPS_0_0 and sample=="ExclusiveMC":
        return True
    if signal_bin=="pixel-pixel" and passesPPS_0_0:
        return True
    return False

def AddFilesToChain(chain,ListOfFiles,DATA):
    i=0
    num_events=0
    for file in ListOfFiles:
        i=i+1
        if not DATA:
            statinfo = os.stat(file)
            if statinfo.st_size > 0:
                chain.Add(file)
                f=TFile(file)
                h=TH1F()
                h=f.Get("totalEvents/h_total_events")
                num_events=num_events+h.GetEntries()
        if DATA:
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
        for d in os.listdir(mypath_prefix+'{0}/{1}'.format(sample_name,file_dir)):
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
        for i in os.listdir(mypath_prefix+'/{0}/{1}/{2}'.format(sample_name,file_dir,sub_dir)):
            mypath=mypath_prefix+'{0}/{1}/{2}/{3}/'.format(sample_name,file_dir,sub_dir,i)
            ListOfFiles += [mypath_prefix+'{0}/{1}/{2}/{3}/{4}'.format(sample_name,file_dir,sub_dir,i,f) for f in listdir(mypath) if isfile(join(mypath, f))]

    if directory_type == 'specific':
        mypath=mypath_prefix+'{0}/{1}/'.format(sample_name,file_dir)
        ListOfFiles = [mypath_prefix+'{0}/{1}/{2}'.format(sample_name,file_dir,f) for f in listdir(mypath) if isfile(join(mypath, f))]
        output_name=sample_name+'_'+file_dir.split('_')[1].split('/')[0]+'_'+file_dir.split('/')[2]

    return ListOfFiles,output_name




#Functions I don't really use anymore

def interactionsFromVertices(nvertices):
    #these numbers were determined fitting the exclusive WW sample a0w=1e-6.
    if nvertices < 45:
        interactions=1.01608*nvertices+5.26672
    if nvertices > 44:
        interactions=0.42657*nvertices+34.5129
    return interactions


def passPPSSimMixingSignal(numI,xi):
    #Sector45
    prob45=(100.-2.718*numI+0.0349*numI*numI-0.000187*numI*numI*numI)/100.
    #Sector56
    prob56=(100.-2.892*numI+0.0387*numI*numI-0.000216*numI*numI*numI)/100.
    tot_prob=prob45*prob56
    num1=r.random()
    num2=r.random()
    if num1 < prob45 and num2 < prob56:
        return True
    else:
        if num1< prob45 and num2 > prob56 and num2 < (prob56+0.295310):
            file_xi=TFile("xi.root")
            h_xi_56=file_xi.Get("h_xi_123")
            xi_56=h_xi_56.GetRandom()
            xi["123"].append(xi_56)
            return True
        if num2< prob56 and num1 > prob45 and num1 < (prob45+0.292298):
            file_xi=TFile("xi.root")
            h_xi_45=file_xi.Get("h_xi_23")
            xi_45=h_xi_45.GetRandom()
            xi["23"].append(xi_45)
            return True
        if num2> prob56 and num1 > prob45 and num1 < (prob45+0.292298) and num2 < (prob56+0.295310):
            file_xi=TFile("xi.root")
            h_xi_56=file_xi.Get("h_xi_123")
            xi_56=h_xi_56.GetRandom()
            xi["123"].append(xi_56)
            h_xi_45=file_xi.Get("h_xi_23")
            xi_45=h_xi_45.GetRandom()
            xi["23"].append(xi_45)
            return False
        return False


def passPPSSimMixing23(xi):
    file_xi=TFile("xi.root")
    num1=r.random()
    returnProton=False
    if num1 < 0.292298:
        h_xi_45=file_xi.Get("h_xi_23")
        xi_45=h_xi_45.GetRandom()
        xi["23"].append(xi_45)
        returnProton=True
    return returnProton

def passPPSSimMixing123(xi):
    file_xi=TFile("xi.root")
    num2=r.random()
    returnProton=False
    if num2 < 0.295310:
        h_xi_56=file_xi.Get("h_xi_123")
        xi_56=h_xi_56.GetRandom()
        xi["123"].append(xi_56)
        returnProton=True
    return returnProton


def passPPSNewStrip(e,xi):
    ii=0
    for detId_rp in e.proton_rpid:
        #pixel
        if detId_rp == 3 and e.proton_ismultirp_[ii]==0: 
            #if e.proton_trackpixshift1[ii]==0:
            xi["3"].append(e.proton_xi[ii])
        #pixel
        if detId_rp == 103 and e.proton_ismultirp_[ii]==0: 
            #if e.proton_trackpixshift1[ii]==0:
            xi["103"].append(e.proton_xi[ii])
        ii=ii+1
    return True


def passPPSSimMixingSignalSingle1Pileup(xi):
    num1=r.random()
    num2=r.random()
    #proton_mixedin=False
    if num2 < 0.295310:
        file_xi=TFile("xi.root")
        h_xi_56=file_xi.Get("h_xi_123")
        xi_56=h_xi_56.GetRandom()
        xi["123"].append(xi_56)
        #return True
    if num1 < 0.292298:
        file_xi=TFile("xi.root")
        h_xi_45=file_xi.Get("h_xi_23")
        xi_45=h_xi_45.GetRandom()
        xi["23"].append(xi_45)
        #return True
    if (len(xi["23"]) == 1 and len(xi["123"])==2) or (len(xi["23"]) == 1 and len(xi["123"])==1) or (len(xi["23"]) == 2 and len(xi["123"])==1):
        return True
    else:    return False
    #return proton_mixedin



