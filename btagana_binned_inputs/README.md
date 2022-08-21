# Histogram and 2D KS p-value plots for various b-tag analyzer inputs

## Instructions
1. Run the [b-tag analyzer ntuplizer](https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements) with the following options/modifications (lxpus recommended):
* Run on `CMSSW_12_2_3_patch1`:

      cmsrel CMSSW_12_2_3_patch1
      cd CMSSW_12_2_3_patch1/src
      cmsenv

      export CMSSW_GIT_REFERENCE=/cvmfs/cms.cern.ch/cmssw.git.daily

      git cms-init
      
      git clone -b 12_2_X --recursive https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements.git RecoBTag/PerformanceMeasurements
      
      scram b -j 12

* Create a new [default](https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements/tree/9_4_X/python/defaults) configuration for Run3 with the corresponding miniAOD sample you would like to run
* Create a new [variable group](https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements/blob/9_4_X/python/varGroups_cfi.py) in varGroups_cfi.py:

      cms.PSet(
        group       = cms.string( "custom" ),
        store       = cms.bool(True),
        description = cms.string( "Variables for studying PV reconstruction" ),
        variables   = cms.vstring(
          "nTrkTagVarCSV",
          "GenPVz",
          "Jet_DeepFlavourB", "Jet_DeepFlavourBB", "Jet_DeepFlavourLEPB",
          "Jet_DeepCSVb", "Jet_DeepCSVbb"
        )
      )

2. Run with the options:

        voms-proxy-init --voms cms
        cmsRun runBTagAnalyzer_cfg.py runOnData=False defaults=Run3 runEventInfo=True

4. Upload the output ntuple `ROOT` file to [SWAN](swan.cern.ch) and run the three notebooks (as needed)
* Methods are defined in `.py` files
