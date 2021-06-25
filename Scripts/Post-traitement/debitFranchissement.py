from paraview.simple import OpenFOAMReader
import sys
import numpy as np
import outilsParaview as opv
import outilsLecture as olec
import outilsDivers as odiv
from os.path import exists

def decoupage(Npoints, xmin, xmax):
    """
    Decoupage de l'intervalle [xmin,xmax] pour le placement de sondes afin 
    de calculer le débit de franchissement

    Paramètres d'entrée:
    -------------------
        - Npoints : nombre de points de calcul
        - xmin, xmax : bornes de l'intervalle (coordonnées x des extremités du bac de récupération)

    Sortie:
    -------
        - xLocations : vecteur de coordonnées x des points de calcul.

    Exemples:
    ---------

        --> Npoints = 1,  xmin = 0, xmax = 1 : xLocations = [0.5]
        --> Npoints = 2,  xmin = 0, xmax = 1 : xLocations = [0.333 0.666]
        --> Npoints = 3,  xmin = 0, xmax = 1 : xLocations = [0.25 0.5 0.75]

    """
    
    dx = xmax - xmin

    assert dx > 0.0
 
    xLocations = np.zeros(Npoints)

    for i in range(Npoints):
       xLocations[i] = xmin + (i+1)*dx/(Npoints+1)
       print("Probe {} :  x{} = {}".format(i,i,xLocations[i]))

    return xLocations


def debit(hauteur, largeurCanal, temps, echelle):
    """
    Calcule le débit de franchissement équivalent à partir d'une hauteur d'eau

    Paramètres d'entrée:
    --------------------
        - hauteur: hauteur d'eau en unité de longueur [L]
        - largeurCanal: largeur du canal en unité de longueur [L]
        - temps : temps pour lequel on souhaite calculer le débit en unité de temps [T]
        - échelle : Pour mettre le débit à l'échelle souhaitée (sans unité)

    Sortie:
    -------
        - débit de franchissement par unité de longueur en [L]*[L]/[T]
    """
    return hauteur*largeurCanal*echelle**1.5 / temps



#================================== Lecture des paramètres et options ======================================================

print("\n++ Lecture des options ++\n")

#Lecture du paramètre de fichier .foam, par défaut foam.foam
foamFile   = olec.readFileOption(sys.argv,
                                 ['-foamFile','--foamFile'],
                                 extension = "foam",
                                 default = "foam.foam")

#Lecture du paramètre de fichier de sortie .csv, par défaut sondes.csv
outputFile = olec.readFileOption(sys.argv,
                                 ['-outputFile','--outputFile'],   
                                 extension = "csv",
                                 default = "debit_franchissement.csv")

#----------- Besoin de lire dans le fichier openFOAM pour initialiser les temps min et max par défaut ---------------

print(" -> Ouverture de  {}".format(foamFile))

if exists(foamFile):    #Si le fichier .foam existe
    Foam1 = OpenFOAMReader( FileName = foamFile )  #Ouvrir le fichier .foam
else:
    raise NameError("{} n'existe pas".format(foamFile))   #Sinon, erreur le fichier n'existe pas

time=Foam1.TimestepValues #On récupère tous les temps
print("\nIntervalle de temps total : [{},{}]".format(time[0],time[-1]))

tmin = olec.readValueOption(sys.argv, ['-tmin', '--tmin'], default = time[0])
tmax = olec.readValueOption(sys.argv, ['-tmax', '--tmax'], default = time[-1])

hauteurRef = olec.readValueOption(sys.argv, ["-hauteurRef","--hauteurRef"], default = 0.945)

minIdx = odiv.find(time, tmin, default = 0)
maxIdx = odiv.find(time, tmax, default = -1)

if maxIdx == -1:
    time = time[minIdx:]
else:
    time = time[minIdx:maxIdx+1]

print("Intervalle de temps final : [{},{}]\n".format(time[0],time[-1]))
#-------------------------------------------------------------------------------------------------------------------

#Nombre de sondes dans le bac
Npoints = olec.readValueOption(sys.argv, ['-nPoints','-n','--nPoints','--n'], 
                               default = 5, 
                               valueType = int)
#Coordonnée min du bac
xmin    = olec.readValueOption(sys.argv, ['-xmin','--xmin'], 
                               default = 21.6)

#Coordonnée max du bac
xmax    = olec.readValueOption(sys.argv, ['-xmax','--xmax'], 
                               default = 22.0) 

#A utiliser si on ne veut pas print les valeurs dans le terminal
noWrite = olec.readOption(sys.argv, ['-noWrite','--noWrite'])

#Coordonnée de découpage y 
ySliceLocation = olec.readValueOption(sys.argv, ['-ySliceLocation','--ySliceLocation'], default = 0.5)

print("\n++ fin de lecture des options ++ \n")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

print("\n--> Découpage avec {} points dans [{},{}]".format(Npoints, xmin, xmax))

ok = input("Lancer le calcul? (n pour annuler):")

if ok == "n":
    raise NameError("Programme annulé")

#Coordonnées des points de calcul
xProbeLocations = decoupage(Npoints, xmin, xmax) #Découpage du domaine

print("\n--> Initialisation du probeDict()")
probeDict = dict()
for i in range(len(xProbeLocations)):
    nom = "x={:.2f}".format(xProbeLocations[i])
    print(nom)
    probeDict[nom]=xProbeLocations[i]

#----------------------------------- Slicing en Y -----------------------
print("Slicing en y = {}".format(ySliceLocation))
Slice1 = opv.ySlice(Foam1, ySliceLocation)
#-------------------------------------------------------------------------

#----- Slicing en X et contours + initialisation dict débit et hauteur d'eau ------
contourDict = dict()
hauteursEau = dict()
debits = dict()

for probeName in probeDict.keys():
    xProbeLocation = probeDict[probeName]
    tempSlice = opv.xSlice(Slice1, xProbeLocation)
    contourDict[probeName] = opv.contour(tempSlice)
    hauteursEau[probeName] = np.zeros(len(time))
    debits[probeName] = np.zeros(len(time))

#--------------------------------------------------------------------------------

#----------------------------------------------- Header -------------------------
fw = open(outputFile, "w")

header = "time[s]"
for probeName in probeDict.keys():
    header += ",h " + probeName+ "[m],Q " + probeName  + "[L/s/m]"
header += ", h moyenne [m],Q Moyen[L/s/m]"
fw.write(header+'\n')
#-------------------------------------------------------------------------------


#-------------------------- Calcul hauteur d'eau et débit ------------------------

hauteurMoyenneTotale = 0.0
debitMoyenTotal = 0.0
nMoyenneTotale = 0


for timeIndex in range(len(time)):

    print("\n-> Time {}".format(str(time[timeIndex])))
    
    dataToPrint = str(time[timeIndex])
  
    hauteurMoyenneProbe = 0.0

    for probeName in contourDict.keys():
     
        contour = contourDict[probeName]
        contour.UpdatePipeline(time[timeIndex])
        
        waterHeight = contour.GetDataInformation().DataInformation.GetBounds()[5]
        
        #Si il n'y a rien dans le bac 
        if waterHeight > 10.0 or waterHeight <  0.0:
            waterHeight = 0.0
            Q = 0
        else:
            waterHeight -= hauteurRef
            Q = 1000.0 * debit(waterHeight, 0.55, time[timeIndex], 28.6)
            hauteurMoyenneProbe += waterHeight          
 
        print("--> {} : ".format(probeName))
        print("  h = {:.3f} [m] \n  Q = {:.2f} [L/s/m]".format(waterHeight,Q))  
        
        dataToPrint += ",{:.3f},{:.2f}".format(waterHeight,Q)

    hauteurMoyenneProbe /= len(contourDict)     
    debitMoyenProbe = 1000.0*debit(hauteurMoyenneProbe, 0.55, time[timeIndex], 28.6)
    
    if hauteurMoyenneProbe > 10**-7:
        hauteurMoyenneTotale += hauteurMoyenneProbe
        nMoyenneTotale += 1
        debitMoyenTotal += debitMoyenProbe

    print("Moyenne au temps {} : dh = {}, Q = {}".format(str(time[timeIndex]),
                                                         hauteurMoyenneProbe,
                                                         debitMoyenProbe))

    dataToPrint += ",{:.3f},{:.2f}".format(hauteurMoyenneProbe, debitMoyenProbe)
    fw.write(dataToPrint + "\n")
#------------------------------------------------------------------------

fw.close()

if nMoyenneTotale != 0:
    hauteurMoyenneTotale /= nMoyenneTotale
    debitMoyenTotal /= nMoyenneTotale
else:
    hauteurMoyenneTotale = 0.0
    debitMoyenTotal = 0.0

longueurPrint =  max( len(str(hauteurMoyenneTotale)) , len(str(debitMoyenTotal))) -2

print("\n+++++++++++++++++++++++++++") 
print(  "+ Hauteur moyenne : {:.3f} +".format(hauteurMoyenneTotale))
print(  "+ Débit moyen     : {:.2f}  +".format(debitMoyenTotal))
print(  "+++++++++++++++++++++++++++")


