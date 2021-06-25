"""
Description
===========

Liste de fonctions permettant d'interagir dans l'environnement paraview.

Fonctions
=========

"""

from paraview.simple import Slice, Contour


def ySlice(input, ySliceLocation):
    """Découpe le domaine en une surface dans le plan (x,z)

    :param inputElement: Element parent à partir duquel on va slice
    :type inputElement: dataset (peut être FoamFile ou Slice, Contour, etc...)
    :param ySliceLocation: coordonnée y pour la découpe
    :type ySliceLocation: float
    :return: ySlice : surface dans le plan (x,z) 
    :rtype: paraview.simple.Slice
    """
    #----------------- Slice dans le plan (x,z) ----------------
    # --> Passage de géométrie 3D à 2D (surface)
    #-----------------------------------------------------------
    ySlice = Slice(Input=input, SliceType="Plane" )
    ySlice.SliceType.Normal = [0.0, 1.0, 0.0]                 #Normale au plan de découpe
    ySlice.SliceType.Origin = [0.0, ySliceLocation, 0.0]      #Origine du plan de découpe (seulement position y est importante)

    return ySlice

def xSlice(input, xSliceLocation):
    """Découpe le domaine en une surface dans le plan (y,z)

    :param inputElement: Element parent à partir duquel on va slice
    :type inputElement: dataset (peut être FoamFile ou Slice, Contour, etc...)
    :param xSliceLocation: coordonnée x pour la découpe
    :type xSliceLocation: float
    :return: xSlice : surface dans le plan (y,z) 
    :rtype: paraview.simple.Slice
    """
    #----------------- Slice dans le plan (y,z) ----------------
    # --> Passage de géométrie 3D à 2D (surface)
    #-----------------------------------------------------------
    xSlice = Slice(Input=input, SliceType="Plane" )
    xSlice.SliceType.Normal = [1.0, 0.0, 0.0]                 #Normale au plan de dé$
    xSlice.SliceType.Origin = [xSliceLocation, 0.0, 0.0]      #Origine du plan de dé$

    return xSlice


def contour(input, field = "alpha.water", value = 0.5):
    """Découpe le domaine en une ligne selon l'axe z, puis renvoie le point où alpha.water = 0.5

    :param inputElement: Element parent à partir duquel on va slice
    :type inputElement: dataset (peut être FoamFile ou Slice, Contour, etc...)
    :param field: Variable à partir de laquelle faire le contour, par défaut "alpha.water"
    :type field: str, optional
    :param value: valeur de la variable à tracer, par défaut 0.5
    :type value: float, optional
    :return: contour : le contour où `field = value`
    :rtype: paraview.simple.Contour
    """

    #--- Contour pour récupérer l'interface à alpha = 0.5 ------
    # --> Passage de géométrie 1D à 0D (point)
    #-----------------------------------------------------------
    contour = Contour(Input=input, PointMergeMethod="Uniform Binning" )
    contour.ContourBy = ['POINTS', field]
    contour.Isosurfaces = [value]

    return contour
