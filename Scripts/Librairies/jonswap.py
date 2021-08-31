"""
Informations
============

    * Fichier : ``Knu/Scripts/Librairies/jonswap.py``
    * Auteur: Victor Baconnet
    * Date de dernière modification: 27 août 2021

Description
===========

Fonctions pour générer un spectre JONSWAP et les coefficients d'amplitude, périodes,
et déphasages pour générer le signal de houle irrégulière. 

Génération du spectre
----------------------

Le spectre de JONSWAP est généré selon la formule suivante

.. math::
    
    S(\omega,a) = aH_s^2 \omega_p^4 \omega^{-5} e^{-\\frac{3}{4}\\left( 
        \\frac{\omega_p}{\omega}\\right)^4} \gamma^b

avec 

.. math::
    
    b=\exp{-\\frac{(\omega - \omega_p)^2}{2\sigma^2\omega_p^2}}
   
et :math:`\sigma=0.07` si :math:`\omega < \omega_p`, :math:`\sigma=0.09` sinon. La constante 
réelle :math:`a` peut être déterminée en utilisant la définition de :math:`H_s`

.. math::
    H_s = 4\sqrt{\int_{0}^{+\infty}{S(\omega,a)d\omega}}


De telle sorte que :

.. math::
    a = \\frac{H_s^2}{16}\\left(\int_{0}^{+\infty}{S(\omega, a=1)d\omega}\\right)^{-1}


Génération des amplitudes
--------------------------

Les hauteurs crête-à-creux sont générées avec la relation:
    
.. math::
    \\frac{H_i}{2} = \sqrt{S_i\Delta\omega}

Génération des déphasages
--------------------------

Les déphasages sont générés aléatiroement entre :math:`0` et :math:`2\pi`.

Utilisation
===========

Les fonctions contenues dans ce fichier sont à réutiliser dans d'autres fichiers 
pour générer de la houle irrégulière, comme dans ``genHouleIrreguliere``.

L'éxecution de ce fichier n'affichera aucun résultat.

Exemple d'utilisation
======================

.. code-block:: python
   
    import numpy as np
    import matplotlib.pyplot as plt    
    from jonswap import genJonswapParams, jonswap
    
    # Paramètre du spectre jonswap
    Tmin = 0.87
    Tmax = 2.19
    Tp = 1.57
    Hs = 0.125
    gamma = 3.3
    
    wmin = 2.0*np.pi/Tmax #Fréquence min
    wmax = 2.0*np.pi/Tmin #Fréquence max
    wp   = 2.0*np.pi/Tp   #Pulsation pic
    Ncomposantes = 1000
    dw = (wmax - wmin)/Ncomposantes #Incrément de fréquence
    w = np.arange(wmin,wmax+dw,dw)  #Génération du vecteur de fréquences
    
    # Génération des Amplitudes, déphasages et spectre
    spectre = jonswap(Hs,Tp,gamma,w)
    H, phi = genJonswapParams(spectre, w)
    
    # Génération de houle irrégulière
    t = np.linspace(0.0,100,1001)
    
    houleIrreg = 0.0
    for i in range(len(H)):
        houleIrreg += 0.5*H[i]*np.sin(w[i]*t + phi[i])
    
    # Affichage des résultats
    fig, axs = plt.subplots(figsize = (10,8), nrows = 2)
    
    axs[0].plot(w, spectre)
    axs[0].set_xlabel(r"$\omega$ (rad/s)")
    axs[0].set_ylabel(r"$S(\omega)$ (m²s)")
    axs[0].set_xlim((wmin, wmax))
    axs[0].grid()
    axs[0].set_title(rf"Spectre de paramètres Hs = {Hs}, Tp = {Tp} et $\gamma$ = {gamma}")
    
    axs[1].plot(t,houleIrreg)
    axs[1].set_xlabel("Temps (s)")
    axs[1].set_ylabel(r"$\eta(t)$ (m)")
    axs[1].set_xlim((0, 100))
    axs[1].grid()
    axs[1].set_title("Signal de houle irrégulière")

Dépendances
===========

* ``numpy``
* ``matplotlib``
* ``sys``, 

Code source
============

Lien vers le `code source <https://github.com/victor13165/Knu/blob/main/Scripts/Librairies/jonswap.py>`_

Fonctions
=========
"""

# ---------  module indispensable ----------------
import numpy as np
# ------------------------------------------------

def integre(vec,dx):
    """Intègre un vecteur selon la méthode des trapèzes 
    
    :param vec: Vecteur de valeurs à intégrer
    :type vec: ``numpy.ndarray`` ou itérable
    :param dx: Pas de discrétisation
    :type dx: ``float``
    :return: res : scalaire correspondant à l'intégrale du vecteur
    :rtype: ``float``
    """
    res = 0
    
    for i in range(len(vec)-1):
        res += (vec[i+1]+vec[i])*0.5
        
    return res*dx

def sigma(w,wp):
    """Calcule le coefficient :math:`\sigma = 0.07` si :math:`\omega < \omega_p` et 
    :math:`\sigma = 0.09` si :math:`\omega > \omega_p`, à partir d'une combinaison de
    fonctions de Heaviside. Cela permet de ne pas écrire avec des "if" pour 
    gagner du temps si on utilise un vecteur w très grand.

    :param w: Valeur ou vecteur de fréquences en rad/s
    :type w: ``float`` ou ``numpy.ndarray``
    :param wp: fréquence pic en rad/s
    :type  wp:  ``float``
    :return: 0.07 si :math:`\omega < \omega_p`, 0.09 sinon
    :rtype: ``float``
    """

    termeInferieur = 0.07 * np.heaviside(wp-w, 0.07);
    termeSuperieur = 0.09 * np.heaviside(w-wp, 0.00);
    return termeInferieur + termeSuperieur

def spectreJonswap(a, Hs, Tp, gamma, w):
    """Calcule le spectre de Jonswap avec la formule donnée dans le manuel du canal à houle

    :param a: le coefficient qui doit faire l'objet de l'optimisation
    :type a: ``float``
    :param Hs: hauteur caractéristique
    :type Hs: ``float``
    :param Tp: période pic
    :type Tp: ``float``
    :param gamma: Coefficient d'élancement
    :type gamma: ``float``
    :param w: vecteur de fréquences en rad/s
    :type w: ``numpy.ndarray``
    :return: vecteur densité spectrale de puissance de la même taille que w
    """
    wp = 2.0*np.pi/Tp
    t1 = a * Hs**2 * wp**4 * w**(-5)
    t2 = np.exp( -1.25*(w/wp)**(-4) )
    exposant = np.exp( -0.5 * (w-wp)**2 / (sigma(w,wp)**2 * wp**2) )
    t3 = gamma**exposant
    return t1*t2*t3


def jonswap(Hs, Tp, gamma, w):
    """Renvoie une densité spectrale de puissance selon le modèle JONSWAP, avec 
    le calcul de la constante a
    
    :param Hs: Hauteur caractéristique
    :type Hs: ``float``
    :param Tp: Période pic
    :type Tp: ``float`` 
    :param gamma: Coefficient d'élancement
    :type gamma: ``float`` 
    :param w: Fréquence en rad/s
    :type w: ``float`` ou ``numpy.ndarray``
    :return: Densité spectrale de puissance selon le modèle JONSWAP
    :rtype: ``float`` ou ``numpy.ndarray``
    """
    
    assert Tp != 0

    spectre = spectreJonswap(1.0, Hs, Tp, gamma, w) #Calcul du spectre avec a=1    
    dw = w[1] - w[0]
    a = ( Hs / (4.0 * np.sqrt(integre(spectre,dw))) )**2 
    return spectreJonswap(a, Hs, Tp, gamma, w) #Calcul du spectre avec cette valeur de a


def genJonswapParams(spectreJonswap, w):
    """
    Calcule les amplitudes, déphasages et spectre pour générer une onde irrégulière

    :param spectreJonswap: le spectre de densité d'énergie JONSWAP
    :type spectreJonswap: ``float``
    :param w: Fréquence en rad/s
    :type w: ``float`` ou ``numpy.ndarray``
    
    :return: Amplitudes et déphasages (aléatoires entre :math:`0` et :math:`2\pi`)
    :rtype: ``float`` ou ``numpy.ndarray``
    """
    
    dw = w[1] - w[0]
    
    H = 2.0 * np.sqrt(2.0 * spectreJonswap * dw) #Génération d'amplitudes
    dephasages = 2.0*np.pi*np.random.rand(len(w))   #Génération de déphasage entre 0 et 2pi
    
    return H, dephasages

