#!/bin/bash


if [ $# != 1 ]; then
   echo usage: SubmittingToCondor.sh OUTPUTDIRECTORY
   exit 1
fi

PWD1=`echo $PWD` 
echo $PWD1

mkdir $1
cd $1
mkdir log
cp ../produceHistosSingleE2018.txt .
cp ../htools.py .
cp ../histos_quick.py .
cp ../makeBashScript.sh .
cp ../base.jdl .
sed -i "s|REPLACE|$PWD1|g" base.jdl

for i in {1..29}
do
    cat makeBashScript.sh >> "test_$i.sh"
    echo "tar xvzf inputfiles2018-e.tar.gz" >> "test_$i.sh" 
    output=`sed "${i}q;d" produceHistosSingleE2018.txt`
    echo "$output ${i}">> "test_$i.sh"
    echo "Executable = test_$i.sh" >> "test_$i.jdl"
    cat base.jdl >> "test_$i.jdl"
    condor_submit "test_$i.jdl"
done

