#!/usr/bin/env python
import subprocess
import os

for i in range(0,50):
    subprocess.call("python histos_quick.py latest muon GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6 crab_GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6-signal-proton-propagation-dilepton -nb multi {0}".format(i),shell=True)
    os.popen('cp GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6.root signal_running/GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6_{0}.root'.format(i))
