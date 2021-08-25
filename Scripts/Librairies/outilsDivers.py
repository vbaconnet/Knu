"""
Description
===========

Fonctions non-triées pour effectuer des opérations diverses.

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
    
    if grid:
        ax.grid()

    if tight_layout:
        fig.tight_layout()

    return line


def plot_multi(xs, ys, fig, axs, labels=[], xlabels = None, ylabels = None,
               titles = None, grids = True, tick_fontsize = 14, 
               label_fontsize = 16, xmins = None, xmaxs = None, ymins = None, 
               ymaxs = None, legend = None, tight_layout = True):

    assert len(xs) == len(ys)
    
    from numpy import size
    
    lines = []

    if legend is None:
        legend = True if len(labels) != 0 else False

    if size(axs) == 1:
        for idx in range(len(xs)):
            line, = axs.plot(xs[idx], ys[idx], label = labels[idx])
            lines.append(line)
    elif size(axs) == len(xs):
        for idx in range(len(xs)):
            line, = axs[idx].plot(xs[idx], ys[idx], label = labels[idx])
    else:
        raise ValueError(f"axs invalide. Doit être de taille 1 ou {size(axs)}")

    if legend:
        try:
            axs.legend()
        except AttributeError:
            for ax in axs:
                ax.legend()

    try:

        axs.set_xlim((xmins, xmaxs))
        axs.set_ylim((ymins, ymaxs))
    
        axs.set_xlabel(xlabels, fontsize = label_fontsize)
        axs.set_ylabel(ylabels, fontsize = label_fontsize)
        axs.set_title(titles, fontsize = label_fontsize)
        axs.tick_params(labelsize = tick_fontsize)
    
        if grids:
            axs.grid()
    
    except AttributeError:
        
        for idx, ax in enumerate(axs):
            
            ax.set_xlim((xmins, xmaxs))
            ax.set_ylim((ymins, ymaxs))
        
            ax.set_xlabel(xlabels, fontsize = label_fontsize)
            ax.set_ylabel(ylabels, fontsize = label_fontsize)
            ax.set_title(titles, fontsize = label_fontsize)

            ax.tick_params(labelsize = tick_fontsize)
            
            if grid[idx]:
                ax.grid()

    if tight_layout:
        fig.tight_layout()

    return lines
