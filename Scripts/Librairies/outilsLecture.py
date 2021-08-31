"""
Informations
============

* Fichier: ``Knu/Scripts/Librairies/outilsLecture.py``
* Auteur: Victor Baconnet
* Date de dernière modification: 27 août 2021

Description
===========

Liste de fonctions permettant de lire des options données par l'utilisateur.

Ces fonctions permettent de lire les options, avec plusieurs syntaxes possibles. 
Si l'option n'est pas trouvée, une valeur par défaut peut être donnée. 

Exemple d'utilisation
======================

.. code-block:: python
    
    import outilsLecture as olec
    import numpy as np
    import sys
    
    tmax = olec.readValueOption(sys.argv, ["-tmax","--tmax"],
                                default = 0.0)
    
    N = olec.readValueOption(sys.argv, ["-N","--N"],
                             default = 100, valueType = int)
    
    file = olec.readFileOption(sys.argv, ["--file", "-file"],
                                     default = "out.csv", extension = "csv")
    
    print("Tmax : ", tmax)
    print("N    : ", N)
    print("file : ", file)

Executions possibles:

.. code-block:: bash
    
    $ python3 myscript.py
    Tmax : 0.0
    N    : 100
    file : out.csv
    
    $ python3 myscript.py --tmax 20.0 --N 41 -file wrongfile.csv
    Tmax : 20.0
    N    : 41
    file : wrongfile.csv
    
.. WARNING :: 
    
    Dans le dernier exemple, si l'utilisateur avait précisé ``wrongfile.txt``,
    le programme aurait renvoyé une erreur.

Code source
============

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Librairies/outilsLecture.py>`_

Fonctions
=========

"""

def readFileOption(options, possibleNames, default, extension = "", checkPath = False):
    """Lecture d'option au format : -fichier <nom_fichier> 
    
    :param options: Liste des options données par l'utilisateur
    :type options: list
    :param possibleNames: Liste des options acceptées pour sélectionner ce 
      paramètre (exemple: ["-file", "--file", "-File"])
    :type possibleNames: list
    :param default: Valeur prise par défaut
    :type default: string
    :param extension: extension du fichier (exemple: "csv")
    :type extension: string
    :return: filename : le nom du fichier donné en paramètre, sinon renvoie default
    :rtype: string
    """
    
    from os.path import exists
    
    filename = default
    
    for idx, opt in enumerate(options): #Parcourir les options
        
        #Si l'option donnée est trouvée parmi les noms possibles
        if opt in possibleNames: 
        
            try:
                #On regarde le paramètres d'après
                filename = options[idx+1]   
                
                #Si il commence par un "-" c'est qu'il n'y a pas de nom associé
                #et qu'on a directement donné une nouvelle option
                if filename[0] == "-":  
                    
                    raise ValueError("L'option {} n'a pas de nom associé. \
                                     Veillez à bien préciser le nom du fichier \
                                         après l'option".format(opt))
                                         
                print("{} défini à {}".format(opt,filename))
            
            #Dans ce cas, on n'a pas pu récupérer le paramètre d'après
            except: 
                raise ValueError("{} n'a pas de nom associé.".format(opt))
    
    #Est-ce que l'extension est la bonne?
    if extension not in filename.split(".")[-1] and extension != '':  
        raise ValueError("L'extension .{} n'est pas valide. Extension .{} \
                         attendue".format(filename.split(".")[-1], extension))
                   
    return filename

def readValueOption(options, possibleNames, default, valueType = float):
    """Lecture d'option au format : -parametre <valeur> 
    
    :param options: Liste des options données par l'utilisateur
    :type options: list
    :param possibleNames: Liste des options acceptées pour sélectionner ce paramètre (exemple: ["-val", "--val", "-VAL"])
    :type possibleNames: list
    :param default: Valeur prise par défaut
    :type default: string
    :param valueType: type de la valeur à lire (int, float)
    :type valueType: type
    :return: filename : la valeur donnée en paramètre, sinon renvoie default
    :rtype: valueType
    """
    
    value = default
    
    for idx, opt in enumerate(options):        
    
        if options[idx] in possibleNames:        
            try:
                value = valueType(options[idx+1])
                print("{} définie à {}".format(opt,value))

            except:
                raise ValueError("Un des paramètres n'a pas été donné. Veillez \
                                 à bien préciser la valeur de la variable que \
                                     vous souhaitez définir")
            
    return value

def readDirOption(options, possibleNames, default):
    """Lecture d'option au format : -repertoire <nom-repertoire> 
    
    :param options: Liste des options données par l'utilisateur
    :type options: list
    :param possibleNames: Liste des options acceptées pour sélectionner ce paramètre (exemple: ["-dir", "--dir", "-DIR"])
    :type possibleNames: list
    :param default: Valeur prise par défaut
    :type default: string
    :return: path : le nom du répertoire donné en paramètre, sinon renvoie default
    :rtype: string
    """
    
    path = default
    
    for idx, opt in enumerate(options):        
    
        if options[idx] in possibleNames:        
            try:
                path = options[idx+1]
                
                #Si il commence par un "-" c'est qu'il n'y a pas de nom associé
                #et qu'on a directement donné une nouvelle option
                if path[0] == "-":  
                    raise ValueError("L'option {} n'a pas de nom associé."\
                                     .format(opt))
                print("{} défini à {}".format(opt,path))

            except:
                    raise ValueError("L'option {} n'a pas de nom associé."\
                                     .format(opt))
            
    return path

def readOption(options, possibleNames):
    """Lecture d'option seule
    
    :param options: Liste des options données par l'utilisateur
    :type options: list
    :param possibleNames: Liste des options acceptées pour sélectionner ce paramètre (exemple: ["-doThing", "--doThing", "-DOTHING"])
    :type possibleNames: list
    :return: True si l'option est trouvée, False sinon
    :rtype: bool
    """
    for name in possibleNames:
        if name in options:
            print("{} trouvé".format(name))
            return True
    
    return False
