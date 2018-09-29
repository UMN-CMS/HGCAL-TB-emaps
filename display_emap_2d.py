#!/usr/local/bin/python
import sys
from emap_tools import *

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":


    if len(sys.argv) > 1:
        in_json_fname = sys.argv[1]
        print("## Input JSON emap file: " + in_json_fname)
    else:
        print("## No input JSON emap given!")
        exit(0)

    mdict = pd.read_json(in_json_fname, orient = 'records').T.to_dict()
    modules = [Module(**mdict[key]) for key in mdict]

    cmap = 'viridis'
    m_style = 'H'
    m_size = 100

    ## Global rotation required to have the same x/y as in the CMSSW version
    glob_angle = 30

    ## Use bad channels flag to mark special channels
    bad_chans = [(2,20),(2,22),(2,12),(2,8),(2,10)] # HDMI side
    #bad_chans += [(3,44), (3,60)] # Cells different in v2 and v3 PCBs

    fig = plt.figure(figsize = (8,4))
    ax = fig.add_subplot(111)

    for m in modules:
        print '## Plotting', m
        m.mark_bad_chans(bad_chans)

        x,y = m.get_chan_xy(angle = glob_angle)

        sel = m.channels.bad == False
        ax.scatter(x[sel],y[sel], c = m.channels.CHIP[sel], cmap = cmap, s = m_size, marker = m_style)

        sel = m.channels.bad == True
        ax.plot(x[sel], y[sel], 'r' + m_style, markersize = m_size/10)

    plt.grid()
    plt.show()
