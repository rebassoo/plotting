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
#cp ../produceHistosSingleMu-Xi.txt .
cp ../produceHistosSingleMu2018.txt .
cp ../htools.py .
cp ../histos_quick.py .
#cp ../produceHistosSingleE.txt .
#cp ../produceHistosFew.txt .
cp ../makeBashScript.sh .
#cp ../inputfiles/xiEventsRun*root .
cp ../base.jdl .
#cp ../Electron*root .
#cp ../samples_info.json .
sed -i "s|REPLACE|$PWD1|g" base.jdl

#
#for i in {5..20}
#for i in {21..24}
for i in {1..29}
#for i in {1..20}
#for i in {7..7}
#for i in {1..59}
#for i in {1..4}
#for i in {1..16}
do
    cat makeBashScript.sh >> "test_$i.sh"
    echo "tar xvzf inputfiles2018-mu.tar.gz" >> "test_$i.sh"
    output=`sed "${i}q;d" produceHistosSingleMu2018.txt`
    
    if grep -q "W2JetsToLNu" <<< "$output";
    then
	for a in {1..7}
	do 
	    #echo "I get here"
	    #ls
	    i_plus_a=$((a+i))
	    cp "test_$i.sh" "test_${i}_${a}.sh"
	    echo "$output ${i} ${a}" >> "test_${i}_${a}.sh"
	    echo "Executable = test_${i}_${a}.sh" >> "test_${i}_${a}.jdl"
	    cat base.jdl >> "test_${i}_${a}.jdl"
	    #ls
	    condor_submit "test_${i}_${a}.jdl"	

	done
	rm "test_$i.sh"
    else
	echo "$output ${i}">> "test_$i.sh"
	echo "Executable = test_$i.sh" >> "test_$i.jdl"
	cat base.jdl >> "test_$i.jdl"
	condor_submit "test_$i.jdl"	
    fi


done

