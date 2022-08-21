common = {
  "groups": [
    "custom", # add this to varGroups_cfi.py
    "EventInfo", "PV",
    "JetInfo", "JetSV",
    "CSVTagVar", "CSVTagTrackVar"
  ],
  "eras": [ "Run3" ],
  "miniAOD": True,
  "usePuppi":False,
  "usePuppiForFatJets": True,
  "usePuppiForBTagging": False,
  "mcGlobalTag": "120X_mcRun3_2021_realistic_v4",
  "remakeAllDiscr": True,
  "maxJetEta": 2.5,
  "usePrivateJEC": False,
  "inputFiles": [ "/store/mc/Run3Winter22MiniAOD/TTToSemiLeptonic_TuneCP5_13p6TeV-powheg-pythia8/MINIAODSIM/FlatPU0to70_122X_mcRun3_2021_realistic_v9-v2/60000/043bce28-0eb0-4977-8279-6c1a86de4cda.root" ],
  "outFilename": [ "TTToSemiLeptonic_FlatPU0to70_Run3.root" ],
  #"inputFiles": [ "/store/mc/Run3Winter22MiniAOD/TTToSemiLeptonic_TuneCP5_13p6TeV-powheg-pythia8/MINIAODSIM/PUForMUOVal_122X_mcRun3_2021_realistic_v9-v2/2830000/08d1bfef-c1d8-49a5-88b2-3d117a461fa7.root" ],
  #"outFilename": [ "TTToSemiLeptonic_PUForMUOVal_Run3.root" ]
}
