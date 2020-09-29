#!/usr/bin/env python                                                                                   
#Finn Rebassoo, LLNL 04-16-2020 
from makeSignalRegionPlotGeneral import *

#muon_directory="2020-07-20-MuonMCOnly"
#muon_directory="2020-08-28-MuonNewDataNewSignalOldMC"
#electron_directory="2020-07-31-ElectronDataMC"
#electron_directory="2020-08-28-ElectronNewDataNewSignalOldMC"
#muon_directory="2020-09-23-MuonAllDataMC-JustDataSignal"
muon_directory="2020-09-23-MuonAllDataMC"
electron_directory="2020-09-23-ElectronAllDataMC"

#Ycut=["noYcut","Ycut"]
Ycut=["Ycut"]
#Ycut=["noYcut"]
signal_regions=["MultiRP","PixelPixel","MultiPixel"]
#signal_regions=["MultiRP"]
#makeplot(muon_directory,Ycut[1],"muon","template_5up",signal_regions[0],"2017")
for y in Ycut:
    for s in signal_regions:
        makeplot(muon_directory,y,"muon","template_5up",s,"2017",True)
        makeplot(electron_directory,y,"electron","template_5up",s,"2017",True)
        #sys.exit()
                
