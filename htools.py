#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-16-2017
from ROOT import *
import math as m

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
            arm45=True
            xi_45_n=e.rp_tracks_xi[ii]
        if t == 1981284352 and e.rp_tracks_x[ii] < 11.5:
            arm45=True
            xi_45_f=e.rp_tracks_xi[ii]
        if t == 1998061568 and e.rp_tracks_x[ii] < 10:
            arm56=True
            xi_56_n=e.rp_tracks_xi[ii]
        if t == 1997537280 and e.rp_tracks_x[ii] < 9.5:
            arm56=True
            xi_56_f=e.rp_tracks_xi[ii]
        ii=ii+1
    
    if arm56 and arm45:
        return True
    else:
        return False
