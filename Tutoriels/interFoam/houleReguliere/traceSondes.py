#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 09:23:49 2021

@author: vbaconnet
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


#==============================================================================
#----------------------------- Fonctions----------- ---------------------------
#==============================================================================

def animate(i, line1, line2, line3, t, y1, y2, y3):
    line1.set_data(t[:i+1], y1[:i+1])
    line2.set_data(t[:i+1], y2[:i+1])
    line3.set_data(t[:i+1], y3[:i+1])

#==============================================================================
#-------------------------- Exécution du programme ----------------------------
#==============================================================================

if __name__ == "__main__":

    sondeData =  pd.read_csv("RESAMPLED_line_probes.csv")
    
    t  = sondeData["time"]
    y1 = sondeData["S1-1.0"]
    y2 = sondeData["S2-2.0"]
    y3 = sondeData["S3-3.0"]
    
    fig, ax = plt.subplots()

    ax.set_xlim((0,10))
    ax.set_ylim((0.7,1))
    
    line1, line2, line3 = ax.plot(t[0], y1[0], t[0], y2[0], t[0], y3[0])
    
    ani = animation.FuncAnimation(fig, animate, frames=100,
                                  fargs=(line1, line2, line3, t, y1, y2, y3), 
                                  interval = 100, repeat = False)