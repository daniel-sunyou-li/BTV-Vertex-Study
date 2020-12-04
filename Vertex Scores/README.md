Study the performance of the vertex sorting algorithm that operates on AOD files.  The scripts in this directory are to be run on `CMSSW_10_6_16`.  Setup can be run on LXPLUS:

    source /cvmfs/cms.cern.ch/cmsset_default.sh
    cmsenv
    cmsrel CMSSW_10_6_16
    cd CMSSW_10_6_16/src/
    git cms-addpkg CommonTools/RecoAlgos
    cd CommonTools/RecoAlgos/test/
    git clone https://github.com/daniel-sunyou-li/BTV-Vertex-Study.git 
