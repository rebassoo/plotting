# plotting
All this code was developed a couple years ago so is currently using python2, have not yet updated it to python3. Assumes that you can run root in python

To run on the data ntuples to produce histograms for 2018 RunA Single Muon channel do the command:
python histos_quick.py local muon SingleMuon SlimmedNtuple_SingleMuon2018-RunA.root -nb
"histos_quick.py" is the script that will make all the histograms
"local" means that the ntuple is in the git directory. This is only the case for the Data RunA and RunB
"muon" is for the muon channel, "electron" for electron channel
"SingleMuon" is the data stream
"-nb" means that you are running the job interactivaly (not batch submission)

To see the commands to run the rest of the samples you can look here:
produceHistosSingleMu2018.txt
The commands in that text file assume that the ntuples are located in a path /hadoop/cms/store/user/rebassoo/
You will need to change this in htools.py L565 to whatever the path is for you for the ntuples

Once you make all the histograms then you can make stacked plots comparing data and MC:
python makeplots.py
You will need to change the line hdirectory in makeplots.py to whatever directory all the histograms files for the different data and MC samples are. You will also have to combine the data from different eras into one file (SingleMuonTotal.root for the muon channel, SingleElectronTotal.root for the electron channel).
