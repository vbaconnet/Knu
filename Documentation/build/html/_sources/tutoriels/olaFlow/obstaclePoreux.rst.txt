Obstacle poreux
=====================

Ce tutoriel est une introduction à l'outil ``olaFlow``. ``olaFlow`` est un solveur
spécialement conçu pour l'ingénierie côtière. Vous pouvez le télécharger à l'adresse::

    https://github.com/phicau/olaFlow

en suivant les instructions. Consultez aussi
sa `page web <https://olaflow.github.io/>`_, qui expose toutes les 
capacités du solveur.

Pour nos simulations, ``olaFlow`` est intéressant car il utilise une
modélisation assez avancée des milieux poreux. En ingénierie côtière, 
les milieux poreux nous permettent de modéliser les enrochements sur des digues
de protection, par exemple.

Ce tutoriel est similaire au tutoriel de l':doc:`obstacle poreux <../interFoam/obstaclePoreux>` 
pour le solveur ``interFoam``. La seule différence est dans la modélisation du milieu poreux. 
Ce tutoriel est directement tiré des tutoriels d'olaFlow.

L'ensemble des commandes à exécuter se trouve dans les fichiers ``Allrun.case.laminar``
et ``Allrun.case.turbulent`` selon le type de simulation que vous voulez effectuer. Vous
pouvez les exécuter directement pour ne pas avoir à exécuter chaque commande individuellement.
Voici un exemple avec le fichier ``Allrun.case.turbulent``:

.. code-block:: none

    #!/bin/bash

    # Lancer le maillage
    Allmesh -c

    # Générer la houle irrégulière
    genHouleIrreguliere --solver olaFlow

    # Choisir le modèle de turbulence kEpsilon
    cp constant/turbulenceProperties.turbulent constant/turbulenceProperties

    # Lancer le calcul. L'option -s lance setFields
    Allrun -s &

    # Attendre 2 secondes avant de lancer le monitoring
    sleep 5

    # Suivre la progression du calcul et lancer la lecture
    # des points de mesure de pression
    AllpostProcess lirePoints.py

    traceSondes.py point1.csv


**Maillage**

Le maillage que nous allons utiliser est un maillage rectangulaire simple.
Consultez le fichier ``system/blockMeshDict`` pour plus de détails.

Lancez ``blockMesh`` avec la commande::

    blockMesh

Visualisez-le si besoin avec ``ParaView``.

**Paramétrage du milieu poreux**

La géométrie que nous allons étudier utilise plusieurs zones d'enrochements,
définies par des surfaces dans le dossier ``constant/triSurface/``. Chaque surface
correspond à un type d'enrochement différent, donc à un milieu poreux différent.

Dans ``olaFlow``, chaque milieu poreux est marqué par la variable ``porosityIndex``, qui
part de la valeur 0 pour un milieu non-poreux, et qui s'incrémente de 1 pour référencer
chaque milieu poreux ajouté. Pour initialiser la valeur de ``porosityIndex`` à chaque 
surface, nous utilisons l'outil ``setFields``. Le paramétrage s'effectue dans le fichier 
``system/setFieldsDict``:

.. code-block:: none

    defaultFieldValues
    (
        volScalarFieldValue alpha.water 0
        volScalarFieldValue porosityIndex 0
    );

    regions
    (
        boxToCell
        {
            box (-10 -10 -10) (500 10 0.8);

            fieldValues
            (
                volScalarFieldValue alpha.water 1
            );
        }

        surfaceToCell
        {
            file            "./constant/triSurface/primLayer.stl";
            outsidePoints   ((16 0.001 0.25));    // definition of outside
            includeCut      true;              // cells cut by surface
            includeInside   true;              // cells not on outside of surf
            includeOutside  false;              // cells on outside of surf
            nearDistance    -1;                 // cells with centre near surf
                                                // (set to -1 if not used)
            curvature       -100;                // cells within nearDistance
                                                // and near surf curvature
                                                // (set to -100 if not used)

            fieldValues
            (
                volScalarFieldValue porosityIndex 3
            );
        }

        surfaceToCell
        {
            file            "./constant/triSurface/secLayer.stl";
            outsidePoints   ((16 0.001 0.25));    // definition of outside
            includeCut      true;              // cells cut by surface
            includeInside   true;              // cells not on outside of surf
            includeOutside  false;              // cells on outside of surf
            nearDistance    -1;                 // cells with centre near surf
                                                // (set to -1 if not used)
            curvature       -100;                // cells within nearDistance
                                                // and near surf curvature
                                                // (set to -100 if not used)

            fieldValues
            (
                volScalarFieldValue porosityIndex 2
            );
        }

        surfaceToCell
        {
            file            "./constant/triSurface/core.stl";
            outsidePoints   ((16 0.001 0.25));    // definition of outside
            includeCut      true;              // cells cut by surface
            includeInside   true;              // cells not on outside of surf
            includeOutside  false;              // cells on outside of surf
            nearDistance    -1;                 // cells with centre near surf
                                                // (set to -1 if not used)
            curvature       -100;                // cells within nearDistance
                                                // and near surf curvature
                                                // (set to -100 if not used)

            fieldValues
            (
                volScalarFieldValue porosityIndex 1
            );
        }
    );

La première liste ``defaultFieldValues`` met une valeur par défaut pour chaque
variable dans l'ensemble du domaine. Le premier sous-dictionnaire de la liste
``regions`` permet d'initialiser la hauteur d'eau, mais ce n'est pas ce qui nous
intéresse ici. Le deuxième sous-dossier initialise la valeur 3 dans la zone
délimitée par la surface ``./constant/triSurface/primLayer.stl``. On effectue la même
chose pour les 2 autres surfaces, en leur attribuant un ``porosityIndex`` différent.

Créez le dossier ``0`` en copiant le dossier ``0.orig``, et lancez ``setFields``::

    cp -r 0.orig 0
    setFields

Visualisez les zones poreuses sous ``ParaView`` en affichant le champ ``porosityIndex``.

**Génération de houle**

Nous allons générer de la houle irrégulière, de la même manière que pour
le tutoriel de :doc:`houle irrégulière <../interFoam/houleIrreguliere>`. les
paramètres du spectre de JONSWAP sont donnés dans le fichier ``jonswapDict``:

.. code-block:: none

    Tmin  5.9
    Tmax  14.8
    Tp    10.6
    Hs    3.1
    gamma 1.0
    scale 28.6 

Générez le fichier ``constant/waveProperties`` avec la commande::

    genHouleIrreguliere --solver olaFlow

``olaFlow`` utilise un format légèrement différent de ``interFoam``, pour
indiquer les paramètres de houle dans ``constant/waveProperties``,
donc il faut préciser l'option ``--solver olaFlow`` pour qu'il soit pris 
en compte par le programme de génération de houle.

De même, il faut modifier les conditions limites de houle dans les fichiers 
``0.orig/alpha.water``:

.. code-block:: none

    inlet
    {
        type            waveAlpha;
        waveDictName    waveProperties;
        value           uniform 0;
    }

et ``0.orig/U``: 

.. code-block:: none

    inlet
    {
        type            waveVelocity;
        waveDictName    waveProperties;
        value           uniform (0 0 0);
    }

    outlet
    {
        type            waveAbsorption2DVelocity;
        absorptionDir   666.0;
        value           uniform (0 0 0);
    }

Notez dans ce dernier fichier que la condition d'absorption
sur le patch ``outlet`` peut se donner directement dans la condition limite, sans définir 
cette condition dans ``constant/waveProperties``.

**Lancement de la simulation**

Vérifiez les paramètres de simulation dans ``system/controlDict``. Notez que nous avons posé 
deux points de mesure de part et d'autre du système d'enrochements, où nous préleverons 
la pression pour mettre en lumière les effets des enrochements.

.. code-block:: none

    functions
    {

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
            writeInterval    1;
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
                        (17.5 0 0.8)
                        (19.3 0 0.95)
                    );
                }
            );
            fields
            (
                p
            );
        }
    }

Pour une explication détaillée de la mesure de pression en plusieurs points,
consultez le tutoriel sur la :doc:`mesure de pression<../interFoam/mesurePressionOuvrage>`.

Vous pouvez maintenant lancer la simulation, en exécutant la commande::

    olaFlow > log.olaFlow &

Vous pouvez aussi lancer ``setFields`` et ``olaFlow`` directement avec ::

    Allrun -s &

**Surveillance de simulation et post-traitement**

Exécutez la commande suivante pour suivre le statut de votre simulation,
et lire les points de mesure de pression lorsqu'elle sera terminée::

    AllpostProcess lirePoints.py 

Une fois tous les points lus, ``traceSondes.py`` va créer un fichier
``.csv`` avec les mesures de pression. Exécutez la commande suivante pour tracer
ces mesures de pression::

    traceSondes.py points1.csv

Ou en remplaçant ``points1.csv`` par le nom de votre fichier.
