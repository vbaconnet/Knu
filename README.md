# Knu (Canal Numérique) - ACRI-IN

## Description

Ensemble de scripts, fonctions, et outils pour l'automatisation des simulations
d'ACRI-IN. Les simulations peuvent être classées en 3 catégories:

- Houle : solveur diphasique eau/air pour tout ce qui concerne les simulations
type franchissement, débordement, interaction fluide-structure, etc. 
Le solveur supporte la mise en place d'écoulements en milieu poreux.

- Transport de sédiments : solveur *sedFoam* diphasique eau/milieu granulaire 
pour du	transport de sédiments. Le solveur modifié *sedPassiveScalarFoam*
implémente le transport d'un "scalaire passif" type colorant.

## Installation

```bash
git clone https://github.com/victor13165/Knu
cd Knu
source sourceMe
```
Pour utiliser les scripts Python, il est préférable d'installer les versions de ``numpy``, ``scipy`` et ``matplotlib`` données dans ``requirements.txt``:
```
pip install requirements.txt
```

**ATTENTION**
Pour l'instant, le calcul du débit de franchissement nécéssite que le module `paraview.simple` puisse être importé. Il faut avoir installé paraview. Ce script va prochainement être modifié pour ne pas avoir à se reposer sur Paraview et utiliser directement l'intégration volumique d'OpenFOAM.

## Support

victor.baconnet@acri-in.fr
