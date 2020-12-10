# Vertex Scores -- Quick Start Instructions

Study the performance of the vertex sorting algorithm that operates on AOD files. The Github update can be found [here](https://github.com/cms-sw/cmssw/pull/7285/commits/539197c593270b7515a8b07c1891e3bfcd9fc89c#diff-184be42e35fb4bb9419eaba0e7f290f5). The scripts in this directory are to be run on `CMSSW_10_6_16`.  Setup can be run on LXPLUS:

    source /cvmfs/cms.cern.ch/cmsset_default.sh
    cmsenv
    cmsrel CMSSW_10_6_16
    cd CMSSW_10_6_16/src/
    cmsenv
    git cms-addpkg CommonTools/RecoAlgos
    cd CommonTools/RecoAlgos/test/
    git clone https://github.com/daniel-sunyou-li/BTV_Vertex_Study.git 
    cd BTV-Vertex-Study/Vertex\ Scores/
    chmod u+rwx *
    ./setup.sh
    
## Running the sorting algorithm `pvSorting.py`
First, replace the sorting algorithm code `/CommonTools/RecoAlgos/src/PrimaryVertexSorting.cc` with the updated version in `/BTV-Vertex-Study/Vertex Scores/`:

    cd CMSSW_10_6_16/src/CommonTools/RecoAlgos/src/
    rm PrimaryVertexSorting.cc
    cd ../test/BTV-Vertex-Study/Vertex\ Scores/
    cp PrimaryVertexSorting.cc ../../../src/
    
Next, replace the `python` configuration script `/CommonTools/RecoAlgos/test/pvSorting.py` with the updated version in `/BTV-Vertex-Study/Vertex Scores/`.  Before moving, edit `/BTV-Vertex-Study/Vertex Scores/pvSorting.py` to edit the desired number of `events` (default = `5000`) and the desired file for `process.source`.

    cd CMSSW_10_6_16/src/CommonTools/RecoAlgos/test/
    rm pvSorting.py
    cd BTV-Vertex-Study/Vertex\ Scores/
    cp pvSorting.py ../../
    
The updated sorting `.cc` files need to be recompiled:

    cd CMSSW_10_6_16/src/CommonTools/RecoAlgos/src/
    scram b -j4

The sorting algorithm can be run using:

    cmsRun pvSorting.root
    
resulting in the production of `ROOT` file `AOD_[# events].root` containing the newly sorted vertices.  The scores for the jet, MET and lepton contributions as well as the vertex coordinates are stored in a separate `.txt` file `/test/sort_score.txt`.  
    
## Running `study_pv_sorting.py`
This script looks at the AOD_[# events].root file and  compares the coordinate values of the objects `genParticles`, `offlinePrimaryVertices` and `sortedPrimaryVertices.  The results are saved to a pickled file, `AOD_PV_[# events].pkl`

    python study_pv_sorting.py -f AOD_[# events].root -v -s
    
The option `-n` can be used to specify how many events are to be stored in the `.pkl` file.
