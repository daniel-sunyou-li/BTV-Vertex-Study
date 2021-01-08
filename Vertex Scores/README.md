# Vertex Scores -- Quick Start Instructions

Study the performance of the vertex sorting algorithm that operates on AOD files. The Github update can be found [here](https://github.com/cms-sw/cmssw/pull/7285/commits/539197c593270b7515a8b07c1891e3bfcd9fc89c#diff-184be42e35fb4bb9419eaba0e7f290f5). A presentation explaining the motivation behind the scoring algorithm can be found [here](https://indico.cern.ch/event/369417/contributions/1788757/attachments/734933/1008272/pv-sorting-xpog.pdf). The scripts in this directory are to be run on `CMSSW_10_6_16`. The sorting algorithm operates on either tracks or PF candidates.  Refer to the `README.md` instructions in the respective subdirectories 'track-based' and 'PF-based'.  Setup can be run on LXPLUS:

    source /cvmfs/cms.cern.ch/cmsset_default.sh
    cmsenv
    cmsrel CMSSW_10_6_16
    cd CMSSW_10_6_16/src/
    cmsenv
    git cms-addpkg CommonTools/RecoAlgos
    cd CommonTools/RecoAlgos/test/
    git clone https://github.com/daniel-sunyou-li/BTV_Vertex_Study.git 
    cd BTV_Vertex_Study/Vertex\ Scores/
    chmod u+rwx *

Be sure to recompile the `C++` files using `scram b` after making any edits.
