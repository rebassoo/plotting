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
SIGNAL_BIN="multiRP"
#SIGNAL_BIN="multiPixel"
#SIGNAL_BIN="pixel-pixel"
#cp ../produceHistosSingleMu-Xi.txt .
cp ../produceHistosSingleMu-dilepton.txt .
cp ../htools.py .
cp ../histos_quick.py .
#cp ../produceHistosSingleE.txt .
#cp ../produceHistosFew.txt .
cp ../makeBashScript.sh .
cp ../xiEventsRun*root .
cp ../base.jdl .
sed -i "s|REPLACE|$PWD1|g" base.jdl

#
for i in {6..16}
#for i in {1..59}
#for i in {1..5}
#for i in {1..16}
do
    cat makeBashScript.sh >> "test_$i.sh"
    output=`sed "${i}q;d" produceHistosSingleMu-dilepton.txt`
    #output=`sed "${i}q;d" produceHistosSingleMu-Xi.txt`
    #output=`sed "${i}q;d" produceHistosFew.txt`
    #echo "cp samples_info.json samples_info_$i.json" >> "test_$i.sh"
    #echo "transfer_output_files = samples_info_WW_TuneCP5_13TeV-pythia8.json" >> "test_$i.jdl"
    
    if grep -q "W2JetsToLNu" <<< "$output";
    then
	for a in {1..7}
	do 
	    #echo "I get here"
	    #ls
	    i_plus_a=$((a+i))
	    cp "test_$i.sh" "test_${i}_${a}.sh"
	    echo "$output $SIGNAL_BIN ${i} ${a}" >> "test_${i}_${a}.sh"
	    echo "Executable = test_${i}_${a}.sh" >> "test_${i}_${a}.jdl"
	    cat base.jdl >> "test_${i}_${a}.jdl"
	    #ls
	    condor_submit "test_${i}_${a}.jdl"	

	done
	rm "test_$i.sh"
    else
	echo "$output $SIGNAL_BIN ${i}">> "test_$i.sh"
	echo "Executable = test_$i.sh" >> "test_$i.jdl"
	cat base.jdl >> "test_$i.jdl"
	condor_submit "test_$i.jdl"	
    fi


done

