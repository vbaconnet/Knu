#!/usr/bin/env python3
"""
Informations
============

* Auteur: Victor Baconnet
    
* Date de dernière modification: 08 Juillet 2021

Description
===========

Génère le fichier ``constant/waveProperties`` contenant les paramètres et coefficients 
d'amplitude, périodes, déphasages et directions pour le patch inlet, et des 
paramètres d'absorption pour le patch outlet.

La génération peut se faire selon la syntaxe interFoam/interIsoFoam ou olaFlow, 
toujours à partir du fichier ``constant/regularWaveDict``.

Pour exécuter ce fichier, vous devez spécifier les paramètres de houle régulière
comme suit::
    
  T 1.78
  H 1.0
    
L'exécution de ce fichier renverra une erreur si ``regularWaveDict`` n'est pas trouvé.
Vous pouvez, si besoin, préciser le chemin d'accès vers le fichier de votre 
choix avec l'option ``--waveDict``.

Le fichier de sortie ``waveProperties`` sera créé dans le répertoire ``constant``
si il existe, ou directement dans le répertoire courant. Vous pouvez, si besoin,
préciser le chemin d'accès vers le répertoire de votre choix avec l'option 
``--wavePropertiesPath``.

Utilisation
===========

genWaveProperties [OPTIONS]

Options
-------

-h, --help                        Afficher l'aide
--wavePropertiesPath path         chemin d'accès vers le répertoire d'écriture
                                  du fichier waveProperties    
--waveDict file                   chemin d'accès vers le fichier contenant les 
                                  paramètres de houle régulière                                
--inlet inletName                 Spécifie le nom du patch inlet (là où la houle
                                  sera générée).
--outlet outletName               Spécifie le nom du patch outlet
--noOutlet                        ne pas créer de patch outlet
--rampTime value                  Spécifier la valeur de rampTime (temps 
                                  d'amortissement) 
--nPaddle value                   Spécifier le nombre de batteurs en entrée 
--Ncomposantes value              nombre de composantes de chaque paramètre (
                                  hauteurs, périodes, déphasages...)    
--writeCsv                        Ecrit les hauteurs, déphasages, périodes et 
                                  directions
                                  dans un fichier au format ".csv". Cette 
                                  option est indispensable si vous 
                                  souhaitez utiliser le script ``traceInterface.py``.
--csvFileName file                nom du fichier ".csv" où écrire les composantes
                                  de hauteur, périodes, déphasages, et direction.
                                  N'est prise en compte uniquement si ``--writeCsv``
                                  est activée.
--solver solver                   Nom du solveur utilisé pour le formatage du 
                                  fichier waveProperties

    
Dépendances
===========

* Pour l'utilisation des fonctions uniquement: ``numpy``
    
* Pour exécuter le fichier : ``numpy``, ``sys``, ``outilsLecture``, 
  ``os``

Fonctions
=========
"""

def writeHeader(f):
    """Ecrit le header OpenFOAM
    
    :param f: Nom du fichier d'écriture
    :type f: ``string``
    """
        
    header = ["/*---------------------------------------------------------------------------*\\",
              "| =========                 |                                                 |",
              "| \\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |",
              "|  \\\    /   O peration     | Version:  v2006                                 |",
              "|   \\\  /    A nd           | Website:  www.openfoam.com                      |",
              "|    \\\/     M anipulation  |                                                 |",
              "\*---------------------------------------------------------------------------*/",
              "FoamFile","{","    version     2.0;","    format      ascii;",
              "    class       dictionary;",'    location    "constant";',
              "    object      waveProperties;","}",
              "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //"]
    
    for txt in header:
        f.write(txt+'\n')
    return

def writeParam(f, paramDict):
    """Ecrit des paramètres simples au format ``<nom>   valeur>;``
    
    :param f: Nom du fichier d'écriture
    :type f: ``string``
    :param paramDict: Dictionnaire de paramètres ``{"nom" => valeur}``
    :type paramDict: ``dict``
    """
    for name in paramDict.keys():
        f.write("\n    " + name + " "*(17-len(name)) + str(paramDict[name]) + ";\n")
    

def writeInlet(f, inletParamsDict, solver, inletName = "inlet"):
    """Ecrit les paramètres pour le patch "inlet" selon la syntaxe interFoam/
        interIsoFoam ou olaFlow
    
    :param f: Nom du fichier d'écriture
    :type f: ``string``
    :param inletParamsDict: Dictionnaire contenant les paramètres "simples" au
        format ``{nom => valeur}``
    :type inletParamsDict: ``dict``
    :param solver: Type de solveur utilisé dans ``system/controlDict``
    :type solver: ``str``
    :param inletName: Nom du patch inlet
    :type inletName: ``string``
    """
    
    # Si on est pas dans olaFlow ou olaIsoFlow, on écrit syntaxe interFoam
    if solver != "olaFlow" and solver != "olaIsoFlow":
        f.write('\n'+inletName+'\n{\n')
        writeParam(f, inletParamsDict)
        f.write('\n')
        f.write("}\n")
    
    # Sinon, syntaxe olaFlow
    else:
        writeParam(f, inletParamsDict)
        f.write('\n')
    
def writeOutlet(f, outletParamsDict, outletName = "outlet"):
    """Ecrit les paramètres correspondant au patch "outlet"
    
    :param f: Nom du fichier d'écriture
    :type f: ``string``
    :param outletParamsDict: Dictionnaire contenant les paramètres "simples" au format {nom => valeur}
    :type outletParamsDict: ``dict``
    :param outletName: Nom du patch outlet
    :type outletName: ``string``
    """
    
    f.write('\n'+outletName+'\n{\n')
    writeParam(f, outletParamsDict)
    f.write("}\n")

def readParams(filename = "jonswapDict"):
    """Lire les paramètres Tp, Hs etc dans le fichier de paramètres jonswap
    
    :param filename: nom du fichier de paramètres
    :type filename: ``string``
    :raises ValueError: Si il manque un paramètre dans le fichier ``filename``, 
        renverra une erreur.
    :return: ``param_dict`` dictionnaire contenant les paramètres donnés dans 
        le fichier ``filename``.
    :rtype: ``dict(float)``    
    """

    param_dict          = dict()
    param_dict["wavePeriod"]  = None
    param_dict["waveHeight"]  = None
    param_dict["waveAngle"]    = 0.0
    param_dict["rampTime"]    = 2.0
    param_dict["nPaddle"] = 1
    param_dict["activeAbsorption"] = "no"
    
    with open(filename,"r") as f:
        
        entries = f.readlines()  # Lire dans le fichier waveDict
        print("\nParamètres du fichier {} :".format(filename))
        print(  "----------------------" + "-"*len(filename) + "--")
        
        for entry in entries: # Parcourir chaque ligne du fichier
            
            temp = entry.split() # Split pour récupérer proprement les valeurs
            
            name = temp[0] # en [0], c'est le nom du paramètre
            if name == "nPaddles":
                value = int(temp[1])
            elif name  == "activeAbsorption":
                value = str(temp[1])
            else:
                value = float(temp[1]) # en [1] c'est sa valeur
                
            # On ne prend pas en compte les paramètres après ([2], [3]...)
            # --> Possibilité de rajouter des commentaires dans jonswapDict
            
            try:  # Essayer d'assigner un paramètre du dictionnaire
                param_dict[name] = value
                print("{} : {:.3}".format(name,value))

            except KeyError: # Si marche pas, paramètre non reconnnu
                print("Paramètre non reconnu : {}".format(name))


    #Si une des valeurs est None, il manque des paramètres
    if None in param_dict.values():
        
        missing_vals = []  # Va stocker les valeur manquantes

        for key, value in param_dict.items():
            if value is None:
                missing_vals.append(key)
            
        raise ValueError("Il manque des paramètres pour le spectre JONSWAP. \
Paramètres manquants : {}".format(missing_vals))
            
    return param_dict

def help_message():
    """Affiche le messge d'aide
    """
    warning("L'aide détaillée est rédigée en en-tête du fichier")
    print("genWaveProperties. Vous pouvez consulter l'aide directement")
    print("en ouvrant le fichier situé dans\n")
    print("   Knu/Scripts/Automatisation-OpenFOAM/genWaveProperties\n")
    print("ou en lisant la documentation qui vous a été fournie")
    print("\n")
    print("Aide rapide")
    print("-----------")
    print("Utilisation : [options] --inlet <inlet> --outlet <outlet>")
    print("              --jonswapDict <dict> --wavePropertiesPath <path>")
    print("              --csvFileName <name> --rampTime <time> ")
    print("              --Ncomposantes <N> --nPaddle <Npaddle>")
    print("\nOptions\n-------")
    print("  -h, --help : afficher cette aide")
    print("  --noOutlet : pas d'outlet")
    print("  --writeCsv : ecrire fichier csv avec composantes")
    print("\n")
    print("Si besoin : victor.baconnet@acri-in.fr\n")

#-----------------------------------------------------------------------------
#                               MAIN
#-----------------------------------------------------------------------------

if __name__  == "__main__":
    
    print("genWaveProperties is main")
    
    #------- ces modules sont indispensables ----------------------------------
    import outilsLecture as olec
    from outilsDivers import warning
    import sys
    import os
    #--------------------------------------------------------------------------
    
    #----------------- Lecture des options d'éxecution ------------------------
    
    send_help = olec.readOption(sys.argv,
                                ['-h','--help','-help'])

    if send_help :
        help_message()
        exit()

    solver = olec.readValueOption(sys.argv,
                                  ["-solver","--solver"],
                                  default = "interFoam",
                                  valueType = str)

    wavePropertiesPath  = olec.readDirOption(sys.argv,
                                             ["-wavePropertiesPath","--wavePropertiesPath"],
                                             default = ".")
    
    waveDict = olec.readFileOption(sys.argv,
                                       ["-waveDict","--waveDict"],
                                       default = "regularWaveDict")  
    
    inletName = olec.readValueOption(sys.argv,
                                     ['-inlet','--inlet'],
                                     default = 'inlet',
                                     valueType = str)
    
    outletName = olec.readValueOption(sys.argv,
                                      ['-outlet','--outlet'],
                                      default = 'outlet',
                                      valueType = str)
    
    noOutlet = olec.readOption(sys.argv,
                               ['-noOutlet', '--noOutlet'])
    
    # Si on est en olaFlow ne pas afficher d'outlet
    if solver == "olaFlow" or solver == "olaIsoFlow":
        warning("olaFlow detected : no outlet printed")
        noOutlet = True
        
        
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    #On vérifie si le chemin donné existe, sinon on se met dans le dossier courant
    if os.path.exists("constant"):
        print("constant directory located")
        wavePropertiesPath = "constant"

    wavePropertiesPath = os.path.join(wavePropertiesPath, "waveProperties")

    print("\nCreating waveProperties in {}".format(wavePropertiesPath))
    print("Reading parameters from {}".format(waveDict))
    
    # ---------------- Paramètres inlet --------------------------------------   
    
    #Lecture des paramètres donnés dans jonswapDict
    param_dict = readParams(waveDict)
    nPaddle = param_dict["nPaddle"]
    rampTime = param_dict["rampTime"]
    T = param_dict["wavePeriod"]
    H = param_dict["waveHeight"]
    angle = param_dict["waveAngle"]
    activeAbsorption = param_dict["activeAbsorption"]
    
    #Absorption active sur le batteur? Permet d'absorber la houle réfléchie
    #sur l'ouvrage pour ne pas générer trop d'ondes stationnaires
    
    #Paramètres du patch inlet
    inletParamDict = {"alpha"           : "alpha.water",
                      "waveModel"       : "StokesI",
                      "nPaddle"         : nPaddle,
                      "rampTime"        : rampTime,
                      "activeAbsorption": activeAbsorption,
                      "waveHeight"      : H,
                      "wavePeriod"      : T,
                      "waveAngle"       : angle
                      } if solver != "olaFlow" else {
                        "waveType"       : "irregular",
                        "genAbs"         : 1,
                        "absDir"         : 0.0,
                        "nPaddles"       : nPaddle,
                        "tSmooth"        : rampTime 
                        }

    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    #-------------------------------- paramètres outlet --------------------------
    
    #Paramètres du patch outlet 
    outletParamsDict = {"alpha"     : "alpha.water",
                        "waveModel" : "shallowWaterAbsorption",
                        "nPaddle"   : nPaddle}
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #---------------------- Ecriture dans le fichier waveProperties --------------
        
    wavePropertiesFile = open(wavePropertiesPath,"w")
    print("Writing header...")
    writeHeader(wavePropertiesFile)   # Ecrire le header
    print("Done. \nWriting inlet parameters...")

    # Ecrire les composantes dans patch inlet
    # si interFoam ou interIsoFoam, ou dans le dict associé pour olaFlow
    writeInlet(wavePropertiesFile,  
                inletParamDict,
                solver,
                inletName = inletName)

    print("Done.")
    
    if not(noOutlet):
        print("Writing outlet parameters...")
        writeOutlet(wavePropertiesFile, outletParamsDict, outletName = outletName)
        print("Done.")
        
    wavePropertiesFile.close()
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++