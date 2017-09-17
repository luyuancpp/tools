#!/bin/bash


c_dir=$(pwd)

set -e
mkdir -p ../build

function build()
{
    for d in $1/*;
    do
        if test -d "$d";then
            ./make.sh -proj-dir=$d -build=../../build/$(basename $d) --vs-file=$(basename $d).vcxproj -tomakefile-dir=$(pwd) -tomakefile-name=vcxproj2mk.sh ; 
        fi
    done
}

build . 

set -ex

exit 0
