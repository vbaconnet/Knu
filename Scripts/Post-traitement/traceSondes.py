#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Informations
-------------

* Fichier : ``Knu/Scripts/Post-traitement/traceSondes.py``
* Auteur : Victor Baconnet
* Dernière modification le : 30/08/2021

Description
------------

Tracer des données à partir d'un fichier .csv, avec en première colonne le 
signal temporel. Trace toutes les valeurs sur le même graphique. 

.. NOTE::

    Pour un affichage de graphiques détaillé, consultez les fonctions 
    disponibles dans :doc:`outilsExcel</fonctions/outilsExcel>` pour
    exporter vos valeurs vers Excel et générer des graphiques 
    automatiquement

Utilisation
------------

.. code-block:: bash

    $ traceSondes.py <fichier>

``<fichier>`` doit être au format ``.csv``, et doit être formaté comme 
le modèle suivant:

.. code-block:: none

    temps,nom_1,nom_2,...,nom_N
    t_1,val_11,val_12,...,val_1N
    ...
    t_N,val_M1,val_M2,...,val_MN

En résumé, les données sont organisées en colonnes, et la première
doit être un vecteur de temps.

Code source
------------

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Post-traitement/traceSondes.py>`_

"""

import numpy as np
import pandas as pd
from matplotlib.pyplot import subplots, show
import matplotlib.animation as animation
from outilsDivers import plot
import sys
from os.path import exists

if __name__ == "__main__":

    probefile = sys.argv[1]

    if probefile == "":
        raise ValueError("Précisez un fichier dans lequel lire!")

    if not exists(probefile):
        raise FileNotFoundError("Fichier {} inexistant")

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
