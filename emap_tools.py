#!/usr/local/bin/python

import json
import numpy as np
import pandas as pd

from math import sin, cos, sqrt, pi

## Load basic EMaps

df_emap_v3 = pd.read_csv('basemaps/base_emap_v3_front-view_HDMI-NE.txt', delim_whitespace=True)
df_emap_v2 = pd.read_csv('basemaps/base_emap_v2_front-view_HDMI-NE.txt', delim_whitespace=True)

def rotate_uv(u,v,theta_deg = 0):
    theta = np.radians(theta_deg)

    u1 = (sin(theta)/sqrt(3) + cos(theta)) * u + 2/sqrt(3) * sin(theta) * v
    v1 = -2/sqrt(3) * sin(theta)  * u + (cos(theta) - sin(theta)/sqrt(3)) * v

    if theta_deg%60 == 0: return int(round(u1)), int(round(v1))
    else: return u1,v1

def rotate_u(u,v,theta_deg = 0):
    theta = np.radians(theta_deg)

    u1 = (sin(theta)/sqrt(3) + cos(theta)) * u + 2/sqrt(3) * sin(theta) * v

    if theta_deg%60 == 0: return int(round(u1))
    else: return u1

def rotate_v(u,v,theta_deg = 0):
    theta = np.radians(theta_deg)

    v1 = -2/sqrt(3) * sin(theta)  * u + (cos(theta) - sin(theta)/sqrt(3)) * v

    if theta_deg%60 == 0: return int(round(v1))
    else: return v1

def get_x_from_uv(u,v, A = 0.65):
    return A * sqrt(3) *(u + v/2.)

def get_y_from_uv(u,v, A = 0.65):
    return A * 3/2. * v

class Module():

    def __init__(self, ID, layer, pcb_version,
                 angle = 0, facing = 'front', bad_chans = [],
                 module_IX = 0, module_IV = 0, subdet = None, z_position = None):

        self.ID = ID
        self.layer = layer
        self.bad_chans = bad_chans

        self.pcb_version = pcb_version
        self.angle = angle
        self.facing = facing

        self.module_IX = module_IX
        self.module_IV = module_IV

        self.module_X = get_x_from_uv(self.module_IX, self.module_IV, A = 12*0.65)
        self.module_Y = get_y_from_uv(self.module_IX, self.module_IV, A = 12*0.65)

        print("Created: module ID %i, layer %i, PCB version %s" %(self.ID, self.layer, self.pcb_version))

        ## Get Channels
        if pcb_version == 'v3':
            self.channels = df_emap_v3.copy()
        else:
            self.channels = df_emap_v2.copy()

        ## remove bad_channels
        self.mark_bad_chans(self.bad_chans)

        # set module position
        self.channels['module_IX'] = self.module_IX
        self.channels['module_IV'] = self.module_IV

        ## update chip IDs with layer ID
        self.channels['layer'] = self.layer
        #self.channels.CHIP = self.layer * 4 + self.channels.CHIP

        # hflip
        self.hflip(self.facing)

        # rotate
        self.rotate(self.angle)


    def __repr__(self):
        return "Module ID %i, layer %i, PCB version %s" %(self.ID, self.layer, self.pcb_version)

    def rotate(self, angle):
        # rotate channels by angle (clockwise)
        if angle == 0:
            return 0

        print('Rotating by angle %i' % angle)

        IX_rot = self.channels.apply(lambda row: rotate_u(row.IX, row.IV, angle), axis = 1)
        IV_rot = self.channels.apply(lambda row: rotate_v(row.IX, row.IV, angle), axis = 1)

        self.channels['IX'] = IX_rot
        self.channels['IV'] = IV_rot

        return 1

    def hflip(self, facing):
        # flip horizontally
        if facing == 'back':
            print 'Flipping horizontally, facing backwards'

            self.channels['IX'] = self.channels.apply(lambda row: -(row.IX + row.IV), axis = 1)

    def mark_bad_chans(self, bad_chans):

        self.channels['bad'] = False

        for (chip,chan) in bad_chans:
            sel = self.channels.CHIP == chip
            sel &= self.channels.CHANNEL == chan

            self.channels.loc[sel,'bad'] = True

        if len(bad_chans) > 0:
            print("Marked %i bad channel(s)" % self.channels['bad'].sum())

        return 1

    def get_chan_xy(self, angle = 0):

        x = self.channels.apply(lambda row: get_x_from_uv(row.IX, row.IV), axis = 1) #+ self.module_X
        y = self.channels.apply(lambda row: get_y_from_uv(row.IX, row.IV), axis = 1) #+ self.module_Y

        if angle != 0:
            theta = np.radians(angle)
            c, s = np.cos(theta), np.sin(theta)
            R = np.array(((c,-s), (s, c)))
            x,y = zip(*np.dot(zip(x,y),R))
            x,y = np.array(x),np.array(y)

        x+= + self.module_X
        y+= + self.module_Y

        return x,y
