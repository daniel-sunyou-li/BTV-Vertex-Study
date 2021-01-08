import ROOT, pickle
import numpy as np
from argparse import ArgumentParser
from DataFormats.FWLite import Events, Handle

parser = ArgumentParser()
parser.add_argument("-n", "--numEvents", default="-1", help="Total number of events to store")
parser.add_argument("-V", "--verbose",   action="store_true", help="Turn verbosity on")
parser.add_argument("-s", "--save",      action="store_true", help="Save event information to pickle file")
parser.add_argument("-f", "--file",      required=True, help="AOD file to analyze")
args = parser.parse_args()

events = Events( args.file )

VERBOSE = args.verbose
EVENTS  = int(args.numEvents)
SAVE    = args.save

# vertexing information to store
data = {
    "genParticles": {},
    "sortedPrimaryVertices": {},
    "offlinePrimaryVertices": {},
    "offlinePrimaryVerticesWithBS": {}
}

sortedPV_handle = Handle('vector<reco::Vertex>')
offlinePV_handle = Handle('vector<reco::Vertex>')
offlinePVwithBS_handle = Handle('vector<reco::Vertex>')
genParticles_handle = Handle("vector<reco::GenParticle>")

print_indx = int(events.size()) / 10
if EVENTS > 0:
    print_indx = EVENTS / 10

for i, event in enumerate(events):
    # gen particles
    gen_pv_count = 0
    event.getByLabel("genParticles",genParticles_handle)
    genParticles = genParticles_handle.product()
    data["genParticles"][i] = []
    for P in genParticles:
        if P.isHardProcess():
            data["genParticles"][i].append([P.vx(),P.vy(),P.vz(),P.pdgId()])
            gen_pv_count += 1
    # reco particles
    reco_pv_count = 0
    event.getByLabel("sortedPrimaryVertices",sortedPV_handle)
    sortedPVs = sortedPV_handle.product()
    data["sortedPrimaryVertices"][i] = []
    for PV in sortedPVs:
        data["sortedPrimaryVertices"][i].append([PV.x(),PV.y(),PV.z()])
        reco_pv_count += 1
    event.getByLabel("offlinePrimaryVertices",offlinePV_handle)
    offlinePVs = offlinePV_handle.product()
    data["offlinePrimaryVertices"][i] = []
    for PV in offlinePVs:
        data["offlinePrimaryVertices"][i].append([PV.x(),PV.y(),PV.z()])
    event.getByLabel("offlinePrimaryVerticesWithBS",offlinePVwithBS_handle)
    offlinePVWithBSs = offlinePVwithBS_handle.product()
    data["offlinePrimaryVerticesWithBS"][i] = []
    for PV in offlinePVWithBSs:
        data["offlinePrimaryVerticesWithBS"][i].append([PV.x(),PV.y(),PV.z()])
        
    if VERBOSE and i % print_indx == 0:
        print("=== Event {}: Gen PV: {} , Reco PV: {} ===".format(i,gen_pv_count,reco_pv_count))
        print("{:<30} {:<30} {:<30} {:<30}".format(
             "genParticles","sortedPrimaryVertices","offlinePrimaryVertices","offlinePrimaryVerticesWithBS"
        ))
        #print("{:<30} {:<30} {:<30} {:<30}".format(list(data.keys())))
        for j in range(4):
            print("{:<30} {:<30} {:<30} {:<30}".format(
                np.around(data["genParticles"][i][j][1:],4),
                np.around(data["sortedPrimaryVertices"][i][j],4),
                np.around(data["offlinePrimaryVertices"][i][j],4),
                np.around(data["offlinePrimaryVerticesWithBS"][i][j],4)
            ))
    if i == EVENTS: break

if VERBOSE: print("Scanned over a total of {} events".format(i+1))

if SAVE:
    print("Pickling vertexing information...")
    data_file = open( "AOD_PV_{}.pkl".format( i ), "wb" )
    pickle.dump( data, data_file )
    data_file.close()
