Calcul de débit de franchissement 
==================================

Informations
-------------

    * Fichier: ``Knu/Scripts/Post-traitement/debitFranchissement.py``
    * Auteur: Victor Baconnet
    * Date de dernière modification: 27 août 2021

Description
-------------

Calcule le débit de franchissement à partir de mesures de volume écrites dans
un fichier du dossier postProcessing. Le nom de ce fichier est par défaut
``postProcessing/waterVolume/0/volFieldValue.dat`` mais peut être modifié
avec l'option ``--path``.

Utilisation
-------------

--largeur l                       Largeur du canal
--outputFile fichier              Chemin vers fichier de sortie où seront écrits
                                  les débits de franchissement. Doit être au format ``.csv``
--path file                       Chemin d'accès vers le fichier contenant les 
                                  paramètres de spectre JONSWAP                                 
--echelle scale                   Echelle pour convertir le débit modèle vers 
                                  le débit prototype (réel). Par défaut défini
                                  à 1. Si le fichier ``jonswapDict`` existe,
                                  l'option ne sera pas prise en compte et la
                                  valeur donnée dans le fichier sera utilisée.


Entrées/Sorties
----------------

Crée un fichier de sortie avec les valeurs temporelles, volume mesuré et débit
de franchissement calculé. 

Code source
-------------

lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Post-traitement/debitFranchissement.py>`_

