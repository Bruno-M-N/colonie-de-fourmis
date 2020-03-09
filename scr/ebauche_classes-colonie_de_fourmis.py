""" École Centrale de Lyon
    UE INF S8 Algorithmes collaboratifs et applications 2019-2020

    BE1 et 2 - Colonie de Fourmis
    1- L’implantation d’un système multi-agents de recherche du chemin le plus 
    court (PCC) suivant le principe de la Stigmergie et utilisant les 
    algorithmes génétiques.

    @author: Bruno Moreira Nabinger
"""

from random import randint, uniform
from math import sin, sqrt

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
    def isRoute(ville1, ville2):
        """Vérifie s'il la route relie deux Villes

        Parameters:
            ville1 (Ville): Ville potentiellement connectée à cette route
            ville2 (Ville): Ville potentiellement connectée à cette route
        Returns:
            bool: True indique que la route relie le deux villes
                False indique que la route ne relie pas le deux villes
        """
        if (self.__premiereVille == ville1 and 
            self.__secondeVille == ville2) or (self.__premiereVille == ville2
            and self.__secondeVille == ville1):
            return True
        return False

    def __str__(self): # Opérateur d’affichage utilisé par print
        return 'Premier Ville : {} - Seconde Ville : {},  Longueur = {},' \
        ' pheromone = {}'.format(self.__premiereVille, \
        self.__secondeVille, self.__longueur, self.__pheromone)




class Ville: # Declaration de la classe Ville
    """Représent les noeuds
    
    ***************************************************************************
    
    Attributs:
        x (int): Coordonné x de la ville
        y (int): Coordonné y de la ville
        nom (string): Nom de la ville
    """
    #  constructeurs
    def __init__(self, x, y, nom):
        self.__x = x # Coordonné x de la ville
        self.__y = y # Coordonné y de la ville
        self.__nom = nom # Nom de la ville

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def mesAretes(self, listAretes):
        aretesConectees = []
        for arete in listAretes:
            if (self == arete.getPremiereVille() or self == arete.getSecondeVille()):
                aretesConectees.append(arete)
        return aretesConectees
        

    #  constructeurs, interface et méthodes auxiliares etc

    def __str__(self): # Opérateur d’affichage utilisé par print
        # return 'Nom : {}, Coordonnées : ({}, {})' \
        return '{} ({}, {})' \
        .format(self.__nom, self.__x, self.__y)

class Ant:
    """Représent les agents (fourmis)
    
    Text***********************************************************************
    
    Attributs:
        La sensibilité phéromonale de la fourni
        alpha (float): réel aléatoires choisi dans l'intervale [-5,5]
        beta (float): réel aléatoires choisi dans l'intervale [-5,5]
        gamma (float): réel aléatoires choisi dans l'intervale [-5,5]
        porteFood (bool): Transporte de la nourriture ou non
        nouritureCollectee (int): Quantité de nouriture collectée par
            cette fourmi
        nb_fois_sur_meme_route (int): combien de fois ils ont été sur la même 
            route (arête).
        positionRoute (int): position sur la route (arête) actuel
        --longueurRoute (int): longueur totale de la route (arête) actuel
        actuelRoute (Route): information sur le route où la fourmi se trouve
            dans un instant t.
        distanceParcourue (int): distance totale parcourue par la fourmi
        self.__listVilles (list): mémoire de villes

    """
    #  constructeurs
    # Constructeur par défaut : un individu neuf (utilisé lors de 
    # l'initialisation ou  de migration) 
    def __init__(self, villeNid):
        # La sensibilité phéromonale de la fourmi
        # réels aléatoires choisi dans l'intervale [-5,5]
        self.__alpha =  uniform(-5, 5)
        self.__beta = uniform(-5, 5)
        self.__gamma = uniform(-5, 5)
        self.__porteFood = False # Transporte de la nourriture ou non
        # Le travailleur le plus réussi est celui qui a recueilli davantage de
        #  nourriture
        self.__nouritureCollectee = 0 # Quantité de nouriture collectée
        # Slide 47/69 Les agents comptent combien de fois ils ont été sur la 
        # même route (arête).
        # Les valeurs faibles de ce compteur indiquent les explorateurs avec 
        # succès. Les valeurs plus élevées : des agents qui se sont perdus dans 
        # l’environnement.
        self.__nbFoisSurMemeRoute = 0
        self.__positionRoute = 0 # int: position sur la route (arête)
        #self.__longueurRoute = 0 # int: Longueur totale de la route (arête)
        self.__routeActuel = None; # Longueur totale de la route (arête)
        self.__distanceParcourue = 0 # int distance totale 
        self.__listVilles = [] # mémoire de villes
        
        # villeNid (Ville): Ville où se situe le nid
        self.__listVilles.append(villeNid)

    ###########################################################################

    # Constructeur Crossover, progéniture (croisement, recouvrement)
    @classmethod
    def crossover(self, mere, pere):
        # La sensibilité phéromonale de la fourmi
        if (randint(0,1) == 0):
            self.__alpha = mere.getAlpha()
        else:
            self.__alpha = pere.getAlpha()
        if (randint(0,1) == 0):
            self.__beta = mere.getBeta()
        else:
            self.__beta = pere.getBeta()
        if (randint(0,1) == 0):
            self.__gamma = mere.getGamma()
        else:
            self.__gamma = pere.getGamma()
        # Le travailleur le plus réussi est celui qui a recueilli davantage de
        #  nourriture
        self.__nouritureCollectee = 0 # Quantité de nouriture collectée
        # Slide 47/69 Les agents comptent combien de fois ils ont été sur la 
        # même route (arête).
        # Les valeurs faibles de ce compteur indiquent les explorateurs avec 
        # succès. Les valeurs plus élevées : des agents qui se sont perdus dans 
        # l’environnement.
        self.__nombreFoisSurMemeRoute = 0
        self.__distanceParcourue = 0
        self.__listVilles = [] # villes de l'environement

    def mutation(self):
        """Changer l’une des caractéristiques de l’individu au hasard.
    
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        Méthode qui change l’une des caractéristiques de l’individu au hasard.
        Elle peut être appelée après le croisement (CrossOver) mais c’est un 
        évènement avec une faible probabilité de se produire.
        
        Parameters:
            pheromoneActuel (float): Intensité de la phéromone sur la route, 
                mésure par un nombre réel
        """
        return (1 / self.__distanceParcourue)
        
    ###########################################################################

    def getAlpha(self):
        return self.__alpha
    
    def getBeta(self):
        return self.__beta

    def getGamma(self):
        return self.__gamma

    def getPorteFood(self)
        return self.__porteFood 

    def getNombreFoisSurMemeRoute(self):
        return self.__nombreFoisSurMemeRoute

    def getNouritureCollectee(self):
        return self.__nouritureCollectee

    def getvilleDestination(self):
        return self.__routeActuel.getSecondeVille()

    def avancer(self): # Avancer une étape plus
        """Avancer  sur un graphe, d'un ville vers un autre
        
        Parameters:
            None
        Returns:
            bool: True indique que la fourmi a arrivé dans la nouvelle ville
                  False indique que la fourmi est encore sur le chemin

        """
        if (self.__positionRoute + 1 < self.__routeActuel.getLongueur()):
            self.__positionRoute = self.__positionRoute + 1
            self.__distanceParcourue = self.__distanceParcourue + 1
        if (self.__positionRoute == self.__routeActuel.getLongueur()):
            return True
        else:
            return False
    
    def addVilleMemoire(self): # Avancer une étape plus
        """Add Ville à la mémoire
        
        Parameters:
            ville
        Returns:
            None

        """
        #self.__listVilles.append(ville)
        self.__listVilles.append(self.__routeActuel.getSecondeVille())

    def delVilleMemoire(self): # Avancer une étape plus
        """Add Ville à la mémoire
        
        Parameters:
            ville
        Returns:
            None

        """
        self.__listVilles.pop()


    def prendreFood(self): 
        """Prendre de la nourriture dans la source de nourriture
        
        """
        self.__porteFood = True

    def deposerFood(self):
        """Laisse la nourriture (dans le nid)
        
        """
        self.__nouritureCollectee = self.__nouritureCollectee + 1
        self.__porteFood = False

    def getTendance(self, pheromone):
        """Représent la tendance à choisir une route
    
        Méthode qui évalue la tendance à choisir un itinéraire en fonction de 
        l'intensité de la phéromone, en raison d'une modulation de le taux de 
        phéromone "perceptible" sur l'arête, mésure par un nombre réel. 
        Elle permet une variabilité du comportement des agents au travers de 
        une fonction sinusoïdale avec trois coefficients : alpha, beta, gamma.
        
        Parameters:
            pheromone (float): Intensité de la phéromone sur la route, mésure 
            par un nombre réel
        Returns:
            pheromoneLevel (float): modulation de le taux de phéromone 
                "perceptible" sur l'arête, mésure par un nombre réel. 
        """
        pheromoneLevel = self.__alpha * sin(self.__beta * pheromone 
                                            + self.__gamma)
        return pheromoneLevel

    def choixArete(self, listAretes):
        """Représent la tendance à choisir une route
    
        Cette fonction évaluera la possibilité de choix de toutes les arrêts 
        possibles, puis choisira la meilleure parmi ces possibilités, basée sur
        le taux de phéromone "perceptible" sur l'arête.
        
        Parameters:
            listAretes (list[Route]): 
        Returns:
            None
        """
        
        if (self.__porteFood == False):
            listPheromoneAretes = [0] * len(listAretes)
            for arete in listAretes:
                listPheromoneAretes = arete.getPheromone()

            choixIndex = listPheromoneAretes.index(max(listPheromoneAretes))

            # position sur la nouvelle route (arête)
            self.__positionRoute = 0
            villeDestinationAnterieur = self.__routeActuel.getSecondeVille()
            villeDestination = None
            # une route a deux extrémités 
            if (villeDestinationAnterieur == 
                listAretes[choixIndex].getPremiereVille()):
                villeDestination = listAretes[choixIndex].getSecondVille()
            else: 
                # if (villeDestinationAnterieur == 
                # listAretes[choixIndex].getSecondVille()):
                villeDestination = listAretes[choixIndex].getPremierVille())

            self.__routeActuel = Route(listAretes[choixIndex].getLongueur(),
                                       listAretes[choixIndex].getPheromone(),
                                       villeDestinationAnterieur,
                                       villeDestination)

        else:
            # position sur la nouvelle route (arête)
            self.__positionRoute = 0
            villeDestinationAnterieur = self.__routeActuel.getSecondeVille()
            villeDestination = listVilles[-1] #dernier élément

            for arete in listAretes:
                if (arete.isRoute(villeDestinationAnterieur,villeDestination)):
                    self.__routeActuel = Route(arete.getLongueur(),
                                               arete.getPheromone(),
                                               villeDestinationAnterieur,
                                               villeDestination)


        
    def deposerPheromone(self):
        """Augmenter le niveau de la phéromone de la route
    
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        Méthode qui évalue la tendance à choisir un itinéraire en fonction de 
        l'intensité de la phéromone. Cette fonction évaluera la possibilité de 
        choix de toutes les arrêts possibles, puis choisira la meilleure parmi
        ces possibilités.
        
        Parameters:
            pheromoneActuel (float): Intensité de la phéromone sur la route, 
                mésure par un nombre réel
        Returns:

        """
        return (1 / self.__distanceParcourue)
        
    
    #  constructeurs, interface et méthodes auxiliares etc

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
    """
    #  constructeurs
    # nIndividus = randint(minIndividus, maxIndividus)
    def __init__(self, nom, villeNid, villeFood, nIndividus,
                 toursAvantselection, probabiliteMutation):
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
        self.__probabiliteMutation = probabiliteMutation
        self.__nouritureCollectee = 0

    def tourSuivant(self): 
        """Effectue un tour de la simulation
        
        """

        for ant in self.__listAnts:
            finRoute = ant.avancer()
            # La fourmi avance. Si elle arrive au but, elle est dans une
            #  nouvelle ville.
            if (finRoute == True):
                # TODO vérifier si  soit on mettre un objet Route pour la fourmi savoir où elle est
                # soit on mettre un objet Ville pour la fourmi savoir verd où elle va
                # soit on fait une autre chose
                
                # Si l'agent ne possède pas de nourriture, on ajoute la ville 
                # à sa mémoire (méthode addVilleMemoire)
                if (ant.getPorteFood() == False):
                    # TODO vérifier si  soit on mettre un objet Route pour la fourmi savoir où elle est
                    # soit on mettre un objet Ville pour la fourmi savoir verd où elle va
                    # soit on fait une autre chose
                    ant.addVilleMemoire()
                    #ant.addVilleMemoire(villeDestination)

                # Si la ville est la ville source (villeFood), la fourmi prend 
                # de la nourriture. Dans le prochain tour, la fourmi commence à
                #  retourner
                if (ant.getVilleDestination() == self.__villeFood):
                    if (ant.getPorteFood() == False):
                        ant.prendreFood()
                # Si la ville est la ville de départ (villeNid)
                elif (ant.getVilleDestination() == self.__villeNid):
                    if (ant.getPorteFood() == True):
                        ant.deposerFood()
                        self.__nouritureCollectee += 1
                        ant.choixArete(listAretesConecteesVille)
                else:
                    # TODO La fourmi doit choisir un nouvelle route (méthode 
                    # choisirArete). Si elle porte de la nourriture, on efface la
                    # derniere ville de la liste; elle  choisira 
                    # la route vers la dernière ville de la liste ; 
                    # Sinon on appelle getTendance pour chaque route liée à la ville.
                    if (ant.getPorteFood() == True):
                        ant.delVilleMemoire()
                        ant.choixArete(listAretesConecteesVille)
                    else:
                        ant.choixArete(listAretesConecteesVille)


        # Mise à jour de la phéromone lorsque les fourmis auront chacune 
        # construit leur trajet
        #updatePheromone()####################################################

        # Algorithmes génétiques
        # Les individus les plus efficaces propagent leurs caractéristiques par
        #  les gènes qui seront re-combinés dans la création de nouveaux 
        # individus. La population évolue en s’adaptant à leur environnement à 
        # travers la mutationet la sélection naturelle.

        #selection

        

    def selection(self): #slide 42,43,47/69
        """Retient les meilleurs acteurs (on élimine les autres)
        
        """

        # Comme il y a deux types d’individus nécessaires à la colonie, deux 
        # individus seront créés à chaque cycle évolutif.
        # - L’un d’eux sera descendant des deux travailleurs les plus réussis
        # - L’autre sera descendant des deux meilleurs explorateurs.
        
        # sort https://www.afternerd.com/blog/python-sort-list/
        # reverse = True: sort in a descending order
        # key parameter specifies a function that will be called on each list 
        # item before making comparisons
        # Python Anonymous/Lambda Function

        # les meilleurs explorateurs (les plus rapides ou les moins répétitifs)
        self.__listAnts.sort(reverse = True, 
                             key = lambda ant:
                             ant.getNombreFoisSurMemeRoute())
        fourmisParentsExplorateurs = self.__listAnts[0:1]
        fourmiDescendantExplorateurs = Ant.crossover(
                                       fourmisParentsExplorateurs[0],
                                       fourmisParentsExplorateurs[1])

        # les meilleurs travailleurs (recueillir une grande quantité de 
        # nourriture)
        self.__listAnts.sort(reverse = True,
                             key = lambda ant: ant.getNouritureCollectee())
        fourmisParentsTravailleurs = self.__listAnts[0:1]
        fourmiDescendantTravailleurs = Ant.crossover(
                                       fourmisParentsTravailleurs[0],
                                       fourmisParentsTravailleurs[1])

        # delete les agents qui se perdent
        nombreAgentsAvant = len(self.__listAnts)
        nombreAgentsSupprimes = 0
        self.__listAnts[:] = [ant for ant in self.__listAnts 
                              if ant.getNouritureCollectee() > 0]
        nombreAgents = len(self.__listAnts)
                
        nombreAgentsSupprimes = nombreAgentsAvant - nombreAgents

        if (nombreAgents < 6):
            self.__listAnts = self.__listAnts[0:(len(self.__listAnts)
                                                 - (6 - nombreAgentsSupprimes))]

        self.__listAnts.extend(fourmisParentsTravailleurs, 
                               fourmiDescendantTravailleurs,
                               fourmisParentsExplorateurs,
                               fourmiDescendantExplorateurs)

        # Évaporation : une baisse générale de la quantité sur toutes les 
        # arêtes du graphe par un facteur constant

        # Augmentation : on met à jour la phéromone sur les arêtes empruntées

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