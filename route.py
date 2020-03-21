""" École Centrale de Lyon
    UE INF S8 Algorithmes collaboratifs et applications 2019-2020

    BE1 et 2 - Colonie de Fourmis
    1- L’implantation d’un système multi-agents de recherche du chemin le plus 
    court (PCC) suivant le principe de la Stigmergie et utilisant les 
    algorithmes génétiques.

    @author: Achraf Bella
    @author: Bruno Moreira Nabinger
"""

from ville import * # import classe Ville à partir du fichier ville.py
from math import sqrt

class Route:
    """Représent les arêtes du graphe
    
    Text***********************************************************************
    
    Attributs:
        longueur (int): Longueur de la route (arête)
        pheromone (float): Intensite de la phéromone sur la route, mésure par
            un nombre réel
        premiere (Ville): Ville connectée à cette route
        seconde (Ville): Ville connectée à cette route
    """

    #  constructeurs
    def __init__(self, pheromone, premiereVille, secondeVille):
        # Longueur de la route (arête)
        self.__longueur = sqrt( (secondeVille.getY() - premiereVille.getY())**2
                        + (secondeVille.getX() - premiereVille.getX())**2)
        self.__pheromone = pheromone # Intensite de la phéromone sur la route
        self.__premiereVille = premiereVille # Ville connectés à cette route
        self.__secondeVille = secondeVille # Ville connectés à cette route

    def getLongueur(self):
        return self.__longueur

    def getPheromone(self):
        return self.__pheromone

    def getPremiereVille(self):
        return self.__premiereVille

    def getSecondeVille(self):
        return self.__secondeVille

    # Simulation de l'évaporation de la phéromone
    def ajouterPheromone(self, pheromone): 
        """Représent l'évaporation de la phéromone

        Représent une augmentation de la quantité de la phéromone sur l'arête 
        du graphe.
        
        Parameters:
            pheromone (float): quantité de la phéromone ajouté sur la route,
                mésure par un nombre réel
        Returns:
            None
        """
        self.__pheromone = self.__pheromone + pheromone


    # Simulation de l'évaporation de la phéromone
    def evaporerPheromone(self, tauxEvaporation): 
        """Représent l'évaporation de la phéromone

        Représent une baisse générale de la quantité de la phéromone sur 
        l'arête du graphe par un facteur constant.
        
        Parameters:
            tauxEvaporation (float): réel choisi dans l'intervale [0,1], qui 
                répresent le taux d'évaporation
        Returns:
            None
        """
        self.__pheromone = (1 - tauxEvaporation) * self.__pheromone

    #  constructeurs, interface et méthodes auxiliares etc
    def isRoute(self, ville1, ville2):
        """Vérifie si la route relie deux Villes

        Parameters:
            ville1 (Ville): Ville potentiellement connectée à cette route
            ville2 (Ville): Ville potentiellement connectée à cette route
        Returns:
            bool: True indique que la route relie le deux villes
                False indique que la route ne relie pas le deux villes
        """
        if ((self.__premiereVille == ville1 and 
            self.__secondeVille == ville2) or (self.__premiereVille == ville2
            and self.__secondeVille == ville1)):
            return True
        return False

    def memeRoute(self, routeTest):
        """Vérifie si deux routes sont identiques

        Parameters:
            routeTest (Route): Route potentiellement identique à cette route
        Returns:
            bool: True indique que la route correspond à cette route
                False indique que la route ne correspond pas à cette route
        """
        if ((self.__premiereVille == routeTest.getPremiereVille() and 
            self.__secondeVille == routeTest.getSecondeVille()) or
            (self.__premiereVille == routeTest.getSecondeVille()
            and self.__secondeVille == routeTest.getPremiereVille())):
            return True
        return False

    def __str__(self): # Opérateur d’affichage utilisé par print
        return 'Ville1:{0} - Ville2:{1},  d={2:6.3f},' \
        ' pheromone={3:7.4f}'.format(self.__premiereVille, \
        self.__secondeVille, self.__longueur, self.__pheromone)
        # return 'Premier Ville : {0} - Seconde Ville : {1},  Longueur = {2:7.4f},' \
        # ' pheromone = {3:7.4f}'.format(self.__premiereVille, \
        # self.__secondeVille, self.__longueur, self.__pheromone)

# Test class Route
if __name__ == '__main__':
    # Creation de cinq villes
    ville1 = Ville(60,30,"Lyon")
    ville2 = Ville(20,45,"Nantes")
    ville3 = Ville(45,60,"Paris")
    ville4 = Ville(50,80,"Lille")
    ville5 = Ville(70,10,"Marseille")
    print("Villes en France")
    print("\t1 ", ville1)
    print("\t2 ", ville2)
    print("\t3 ", ville3)
    print("\t4 ", ville4)
    print("\t5 ", ville5)
    # Creation de quatre routes
    routeLyonNantes = Route(100, ville1, ville2)
    routeLyonParis = Route(100, ville1, ville3)
    routeLyonLille = Route(100, ville1, ville4)
    routeLyonMarseille = Route(100, ville1, ville5)
    print("Routes")
    print("\t1 ", routeLyonNantes)
    print("\t2 ", routeLyonParis)
    print("\t3 ", routeLyonLille)
    print("\t4 ", routeLyonMarseille)
    ville1.mesAretes([routeLyonNantes, routeLyonParis, routeLyonLille,
                    routeLyonMarseille])