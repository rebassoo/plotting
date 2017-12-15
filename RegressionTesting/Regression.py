#!/usr/bin/env python
#Finn Rebassoo, LLNL 10-12-2017
from ROOT import *
import datetime
import sys
#To make the validation plots do: python Regression.py plot
#To compare validation plots for different samples do: python Regression.py compare WWinclusive-10k-2017-10-13-10-07.root WWinclusive-10k-2017-10-13-10-09.root

udate=str(datetime.datetime.now())
time="{0}-{1}-{2}".format(udate.split(' ')[0],udate.split(' ')[1].split(':')[0],udate.split(' ')[1].split(':')[1])
print time

if sys.argv[1] == 'compare':
    sample1=sys.argv[2]
    sample2=sys.argv[3]
    tfile1 = TFile(sample1)
    tfile2 = TFile(sample2)
    names1=[h.GetName() for h in tfile1.GetListOfKeys()]
    print "names1: ",names1
    names2=[h.GetName() for h in tfile2.GetListOfKeys()]
    print "names2: ",names2
    #i=0
    c=TCanvas("c","",800,800)
    c.cd()
    c.Print("Comparison-{0}.pdf[".format(time))
    for hname in names1:
        if tfile1.Get(hname).ClassName() == "TH1F":
            h=TH1F()
            h=tfile1.Get(hname)
            h.Draw("hist")
            print hname
            i=0
            for hname2 in names2:
                if hname2 == hname:
                    print hname2
                    h2=TH1F()
                    h2=tfile2.Get(names2[i])
                    h2.SetLineColor(2)
                    h2.SetMarkerStyle(22)
                    h2.Draw("Samee")
                i=i+1
            c.Print("Comparison-{0}.pdf".format(time))
    c.Print("Comparison-{0}.pdf]".format(time))

if sys.argv[1] == 'plot':
    chain=TChain()
    chain.Add('../SlimmedNtuple.root/demo/SlimmedNtuple')
    names = [b.GetName() for b in chain.GetListOfBranches()]
    
    fout = TFile('WWinclusive-10k-{0}.root'.format(time),'recreate')
    fout.cd()
    
    for i in names:
        chain.Draw("{0}>>{0}".format(i))
        
    print names
    print "Muon entries: {0}".format(chain.GetEntries("muon_pt"))
    print "Electron entries: {0}".format(chain.GetEntries("electron_pt"))
        
    fout.Write()




