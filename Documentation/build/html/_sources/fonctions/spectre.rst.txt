Reconstruction de spectre
==========================

Informations
---------------

    * Fichier: ``spectre.py``
    * Auteur: Victor Baconnet
    * Date de dernière modification: 27 août 2021

Description
---------------

Reconstruit et affiche les spectres de densité de puissance à partir de mesures
de hauteur d'interface par des sondes, lues dans un fichier ``.csv``. 

Si le fichier ``jonswapDict`` est 
présent dans le dossier d'exécution, le programme tracera le spectre théorique 
à partir des paramètres du fichier, et calculera les hauteurs :math:`H_s` par intégration
numérique d'après la formule
    
.. math::
    H_s = 4 \sqrt{\int_{0}^{+\infty} S(\omega)d\omega}       
    
ou, sous forme discrétisée, par intégration selon la méthode des trapèzes

.. math:: 
    H_s = 4 \sqrt{ \frac{\Delta \omega }{2}  \sum_{i=0}^{N-1}{ S_{i+1} - S_i }} 

où :math:`S_i` est la valeur du spectre de Jonswap reconstruit.

Entrées/sorties
---------------

* Les mesures des sondes doivent être données dans un fichier au format csv, par défaut
  ``RESAMPLED_line_probes.csv`` mais peut être modifié avec l'option ``--sondeFile``

* Si vous souhaitez comparer les spectres calculés avec un spectre théorique de JONSWAP,
  les paramètres Tp, Hs, Tmin, Tmax, gamma doivent être donnés dans un fichier par défaut 
  ``jonswapDict``, mais peut être modifié avec l'option ``--jonswapFile``
  

Utilisation
---------------

.. code-block:: bash

    $ spectre.py [OPTIONS]

--savefigs                        Sauvegarder les graphiques générés
--sondeFile fichier               Chemin d'accès vers le répertoire d'écriture
                                  du fichier waveProperties    
--jonswapFile file                chemin d'accès vers le fichier contenant les 
                                  paramètres de spectre JONSWAP                                 
--Npoints n                       Nombre de points (longueur) de chaque segment 
                                  de calcul par la méthode de Welch (https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html#r34b375daf612-1)
--scaling scale                   Echelle avec laquelle multiplier les valeurs
                                  de hauteur d'interface lues par les sondes.
                                  Par exemple si les mesures sont en cm, utiliser
                                  ``--scaling 0.01``.
                                                                     
Dépendances
---------------

* ``numpy``, ``scipy``, ``matplotlib``, ``pandas``
* ``jonswap``, ``outilsLecture``, ``outilsDivers``

Code source
---------------

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Post-traitement/spectre.py>`_

