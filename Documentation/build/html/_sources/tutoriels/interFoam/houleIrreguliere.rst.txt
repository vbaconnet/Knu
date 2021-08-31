Houle irrégulière
===============================

**Description de la situation**

Ce tutoriel est une introduction à la génération de houle irrégulière sous OpenFOAM. 

L'ensemble des commandes à lancer est donné dans les fichiers ``Allrun.case.laminaire`` ou 
``Allrun.case.turbulent`` selon le type de simulation que vous voulez lancer. Voici un 
extrait du fichier ``Allrun.case.laminaire``:

.. code-block:: bash

    #!/bin/bash

    Allmesh

    genHouleIrreguliere

    mv constant/turbulenceProperties.laminar constant/turbulenceProperties

    Allrun -s &

    sleep 2

    AllpostProcess lireSondes.py resample.py spectre.py

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

Attention, ce maillage n'est pas optimisé pour des résultats précis,
mais pour que la simulation soit plus rapide. Vous devrez créer un 
maillage plus fin si vous souhaitez obtenir une bonne propagation 
de houle. 

Exécutez ``blockMesh`` avec la commande ::

    $ blockMesh

Vous pouvez visualiser le maillage avec ``ParaView``.

**Génération de houle**

Nous allons générer de la houle irrégulière. Les paramètres doivent être donnés 
dans le fichier ``jonswapDict`` :

.. code-block:: none

    Tmin  5.3
    Tmax  13.2
    Tp    9.5
    Hs    2.8
    gamma 1.0
    scale 28.6 //prototype = scale*modele
    Ncomposantes 500
    activeAbsorption yes

Vous pouvez éventuellement rajouter d'autres paramètres. Pour plus de détails sur
les paramètres à rajouter, consultez la documentation du fichier de génération de houle
irrégulière :doc:`genHouleIrreguliere.py <../../fonctions/genHouleIrreguliere>`.

Pour générer le fichier de houle régulière, lancez la commande::

    $ genHouleIrreguliere.py

Cette commande générera le fichier ``constant/waveProperties``::

    inlet
    {

        alpha            alpha.water;

        waveModel        irregularMultiDirectional;

        nPaddle          1;

        rampTime         2.0;

        activeAbsorption no;

        // Périodes
        wavePeriods
        500
        (
    (2.468260053622327)
    (2.4609090567047303)
    (2.4536017153974696)   
    ...
    (0.9922338633836915)
    (0.9910438094089646)
        );

        // Hauteurs
        waveHeights
        500
        (
    (0.003396375978114038)
    (0.003465582605517084)
    ...
    (0.0033642199662089972)
    (0.0033551190392587947)
        );

        // Déphasages
        wavePhases
        500
        (
    (5.730876186873959)
    (2.1365116696284603)
    ...
    (3.4502359148319943)
    (3.484300558914438)
        );

        // Directions
        waveDirs
        500
        (
    (0.0)
    (0.0)
    ...
    (0.0)
    (0.0)
        );
    }

    // absorption sur la face de sortie
    outlet
    {
        alpha            alpha.water;
        waveModel        shallowWaterAbsorption;
        nPaddle          1;
    }

Comme vous pouvez le voir, d'autres paramètres que ceux spécifiés dans le 
``jonswapDict`` sont présents par défaut. Le programme a généré les 
hauteurs de houle, périodes, déphasages et directions de chaque composante
de houle monochromatique. La géométrie étant 2D, les directions sont toutes 
fixées à 0. Le programme a aussi généré une condition
d'absorption dynamique sur la face ``outlet`` par défaut.

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

    mv constant/turbulenceProperties.komega constant/turbulenceProperties

En faisant cela, vous allez utiliser le modèle de turbulence :math:`k-\omega` SST.

N'oubliez pas de copier le fichier ``0.orig`` vers un nouveau dossier ``0`` et de
lancer ``setFields``, pour initialiser une hauteur d'eau de :math:`0.864\,m`:

.. code-block:: bash

    cp -r 0.orig 0
    setFields

Vous pouvez maintenant lancer ``interFoam``. Si vous le souhaitez, modifiez les
paramètres de ``system/controlDict``. Par défaut, le temps de simulation est de 
10 secondes avec une sauvegarde toutes les 0.1 secondes. 

.. NOTE:: 

    Si vous souhaitez expérimenter avec la reconstruction de spectre,
    il est conseillé d'augmenter le temps de simulation à 300 secondes
    au minimum. 

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


.. code-block:: bash

    interFoam > log.interFoam &

**Post-traitement**

Un fois que la simulation est lancée, vous pouvez la surveiller avec le 
script ``AllpostProcess``. En options, vous pouvez y ajouter des scripts
que vous voulez exécuter. Dans notre cas, nous allons exécuter le fichier
de lecture de sondes ``lireSondes.py``, puis afficher le signal de houle 
mesuré par ces sondes.

.. code-block:: bash

    AllpostProcess lireSondes.py traceSondes.py

.. NOTE::

    Pour la reconstruction de spectre, la commande à lancer
    est 

    .. code-block:: bash

        AllpostProcess lireSondes.py resample.py spectre.py

    Qui correspond à la lecture de sondes, rééchantillonnage du signal
    et reconstruction de spectre.
