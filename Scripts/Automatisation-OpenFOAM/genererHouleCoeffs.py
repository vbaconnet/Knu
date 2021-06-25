"""
Informations
============

* Auteur: Victor Baconnet
    
* Date de dernière modification: 31 mai 2021

Description
===========

Génère le fichier ``constant/waveProperties`` contenant les paramètres et coefficients 
d'amplitude, périodes, déphasages et directions pour le patch inlet, et des 
paramètres d'absoroption pour le patch outlet

Utilisation
===========

Pour exécuter ce fichier, vous devez spécifier les paramètres de spectre JONSWAP
dans le fichier "jonswapDict" formaté comme suit::
    
  Tp 1.78
  Tmin 1.0
  Tmax 3.0
  Hs 1.5
  gamma 3.2
  scale (ou échelle) 25.0 //optionnel
    
L'exécution de ce fichier renverra une erreur si ``jonswapDict`` n'est pas trouvé.
Vous pouvez, si besoin, préciser le chemin d'accès vers le fichier de votre 
choix avec l'option ``--jonswapFile``.

Le fichier de sortie ``waveProperties`` sera créé dans le répertoire ``constant``
si il existe, ou directement dans le répertoire courant. Vous pouvez, si besoin,
préciser le chemin d'accès vers le répertoire de votre choix avec l'option 
``--wavePropertiesPath``.

Options d'exécution:
====================

--wavePropertiesPath path         chemin d'accès vers le répertoire d'écriture
                                  du fichier waveProperties    
--jonswapFile file                chemin d'accès vers le fichier contenant les 
                                  paramètres de spectre JONSWAP                                 
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

    
Dépendances
===========

* Pour l'utilisation des fonctions uniquement: ``numpy``
    
* Pour exécuter le fichier : ``numpy``, ``sys``, ``jonswap``, ``outilsLecture``, 
  ``os``

Fonctions
=========
"""

import numpy as np

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
    
def writeMatrix(f, name, matrix):
    """Ecrit une matrice avec son nom associé, au format::
        
          nom
          nombre de lignes
          (
          valeurs
          );
    
    :param f: Nom du fichier d'écriture
    :type f: ``string``
    :param name: Nom du paramètre (waveHeights, wavePeriods...)
    :type name: ``string``
    :param matrix: Matrice de valeurs. Peut être un vecteur COLONNE ou une matrice
    :type matrix: ``numpy.ndarray``
    """
        
    try:   #Si matrix est 3D, aucun souci, on récupère le nombre de colonnes
        
        Nj = matrix.shape[1]
    
    except:  #Dans ce cas il faut reshape car matrix est un vecteur
    
        matrix = matrix.reshape( (len(matrix),1) )
        Nj = 1
        
    Ni = len(matrix)   # Nombre de lignes
    f.write("    "+name+"\n    "+str(Ni)+"\n    (\n")
            
    for i in range(Ni):
        temp = "("
        for j in range(Nj-1):
            temp += str(matrix[i,j]) + " "
        temp += str(matrix[i,Nj-1]) + ")\n"
        f.write(temp)
            
    f.write("    );\n\n")


def writeInlet(f, inletParamsDict, inletWaveParamsDict, inletName = "inlet"):
    """Ecrit les paramètres pour le patch "inlet"
    
    :param f: Nom du fichier d'écriture
    :type f: ``string``
    :param inletParamsDict: Dictionnaire contenant les paramètres "simples" au
        format ``{nom => valeur}``
    :type inletParamsDict: ``dict``
    :param inletWaveParamsDict: Dictionnaire contenant les composantes d'un 
        paramètre (waveHeights, wavePeriods...)
    :type inletParamsDict: ``dict``
    :param inletName: Nom du patch inlet
    :type inletName: ``string``
    """
    
    f.write('\n'+inletName+'\n{\n')
    writeParam(f, inletParamsDict)
    f.write('\n')
    
    for waveName, waveData in inletWaveParamsDict.items():
        writeMatrix(f, waveName, waveData)
        
    f.write("}\n")
    
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
    :return: Tmin, Tmax, Tp, Hs, gamma les paramètres donnés dans le fichier ``filename``
    :rtype: ``float``    
    """
    
    param_dict          = dict()
    param_dict["tmin"]  = None
    param_dict["tmax"]  = None
    param_dict["tp"]    = None
    param_dict["hs"]    = None
    param_dict["gamma"] = None
    param_dict["scale"] = None
    
    with open(filename,"r") as f:
        
        entries = f.readlines()
        
        print("\nParamètres du fichier {} :".format(filename))
        print(  "----------------------" + "-"*len(filename) + "--")
        
        for entry in entries:
            
            temp = entry.split()
            name = temp[0].lower()
            value = float(temp[1])
            
            try:
                param_dict[name] = value
                print("{} : {:.3}".format(name.capitalize(),value))
            except KeyError:
                print("Paramètre non reconnu : {}".format(name))

        f.close()

    #Si une des valeurs est None, il manque des paramètres
    if None in param_dict.values():
        
        missing_vals = []
        for key, value in param_dict.items():
            if value is None:
                missing_vals.append(key)
            
        raise ValueError("Il manque des paramètres pour le spectre JONSWAP. \
                         Paramètre manquants : {}".format(missing_vals))

    #Si les paramètres ne sont pas tous spécifiés, renverra une erreur!
    if abs(param_dict["scale"] - 1.0) > 0.00001 : #si l'échelle est différente de 1

        param_dict["tmin"] /= np.sqrt(param_dict["scale"] )
        param_dict["tmax"] /= np.sqrt(param_dict["scale"] )
        param_dict["tp"]   /= np.sqrt(param_dict["scale"] )
        param_dict["hs"]   /= param_dict["scale"] 
        print("\nParamètres à l'échelle {} :".format(param_dict["scale"] ))
        print(  "-----------------------"+"-" * ( len(str(param_dict["scale"] ))+2 ) )
        
        for name, value in param_dict.items():
            print("{} : {:.3}".format(name.capitalize(),value))
            
    return param_dict


#-----------------------------------------------------------------------------
#                               MAIN
#-----------------------------------------------------------------------------

if __name__  == "__main__":
    
    print("genWaveProperties is main")
    
    #------- ces modules sont indispensables ----------------------------------
    import outilsLecture as olec
    import jonswap as jswp
    import sys
    import os
    #--------------------------------------------------------------------------
    
    #----------------- Lecture des options d'éxecution ------------------------
    
    wavePropertiesPath  = olec.readDirOption(sys.argv,
                                             ["-wavePropertiesPath","--wavePropertiesPath"],
                                             default = ".")
    
    jonswapFile = olec.readFileOption(sys.argv,
                                       ["-jonswapFile","--jonswapFile"],
                                       default = "jonswapDict")  
    
    inletName = olec.readValueOption(sys.argv,
                                     ['-inlet','--inlet'],
                                     default = 'inlet',
                                     valueType = str)
    
    outletName = olec.readValueOption(sys.argv,
                                      ['-outlet','--outlet'],
                                      default = 'outlet',
                                      valueType = str)
    
    noOutlet = olec.readOption(sys.argv,
                               ['-noOutlet'])
    
    rampTime = olec.readValueOption(sys.argv,
                                    ['-rampTime'],
                                    default = 2.0,
                                    valueType = float)
    
    nPaddle = olec.readValueOption(sys.argv,
                                   ['-nPaddle'],
                                   default = 1,
                                   valueType = int)
    
    Ncomposantes = olec.readValueOption(sys.argv, ['-n','--Ncomposantes','-Ncomposantes','-N'],
                                    default = 600,
                                    valueType = int)
    
    writeCsv = olec.readOption(sys.argv,
                               ["-writeCsv", "--writeCsv"])
    
    csvFileName  = olec.readFileOption(sys.argv,
                                       ["-csvFile", "--csvFile"],
                                       default = "waveProperties.csv")
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
    #On vérifie si le chemin donné existe, sinon on se met dans le dossier courant
    if os.path.exists("constant"):
        print("constant directory located")
        wavePropertiesPath = "constant"

    wavePropertiesPath = os.path.join(wavePropertiesPath, "waveProperties")

    print("\nCreating waveProperties in {}".format(wavePropertiesPath))
    print("Reading parameters from {}".format(jonswapFile))
    
    # ---------------- Paramètres inlet --------------------------------------   
    
    #Absorption active sur le batteur? Permet d'absorber la houle réfléchie
    #sur l'ouvrage pour ne pas générer trop d'ondes stationnaires
    activeAbsorption = "no"
    
    #Paramètres du patch inlet
    inletParamDict = {"alpha"           : "alpha.water",
                      "waveModel"       : "irregularMultiDirectional",
                      "nPaddle"         : nPaddle,
                      "rampTime"        : rampTime,
                      "activeAbsorption": activeAbsorption,
                      }
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #---------------------------- Génération JONSWAP -------------------------
    
    #Lecture des paramètres donnés dans jonswapDict
    param_dict = readParams(jonswapFile)
    
    Tmin,Tmax,Tp = param_dict["tmin"], param_dict["tmax"], param_dict["tp"]
    Hs,gamma = param_dict["hs"],param_dict["gamma"]
    
    wmax     = 2.0*np.pi/Tmin                   #Fréquence min
    wmin     = 2.0*np.pi/Tmax                   #Fréquence max
    wp       = 2.0*np.pi/Tp                     #Pulsation pic 
    dw       = (wmax-wmin)/(Ncomposantes-1)          #Incrément de fréquence
    w        = np.linspace(wmin,wmax,Ncomposantes)   #Génération du vecteur de fréquences
    periodes = 2.0*np.pi/w                      #Périodes T = 2pi/w

    #Génération des amplitudes et déphasages
    amplitudes, dephasages, spectre = jswp.genJonswapParams(Hs, Tp, gamma, w)
    
    #Directions [0 0 0 0 ... 0] en 2D
    directions = np.zeros(len(amplitudes))
    
    #Dictionnaire qui contient toutes les composantes 
    inletWaveParamsDict = {"wavePeriods" : periodes,
                           "waveHeights" : 2.0*amplitudes, #!! Multiplication par 2 car hauteur = 2*amplitude !!
                           "wavePhases"  : dephasages,
                           "waveDirs"    : directions
                           }
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #-------------------------------- paramètres outlet --------------------------
    
    #Nombre de batteurs. En 2D doit être = 1
    nPaddle = 1
    
    #Paramètres du patch outlet 
    outletParamsDict = {"alpha"     : "alpha.water",
                        "waveModel" : "shallowWaterAbsorption",
                        "nPaddle"   : nPaddle}
    
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #---------------------- Ecriture dans le fichier waveProperties --------------
        
    wavePropertiesFile = open(wavePropertiesPath,"w")
    print("Writing header...")
    writeHeader(wavePropertiesFile)
    print("Done. \nWriting inlet parameters...")
    writeInlet(wavePropertiesFile, inletParamDict, inletWaveParamsDict, inletName = inletName)
    print("Done.")
    
    if not(noOutlet):
        print("Writing outlet parameters...")
        writeOutlet(wavePropertiesFile, outletParamsDict, outletName = outletName)
        print("Done.")
        
    wavePropertiesFile.close()
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    #---------------------------- Ecriture dans le fichier csv -------------------
    
    if writeCsv:
        
        csvFile = open(csvFileName, "w")
        
        print("wavePeriods,waveHeights,wavePhases,waveDirs", file = csvFile)
        
        for n in range(Ncomposantes):
            for key, value in inletWaveParamsDict.items():
                if key != "waveDirs":
                    endLine = ","
                else:
                    endLine = "\n"
                
                print(value[n], file =  csvFile, end = endLine)
                
        
        csvFile.close()
    #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
