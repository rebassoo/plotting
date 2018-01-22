#!/bin/bash

#/hadoop/cms/store/user/rebassoo/


python histos_mumu.py latest DoubleMuon crab_runBv3
#Need to wait until get this job finished
python histos_mumu.py latest DoubleMuon crab_runC
python histos_mumu.py latest DoubleMuon crab_runG

python histos_mumu.py latest DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 crab_DY-50-up-mumu

#MC
#python histos_mue.py WWTo2L2Nu_13TeV-powheg crab_WWTo2L2Nu_13TeV-powheg/170428_214517/0000/
#/hadoop/cms/store/user/rebassoo/TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/170428_214534/0000/
#python histos_mue.py TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 crab_TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/170428_214534/0000/
#/hadoop/cms/store/user/rebassoo/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/crab_WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/170428_214552/0000
#python histos_mue.py WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 crab_WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/170428_214552/0000/
#/hadoop/cms/store/user/rebassoo/DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DY-10-50/170505_161702/0000
#python histos_mue.py DYJetsToLL_M-10to50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 crab_DY-10-50/170505_161702/0000
#/hadoop/cms/store/user/rebassoo/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/crab_DY-50-up/170505_161719/0000
#python histos_mue.py DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 crab_DY-50-up/170505_161719/0000

#Data
#python histos_mue.py MuonEG crab_runD/170627_231930/0000
#python histos_mue.py MuonEG crab_runG/170627_232652/0000

#python histos_mue.py MuonEG crab_runBv3/170428_221507/0000
#python histos_mue.py MuonEG crab_runBv3/170428_221507/0001
#python histos_mue.py MuonEG crab_runC/170428_221523/0000
#python histos_mue.py MuonEG crab_runD/170505_164117/0000
#python histos_mue.py MuonEG crab_runE/170428_221558/0000
#python histos_mue.py MuonEG crab_runF/170428_221615/0000

#python histos_mue.py MuonEG crab_runHv2/170428_221707/0000
#python histos_mue.py MuonEG crab_runHv3/170428_221723/0000