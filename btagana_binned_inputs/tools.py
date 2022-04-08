import numpy as np
import tqdm
import config
from ROOT import TFile

def load_files( filenames ):
    print( "[START] Loading ROOT files:" )
    rFiles = { filename: TFile.Open( filename ) for filename in filenames }
    rTrees = { filename: rFiles[ filename ].Get( "btagana" ).Get( "ttree" ) for filename in filenames }
    pyTrees = {}
    total_events = 0
    
    for filename in rTrees:
        columns = [ branch.GetName() for branch in rTrees[ filename ].GetListOfBranches() if branch.GetName() not in ['SV_vtxDistJetAxis', 'SV_EnergyRatio'] ]
        pyTrees[ filename ], variables = rTrees[ filename ].AsMatrix( columns = columns, return_labels = True )
        print( "+ {} has {} events".format( filename, pyTrees[ filename ].shape[0] ) )
        total_events += pyTrees[ filename ].shape[0]
    print( "[DONE] Loaded {} events with {} variables".format( total_events, len( variables ) ) )
    return pTrees, variables

def get_nB( tree, nJ, btagger, wp ):
    nB = 0
    for i in range( int(nJ) ):
        bdisc = 0
        for bdisc_var in config.bdiscs[ btagger ]:
            bdisc += getattr( tree, bdisc_var )[i]
        if bdisc > config.wp[ btagger ][ wp ]: nB += 1
    return nB

def get_bins( trees, btagger, wp ):
    print( "[START] Evaluating bins for:" )
    print( "  + jet multiplicity" )
    print( "  + b jet multiplicity" )
    print( "  + dz PV(RECO,GEN)" )

    total_events = 0
    for filename in trees:
        total_events += trees[ filename ].GetEntries()

    event_stats = {
        i: {
            "nJ": 0,
            "nB": 0,
            "dz": 0
        } for i in range( 0, total_events + 1 )
    }
    bin_hists = {
        "nJ": [],
        "nB": [],
        "dz": []
    }
    
    i = 0
    for filename in trees:
        print( ">> Loading: {}".format( filename ) )
        tree = trees[ filename ]
        for j in tqdm.trange( 0, tree.GetEntries() ):
            tree.GetEntry(j)
            nJ_ = getattr( tree, "nJet" )
            bin_hists[ "nJ" ].append( nJ_ )
            event_stats[i][ "nJ" ] = nJ_
            
            z_RECO_ = getattr( tree, "PV_z" )[0]
            z_GEN_ = getattr( tree, "GenPVz" )
            bin_hists[ "dz" ].append( abs( z_RECO_ - z_GEN_ ) )
            event_stats[i][ "dz" ] = abs( z_RECO_ - z_GEN_ )
            nB_ = get_nB( tree, nJ_, btagger, wp )
            bin_hists[ "nB" ].append( nB_ )
            event_stats[i][ "nB" ] = nB_
            
            i += 1
            
    return event_stats, bin_hists
    
def get_hist( trees, stats, bins, variable ):
    hists = {
        key: {
            i: [] for i in range( len( bins[ key ] ) )
        } for key in bins
    }
    
    i = 0
    for filename in trees:
        tree = trees[ filename ]
        for j in tqdm.trange( 0, tree.GetEntries() ):
            tree.GetEntry(j)
            
            values_ = getattr( tree, variable )
            
            for key in hists:
                for idx, bin_val in enumerate( bins[ key ] ):
                    if stats[i][key] <= bin_val: break
                if type( values_ ) in [ int, float ]:
                    hists[ key ][ idx ].append( values_ )
                else:
                    for value_ in values_:
                        hists[ key ][ idx ].append( value_ )
            i += 1
    
    return hists
          
def get_hist_nJnB( trees, variable, nJ_edges, nB_edges, btagger, wp ):
    hists = {
        nB_: {
            nJ_: [] for nJ_ in nJ_edges
        } for nB_ in nB_edges
    }
    i = 0
    for filename in trees:
        tree = trees[ filename ]
        for j in tqdm.trange( 0, tree.GetEntries() ):
            tree.GetEntry(j)
            values_ = getattr( tree, variable )
            nJ_ = getattr( tree, "nJet" )
            nB_ = get_nB( tree, nJ_, btagger, wp )
            
            nJ_ = np.clip( nJ_, min(nJ_edges), max(nJ_edges) )
            nB_ = np.clip( nB_, min(nB_edges), max(nB_edges) )
            
            if type( values_ ) in [ int, float ]:
                hists[nB_][nJ_].append( values_ )
            else:
                for value_ in values_:
                    hists[nB_][nJ_].append( value_ )
                    
    return hists
    
def efficiency_err(n,k):
    return np.sqrt( ( (k+1)*(k+2) ) / ( (n+2)*(n+3) ) ) - ( (k+1)**2 / (n+2)**2  )

def get_PVRecoAcc_1D( trees, variable, edges, btagger, wp ):
    hists = {
        "ACCURATE": np.zeros( len( edges ) ),
        "TOTAL": np.zeros( len( edges ) )
    }
    for filename in trees:
        tree = trees[ filename ]
        for i in tqdm.trange( 0, tree.GetEntries() ):
            tree.GetEntry(i)
            
            z_RECO = getattr( tree, "PV_z" )
            z_GEN = getattr( tree, "GenPVz" )
            dz = [ abs( z - z_GEN ) for z in z_RECO ]
            
            if variable == "nJ":
                value = np.clip( getattr( tree, "nJet" ), edges[0], edges[-1] )
            elif variable == "nB":
                value = np.clip( get_nB( tree, getattr( tree, "nJet" ), btagger, wp ), edges[0], edges[-1] )
            elif variable == "dz":
                value = np.clip( dz[0], edges[0], edges[-1] )
            else:
                print( "[ERR] Invalid variable argument, returning empty histogram" )

            for j, edge in enumerate( edges ):
                if value <= edge: break
            if dz[0] == min(dz):
                hists[ "ACCURATE" ][j] += 1
            hists[ "TOTAL" ][j] += 1
            
    hists[ "EFFICIENCY" ] = hists[ "ACCURATE" ] / hists[ "TOTAL" ]
    hists[ "EFFICIENCY ERR" ] = efficiency_err( hists["TOTAL"], hists["ACCURATE"] )
    return hists
            
def get_PVRecoAcc_2D( trees, x1, x2, x1_edges, x2_edges, btagger, wp ):
    hists = {
        "ACCURATE": np.zeros( ( len( x1_edges ), len( x2_edges ) ) ),
        "TOTAL": np.zeros( ( len( x1_edges ), len( x2_edges ) ) )
    }
    for filename in trees:
        tree = trees[ filename ]
        for i in tqdm.trange( 0, tree.GetEntries() ):
            tree.GetEntry(i)
            
            z_RECO = getattr( tree, "PV_z" )
            z_GEN = getattr( tree, "GenPVz" )
            dz = [ abs( z - z_GEN ) for z in z_RECO ]
            
            if x1 == "nJ":
                val1 = np.clip( getattr( tree, "nJet" ), min( x1_edges ), max( x1_edges ) )
            elif x1 == "nB":
                val1 = np.clip( get_nB( tree, getattr( tree, "nJet" ), btagger, wp ), x1_edges[0], x1_edges[-1] )
            elif x1 == "dz":
                val1 = np.clip( dz[0], x1_edges[0], x1_edges[-1] )
            
            if x2 == "nJ":
                val2 = np.clip( getattr( tree, "nJet" ), min( x2_edges ), max( x2_edges ) )
            elif x2 == "nB":
                val2 = np.clip( get_nB( tree, getattr( tree, "nJet" ), btagger, wp ), x2_edges[0], x2_edges[-1] )
            elif x2 == "dz":
                val2 = np.clip( dz[0], x2_edges[0], x2_edges[-1] )
            
            for j, edge in enumerate( x1_edges ):
                if val1 <= edge: break
            for k, edge in enumerate( x2_edges ):
                if val2 <= edge: break
            if dz[0] == min(dz):
                hists[ "ACCURATE" ][j][k] += 1
            hists["TOTAL"][j][k] += 1
            
    hists[ "EFFICIENCY" ] = hists[ "ACCURATE" ] / hists[ "TOTAL" ]
    hists[ "EFFICIENCY ERR" ] = efficiency_err( hists["TOTAL"], hists["ACCURATE"] )

    return hists
          
def get_dz_1D( trees, edges, variable, btagger, wp ):
    hist = {
        "DZ PV": [],
        "DZ AV": [],
        "DZ PV BINNED": { edge: [] for edge in edges },
        "DZ AV BINNED": { edge: [] for edge in edges }
    }
    for filename in trees:
        tree = trees[ filename ]
        for i in tqdm.trange( 0, tree.GetEntries() ):
            tree.GetEntry(i)
            
            z_RECO = getattr( tree, "PV_z" )
            z_GEN = getattr( tree, "GenPVz" )
            dz = [ abs( z - z_GEN ) for z in z_RECO ]
            
            dz_PV = dz[0]
            dz_AV = min(dz)
            
            hist[ "DZ PV" ].append( dz_PV )
            hist[ "DZ AV" ].append( dz_AV )
            
            if variable == "nJ":
                value = np.clip( getattr( tree, "nJet" ), edges[0], edges[-1] )
            elif variable == "nB":
                value = np.clip( get_nB( tree, getattr( tree, "nJet" ), btagger, wp ), edges[0], edges[-1] )
            else:
                print( "[ERR] Invalid variable argument, returning empty histogram" )
                return hist

            hist[ "DZ PV BINNED" ][value].append( dz_PV )
            hist[ "DZ AV BINNED" ][value].append( dz_AV )
            
    return hist

def get_dz_2D( trees, nj_edges, nb_edges, btagger, wp ):
    hists = {
        "nJ": [],
        "nB": [],
        "dzAV": [],
        "dzPV": []
    }
    binned_hists = {
        key: {
            nj: {
                nb: [] for nb in nb_edges
            } for nj in nj_edges
        } for key in [ "dzAV", "dzPV" ]
    }
    
    for filename in trees:
        tree = trees[ filename ]
        for i in tqdm.trange( 0, tree.GetEntries() ):
            tree.GetEntry(i)
            
            z_RECO = getattr( tree, "PV_z" )
            z_GEN = getattr( tree, "GenPVz" )
            dz = [ abs( z - z_GEN ) for z in z_RECO ]
            
            nJ_ = int( getattr( tree, "nJet" ) )
            nB_ = int( get_nB( tree, getattr( tree, "nJet" ), btagger, wp ) )
            
            hists["nJ"].append( nJ_ )
            hists["nB"].append( nB_ )
            hists["dzAV"].append( min(dz) )
            hists["dzPV"].append( dz[0] )
            
            binned_hists[ "dzAV" ][ np.clip( nJ_, nj_edges[0], nj_edges[-1] ) ][ np.clip( nB_, nb_edges[0], nb_edges[-1] ) ].append( min(dz) )
            binned_hists[ "dzPV" ][ np.clip( nJ_, nj_edges[0], nj_edges[-1] ) ][ np.clip( nB_, nb_edges[0], nb_edges[-1] ) ].append( dz[0] )
            
    hist_stats = {}
    for key in binned_hists:
        hist_stats[ key + "_avg" ] = np.zeros( ( len( nj_edges ), len( nb_edges ) ) )
        hist_stats[ key + "_err" ] = np.zeros( ( len( nj_edges ), len( nb_edges ) ) )
        for nj in binned_hists[key]:
            for nb in binned_hists[key][nj]:
                hist_stats[ key + "_avg" ][int(nj)][int(nb)] = np.mean( binned_hists[ key ][int(nj)][int(nb)] )
                hist_stats[ key + "_err" ][int(nj)][int(nb)] = np.std( binned_hists[ key ][int(nj)][int(nb)] )
    return hists, hist_stats

