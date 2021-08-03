# Knu (Canal Numérique) - ACRI-IN

## Description

Ensemble de scripts, fonctions, et outils pour l'automatisation des simulations
d'ACRI-IN. Les simulations peuvent être classées en 3 catégories:

- Houle : solveur diphasique eau/air pour tout ce qui concerne les simulations
type franchissement, débordement, etc. Le solveur supporte la mise en place 
d'écoulements en milieu poreux.

- Transport de sédiments : solveur *sedFoam* diphasique eau/milieu granulaire 
pour du	transport de sédiments. Le solveur modifié *sedPassiveScalarFoam*
implémente le transport d'un "scalaire passif" type colorant.

- Interaction fluide-structure avec maillage dynamique

## Installation

Téléchargez le code source
```bash
git clone https://github.com/victor13165/Knu
```
Allez dans le dossier ``Knu`` et initialisez les variables d'environnement
```bash
cd Knu
source sourceMe
```
Compilez les solveurs OpenFOAM ``sedFoam``, ``interFranchissementFoam``,
``olaFlow`` ainsi que les modèles de turbulence modifiés
``buoyancyModifiedTurbulenceModels`` et ``stabRAS``.
```bash
Allwmake
```
Si vous ne voulez pas tout compiler, allez dans le dossier qui vous intéresse
et lancez
```bash
<solver>/Allwmake
```
Où ``<solver>`` est le nom du solveur qui vous intéresse. 

Pour utiliser les scripts Python, il est préférable d'installer les versions 
de ``numpy``, ``scipy`` et ``matplotlib`` données dans ``requirements.txt``:
```
pip install requirements.txt
```

**ATTENTION**
Pour l'instant, le calcul du débit de franchissement nécéssite que le module
 `paraview.simple` puisse être importé. Il faut avoir installé paraview. 
Ce script va prochainement être modifié pour ne pas avoir à se reposer sur 
Paraview et utiliser directement l'intégration volumique d'OpenFOAM.

## Support

victor.baconnet@acri-in.fr
