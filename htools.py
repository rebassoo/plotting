#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-16-2017
from ROOT import *
import math as m
import random as r

def passAcc(x_value,detId_value):
    #print x_value
    if detId_value == 1980760064 and x_value < 11.5: 
        return True
    if detId_value == 1981284352 and x_value < 11.5:
        return True
    if detId_value == 1998061568 and x_value < 10:
        return True
    if detId_value == 1997537280 and x_value < 9.5:
        return True
    return False

def addPUProtons(numInteractions,ev_sd,ev_dd,ev_nondiff,ev_elastic,ev_cd):
    counting=[0,0,0,0,0,0,0,0,0,0]
    arm45=False
    arm56=False
    ii=0
    numSD=0
    numDD=0
    numElastic=0
    numCD=0
    numnonDiff=0
    #First list in dictionary is Xi value
    #Second list in dictionary is interaction number
    #Third list in dictionary is what type of interaction it came from 0=sd, 1=dd, 2=nondiff, 3=elastic, 4=cd
    di={1980760064:[[],[],[]],1981284352:[[],[],[]],1998061568:[[],[],[]],1997537280:[[],[],[]]}
    #print "addPUProtons"
    #print numInteractions
    for i in range(0,numInteractions):
        num=r.random()
        num=num*1.0082
        if num > 1:
            #Do cd
            ev_cd.GetEntry(int(num*10000.-10000.))
            #What about multiple protons per interactions, is this possibles? Yes?
            ii=0
            for t in ev_cd.rp_tracks_x:
                passA=passAcc(t,ev_cd.rp_tracks_detId[ii])
                if passA:
                    di[ev_cd.rp_tracks_detId[ii]][0].append(ev_cd.rp_tracks_xi[ii])
                    di[ev_cd.rp_tracks_detId[ii]][1].append(i)
                    di[ev_cd.rp_tracks_detId[ii]][2].append(4)
                    numCD=numCD+1
                ii=ii+1


        if num > 0.4352 and num < 1:
            #Do non-diff
            ev_nondiff.GetEntry(int(num*10000.-4352))
            #What about multiple protons per interactions, is this possibles? Yes?
            ii=0
            for t in ev_nondiff.rp_tracks_x:
                passA=passAcc(t,ev_nondiff.rp_tracks_detId[ii])
                if passA:
                    di[ev_nondiff.rp_tracks_detId[ii]][0].append(ev_nondiff.rp_tracks_xi[ii])
                    di[ev_nondiff.rp_tracks_detId[ii]][1].append(i)
                    di[ev_nondiff.rp_tracks_detId[ii]][2].append(2)
                    numnonDiff=numnonDiff+1
                ii=ii+1
            
        if num<0.12832:
            #Do single dissoc
            ev_sd.GetEntry(int(num*10000.))
            #What about multiple protons per interactions, is this possibles? Yes?
            ii=0
            for t in ev_sd.rp_tracks_x:
                passA=passAcc(t,ev_sd.rp_tracks_detId[ii])
                if passA:
                    di[ev_sd.rp_tracks_detId[ii]][0].append(ev_sd.rp_tracks_xi[ii])
                    di[ev_sd.rp_tracks_detId[ii]][1].append(i)
                    di[ev_sd.rp_tracks_detId[ii]][2].append(0)
                    #di[ev_sd.rp_tracks_detId[ii]][1][0]=di[ev_sd.rp_tracks_detId[ii]][1][0]+1
                    #di[ev_sd.rp_tracks_detId[ii]].append(ev_sd.rp_tracks_x[ii])
                    numSD=numSD+1
                ii=ii+1

        if num<0.2163 and num>0.12832:
            #Do double dissoc:
            ev_dd.GetEntry(int(num*10000.-1283))
            #What about multiple protons per interactions, is this possibles? Yes?
            ii=0
            for t in ev_dd.rp_tracks_x:
                passA=passAcc(t,ev_dd.rp_tracks_detId[ii])
                if passA:
                    di[ev_dd.rp_tracks_detId[ii]][0].append(ev_dd.rp_tracks_xi[ii])
                    di[ev_dd.rp_tracks_detId[ii]][1].append(i)
                    di[ev_dd.rp_tracks_detId[ii]][2].append(1)
                    #di[ev_dd.rp_tracks_detId[ii]][1][1]=di[ev_dd.rp_tracks_detId[ii]][1][1]+1
                    #di[ev_dd.rp_tracks_detId[ii]].append(ev_dd.rp_tracks_x[ii])
                    numDD=numDD+1
                ii=ii+1

        if num<0.4352 and num>0.2163:        
            #Elastic
            ev_elastic.GetEntry(int(num*10000.-2163))
            #What about multiple protons per interactions, is this possibles? Yes?
            ii=0
            for t in ev_elastic.rp_tracks_x:
                passA=passAcc(t,ev_elastic.rp_tracks_detId[ii])
                if passA:
                    di[ev_elastic.rp_tracks_detId[ii]][0].append(ev_elastic.rp_tracks_xi[ii])
                    di[ev_elastic.rp_tracks_detId[ii]][1].append(i)
                    di[ev_elastic.rp_tracks_detId[ii]][2].append(3)
                    #di[ev_elastic.rp_tracks_detId[ii]][1][1]=di[ev_elastic.rp_tracks_detId[ii]][1][1]+1
                    #di[ev_elastic.rp_tracks_detId[ii]].append(ev_elastic.rp_tracks_x[ii])
                    numElastic=numElastic+1
                ii=ii+1

    arm45=False
    arm56=False
    #print di
    if len(di[1980760064][0]) ==1 or len(di[1981284352][0]) == 1:
        arm45=True
        #if len(di[1980760064][0]) ==1 and len(di[1981284352][0]) == 1:
        #    arm45=False
    if len(di[1998061568][0]) ==1 or len(di[1997537280][0]) == 1:
        #if di[1998061568][1] != di[1997537280][1]:
        #    print "Different tracks in arm 56"
        arm56=True
        #    arm56=False

    if arm56 and arm45:
        counting[0]=counting[0]+numSD
        counting[1]=counting[1]+numDD
        counting[2]=counting[2]+numnonDiff
        counting[3]=counting[3]+numElastic
        counting[4]=counting[4]+numCD

        #This block finds out whether there is a double tag from a single interaction
        count_overlap=0
        if len(set(di[1980760064][1]) & set (di[1998061568][1])) > 0: count_overlap=1
        if len(set(di[1980760064][1]) & set (di[1997537280][1])) > 0: count_overlap=1
        if len(set(di[1981284352][1]) & set (di[1998061568][1])) > 0: count_overlap=1
        if len(set(di[1981284352][1]) & set (di[1997537280][1])) > 0: count_overlap=1

        if count_overlap>0:
            print "Overlap"
            print di
        counting[9]=count_overlap
        
        #This block finds out whether there is a double tag from two SD events (they can be from 2 interactions or 1 interaction
        twoRandomSD=0
        if 0 in di[1980760064][2] and 0 in di[1998061568][2]: twoRandomSD=1
        if 0 in di[1980760064][2] and 0 in di[1997537280][2]: twoRandomSD=1
        if 0 in di[1981284352][2] and 0 in di[1998061568][2]: twoRandomSD=1
        if 0 in di[1981284352][2] and 0 in di[1997537280][2]: twoRandomSD=1
        counting[8]=twoRandomSD

        #This block finds out whether there is a double tag from two DD events (they can be from 2 interactions or 1 interaction
        twoRandomDD=0
        if 1 in di[1980760064][2] and 1 in di[1998061568][2]: twoRandomDD=1
        if 1 in di[1980760064][2] and 1 in di[1997537280][2]: twoRandomDD=1
        if 1 in di[1981284352][2] and 1 in di[1998061568][2]: twoRandomDD=1
        if 1 in di[1981284352][2] and 1 in di[1997537280][2]: twoRandomDD=1
        counting[7]=twoRandomDD

        #This block finds out whether there is a double tag from two CD events (they can be from 2 interactions or 1 interaction
        twoRandomCD=0
        if 4 in di[1980760064][2] and 4 in di[1998061568][2]: twoRandomCD=1
        if 4 in di[1980760064][2] and 4 in di[1997537280][2]: twoRandomCD=1
        if 4 in di[1981284352][2] and 4 in di[1998061568][2]: twoRandomCD=1
        if 4 in di[1981284352][2] and 4 in di[1997537280][2]: twoRandomCD=1
        counting[6]=twoRandomCD


        return True, counting
    else:
        return False, counting


def passPPS(e,xi):
    left=False
    right=False
    passesPPS=False
    ii=0
    #xi2,xi3,xi102,xi103=[],[],[],[]
    for detId_rp in e.rp_tracks_detId:
                    #print detId_rp
        if detId_rp == 2: 
            left=True
                    #if lessthan6: print "DetId 2, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["2"].append(e.rp_tracks_xi[ii])
        if detId_rp == 3: 
            left=True
                    #if lessthan6: print "DetId 3, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["3"].append(e.rp_tracks_xi[ii])
        if detId_rp == 102: 
            right=True
                    #xi_right.append(float(e.rp_tracks_xi))
                    #if lessthan6: print "DetId 102, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["102"].append(e.rp_tracks_xi[ii])
        if detId_rp == 103: 
            right=True
                    #xi_right.append(float(e.rp_tracks_xi))
                    #if lessthan6: print "DetId 103, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["103"].append(e.rp_tracks_xi[ii])
        ii=ii+1

    if (left == True) and (right == True):
        passesPPS=True
        
    if len(xi["2"]) > 1 or len(xi["3"]) > 1 or len(xi["102"]) > 1 or len(xi["103"]) > 1:
        print "This event has multiple tracks in a single pot"
        print "Xi_2:",xi["2"],"Xi_3:",xi["3"],"Xi_102:",xi["102"],"Xi_103:",xi["103"]
        #passesPPS=False

    return passesPPS


#def passPPSSim(e,xi_reco,xi_sim):
def passPPSSim(e):
    p_pos_four_vector=TLorentzVector()
    p_neg_four_vector=TLorentzVector()
    ip=0
    xi_neg=0.
    xi_pos=0.
    theta_y_1=0
    for p in e.hepmc_pz:
        if p < 0 and abs(p) > 1000:
            #p_neg goes to sector 56
            p_neg_four_vector=TLorentzVector(e.hepmc_px[ip],e.hepmc_py[ip],e.hepmc_pz[ip],e.hepmc_energy[ip])
            p_neg_incom=TLorentzVector(0,0,-6500.,m.sqrt(0.93827231*0.93827231+6500*6500))
            #t1=calculate_t(p_neg_incom,p_neg_four_vector)
            pt=m.sqrt(e.hepmc_px[ip]*e.hepmc_px[ip]+e.hepmc_py[ip]*e.hepmc_py[ip])
            
            #print t1,m.sqrt(e.hepmc_px[ip]*e.hepmc_px[ip]+e.hepmc_py[ip]*e.hepmc_py[ip])
            #print e.hepmc_px[ip],e.hepmc_py[ip],e.hepmc_pz[ip],e.hepmc_energy[ip]
            xi_neg=e.hepmc_pz[ip]/6500.
            #h_xi_1.Fill(1.-abs(xi_neg))
            theta_y_1=abs(m.atan(e.hepmc_py[ip]/e.hepmc_pz[ip]))
            #print 1.-abs(xi_neg)
        if p > 0 and abs(p) > 1000:
            #p_pos goes to sector 45
            p_pos_four_vector=TLorentzVector(e.hepmc_px[ip],e.hepmc_py[ip],e.hepmc_pz[ip],e.hepmc_energy[ip])
            p_pos_incom=TLorentzVector(0,0,6500.,m.sqrt(0.93827231*0.93827231+6500*6500))
            #t2=calculate_t(p_pos_four_vector,p_pos_incom)
            #print t2,e.hepmc_px[ip],e.hepmc_py[ip],e.hepmc_pz[ip],e.hepmc_energy[ip]
            xi_pos=e.hepmc_pz[ip]/6500.
            #h_xi_2.Fill(1.-abs(xi_pos))
            theta_y_2=abs(m.atan(e.hepmc_py[ip]/e.hepmc_pz[ip]))
        ip=ip+1
    xi_45=1.-abs(xi_pos)
    xi_56=1.-abs(xi_neg)


    ii=0
    xi_45_n=0
    xi_45_f=0
    xi_56_n=0
    xi_56_f=0
    arm45=False
    arm56=False
    for t in e.rp_tracks_detId:
        if t == 1980760064 and e.rp_tracks_x[ii] < 11.5: 
        #if t == 1980760064 and e.rp_tracks_x[ii] < 14: 
            arm45=True
            xi_45_n=e.rp_tracks_xi[ii]
        if t == 1981284352 and e.rp_tracks_x[ii] < 11.5:
        #if t == 1981284352 and e.rp_tracks_x[ii] < 14:
            arm45=True
            xi_45_f=e.rp_tracks_xi[ii]
        if t == 1998061568 and e.rp_tracks_x[ii] < 10:
        #if t == 1998061568 and e.rp_tracks_x[ii] < 12.5:
            arm56=True
            xi_56_n=e.rp_tracks_xi[ii]
        if t == 1997537280 and e.rp_tracks_x[ii] < 9.5:
        #if t == 1997537280 and e.rp_tracks_x[ii] < 12:
            arm56=True
            xi_56_f=e.rp_tracks_xi[ii]
        ii=ii+1
    
    #if arm56 or arm45:
    #    if xi_45 > 0.2 or xi_45 < 0.01:
    #        print "This event has a generator Xi_45 outside of 0.01-0.2"
    #    if xi_56 > 0.2 or xi_45 < 0.01:
    #        print "This event has a generator Xi_56 outside of 0.01-0.2"

    if arm56 and arm45:
        return True
    else:
        return False
