"""
Informations
============

    * Fichier : ``Knu/Scripts/Librairies/outilsDivers.py``
    * Auteur: Victor Baconnet
    * Date de dernière modification: 27 août 2021


Description
===========

Fonctions non-triées pour effectuer des opérations diverses, notamment:

  * Recherche de valeur dans un itérable : ``find()``
  * Calcul de RMSE (Root Mean Squared Error) : ``RMSE()``
  * Afficher un message d'erreur : ``error()``
  * Afficher un warning : ``warning()``
  * Afficher des graphiques bien organisés : ``plot()``
  

Utilisation
===========

Les fonctions sont à importer directement dans vos programmes.

L'exécution de ce fichier ne produira aucun résultat.

Fonctions
=========

"""

def find(tab, value, default = None):
    """
    Trouve l'index de la première valeur cherchée dans un itérable
    
    :param tab: Itérable dans lequel chercher
    :type tab: Iterable (list, tuple...)
    :param value: Valeur à chercher
    :param default: valeur par défaut à renvoyer si value n'est pas trouvée.
    :return: idx, la position de la première occurence de la valeur recherchée.
    :rtype: int
    """
    for idx,val in enumerate(tab):
        if val == value:
            return idx
    return default


def RMSE(y1, y2):
    """Calcule la racine de l'erreur quadratique moyenne, ou en anglais Root Mean
    Squared Error (RMSE), entre deux tableaux (itérables) y1 et y2
    
    :param y1: Première variable
    :type y1:  numpy.darray, list
    :param y2: Deuxième variable
    :type y2:  numpy.darray, list
    :return: Racine de l'erreur quadratique moyenne
    :rtype: float
    """
    from numpy import sqrt
    
    assert len(y1) == len(y2)
    
    res = 0.0
    
    for i in range(len(y1)):
        
        res += (y1[i] - y2[i])**2
    
    return sqrt(res)/len(y1)

def error(message: str, errorType: Exception):
    """Afficher un message d'erreur et quitter le programme
    
    :param message: message à afficher
    :type message: ``str``
    :param errorType:
    :type errorType: ``Exception``
    :raises ``errorType``: Lever exception
    """
    print("\n** Erreur **", message)
    raise errorType

def warning(message: str):
    """Afficher un warning
    """
    print("\n** Warning **", message)

def plot(x, y, fig, ax, label = "", xlabel = "", ylabel = "", title = "", grid = True,
        tick_fontsize = 14, label_fontsize = 16, xmin = None, xmax = None, ymin = None,
        ymax = None, legend = None, tight_layout = True):
    """Tracer (x,y) sur un graphique.
    
    :param x: Abcisses
    :type x: ``iterable``
    :param y: Ordonnées
    :type y: ``iterable``
    :param fig: Objet figure
    :type fig: matplotlib.figure.Figure
    :param ax: Objet axe
    :type ax: matplotlib.axes._subplots.AxesSubplot
    :param label: Légende de la courbe
    :type label: str
    :param xlabel: Nom de l'axe x
    :type xlabel: str
    :param ylabel: Nom de l'axe y
    :type ylabel: str
    :param title: titre du graphique
    :type title: str
    :param grid: Mettre à true pour afficher la grille
    :type grid: bool
    :param tick_fontsize: Taille de police des graduations
    :type tick_fontsize: int
    :param label_fontsize: Taille de police des titres et légendes
    :type label_fontsize: int
    :param xmin: Borne min de l'axe x
    :type xmin: float
    :param xmax: Borne max de l'axe x
    :type xmax: float
    :param ymin: Borne min de l'axe y
    :type ymin: float
    :param ymax: Borne max de l'axe y
    :type ymax: float
    :param legend: Afficher la légende ou non. Si ``label`` est définie, se met
       automatiquement à True.
    :type legend: bool
    :param tight_layout: Reformatage de la fenêtre de la figure pour faire rentrer
       les titres etc. Par défaut à True.
    :type tight_layout: bool
    :returns: Objet ligne issu de la commande ax.plot(), récupérable pour la
       gestion d'animations
    :rtype: matplotlib.lines.Line2D
    """
    
    if legend is None:
        legend = True if label != "" else False

    line, = ax.plot(x, y, label = label)

    if legend:
        ax.legend()

    ax.set_xlim((xmin, xmax))
    ax.set_ylim((ymin, ymax))

    ax.set_xlabel(xlabel, fontsize = label_fontsize)
    ax.set_ylabel(ylabel, fontsize = label_fontsize)
    ax.set_title(title, fontsize = label_fontsize)

    ax.tick_params(labelsize = tick_fontsize)
    
    ax.grid(b = grid)

    if tight_layout:
        fig.tight_layout()

    return line
