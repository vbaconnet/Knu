Génération de houle régulière
==============================

Informations
------------

* Auteur: Victor Baconnet
    
* Date de dernière modification: 08 Juillet 2021

Description
------------

Génère le fichier ``constant/waveProperties`` contenant les paramètres et coefficients 
d'amplitude, périodes, déphasages et directions pour le patch inlet, et des 
paramètres d'absorption pour le patch outlet.

La génération peut se faire selon la syntaxe interFoam/interIsoFoam ou olaFlow, 
toujours à partir du fichier ``constant/regularWaveDict``.

Pour exécuter ce fichier, vous devez spécifier les paramètres de houle régulière
comme suit::
    
  wavePeriod 1.78
  waveHeight 1.0

Vous pouvez aussi rajouter d'autres paramètres, comme::
    
    waveAngle 0.0
    rampTime 2.0
    nPaddle 1
    activeAbsorption no
    
.. NOTE ::
    
    Veillez à bien respecter la casse des paramètres dans le fichier ``regularWaveDict``

L'exécution de ce fichier renverra une erreur si ``regularWaveDict`` n'est pas trouvé.
Vous pouvez, si besoin, préciser le chemin d'accès vers le fichier de votre 
choix avec l'option ``--waveDict``.

Le fichier de sortie ``waveProperties`` sera créé dans le répertoire ``constant``
si il existe, ou directement dans le répertoire courant. Vous pouvez, si besoin,
préciser le chemin d'accès vers le répertoire de votre choix avec l'option 
``--wavePropertiesPath``.

Utilisation
------------

-h, --help                        Afficher l'aide
--wavePropertiesPath path         chemin d'accès vers le répertoire d'écriture
                                  du fichier waveProperties    
--waveDict file                   chemin d'accès vers le fichier contenant les 
                                  paramètres de houle régulière                                
--inlet inletName                 Spécifie le nom du patch inlet (là où la houle
                                  sera générée).
--outlet outletName               Spécifie le nom du patch outlet (là où la 
                                   houle sera absorbée)
--noOutlet                        ne pas créer de patch outlet
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
------------

* ``numpy``
* ``sys``, ``os``
* ``outilsLecture`` 

Code source
------------

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Automatisation-OpenFOAM/genHouleReguliere.py>`_

