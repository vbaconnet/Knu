"""
Description
===========

Liste de fonctions permettant de lire des options données par l'utilisateur.

Ces fonctions permettent de lire les options, avec plusieurs syntaxes possibles. 
Si l'option n'est pas trouvée, une valeur par défaut peut être donnée. 

Les fonctions ne vérifient pas l'existence, ou la validité des 
valeurs données par l'utilisateur.


Fonctions
=========

"""

def readFileOption(options, possibleNames, default, extension = "", checkPath = False):
    """Lecture d'option au format : -fichier <nom_fichier> 
    
    :param options: Liste des options données par l'utilisateur
    :type options: list
    :param possibleNames: Liste des options acceptées pour sélectionner ce paramètre (exemple: ["-file", "--file", "-File"])
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

def userInputChoice(listOfOptions, offset = "", retour = None):
    """Lecture de choix utilisateur parmi une liste d'options
    
    :param listOfOptions: Liste des choix possibles
    :type listOfOptions: ``list``
    :param expectedType: Type de choix à lire
    :param expectedType: ``type``
    :return: 
          * Si le choix est dans la liste des options possibles, retourne
            le choix et ``True``
          * Si le choix n'est  pas dans la liste des options possibles, retourne
            le choix et ``False``
        
    """
    
    #Liste des choix possible, initialisée avec le choix par défaut 0. Cette
    #liste va contenir [0,1,2...,N] avec N le nombre d'éléments dans listOfOptions
    possibleChoices = [0]   
    
    #Afficher les possibilités
    print("\n" + offset + "Que voulez-vous faire?\n")
    for idx, option in enumerate(listOfOptions):
        print(offset + "  {}. ".format(idx+1) + option)
        possibleChoices.append(idx+1)

    #Afficher l'option par défaut
    if retour:
        print(offset + "  0. Retour")
    elif not retour:
        print(offset + "  0. Quitter")
    
    while True:
    
        rawChoice = input("\n--> Votre choix : ")
        
        try:   
            
            choix = int(rawChoice)
            
            if choix in possibleChoices:
                return choix
            else:
                print("{} n'est pas un choix valide. Veuillez rééssayer.".format(choix))
            
        except ValueError:
            print("{} n'est pas un choix valide. Veuillez rééssayer.".format(rawChoice))

def userInputPath(description, checkPath = True, safeExit = None):
    """Lecture d'un chemin d'accès donné par l'utilisateur
    
    :param expectedType: Type de choix à lire
    :param expectedType: ``type``
    """
    
    from os.path import exists
    
    print(description)
    
    
    while True:
        
        if safeExit is not None:
            rawChoice = input("\n--> Entrez un chemin ({} pour annuler) : ".format(safeExit))
        else:
            rawChoice = input("\n--> Entrez un chemin : ")
        
        try:
            choix = str(rawChoice)
            
            #Test à effectuer selon la valeur de checkPath
            test = exists(choix) if checkPath else True
            
                
            if test or choix == safeExit:
                return choix
            else:
                mess = "n'existe pas" if checkPath else "existe déjà"
                print(f"{choix} {mess}. Veuillez rééssayer.".format(choix))
                    
        except:
            print("{} n'est pas un choix valide. Veuillez rééssayer.".format(rawChoice))
    
def userInputValue(description, expectedType = float, safeExit = None):
    """Lecture d'une valeur donnée par l'utilisateur
    
    :param description: Description de la valeur à lire
    :type description: ``str`` 
    :param expectedType: Type de choix à lire (float ou int)
    :param expectedType: ``type``
    :param safeExit: Valeur à donner pour interrompre la lecture
    :param expectedType: ``expectedType``
    """
    
    print("\n")
    print(description)
    
    while True:
        
        if safeExit is not None:
            rawChoice = input("--> Entrez une valeur ({} pour annuler): ".format(safeExit))
        else:
            rawChoice = input("--> Entrez une valeur : ")
        
        try:
            choix = expectedType(rawChoice)
            
            if choix == safeExit:
                return
            else:
                return choix
            
        except:
            print("{} n'est pas un choix valide. Veuillez rééssayer.".format(rawChoice))
    
def userInputValueOrDefault(description, expectedType, default):
    """Lecture d'une valeur donnée par l'utilisateur
    
    :param description: Description de la valeur à lire
    :type description: ``str`` 
    :param expectedType: Type de choix à lire (float ou int)
    :param expectedType: ``type``
    :param safeExit: Valeur à donner pour interrompre la lecture
    :param expectedType: ``expectedType``
    """
    
    print(description)
    
    while True:
        
        rawChoice = input("--> Entrez une valeur (Par défaut {}): ".format(default))
        
        try:
            
            #Si on donne une ligne vide, on renvoie la valeur par défaut
            if rawChoice == "":
                return default
            
            #Sinon on lit la valeur donnée
            else:
                choix = expectedType(rawChoice)
                return choix
            
        except:
            print("{} n'est pas un choix valide. Veuillez rééssayer.".format(rawChoice))
