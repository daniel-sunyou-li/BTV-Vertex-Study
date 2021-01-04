from DataFormats.FWLite import Handle, Events
from argparse import ArgumentParser
import pickle

parser = ArgumentParser()
parser.add_argument("-n", "--numEvents", default="-1", help="the number of events to store")
parser.add_argument("-v", "--verbose", action="store_true", help="Display vertex information per event")
parser.add_argument("-s", "--save", action="store_true", help="Save the vertexing information as a .npy file")

args = parser.parse_args()

VERBOSE = args.verbose
EVENTS  = int(args.numEvents)
SAVE    = args.save

events = Events("root://xrootd-cms.infn.it//store/mc/PhaseIITDRSpring19MiniAOD/TT_TuneCP5_14TeV-powheg-pythia8/MINIAODSIM/PU200_106X_upgrade2023_realistic_v3-v1/20000/07802317-3808-D14D-94DD-66C7340D821E.root")

# To add simulated PV, rely on the BTagAnalyzer implementation
# https://github.com/cms-btv-pog/RecoBTag-PerformanceMeasurements/blob/d495d00ef3839333a4f2423f89b51a00a5eaab46/plugins/BTagAnalyzer.cc#L956-L963
genParticles = Handle("vector<reco::GenParticle>")

# http://cmsdoxygen.web.cern.ch/cmsdoxygen/CMSSW_10_6_0/doc/html/da/d95/classreco_1_1Vertex.html
pv_3D = Handle("vector<reco::Vertex>")
pv_4D = Handle("vector<reco::Vertex>")
#tracks = Handle("std::vector<reco::Track>")

z_hard = {}
pv_3D_data = {}
pv_4D_data = {}

i = 0

#print(dir(events))
events.toBegin()

print("Event # / # Hard Process / # 3D Vertex / # 4D Vertex")

for event in events:

    # Simulated Vertices
    # event.getByLabel("generalTracks", tracks)
    event.getByLabel("prunedGenParticles", genParticles)
    z_hard[i] = {
      "vx": [],
      "vy": [],
      "vz": [],
      "ID": []
    }
    for genparticle in genParticles.product():
        if genparticle.isHardProcess():
             z_hard[i]["vx"].append(genparticle.vx())
             z_hard[i]["vy"].append(genparticle.vy())
             z_hard[i]["vz"].append(genparticle.vz())
             z_hard[i]["ID"].append(genparticle.pdgId())

    # Reconstructed Vertices

    event.getByLabel("offlineSlimmedPrimaryVertices4D", pv_4D)

    pv_4D_data[i] = {}
    for j, vertex in enumerate(pv_4D.product()):
        pv_4D_data[i][j] = {
            "4D x": vertex.x(),
            "4D y": vertex.y(),
            "4D z": vertex.z()
        }
        #print(vertex.pz())
        #print(dir(vertex))
        break

    event.getByLabel("offlineSlimmedPrimaryVertices", pv_3D)

    pv_3D_data[i] = {}
    for j, vertex in enumerate(pv_3D.product()):
        pv_3D_data[i][j] = {
            "3D x": vertex.x(),
            "3D y": vertex.y(),
            "3D z": vertex.z(),
            "3D chi2": vertex.chi2(),
            "3D Ntracks": vertex.nTracks()
        }
        print(vertex.p4().Px(), vertex.p4().Py(), vertex.p4().Pz(), vertex.p4().Pt())
        #print(dir(vertex))
        #print(dir(vertex.p4()))
        break
    nHard = len(z_hard[i]["vz"])
    nVertex_4D = max(list(pv_4D_data[i].keys()))
    nVertex_3D = max(list(pv_3D_data[i].keys()))
    if VERBOSE:
        print("{:<8}  {:<15}  {:<12}  {:<12}".format(
            i, nHard, nVertex_3D, nVertex_4D
        ))
    i+=1
    if i == EVENTS:
       print("Ending read out early after {} events...".format(EVENTS))
       break
       
if SAVE:
    print("Pickling vertexing information...")
    z_hard_file = open("z_hard.pkl","wb")
    pickle.dump(z_hard, z_hard_file)
    z_hard_file.close()
    pv_3D_file = open("pv_3D.pkl","wb")
    pickle.dump(pv_3D_data, pv_3D_file)
    pv_3D_file.close()
    pv_4D_file = open("pv_4D.pkl","wb")









