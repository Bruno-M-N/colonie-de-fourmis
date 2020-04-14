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
from random import randint, uniform
from math import sin#, sqrt

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
        nbFoisSurMemeRoute (int): combien de fois ils ont été sur la même 
            route (arête).
        positionRoute (int): position sur la route (arête) actuel
        routeActuelle (Route): route où la fourmi se trouve dans un instant t.
        distanceParcourue (int): distance totale parcourue par la fourmi
        self.__listVilles (list): mémoire de villes

    """
    #  constructeurs
    # "Constructeur" par défaut : un individu neuf (utilisé lors de 
    # l'initialisation ou de migration) 
    def __init__(self, villeNid, alpha = 10, beta = 10, gamma = 10):
        # La sensibilité phéromonale de la fourmi
        # réels aléatoires choisi dans l'intervale [-5,5]
        if (alpha < -5 or alpha > 5):
            self.__alpha =  uniform(-5, 5)
        else:
            self.__alpha = alpha
        if (beta < -5 or beta > 5):
            self.__beta =  uniform(-5, 5)
        else:
            self.__beta = beta
        if (gamma < -5 or gamma > 5):
            self.__gamma =  uniform(-5, 5)
        else:
            self.__gamma = gamma
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
        self.__routeActuelle = None # Longueur totale de la route (arête)
        self.__distanceParcourue = 0 # int distance totale 
        self.__listVilles = [] # mémoire de villes
        
        # villeNid (Ville): Ville où se situe le nid
        self.__listVilles.append(villeNid)

    ###########################################################################

    # Constructeur Crossover, progéniture (croisement, recouvrement)
    @classmethod
    def crossover(cls, mere, pere):
        """Crossover des caractéristiques des parents pour créer un individu
    
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        Méthode qui réalise le croisement des caractéristiques des parents pour 
        créer un nouveau individu. Il y a une faible probabilité de mutation, que peut changer l’une des caractéristiques de l’individu au hasard.
        
        Parameters:
            mere (Ant)
            pere (Ant)
        """
        # La sensibilité phéromonale de la fourmi
        if (randint(0,1) == 0):
            alpha = mere.getAlpha()
        else:
            alpha = pere.getAlpha()
        if (randint(0,1) == 0):
            beta = mere.getBeta()
        else:
            beta = pere.getBeta()
        if (randint(0,1) == 0):
            gamma = mere.getGamma()
        else:
            gamma = pere.getGamma()

        return cls(mere.getVilleNid(), alpha, beta, gamma)

    def mutation(self, probabiliteMutation):
        """Changer l’une des caractéristiques de l’individu au hasard.
    
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        Méthode qui change l’une des caractéristiques de l’individu au hasard.
        Elle peut être appelée après le croisement (CrossOver) mais c’est un 
        évènement avec une faible probabilité de se produire.
        
        Parameters:
            probabiliteMutation (float): réel choisi dans l'intervale [0,1],
                qui répresent la probabilité qu'une mutation se produise. Après 
                un croisement, il y a une faible probabilité de mutation.
        """
        mutation =  uniform(0, 1)
        if(mutation < probabiliteMutation):
            randomCaracteristique =  randint(0, 2)
            # La sensibilité phéromonale de la fourmi
            # réels aléatoires choisi dans l'intervale [-5,5]
            if (randomCaracteristique == 0):
                self.__alpha =  uniform(-5, 5)
            elif (randomCaracteristique == 1):
                self.__beta =  uniform(-5, 5)
            else:
                self.__gamma =  uniform(-5, 5)
   
    ###########################################################################

    def getAlpha(self):
        return self.__alpha
    
    def getBeta(self):
        return self.__beta

    def getGamma(self):
        return self.__gamma

    def getPorteFood(self):
        return self.__porteFood 

    def getNombreFoisSurMemeRoute(self):
        return self.__nbFoisSurMemeRoute

    def getNouritureCollectee(self):
        return self.__nouritureCollectee

    def getVilleNid(self):
        if (len(self.__listVilles) != 0):
            return (self.__listVilles[0])
        else:
            return None

    def getVilleDestination(self):
        return (self.__routeActuelle.getSecondeVille())

    def getRouteActuelle(self):
        return self.__routeActuelle


    def calculeNbFoisSurMemeRoute(self):
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
        taille = len(self.__listVilles)
        for i in range(taille - 4): # 0 1 .. n-5
            for j in range(i + 3, taille-1): # i + 3, i + 4 .. n-2
                if (self.__listVilles[i] == self.__listVilles[j]):
                    if (self.__listVilles[i+1] == self.__listVilles[j+1]):
                        self.__nbFoisSurMemeRoute = \
                            self.__nbFoisSurMemeRoute + 1

    def avancer(self): # Avancer une étape plus
        """Avancer  sur un graphe, d'un ville vers un autre
        
        Parameters:
            None
        Returns:
            bool: True indique que la fourmi a arrivé dans la nouvelle ville
                  False indique que la fourmi est encore sur le chemin

        """
        # print(" Before positionRoute", self.__positionRoute, 
        #       "routeActuelle.getLongueur()", self.__routeActuelle.getLongueur())
        if (self.__positionRoute + 1 < self.__routeActuelle.getLongueur()):
            self.__positionRoute = self.__positionRoute + 1
            self.__distanceParcourue = self.__distanceParcourue + 1
            # print("positionRoute = ", self.__positionRoute)
            return False
        else:
            #prendre partie non entier
            self.__distanceParcourue = (self.__distanceParcourue 
                + self.__routeActuelle.getLongueur() 
                - self.__positionRoute)
            self.__positionRoute = 0
            return True
        # if (self.__positionRoute >= self.__routeActuelle.getLongueur()):
        #     return True
        # else:
        #     return False
    
    def addVilleMemoire(self): # Avancer une étape plus
        """Add ville à la mémoire

        Add la deuxième ville (ville destination) de la routeActuelle à la 
        mémoire
        
        Parameters:
            None
        Returns:
            None

        """
        #self.__listVilles.append(ville)
        self.__listVilles.append(self.__routeActuelle.getSecondeVille())

    def delVilleMemoire(self): # Avancer une étape plus
        """Delete la dernière ville de la mémoire
        
        Parameters:
            None
        Returns:
            None

        """
        self.__listVilles.pop()

    def prendreFood(self): 
        """Prendre de la nourriture dans la source de nourriture

        Parameters:
            None
        Returns:
            None
        """
        self.__porteFood = True

    def deposerFood(self):
        """Laisse la nourriture (dans le nid)

        Parameters:
            None
        Returns:
            None
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

    def choixArete(self, listAretesEnvironement):
        """Représent la tendance à choisir une route
    
        Cette fonction évaluera la possibilité de choix de toutes les arrêts 
        possibles, puis choisira la meilleure parmi ces possibilités, basée sur
        le taux de phéromone "perceptible" sur l'arête.
        
        Parameters:
            listAretesEnvironement (list[Route]): liste des toutes les routes de l'environement
        Returns:
            __routeActuelle (Route): arête sélectionnée
        """
        #print("Memoire Villes: ", *self.__listVilles, sep=', ')        

        if (self.__porteFood == False):
            # Initialisation des variables 
            # Si la ville est la ville de départ (villeNid)
            if (len(self.__listVilles) == 1):
                villeActuelle = self.__listVilles[0]
                villeDestinationAnterieur = villeActuelle
            else:
                villeActuelle = self.getVilleDestination()
                villeDestinationAnterieur = \
                    self.__routeActuelle.getSecondeVille()
            
            villeActuelle.updatePheromoneAretesConectees(listAretesEnvironement)

            listAretes = villeActuelle.getAretesConectees()

            # print("ListAretes:", *listAretes, sep='\n')
            # print(*listAretes, sep='\n')

            # choix la nouvelle route (arête) basée sur la perception de 
            # phéromone
            listPheromoneAretes = [0] * len(listAretes)
            i = 0
            for arete in listAretes:
                # vérifie qui on n'as pas le même route qu'avant
                # Si la ville n'est pas la première ville visité après la ville
                # de départ (villeNid)
                if (len(self.__listVilles) > 2):
                    if (self.__routeActuelle.memeRoute(arete) == True):
                        listPheromoneAretes[i] = float('-inf')
                    else:
                        listPheromoneAretes[i] = \
                            self.getTendance(arete.getPheromone())
                else:
                    listPheromoneAretes[i] = self.getTendance(arete.getPheromone())
                i = i + 1
            choixIndex = listPheromoneAretes.index(max(listPheromoneAretes))
            # print("ListAretes:", *listAretes, sep='\n')
            # print("listPheromoneAretes", listPheromoneAretes, "\t choixIndex = ", choixIndex)
            # print("__________________________________________________________")
            # print("listAretes[choixIndex] :\n \t", listAretes[choixIndex])
            # print("__________________________________________________________")

            # # vérifie qui on n'as pas le même route qu'avant
            # # Si la ville n'est pas la première ville visité après la ville de 
            # # départ (villeNid)
            # if (len(self.__listVilles) > 2):
            #     # print("Memoire listVilles", *self.__listVilles, sep=', ')        
            #     # https://docs.python.org/2/library/heapq.html#heapq.nlargest
            #     if (self.__routeActuelle.memeRoute(listAretes[choixIndex])):
            #         del(listAretes[choixIndex])
                    
                    
            #         print("Sorted : ", sorted(listPheromoneAretes, reverse=True)[-2])
            #         choixIndex = listPheromoneAretes.index(sorted(listPheromoneAretes, 
            #                                                       reverse=True)[-2])
            #         choixIndexType = type (choixIndex)
            #         print("choixIndexType:", choixIndexType, "choixIndex", choixIndex)
            #         print("Même route !", "listPheromoneAretes", listPheromoneAretes, "choixIndex = ", choixIndex)
            #         print("New listAretes[choixIndex] :\n \t", listAretes[choixIndex])


            # position sur la nouvelle route (arête)
            self.__positionRoute = 0
            villeDestination = None
            # une route a deux extrémités 
            # pour convention, on réalise une permutation si nécessaire pour 
            # que la ville Destination soit toujours la seconde ville d'une 
            # route
            if (villeDestinationAnterieur == 
                listAretes[choixIndex].getPremiereVille()):
                villeDestination = listAretes[choixIndex].getSecondeVille()
            else: 
                # if (villeDestinationAnterieur == 
                # listAretes[choixIndex].getSecondVille()):
                villeDestination = listAretes[choixIndex].getPremiereVille()

            self.__routeActuelle = Route(listAretes[choixIndex].getPheromone(),
                                       villeDestinationAnterieur,
                                       villeDestination)
            # print("Nouvelle Route________________________________")
            # print("Longueur:", listAretes[choixIndex].getLongueur())
            # print("Pheromone:",listAretes[choixIndex].getPheromone())
            # print("villeDestinationAnterieur:", villeDestinationAnterieur)
            # print("villeDestination:", villeDestination)

        else:
            # position sur la nouvelle route (arête)
            self.__positionRoute = 0
            villeDestinationAnterieur = self.__listVilles[-1] #dernier élément
            if (len(self.__listVilles) > 1):
                villeDestination = self.__listVilles[-2]

            # print("villeDestinationAnterieur", villeDestinationAnterieur)
            # print("villeDestination =", villeDestination)
            
            villeDestinationAnterieur.updatePheromoneAretesConectees(listAretesEnvironement)

            listAretes = villeDestinationAnterieur.getAretesConectees()

            for arete in listAretes:
                if (arete.isRoute(villeDestinationAnterieur,villeDestination)):
                    self.__routeActuelle = Route(arete.getPheromone(),
                                               villeDestinationAnterieur,
                                               villeDestination)
        
        return self.__routeActuelle

    def deposerPheromone(self):
        """Augmenter le niveau de la phéromone de la route
    
        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        Méthode qui évalue la tendance à choisir un itinéraire en fonction de 
        l'intensité de la phéromone. Cette fonction évaluera la possibilité de 
        choix de toutes les arrêts possibles, puis choisira la meilleure parmi
        ces possibilités.
        
        Parameters:
            None
        Returns:
            pheromone (float): si la distance parcourue par la fourmi est 
                différent de 0, retourne l'inverse de la distance parcourue.
                Sinon, retourne 0 
        """
        if (self.__distanceParcourue != 0):
            return (1 / self.__distanceParcourue)
        else:
            return 0

    def verifieVille(self, villeFood):
        """Vérifie la ville pour déterminer la prochaine action de l'agent
        
        Parameters:
            villeFood (Ville): Ville où se situe la source de nourriture
        Returns:
            None 
        """
        # Si l'agent ne possède pas de nourriture, on ajoute la ville 
        # à sa mémoire (méthode addVilleMemoire)
        if (self.__porteFood == False):
            self.addVilleMemoire()
            #ant.addVilleMemoire(villeDestination)

        # Si la ville est la ville source (villeFood), la fourmi prend 
        # de la nourriture. Dans le prochain tour, la fourmi commence à
        # retourner
        villeActuelle = self.getVilleDestination()
        if (villeActuelle == villeFood):
            if (self.__porteFood == False):
                self.prendreFood()
                self.calculeNbFoisSurMemeRoute()
                # print("PorteFood = True______________________________________")
                return 'villeFood - prendreFood()'
            return 'villeFood - already hadFood()'
        # Si la ville est la ville de départ (villeNid)
        elif (villeActuelle == self.__listVilles[0]):
            if (self.__porteFood  == True):
                self.deposerFood()
                self.__nouritureCollectee += 1
                self.delVilleMemoire()
                self.__distanceParcourue = 0
                return 'villeNid - deposeFood()'
                # print("DeposeFood = True_____________________________________")
                #print("_" * 80)
                
        else:
            # TODO La fourmi doit choisir un nouvelle route (méthode 
            # choisirArete). Si elle porte de la nourriture, on efface la
            # derniere ville de la liste; elle  choisira 
            # la route vers la dernière ville de la liste ; 
            # Sinon on appelle getTendance pour chaque route liée à la ville.
            if (self.__porteFood  == True):
                self.delVilleMemoire()
        return None

    def reset(self, villeNid):
        """Réinitialisation des paramètres non génétiques

        Méthode qui réinitialise les paramètres non génétiques de l'agent. Les
        trois coefficients alpha, beta et gamma ne sont pas affectés. Cette 
        méthode doit être appelée lors de la sélection des fourmis.
        
        Parameters:
            villeNid (Ville): Ville où se situe le nid
        Returns:
            None 
        """
        self.__porteFood = False 
        self.__nouritureCollectee = 0 
        self.__nbFoisSurMemeRoute = 0
        self.__positionRoute = 0 
        self.__routeActuelle = None 
        self.__distanceParcourue = 0  
        self.__listVilles = []
        
        self.__listVilles.append(villeNid)

    def __str__(self): # Opérateur d’affichage utilisé par print
        return '<a {0:7.4f}, b {1:7.4f}, g {2:7.4f}>, ' \
        'Food  = {3:2d}, nbMemeRoute  = {4:2d}, ' \
        'd = {5:5.2f}'.format(self.__alpha, self.__beta, \
        self.__gamma, self.__nouritureCollectee, self.__nbFoisSurMemeRoute, \
        self.__distanceParcourue)
        # return 'Ant : <alpha {0:7.4f}> <beta {1:7.4f}> <gamma {2:7.4f}>, ' \
        # 'NourritureCollecte  = {3:3d}, nbFoisSurMemeRoute  = {4:3d}, ' \
        # 'distParcourue = {5:8.4f}'.format(self.__alpha, self.__beta, \
        # self.__gamma, self.__nouritureCollectee, self.__nbFoisSurMemeRoute, \
        # self.__distanceParcourue)

# Test class Ant
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

    villeNid = listVilles[4]
    # Creation d'une fourmis
    agent = Ant(villeNid) # villeNid Marseille
    villeFood = listVilles[2]  # villeNid Paris
    print("VilleNid : ", listVilles[4])
    print("VilleFood : ", villeFood)
    print("_" * 80)
    routeActuelle = agent.choixArete(listRoutes)
    print("Route actuelle : ", routeActuelle)
    #print("\t1 Route actuel", listRoutes)
    tours = 0
    nMaxTours = 380
    finRoute = agent.avancer()
    while (tours < nMaxTours):
        tours = tours + 1
        # print("Tours : ", tours)
        finRoute = agent.avancer()
        # La fourmi avance. Si elle arrive au but, elle est dans une
        #  nouvelle ville.
        # Mise à jour de la phéromone lorsque les fourmis auront construit
        #  leur trajet
        if (finRoute == True):                
            print("finRoute!")
            agent.verifieVille(villeFood)
            routeActuelle = agent.choixArete(listRoutes)
            print("Nouvelle Route : ", routeActuelle)

    print(agent)