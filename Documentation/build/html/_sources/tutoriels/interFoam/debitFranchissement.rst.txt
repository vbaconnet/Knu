Mesures de débit de franchissement
===================================

**Description de la situation**

Ce tutoriel est une copie de la géométrie de Port-La-Galère, pour montrer
comment mesurer un débit de franchissement.

La géométrie de Port-La-Galère utilisée porte le nom de "actuel2", et comporte 
une couche d'enrochements. Ci-dessous, vous trouverez la configuration
testée en canal réel lors de la campagne d'essais.

.. image /images/actuel2.png
   :width: 500
   :alt:Actuel2

Vous trouverez l'ensemble des commandes à effectuer dans les fichiers
``Allrun.case.serial`` ou ``Allrun.case.parallel`` selon si vous voulez
lancer la simulation en parallèle ou non.

.. code-block:: bash

    #!/bin/bash

    # Lancer le maillage
    Allmesh -eSc

    # Générer la houle irrégulière
    genHouleIrreguliere

    # Lancer le calcul. L'option -s lance setFields
    Allrun -st &

    # Attendre 5 secondes avant de lancer le monitoring
    sleep 5

    # Suivre la progression du calcul et lancer le calcul de débits de franchissement
    # lorsque terminé
    AllpostProcess debitFranchissement.py

**Maillage**

Pour générer le profil de la géométrie actuel2, il faut d'abord générer un maillage
de base dans lequel nous allons "découper". Ce maillage de base se génère avec l'outil 
``blockMesh``, selon les paramètres définis dans ``system/blockMeshDict``

.. code-block:: none

    xmin  0.0;
    xmax 30.0;
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


Lancez l'outil ``blockMesh`` avec la commande::

    $ blockMesh

Vous pouvez visualiser ce maillage avec ``ParaView``. La géométrie de Port-La-Galère
se trouve dans ``constant/triSurface/``, c'est le fichier ``actuel2.stl``. Avec 
``ParaView``, vous pouvez afficher la géométrie par dessus le maillage que vous venez
de générer pour visualiser où nous allons découper. Le deuxième fichier ``actuel2_enrochement.stl``
correspond à la zone d'enrochements. Vous pouvez aussi la visualiser avec ``ParaView``.

La découpe du maillage se fait avec l'outil ``snappyHexMesh``, selon les paramètres donnés
dans ``system/snappyHexMeshDict``. Ce fichier étant assez long, nous allons nous concentrer
sur les paramètres dont nous avons besoin pour ce tutoriel. Pour plus de détails sur l'utilisation
de ``snappyHexMesh``, consultez la `documentation <https://www.openfoam.com/documentation/guides/latest/doc/guide-meshing-snappyhexmesh.html>`_.

Dans un premier temps, nous définissons les zones avec lesquelles nous allons travailler:

.. code-block:: none

    geometry
    {
        actuel2.stl
        {
            type triSurfaceMesh;
            name actuel2;
        }

        interface
        {
            type   searchableBox;
            min    (-99  -99  0.8);
            max    (21.0  99  0.97);
        }

    }

Le premier sous-dictionnaire charge la surface nommée ``actuel2.stl``. Le mot-clé ``type triSurfaceMesh`` 
indique le type de maillage sur cette surface. Ne changez pas ce paramètre. Le mot-clé ``name`` permet de
donner un nom à cette surface. C'est ce nom que vous utiliserez pour faire référence à cette surface désormais.
Le deuxième sous-dictionnaire nous permet de sélectionner une zone, dans notre cas une boîte. Les dimensions 
sont telles que cette boîte englobe l'interface eau/air, dans laquelle nous allons raffiner le maillage. 
Vous pourrez visualiser le raffinement après avoir lancé ``snappyHexMesh``.

Une fois les zones définies, nous allons indiquer ce que nous souhaitons faire avec ces dernières. Cela se fait
dans le dictionnaire ``castellatedMeshControls``. Référez vous à la `documentation <https://www.openfoam.com/documentation/guides/latest/doc/guide-meshing-snappyhexmesh.html>`_
pour plus de détails. Dans ce dictionnaire, le contrôle de s'effectue dans le sous-dictionnaire ``refinementRegions``:

.. code-block:: none

    refinementRegions
    {
        actuel2
        {
            mode distance;
            levels ((0.15 1));
        }
        interface
        {
            mode inside;
            levels ((1 1));
        }
    }

Ce sous-dictionnaire nous permet d'indiquer où raffiner, et à quel niveau raffiner. 
Notez qu'il n'est pas nécessaire de raffiner, et que l'outil va découper par défaut
la géométrie ``actuel2``. En revanche, la zone ``interface`` n'aura aucune influence
tant qu'une instruction de raffinement ne sera pas donnée. La première instruction
concerne donc la géométrie ``actuel2``. Le mot-clé ``mode distance`` permet d'indiquer
que nous allons raffiner par rapport à la distance à cette surface. Le mot-clé 
``levels ((0.15 1))`` précise que nous allons raffiner 1 seule fois les mailles
qui se trouvent à :math:`0.15\,m` de notre surface ``actuel2``. Notez que vous pourriez
donner plusieurs niveaux pour plusieurs distances, en écrivant par exemple

.. code-block:: none

    actuel2
    {
        mode distance;
        levels ((0.15 3) (0.5 2) (1.2 1));
    }

Pour raffiner 3 fois à :math:`0.15\,m`, 2 fois à :math:`0.5\,m`, etc. La deuxième instruction
traite la zone ``interface``. le mot-clé ``mode inside`` indique que nous allons traiter
l'intérieur de la zone (on pourrait aussi traiter l'extérieur uniquement, du type
"raffiner tout sauf dans cette zone"). Le mot-clé ``levels ((1 1))`` indique que nous allons
raffiner une seule fois. Notez que le premier ``1`` n'est pas utilisé par ``snappyHexMesh``. Le
niveau de raffinement est à indiquer avec le deuxième chiffre.

.. NOTE::

    Un raffinement de niveau 1 signifie que chaque élément sera divisé en deux dans toutes les directions. 
    Par exemple, si un élément du maillage est de dimensions ``(1x2x1)``, un 
    raffinement de niveau 1 donnera 8 sous-éléments de dimensions ``(0.5x1x0.5)``.

Vous pouvez consulter le fichier ``system/snappyHexMeshDict`` pour voir tous les paramètres
qui existent. Le fichier est annoté pour expliquer au mieux à quoi servent les paramètres. 
Si vous rencontrez un problème, référez vous à la `documentation <https://www.openfoam.com/documentation/guides/latest/doc/guide-meshing-snappyhexmesh.html>`_.
Il existe aussi beaucoup de ressources, en particulier sur le forum cfd-online.com ou sur YouTube. Le problème
que vous avez a déjà été rencontré par quelqu'un avant vous, ``snappyHexMesh`` n'est pas un outil
simple à utiliser!

Lancez ``snappyHexMesh`` avec la commande::

    snappyHexMesh -overwrite

L'option ``-ovewrite`` permet d'écrire le nouveau maillage directement par-dessus le
maillage existant. Sans cette option, le nouveau maillage découpé sera écrit dans un 
autre dossier. 

``snappyHexMesh`` peut parfois effectuer des calculs assez lourds, selon
la taille de votre maillage de base et du niveau de raffinement demandé. 
Vous pouvez donc le lancer en parallèle pour gagner du temps. Pour cela,
configurez le fichier ``system/decomposeParDict`` comme suit:

.. code-block:: none

    numberOfSubdomains 4;

    method          hierarchical;

    coeffs
    {
        n           (4 1 1);
    }

Le premier mot-clé correspond au nombre de sous-domaines avec lequel vous allez
découper votre maillage. Il correspond au nombre de processeurs que vous allez utiliser.
Le mot-clé ``method   hierarchical`` permet d'indiquer la méthode de découpage. Il en existe
plusieurs, plus d'informations `ici <https://www.openfoam.com/documentation/guides/latest/doc/openfoam-guide-parallel.html>`_.
Enfin, le sous-dictionnaire ``coeffs`` vous permet d'indiquer le nombre de fois qu'il faut 
découper le maillage dans les 3 directions. Le produit des trois nombres doit être égal
au nombre de processeurs/sous-divisions. Par exemple, on aurait pu aussi donner ``n   (2 1 2)`` pour 
découper deux fois dans la directions :math:`\vec{x}`, une fois dans la direction :math:`\vec{y}`
et deux fois dans la direction :math:`\vec{z}`.

Découpez le maillage existant avec l'outil ``decomposePar``, avec la commande::

    decomposePar

Notez que de nouveaux dossiers ont été créés dans votre dossier courant, dont les noms sont 
``processor0``, ``processor1``, etc. Chaque sous-domaine du maillage est stocké dans son 
fichier processeur individuel. Pour lancer ``snappyHexMesh`` en parallèle, nous allons
utiliser l'utilitaire ``MPI``. Pour cela, lancez la commande::

    mpirun -n 4 snappyHexMesh -parallel -overwrite

.. WARNING::

    Si vous avez plus de 4 processeurs, pensez à modifier la commande.
    Pour ne pas avoir à ajuster ce nombre à chaque fois, vous pouvez 
    utiliser la commande ``runParallel``, en chargeant bien la bibliothèque d'OpenFOAM::

        . ${WM_PROJECT_DIR:?}/bin/tools/RunFunctions 
        runParallel snappyHexMesh -overwrite

Notez que nous utilisons l'option ``-parallel``, sans laquelle l'outil ne peut pas se lancer
en parallèle. Autrement dit, sans cette option, vous lancerez ``snappyHexMesh`` 4 fois indépendamment,
au lieu de lui indiquer d'aller travailler dans les fichiers processeurs ``processorN``.

Une fois le maillage terminé, vous pouvez le reconstruire à l'aide de la commande::

    reconstructParMesh -constant

Qui vous permet de reconstruire le maillage à partir des fichiers ``processorN``. L'option
``-constant`` permet d'écrire le maillage reconstruit dans le dossier ``constant/polyMesh``, là
où le maillage est stocké par défaut. Cette option fait quasiment le même travail que ``-overwrite``.

Supprimez les fichiers processeurs pour libérer de l'espace::

    rm -rf processor*

Une fois que ``snappyHexMesh`` est terminé, visualisez le maillage sous ``ParaView``. Lors 
de la découpe, les nouvelles faces créées ont été attribuées à une nouvelle condition limite 
(un nouveau ``patch``) nommé ``actuel2``.

Notez que le maillage initial généré avec ``blockMesh`` était en 2 dimension, c'est-à-dire
que le maillage n'avait qu'un seul élément dans la direction :math:`\vec{y}`, mais que ce
n'est plus le cas. En effet, ``snappyHexMesh`` va raffiner dans toutes les 
directions quel que soit le nombre d'éléments. Pour revenir à une géométrie 2D,
nous allons utiliser l'outil ``extrudeMesh``. Le paramétrage s'effectue dans ``system/extrudeMeshDict``:

.. code-block:: none

    constructFrom patch;    //surface;

    // If construct from (flipped) patch
    sourceCase ".";
    sourcePatches (backPlane);
    exposedPatchName backPlane;

    // Flip surface normals before usage.
    flipNormals false;

    // Do front and back need to be merged? Usually only makes sense for 360
    // degree wedges.
    mergeFaces false; //true;

    //- Linear extrusion in point-normal direction
    extrudeModel        linearNormal;

    nLayers          1; // was 20;

    linearNormalCoeffs
    {
        thickness       1.0; // was 0.05;
    }


Dans l'ordre d'apparition des paramètres, nous indiquons que nous allons extraire
le maillage depuis un ``patch``, c'est-à-dire une de nos conditions limites. Ensuite,
nous indiquons le chemin d'accès vers le dossier de travail, ici ``.``, et le patch
source à partir duquel extraire le maillage. Ici, nous utiliserons la face ``backPlane``.
Le mot-clé ``exposedPatchName  backPlane`` permet d'indiquer un nouveau nom à la face
extrudée. Le prochain paramètre important est ``extrudeModel      linearNormal`` qui 
indique que nous allone extruder selon une direction normale à la face d'extrusion. Le 
mot-clé ``nLayers   1`` indique le nombre d'éléments a créer après l'extrusion, dans la
direction de cette dernière. C'est cela qui va nous permettre de revenir vers un maillage 2D.
Notez que la direction normale à ``backPlane`` est bien la direction :math:`\vec{y}`. Si
vous n'êtes pas convaincu, aidez-vous de ``ParaView``. Le dernier sous-dictionnaire
``linearNormalCoeffs``, et le mot-clé ``thickness       1.0`` contrôle la distance 
d'extrusion. Ici, nous allons extraire sur 1 mètre, c'est-à-dire que notre 
géométrie aura une épaisseur de 1 mètre.

Lancez l'outil avec la commande::

    extrudeMesh

Toutes ces étapes peuvent se faire avec une seule commande::

    Allmesh -peS

Pour ne pas lancer en parallèle, omettez l'option ``-p``. 

Félicitations! Votre maillage est maintenant prêt à l'emploi.

**Génération de houle**

Nous allons soumettre notre ouvrage à de la houle irrégulière. La génération 
suit le même principe que le tutoriel de :doc:`houle irrégulière <houleIrreguliere>`.

Les paramètres de houle sont donnés dans le fichie ``jonswapDict``.

.. code-block::

    Tmin  5.3
    Tmax  13.2
    Tp    9.5
    Hs    2.8
    gamma 1.0
    scale 28.6 
    Ncomposantes 1000

Générez le fichier de houle irrégulière avec la commande::

    genHouleIrreguliere

Vérifiez le fichier ``constant/waveProperties`` et modifiez ce dont vous avez 
besoin.

**Enrochements**

Pour prendre en compte les enrochements, nous allons utiliser une modélisation
de Darcy-Forchheimer. Pour plus de détails, consultez la `documentation <https://openfoamwiki.net/index.php/DarcyForchheimer>`
sur le modèle de porosité. Si vous y avez accès, mon rapport de stage présente les théories
de modélisation en milieu poreux.

Dans un premier temps, il faut créer la zone d'enrochements, en prenant en 
compte la surface ``constant/triSurface/actuel2_enrochement.stl``. Pour cela, 
nous allons utiliser l'utilitaire ``topoSet``. Configurez l'outil avec le fichier
``system/topoSetDict``.

.. code-block:: none

    actions
    (

    // * * * * * * Zone d'enrochements * * * * * * * * * *

        {
            name    porousCellSet;
            type    cellSet;
            action  new;
            source  surfaceToCell;
            file    "constant/triSurface/actuel2_enrochements.stl";
            outsidePoints
            (
                (10.0 0.5 1.0)
            );

            includeCut      true;
            includeInside   true;
            includeOutside  false;
            nearDistance    -1;
            curvature       -100;
        }

        {
            name actuel2_enrochements;
            type cellZoneSet;
            action new;
            source setToCellZone;
            sourceInfo
            {
                set porousCellSet;
            }

        }

    );


Le premier sous-dictionnaire permet de sélectionner la zone délimitée par 
la surface sous la forme d'un ``cellSet``. Utilisez le mot-clé ``source surfaceToCell``
pour indiquer que la zone provient d'un fichier de surface, et indiquez son chemin
d'accès avec ``file "constant/triSurface/actuel2_enrochements.stl"``. Le mot-clé
``oustidePoints`` doit être un point en dehors de la zone de la surface.

Le deuxième sous-dictionnaire permet de convertir le ``cellSet`` en une ``cellZone``.
Nous nommons cette ``cellZone`` avec le mot-clé ``name actuel2_enrochements``. C'est 
avec ce nom que nous feront référence à la ``cellZone``.

Les paramètres du milieu poreux sont donnés dans le fichier ``constant/fvOptions``:

.. code-block:: none

    porosity1
    {
        type            explicitPorositySource;

        explicitPorositySourceCoeffs
        {
            selectionMode   cellZone;
            cellZone        actuel2_enrochements;

            type            DarcyForchheimer;

            d   (211.7 211.7 211.7);
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
s'indique avec le mot-clé ``cellZone  actuel2_enrochements``. Les coefficients
du modèle de Darcy-Forchheimer sont les vecteurs ``d`` et ``f``. Ce sont
des vecteurs car vous pouvez préciser des coefficients différents selon chaque direction.
Nous considérons un matériau homogène et isotrope, donc nos coefficients sont les mêmes
dans chaque direction.

Ne lancez pas encore ``topoSet``, nous avons quelques choses à ajouter avant.

**Débit de franchissement**

Pour calculer le débit de franchissement, il faut mesurer le volume d'eau dans 
le bac de récupération. Dans un premier temps, définissez la zone de votre bac 
de récupération en ajoutant le sous-dictionnaire suivant à ``system/topoSetDict``:

.. code-block:: none

    {
        name    bacCellSet;
        type    cellSet;
        action  new;
        source  boxToCell;
        box     (21.6 -2 -2) (22.0 2 2);
    }

    {
        name    bac;
        type    cellZoneSet;
        action  new;
        source  setToCellZone;
        set     bacCellSet;
    }

Vous commencez à y être habitué: on délimite la zone du bac par une boîte
dont on donne les dimensions. Cela va sélectionner les éléments du maillage
dans cette zone, sous la forme d'un ``cellSet``. Ensuite, nous convertissons
ce ``cellSet`` en un ``cellZone``, que nous nommons ``bac``.

Pour mesurer le volume d'eau dans le bac, nous allons effectuer une intégrale
de volume sur chaque élément du maillage de la ``cellZone`` :

.. math::

    V_{eau} = \iiint_{bac}{\alpha \delta V}

Où :math:`\alpha` est la variable ``alpha.water``. Pour calculer cette intégrale,
il faut se rendre dans le fichier ``system/controlDict``:

.. code-block::

    functions
    {

        waterVolume
        {
            type            volFieldValue;
            libs            ("libfieldFunctionObjects.so");
            log             true;

            enabled         true;

            writeControl    adjustableRunTime;
            writeInterval   20;

            writeFields     true;

            regionType      cellZone;
            name            bac;

            operation       volIntegrate;
            fields
            (
                alpha.water
            );

        }
    }

Il y a 3 choses importantes ici:

1. Le nom de la zone dans laquelle intégrer. Indiquez qu'elle est de type ``cellZone``
   avec le mot-clé ``regionType cellZone``, puis son nom avec le mot-clé ``name bac``.

2. L'opération "intégrale de volume" s'indique dans le paramètre ``operation  volIntegrate``,
   et le champ à intégrer est bien ``alpha.water``, à mettre dans la liste ``fields``.

3. L'intervalle d'écriture des valeurs se contrôle avec les mot-clés ``writeControl`` et 
   ``writeInterval``. Le premier vous permet d'indiquer si vous voulez écrire par itération (``timeStep``),
   ou par valeur de temps directement (``adjustableRunTime`` si vous utilisez un pas de temps adaptatif,
   ``runTime`` pour un pas de temps constant). Le mot-clé ``writeInterval`` correspond à l'intervalle
   d'écriture. Dans notre cas, nous écrivons toutes les 20 secondes. Si vous auriez voulu écrire
   toutes les 5 itérations, vous auriez écrit:

      .. code-block::

        writeControl    timeStep;
        writeInterval   5;

Vous êtes presque prêt(e) à lancer la simulation!

**solveur**

Il ne nous manque plus que les conditions limites. Allez voir les fichiers
dans le dossier ``0.orig`` pour les vérifier. Notez qu'il faut ajouter
des conditions limites pour notre ouvrage ``actuel2``, car nous
avons créé de nouvelles faces lors de la découpe du maillage. Toutes les faces 
(ou ``patch``) doivent être traités. Notez que ``actuel2_enrochements`` n'est
pas un patch, car nous n'avons pas découpé dans le maillage, seulement défini 
une zone dans laquelle appliquer le modèle de porosité.

Vous pouvez maintenant lancer ``topoSet``, et ``setFields``, qui va initialiser
une hauteur d'eau de :math:`0.864\,m`. Pensez à bien créer le dossier ``0`` en copiant
le dossier ``0.orig`` avant de lancer ``setFields``::

    topoSet
    cp -r 0.orig 0
    setFields

Vous êtes maintenant prêt à lancer la simulation. Ajustez
vos paramètres de simulation dans ``system/controlDict``. Par défaut,
la durée de simulation est de 2000 secondes pour simuler une durée
de tempête. Ce calcul vous prendra du temps: réduisez la durée de simulation
si besoin. Lancez le solveur et redirigez la sortie dans un fichier log avec la commande::

    interFoam > log.interFoam &

Pour lancer le calcul en parallèle, relancez ``decomposePar`` et utilisez
la même syntaxe que pour ``snappyHexMesh``::

    decomposePar
    mpirun -n 4 interFoam -parallel > log.interFoam &

Ce calcul étant assez long, vous pouvez augmenter le nombre de processeurs à 8 ou 12
si besoin.

.. NOTE::

    Toutes ces étapes peuvent être lancées directement avec la commande::

        Allrun -pst

    Pour ne pas lancer en parallèle, omettez l'option ``-p``

**Surveillance du statut de la simulation et post-traitement**

La commande ``AllpostProcess`` permet de lancer des scripts une fois 
que la simulation sera terminée. Lancez la commande::

    AllpostProcess debitFranchissement.py

Lorsque la simulation sera finie, le script ``debitFranchissement.py``
va aller lire les mesures de volume et les convertir en débit de 
franchissement. Le résultat sera écrit dans le fichier ``debitFranchissement.csv``.
Libre à vous d'afficher et de traiter ces données comme vous le souhaitez.
