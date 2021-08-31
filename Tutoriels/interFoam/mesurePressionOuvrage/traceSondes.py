#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tracer des données à partir d'un fichier .csv, avec
en première colonne le signal temporel.

Trace tout sur le même graphique.
"""

import numpy as np
import pandas as pd
from matplotlib.pyplot import subplots, show
import matplotlib.animation as animation
from outilsDivers import plot
from outilsLecture import readFileOption
import sys

if __name__ == "__main__":

    probefile = readFileOption(sys.argv, ["-probefile","--probefile"],
				   default = "line_probes.csv",
			           checkPath = True)

    print("Probefile : {}".format(probefile))
    sondeData =  pd.read_csv(probefile)

    cols = []

    for idx,col in enumerate(sondeData.columns):
        cols.append(sondeData.iloc[:,idx])

    fig, ax = subplots()

    for i in range(1,len(cols)-1):
        plot(cols[0], cols[i], fig, ax, label = sondeData.columns[i],
      	     tight_layout = False, grid = True)

    plot(cols[0], cols[-1], fig, ax, label = sondeData.columns[-1],
	 tight_layout = True, xlabel = "Temps (s)")

    show()
