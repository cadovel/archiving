#!/bin/bash

set -e 

if [ ! -e $SDRROOT/dom/components/rh/FileWriter ]; then
  echo "rh.FileWriter must be installed"
  exit 1
fi

if [ ! -e $SDRROOT/dom/components/rh/FileReader ]; then
  echo "rh.FileReader must be installed"
  exit 1
fi

if [ ! -e $SDRROOT/dom/components/rh/TuneFilterDecimate ]; then
  echo "rh.TuneFilterDecimate must be installed"
  exit 1
fi

pushd control_writes/python
./reconf
./configure
make install -j
popd

pushd splitter/cpp
./reconf
./configure
make install -j
popd

pushd rfdatagen/cpp
./reconf
./configure
make install -j
popd

mkdir -p $SDRROOT/dom/waveforms/archiver
cp -f archiver/archiver.sad.xml $SDRROOT/dom/waveforms/archiver/

mkdir -p $SDRROOT/dom/waveforms/sample_write
cp -f sample_write/sample_write.sad.xml $SDRROOT/dom/waveforms/sample_write/
