#!/bin/bash

#/hadoop/cms/store/user/rebassoo/

python histos_mue.py latest MuonEG crab_runBv3
python histos_mue.py latest MuonEG crab_runC
#python histos_mue.py latest MuonEG crab_runD
#python histos_mue.py latest MuonEG crab_runE
#python histos_mue.py latest MuonEG crab_runF
python histos_mue.py latest MuonEG crab_runG
#python histos_mue.py latest MuonEG crab_runHv2
#python histos_mue.py latest MuonEG crab_runHv3

python histos_mue.py latest DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 crab_DY-50-up
python histos_mue.py latest WWTo2L2Nu_13TeV-powheg crab_WWTo2L2Nu_13TeV-powheg
python histos_mue.py latest TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 crab_TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
python histos_mue.py latest WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 crab_WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8
python histos_mue.py latest ExclusiveWW SM_Madgraph