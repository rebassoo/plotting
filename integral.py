#!/usr/bin/env python                                                                                   
#Finn Rebassoo, LLNL 01-06-2020 
import math as m
import sys
from ptools import *
from ROOT import *
from htools import *


filename=sys.argv[1]

#for 


#List all the histograms in the root file
f0=TFile(filename)
#f=TFile.Open("histos/WWTo2L2Nu_13TeV-powheg.root")
f0.cd()
List=f0.GetListOfKeys()
it=0
histo_list=[]
for k1 in List:
    h1 = k1.ReadObj()
    it=it+1
    #print "Histo {0}: {1}".format(it,h1.GetName())
    #print "{0}, Integral: {1}".format(k1.GetName(),h1.Integral(0,1001))
    print "{0}, Integral: {1}".format(k1.GetName(),h1.Integral(0,20))
    #histo_list.append(h1.GetName())
#print histo_list
