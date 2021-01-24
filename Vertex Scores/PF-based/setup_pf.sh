#!/bin/sh

useTiming=${1} # 3D or 4D

if [ $useTiming = "3D" ]
then
  echo Setting up workspace with track assignment not using timing
  echo Updating CMSSW_10_6_16/src/CommonTools/RecoAlgos/plugins/PrimaryVertexSorter.h
  cp 3D/PrimaryVertexSorter.h ../../../../plugins/
  echo Updating CMSSW_10_6_16/src/CommonTools/RecoAlgos/python/sortedPFPrimaryVertices_cfi.py
  cp 3D/sortedPFPrimaryVertices_cfi.py ../../../../python/
fi
if [ $useTiming = "4D" ]
then
  echo Setting up workspace with track assignment using timing
  echo Updating CMSSW_10_6_16/src/CommonTools/RecoAlgos/plugins/PrimaryVertexSorter.h
  cp 4D/PrimaryVertexSorter.h ../../../../plugins/
  echo Updating CMSSW_10_6_16/src/CommonTools/RecoAlgos/python/sortedPFPrimaryVertices_cfi.py
  cp 4D/sortedPFPrimaryVertices_cfi.py ../../../../python
fi

# copy the analysis scripts to the /test/ directory
echo Copying analysis script study_pv_sorting.py to CMSSW_10_6_16/src/CommonTools/RecoAlgos/test/
cp study_pf_sorting.py ../../../
cp pf_contents.py ../../../

# replace the pvSorting.py script
echo Adding new CMSSW_10_6_16/src/CommonTools/RecoAlgos/test/pvSorting.py script: pvSorting_pf.py
cp pvSorting_pf.py ../../../

# replace the PrimaryVertexSorter.cc script
echo Updating CMSSW_10_6_16/src/CommonTools/RecoAlgos/plugins/PrimaryVertexSorter.cc
rm ../../../../plugins/PrimaryVertexSorter.cc
cp PrimaryVertexSorter.cc ../../../../plugins/

# replace the PrimaryVertexSorting.cc script
echo Updating CMSSW_10_6_16/src/CommonTools/RecoAlgos/src/PrimaryVertexSorting.cc
rm ../../../../src/PrimaryVertexSorting.cc
cp PrimaryVertexSorting.cc ../../../../src/

# replace the PrimaryVertexSorting.h script
echo Updating CMSSW_10_6_16/src/CommonTools/RecoAlgos/interface/PrimaryVertexSorting.h
rm ../../../../interface/PrimaryVertexSorting.h
cp PrimaryVertexSorting.h ../../../../interface/

echo Recompiling the Primary Vertex Sorting scripts
cd ../../../../
scram b -j4
