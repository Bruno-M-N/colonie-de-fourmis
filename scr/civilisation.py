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

# tourner en rond
def testIsInLoop(listVilles):
    """Vérifie si l'algorithme est dans un boucle

    Vérifie si l'algorithme de la méthode statique tourOptimise, qui calcule la longueur de la tournée basée sur le choix de la quantité de pheromone et retorne aussi le chemin utilisé, est dans un boucle.

    Parameters:
        lisVilles (list[Ville]): Liste qui contient les villes utilisées pour
            réaliser le parcours optimal
    Returns:
        bool: True indique que l'algorithme est dans une boucle dans le 
            graphe
              False indique que l'algorithme n'est pas dans un boucle dans 
            le graphe
    """
    # On remarque que une fourmie qui ne porte pas de la nourriture ne peut
    #  pas choisir la même route qui elle vient d'utiliser
    #  
    # Dans une séquence de n villes, les deux premières (0 et 1) villes 
    # sont vérifiées à partir de la quatrième et cinquième villes, ensuite 
    # la cinquième et sixième villes, jusqu'à l'avant-dernière (n-2) et 
    # dernière (n-1) villes
    # 
    # Après, on vérifie les deuxième et troisième villes à partir de la 
    # cinquième et sixième villes, ensuite la sixième et septième villes, 
    # jusqu'à l'avant-dernière (n-2) et dernière (n-1) villes
    #
    # On répète ce processus jusqu'à vérifier les villes n-5 et n-4 avec 
    # les villes avant-dernière (n-2) et dernière (n-1)
    taille = len(listVilles)
    for i in range(taille - 4): # 0 1 .. n-5
        for j in range(i + 3, taille-1): # i + 3, i + 4 .. n-2
            if (listVilles[i] == listVilles[j]):
                if (listVilles[i+1] == listVilles[j+1]):
                    return True
    return False


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
        nIndividus (int): Représente le nombre d'individus dans la 
            population.
        listRoutes (list[Route]): toutes les routes de l'environement
        listVilles (list[Ville]): toutes les villes de l'environement
        selectionNaturelle (int): indique dans quels tours multiples de sa
            valeur une sélection (pour l'algorithme génétique) doit avoir lieu.
        toursAvantselection (int): compteur qui indique les tours restants 
            avant la prochaine sélection (pour l'algorithme génétique)
        probabiliteMutation (float): réel choisi dans l'intervale [0,1], qui 
           répresent la probabilité qu'une mutation se produise. Après un 
           croisement, il y a une faible probabilité de mutation.
        tauxEvaporation (float): réel choisi dans l'intervale [0,1], qui 
            répresent le taux d'évaporation
        nouritureCollectee (int): quantité de nourriture collectées par les
            agents
        crossoverSize (int): combient d'enfants de chaque type on veut gérér à 
            chaque selection. Il faut le double de parents de chaque type. La 
            function génere donc  2*crossoverSize enfants

        Variables utiles pour la réglage des tours de sélection
        selectionNaturelle
        
        flagFirstsAntsGotFood(bool): indique que un agent est parmi les 
            premiers à prendre de la nourriture dans la source de nourriture
        flagFirstAntNidFood(bool): indique qu'un agent est le premier à 
            laisser la nourriture (dans le nid)
    """
    #  constructeurs
    # nIndividus = randint(minIndividus, maxIndividus)
    def __init__(self, nom, villeNid, villeFood, nIndividus,
                 toursAvantselection, probabiliteMutation, 
                 tauxEvaporation, crossoverSize=1):
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
        self.__crossoverSize = crossoverSize
        self.__nouritureCollectee = 0

        self.__flagFirstsAntsGotFood = False
        self.__flagFirstAntNidFood = False
        

    # Au départ, on initialise les paramètres de la manière suivante :
    # for all (i, j) arete du graphe, tij = t0 = m / Cnn
    # Où m est le nombre de fourmis et Cnn est la longueur de la tournée 
    # réalisée par  l’heuristique "les plus proches voisins" (va simplement de 
    # proche en proche voisin).
    # + Ou bien par tout autre algorithme qui permet de construire 
    # raisonnablement un tour optimisé, au moins localement.
    @staticmethod
    def longueurTournee(listVilles, villeNid, villeFood):
        longueurTourneeTotal = 0
        ville = villeNid #listVilles[0]
        listAretes = ville.getAretesConectees()
        distances = [0] * len(listAretes)
        i = 0
        for arete in listAretes:
            distances[i] = (arete.getLongueur())
            i = i + 1
        # print("Premières distances", *distances)
        minDistance = min(distances)
        longueurTourneeTotal = longueurTourneeTotal + minDistance
        choixIndex = distances.index(minDistance)
        routeActuelle = listAretes[choixIndex]
        # print("Premières Route", routeActuelle)
        ville = routeActuelle.getSecondeVille()
        
        while (ville != villeFood):
            listAretes = ville.getAretesConectees()
            distances = [0] * len(listAretes)
            i = 0
            for arete in listAretes:
                # vérifie qui on n'as pas le même route qu'avant
                if (routeActuelle.memeRoute(arete) == True):
                    distances[i] = float('inf')
                else:
                    distances[i] = (arete.getLongueur())
                i = i + 1
            # print(distances)
            minDistance = min(distances)
            longueurTourneeTotal = longueurTourneeTotal + minDistance
            choixIndex = distances.index(minDistance)
            routeActuelle = listAretes[choixIndex]
            # print("Route", routeActuelle)
            ville = routeActuelle.getSecondeVille()
        print("Longueur Tournée totale par l’heuristique \"les plus proches"\
              " voisins\": ", longueurTourneeTotal)
        return longueurTourneeTotal

    @staticmethod
    def tourOptimise(listVilles, villeNid, villeFood):
        longueurTourneeTotal = 0
        listTourneeVilles = []
        listTourneeRoutes = []
        listTourneeVilles.append(villeNid)
        ville = villeNid #listVilles[0]
        listAretes = ville.getAretesConectees()
        pheromone = [0] * len(listAretes)
        i = 0
        for arete in listAretes:
            pheromone[i] = (arete.getPheromone())
            i = i + 1
        maxPheromone = max(pheromone)
        choixIndex = pheromone.index(maxPheromone)
        routeActuelle = listAretes[choixIndex]
        distanceMaxPheromone = routeActuelle.getLongueur()
        longueurTourneeTotal = longueurTourneeTotal + distanceMaxPheromone
        listTourneeRoutes.append(routeActuelle)
        print("Premières Route", routeActuelle)
        ville = routeActuelle.getSecondeVille()
        listTourneeVilles.append(ville)
        while (ville != villeFood):
            listAretes = ville.getAretesConectees()
            pheromone = [0] * len(listAretes)
            i = 0
            for arete in listAretes:
                # vérifie qui on n'as pas le même route qu'avant
                if (routeActuelle.memeRoute(arete) == True):
                    pheromone[i] = float('-inf')
                else:
                    pheromone[i] = (arete.getPheromone())
                i = i + 1
            # print(pheromone)
            maxPheromone = max(pheromone)
            choixIndex = pheromone.index(maxPheromone)
            routeActuelle = listAretes[choixIndex]
            distanceMaxPheromone = routeActuelle.getLongueur()
            longueurTourneeTotal = longueurTourneeTotal + distanceMaxPheromone
            listTourneeRoutes.append(routeActuelle)
            print("Route", routeActuelle)
            ville = routeActuelle.getSecondeVille()
            listTourneeVilles.append(ville)
            if (len(listTourneeVilles) >= 5):
                if (testIsInLoop(listTourneeVilles)):
                    print("L'algorithme génétique n'a pas trouvé une solution" \
                      " avec les paramètres de configuration données")
                    return None, None, None
        print("Longueur Tournée optimisée totale : ", longueurTourneeTotal)
        print("\tTournee (Villes):", *listTourneeVilles, sep='\n')
        print("\tTournee (Routes):", *listTourneeRoutes, sep='\n')
        return longueurTourneeTotal, listTourneeVilles, listTourneeRoutes

    def getVilleNid(self):
        return self.__villeNid
    
    def getVilleFood(self):
        return self.__villeFood

    def getNIndividus(self):
        return self.__nIndividus
    
    def getSelectionNaturelle(self): # Sélection en tours multiples de
        return self.__selectionNaturelle
    
    def getProbabiliteMutation(self):
        return self.__probabiliteMutation
    
    def getTauxEvaporation(self):
        return self.__tauxEvaporation

    def getCrossoverSize(self):
        return self.__crossoverSize
    
    def getNouritureCollectee(self):
        return self.__nouritureCollectee

    def configTour(self):
        """Réalise la mise à jour de la phéromone des arêtes conectées
    
        Méthode qui réalise la mise à jour de la quantité de phéromone des
        arêtes stockées dans un objet ville et réalise la premier choix de 
        route par les agents. configTour doit être appelé avant le premier tour
        de simulation et après chaque selection pour que les individus 
        choisisent une route
        
        Parameters:
            None
        Returns:
            None
        """
        [ville.updatePheromoneAretesConectees(self.__listRoutes) for ville in self.__listVilles]

        [ant.choixArete(self.__listRoutes) for ant in self.__listAnts]
        # print("FIRST\n*self.__listRoutes, size", len(self.__listRoutes), *self.__listRoutes ,sep="\n")


    def tourSuivant(self, tour): 
        """Effectue un tour de la simulation

        Effectue un tour de la simulation, ou les fourmis réalisent ses 
        actions, l'évaporarion de la phéromone a lieu et la sélection est 
        réalisé lors du nombre de tours définie par selectionNaturelle

        Parameters:
            Tour (int): nombre du tour de la simulation
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
                status = ant.verifieVille(self.__villeFood)
                if(status == 'villeFood - prendreFood()'):
                    self.__nouritureCollectee += 1 

                if ((self.__flagFirstsAntsGotFood and self.__flagFirstAntNidFood) == False):
                    if (status == 'villeFood - prendreFood()'):
                        print("Tour : ", tour, " - Un agent est parmi les premiers à prendre de la nourriture dans la source de nourriture")
                        self.__flagFirstsAntsGotFood = True
                    elif (status == 'villeNid - deposeFood()'):
                        print("Tour : ", tour, "Un agent est le premier à laisser la nourriture (dans le nid)")
                        self.__flagFirstAntNidFood = True
                
                routeEmpruntee = ant.getRouteActuelle()
                ant.choixArete(self.__listRoutes)

                # Augmentation : on met à jour la phéromone sur les arêtes
                #  empruntées
                for arete in self.__listRoutes:
                    if (routeEmpruntee.memeRoute(arete)):
                        arete.ajouterPheromone(ant.deposerPheromone())
            
        # Évaporation : une baisse générale de la quantité sur toutes les 
        # arêtes du graphe par un facteur constant
        for arete in self.__listRoutes:
            arete.evaporerPheromone(self.__tauxEvaporation)
        # print("\tÉvaporation\n*self.__listRoutes, size", len(self.__listRoutes), *self.__listRoutes ,sep="\n")

        for ville in self.__listVilles:
            ville.updatePheromoneAretesConectees(self.__listRoutes)

        if (self.__toursAvantselection > 0):
            self.__toursAvantselection = self.__toursAvantselection - 1
        else:
            self.__toursAvantselection = self.__selectionNaturelle

            # Algorithmes génétiques
            # Les individus les plus efficaces propagent leurs caractéristiques 
            # par les gènes qui seront re-combinés dans la création de nouveaux 
            # individus. La population évolue en s’adaptant à leur 
            # environnement à travers la mutation et la sélection naturelle.
            self.selection()
            #Pour que les individus choisisent une route
            # print("After Selection *self.__listAnts", *self.__listAnts, sep="\n")
            self.configTour()

    def selection(self): #slide 42,43,47/69
        """Retient les meilleurs acteurs (on élimine les autres)
        
        CrossoverSize (int) : combient d'enfants de chaque type on veut gérér. 
        Il faut le double de parents de chaque type. La function génere donc  2 
        * crossoverSize. Si crossoverSize  est égal ou inférieur à un ou encore 
        superieur à le nombre d'individus fois 6, la méthode selectionSimple, 
        qui génère seulement 2 enfants (l'un descendant de parents 
        explorateurs, ceux qui ont été le moins de fois sur la même route et
        l'un descendant de parents "Travailleurs", ceux qui recueillent plus de 
        nourriture )

        Parameters:
            None
        Returns:
            None
        """
        if (self.__crossoverSize <= 1 or 
                self.__crossoverSize*6 > self.__nIndividus ):
            self.selectionSimple()
            return
        # print("*self.__listAnts", *self.__listAnts, sep="\n")
        # Comme il y a deux types d’individus nécessaires à la colonie, deux* 
        # individus (ou 2*crossoverSize individus) seront créés à chaque cycle 
        # évolutif.
        # - L’un d’eux sera descendant des deux travailleurs les plus réussis
        # - L’autre sera descendant des deux meilleurs explorateurs.
        
        # sort https://www.afternerd.com/blog/python-sort-list/
        # reverse = True: sort in a descending order
        # key parameter specifies a function that will be called on each list 
        # item before making comparisons
        # Python Anonymous/Lambda Function

        # print("\tExplorateurs")
        # les meilleurs explorateurs (les plus rapides ou les moins répétitifs)
        self.__listAnts.sort(key = lambda ant: ant.getNombreFoisSurMemeRoute())
        
        fourmisParentsExplorateurs = self.__listAnts[0:2*self.__crossoverSize]
        # print("*self.__listAnts", *self.__listAnts, sep="\n")
        # print("*fourmisParentsExplorateurs", *fourmisParentsExplorateurs, sep="\n")
        fourmiDescendantExplorateurs = []
        for i in range(0, 2*self.__crossoverSize, 2):
            nouveauExplorateur = Ant.crossover(
                                       fourmisParentsExplorateurs[i],
                                       fourmisParentsExplorateurs[i+1])
            nouveauExplorateur.mutation(self.__probabiliteMutation)
            fourmiDescendantExplorateurs.append(nouveauExplorateur) 
        # print("fourmiDescendantExplorateurs", fourmiDescendantExplorateurs)
        # print("*fourmiDescendantExplorateurs", *fourmiDescendantExplorateurs, sep="\n")

        # print("\tTravailleurs")
        # les meilleurs travailleurs (recueillir une grande quantité de 
        # nourriture)
        self.__listAnts.sort(reverse = True,
                             key = lambda ant: ant.getNouritureCollectee())
        fourmisParentsTravailleurs = self.__listAnts[0:2*self.__crossoverSize]
        # print("*fourmisParentsTravailleurs", *fourmisParentsTravailleurs, sep="\n")
        fourmiDescendantTravailleurs = []
        for i in range(0, 2*self.__crossoverSize, 2):
            nouveauTravailleur = Ant.crossover(
                                       fourmisParentsTravailleurs[i],
                                       fourmisParentsTravailleurs[i+1])
            nouveauTravailleur.mutation(self.__probabiliteMutation)
            fourmiDescendantTravailleurs.append(nouveauTravailleur)
        # print("fourmiDescendantTravailleurs", fourmiDescendantTravailleurs, sep="\n")

        # print("\tDelete les agents qui se perdent")
        # delete les agents qui se perdent
        nombreAgentsAvant = len(self.__listAnts) #20
        nombreAgentsSupprimes = 0 #5
        self.__listAnts[:] = [ant for ant in self.__listAnts 
                              if ant.getNouritureCollectee() > 0]
        nombreAgents = len(self.__listAnts) #15
                
        nombreAgentsSupprimes = nombreAgentsAvant - nombreAgents
        # print("nombreAgentsSupprimes", nombreAgentsSupprimes)
        # print("nombreAgentsAvant", nombreAgentsAvant)
        # print("nombreAgents", nombreAgents)
        

        # Extintion des agents pour avoir space  
        if (nombreAgentsSupprimes <= 6*self.__crossoverSize):
            self.__listAnts = self.__listAnts[0:(len(self.__listAnts)
                                                 - (6*self.__crossoverSize - nombreAgentsSupprimes))]
        
        nombreAgents = len(self.__listAnts)
        # print("nombreAgents", nombreAgents)
        fourmisExtendList = (fourmisParentsTravailleurs 
                            + fourmiDescendantTravailleurs
                            + fourmisParentsExplorateurs
                            + fourmiDescendantExplorateurs)
        # print("*fourmisExtendList, size", len(fourmisExtendList), *fourmisExtendList ,sep="\n")

        self.__listAnts.extend(fourmisExtendList)

        # print("Migration")
        # Migration    
        #self.__listAnts = [Ant(villeNid) for i in range(nombreAgents,
        #                                              nombreAgentsAvant-6)]
        for i in range(nombreAgents, nombreAgentsAvant-6*self.__crossoverSize):
            self.__listAnts.append(Ant(self.__villeNid))

        # print("*self.__listAnts, size", len(self.__listAnts), *self.__listAnts ,sep="\n")
        # print("*self.__listRoutes, size", len(self.__listRoutes), *self.__listRoutes ,sep="\n")
        # print("RESET")
        [ant.reset(ant.getVilleNid()) for ant in self.__listAnts]
            

    def selectionSimple(self): #slide 42,43,47/69
        """Retient les meilleurs acteurs (on élimine les autres)

        Parameters:
            None
        Returns:
            None
        """
        # print("*self.__listAnts", *self.__listAnts, sep="\n")

        # Comme il y a deux types d’individus nécessaires à la colonie, deux 
        # individus seront créés à chaque cycle évolutif.
        # - L’un d’eux sera descendant des deux travailleurs les plus réussis
        # - L’autre sera descendant des deux meilleurs explorateurs.
        
        # sort https://www.afternerd.com/blog/python-sort-list/
        # reverse = True: sort in a descending order
        # key parameter specifies a function that will be called on each list 
        # item before making comparisons
        # Python Anonymous/Lambda Function

        # print("\tExplorateurs")
        # les meilleurs explorateurs (les plus rapides ou les moins répétitifs)
        self.__listAnts.sort(key = lambda ant: ant.getNombreFoisSurMemeRoute())
        
        fourmisParentsExplorateurs = self.__listAnts[0:2]
        # print("*fourmisParentsExplorateurs", *fourmisParentsExplorateurs, sep="\n")
        fourmiDescendantExplorateurs = Ant.crossover(
                                       fourmisParentsExplorateurs[0],
                                       fourmisParentsExplorateurs[1])
        fourmiDescendantExplorateurs.mutation(self.__probabiliteMutation)
        # print("fourmiDescendantExplorateurs", fourmiDescendantExplorateurs)
        # print("*fourmiDescendantExplorateurs", *fourmiDescendantExplorateurs, sep="\n")

        # print("\tTravailleurs")
        # les meilleurs travailleurs (recueillir une grande quantité de 
        # nourriture)
        self.__listAnts.sort(reverse = True,
                             key = lambda ant: ant.getNouritureCollectee())
        fourmisParentsTravailleurs = self.__listAnts[0:2]
        # print("*fourmisParentsTravailleurs", *fourmisParentsTravailleurs, sep="\n")
        fourmiDescendantTravailleurs = Ant.crossover(
                                       fourmisParentsTravailleurs[0],
                                       fourmisParentsTravailleurs[1])
        fourmiDescendantTravailleurs.mutation(self.__probabiliteMutation)
        # print("fourmiDescendantTravailleurs", fourmiDescendantTravailleurs, sep="\n")

        # print("\tDelete les agents qui se perdent")
        # delete les agents qui se perdent
        nombreAgentsAvant = len(self.__listAnts) #20
        nombreAgentsSupprimes = 0 #5
        self.__listAnts[:] = [ant for ant in self.__listAnts 
                              if ant.getNouritureCollectee() > 0]
        nombreAgents = len(self.__listAnts) #15
                
        nombreAgentsSupprimes = nombreAgentsAvant - nombreAgents
        # print("nombreAgentsSupprimes", nombreAgentsSupprimes)
        # print("nombreAgentsAvant", nombreAgentsAvant)
        # print("nombreAgents", nombreAgents)
        

        # Extintion des agents pour avoir space  
        if (nombreAgentsSupprimes <= 6):
            self.__listAnts = self.__listAnts[0:(len(self.__listAnts)
                                                 - (6 - nombreAgentsSupprimes))]
        
        nombreAgents = len(self.__listAnts)
        # print("nombreAgents", nombreAgents)
        fourmisExtendList = (fourmisParentsTravailleurs 
                            + [fourmiDescendantTravailleurs]
                            + fourmisParentsExplorateurs
                            + [fourmiDescendantExplorateurs])
        # print("*fourmisExtendList, size", len(fourmisExtendList), *fourmisExtendList ,sep="\n")

        self.__listAnts.extend(fourmisExtendList)

        # print("Migration")
        # Migration    
        #self.__listAnts = [Ant(villeNid) for i in range(nombreAgents,
        #                                              nombreAgentsAvant-6)]
        for i in range(nombreAgents, nombreAgentsAvant-6):
            self.__listAnts.append(Ant(self.__villeNid))

        # print("*self.__listAnts, size", len(self.__listAnts), *self.__listAnts ,sep="\n")
        # print("*self.__listRoutes, size", len(self.__listRoutes), *self.__listRoutes ,sep="\n")
        # print("RESET")
        [ant.reset(ant.getVilleNid()) for ant in self.__listAnts]
        

    # def updatePheromone(self):
    #     """Mise à jour de la phéromone lorsque les fourmis auront chacune 
    #     construit leur trajet
        
    #     """
    #     pass
        # Évaporation : une baisse générale de la quantité sur toutes les 
        # arêtes du graphe par un facteur constant

        # Augmentation : on met à jour la phéromone sur les arêtes empruntées

#  constructeurs, interface et méthodes auxiliares etc
    def setListRoutes(self, listRoutes):
        self.__listRoutes = listRoutes

    def setListVilles(self, listVilles):
        self.__listVilles = listVilles

    def setListAnts(self, listAnts):
        self.__listAnts = listAnts

    def getListVilles(self):
        return self.__listVilles

    def getListRoutes(self):
        return self.__listRoutes

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
    nAnts = 14
    listAnts = [Ant(villeNid) for i in range(nAnts)]
    print("VilleNid : ", listVilles[4])
    print("VilleFood : ", villeFood)
    print("_" * 80)

    #     Au départ, on initialise les paramètres de la manière suivante :
    # for all (i, j) arete du graphe, tij = t0 = m / Cnn
    # Où m est le nombre de fourmis et Cnn est la longueur de la tournée 
    # réalisée par  l’heuristique "les plus proches voisins" (va simplement de 
    # proche en proche voisin).
    # + Ou bien par tout autre algorithme qui permet de construire 
    # raisonnablement un tour optimisé, au moins localement.
    longueurTournee = Civilisation.longueurTournee(listVilles, villeNid,
                                                   villeFood)
    pheromoneInitialSurRoutes = nAnts/longueurTournee
    print("pheromoneInitialSurRoutes : ", pheromoneInitialSurRoutes)
    [arete.setPheromone(pheromoneInitialSurRoutes) for arete in listRoutes]

    [ville.updatePheromoneAretesConectees(listRoutes) for ville in listVilles]

    nom = "Colonie-de-fourmis-Test"
    toursAvantselection = 400 #400 
    nMaxTours = 4000 #2000
    probabiliteMutation = 0.01 
    tauxEvaporation = 0.0005

    civilisation = Civilisation(nom, villeNid, villeFood, nAnts,
                 toursAvantselection, probabiliteMutation, 
                 tauxEvaporation, crossoverSize=2)

    civilisation.setListRoutes(listRoutes)
    civilisation.setListVilles(listVilles)
    civilisation.setListAnts(listAnts)
    tours = 0

    civilisation.configTour()

    while (tours < nMaxTours):
        if (tours % 1000 == 0):   
            print("Tour : ", tours)
            # print("*self.__listAnts, size", len(self.__listAnts), *self.__listAnts ,sep="\n")
            # print("*self.__listRoutes, size", *(civilisation.getListRoutes()),sep="\n")

        civilisation.tourSuivant(tours)
        tours = tours + 1

    print("*self.__listRoutes, size", *(civilisation.getListRoutes()),sep="\n")

    longueurTourOptimise, listVillesTourOptimise, listRoutesTourOptimise = \
        Civilisation.tourOptimise(civilisation.getListVilles(),
                                         civilisation.getVilleNid(),
                                         civilisation.getVilleFood())