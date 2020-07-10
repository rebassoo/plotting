#!/usr/bin/env python                                                                                   
#Finn Rebassoo, LLNL 04-16-2020 
from makeSignalRegionPlotGeneral import *

#muon_directory="2020-04-30-MuonAllDataMC"
#muon_directory="2020-04-30-MuonAllDataMC-XiCMSCut"
muon_directory="2020-07-02-MuonAllDataMC-XiCMSCut"
#muon_directory="2020-06-24-MuonAllDataMC-XiCMSCut-LessStrictMixing"
#electron_directory="2020-04-30-ElectronAllDataMC"
#electron_directory="2020-04-30-ElectronAllDataMC-XiCMSCut"

Ycut=["noYcut","Ycut"]
#Ycut=["Ycut"]
#Ycut=["noYcut"]
signal_regions=["MultiRP","PixelPixel","MultiPixel"]
#signal_regions=["MultiRP"]
#makePlot(muon_directory,Ycut[0],"muon","template_5up",signal_regions[2],True)
#makePlot(electron_directory,Ycut[0],"electron","template_5up",signal_regions[0])
#makePlot(muon_directory,Ycut[0],"muon","template_5up",signal_regions[1])
#sys.exit(1)
for y in Ycut:
    for s in signal_regions:
        #makePlot(muon_directory,y,"muon","template_5up",s)
        makePlot(muon_directory,y,"muon","template_5up",s,True)
        #makePlot(electron_directory,y,"electron","template_5up",s)
        
