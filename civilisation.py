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
from route import * # import classe Route à partir du fichier route.py
from ant import * # import classe Route à partir du fichier route.py

class Civilisation:
    """Représent l'environnement
    
    Contrôle l'ensemble de l'environnement, les procesus d'évolution et de 
    simulation.
    -Deux noeuds du graphe désignent le nid et la source de nourriture.
    -Au début de la simulation, on crée un nombre aléatoire d’agents dans le 
    nid.
    -À chaque tour, les agents effectuent des actions en fonction de leur
    position actuelle.
    -Pendant l’exécution de la simulation, les itinéraires les plus utilisés 
    verront leur niveau de phéromone augmenter et après quelque temps, une 
    solution émergera du comportement collectif de ces fourmis virtuelles.
    
    Attributs:
        nom (string): Nom de la civilisation
        villeNid (Ville): Ville où se situe le nid
        villeFood (Ville): Ville où se situe la nourriture
        nIndividus (int): Au début de la simulation, on crée un nombre 
            aléatoire d’agents dans le nid.
        probabiliteMutation (float): réel choisi dans l'intervale [0,1], qui 
           répresent la probabilité qu'une mutation se produise. Après un 
           croisement, il y a une faible probabilité de mutation.

        tauxEvaporation (float): réel choisi dans l'intervale [0,1], qui 
                répresent le taux d'évaporation 
    """
    #  constructeurs
    # nIndividus = randint(minIndividus, maxIndividus)
    def __init__(self, nom, villeNid, villeFood, nIndividus,
                 toursAvantselection, probabiliteMutation, 
                 tauxEvaporation):
        self.__nom = nom # Nom de la ville
        self.__villeNid = villeNid # Ville où se situe le nid
        self.__villeFood = villeFood # Ville où se situe la nourriture
        self.__nIndividus = nIndividus # Au début de la simulation, on crée un 
            # nombre aléatoire d’agents dans le nid.
        self.__listRoutes = [] # toutes les routes de l'environement
        self.__listVilles = [] # toutes les villes de l'environement
        self.__listAnts = [] # toutes les fourmis de l'environement
        # les tours restants avant la prochaine sélection (pour l'algorithme génétique)
        self.__selectionNaturelle = toursAvantselection
        self.__toursAvantselection = toursAvantselection # compteur
        self.__probabiliteMutation = probabiliteMutation
        self.__tauxEvaporation = tauxEvaporation
        self.__nouritureCollectee = 0

    def configTour(self):
        [ant.choixArete() for ant in self.__listAnts]
        print("FIRST\n*self.__listRoutes, size", len(self.__listRoutes), *self.__listRoutes ,sep="\n")


    def tourSuivant(self): 
        """Effectue un tour de la simulation

        Effectue un tour de la simulation, ou les fourmis réalisent ses 
        actions, l'évaporarion de la phéromone a lieu et la sélection est 
        réalisé lors du nombre de tours définie par selectionNaturelle

        Parameters:
            None
        Returns:
            None
        """
        for ant in self.__listAnts:
            finRoute = ant.avancer()
            # La fourmi avance. Si elle arrive au but, elle est dans une
            #  nouvelle ville.
            # Mise à jour de la phéromone lorsque les fourmis auront construit
            #  leur trajet
            if (finRoute == True):                
                ant.verifieVille(self.__villeFood)
                routeActuelle = ant.choixArete()

                # Augmentation : on met à jour la phéromone sur les arêtes
                #  empruntées
                for arete in self.__listRoutes:
                    if (arete == routeActuelle):
                        arete.ajouterPheromone(ant.deposerPheromone())
            
        # Évaporation : une baisse générale de la quantité sur toutes les 
        # arêtes du graphe par un facteur constant
        for arete in self.__listRoutes:
            arete.evaporerPheromone(self.__tauxEvaporation)
        print("\tÉvaporation\n*self.__listRoutes, size", len(self.__listRoutes), *self.__listRoutes ,sep="\n")


        if (self.__toursAvantselection > 0):
            self.__toursAvantselection = self.__toursAvantselection - 1
        else:
            self.__toursAvantselection = self.__selectionNaturelle

            # Algorithmes génétiques
            # Les individus les plus efficaces propagent leurs caractéristiques par
            #  les gènes qui seront re-combinés dans la création de nouveaux 
            # individus. La population évolue en s’adaptant à leur environnement à 
            # travers la mutationet la sélection naturelle.
            self.selection()
            #Pour que les individus choisisent une route
            print("After Selection *self.__listAnts", *self.__listAnts, sep="\n")
            self.configTour()

        

    def selection(self): #slide 42,43,47/69
        """Retient les meilleurs acteurs (on élimine les autres)

        Parameters:
            None
        Returns:
            None
        """
        print("*self.__listAnts", *self.__listAnts, sep="\n")

        # Comme il y a deux types d’individus nécessaires à la colonie, deux 
        # individus seront créés à chaque cycle évolutif.
        # - L’un d’eux sera descendant des deux travailleurs les plus réussis
        # - L’autre sera descendant des deux meilleurs explorateurs.
        
        # sort https://www.afternerd.com/blog/python-sort-list/
        # reverse = True: sort in a descending order
        # key parameter specifies a function that will be called on each list 
        # item before making comparisons
        # Python Anonymous/Lambda Function

        print("\tExplorateurs")
        # les meilleurs explorateurs (les plus rapides ou les moins répétitifs)
        self.__listAnts.sort(reverse = True, 
                             key = lambda ant:
                             ant.getNombreFoisSurMemeRoute())
        
        fourmisParentsExplorateurs = self.__listAnts[0:2]
        print("*fourmisParentsExplorateurs", *fourmisParentsExplorateurs, sep="\n")
        fourmiDescendantExplorateurs = Ant.crossover(
                                       fourmisParentsExplorateurs[0],
                                       fourmisParentsExplorateurs[1])
        print("fourmiDescendantExplorateurs", fourmiDescendantExplorateurs)
        # print("*fourmiDescendantExplorateurs", *fourmiDescendantExplorateurs, sep="\n")

        print("\tTravailleurs")
        # les meilleurs travailleurs (recueillir une grande quantité de 
        # nourriture)
        self.__listAnts.sort(reverse = True,
                             key = lambda ant: ant.getNouritureCollectee())
        fourmisParentsTravailleurs = self.__listAnts[0:2]
        print("*fourmisParentsTravailleurs", *fourmisParentsTravailleurs, sep="\n")
        fourmiDescendantTravailleurs = Ant.crossover(
                                       fourmisParentsTravailleurs[0],
                                       fourmisParentsTravailleurs[1])
        print("fourmiDescendantTravailleurs", fourmiDescendantTravailleurs, sep="\n")

        print("\tDelete les agents qui se perdent")
        # delete les agents qui se perdent
        nombreAgentsAvant = len(self.__listAnts) #20
        nombreAgentsSupprimes = 0 #5
        self.__listAnts[:] = [ant for ant in self.__listAnts 
                              if ant.getNouritureCollectee() > 0]
        nombreAgents = len(self.__listAnts) #15
                
        nombreAgentsSupprimes = nombreAgentsAvant - nombreAgents
        print("nombreAgentsSupprimes", nombreAgentsSupprimes)
        print("nombreAgentsAvant", nombreAgentsAvant)
        print("nombreAgents", nombreAgents)
        

        # Extintion des agents pour avoir space  
        if (nombreAgentsSupprimes <= 6):
            self.__listAnts = self.__listAnts[0:(len(self.__listAnts)
                                                 - (6 - nombreAgentsSupprimes))]
        
        nombreAgents = len(self.__listAnts)
        print("nombreAgents", nombreAgents)
        fourmisExtendList = (fourmisParentsTravailleurs 
                            + [fourmiDescendantTravailleurs]
                            + fourmisParentsExplorateurs
                            + [fourmiDescendantExplorateurs])
        print("*fourmisExtendList, size", len(fourmisExtendList), *fourmisExtendList ,sep="\n")

        self.__listAnts.extend(fourmisExtendList)

        print("Migration")
        # Migration    
        #self.__listAnts = [Ant(villeNid) for i in range(nombreAgents,
        #                                              nombreAgentsAvant-6)]
        for i in range(nombreAgents, nombreAgentsAvant-6):
            self.__listAnts.append(Ant(villeNid))

        print("*self.__listAnts, size", len(self.__listAnts), *self.__listAnts ,sep="\n")
        print("*self.__listRoutes, size", len(self.__listRoutes), *self.__listRoutes ,sep="\n")
        print("RESET")
        [ant.reset(ant.getVilleNid()) for ant in self.__listAnts]
        

    def updatePheromone(self):
        """Mise à jour de la phéromone lorsque les fourmis auront chacune 
        construit leur trajet
        
        """
        pass
        # Évaporation : une baisse générale de la quantité sur toutes les 
        # arêtes du graphe par un facteur constant

        # Augmentation : on met à jour la phéromone sur les arêtes empruntées

        # def getRoute(VilleA, VilleB):
        #     for arete in listRoutes:
        #         if ((VilleA == arete.getPremiereVille() 
        #             && VilleB == arete.getSecondeVille()) || 
        #             (VilleA == arete.getSecondeVille() 
        #             && VilleB == arete.getPremiereVille())
        #             return arete
        #     return None

#  constructeurs, interface et méthodes auxiliares etc
    def setListRoutes(self, listRoutes):
        self.__listRoutes = listRoutes

    def setListVilles(self, listVilles):
        self.__listAnts = listVilles

    def setListAnts(self, listAnts):
        self.__listAnts = listAnts

# Test class Civilization
if __name__ == '__main__':
    listVilles = []
    # Creation de cinq villes
    listVilles.append(Ville(60,30,"Lyon"))
    listVilles.append(Ville(20,45,"Nantes"))
    listVilles.append(Ville(45,60,"Paris"))
    listVilles.append(Ville(50,80,"Lille"))
    listVilles.append(Ville(70,10,"Marseille"))
    print("Villes en France")
    # print("\t ", listVilles)
    print(*listVilles, sep='\n')
    listRoutes = []
    # Creation de huit routes
    listRoutes.append(Route(100, listVilles[0], listVilles[1])) # routeLyonNantes
    listRoutes.append(Route(100, listVilles[0], listVilles[2])) # routeLyonParis
    listRoutes.append(Route(100, listVilles[0], listVilles[3])) # routeLyonLille
    listRoutes.append(Route(100, listVilles[0], listVilles[4])) # routeLyonMarseille
    listRoutes.append(Route(100, listVilles[1], listVilles[2])) # routeNantesParis
    listRoutes.append(Route(100, listVilles[1], listVilles[3])) # routeNantesLille
    listRoutes.append(Route(100, listVilles[1], listVilles[4])) # routeNantesMarseille
    listRoutes.append(Route(100, listVilles[2], listVilles[3])) # routeParisLille

    # Identifie et stock les arêtes conectées
    for ville in listVilles:
        ville.mesAretes(listRoutes)
    print("Routes")
    # print("\t1 ", listRoutes)
    print(*listRoutes, sep='\n')

    villeNid = listVilles[4]# villeNid Marseille
    villeFood = listVilles[2]  # villeNid Paris

    # Creation des agents (fourmis)
    nAnts = 20
    listAnts = [Ant(villeNid) for i in range(nAnts)]
    print("VilleNid : ", listVilles[4])
    print("VilleFood : ", villeFood)
    print("_" * 80)

    nom = "Colonie-de-fourmis-Test"
    toursAvantselection = 400 #400 
    nMaxTours = 4000 #2000
    probabiliteMutation = 0.01 
    tauxEvaporation = 0.0005

    civilisation = Civilisation(nom, villeNid, villeFood, nAnts,
                 toursAvantselection, probabiliteMutation, 
                 tauxEvaporation)

    civilisation.setListRoutes(listRoutes)
    civilisation.setListVilles(listVilles)
    civilisation.setListAnts(listAnts)
    tours = 0

    civilisation.configTour()

    while (tours < nMaxTours):
        civilisation.tourSuivant()
        tours = tours + 1