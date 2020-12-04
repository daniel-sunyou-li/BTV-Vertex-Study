import FWCore.ParameterSet.Config as cms
process = cms.Process("PV")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring( 
  "root://xrootd-cms.infn.it//store/relval/CMSSW_10_6_11_CANDIDATE/RelValTTbarLepton_13UP16/AODSIM/PU25ns_106X_mcRun2_asymptotic_v12_hlt16post-v1/10000/0D7466F6-988D-BE4B-A994-9F0A11B7402F.root" 
  ) )
  
events = 5000

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(events) )
process.load("Configuration.EventContent.EventContent_cff")
process.out = cms.OutputModule(
    "PoolOutputModule",
    process.AODSIMEventContent,
    fileName = cms.untracked.string('AOD_{}.root'.format(events)),
    )
process.out.outputCommands.extend(
    [
      'keep *'
    ])
process.load("CommonTools.RecoAlgos.sortedPrimaryVertices_cfi")
process.load("CommonTools.RecoAlgos.sortedPFPrimaryVertices_cfi")

process.sortedPrimaryVertices.jets = "ak4CaloJets"

from CommonTools.RecoAlgos.TrackWithVertexRefSelector_cfi import *
from RecoJets.JetProducers.TracksForJets_cff import *
from CommonTools.RecoAlgos.sortedPrimaryVertices_cfi import *
from RecoJets.JetProducers.caloJetsForTrk_cff import *

process.trackWithVertexRefSelectorBeforeSorting = trackWithVertexRefSelector.clone(vertexTag="offlinePrimaryVertices")
process.trackWithVertexRefSelectorBeforeSorting.ptMax=9e99
process.trackWithVertexRefSelectorBeforeSorting.ptErrorCut=9e99
process.trackRefsForJetsBeforeSorting = trackRefsForJets.clone(src="trackWithVertexRefSelectorBeforeSorting")
process.sortedPrimaryVertices.particles="trackRefsForJetsBeforeSorting"

process.p = cms.Path(process.trackWithVertexRefSelectorBeforeSorting+process.trackRefsForJetsBeforeSorting+process.sortedPrimaryVertices)

process.endpath = cms.EndPath( process.out )
