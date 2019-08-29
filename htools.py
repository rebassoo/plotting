#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-16-2017
import math as m
import random as r
import os
import sys
import json
from ROOT import *
from os import listdir
from os.path import isfile, join


def modifyJson(sample,num_events):
    changeNumEvents=False
    with open('samples_info.json') as json_file:
        data=json.load(json_file)
        print num_events
        print data[sample][0]
        if num_events != data[sample][0]:
            changeNumEvents=True
    
    if changeNumEvents:
        data[sample][0]=num_events
        with open("samples_info.json","w") as jsonFile:
            json.dump(data,jsonFile)

def GetDphi(phi1,phi2):
    result = phi1-phi2
    #print result
    while result > m.pi: result = 2*m.pi - result
    while result < -m.pi: result = 2*m.pi + result
    return result

def passPPSSimMixingSignal(numI):
    #Sector45
    prob45=100.-2.718*numI+0.0349*numI*numI-0.000187*numI*numI*numI
    #Sector56
    prob56=100.-2.892*numI+0.0387*numI*numI-0.000216*numI*numI*numI

    tot_prob=prob45*prob56
    num1=r.random()
    num2=r.random()
    if num1 < prob45 and num2 < prob56:
        return True
    else:
        return False

def protonDataMixing():
    file_xi=TFile("xi.root")
    #num1=r.random()
    h_xi_45=file_xi.Get("h_xi_23")
        #h_xi_56=file_xi.Get("h_pixel_xi_56_1track")
    h_xi_56=file_xi.Get("h_xi_123")
    xi_56=h_xi_56.GetRandom()
    xi_45=h_xi_45.GetRandom()
    #print "xi_45: ",xi_45
    #print "xi_56: ",xi_56
    xi=[xi_45,xi_56]
    return xi

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


def passPPSSimMixing():
    passPPS=False
    file_xi=TFile("xi.root")
    #h_num_pix_45=file_xi.Get("h_numPixTracks_45")
    #h_num_pix_56=file_xi.Get("h_numPixTracks_56")
    #num_pix_45=h_num_pix_45.GetRandom()
    #num_pix_56=h_num_pix_56.GetRandom()
    num1=r.random()
    num2=r.random()
    #print "num1: ",num1
    #print "num2: ",num2
    #if num_pix_45 == 1 and num_pix_56 ==1:
    #if num1 < 0.292298 and num2 < 0.295310:
        #h_xi_45=file_xi.Get("h_pixel_xi_45_1track")
    h_xi_45=file_xi.Get("h_xi_23")
        #h_xi_56=file_xi.Get("h_pixel_xi_56_1track")
    h_xi_56=file_xi.Get("h_xi_123")
    xi_45=h_xi_45.GetRandom()
    xi_56=h_xi_56.GetRandom()
    xi=[xi_45,xi_56]
        #print "xi: ",xi
    passPPS=True
    return passPPS,xi
    #else:
    #    xi=[]
    #    return passPPS,xi

def passPPSNewPixel(e,xi):
    ii=0
    for detId_rp in e.proton_rpid:
        #pixel
        if detId_rp == 23 and e.proton_ismultirp_[ii]==0: 
            xi["23"].append(e.proton_xi[ii])
        #pixel
        if detId_rp == 123 and e.proton_ismultirp_[ii]==0: 
            xi["123"].append(e.proton_xi[ii])
        ii=ii+1
    return True

def passPPSMulti(e,xi):
    left=False
    right=False
    passesPPS=False
    ii=0
    for xi_ in e.proton_xi:
        if e.proton_arm[ii]==0 and e.proton_ismultirp_[ii]==1:
            xi["23"].append(xi_)
            left=True
        if e.proton_arm[ii]==1 and e.proton_ismultirp_[ii]==1:
            xi["123"].append(xi_)
            right=True
        ii=ii+1
    if left and right: passesPPS=True
    return passesPPS

def passPPSNew(e,xi):
    left=False
    right=False
    passesPPS=False
    ii=0
    for detId_rp in e.proton_rpid:
        #pixel
        if detId_rp == 23 and e.proton_ismultirp_[ii]==0: 
            xi["23"].append(e.proton_xi[ii])
        #strips
        if detId_rp == 3 and e.proton_ismultirp_[ii]==0: 
            xi["3"].append(e.proton_xi[ii])
        #diamond
        if detId_rp == 16 and e.proton_ismultirp_[ii]==0: 
            xi["16"].append(e.proton_xi[ii])
        #pixel
        if detId_rp == 123 and e.proton_ismultirp_[ii]==0: 
            xi["123"].append(e.proton_xi[ii])
        #strips
        if detId_rp == 103 and e.proton_ismultirp_[ii]==0: 
            xi["103"].append(e.proton_xi[ii])
        #diamond
        if detId_rp == 116 and e.proton_ismultirp_[ii]==0: 
            xi["116"].append(e.proton_xi[ii])
        ii=ii+1

    if len(xi["123"])==1 and len(xi["23"])==1:
        passesPPS=True

    return passesPPS


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

def GetListOfFiles(sample_name,file_dir,DATA):
    print "Is is Data: ",DATA
    mypath_prefix='/hadoop/cms/store/user/rebassoo/'
    #mypath_prefix='/eos/uscms/store/user/rebassoo/'
    #print os.listdir('/hadoop/cms/store/user/rebassoo/{0}/{1}'.format(sample_name,file_dir))
    ListOfFiles=[]
    if sys.argv[1] == 'latest':
        if DATA: output_name=sample_name+'_'+file_dir.split('_')[1]
        else: output_name=sample_name
        m_date=0.
        m_date_string=0.
        m_time=0.
        m_time_string=0.
        for d in os.listdir(mypath_prefix+'/{0}/{1}'.format(sample_name,file_dir)):
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

    if sys.argv[1] == 'specific':
        mypath=mypath_prefix+'{0}/{1}/'.format(sample_name,file_dir)
        ListOfFiles = [mypath_prefix+'{0}/{1}/{2}'.format(sample_name,file_dir,f) for f in listdir(mypath) if isfile(join(mypath, f))]
        output_name=sample_name+'_'+file_dir.split('_')[1].split('/')[0]+'_'+file_dir.split('/')[2]

    return ListOfFiles,output_name



