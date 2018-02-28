#!/bin/bash

#/hadoop/cms/store/user/rebassoo/

#python histos_mue.py latest ExclusiveWW SM_Madgraph
python histos_mue.py latest ExclusiveWW SM_FPMC
mv histos/ExclusiveWW.root histos/ExclusiveWW-FPMC.root
python histos_mue.py latest ExclusiveWW a0w5e-6
mv histos/ExclusiveWW.root histos/ExclusiveWW-a0w-5e-6.root
python histos_mue.py latest ExclusiveWW a0w5e-6-withXiCut
mv histos/ExclusiveWW.root histos/ExclusiveWW-a0w-5e-6-withXiCut.root

python histos_mue.py specific MuonEG crab_runBv3/171219_181133/0000
python histos_mue.py specific MuonEG crab_runBv3/171219_181133/0001
python histos_mue.py specific MuonEG crab_runC/171211_194321/0000
python histos_mue.py specific MuonEG crab_runG/171211_194414/0000

exit 1

#python histos_mue.py latest MuonEG crab_runBv3
#python histos_mue.py latest MuonEG crab_runC

python histos_mue.py latest MuonEG crab_runD
python histos_mue.py latest MuonEG crab_runE
python histos_mue.py latest MuonEG crab_runF
python histos_mue.py latest MuonEG crab_runG

python histos_mue.py latest MuonEG crab_runHv2
python histos_mue.py latest MuonEG crab_runHv3

python histos_mue.py latest DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 crab_DY-50-up
python histos_mue.py latest WWTo2L2Nu_13TeV-powheg crab_WWTo2L2Nu_13TeV-powheg
python histos_mue.py latest TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 crab_TTJets_DiLept_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
python histos_mue.py latest WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 crab_WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8


python histos_mue.py latest ZZ_TuneCUETP8M1_13TeV-pythia8 crab_ZZ_TuneCUETP8M1_13TeV-pythia8
python histos_mue.py latest WZ_TuneCUETP8M1_13TeV-pythia8 crab_WZ_TuneCUETP8M1_13TeV-pythia8
#python histos_mue.py latest ZZTo4L_13TeV_powheg_pythia8 crab_ZZTo4L_13TeV_powheg_pythia8
python histos_mue.py latest WpWpJJ_EWK-QCD_TuneCUETP8M1_13TeV-madgraph-pythia8 crab_WpWpJJ_EWK-QCD_TuneCUETP8M1_13TeV-madgraph-pythia8
python histos_mue.py latest WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8 crab_WGToLNuG_TuneCUETP8M1_13TeV-madgraphMLM-pythia8
python histos_mue.py latest ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8 crab_ZGTo2LG_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8
