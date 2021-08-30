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

    sondeData =  pd.read_csv("line_probes.csv")
    
    t  = sondeData.iloc[:,0]
    y1 = sondeData.iloc[:,1]
    y2 = sondeData.iloc[:,2]
    y3 = sondeData.iloc[:,3]
    
    fig, ax = plt.subplots()

    ax.set_xlim((0,10))
    ax.set_ylim((0.7,1))
    
    ax.plot(t, y1, label = sondeData.columns[1])
    ax.plot(t, y2, label = sondeData.columns[2])
    ax.plot(t, y3, label = sondeData.columns[3])

    plt.legend()
    plt.grid()
    plt.show()
