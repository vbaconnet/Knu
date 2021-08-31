Milieu poreux
===============


**Description de la situation**

Ce tutoriel est une introduction aux milieux poreux sous OpenFOAM.

L'ensemble des commandes à lancer est donné dans les fichiers ``Allrun.case.laminaire`` ou 
``Allrun.case.turbulent`` selon le type de simulation que vous voulez lancer. Voici un 
extrait du fichier ``Allrun.case.turbulent``:

.. code-block:: bash

    #!/bin/bash

    # Lancer le maillage
    Allmesh -c

    # Générer la houle irrégulière
    genHouleIrreguliere

    # Copier le fichier turbulence à utiliser
    cp constant/turbulenceProperties.turbulent constant/turbulenceProperties

    # Lancer le calcul. L'option -s lance setFields
    Allrun -ts &

    # Attendre 2 secondes avant de lancer le monitoring
    sleep 2

    # Suivre la progression du calcul et lancer la commande
    # ls lorsque le calcul est terminé
    AllpostProcess ls


**Maillage**

Le maillage est le même que pour le tutoriel de obstacle_zone.
Lancez l'outil ``blockMesh`` avec la commande::

    $ blockMesh

Vous pouvez visualiser ce maillage avec ``ParaView``. 

**Génération de houle**

La condition de houle est la même que pour le tutoriel de :doc:`houle irrégulière<houleIrreguliere>`.

**Milieu poreux**

Pour prendre en compte les enrochements, nous allons utiliser une modélisation
de Darcy-Forchheimer. Pour plus de détails, consultez la `documentation <https://openfoamwiki.net/index.php/DarcyForchheimer>`
sur le modèle de porosité. Si vous y avez accès, mon rapport de stage présente les théories
de modélisation en milieu poreux.

Dans un premier temps, il faut créer la zone poreuse. Pour cela, 
nous allons utiliser l'utilitaire ``topoSet``. L'obstacle sera exactement
le même que dans le tutoriel de :doc:`mesure de pression <mesurePressionOuvrage>`.
Configurez le fichier ``topoSetDict`` comme suit:

.. code-block:: none

    actions
    (

    // * * * * * * Zone d'enrochements * * * * * * * * * *

        {
            name    c0;
            type    cellSet;
            action  new;
            source  boxToCell;
            sourceInfo
            {
                box (10 -99 -99) (15 99 1); // Edit box bounds as required
            }
        }

        {
            name    obstacle_zone;
            type    cellZoneSet;
            action  new;
            source  setToCellZone;
            set     c0;
        }

    );


Le premier sous-dictionnaire sélectionne la zone qui correspond à l'obstacle, 
sous la forme d'un ``cellSet``. Le deuxième sous-dictionnaire permet de convertir 
ce ``cellSet`` en une ``cellZone``. Nommons cette zone ``obstacle_zone``. C'est 
avec ce nom que nous y ferons référence désormais.

Lancez ``topoSet`` avec la commande::

    topoSet

Les paramètres du milieu poreux sont donnés dans le fichier ``constant/fvOptions``:

.. code-block:: none

    porosity1
    {
        type            explicitPorositySource;

        explicitPorositySourceCoeffs
        {
            selectionMode   cellZone;
            cellZone        obstacle_zone;

            type            DarcyForchheimer;

            d   (2111.7 2111.7 2111.7);
            f   (0.0 0.0 0.0);

            coordinateSystem
            {
                origin  (0 0 0);
                e1      (1 0 0);
                e2      (0 1 0);
            }
        }

    }

On y précise le type de modèle avec ``type  explicitPorositySource``. La zone poreuse 
s'indique avec le mot-clé ``cellZone  obstacle_zone``. Les coefficients
du modèle de Darcy-Forchheimer sont les vecteurs ``d`` et ``f``. Ce sont
des vecteurs car vous pouvez préciser des coefficients différents selon chaque direction.
Nous considérons un matériau homogène et isotrope, donc nos coefficients sont les mêmes
dans chaque direction.

**solveur**

Les conditions limites sont inchangées par rappport au tutoriel :doc:`houle irrégulière<houleIrreguliere>`,
mais vous pouvez aller les vérifier dans le dossier ``0.orig``.

Pensez à bien créer le dossier ``0`` en copiant le dossier ``0.orig`` avant de lancer ``setFields``::

    cp -r 0.orig 0
    setFields

Notez que nous avons rajouté un point de mesure de pression dans ``system/controlDict``:

.. code-block:: none

    points
    {
        type            sets;
        libs            ("libsampling.so");
        enabled         true; // Mettre à false pour désactiver les sondes

        // Contrôle d'écriture :
        //  - timeStep   : pas de temps
        //  - adjustable : temps (si pas de temps adaptatif)
        //  - runTime    : temps (si pas de temps constant)
        writeControl     timeStep;
        writeInterval    2;
        fixedLocations false;
        interpolationScheme cellPoint;
        setFormat       raw;
        sets
        (
            point1
            {
                type cloud;
                axis distance;
                points
                (
                    (10 0 1)
                );
            }
        );
        fields
        (
            p
        );
    }

Ce point est le même que pour le tutoriel de :doc:`mesure de pression sur un ouvrage <mesurePressionOuvrage>`.
Vous êtes maintenant prêt(e) à lancer la simulation. Ajustez vos paramètres de 
simulation dans ``system/controlDict``. Lancez ``interFoam`` et redirigez
la sortie dans un fichier log::

    interFoam > log.interFoam &

.. NOTE::
    
    Toutes ces étapes peuvent être effectuées avec la commande::

        Allrun -st &
    
**Surveillance du statut de la simulation et post-traitement**

La commande ``AllpostProcess`` permet de lancer des scripts une fois 
que la simulation sera terminée. En attendant, vous pourrez
voir le statut de simulation. Lancez la commande::

    AllpostProcess lirePoints.py

Lorsque la simulation sera finie, le script ``lirePoints.py``
va lire les données de pression, et les écrira dans un fichier .csv.

Utilisez la commande suivante pour tracer la mesure de pression::

    traceSondes.py points1.csv

Ou en remplaçant ``points1.csv`` par le nom de votre fichier de mesures.