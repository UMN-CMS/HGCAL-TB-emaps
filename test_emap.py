#!/usr/local/bin/python
from emap_tools import *

import matplotlib as mpl
import matplotlib.pyplot as plt

plt.figure(figsize = (12,4))

cmap = 'viridis'
m_style = 'H'
m_size = 300

glob_angle = -30

bad_chans = [(2,20),(2,22),(2,12),(2,8),(2,10)] # HDMI side
bad_chans += [(3,44), (3,60)] # Cells different in v2 and v3 PCBs 

plt.subplot(121)
plt.title('V2 PCB')

mv2 = Module(45, 0, 'v2', angle = 0, facing = 'front', bad_chans=bad_chans)
x,y = mv2.get_chan_xy(angle = glob_angle)
plt.scatter(x,y, c = mv2.channels.CHIP, cmap = cmap, s = m_size, marker = m_style)#, s = 10*(5 - mv2.channels.TYPE))
sel = mv2.channels.bad == True
plt.plot(x[sel],y[sel], 'r' + m_style, markersize = m_size//30)

plt.grid()
plt.colorbar()

plt.subplot(122)
plt.title('V3 PCB')

mv3 = Module(45, 0, 'v3', angle = 0, facing = 'front', bad_chans=bad_chans)
x,y = mv3.get_chan_xy(angle = glob_angle)
plt.scatter(x,y, c = mv3.channels.CHIP, cmap = cmap, s = m_size, marker = m_style)#, s = 10*(5 - mv3.channels.TYPE))
sel = mv3.channels.bad == True
plt.plot(x[sel],y[sel], 'r'+m_style, markersize = m_size/30)

plt.colorbar()
plt.grid()

plt.show()
