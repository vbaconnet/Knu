"""
Informations
============

    * Auteur: Victor Baconnet
    * Date de dernière modification: 31 mai 2021

Description
===========

Fonctions pour générer un spectre JONSWAP et les coefficients d'amplitude, périodes,
et déphasages pour générer le signal de houle irrégulière.

Utilisation
===========

Les fonctions contenues dans ce fichier sont à réutiliser dans d'autres fichiers 
pour générer de la houle irrégulière, comme dans ``genWaveProperties``.

L'éxecution de ce fichier affichera 2 graphiques:
    
* Spectres de JONSWAP pour différents coefficients d'élancement
* Exemple de signal de houle irrégulière

Les coefficients pour le spectre JONSWAP peuvent être spécifiés dans un fichier
nommé "jonswapDict" formaté comme suit::
    
  Tp 1.78
  Tmin 1.0
  Tmax 3.0
  Hs 1.5
  gamma 3.2
  scale (ou échelle) 25.0 //optionnel

Options d'exécution
====================

--savefigs     sauvegarder les graphiques générés dans le dossier d'éxection

Dépendances
===========

* Pour l'utilisation des fonctions uniquement: ``numpy``
* Pour exécuter le fichier : ``numpy``, ``matplotlib``, ``sys``, 
  ``genWaveProperties``, ``outilsLecture``, ``onde``

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
    """Calcule le coefficient sigma = 0.07 si w < wp et 0.09 si w > wp, à partir d'une combinaison de
    fonctions de Heaviside. Cela permet de ne pas écrire avec des "if" pour gagner du temps si on utilise
    un vecteur w très grand. Sinon aucune utilité :)

    :param w: Valeur ou vecteur de fréquences en rad/s
    :type w: ``float`` ou ``numpy.ndarray``
    :param wp: fréquence pic en rad/s
    :type  wp:  ``float``
    :return: 0.07 si w < wp, 0.09 sinon
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


def genJonswapParams(Hs, Tp, gamma, w):
    """
    Calcule les amplitudes et déphasages pour générer une onde irrégulière

    :param Hs: Hauteur caractéristique
    :type Hs: ``float``
    :param Tp: Période pic
    :type Tp: ``float`` 
    :param gamma: Coefficient d'élancement
    :type gamma: ``float`` 
    :param w: Fréquence en rad/s
    :type w: ``float`` ou ``numpy.ndarray``
    
    :return: Amplitudes, déphasages (aléatoires entre 0 et 2pi) et Spectre Jonswap
    :rtype: ``float`` ou ``numpy.ndarray``
    """
    
    dw = w[1] - w[0]
    spectreJonswap = jonswap(Hs, Tp, gamma, w)
    
    amplitudes = np.sqrt(2.0 * spectreJonswap * dw) #Génération d'amplitudes
    dephasages = 2.0*np.pi*np.random.rand(len(w))   #Génération de déphasage entre 0 et 2pi
    
    return amplitudes, dephasages, spectreJonswap


# ============================= MAIN =======================================================

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    import genWaveProperties as gwp
    import outilsLecture as olec
    from outilsDivers import trace
    import sys
    
    # Sauvegarde des figures ou pas
    savefigs = olec.readOption(sys.argv, ["-savefigs","--savefigs"])
    
    #On essaie de récupérer les paramètres dans jonswapDict
    try: 
        param_dict = gwp.readParams("jonswapDict")
        Tmin,Tmax,Tp = param_dict["tmin"], param_dict["tmax"], param_dict["tp"]
        Hs,gamma = param_dict["hs"],param_dict["gamma"]
    
    #Sinon on utilise les coefficients ci-dessous
    except: 
        
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
    
    spectreJonswap1 = jonswap(Hs, Tp, gamma, w) #Calcul du spectre de jonswap
    spectreJonswap2  = jonswap(Hs, Tp, 3.3, w)  #Calcul du spectre de jonswap avec gamma = 3.3
    spectreJonswap3 = jonswap(Hs, Tp, 6.0, w)   #Calcul du spectre de jonswap avec gamma = 6.0

    amplitude1 = np.sqrt(2.0*spectreJonswap2*dw)   #Générer amplitudes
    amplitude2 = np.sqrt(2.0*spectreJonswap1*dw)    #Générer amplitudes gamma = 3.3
    amplitude3 = np.sqrt(2.0*spectreJonswap3*dw)    #Générer amplitudes gamma = 6.0
    
    #==========================================================================
    #-------------------- Affichage des figures de spectres -------------------
    #==========================================================================    
    
    plt.close('all')
    
    fig, axs = plt.subplots(figsize = (10,8), nrows = 2)

    trace(
        w, spectreJonswap1, 
        fig, axs[0],
        #label = fr"$\gamma = {gamma}$", 
        xmin = wmin, xmax = wmax, 
        xlabel = r"$\omega$ (rad/s)",
        ylabel = r"$S(\omega)$ ($m^2 s$)",
        title = r"Hs = {:.3f} m, Tp = {:.3f} s, $\omega_p$ = {:.3f}".format(Hs,Tp,wp),
        tight_layout = False
    )

    t = np.linspace(0.0,0.224*3600,1000)
    A, phi, spectre = genJonswapParams(Hs, Tp, gamma, w)

    houleIrreg = 0.0
    for i in range(len(A)):
        houleIrreg += A[i]*np.sin(w[i]*t + phi[i])

    trace(
        t, houleIrreg,
        fig, axs[1],
        #title = r"Hs = {:.3f} m, Tp = {:.3f} s, $\omega_p$ = {:.3f}, $\gamma$ = {:.2f}".format(Hs,Tp,wp, gamma),
        xlabel = "t (s)",
        ylabel = r"$\eta(t)$ (m)",
        xmin = t[0],
        xmax = t[-1]
    )

    if savefigs:
        plt.savefig(f"jonswap_Tp{Tp}_Hs{Hs}_gamma{gamma}.png")

    plt.show()