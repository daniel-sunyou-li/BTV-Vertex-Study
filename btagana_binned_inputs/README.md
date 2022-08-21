# Histogram and 2D KS p-value plots for various b-tag analyzer inputs

## Instructions
1. Run the [b-tag analyzer ntuplizer](https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements) with the following options/modifications (lxpus recommended):
* Run on `CMSSW_12_2_3_patch1`
* Create a new [default](https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements/tree/9_4_X/python/defaults) configuration for 2016/2017/2018 with the corresponding miniAOD sample you would like to run
* Create a new [variable group](https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements/blob/9_4_X/python/varGroups_cfi.py) with all relevant inputs desired (i.e. TagVarCSV_\*, PV_\*, SV_\*, GenPVz)
### `custom` variable group in `varGroups_cfi.py`:

    cms.PSet(
      group       = cms.string( "custom" ),
      store       = cms.bool(True),
      description = cms.string( "Variables for studying PV reconstruction" ),
      variables   = cms.vstring(
        "nTrkTagVarCSV",
        "nPV", "PV_x", "PV_y", "PV_z", "PV_chi2",
        "GenPVz",
        "nJet",
        "Jet_eta",
        "Jet_pt",
        "Jet_DeepFlavourB", "Jet_DeepFlavourBB", "Jet_DeepFlavourLEPB",
        "Jet_DeepCSVb", "Jet_DeepCSVbb"
      )
    )

2. Run with the options:
* `runOnData=False`
* `defaults=2017_UltraLegacy`
* `runEventInfo=True`
3. Upload the output ntuple `ROOT` file to [SWAN](swan.cern.ch) and run the three notebooks (as needed)
* Methods are defined in `.py` files
