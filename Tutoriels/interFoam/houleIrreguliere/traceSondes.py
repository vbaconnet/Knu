#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 09:23:49 2021

@author: vbaconnet
"""

import numpy as np
import pandas as pd
from matplotlib.pyplot import subplots, show
import matplotlib.animation as animation
from outilsDivers import plot


if __name__ == "__main__":

    sondeData =  pd.read_csv("line_probes.csv")

    t  = sondeData.iloc[:,0]
    y1 = sondeData.iloc[:,1]
    y2 = sondeData.iloc[:,2]
    y3 = sondeData.iloc[:,3]

    ax.set_xlim((0,10))
    ax.set_ylim((0.7,1))

    plot(t, y1, fig, ax, label = sondeData.columns[1],
	 tight_layout = False)

    plot(t, y2, fig, ax, label = sondeData.columns[2],
	 tight_layout = False)

    plot(t, y3, fig, ax, label = sondeData.columns[3],
	 tight_layout = True, xmin = 0.0, xmax = max(t),
	 ymin = 0.7, ymax = 1, xlabel = "Temps (s)",
	 ylabel = r"$\eta(t)$")

    show()
