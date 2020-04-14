""" École Centrale de Lyon
    UE INF S8 Algorithmes collaboratifs et applications 2019-2020

    BE1 et 2 - Colonie de Fourmis
    1- L’implantation d’un système multi-agents de recherche du chemin le plus 
    court (PCC) suivant le principe de la Stigmergie et utilisant les 
    algorithmes génétiques.

    @author: Achraf Bella
    @author: Bruno Moreira Nabinger
"""

from zoneaffichage import *

class FileManager:

    def __init__(self, nomFichier=None):
        self.__listRoutes = [] # toutes les routes de l'environnement
        self.__listVilles = [] # toutes les villes de l'environnement
        if (nomFichier is None):
            nomFichier = "text"

#       'a' open for writing, appending to the end of the file if it exists
#       '+' 	open a disk file for updating (reading and writing)
        # file = open(nomFichier + '.towns', "a+")
        # file.close()
    
    def lireEnvironementDansFichier(self, nomFichier):
        """Lecture de l'environnement stocké dans fichier de même nom

        Parameters:
            nomFichier (string): nom du Fichier avec l'environnement et
                l'extension .town
        Returns:
            villeNid (Ville): Ville où se situe le nid
            villeFood (Ville): Ville où se situe la nourriture
            listVilles (list[Ville]): liste des toutes les villes de 
                l'environnement
            listRoutes (list[Route]): liste des toutes les routes de 
                l'environnement
        """
        self.__villeNid = None # Ville où se situe le nid
        self.__villeFood = None # Ville où se situe la nourriture
        self.__listRoutes = [] # toutes les routes de l'environnement
        self.__listVilles = [] # toutes les villes de l'environnement
        with open(nomFichier, 'r') as file:
            liste = file.read().splitlines()
            # print("Liste\n",liste)

            villeNidNom = liste[0]
            villeFoodNom = liste[1]
            listVillesSize = int(liste[2])
            listRoutesSize = int(liste[3])

            i = 4
            for j in range(i, i + listVillesSize):
                x, y, nom, = liste[j].split()
                ville = Ville(int(x), int(y), nom)
                self.__listVilles.append(ville)
            i = j + 1            
            for j in range(i, i + listRoutesSize):
                premiereVilleX, premiereVilleY, premiereVilleNom, \
                secondeVilleX, secondeVilleY, secondeVilleNom = liste[j].split()
                
                ville1 = None
                ville2 = None
                for ville in self.__listVilles:
                    if(ville.getX() == int(premiereVilleX) and
                       ville.getY() == int(premiereVilleY) and 
                       ville.getNom() == premiereVilleNom):
                       ville1 = ville
                    elif(ville.getX() == int(secondeVilleX) and
                       ville.getY() == int(secondeVilleY) and 
                       ville.getNom() == secondeVilleNom):
                       ville2 = ville
                route = Route(0, ville1, ville2)
                self.__listRoutes.append(route)

            for ville in self.__listVilles:
                if(ville.getNom() == villeNidNom):
                    self.__villeNid = ville
                elif(ville.getNom() == villeFoodNom):
                    self.__villeFood = ville

            # Identifie et stock les arêtes conectées
            for ville in self.__listVilles:
                ville.mesAretes(self.__listRoutes)
            
            self.printDataReadFromFile()
        file.close()
        return self.__listVilles, self.__listRoutes, \
               self.__villeNid, self.__villeFood
        

    def printDataReadFromFile(self):
        print("VilleNid :", self.__villeNid)
        print("VilleFood :", self.__villeFood)
        print("Villes")
        print(*self.__listVilles, sep='\n')
        print("Routes")
        print(*self.__listRoutes, sep='\n')    

    def sauverEnvironementDansFichier(self, nomFichier,
                                      listVilles, listRoutes,
                                      villeNid, villeFood):
        """Sauvagarde l'environnement stocké dans fichier de même nom

        Parameters:
            nomFichier (string): nom du Fichier avec l'environnement et
                l'extension .town
            villeNid (Ville): Ville où se situe le nid
            villeFood (Ville): Ville où se situe la nourriture
            listVilles (list[Ville]): liste des toutes les villes de 
                l'environnement
            listRoutes (list[Route]): liste des toutes les routes de 
                l'environnement
        Returns:
            None
        """
        with open(nomFichier + '.towns', 'w') as file:
            villeNidNom = villeNid.getNom()
            print("villeNidNom", villeNidNom)
            villeFoodNom = villeFood.getNom()
            print("villeFoodNom", villeFoodNom)
            listVillesSize = len(listVilles)
            print("listVilles", *listVilles, sep='\n')
            listRoutesSize = len(listRoutes)
            print("listRoutes", *listRoutes, sep='\n')
            file.write(str(villeNid.getNom())+"\n")
            file.write(str(villeFood.getNom())+"\n")
            file.write(str(listVillesSize)+"\n")
            file.write(str(listRoutesSize)+"\n")

            for ville in listVilles:
                file.write(str(ville.getX())  + " "
                           + str(ville.getY())  + " "
                           + str(ville.getNom())+"\n")

            for route in listRoutes:
                ville1 = route.getPremiereVille()
                ville2 = route.getSecondeVille()
                file.write(str(ville1.getX())  + " "
                           + str(ville1.getY())  + " "
                           + str(ville1.getNom())  + " "
                           + str(ville2.getX())  + " "
                           + str(ville2.getY())  + " "
                           + str(ville2.getNom())+"\n")
        file.close()