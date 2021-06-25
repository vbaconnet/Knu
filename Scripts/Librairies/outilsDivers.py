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
