""" École Centrale de Lyon
    UE INF S8 Algorithmes collaboratifs et applications 2019-2020

    BE1 et 2 - Colonie de Fourmis
    1- L’implantation d’un système multi-agents de recherche du chemin le plus 
    court (PCC) suivant le principe de la Stigmergie et utilisant les 
    algorithmes génétiques.

    @author: Achraf Bella
    @author: Bruno Moreira Nabinger
"""

from route import * # import classe Route à partir du fichier route.py

class Ville: # Declaration de la classe Ville
    """Représent les noeuds
    
    ***************************************************************************
    
    Attributs:
        x (int): Coordonné x de la ville
        y (int): Coordonné y de la ville
        nom (string): Nom de la ville
        aretesConectees (list[Route]): Liste des arêtes conectées à la ville
    """
    #  constructeurs
    def __init__(self, x, y, nom):
        self.__x = x # Coordonné x de la ville
        self.__y = y # Coordonné y de la ville
        self.__nom = nom # Nom de la ville
        self.__aretesConectees = [] # arêtes conectées à la ville

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y
    
    def getNom(self):
        return self.__nom

    def getAretesConectees(self):
        return self.__aretesConectees

    def updatePheromoneAretesConectees(self, listAretes):
        """Réalise la mise à jour de la phéromone des arêtes conectées
    
        Méthode qui réalise la mise à jour de la quantité de phéromone des
        arêtes stockées dans un objet ville. Cette méthode doit être appelée
        avant le choix de la nouvelle arête par l'agent
        
        Parameters:
            listAretes (list[Route]): liste des toutes les routes de 
                l'environement
        Returns:
            None
        """
        for aretesConectees in self.__aretesConectees:
            for arete in listAretes:
                if (aretesConectees.memeRoute(arete)):
                    aretesConectees.setPheromone(arete.getPheromone())


    def mesAretes(self, listAretes):
        """Identifie et stock les arêtes conectées
    
        Méthode qui identifie et stocke les arêtes conectées à la ville. Cette
        méthode doit être appelée après la création des villes et des routes
        
        Parameters:
            listAretes (list[Route]): liste des toutes les routes de 
                l'environement
        Returns:
            None
        """
        self.__aretesConectees = []
        for arete in listAretes:
            if (self == arete.getPremiereVille()):
                self.__aretesConectees.append(arete)
            elif (self == arete.getSecondeVille()):
                # aretesConectees.append(arete)
                self.__aretesConectees.append(Route(arete.getPheromone(), self,
                                                    arete.getPremiereVille()))
        # print(*self.__aretesConectees, sep='\n')

    #  constructeurs, interface et méthodes auxiliares etc
    def __str__(self): # Opérateur d’affichage utilisé par print
        # return 'Nom : {}, Coordonnées : ({}, {})' \
        return '{} ({}, {})' \
        .format(self.__nom, self.__x, self.__y)

# Test class Ville
if __name__ == '__main__':
    # Creation de cinq villes
    ville1 = Ville(60,30,"Lyon")
    ville2 = Ville(20,45,"Nantes")
    ville3 = Ville(45,60,"Paris")
    ville4 = Ville(50,80,"Lille")
    ville5 = Ville(70,10,"Marseille")
    print("Villes en France")
    print("\t1 Nom : ", ville1)
    print("\t2 Nom : ", ville2)
    print("\t3 Nom : ", ville3)
    print("\t4 Nom : ", ville4)
    print("\t5 Nom : ", ville5)