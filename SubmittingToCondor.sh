#!/bin/bash


if [ $# != 1 ]; then
   echo usage: SubmittingToCondor.sh OUTPUTDIRECTORY
   exit 1
fi

PWD1=`echo $PWD` 
echo $PWD1

mkdir $1
#mkdir /hadoop/cms/store/user/rebassoo/2018_02_20_FPMC-Reco/$1
cd $1
mkdir log
#SIGNAL_BIN="multiRP"
SIGNAL_BIN="multiPixel"
#SIGNAL_BIN="pixel-pixel"
#cp ../produceHistosSingleMu-Xi.txt .
cp ../produceHistosSingleMu.txt .
cp ../htools.py .
cp ../histos_quick.py .
#cp ../produceHistosSingleE.txt .
#cp ../produceHistosFew.txt .
cp ../makeBashScript.sh .
cp ../base.jdl .
sed -i "s|REPLACE|$PWD1|g" base.jdl

#for i in {0..1}
for i in {1..54}
#for i in {6..11}
#for i in {48..48}
#for i in {1..3}
#for i in {1..11}
#for i in {1..5}
#for i in {1..1}
#for i in {1..49}
do
    cat makeBashScript.sh >> "test_$i.sh"
    output=`sed "${i}q;d" produceHistosSingleMu.txt`
    #output=`sed "${i}q;d" produceHistosSingleMu-Xi.txt`
    #output=`sed "${i}q;d" produceHistosFew.txt`
    echo "$output $SIGNAL_BIN" >> "test_$i.sh"
    #echo "cp samples_info.json samples_info_$i.json" >> "test_$i.sh"
    #echo "transfer_output_files = samples_info_WW_TuneCP5_13TeV-pythia8.json" >> "test_$i.jdl"
    echo "Executable = test_$i.sh" >> "test_$i.jdl"
    cat base.jdl >> "test_$i.jdl"

    condor_submit "test_$i.jdl"
done

