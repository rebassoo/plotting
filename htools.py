#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-16-2017
import math as m
import random as r
from ROOT import *
import os
import sys
from os import listdir
from os.path import isfile, join



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
        if detId_rp == 23: 
            xi["23"].append(e.proton_xi[ii])
        #pixel
        if detId_rp == 123: 
            xi["123"].append(e.proton_xi[ii])
        ii=ii+1
    return True

def passPPSNew(e,xi):
    left=False
    right=False
    passesPPS=False
    ii=0
    #print "Run: ",e.run
    #print "Lumiblock: ",e.lumiblock
    run=e.run
    lumiblock=e.lumiblock
    for detId_rp in e.proton_rpid:
        #pixel
        if detId_rp == 23: 
            xi["23"].append(e.proton_xi[ii])
        #strips
        if detId_rp == 3: 
            xi["3"].append(e.proton_xi[ii])
        #diamond
        if detId_rp == 16: 
            xi["16"].append(e.proton_xi[ii])
        #pixel
        if detId_rp == 123: 
            xi["123"].append(e.proton_xi[ii])
        #strips
        if detId_rp == 103: 
            xi["103"].append(e.proton_xi[ii])
        #diamond
        if detId_rp == 116: 
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
    #if i>5:
    #    break


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



def GetCrossingAngles():
    crossingAngles=dict()
    run=0
    lumiblock = 0
    crossingAngle=0
    txtfile='xangle_afterTS2_STABLEBEAMS_CLEANUP.csv'
    f = open(txtfile)
    for line in f:
        run=line.split(' ')[0]
        lumiblock=line.split(' ')[2]
        crossingAngle=line.split(' ')[4]
        crossingAngles['{0}:{1}'.format(run,lumiblock)]=crossingAngle
    txtfile='xangle_tillTS2_STABLEBEAMS_CLEANUP.csv'
    f2 = open(txtfile)
    for line in f2:
        run=line.split(' ')[0]
        lumiblock=line.split(' ')[2]
        crossingAngle=line.split(' ')[4]
        crossingAngles['{0}:{1}'.format(run,lumiblock)]=crossingAngle
    return crossingAngles
    

def GetXi(x,y,pot,run,crossingAngle):
    x_corr=0
    #crossingAngle=GetCrossingAngle(run,lumiblock)
    D=100000.
    xi=0.
    #print "x,:",x
    #print "crossing Angle: ",crossingAngle
    if pot == 3:
        #Alignment from Jan's talk 30Jan2017 and his 20Feb2018 talk for postTS2
        #print "x of track: ",x
        if run > 303718: x_corr = x *m.cos(m.radians(8)) + y*m.sin(m.radians(8)) - 3.6
        else:    x_corr = x - 3.7
        #print "x,:",x_corr
        #Dispersion values in cm, x values in mm
        #Dispersion values come from Fricis talk 2017_11_22
        #Using 120 as starting point
        #print crossingAngle
        if crossingAngle ==120.: xi = x_corr / (-9.145*10)
        else:
            #0.46 cm per 10 murad, so 0.046 cm per 1 murad
            D_corr = (crossingAngle-120.)*0.046*10 - 9.145*10
            xi = x_corr / D_corr
        #if crossingAngle ==130.: xi = x_corr / (-8.591*10)
        #if crossingAngle ==140.: xi = x_corr / (-9.226*10)
    if pot == 103:
        #Alignment from Jan's talk 30Jan2017 and his 20Feb2018 talk for postTS2
        #print "x of track: ",x
        if run > 303718: x_corr = x *m.cos(m.radians(8)) + y*m.sin(m.radians(8)) - 2.8
        else: x_corr = x - 2.75
        #print "x,:",x_corr
        #Dispersion values in cm, x values in mm
        if crossingAngle ==120.: xi = x_corr / (-7.291*10)
        else:
            #0.46 cm per 10 murad, so 0.046 cm per 1 murad
            D_corr = (crossingAngle-120.)*0.046*10 - 7.291*10
            xi = x_corr / D_corr
        #if crossingAngle ==130.: xi = x_corr / (-6.621*10)
        #if crossingAngle ==140.: xi = x_corr / (-6.191*10)

    #This is for pixels
    #Use same dispersion values as for strips?
    if pot == 23:
        if run > 503718: x_corr =x *m.cos(m.radians(8)) + y*m.sin(m.radians(8)) - 42.2
        else: x_corr = x - 42.05
        if crossingAngle ==120.: xi = x_corr / (-9.145*10)
        else:
            #0.46 cm per 10 murad, so 0.046 cm per 1 murad
            D_corr = (crossingAngle-120.)*0.046*10 - 9.145*10
            xi = x_corr / D_corr

    if pot == 123:
        if run > 503718: x_corr =x *m.cos(m.radians(8)) + y*m.sin(m.radians(8)) - 42.2
        else: x_corr = x - 42.05
        if crossingAngle ==120.: xi = x_corr / (-7.291*10)
        else:
            #0.46 cm per 10 murad, so 0.046 cm per 1 murad
            D_corr = (crossingAngle-120.)*0.046*10 - 7.291*10
            xi = x_corr / D_corr

    return abs(xi)


def passPPS(e,xi,crossingAngle):
    left=False
    right=False
    passesPPS=False
    ii=0
    #print "Run: ",e.run
    #print "Lumiblock: ",e.lumiblock
    run=e.run
    lumiblock=e.lumiblock
    #crossingAngle=GetCrossingAngle(run,lumiblock)
    for detId_rp in e.pps_track_rpid:
                    #print detId_rp
        #pixel
        if detId_rp == 23: 
            #left=True
                    #if lessthan6: print "DetId 2, Xi: {0}".format(e.pps_track_xi[i])
            xi["23"].append(GetXi(e.pps_track_x[ii],e.pps_track_y[ii],23,run,crossingAngle))
        #strips
        if detId_rp == 3: 
            #left=True
                    #if lessthan6: print "DetId 3, Xi: {0}".format(e.pps_track_xi[i])
            xi["3"].append(GetXi(e.pps_track_x[ii],e.pps_track_y[ii],3,run,crossingAngle))
        #diamond
        if detId_rp == "16": 
            #left=True
                    #if lessthan6: print "DetId 3, Xi: {0}".format(e.pps_track_xi[i])
            #print e.pps_tracktime[ii]
            xi["16"].append(GetXi(e.pps_track_x[ii],e.pps_track_y[ii],16,run,crossingAngle))
        #pixel
        if detId_rp == 123: 
            #right=True
                    #xi_right.append(float(e.pps_track_xi))
                    #if lessthan6: print "DetId 102, Xi: {0}".format(e.pps_track_xi[i])
            xi["123"].append(GetXi(e.pps_track_x[ii],e.pps_track_y[ii],123,run,crossingAngle))
        #strips
        if detId_rp == 103: 
            #right=True
                    #xi_right.append(float(e.pps_track_xi))
                    #if lessthan6: print "DetId 103, Xi: {0}".format(e.pps_track_xi[i])
            xi["103"].append(GetXi(e.pps_track_x[ii],e.pps_track_y[ii],103,run,crossingAngle))
        #diamond
        if detId_rp == "116": 
            #left=True
                    #if lessthan6: print "DetId 3, Xi: {0}".format(e.pps_track_xi[i])
            xi["116"].append(GetXi(e.pps_track_x[ii],e.pps_track_y[ii],116,run,crossingAngle))
            #if e.pps_tracktime[ii] !=0:
            #    print e.pps_tracktime[ii]
        ii=ii+1

    if len(xi["123"])==1 and len(xi["23"])==1:
        passesPPS=True
    #if (left == True) or (right == True):
    #    passesPPS=True
        
    #if len(xi["2"]) > 1 or len(xi["3"]) > 1 or len(xi["102"]) > 1 or len(xi["103"]) > 1:
    #    print "This event has multiple tracks in a single pot"
    #    print "Xi_2:",xi["2"],"Xi_3:",xi["3"],"Xi_102:",xi["102"],"Xi_103:",xi["103"]
    #    #passesPPS=False

    return passesPPS

