#!/usr/bin/env python3

"""
Lecture des fichiers sondes dans les fichiers postProcessing/line
"""

import os
from pandas import read_csv, DataFrame
import outilsLecture as olec
import sys

def debit_franchissement(volume, largeur, echelle, temps):
    """Calcule le débit de franchissement
    
    :param volume: Volume d'eau dans le bac
    :type volume: float
    :param largeur: Largeur du bac
    :type largeur: float
    :param echelle: Echelle de transformation vers débit réel
    :type echelle: float
    :param temps: Temps de simulation
    :type temps: float
    """
    
    return  volume/temps/largeur * echelle**(1.5) * 1000


if __name__ == "__main__":

    #==========================================================================
    #------------------- Lecture des options ----------------------------------
    #==========================================================================

    # Largeur du canal
    largeur  = olec.readValueOption(sys.argv, ["-largeur","--largeur"],
                                      default = 1.0)

    print("Largeur du canal :", largeur)

    # Fichier de sortie
    outputFile = olec.readFileOption(sys.argv, ["-output","--output",
                                                "-outputFile","--outputFile"],
                                    default = "test.csv",
                                    extension = "csv")
    
    # Chemin vers fichier de volumes
    path = olec.readFileOption(sys.argv, ["-path","--path"],
                               default = "volFieldValue.dat",
                               checkPath = True)
    
    # Lire échelle dans le fichier jonswapDict si il existe                   
    if os.path.exists("jonswapDict"):
        with open('jonswapDict', 'r') as f:
            for line in f.readlines():
                if line.split()[0] == "scale" or line.split()[0] == "echelle":
                    echelle = float(line.split()[1])
                    print("Echelle : {}".format(echelle))
                    
    # Sinon lire la valeur 1 par défaut
    else:
        echelle = olec.readValueOption(sys.argv, ["-echelle","--echelle",
                                                 "-scale","--scale"],
                                       default = 1.0)
                                       

    print("Echelle", echelle)

    #==========================================================================
    #------------------- Lecture dans mesures de volume OpenFOAM---------------
    #==========================================================================

    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} n'existe pas, veuillez préciser un \
                                fichier source avec l'option \n --path <path>")
                         
    data = read_csv(path, header = 4, delimiter = "\t")
    temps = data.iloc[:,0]
    volumes = data.iloc[:,1]
    
    debits = debit_franchissement(volumes, largeur, echelle, temps)
    
    print("Débit de franchissement maximal : {}".format(max(debits)))
    
    df = DataFrame(data = [temps, volumes, debits]).transpose()
    df.columns = ["Temps", "Volume (m³)", "Debit (L/s/m)"]
    
    df.set_index("Temps").to_csv(outputFile)

