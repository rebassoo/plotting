#!/usr/bin/env python                                                                                   
#Finn Rebassoo, LLNL 04-16-2020 
from makeSignalRegionPlotGeneral import *

muon_directory="2020-04-27-DataWithSignal"
electron_directory="2020-04-27-DataWithSignal-Electron"

#Ycut=["noYcut","Ycut"]
Ycut=["Ycut"]
signal_regions=["MultiRP","PixelPixel","MultiPixel"]
#signal_regions=["MultiRP"]
#makePlot(muon_directory,Ycut[0],"muon","template_5up",signal_regions[0])
#makePlot(muon_directory,Ycut[0],"muon","template_5up",signal_regions[1])
#sys.exit(1)
for y in Ycut:
    for s in signal_regions:
        makePlot(muon_directory,y,"muon","template_5up",s)
        makePlot(electron_directory,y,"electron","template_5up",s)
        
