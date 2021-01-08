# Particle Flow Candidate Vertex Scoring -- Quick Instructions

The sorting algorithm defaults to using tracks as the inputs, however, Particle Flow candidates can also be used to compute a scoring.  Because the scores are computed after an initial reconstruction (which produced the PF candidates, to begin with), additional steps would have to be made to re-do reconstruction using the new primary vertex order. However, by using PF candidates as the inputs, the particle identity (`pdgId`) can be used to incorporate a separate scoring for leptonic (electron, muon) contributions. 

The Particle Flow candidates are stored in AOD with the handle: `Handle( "vector<reco::PFCandidate>" )`, and the label: `event.getByLabel( "particleFlow", handle )`. A separate script, `pf_contents.py`, can be used to see information available in the AOD collection of PF candidates.

Setup for the PF-based sorting is as follows:

    cd /CMSSW_10_6_16/src/BTV_Vertex_Study/Vertex\ Scores/PF-based/
    chmod u+rwx *
    ./setup_pf.sh
    
## Running the sorting algorithm
Before running the sorting algorithm, be sure to edit `/CommonTools/RecoAlgos/test/pvSorting.py` to specify which AOD file to run on in `process.source()` and the number of events (default = `5000`) should be stored in the resulting `.root` file.  

    cd /CMSSW_10_6_16/src/
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    cmsenv
    voms-proxy-init --voms cms
    cd /CMSSW_10_6_16/src/CommonTools/RecoAlgos/test/
    cmsRun pvSorting.py
    
Output files made from the PF candidate-based algorithm will be tagged with 'pf', and the track-based with 'track'.
