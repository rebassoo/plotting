#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-16-2017

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


