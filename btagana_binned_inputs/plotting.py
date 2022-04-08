import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm, colors
import numpy as np
import mplhep as hep
import config
    
def plot_1D( values, variables, year, lumitext, xlabel, btagger, wp, saveDir ):
    plt.style.use( hep.style.CMS )
    plt.figure( figsize = (8,8) )
    
    hists = {}
    for variable in variables:
        hists[ variable ] = np.histogram(
            values[ variable ],
            bins = config.plot_params[ variable ][ "BINS" ]
        )
        legend_label = "${}$".format( config.plot_params[ variable ][ "LATEX" ] )
        if variable in [ "nB" ]:
            legend_label += " {} ({})".format( btagger, wp[0] )
                                     
        plt.errorbar(
            0.5 * ( hists[ variable ][1][1:] + hists[ variable ][1][:-1] ),
            hists[ variable ][0],
            yerr = np.sqrt( hists[ variable ][0] ),
            marker = ".", drawstyle = "steps-mid",
            label = legend_label
        )


    hep.cms.text( "Preliminary", fontsize = 24 )
    hep.cms.lumitext( "{} {}".format( year, lumitext ), fontsize = 16 )

    plt.xlabel( "${}$".format( xlabel ), ha = "right", x = 1.0, fontsize = 16 )
    plt.yscale( "log" )
    plt.ylabel( "Count", ha = "right", y = 1.0, fontsize = 16 )
    plt.legend( loc = "best", fontsize = 12 )
    plt.savefig( saveDir )
    plt.show()
    plt.close()
               

def plot_binned( hists, plotVar, binVar, histBins, year, lumitext, btagger, wp, hide = [], thresh = 5e3 ):
    plt.style.use( hep.style.CMS )
    plt.figure( figsize = (8,8) )
    i = 0
    for i in hists[ binVar ]:
        binVal = histBins[ binVar ][i]
        if binVal in hide: continue
        if len( hists[ binVar ][i] ) < thresh: continue
        plt.hist(
           hists[ binVar ][i], bins = config.plot_params[ plotVar ][ "BINS" ],
           label = "${}$={:.1e} ({})".format( 
               config.plot_params[ binVar ][ "LATEX" ],
               binVal,
               len( hists[ binVar ][i] )
           ),
            density = True, histtype = "step", linewidth = 2, color = cm.tab20c.colors[i]
        )
        i += 1
    hep.cms.text( "Preliminary", fontsize = 24 )
    hep.cms.lumitext( "{} {}".format( year, lumitext ), fontsize = 16 )
    
    plt.xlabel(
        "${}$".format( config.plot_params[ plotVar ][ "LATEX" ] ),
        x = 1.0, ha = "right", fontsize = 20
    )
    plt.ylabel( "Normalized Count", y = 1.0, ha = "right", fontsize = 20 )
    plt.yscale( "log" )
    if binVar == "nB": 
        plt.legend( 
            title = "{} ({})".format( btagger, wp[0] ),
            loc = "best", fontsize = 12, title_fontsize = 14
        )
    else:
        plt.legend( loc = "best", fontsize = 12 )
    
    plt.show()
    plt.close()
    
def add_subplot(ax,rect):
    fig = plt.gcf()
    box = ax.get_position()
    width = box.width
    height = box.height
    inax_position = ax.transAxes.transform(rect[0:2])
    transFigure = fig.transFigure.inverted()
    infig_position = transFigure.transform(inax_position)
    x = infig_position[0]
    y = infig_position[1]
    width *= rect[2]
    height *= rect[3]
    subax = fig.add_axes([x,y,width,height])
    x_labelsize = subax.get_xticklabels()[0].get_size() * rect[2]**0.5
    y_labelsize = subax.get_yticklabels()[0].get_size() * rect[3]**0.5
    subax.xaxis.set_tick_params(labelsize=x_labelsize)
    subax.yaxis.set_tick_params(labelsize=y_labelsize)
    return subax

def plot_hist_nJnB( hist, variable, nJ_edges, nB_edges, year, lumitext, saveDir ):
    figure, subplots = plt.subplots( 
        len( nB_edges ) + 1, len( nJ_edges ) + 1, figsize = ( ( 4*( len(nJ_edges) + 1 ), 4*( len(nB_edges) + 1 ) ) )
    )
    
    nEvents = [ len( hist[x][y] ) for x in hist for y in hist[x] ]

    for i, nB in enumerate( nB_edges ):
        for j, nJ in enumerate( nJ_edges ):
            subplots[i][j].hist( hist[nB][nJ], bins = config.plot_params[ variable ][ "BINS" ] )
            subplots[i][j].set_ylim( 0.9, 5*np.max( nEvents ) )
            subplots[i][j].set_yscale( "log" )
            
            nB_eq = "="
            nJ_eq = "="
            if nB == nB_edges[0]: nB_eq = "\leq"
            if nB == nB_edges[-1]: nB_eq = "\geq" 
            if nJ == nJ_edges[0]: nJ_eq = "\leq"
            if nJ == nJ_edges[-1]: nJ_eq = "\geq"
                
            subplots[i][j].set_title(
                "$N_b{}{},\ N_j{}{}$".format( nB_eq, int(nB), nJ_eq, int(nJ) ), x = 1.0, ha = "right", fontsize = 25
            )
            subplots[i][j].text(
                0.95*max( config.plot_params[ variable ][ "BINS" ] ), 2 * np.max( nEvents ),
                "$N_{events}=$" + str( len( hist[nB][nJ] ) ),
                fontsize = 24, ha = "right", va = "top"
            )
            if j != 0:
                subplots[i][j].set_yticklabels( [] )
            subplots[i][j].set_xticklabels( [] )
            if i == 0 and j == 0:
                subplots[i][j].set_ylabel( "Event Count", y = 1.0, ha = "right", fontsize = 30 )
            subplots[i][j].tick_params( axis = "both", labelsize = 20 )
    

    for i, nB in enumerate( nB_edges ):
        for j, nJ in enumerate( nJ_edges ):
            subplots[i][-1].hist(
                hist[nB][nJ], bins = config.plot_params[ variable ][ "BINS" ],
                label = int(nJ),
                density = True, histtype = "step"
            )
        nB_eq = "="
        if nB == nB_edges[0]: nB_eq = "\leq"
        if nB == nB_edges[-1]: nB_eq = "\geq"
        
        subplots[i][-1].set_title( "$N_b{}{}$".format( nB_eq, int(nB) ), x = 1.0, ha = "right", fontsize = 24 )
        subplots[i][-1].set_yscale( "log" )
        subplots[i][-1].set_yticklabels( [] )
        subplots[i][-1].set_xticklabels( [] )
        subplots[i][-1].legend( fontsize = 12 )
        subplots[i][-1].tick_params( axis = "both", labelsize = 20 )
        
    for j, nJ in enumerate( nJ_edges ):
        for i, nB in enumerate( nB_edges ):
            subplots[-1][j].hist(
                hist[nB][nJ], bins = config.plot_params[ variable ][ "BINS" ],
                label = int(nB),
                density = True, histtype = "step"
            )
        subplots[-1][j].set_yscale( "log" )
        if j != 0: 
            subplots[-1][j].set_yticklabels( [] )
        if nJ == nJ_edges[-1]:
            subplots[-1][j].set_xlabel( "${}$".format( config.plot_params[ variable ][ "LATEX" ] ), x = 1.0, ha = "right", fontsize = 30 )
        nJ_eq = "="
        if nJ == nJ_edges[0]: nJ_eq = "\leq "
        if nJ == nJ_edges[-1]: nJ_eq = "\geq "
        subplots[-1][j].set_title( "$N_j{}{}$".format( nJ_eq, int(nJ) ), x = 1.0, ha = "right", fontsize = 24  )
        subplots[-1][j].legend( fontsize = 12 )
        subplots[-1][j].tick_params( axis = "both", labelsize = 20 )
        
    subplots[-1][-1].axis("off")
    plt.suptitle( "{} {}".format( year, lumitext ), x = 1.0, ha = "right", fontsize = 40 )
    plt.tight_layout()

    plt.savefig( saveDir )
    plt.show()
    plt.close()
    
def plot_PVRecoAcc_1D( hist, edges, variable, year, lumitext, btagger, wp, saveDir ):
    plt.style.use( hep.style.CMS )
    figure, subplots = plt.subplots(
        2, 1, figsize = (10,10),
        gridspec_kw = { "height_ratios": [2,1] }
    )
    subplots[0].errorbar(
        edges, hist["EFFICIENCY"], yerr = hist["EFFICIENCY ERR"],
        ms = 10, mec = "k", marker = "o", ls = "", elinewidth = 2, ecolor = "k", capsize = 5
    )
    
    xticklabels = []
    xticks = []
    for edge in edges:
        if variable in [ "nJ", "nB" ]:
            tick_label = int(edge)
        else:
            tick_label = "{:.3f}".format( edge )
        
        if edge == edges[0]:
            xticklabels.append( "$\leq {}$".format( tick_label ) )
        elif edge == edges[-1]:
            xticklabels.append( "$\geq {}$".format( tick_label ) )
        else:
            xticklabels.append( tick_label )
        xticks.append( edge )
    
    subplots[0].set_ylabel( "PV Reconstruction Efficiency", fontsize = 20, y = 1.0, ha = "right" )
    subplots[0].set_ylim( -0.05, 1.05 )
    subplots[0].set_xticks( [] )
    subplots[0].tick_params( axis = "both", labelsize = 18 )
    subplots[0].grid( which = "both", ls = ":", lw = 2 )
    
    subplots[1].errorbar(
        edges, hist["TOTAL"], yerr = np.sqrt( hist["TOTAL"] ),
        ms = 10, mec = "k", marker = "o", ls = "", elinewidth = 2, ecolor = "k", capsize = 5
    )
    subplots[1].set_xticklabels( xticklabels )
    subplots[1].set_xticks( xticks )
    subplots[1].set_ylabel( "Event Count", fontsize = 24, y = 1.0, ha = "right" )
    subplots[1].set_yscale( "log" )
    xlabel = r"${}$".format( config.plot_params[ variable ][ "LATEX" ] )
    if variable == "nB": xlabel += " {} ({})".format( btagger, wp[0] )
    subplots[1].set_xlabel( xlabel, fontsize = 24, x = 1.0, ha = "right" )
    subplots[1].tick_params( axis = "both", labelsize = 18 )
    subplots[1].grid( which = "major", ls = ":", lw = 2 )
    
    hep.cms.text( "Preliminary", ax = subplots[0], fontsize = 24 )
    hep.cms.lumitext( "{} {}".format( year, lumitext ), ax = subplots[0], fontsize = 20 )
        
    subplot = add_subplot( subplots[0], [0.25,0.2,0.6,0.6] )
    subplot.errorbar(
        edges, hist[ "EFFICIENCY" ], yerr = hist["EFFICIENCY ERR"],
        ms = 10, mec = "k", marker = "o", ls = "", elinewidth = 2, ecolor = "k", capsize = 5
    )
    subplot.set_xticklabels( xticklabels )
    subplot.set_xticks( xticks )
    subplot.set_ylim( 0.85, 1.01 )
    subplot.set_yticks( [0.85,0.9,0.95,1.0] )

    plt.tight_layout()

    plt.savefig( saveDir )
    plt.show()
    plt.close()
    
def plot_PVRecoAcc_2D( hist, x, y, x_edges, y_edges, year, lumitext, btagger, wp, saveDir ):
    plt.style.use( hep.style.CMS )
    plt.figure( figsize = ( 2*len( x_edges ), 2*len( y_edges ) ) )
    plt.imshow( hist[ "EFFICIENCY" ].transpose(), cmap = "Blues", vmin = 0, vmax = 1 )
    plt.colorbar( label = "Reconstruction Efficiency" )
    for x_ in range( len( x_edges ) ):
        for y_ in range( len( y_edges ) ):
            color = "white" if hist[ "EFFICIENCY" ][x_][y_] > 0.7 else "black"
            if np.isnan( hist[ "EFFICIENCY" ][x_][y_] ): hist[ "EFFICIENCY" ][x_][y_] = 0
            plt.text(
                x_, y_, "{:.2f}$\pm${:.2f}".format( hist["EFFICIENCY"][x_][y_], hist["EFFICIENCY ERR"][x_][y_] ),
                ha = "center", va = "center", fontsize = 14, color = color
            )
            
    xlabels = []
    for x_, x_edge in enumerate( x_edges ):
        if x in [ "nJ", "nB" ]:
            xtick = int( x_edge )
        else:
            xtick = "{:.4f}".format( x_edge )
        if x_edge == x_edges[0]: xlabels.append( r"$\leq {}$".format( xtick ) )
        elif x_edge == x_edges[-1]: xlabels.append( r"$\geq {}$".format( xtick ) )
        else: xlabels.append( "{}".format( xtick ) )
    ylabels = []
    for y_, y_edge in enumerate( y_edges ):
        if y in [ "nJ", "nB" ]:
            ytick = int( y_edge )
        else:
            ytick = "{:.4f}".format( y_edge )
        if y_edge == y_edges[0]: ylabels.append( r"$\leq {}$".format( ytick ) )
        elif y_edge == y_edges[-1]: ylabels.append( r"$\geq {}$".format( ytick ) )
        else: ylabels.append( "{}".format( ytick ) )
            
    hep.cms.text( "Preliminary", fontsize = 30 )
    hep.cms.lumitext( "{} {}".format( year, lumitext ), fontsize = 16 )
    xlabel = "${}$".format( config.plot_params[x]["LATEX"] )
    if x == "nB": xlabel += " {} ({})".format( btagger, wp[0] )
    plt.xlabel( xlabel, fontsize = 30 )
    plt.xticks(
        ticks = list( range( len(x_edges) ) ),
        labels = xlabels
    )
    ylabel = "${}$".format( config.plot_params[y]["LATEX"] )
    if y == "nB": ylabel += " {} ({})".format( btagger, wp[0] )
    plt.ylabel( ylabel, fontsize = 30 )
    plt.yticks(
        ticks = list( range( len(y_edges) ) ),
        labels = ylabels
    )
    
    plt.savefig( saveDir )
    plt.show()
    plt.close()
    
def plot_yield_2D( hist, x, y, x_edges, y_edges, year, lumitext, btagger, wp, saveDir ):
    plt.style.use( hep.style.CMS )
    plt.figure( figsize = ( 2*len( x_edges ), 2*len( y_edges ) ) )
    plt.imshow( hist[ "TOTAL" ].transpose(), cmap = "Blues" )
    plt.colorbar( label = "Yield" )
    for x_ in range( len( x_edges ) ):
        for y_ in range( len( y_edges ) ):
            color = "white" if hist[ "TOTAL" ][x_][y_] > 0.7 * hist[ "TOTAL" ].max() else "black"
            plt.text(
                x_, y_, "{:.0f}$\pm${:.0f}".format( hist["TOTAL"][x_][y_], np.sqrt( hist["TOTAL"][x_][y_] ) ),
                ha = "center", va = "center", fontsize = 14, color = color
            )
            
    xlabels = []
    for x_, x_edge in enumerate( x_edges ):
        if x in [ "nJ", "nB" ]:
            xtick = int( x_edge )
        else:
            xtick = "{:.4f}".format( x_edge )
        if x_edge == x_edges[0]: xlabels.append( r"$\leq {}$".format( xtick ) )
        elif x_edge == x_edges[-1]: xlabels.append( r"$\geq {}$".format( xtick ) )
        else: xlabels.append( "{}".format( xtick ) )
    ylabels = []
    for y_, y_edge in enumerate( y_edges ):
        if y in [ "nJ", "nB" ]:
            ytick = int( y_edge )
        else:
            ytick = "{:.4f}".format( y_edge )
        if y_edge == y_edges[0]: ylabels.append( r"$\leq {}$".format( ytick ) )
        elif y_edge == y_edges[-1]: ylabels.append( r"$\geq {}$".format( ytick ) )
        else: ylabels.append( "{}".format( ytick ) )
            
    hep.cms.text( "Preliminary", fontsize = 30 )
    hep.cms.lumitext( "{} {}".format( year, lumitext ), fontsize = 16 )
    xlabel = "${}$".format( config.plot_params[x]["LATEX"] )
    if x == "nB": xlabel += " {} ({})".format( btagger, wp[0] )
    plt.xlabel( xlabel, fontsize = 30 )
    plt.xticks(
        ticks = list( range( len(x_edges) ) ),
        labels = xlabels
    )
    ylabel = "${}$".format( config.plot_params[y]["LATEX"] )
    if y == "nB": ylabel += " {} ({})".format( btagger, wp[0] )
    plt.ylabel( ylabel, fontsize = 30 )
    plt.yticks(
        ticks = list( range( len(y_edges) ) ),
        labels = ylabels
    )
    
    plt.savefig( saveDir )
    plt.show()
    plt.close()
    
def plot_vertex_1D( dzPV, dzAV, edges, sub_edges, year, lumitext, savedir ):
    plt.style.use( hep.style.CMS )
    fig, ax = plt.subplots( figsize = (10,10) )
    plt.hist( 
        dzPV, bins = edges,
        alpha = 0.5, label = "$\Delta z_{PV}$"
    )
    plt.hist( 
        dzAV, bins = edges,
        alpha = 0.5, label = "$\Delta z_{AV}$"
    )

    plt.xlabel( r"$|\Delta z|$ (cm)" )
    plt.xlim( edges[0], edges[-1] )

    plt.ylabel( "Count" )
    plt.yscale( "log" )
    hep.cms.text( "Preliminary", fontsize = 24 )
    hep.cms.lumitext( "{} {}".format( year, lumitext ), fontsize = 20 )
    plt.legend( loc = "best", fontsize = 24 )

    subplot = add_subplot( ax, [0.17,0.47,0.45,0.45] )
    subplot.hist( 
        dzPV, bins = sub_edges,
        alpha = 0.5
    )
    subplot.hist(
        dzAV, bins = sub_edges,
        alpha = 0.5
    )
    subplot.set_yscale( "log" )
    subplot.set_xlim( sub_edges[0], sub_edges[-1] )

    plt.savefig( savedir )
    plt.show()
    plt.close()
    
def plot_binned_vertex( hist, variable, binVar, edges, year, lumitext, btagger, wp, hide = [], thresh = 1e3 ):
    plt.style.use( hep.style.CMS )
    plt.figure( figsize = (10,10) )
    
    i = 0
    for edge in hist[ variable ]:
        if edge in hide: continue
        if len( hist[ variable ][ edge ] ) < thresh: continue
        plt.hist(
            hist[ variable ][ edge ], edges, 
            label = "${}$={} ({})".format(
                config.plot_params[ binVar ][ "LATEX" ],
                edge, len( hist[ variable ][ edge ] )
            ),
            density = True, histtype = "step", linewidth = 2, color = cm.tab20c.colors[i]
        )
        i += 1
    
    hep.cms.text( "Preliminary", fontsize = 24 )
    hep.cms.lumitext( "{} {}".format( year, lumitext ), fontsize = 20 )
    
    xlabel = "$\Delta z_{PV}$" if "PV" in variable else "$\Delta z_{AV}$"
    
    plt.xlabel(
        xlabel,
        x = 1.0, ha = "right", fontsize = 20
    )
    plt.ylabel( "Normalized Count", y = 1.0, ha = "right", fontsize = 20 )
    plt.yscale( "log" )
    if binVar == "nB":
        plt.legend( 
            title = "{} ({})".format( btagger, wp[0] ), 
            loc = "best", fontsize = 12, title_fontsize = 14
        )
    else:
        plt.legend( loc = "best", fontsize = 12 )
    
    plt.show()
    plt.close()
    
def plot_yield_dz2D( hist, edges, xVar, dzVar, btagger, wp, year, lumitext, savedir ):
    plt.style.use( hep.style.CMS )
    geq_count = 0
    for dz in hist[dzVar]:
        if dz >= 0.005: geq_count += 1
    
    plt.figure( figsize = (15,10) )
    color = mpl.cm.Greens if "PV" in dzVar else mpl.cm.Blues
    plt.hist2d(
        hist[xVar], hist[dzVar],
        bins = ( edges[xVar], edges[dzVar] ),
        norm = mpl.colors.LogNorm(), cmap = color
    )
    plt.colorbar( label = "Event Count" )
    plt.plot(
        [0,25],[0.005,0.005],
        color = "k"
    )
    plt.text(
        edges[xVar][-2], edges[dzVar][-2],
        "$N(\Delta z\geq 0.005\ cm)={}\ ({:.2f}\%)$".format( geq_count, 100. * geq_count / len( hist[dzVar] ) ),
        ha = "right", va = "top",
        bbox = dict( facecolor="white", alpha=1.0 ),
        fontsize = 20
    )
    plt.text(
        edges[xVar][-2] - 0.1, 0.0055,
        "$\Delta z=0.005\ cm$",
        ha = "right", va = "bottom", fontsize = 20
    )
    plt.xticks( edges[xVar] )
    xlabel = config.plot_params[ xVar ][ "LATEX" ]
    if xVar == "nB": xlabel += "{} ({})".format( btagger, wp[0] )
    plt.xlabel( "${}$".format( xlabel ) )
    plt.yscale( "log" )
    ylabel = "$|z^{GEN}_{PV}-z^{RECO}_{PV}|$" if "PV" in dzVar else "$|z^{GEN}_{PV}-z^{RECO}_{AV}|$"
    plt.ylabel( ylabel )
    plt.minorticks_on()
    plt.grid( which = "major", ls = ":", lw = 2 )
    hep.cms.text( "Preliminary", fontsize = 24 )
    hep.cms.lumitext( "{} {}".format( year, lumitext ), fontsize = 20 )
    plt.savefig( savedir )
    plt.show()
    plt.close()
    
def plot_dz2D( hist, x_edges, y_edges, dzVar, btagger, wp, year, lumitext, savedir ):
    plt.style.use( hep.style.CMS )
    plt.figure( figsize = ( len( x_edges ), len( y_edges ) ) )
    if "PV" in dzVar:
        hist_plot = 1e3 * np.array( hist[ "dzPV_avg" ] )
        hist_err = 1e3 * np.array( hist[ "dzPV_err" ] )
        color = "Greens"
    else:
        hist_plot = 1e3 * np.array( hist[ "dzAV_avg" ] )
        hist_err = 1e3 * np.array( hist[ "dzAV_err" ] )
        color = "Blues"
        
    for x_ in range( len( x_edges ) ):
        for y_ in range( len( y_edges ) ):
            if np.isnan( hist_plot[x_][y_] ):
                hist_plot[x_][y_] = 0
            if np.isnan( hist_err[x_][y_] ):
                hist_err[x_][y_] = 0
        
    plt.imshow(
        np.transpose( hist_plot ),
        cmap = color, norm = colors.LogNorm()
    )
    if "PV" in dzVar:
        plt.colorbar( label = "Avg. $\Delta z_{PV}$ (mm)" )
    else:
        plt.colorbar( label = "Avg. $\Delta z_{AV}$ (mm)" )
            
    xlabels = []
    for x, x_edge in enumerate( x_edges ):
        if x_edge == x_edges[0]: xlabels.append( "$\leq {}$".format( int(x_edge) ) )
        elif x_edge == x_edges[-1]: xlabels.append( "$\geq {}$".format( int(x_edge) ) )
        else:
            xlabels.append( str( int( x_edge ) ) )                              
    ylabels = []
    for y, y_edge in enumerate( y_edges ):
        if y_edge == y_edges[0]: ylabels.append( "$\leq {}$".format( int(y_edge) ) )
        elif y_edge == y_edges[-1]: ylabels.append( "$\geq {}$".format( int(y_edge) ) )
        else:
            ylabels.append( str( int( y_edge ) ) )
        
    for x_ in range( len( x_edges ) ):
        for y_ in range( len( y_edges ) ):
            if hist_plot[x_][y_] > 5:
                plt.text( x_, y_, "X", color = "Red", ha = "center", va = "center" )
        
    hep.cms.text( "Preliminary", fontsize = 30 )
    hep.cms.lumitext( "{} {}".format( year, lumitext ), fontsize = 20 )
    plt.xlabel( "$N_j$", fontsize = 30 )
    plt.xticks(
       ticks = list( range( len( x_edges ) ) ),
       labels = xlabels
    )
    plt.ylabel( "$N_b$ {} ({})".format( btagger, wp[0] ), fontsize = 30 )
    plt.yticks(
       ticks = list( range( len( y_edges ) ) ),
       labels = ylabels
    )
    
    plt.show()
    plt.close()