Digue flottante de Monaco
===========================

**Description de la situation**

Nous allons dans ce tutoriel reproduire la digue flottante de Monaco, 
que nous allons soumettre à de la houle, et analyser son mouvement en rotation. La géométrie de
la digue est donnée dans le fichier ``floatingBody/constant/triSurface/monaco_flottante.stl``.

Pour ce tutoriel, nous allons utiliser la technique de maillage dynamique de type "overset",
c'eest-à-dire qu'un morceau du maillage va se déplacer dans un maillage statique fixe. Pour
plus d'informations sur le maillage overset, consultez la `documentation <https://www.openfoam.com/documentation/guides/latest/doc/guide-overset.html>`_.

Comme d'habitude, le script ``Allrun.pre`` vous permet de lancer le calcul automatiquement.

**Maillage**

Dans un premier temps, nous allons générer le maillage qui va se déplacer: 
le maillage "overset". Pour cela, allez dans le dossier ``floatingBody``::

    cd floatingBody

Nous allons créer un maillage de base avec ``blockMesh``, dans lequel nous allons
découper la géométrie de la digue. Générez le maillage de base avec la commande::

    blockMesh

La configuration du ``system/blockMeshDict`` est un peu particulière, car nous
fixons toutes les faces du domaine au type ``overset``:

.. code-block:: none

    xmin -10;
    xmax 360;
    ymin -32;
    ymax 32;
    zmin -10;
    zmax 30;

    dx 1.5;

    Nx #calc "std::floor(($xmax - $xmin) / $dx)";
    Ny #calc "std::floor(($ymax - $ymin) / $dx)";
    Nz #calc "std::floor(($zmax - $zmin) / $dx)";

    vertices
    (
        ($xmin $ymin $zmin)
        ($xmax $ymin $zmin)
        ($xmax $ymax $zmin)
        ($xmin $ymax $zmin)

        ($xmin $ymin $zmax)
        ($xmax $ymin $zmax)
        ($xmax $ymax $zmax)
        ($xmin $ymax $zmax)
    );

    blocks
    (
        hex (0 1 2 3 4 5 6 7) ($Nx $Ny $Nz) simpleGrading (1 1 1)
    );

    edges
    (
    );


    boundary
    (
        sides
        {
            type overset;
            faces
            (
                (2 6 5 1)
                (1 5 4 0)
                (3 7 6 2)
                (0 4 7 3)
                (0 3 2 1)
                (4 5 6 7)
            );
        }
    );

C'est très important, car sans cela nous ne pourrons pas utiliser le maillage overset.
Le découpage de la digue se fait avec ``snappyHexMesh``. Les paramètres de ``snappyHexMesh``
ne seront pas expliqués ici, mais vous trouverez une explication dans le tutoriel de
:doc:`mesure de débit de franchissement<../interFoam/debitFranchissement>`. Lancez snappyHexMesh 
avec la commande::

    snappyHexMesh -overwrite

.. NOTE::

    Vous pouvez directement lancer ``blockMesh`` et ``snappyHexMesh``,
    en parallèle ou non, avec la commande::

        Allmesh -pS &
    
    Omettez l'option ``-p`` si vous ne souhaitez pas lancer en parallèle.

Visualisez la géometrie créée avec ``ParaView``.

Une fois que nous avons créé le maillage mobile, nous allons créer le maillage fixe.
Pour cela, allez dans le dossier ``background``::

    cd ../background

Nous n'aurons besoin que de lancer ``blockMesh``::

    blockMesh

Ce maillage est plus grand que le précédent, ce qui est normal
puisqu'il doit "contenir" le maillage mobile. A présent, 
nous allons fusionner les deux maillages avec l'outil ``mergeMeshes``.
Pour cela, lancez la commande::

    mergeMeshes . ../floatingBody -overwrite

L'ordre des options est le suivant::

    mergeMeshes <chemin_origine> <chemin_fils>

C'est-à-dire que l'on fusionne le maillage de ``floatingBody`` dans celui
de ``background``, et pas l'inverse.

Le maillage est prêt! Visualisez-le avec ``ParaView``. Voici un exemple
de visualisation:

.. image images/full_mesh
   :alt: maillage overset

**Configuration du maillage dynamique**

Pour utiliser le maillage overset, il faut d'abord sélectionner la zone
qui sera mobile. La zone mobile a été définie dans la création
du maillage ``floatingBody``. Lorsque nous avons utilisé ``snappyHexMesh``, nous avons
créé des nouvelles faces, que nous avons stocké dans le patch ``floatingBody``. Ainsi,
nous n'avons rien à faire de particulier, car nous pouvons directement utiliser ce patch
pour faire référence à la digue. La configuration du maillage dynamique se fait
dans le fichier ``constant/dynamicMeshDict``.

.. code-block:: none

    motionSolverLibs    (sixDoFRigidBodyMotion);

    dynamicFvMesh       dynamicOversetFvMesh;

    solver          sixDoFRigidBodyMotion;

    sixDoFRigidBodyMotionCoeffs
    {

        patches         (floatingObject);
        innerDistance   999.0;
        outerDistance   1000.0;

        mass            164286000;
        centreOfMass    (171.88 0.005 8.32);

        momentOfInertia (16011409852.7 1.6e+12 1.66e+12);

        rotule      (-2.87 0 8.0);

        report          on;
        accelerationRelaxation 0.6;
        accelerationDamping    0.9;

        solver
        {
            type Newmark;
        }

        constraints
        {
            fixedPoint
            {
                sixDoFRigidBodyMotionConstraint point;
                centreOfRotation $rotule;
            }

        }

        /*
            restraints
            {
                chaine1_horizontal
                {
                    sixDoFRigidBodyMotionRestraint linearSpring;
                    anchor              (326.0  -15.14 0.56);
                    refAttachmentPt     (326.0 -100.0  0.56);
                    stiffness           50000;
                    damping             0;
                    restLength          0;
                }
            }
        */
    }

Les paramètres importants sont les suivants:

* Indication de l'utilisation du solveur de maillage overset : ``dynamicFvMesh dynamicOversetFvMesh``
* **Solveur** de déplacement de la zone mobile : ``solver sixDoFRigidBodyMotion``
* **Zone** à faire bouger : ``patches (floatingBody)``
* **Important** : les mots-clés ``innerDistance`` et ``outerDistance`` correspondent respectivement à 
  la distance à laquelle les éléments qui doivent bouger avec la digue se situent, et à la distance maximale
  à partir de laquelle bloquer le maillage. Pour des simulations en maillage overset, ces distances doivent
  être en dehors du maillage, et de sorte ``innerDistance < outerDistance``.
* **Caractéristiques inertielles** de la digue::
    mass            164286000;
    centreOfMass    (171.88 0.005 8.32);
    momentOfInertia (16011409852.7 1.6e+12 1.66e+12);

  qui correspondent à la masse, aux coordonnées du centre de masse et au moment d'inertie de la digue.
  Vous pouvez calculer ces caractéristiques avec la commande ``surfaceInertia constant/triSurface/monaco_flottante.stl``.
  Attention, les calculs sont faits avec une masse volumique de :math:`1\,kg/m^3`, il faut donc faire attention 
  d'avoir la masse volumique de la digue (dans l'hypothèse d'une digue homogène).
* **Liaisons** de fixation de la digue ::

        fixedPoint
        {
             sixDoFRigidBodyMotionConstraint point;
             centreOfRotation $rotule;
        }

  La liaison de type ``point`` est une liaison rotule. Elle n'a besoin que d'un paramètre,
  le centre de rotation de la rotule. Ici nous avions défini au préalable la variable ``rotule (-2.87 0 8.0)``.
  Il existe d'autres types de liaisons, par exemple::
    
    axis 
    line 
    orientation 
    plane

  Pour un descriptif complet de chaque liaison, vous pouvez consulter la description des fichiers `.H`
  dans le dossier ``src/sixDoFRigidBodyMotion/sixDoFRigidBodyMotion/constraints`` de votre dossier
  d'installation OpenFOAM. Si vous ne savez pas où aller, essayez ce chemin::

    /mount/internal/work-in/apps/util/OpenFoam/v2006/Linux-4.18.0-240.1.1.el8_3.x86_64/OpenFOAM-v2006/src/sixDoFRigidBodyMotion/sixDoFRigidBodyMotion/constraints
* **Forces** : vous pouvez ajouter des forces appliquées sur la digue. Dans ce tutoriels, elles ne sont pas utilisées, mais l'instruction
  à indiquer dans ``constant/dynamicMeshDict`` est écrite en commentaire tout en bas du fichier::

    restraints
    {
        chaine1_horizontal
        {
            sixDoFRigidBodyMotionRestraint linearSpring;
            anchor              (326.0  -15.14 0.56);
            refAttachmentPt     (326.0 -100.0  0.56);
            stiffness           50000;
            damping             0;
            restLength          0;
        }
    }

  Dans cet exemple, nous avons ajouté une force de type ressort linéaire. Vous devez y préciser des 
  paramètres comme le point d'attache fixe, point d'attache sur la digue, raideur, amortissement,
  longueur au repos. 
  Il existe d'autres types de forces, que vous trouverez dans le dossier 
  ``src/sixDoFRigidBodyMotion/sixDoFRigidBodyMotion/restraints`` de votre dossier d'installation
  OpenFOAM. 
  Si vous ne savez pas où aller, essayez ce chemin::

    /mount/internal/work-in/apps/util/OpenFoam/v2006/Linux-4.18.0-240.1.1.el8_3.x86_64/OpenFOAM-v2006/src/sixDoFRigidBodyMotion/sixDoFRigidBodyMotion/restraints

Il reste une dernière étape à faire avant de lancer la simulation. Le maillage overset utilise
une variable nommée ``zoneID``, qu'il faut initialiser correctement. Cette initialisation se fait
dans le fichier ``system/setFieldsDict``, pour utiliser l'outil ``setFields``::

    defaultFieldValues
    (
        volScalarFieldValue alpha.water 0
        volScalarFieldValue zoneID 123
    );

    regions
    (
        boxToCell
        {
            box ( -999 -999 -999 ) ( 999 999 16 );
            fieldValues
            (
                volScalarFieldValue alpha.water 1
            );
        }


        cellToCell
        {
            set c0;

            fieldValues
            (
                volScalarFieldValue zoneID 0
            );
        }
        cellToCell
        {
            set c1;

            fieldValues
            (
                volScalarFieldValue zoneID 1
            );
        }

    );


Sans faire attention à l'initialisation de la hauteur d'eau, regardons les deux derniers
sous-dictionnaires. Dans le cellSet ``c0``, on fixe la ``zoneID=0``, et dans  
le cellSet ``c1``, on fixe la ``zoneID=1``. Ces cellSet sont définis dans ``system/topoSetDict``::

    actions
    (
        {
            name    c0;
            type    cellSet;
            action  new;
            source  regionToCell;
            insidePoints ((398 10 25));
        }

        {
            name    c1;
            type    cellSet;
            action  new;
            source  cellToCell;
            set     c0;
        }

        {
            name    c1;
            type    cellSet;
            action  invert;
        }
    );

La première instruction sélectionne la région de maillage ``background``, en 
faisant bien attention à ce que le point ``insidePoints`` soit à l'intérieur 
du maillage ``background`` mais à l'extérieur du maillage ``floatingBody``. Ainsi,
le cellSet ``c0`` contient le maillage ``background``. La seconde instruction copie
le cellSet ``c0`` vers un nouveau cellSet ``c1``. Enfin, on inverse la séléction
du cellSet ``c1``, pour sélectionner les éléments du maillage ``floatingBody``. Ainsi,
le cellSet ``c1`` contient le maillage ``floatingBody``.

Finalement, nous allons donc fixer ``zoneID=0`` dans le maillage ``background``, et 
``zoneID=1`` dans le maillage ``floatingBody``.

Lancez ``topoSet`` pour créer ``c0`` et ``c1``::

    topoSet

**Lancement de la simulation**

Nous y sommes presque. Nous n'irons pas en détails dans les conditions limites,
mais notez l'ajout du fichier ``0.orig/zoneID``, où nous avons ajouté des conditions
limites (qui n'ont aucune importance):

.. code-block:: none

    dimensions      [0 0 0 0 0 0 0];

    internalField   uniform 0;

    boundaryField
    {
        #includeEtc "caseDicts/setConstraintTypes"

        "(inlet|bottom|wall1|wall2|wall3)"
        {
            type            zeroGradient;
        }

        atmosphere
        {
            type            zeroGradient;
        }

        floatingObject
        {
            type            zeroGradient;
        }
    }

Pensez à créer le dossier ``0`` en copiant le dossier ``0.orig`` avant de lancer setFields::

    cp -r 0.orig 0
    setFields

Vous pouvez maintenant lancer la simulation::

    overInterDyMFoam > log.overInterDyMFoam &

.. WARNING::

    Cette géométrie est (très) lourde. Privilégiez le calcul parallèle!

Vous pouvez directement effectuer toutes ces étapes avec la commande::

    Allrun -psrt &

L'option ``-r`` permet de ne pas reconstruire les fichiers processeurs à la 
fin de la simulation, car ils sont très lourds et la reconstruction prend beaucoup de temps.
Libre à vous de l'enlever si vous le souhaitez.

**Surveillance de la simulation et post-traitement**

Le but de la simulation est de mesurer les angles de roulis, lacet, et tangage de la digue.
Si vous lisez la sortie du solveur overInterDyMFoam, vous remarquerez qu'à chaque itération
on peut voir des informations liées au mouvement de la digue:

.. code-block:: none

    6-DoF rigid body motion
        Centre of rotation: (-2.87 0 8)
        Centre of mass: (171.880000089 0.00500000105165 8.31995137852)
        Orientation: (1 -7.31678947183e-16 2.78234418913e-07 -1.82737563546e-16 1 3.28649674005e-09 -2.78234418913e-07 -3.28649674005e-09 1)
        Linear velocity: (0 0 0)
        Angular velocity: (-1.7030972555e-06 0.000144184008078 2.71368210221e-14)

Ce qui nous intéresse pour mesurer les angles, c'est la valeur de ``Orientation``.
En fait, la série de chiffres qui suit sont les coordonnées du référentiel lié à la digue.
La syntaxe de cette série de chiffres est :math:`(xx\,xy\,xz\,yx\,yy\,yz\,zx\,zy\,zz)`. Ainsi, le vecteur
:math:`\vec{x}` aura pour coordonnées :math:`(xx\,xy\,xz)`, et ainsi de suite.

Le script ``read_orientation`` permet de récupérer les coordonnées et les stocker dans un fichier
``orientation.csv``, et lit également chaque pas de temps et stocke le signal temporel dans le fichier
``time.csv``. Le script ``angles.py`` permet de calculer les angles à partir de l'orientation 
des vecteurs. Les calculs ont été obtenus à partir des formules classiques de matrices de rotation pour des changements
de repère. L'exécution de ``angles.py`` crée un fichier ``angles.csv`` dans lesquels les angles sont affichés. Pour rappel::

    alpha -> tangage (rotation axe y)
    beta  -> lacet   (rotation axe z)
    gamma -> roulis  (rotation axe x)

En attendant que la simulation termine, vous pouvez surveiller son statut et lancer
les scripts lorsqu'elle sera terminée::

    AllpostProcess ./read_orientation ./angles.csv

Puis, pour tracer les angles en fonction du temps ::

        traceSondes.py angles.csv

Lorsqu'elle sera terminée. 

.. NOTE::

    Le graphique n'est pas bien ajusté? Ajoutez les valeurs minimales et maximales
    de l'axe des ordonnées en paramètres supplémentaires si besoin ::

        traceSondes.py angles.csv -10 10