#!/bin/bash

#/hadoop/cms/store/user/rebassoo/

#python histos_quick.py latest muon GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6 crab_GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6-signal-proton-propagation

#python histos_quick.py latest muon ExclusiveWW a0w1e-6-SingleLepton-2017
#cp histos_muon/ExclusiveWW.root histos_muon/ExclusiveWW_a0w1e-6-SingleLepton-2017.root

python histos_quick.py latest muon SingleMuon crab_Run2017B -nb
python histos_quick.py latest muon SingleMuon crab_Run2017C -nb
python histos_quick.py latest muon SingleMuon crab_Run2017D -nb
python histos_quick.py latest muon SingleMuon crab_Run2017E -nb
python histos_quick.py latest muon SingleMuon crab_Run2017F -nb

python histos_quick.py latest muon GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6 crab_GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6-signal-proton-propagation -nb
#python histos_quick.py latest muon GGToWW_bSM-A0W5e-6_13TeV-fpmc-herwig6 crab_GGToWW_bSM-A0W5e-6_13TeV-fpmc-herwig6-signal-proton-propagation -nb
python histos_quick.py latest muon GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6 crab_GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6-signal-proton-propagation -nb
#python histos_quick.py latest muon GGToWWTo3L3Nu_PtL-20_13TeV-fpmc-herwig6 crab_GGToWWTo3L3Nu_PtL-20_13TeV-fpmc-herwig6-signal-proton-propagation -nb
python histos_quick.py latest muon GGToWWToJJENu_PtL-15_13TeV-fpmc-herwig6 crab_GGToWWToJJENu_PtL-15_13TeV-fpmc-herwig6-signal-proton-propagation -nb
python histos_quick.py latest muon GGToWWToJJMuNu_PtL-15_13TeV-fpmc-herwig6 crab_GGToWWToJJMuNu_PtL-15_13TeV-fpmc-herwig6-signal-proton-propagation -nb


exit 1

python histos_quick.py latest muon GGToWWToJJENu_PtL-15_13TeV-fpmc-herwig6 crab_GGToWWToJJENu_PtL-15_13TeV-fpmc-herwig6-signal-proton-propagation
python histos_quick.py latest muon GGToWWToJJMuNu_PtL-15_13TeV-fpmc-herwig6 crab_GGToWWToJJMuNu_PtL-15_13TeV-fpmc-herwig6-signal-proton-propagation



python histos_quick.py latest muon SingleMuon crab_Run2017B
python histos_quick.py latest muon SingleMuon crab_Run2017C
python histos_quick.py latest muon SingleMuon crab_Run2017D
python histos_quick.py latest muon SingleMuon crab_Run2017E
python histos_quick.py latest muon SingleMuon crab_Run2017F

python histos_quick.py latest muon GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6 crab_GGToWW_bSM-A0W1e-6_13TeV-fpmc-herwig6-signal-proton-propagation
python histos_quick.py latest muon GGToWW_bSM-A0W5e-6_13TeV-fpmc-herwig6 crab_GGToWW_bSM-A0W5e-6_13TeV-fpmc-herwig6-signal-proton-propagation
python histos_quick.py latest muon GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6 crab_GGToWW_bSM-A0W2e-6_13TeV-fpmc-herwig6-signal-proton-propagation
python histos_quick.py latest muon GGToWWTo3L3Nu_PtL-20_13TeV-fpmc-herwig6 crab_GGToWWTo3L3Nu_PtL-20_13TeV-fpmc-herwig6-signal-proton-propagation

python histos_quick.py latest muon WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8 crab_WJets-0jets_JEC-proton-propagation
python histos_quick.py latest muon WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8 crab_WJets-1jets_JEC-proton-propagation
python histos_quick.py latest muon WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8 crab_WJets-2jets_JEC-proton-propagation

python histos_quick.py latest muon DYJetsToLL_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8 crab_DYJetsToLL_0J_JEC-proton-propagation
python histos_quick.py latest muon DYJetsToLL_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8 crab_DYJetsToLL_1J_JEC-proton-propagation
python histos_quick.py latest muon DYJetsToLL_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8 crab_DYJetsToLL_2J_JEC-proton-propagation

python histos_quick.py latest muon TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8 crab_TTToSemiLeptonic_JEC-proton-propagation
python histos_quick.py latest muon TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8 crab_TTbar-Inclusive_JEC-proton-propagation-test
python histos_quick.py latest muon WW_TuneCP5_13TeV-pythia8 crab_WW_JEC-proton-propagation
python histos_quick.py latest muon WZ_TuneCP5_13TeV-pythia8 crab_WZ_JEC-proton-propagation
python histos_quick.py latest muon ZZ_TuneCP5_13TeV-pythia8 crab_ZZ_JEC-proton-propagation

python histos_quick.py latest muon ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-amcatnlo-pythia8 crab_ST_s-channel_JEC-proton-propagation
python histos_quick.py latest muon ST_t-channel_top_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8 crab_ST_t-channel_top_JEC-proton-propagation
python histos_quick.py latest muon ST_t-channel_antitop_4f_inclusiveDecays_TuneCP5_13TeV-powhegV2-madspin-pythia8 crab_ST_t-channel_antitop_JEC-proton-propagation
python histos_quick.py latest muon ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8 crab_ST_tW_top_5f_JEC-proton-propagation
python histos_quick.py latest muon ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8 crab_ST_tW_antitop_5f_JEC-proton-propagation

python histos_quick.py latest muon QCD_Pt_170to300_TuneCP5_13TeV_pythia8 crab_QCD_Pt_170to300_JEC-proton-propagation
python histos_quick.py latest muon QCD_Pt_300to470_TuneCP5_13TeV_pythia8 crab_QCD_Pt_300to470_JEC-proton-propagation
python histos_quick.py latest muon QCD_Pt_470to600_TuneCP5_13TeV_pythia8 crab_QCD_Pt_470to600_JEC-proton-propagation
python histos_quick.py latest muon QCD_Pt_600to800_TuneCP5_13TeV_pythia8 crab_QCD_Pt_600to800_JEC-proton-propagation
python histos_quick.py latest muon QCD_Pt_800to1000_TuneCP5_13TeV_pythia8 crab_QCD_Pt_800to1000_JEC-proton-propagation
python histos_quick.py latest muon QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8 crab_QCD_Pt_1000to1400_JEC-proton-propagation
python histos_quick.py latest muon QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8 crab_QCD_Pt_1400to1800_JEC-proton-propagation
python histos_quick.py latest muon QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8 crab_QCD_Pt_1800to2400_JEC-proton-propagation
python histos_quick.py latest muon QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8 crab_QCD_Pt_2400to3200_JEC-proton-propagation
python histos_quick.py latest muon QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8 crab_QCD_Pt_3200toInf_JEC-proton-propagation

python histos_quick.py latest muon DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8 crab_DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX_JEC-proton-propagation

exit 1

#python histos_quick.py latest muon W1JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W1JetsToLNu_LHEWpT_100-150_ext1_JEC-proton-propagation
#python histos_quick.py latest muon W1JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W1JetsToLNu_LHEWpT_150-250_ext1_JEC-proton-propagation
#python histos_quick.py latest muon W1JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W1JetsToLNu_LHEWpT_250-400_ext1_JEC-proton-propagation
#python histos_quick.py latest muon W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W1JetsToLNu_LHEWpT_400-inf_ext1_JEC-proton-propagation

#python histos_quick.py latest muon W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W2JetsToLNu_LHEWpT_100-150_ext1_JEC-proton-propagation
#python histos_quick.py latest muon W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W2JetsToLNu_LHEWpT_100-150_ext1_JEC-proton-propagation
#python histos_quick.py latest muon W2JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W2JetsToLNu_LHEWpT_250-400_ext1_JEC-proton-propagation
#python histos_quick.py latest muon W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W2JetsToLNu_LHEWpT_400-inf_ext1_JEC-proton-propagation

python histos_quick.py latest muon W1JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W1JetsToLNu_LHEWpT_100-150_JEC-proton-propagation
python histos_quick.py latest muon W1JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W1JetsToLNu_LHEWpT_150-250_JEC-proton-propagation
python histos_quick.py latest muon W1JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W1JetsToLNu_LHEWpT_250-400_JEC-proton-propagation
python histos_quick.py latest muon W1JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W1JetsToLNu_LHEWpT_400-inf_JEC-proton-propagation

python histos_quick.py latest muon W2JetsToLNu_LHEWpT_100-150_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W2JetsToLNu_LHEWpT_100-150_JEC-proton-propagation
python histos_quick.py latest muon W2JetsToLNu_LHEWpT_150-250_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W2JetsToLNu_LHEWpT_150-250_JEC-proton-propagation
python histos_quick.py latest muon W2JetsToLNu_LHEWpT_250-400_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W2JetsToLNu_LHEWpT_250-400_JEC-proton-propagation
python histos_quick.py latest muon W2JetsToLNu_LHEWpT_400-inf_TuneCP5_13TeV-amcnloFXFX-pythia8 crab_W2JetsToLNu_LHEWpT_400-inf_JEC-proton-propagation

exit 1



python histos_quick.py latest muon ExclusiveWW a0w1e-6-SingleLepton-2017
cp histos_muon/ExclusiveWW.root histos/ExclusiveWW_a0w1e-6-SingleLepton-2017.root

python histos_quick.py latest muon ExclusiveWW SM_FPMC-SingleLepton-2017
cp histos_muon/ExclusiveWW.root histos/ExclusiveWW_SM_FPMC-SingleLepton-2017.root

python histos_quick.py latest muon ExclusiveWW a0w2p5e-6-SingleLepton-2017
cp histos_muon/ExclusiveWW.root histos/ExclusiveWW_a0w2p5e-6-SingleLepton-2017.root