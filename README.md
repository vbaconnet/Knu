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

