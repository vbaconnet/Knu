Afouillement sous un cylindre
===============================

Ce tutoriel est un tutoriel disponible avec l'installation 
de ``sedFoam``. Une description détaillée du tutoriel est donnée
sur son `site web <https://sedfoam.github.io/sedfoam/tutorials_2d3d.html#Scour2DCylinder>`_.

.. NOTE:: 

    Pour installer ``sedFoam``, rendez-vous sur https://github.com/sedfoam/sedfoam
    et suivez les instructions d'installation.

Le script ``Allrun`` vous permet de lancer le calcul automatiquement.

Une fonctionnalité intéressante utilisée dans les fichiers de ``sedFoam``
est l'intégration de morceaux de code dans le fichier ``0.orig/Ua`` 
par exemple. Cela permet de spécifier un profil de vitesse de type couche limite
en entrée:

.. code-block:: none

    inlet
    {
        type            codedFixedValue; 
        value           uniform (0 0 0);

        name    inlet;

        codeInclude
        #{
            #include "fvCFD.H"
        #};

        codeOptions
        #{
            -I$(LIB_SRC)/finiteVolume/lnInclude \
            -I$(LIB_SRC)/meshTools/lnInclude
        #};
        codeLibs
        #{
            -lfiniteVolume \
            -lmeshTools
        #};
        code
        #{
            const fvPatch& boundaryPatch = patch();
            const vectorField& Cf = boundaryPatch.Cf();
            vectorField& field = *this;
            scalar t = this->db().time().value(); // Accès au temps de simulation

            forAll(Cf, faceI) // Parcourir les faces du patch inlet
            {
               if (Cf[faceI].y() >= -0.025) 
               {
                  if (t <= 4.0)
                  {
                     field[faceI] = (0.1 + 0.9*(t/4.0))
                                     *vector
                                      (
                                         0.04318/0.41
                                         *log(30*(Cf[faceI].y()+0.025)
                                              /9e-4),
                                         0,
                                         0
                                       );
                  }
                  else
                  {
                     field[faceI] = vector
                                    (
                                       0.04318/0.41
                                       *log(30*(Cf[faceI].y()+0.025)
                                            /9e-4),
                                       0,
                                       0
                                    );
                  }
               }
               else
               {
                  field[faceI] = vector(0,0,0);
               }
            }
        #};
    }

La condition limite ``codedFixedValue`` permet d'intégrer du code. Notez l'inclusion
d'options de compilation avec ``codeInclude``, de librairies avec ``codeLibs``, et le code 
lui-même avec le mot-clé ``code``.

* Le code est écrit en C++

* L'accès aux éléments sur la face ``inlet`` se fait avec::

    const fvPatch& boundaryPatch = patch();

* La ligne ::

    const vectorField& Cf = boundaryPatch.Cf();

  permet d'avoir accès aux faces des éléments qui sont sur le patch ``inlet``,
  et c'est sur ces faces que nous allons modifier la valeur de la vitesse.

* Pour avoir accès aux coordonnées de chaque face du patch, utilisez::

    Cf[faceI].x();
    Cf[faceI].y();
    Cf[faceI].z();

  Notez que ``faceI`` est l'indice de la face désirée. Vous pouvez parcourir toutes 
  les faces d'un coup à l'aide d'une boucle ``forAll``::

    forAll(Cf, faceI)
    {
        // code
    }

Le reste est du C++ classique. N'hésitez pas à regarder les liens fournis sur la 
`page principale </index>` qui expliquent la programmation sous OpenFOAM.

.. WARNING::

    La simulation pour ce cas est lancée en parallèle avec 16 processeurs. 
    Vérifiez que vous avez les ressources disponibles, ou diminuez
    le nombre de processeurs.
    