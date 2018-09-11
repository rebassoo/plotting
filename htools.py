#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-16-2017
import math as m

def GetDphi(phi1,phi2):
    result = phi1-phi2
    #print result
    while result > m.pi: result = 2*m.pi - result
    while result < -m.pi: result = 2*m.pi + result
    return result

#def GetCrossingAngle(run,lumiblock):
#    crossingAngle=0
#    txtfile=''
#    if run > 303718: txtfile='xangle_afterTS2_STABLEBEAMS_CLEANUP.csv'
#    if run < 303718: txtfile='xangle_tillTS2_STABLEBEAMS_CLEANUP.csv'
#    f = open(txtfile)
#    for line in f:
#        if float(line.split(' ')[0]) == run and float(line.split(' ')[2]) == lumiblock:
#            crossingAngle=float(line.split(' ')[4])
#            #if crossingAngle < 150:
#            #    print crossingAngle
#            break
#    return crossingAngle

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
    if pot == 1981284352:
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
    if pot == 1998061568:
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
    if pot == 2023227392:
        if run > 503718: x_corr =x *m.cos(m.radians(8)) + y*m.sin(m.radians(8)) - 42.2
        else: x_corr = x - 42.05
        if crossingAngle ==120.: xi = x_corr / (-9.145*10)
        else:
            #0.46 cm per 10 murad, so 0.046 cm per 1 murad
            D_corr = (crossingAngle-120.)*0.046*10 - 9.145*10
            xi = x_corr / D_corr

    if pot == 2040004608:
        if run > 503718: x_corr =x *m.cos(m.radians(8)) + y*m.sin(m.radians(8)) - 42.2
        else: x_corr = x - 42.05
        if crossingAngle ==120.: xi = x_corr / (-7.291*10)
        else:
            #0.46 cm per 10 murad, so 0.046 cm per 1 murad
            D_corr = (crossingAngle-120.)*0.046*10 - 7.291*10
            xi = x_corr / D_corr

    return xi

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
    for detId_rp in e.rp_tracks_detId:
                    #print detId_rp
        #pixel
        if detId_rp == 2023227392: 
            #left=True
                    #if lessthan6: print "DetId 2, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["2023227392"].append(GetXi(e.rp_tracks_x[ii],e.rp_tracks_y[ii],2023227392,run,crossingAngle))
        #strips
        if detId_rp == 1981284352: 
            #left=True
                    #if lessthan6: print "DetId 3, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["1981284352"].append(GetXi(e.rp_tracks_x[ii],e.rp_tracks_y[ii],1981284352,run,crossingAngle))
        #diamond
        if detId_rp == "2070937600": 
            #left=True
                    #if lessthan6: print "DetId 3, Xi: {0}".format(e.rp_tracks_xi[i])
            #print e.rp_tracks_time[ii]
            xi["2070937600"].append(GetXi(e.rp_tracks_x[ii],e.rp_tracks_y[ii],2070937600,run,crossingAngle))
        #pixel
        if detId_rp == 2040004608: 
            #right=True
                    #xi_right.append(float(e.rp_tracks_xi))
                    #if lessthan6: print "DetId 102, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["2040004608"].append(GetXi(e.rp_tracks_x[ii],e.rp_tracks_y[ii],2040004608,run,crossingAngle))
        #strips
        if detId_rp == 1998061568: 
            #right=True
                    #xi_right.append(float(e.rp_tracks_xi))
                    #if lessthan6: print "DetId 103, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["1998061568"].append(GetXi(e.rp_tracks_x[ii],e.rp_tracks_y[ii],1998061568,run,crossingAngle))
        #diamond
        if detId_rp == "2054160384": 
            #left=True
                    #if lessthan6: print "DetId 3, Xi: {0}".format(e.rp_tracks_xi[i])
            xi["2054160384"].append(GetXi(e.rp_tracks_x[ii],e.rp_tracks_y[ii],2054160384,run,crossingAngle))
            if e.rp_tracks_time[ii] !=0:
                print e.rp_tracks_time[ii]
        ii=ii+1

    if len(xi["2040004608"])==1 and len(xi["2023227392"])==1:
        passesPPS=True
    #if (left == True) or (right == True):
    #    passesPPS=True
        
    #if len(xi["2"]) > 1 or len(xi["3"]) > 1 or len(xi["102"]) > 1 or len(xi["103"]) > 1:
    #    print "This event has multiple tracks in a single pot"
    #    print "Xi_2:",xi["2"],"Xi_3:",xi["3"],"Xi_102:",xi["102"],"Xi_103:",xi["103"]
    #    #passesPPS=False

    return passesPPS


