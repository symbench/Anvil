#!/bin/bash

echo "******************************************"
echo "**     DEXTER-OPENFOAM INTERFACE        **"
echo "**  Stevens Institute of Technology     **"
echo "**  No warranties: use at your own risk **"
echo "******************************************"

echo "USAGE: run_one_aoa.sh dexfile stlfile aoa "
echo $1
echo $2 
echo $3


if [ -z "$1" ]
  then
    echo "No dex file is not supplied"
    exit 1
fi

if [[ $1 != *.dex ]]
    then
        echo "First Argument must be a .dex file"
        exit 2
    fi
if [ -z "$2" ]
  then
    echo " STL file is required "
    exit 2
fi

if [[ $2 != *.stl ]]
    then
        echo "Second argument must be a .stl file"
        exit 2
    fi

if [ -z "$3" ]
  then
    echo " AOA is required "
    exit 2
fi


echo "Running openfoam in Docker "

docker run --rm -v ${PWD}:/home/aimed_user/dexof_work kishorestevens/dexof /home/aimed_user/dex_of/run_one_aoa.sh $1 $2 $3

echo "*** ALL DONE -- ALL DONE ***"
