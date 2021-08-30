Rééchantillonnage des données de sondes 
========================================

Informations
---------------

    * Fichier : ``resample.py``
    * Auteur: Victor Baconnet
    * Date de dernière modification: 27 août 2021

Description
---------------

Rééchantillonne un signal avec une fréquence par défaut de 50 Hz, mais peut être
changée avec l'option ``--samplingfreq <freq>``

Entrées/sorties
---------------

*  Lecture des valeurs à traiter dans un fichier par défaut ``line_probes.csv``,
   mais peut être modifié avec la commande ``--file file.csv``. Le fichier
   doit être formaté comme suit::
       
       temps,val1,val2
       t1,v11,v12
       t2,v21,v22
       ...
       tn,vn1,vn2

   où les ``tn,vn1,vn2`` sont des valeurs numériques.

*  Données rééchantillonnées écrites dans le fichier dont le préfixe est 
   ``RESAMPLED_``, suivi du nom du fichier original.

Utilisation
---------------

.. code-block:: bash

  $ resample [OPTIONS]

--file file             Nom du fichier dans lequel lire le signal à traiter.
                        Doit être au format ``.csv``.
--samplingfreq freq     Fréquence de rééchantillonnage. Par défaut à 50 Hz  

Code source
----------------

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Post-traitement/resample.py>`_
