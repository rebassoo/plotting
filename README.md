# plotting
#This directory has scripts that will run on the data/MC ntuples to make histogram files for each data/MC sample. 
#Then a script is used to take these histogram files and make data vs. MC plots and signal predictions
#Some of these scripts have commands that are specific to the T2_UCSD site
#Analysis steps
#1) Submit to run batch jobs for all data/MC to make histogram files
#   a) The scripts SubmittingToCondor*sh do this. An example of this is "./SubmittingToCondorE.sh 2021-01-24-Output", 
#      where 2021-01-24-Output is the output directory all the histograms will be made in
#   b) The Submit*sh scripts call the files produceHistosSingle*-dilepton.txt, which in them have the commands to run on each sample
#   c) An example of running on a particular sample is: python histos_quick.py latest muon SingleMuon crab_Run2017F-withDilepton -b
#       histos_quick.py is what has the code to run over the ntuples, make cuts, and output the histograms to a root file
#2) After all jobs are done there is some postprocessing that needs to be done
#   a) This combines all the data files from different eras, and combines all the information on number of events, etc. into a single json file
#   b) To run this on the do: "python postprocess.py 2019-11-08-Electron electron", where electron denotes electron channel
#      or if you are running on the W+jets pt samples "python postprocessManyWJets.py 2019-11-08-Electron electron"
#3) Once the postprocessing is done then you can make nice plots
#   a) For data vs. MC use the script makeplots.py, this will also make a ratio plot. Can specify to make several plots at the same time or one at a time
#   b) For signal prediction plots use makeSignalRegionPlotGeneral.py
