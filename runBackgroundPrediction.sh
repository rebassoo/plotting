#!/bin/bash

python makeSignalRegionPlotGeneral.py 2019-11-05-Pixel-Pixel noYcut muon 5_up
python makeSignalRegionPlotGeneral.py 2019-11-05-MultiRP noYcut muon 5_up
python makeSignalRegionPlotGeneral.py 2019-11-08-MultiPixel noYcut muon 5_up

python makeSignalRegionPlotGeneral.py 2019-11-05-Pixel-Pixel noYcut muon template
python makeSignalRegionPlotGeneral.py 2019-11-05-MultiRP noYcut muon template
python makeSignalRegionPlotGeneral.py 2019-11-08-MultiPixel noYcut muon template

python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-Pixel-Pixel noYcut electron 5_up
python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-MultiRP noYcut electron 5_up
python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-MultiPixel noYcut electron 5_up

python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-Pixel-Pixel noYcut electron template
python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-MultiRP noYcut electron template
python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-MultiPixel noYcut electron template



#python makeSignalRegionPlotGeneral.py 2019-11-05-Pixel-Pixel Ycut muon 5_up
#python makeSignalRegionPlotGeneral.py 2019-11-05-MultiRP Ycut muon 5_up
#python makeSignalRegionPlotGeneral.py 2019-11-08-MultiPixel Ycut muon 5_up

#python makeSignalRegionPlotGeneral.py 2019-11-05-Pixel-Pixel Ycut muon template
#python makeSignalRegionPlotGeneral.py 2019-11-05-MultiRP Ycut muon template
#python makeSignalRegionPlotGeneral.py 2019-11-08-MultiPixel Ycut muon template

#python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-Pixel-Pixel Ycut electron 5_up
#python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-MultiRP Ycut electron 5_up
#python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-MultiPixel Ycut electron 5_up

#python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-Pixel-Pixel Ycut electron template
#python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-MultiRP Ycut electron template
#python makeSignalRegionPlotGeneral.py 2019-11-08-Electron-MultiPixel Ycut electron template
