# Track Vertex Scores -- Quick Start Instructions

The sorting algorithm defaults to using tracks as inputs, which allows for the rest of an analysis to benefit from a reconstruction based on the _improved_ sorted primary vertices. However, since tracks do not have an associated particle identification, the track-based scoring does not include a designated leptonic contribution.  
The track objects are stored in the AOD format with the handle: `Handle( "vector<reco::RecoChargedRefCandidate>" )`, and with the label, `event.getByLabel( "trackRefsForJets", handle )`. A separate script, `track_contents.py`, can be used to see information available in the AOD collection of tracks.  
Setup for the track-based sorting is as follows:

    cd /CMSSW_10_6_16/src/BTV_Vertex_Study/Vertex\ Scores/track-based/
    chmod u+rwx *
    ./setup_track.sh
    
## Running the sorting algorithm 
Before running the sorting algorithm, be sure to edit `/CommonTools/RecoAlgos/test/pvSorting.py` to specify which AOD file to run on in `process.source()` and the number of events (default = `5000`) should be stored in the resulting `.root` file.

    cd CMSSW_10_6_16/src/CommonTools/RecoAlgos/src/
    source /cvmfs/cms.cern.ch/cmsset_default.sh
    cmsenv
    voms-proxy-init --voms cms
    cd /CMSSW_10_6_16/src/CommonTools/RecoAlgos/test/
    cmsRun pvSorting.py
    
Running `pvSorting.py` will produce a data file `score_track_[# events].txt` containing `GEN` coordinates, `RECO` coordinates, and the vertex scores, and will produce a `ROOT` file, `AOD_track_[# events].root`, containing the new collection of `sortedPrimaryVertices`, along with other assignment/sorting related quantities, defined in the presentation.  Generally, output files made from the track-based algorithm will be tagged with 'track', and the PF-baesd with 'pf'. When switching between the track-based and PF-based algorithms, be sure to re-run the `setup_track.sh` script.
    
## Running `study_pv_sorting.py`
This script looks at the AOD_[# events].root file and compares the coordinate values of the objects `genParticles`, `offlinePrimaryVertices` and `sortedPrimaryVertices.  The results are saved to a pickled file, `AOD_PV_[# events].pkl`

    python study_pv_sorting.py -f AOD_[# events].root -v -s
    
The option `-n` can be used to specify how many events are to be stored in the `.pkl` file.
