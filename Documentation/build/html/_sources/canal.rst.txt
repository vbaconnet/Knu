
.. outils documentation master file, created by
   sphinx-quickstart on Fri Apr 30 14:52:41 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Guide de programmation du canal
================================

Cette documentation présente la théorie et programmation du canal à houle
et la génération de houle irrégulière et de vagues scélérates. Les 
programmes de génération sont situés dans le dossier ``Knu/Scripts/Canal/``.

Utilisation rapide
-------------------

1. Allez dans le dossier ``Knu/Canal/houle_irreguliere``
2. Editez le fichier ``params.txt``. Pour plus d'informations, 
   lisez la sections sur le :ref:`rôle de chaque paramètre <controleprogramme>`.
3. Exécutez le fichier ``generer_irreguliere.m``
4. Récupérez les fichiers ``.dat`` et ``.volts`` générés.

Génération de houle irrégulière
--------------------------------

La génération de houle irrégulière se fait à partir d'un spectre JONSWAP,
avec la fonction ``jonswap`` dans le fichier ``jonswap.m``.

Le spectre de JONSWAP est calculé avec la formule suivante: 

.. math::

    S(\omega,a) = aH_s^2 \omega_p^4 \omega^{-5} e^{-\frac{3}{4}\left(
        \frac{\omega_p}{\omega}\right)^4} \gamma^b

avec

.. math::

    b=\exp{-\frac{(\omega - \omega_p)^2}{2\sigma^2\omega_p^2}}

et :math:`\sigma=0.07` si :math:`\omega < \omega_p`, :math:`\sigma=0.09` sinon. La constante
réelle :math:`a` peut être déterminée en utilisant la définition de :math:`H_s`

.. math::
    H_s = 4\sqrt{\int_{0}^{+\infty}{S(\omega,a)d\omega}}


De telle sorte que :

.. math::

    a = \frac{H_s^2}{16}\left(\int_{0}^{+\infty}{S(\omega, a=1)d\omega}\right)^{-1}

A partir du spectre, on peut obtenir les amplitudes de houle avec la formule

.. math::

   H_i = 2\sqrt{S_i\Delta\omega}

Où les :math:`S_i` sont les composantes du spectre discrétisé 
telles que :math:`S_i=S(\omega_i)`. Le nombre de fréquences :math:`\omega_i`
correspond au nombre de composantes de houle désiré, en général
de 1000. Le paramètre :math:`\Delta\omega` est le pas de discrétisation
du vecteur de fréquences, qui est constant.

Les déphasages peuvent être générés aléatoirement entre :math:`0`
et :math:`2\pi`. 

Avec ces données, on peut obtenir un signal de houle de type:

.. math::

   \eta(x=0,t) = \sum_{i=0}^{N}{\frac{H_i}{2}\cos{(-\omega_i t + \phi_i)}}

Théorie batteur-piston
-----------------------

Pour convertir ce signal de houle en signal de batteur, nous allons
utiliser la théorie de batteur piston. Le signal du batteur est
donné par:

.. math::

   x(t) = \sum_{i=0}^{N}{x_i(t)} = \sum_{i=0}^{N}{\frac{H_i}{\tau_i}\cos{(-\omega_i t + \phi_i)}}

où :math:`\tau_i` est donné par:

.. math::

   \tau_i = 2 \frac{\cosh{(2k_ih)} - 1}{\sinh(2k_ih) +  2k_ih}

Où les :math:`k_i` sont les nombres d'onde et :math:`h` la
hauteur d'eau initiale devant le batteur. Cette formule est
issue de la référence :

.. code-block:: none

   [Advanced series on ocean engineering 2] Robert G. Dean, 
   Robert A. Dalrymple - Water wave mechanics for engineers and scientists 
   (1991, World Scientific)

Consultable dans : ``T:\Services\Production\Sophia\Modelisation_Physique\_DOCUMENTATION``

Les nombres d'onde :math:`k_i` se calculent à partir de la
relation de dispersion :

.. math::

   \omega_i^2 = gk_i \tanh(k_i h)

Que l'on peut réécrire

.. math::

   \frac{1}{k_i} = \frac{g}{\omega_i^2}\tanh(k_i h)

Dans le programme de génération, cette équation est résolue par 
la méthode du point fixe dans la fonction ``dispersion`` 
du fichier ``deplacement_batteur.m``.

La fonction ``deplacement_batteur`` renvoie le signal 
:math:`x_i(t)`. Le programme principal additionne chaque :math:`x_i(t)`
pour obtenir le signal de batteur :math:`x(t)` (variable ``x_batteur``
dans le programme ``generer_irreguliere.m``).

Pour ne pas que le batteur fasse d'à-coups, une rampe linéaire
est appliquée au début et à la fin du signal, de telle sorte que
:math:`x(0) = 0` et :math:`x(t_{max}) = 0`. De même, le 
programme vérifie que le batteur ne se déplace pas plus de 
:math:`30\,cm`, ne subit pas de vitesses au dessus de :math:`2.5\,m/s`
et pas d'accélérations au dessus de :math:`0.7\,m/s^2`. Si
c'est le cas, le programme renverra un avertissement.

.. WARNING::

   C'est à vous de générer un signal adapté aux contraintes
   mécaniques du batteur. Le programme ne corrige pas le signal
   s'il n'est pas adapté.


.. _controleprogramme:

Contrôle du programme
----------------------

Le contrôle des paramètres se fait dans le fichier ``params.txt``:

.. code-block:: none

   Tmin 0.87
   Tmax 2.19
   Tp 1.57
   Hs 0.125		    
   gamma 3.3		    
   Ncomposantes 1000	    % Nombre de composantes de houle
   h 1.38			    % Hauteur d'eau devant le batteur
   duree_simu 100	            % Durée de la simulation
   rampe 10		    % Durée de la rampe en secondes
   fichier_sortie test1        	  % Nom du fichier de sortie (sans extension)
   fichier_dephasages dephasages.dat % Nom du fichier de déphasages
   afficher_graphiques 0 	    % Mettre à 1 pour afficher les graphiques
   sauvegarder_fichiers 1	    % Mettre à 0 pour ne pas sauvegarder les fichiers
   generer_dephasages 1	    % Mettre à 1 ou 0 pour générer ou non les déphasages

* Les 5 premiers paramètres ``Tmin``, ``Tmax``, ``Tp``, ``Hs`` et
  ``gamma`` servent à la génération du spectre JONSWAP. Les temps
  doivent être donnés en secondes et ``Hs`` en mètres.

* ``Ncomposantes`` permet de gérer le nombre de composantes de
  houle mononchromatique (i.e. le nombre de fréquences)

* ``h`` est la hauteur d'eau devant le batteur, en mètres

* ``duree_simu`` est la durée du signal temporel à générer,
  en secondes.

* ``rampe`` permet de gérer la durée de la rampe (au début
  et à la fin du signal). La rampe appliquée est une rampe 
  linéaire.

* ``fichier_sortie`` est le nom des fichiers de sortie au format
  ``.dat`` et ``.volts``.

* ``fichier_dephasages`` est le nom du fichier de déphasages,
  si l'utilisateur ne souhaite pas en générer des nouveaux. 
  La gestion de la génération aléatoire de déphasages se fait 
  avec le paramètre ``generer_dephasages``.

* ``afficher_graphiques`` permet d'afficher ou non le spectre 
  généré ainsi que le signal de batteur. 0 : ne pas afficher, 
  1: afficher.

* ``sauvegarder_fichiers`` permet de gérer l'écriture des fichiers
  ``.dat`` et ``.volts``. 0 : ne pas écrire les fichiers, 1 : 
  écrire les fichiers. 

* ``generer_dephasages`` permet d'indiquer si l'on souhaite 
  générer des nouveaux déphasages ou non. 0 : ne pas générer
  de déphasages. Dans ce cas, le programme va aller lire dans
  le fichier ``fichier_dephasages``. Si ce fichier n'existe pas,
  le programme renverra un avertissement. 1 : générer des 
  nouveaux déphasages entre :math:`0` et :math:`2\pi`. 

Vagues scélérates
------------------

Une vague scélérate est une focalisation de toutes les composantes
monochromatiques sur un même point :math:`x_s`, en un temps 
donné :math:`t_s`. Cette condition implique donc que chaque composantes
monochromatique soit maximale au point :math:`(x_s,t_s)`, c'est-à-dire:

.. math::

   \eta(x_s,t_s) = \sum_{i=0}^{N}{\frac{H_i}{2}}

Pour rappel, le signal de houle :math:`\eta(x,t)` est donné par

.. math::

   \eta(x,t) = \sum_{i=0}^{N}{\frac{H_i}{2}\cos{( k_i x - \omega_i t + \phi_i)}}

La condition de focalisation impose donc que : 

.. math::

   \phi_i = \omega_i t_s - k_i x_s

Ainsi, le signal de houle scélérate devient:

.. math::

    \eta(x,t) = \sum_{i=0}^{N}{\frac{H_i}{2}\cos{( k_i (x-x_s) - \omega_i (t-t_s))}}

Le programme ``generer_scelerate.m`` agit uniquement sur le 
déphasage :math:`\phi_i = \omega_i t_s - k_i x_s`.  Les paramètres
:math:`x_s` et :math:`t_s` doivent être donnés dans le fichier
``params.txt`` 

.. code-block:: none

   Tmin 0.87
   Tmax 2.19
   Tp 1.57
   Hs 0.125		    
   gamma 3.3		    
   xS 5.0			    % Coordonnée x du point de focus (m)
   tS 50.0			    % Temps du point de focus (s)
   Ncomposantes 1000	    % Nombre de composantes de houle
   h 1.38			    % Hauteur d'eau devant le batteur
   duree_simu 100	            % Durée de la simulation
   rampe 10		    % Durée de la rampe en secondes
   fichier_sortie test1        	  % Nom du fichier de sortie (sans extension)
   fichier_dephasages dephasages.dat % Nom du fichier de déphasages
   afficher_graphiques 0 	    % Mettre à 1 pour afficher les graphiques
   sauvegarder_fichiers 1	    % Mettre à 0 pour ne pas sauvegarder les fichiers
   generer_dephasages 1	    % Mettre à 1 ou 0 pour générer ou non les déphasages
