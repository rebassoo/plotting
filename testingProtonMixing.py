#!/usr/bin/env python
#Finn Rebassoo, LLNL 12-2016-01
import os
from ROOT import *
import math as m
from htools import *
import sys
import time

h_xi_1_control_notPPS=TH1F("h_xi_1_control_notPPS",";#xi_{1};",128,0,0.32)
h_xi_2_control_notPPS=TH1F("h_xi_2_control_notPPS",";#xi_{2};",128,0,0.32)


for i in range(0,10000):
    xi = {"3":[],"16":[],"23":[],"103":[],"116":[],"123":[]}
    xi_data=protonDataMixing()
    xi["23"].append(xi_data[0])
    xi["123"].append(xi_data[1])
    h_xi_1_control_notPPS.Fill(xi["23"][0])#,pileupw*rw_extrk*rw_failPPS)
    h_xi_2_control_notPPS.Fill(xi["123"][0])#,pileupw*rw_extrk*rw_failPPS)
        



