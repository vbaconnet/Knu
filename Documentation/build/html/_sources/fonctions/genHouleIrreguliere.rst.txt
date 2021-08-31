Génération de houle irrégulière
================================

Informations
------------

* Fichier : ``Knu/Scripts/Automatisation-OpenFOAM/genHouleIrreguliere.py`` 

* Auteur: Victor Baconnet
    
* Date de dernière modification: 08 Juillet 2021

Description
------------

Génère le fichier ``constant/waveProperties`` contenant les paramètres et coefficients 
d'amplitude, périodes, déphasages et directions pour le patch inlet, et des 
paramètres d'absorption pour le patch outlet.

La génération peut se faire selon la syntaxe interFoam/interIsoFoam ou olaFlow, 
toujours à partir du fichier ``jonswapDict``.

Pour exécuter ce fichier, vous devez spécifier les paramètres de spectre JONSWAP
dans le fichier "jonswapDict" formaté comme suit::
    
  Tp 1.78
  Tmin 1.0
  Tmax 3.0
  Hs 1.5
  gamma 3.2
  scale 25.0 //optionnel
    
L'exécution de ce fichier renverra une erreur si ``jonswapDict`` n'est pas trouvé.
Vous pouvez, si besoin, préciser le chemin d'accès vers le fichier de votre 
choix avec l'option ``--jonswapFile``.

Le fichier de sortie ``waveProperties`` sera créé dans le répertoire ``constant``
si il existe, ou directement dans le répertoire courant. Vous pouvez, si besoin,
préciser le chemin d'accès vers le répertoire de votre choix avec l'option 
``--wavePropertiesPath``.

Utilisation
------------

.. code-block:: bash

   $ genHouleIrreguliere.py [OPTIONS]
   $ python3 genHouleIrreguliere.py [OPTIONS]

**Options**

-h, --help                        Afficher l'aide
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
--solver solver                   Nom du solveur utilisé pour le formatage du 
                                  fichier waveProperties

    
Dépendances
-----------

    
* ``numpy``
* ``sys``, ``os``
* ``jonswap``, ``outilsLecture``, 
  
Code source
------------

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Automatisation-OpenFOAM/genHouleIrreguliere.py>`_

