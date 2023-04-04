# Histogram and 2D KS p-value plots for various b-tag analyzer inputs

## Instructions
1. Run the [b-tag analyzer ntuplizer](https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements) with the following options/modifications (lxpus recommended):
* For EOY, use branch `CMSSW_9_4_X`, and for UL, use branch `CMSSW_12_2_X`
* Create a new [default](https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements/tree/9_4_X/python/defaults) configuration for 2016/2017/2018 with the corresponding miniAOD sample you would like to run
* Create a new [variable group](https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements/blob/9_4_X/python/varGroups_cfi.py) with all relevant inputs desired (i.e. TagVarCSV_\*, PV_\*, SV_\*, GenPVz)
2. Upload the output ntuple `ROOT` file to [SWAN](swan.cern.ch) and run the two notebooks
