Houle régulière
=================

**Description de la situation**

Ce tutoriel est une introduction à la génération de houle régulière sous OpenFOAM. 

L'ensemble des commandes à lancer est donné dans les fichiers ``Allrun.case.laminaire`` ou 
``Allrun.case.turbulent``, que vous pouvez exécuter directement selon le type de 
simulation que vous voulez lancer. Voici un extrait du fichier ``Allrun.case.laminaire``:

.. code-block:: bash

    #!/bin/bash

    Allmesh

    genHouleReguliere

    mv constant/turbulenceProperties.laminar constant/turbulenceProperties

    Allrun -s &

    sleep 2

    AllpostProcess lireSondes.py 

    traceSondes.py line_probes.csv



**Maillage**

Nous utiliserons une géométrie rectangulaire 2D. Le maillage est défini dans le fichier
``system/blockMeshDict``::

    xmin  0.0;
    xmax 10.0;
    ymin -0.5;
    ymax  0.5;
    zmin  0.0;
    zmax  2.0;

    Nz    60;

    Nx #calc "$Nz * ( $xmax - $xmin) / ( $zmax - $zmin )";

    vertices
    (

        ( $xmin $ymin $zmin) //0
        ( $xmax $ymin $zmin) //1
        ( $xmax $ymax $zmin) //2
        ( $xmin $ymax $zmin) //3

        ( $xmin $ymin $zmax) //4
        ( $xmax $ymin $zmax) //5
        ( $xmax $ymax $zmax) //6
        ( $xmin $ymax $zmax) //7

    );

    blocks
    (
        hex (0 1 2 3 4 5 6 7) ($Nx 1 $Nz) simpleGrading (1 1 1)
    );

    edges
    (
    );

    boundary
    (
        inlet
        {
            type patch;
            faces
            (
                (0 4 7 3)
            );
        }
        outlet
        {
            type wall;
            faces
            (
                (1 5 6 2)
            );
        }
        BOTTOM
        {
            type wall;
            faces
            (
                (0 1 2 3)
            );
        }
        TOP
        {
            type patch;
            faces
            (
                (4 5 6 7)
            );
        }
        frontPlane
        {
            type empty;
            faces
            (
                (0 1 5 4)
            );
        }
        backPlane
        {
            type empty;
            faces
            (
                (3 2 6 7)
            );
        }
    );

Exécutez ``blockMesh`` avec la commande ::

    $ blockMesh

Vous pouvez visualiser le maillage avec ``ParaView``.

**Génération de houle**

Nous allons générer de la houle régulière. Les paramètres doivent être donnés 
dans le fichier ``regularWaveDict`` :

.. code-block:: none

    waveHeight 0.12       // Hauteur ( = 2*amplitude )
    wavePeriod 1.3        // Période
    activeAbsorption yes  // Absorption sur la face d'entrée
    ramptime   0.5        // Durée de la rampe en entrée

Vous pouvez éventuellement rajouter d'autres paramètres. Pour plus de détails sur
les paramètres à rajouter, consultez la documentation du fichier de génération de houle
régulière :doc:`genHouleReguliere.py <../../fonctions/genHouleReguliere>`.

Pour générer le fichier de houle régulière, lancez la commande::

    $ genHouleReguliere.py

Cette commande générera le fichier ``constant/waveProperties``::

    inlet
    {
        alpha            alpha.water;
        waveModel        StokesI;
        nPaddle          1;

        rampTime         0.5;
        activeAbsorption yes;
        waveHeight       0.12;
        wavePeriod       1.3;

        waveAngle        0.0;
    }

    //  Absorption sur la face de sortie
    outlet
    {
        alpha            alpha.water;
        waveModel        shallowWaterAbsorption;
        nPaddle          1;
    }

Comme vous pouvez le voir, d'autres paramètres que ceux spécifiés dans le 
``regularWaveDict`` sont présents par défaut. Le programme a aussi généré
une condition d'absorption dynamique sur la face ``outlet`` par défaut.

**Conditions limites**

Pour indiquer une condition de houle sur les faces d'entrée/sortie, 
nous devons spécifier la condition ``waveAlpha`` dans le fichier
``0.orig/alpha.water``::

    dimensions      [0 0 0 0 0 0 0];

    internalField   uniform 0;

    boundaryField
    {
        inlet
        {
            type            waveAlpha;
            value           uniform 0;
        }

        outlet
        {
            type            waveAlpha;
            value           uniform 0;
        }

        BOTTOM
        {
            type            zeroGradient;
        }

        TOP
        {
            type            inletOutlet;
            inletValue      uniform 0;
            value           uniform 0;
        }

        frontPlane
        {
            type            empty;
        }

        backPlane
        {
            type            empty;
        }
    }

De manière générale, un mur sera de type ``zeroGradient``. Notez la condition
``inletOutlet`` pour la face horizontale supérieure, qui modélise une condition
d'atmosphère.

Il faut également rajouter une condition limite de type ``waveVelocity`` dans le 
fichier ``0.orig/U``::

    dimensions      [0 1 -1 0 0 0 0];

    internalField   uniform (0 0 0);

    boundaryField
    {
        inlet
        {
            type            waveVelocity;
            value           uniform (0 0 0);
        }

        outlet
        {
            type            waveVelocity;
            value           uniform (0 0 0);
        }

        BOTTOM
        {
            type            fixedValue;
            value           uniform (0 0 0);
        }

        TOP
        {
            type            pressureInletOutletVelocity;
            value           uniform (0 0 0);
        }

        frontPlane
        {
            type            empty;
        }

        backPlane
        {
            type            empty;
        }
    }

Notez là aussi la condition ``pressureInletOutletVelocity`` pour la modélisation
de l'atmosphère pour la face horizontale supérieure.

Il n'y a pas de traitement particulier pour les conditions limites de pression.

**Lancement de la simulation**

Si vous le souhaitez, vous pouvez utiliser un modèle de turbulence. Pour cela,
utilisez le script ``Allrun.case.turbulent`` ou lancez la commande:

.. code-block:: bash

    cp constant/turbulenceProperties.komega constant/turbulenceProperties

En faisant cela, vous allez utiliser le modèle de turbulence :math:`k-\omega` SST.

N'oubliez pas de copier le fichier ``0.orig`` vers un nouveau dossier ``0`` et de
lancer ``setFields``, pour initialiser une hauteur d'eau de :math:`0.864\,m`:

.. code-block:: bash

    cp -r 0.orig 0
    setFields

Vous pouvez maintenant lancer ``interFoam``. Si vous le souhaitez, modifiez les
paramètres de ``system/controlDict``. Par défaut, le temps de simulation est de 
10 secondes avec une sauvegarde toutes les 0.1 secondes.

Nous avons aussi posé 4 sondes le long du canal, définies dans le dictionnaire
``functions`` de ``system/controlDict``::

    // Indiquer ici les sondes et leurs coordonnées (position x en m)
    sonde1      S1-1.0;
    x1          1.0;
    sonde2      S2-4.0;
    x2          4.0;
    sonde3      S3-7.0;
    x3          7.0;

    // Coordonnées des points de mesure
    ystart      0.0;
    yend        0.0;
    zstart      0.0;
    zend        2.0;
    N           301; // Nombre de points

    functions
    {

        line
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
                $sonde1
                {
                    type uniform;
                    axis distance;
                    start   ( $x1 $ystart $zstart );
                    end     ( $x1 $yend   $zend   );
                    nPoints $N;
                }
                $sonde2
                {
                    type uniform;
                    axis distance;
                    start   ( $x2 $ystart $zstart );
                    end     ( $x2 $yend   $zend   );
                    nPoints $N;
                }
                $sonde3
                {
                    type uniform;
                    axis distance;
                    start   ( $x3 $ystart $zstart );
                    end     ( $x3 $yend   $zend   );
                    nPoints $N;
                }
            );
            fields (
                alpha.water
            );
        }
    }

Lancez la simulation avec

.. code-block:: bash

    interFoam > log.interFoam &

Vous pouvez aussi lancer ``setFields`` et ``interFoam`` directement avec la commande::

    Allrun -s &

**Post-traitement**

Un fois que la simulation est lancée, vous pouvez la surveiller avec le 
script ``AllpostProcess``. En options, vous pouvez y ajouter des scripts
que vous voulez exécuter lorsque la simulation sera terminée.
Dans notre cas, nous allons exécuter le fichier de lecture de sondes 
``lireSondes.py``, puis afficher le signal de houle 
mesuré par ces sondes.

.. code-block:: bash

    AllpostProcess lireSondes.py 
    traceSondes.py line_probes.csv

