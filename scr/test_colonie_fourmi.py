""" École Centrale de Lyon
    UE INF S8 Algorithmes collaboratifs et applications 2019-2020

    BE1 et 2 - Colonie de Fourmis
    1- L’implantation d’un système multi-agents de recherche du chemin le plus 
    court (PCC) suivant le principe de la Stigmergie et utilisant les 
    algorithmes génétiques.

    @author: Achraf Bella
    @author: Bruno Moreira Nabinger
"""

from tkinter import *
from tkinter.filedialog import askopenfilename
from random import randint, seed
seed(1)

from ville import * # import classe Ville à partir du fichier ville.py
from route import * # import classe Route à partir du fichier route.py
# import classe Civilisation à partir du fichier civilisation.py
from civilisation import *

from zoneaffichage import *

DEFAULT_POPULATION = 100
DEFAULT_N_MAX_TOURS = 16000
DEFAULT_SELECTION_TOURS_MULTIPLES = 800
DEFAULT_PROBABILITE_MUTATION = 0.01
DEFAULT_TAUX_EVAPORATION = 0.0005
DEFAULT_CROSSOVER_SIZE = 8


class FenPrincipale(Tk):
    """Classe de l'interface principale

    Correspondant à l’interface principale et gérant l’application
    """
    def __init__(self):
        Tk.__init__(self)
        self.title('Colonie de fourmi')
        self.iconbitmap("img/ant.ico")
        self.geometry("1120x640+10+10")
        self.resizable(width =False, height=False)

        #self.minsize(360, 240)

        # mainMenu = Menu(self)
        # self.config(mainMenu)

        # fileMenu = Menu(mainMenu)
        # mainMenu.add_cascade(Label="Créer environnement")

        # Création d'un item du menu

        self.__civilisation = None
        

        self._frame = None
        # self.switch_frame(CreationPage, self.__civilisation)#StartPage)
        #self.switch_frame(SetupSimulationPage, self.__civilisation)#StartPage)
        self.switch_frame(StartPage, None)

    def switch_frame(self, frame_class, civilisation):
        """Destroys current frame and replaces it with a new one.

        It works by accepting any Class object that implements Frame. The
        function then creates a new frame to replace the old one.

        Reference:
            Based on the code by Steven M. Vascellaro, in a post called "Switch
            between two frames in tkinter" in Stackoverflow.com, a question and
            answer site for professional and enthusiast programmers.
        Parameters:
            frame_class: Any Class object that implements Frame. For this
                application: StartPage, SetupSimulationPage, SimulationPage,
                CreditsPage ...
            civilisation (Civilisation): Civilisation
        Returns:
            None
        """
        new_frame = frame_class(self, civilisation)
        # Deletes old _frame if it exists, then replaces it with the new frame.
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def setCivilisation(
                        self, listVilles, listRoutes, nom,
                        villeNid, villeFood, nIndividus,
                        toursAvantselection, probabiliteMutation, 
                        tauxEvaporation, crossoverSize):
        self.__civilisation = Civilisation(
                nom, villeNid, villeFood, nIndividus, toursAvantselection,
                probabiliteMutation, tauxEvaporation, crossoverSize)
        # Creation des agents (fourmis)
        listAnts = [Ant(villeNid) for i in range(nIndividus)]
        self.__civilisation.setListRoutes(listRoutes)
        self.__civilisation.setListVilles(listVilles)
        self.__civilisation.setListAnts(listAnts)

    def startCivilisationSimulation(
                                    self, frame_class, nMaxTours,
                                    listVilles, listRoutes, nom,
                                    villeNid, villeFood, nIndividus,
                                    toursAvantselection, probabiliteMutation, 
                                    tauxEvaporation,
                                    crossoverSize,
                                    nomFichier=None):
        
        #     Au départ, on initialise les paramètres de la manière suivante :
        # for all (i, j) arete du graphe, tij = t0 = m / Cnn
        # Où m est le nombre de fourmis et Cnn est la longueur de la tournée 
        # réalisée par  l’heuristique "les plus proches voisins" (va simplement
        # de proche en proche voisin).
        # + Ou bien par tout autre algorithme qui permet de construire 
        # raisonnablement un tour optimisé, au moins localement.
        print("longueurTournee")
        longueurTournee = Civilisation.longueurTournee(listVilles, 
                                                       villeNid,
                                                       villeFood)
        pheromoneInitialSurRoutes = nIndividus/longueurTournee
        print("pheromoneInitialSurRoutes : ", pheromoneInitialSurRoutes)
        [arete.setPheromone(pheromoneInitialSurRoutes) for arete in listRoutes]

        # Mise à jour pheromone pour les arêtes conectées
        [ville.updatePheromoneAretesConectees(listRoutes) 
            for ville in listVilles]
        # print("Routes")

        self.setCivilisation(listVilles, listRoutes, nom,
                             villeNid, villeFood, nIndividus,
                             toursAvantselection, probabiliteMutation, 
                             tauxEvaporation, crossoverSize)
        

        new_frame = frame_class(self, self.__civilisation,
                                nMaxTours, nomFichier)
        # Deletes old _frame if it exists, then replaces it with the new frame.
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def chargerEnvironnemment(self, frame_class, nomFichier=None):
        if(nomFichier == None):
            # show an "Open" dialog box and return the path to the selected file
            nomFichier = askopenfilename(
                    title="Ouvrir un fichier Town (\".town\")",
                    initialfile="Test.towns",
                    filetypes=[('Towns files','.towns'),('all files','.*')])
        if (len(nomFichier) > 0):
            print("Nom du fichier : ", nomFichier)
            
        new_frame = frame_class(self, self.__civilisation, nomFichier)
        # Deletes old _frame if it exists, then replaces it with the new frame.
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

    def quitter(self, frame_class):
        """Ferme le programme

        Accept n'importe quel objet d'une classe qui implements Frame.

        Parameters:
            frame_class: n'importe quel objet d'une classe qui implements
                Frame. Pour cette application: StartPage, SimulationPage, 
                DescriptionPage and PageGame
        Returns:
            None
        """
        self.destroy()

    def updater(self):
        self.update()
        self.update_idletasks()


class StartPage(Frame):
    """Frame Menu

    StartPage correspond à page qui contient un menu pour les autres pages, à
    savoir PageNom, SetupSimulationPage and CreationPage. Elle permettre aussi ]
    de sortir du programme quand l'utilisateur clique sur le bouton "Quitter".
    """
    def __init__(self, master, civilisation):
        Frame.__init__(self, master)
        Label(self, text="Colonie de Fourmie").\
            pack(side="top", fill="x", pady=10)
        Button(self, text="Création d'environnemment",
               command=lambda: master.switch_frame(CreationPage,
                                                   civilisation)).pack(pady=5)
        Button(self, text="Charger environnemment",
               command=lambda: master.chargerEnvironnemment(
                    SetupSimulationPage)).pack(pady=5)
        Button(self, text="Simulation",
               command=lambda: master.switch_frame(SetupSimulationPage,
                                                   civilisation)).pack(pady=5)
        Button(self, text="Description",
               command=lambda: master.switch_frame(DescriptionPage,
                                                   civilisation)).pack(pady=5)
        Button(self, text="Crédits",
               command=lambda: master.switch_frame(CreditsPage,
                                                   civilisation)).pack(pady=5)
        # Création d'un widget Button (bouton Quitter)
        Button(self, text='Quitter', width=15, command=lambda:
               master.quitter(SimulationPage)).pack(pady=5)
               #master.quitter(SimulationPage)).pack(side=LEFT, padx=5, pady=5)


class CreationPage(Frame):
    """Frame page de Simulation

    SimulationPage correspond à page qui contient la description du projet et les crédits. Elle permettre aussi de sortir du programme quand l'utilisateur clique sur le bouton "Quitter".
    """
    def __init__(self, master, civilisation):
        Frame.__init__(self, master)
        self.__master = master
        self.__boutonVilleNidActive = False
        self.__boutonVilleFoodActive = False

        # Création d'une sous boite
        self.__leftFrame = Frame(self, height=640, width=240, bg="#eee4da")
        self.__leftFrame.grid(row=0, column=0)
        # Seulement pour avoir la bonne mise en page avec grid        
        self.__leftSpaceLabelColumn0 = Label(self.__leftFrame,
                                             text="", bg="#eee4da")
        self.__leftSpaceLabelColumn0.grid(row=0, column=0, padx=34, pady=2)
        self.__leftSpaceLabelColumn1 = Label(self.__leftFrame,
                                             text="", bg="#eee4da")
        self.__leftSpaceLabelColumn1.grid(row=0, column=1, padx=40, pady=2)
        self.__leftSpaceLabelColumn2 = Label(self.__leftFrame,
                                             text="", bg="#eee4da")
        self.__leftSpaceLabelColumn2.grid(row=0, column=2, padx=34, pady=2)

        # Création d'un widget Button (bouton Set Ville Nid)
        self.__boutonVilleNid = Button(self.__leftFrame, bg='gray',
                                       text='Ville Nid', 
                                       command=self.toggleVilleNid)
        self.__boutonVilleNid.grid(row=1, column=1, pady=10)

        # Création d'un widget Button (bouton Set Ville Nid)
        self.__boutonVilleFood = Button(self.__leftFrame, bg='gray',
                                        text='Ville Food', 
                                        command=self.toggleVilleFood)
        self.__boutonVilleFood.grid(row=2, column=1, pady=10)

        self.__zoneAffichage = ZoneAffichageCreation(self, 640, 640, 'snow2')
        self.__zoneAffichage.grid(row=0, column=1)

        # Création d'une sous boite
        self.__rightFrame = Frame(self, height=640, width=240, bg="#eee4da")
        self.__rightFrame.grid(row=0, column=2)
        # Seulement pour avoir la bonne mise en page avec grid        
        self.__rightSpaceLabelColumn0 = Label(self.__rightFrame,
                                             text="", bg="#eee4da")
        self.__rightSpaceLabelColumn0.grid(row=0, column=0, padx=34, pady=2)
        self.__rightSpaceLabelColumn1 = Label(self.__rightFrame,
                                             text="", bg="#eee4da")
        self.__rightSpaceLabelColumn1.grid(row=0, column=1, padx=40, pady=2)
        self.__rightSpaceLabelColumn2 = Label(self.__rightFrame,
                                             text="", bg="#eee4da")
        self.__rightSpaceLabelColumn2.grid(row=0, column=2, padx=34, pady=2)

        # Création d'un widget Button (bouton sauvegarder)
        self.__boutonSauvegarder = Button(self.__rightFrame, text='Sauvegarder',
         command=self.sauvegarder).grid(row=1, column=1, pady=10)

        # Création d'un widget Button (bouton Quitter)
        self.__boutonQuitter = Button(self.__rightFrame, text='Quitter', command=master.destroy).grid(row=2, column=1, pady=10)

    def toggleVilleNid(self):
        if (not self.__boutonVilleNidActive):
            self.__boutonVilleNidActive = True
            self.__boutonVilleNid.config(bg='blue')
            self.__boutonVilleFoodActive = False
            self.__boutonVilleFood.config(bg='gray')
        else:
            self.__boutonVilleNidActive = False
            self.__boutonVilleNid.config(bg='gray')
        self.__zoneAffichage.toggleVilleNid(self.__boutonVilleNidActive)

    def toggleVilleFood(self):
        if (not self.__boutonVilleFoodActive):
            self.__boutonVilleFoodActive = True
            self.__boutonVilleFood.config(bg='red')
            self.__boutonVilleNidActive = False
            self.__boutonVilleNid.config(bg='gray')
        else:
            self.__boutonVilleFoodActive = False
            self.__boutonVilleFood.config(bg='gray')
        self.__zoneAffichage.toggleVilleFood(self.__boutonVilleFoodActive)

    def sauvegarder(self):
        villesGraphiques = self.__zoneAffichage.getVillesGraphiques()
        routesGraphiques = self.__zoneAffichage.getRoutesGraphiques()
        listVilles = []
        listRoutes = []
        villeNid = None
        villeFood = None

        for ville in villesGraphiques:
            listVilles.append(ville.getVille())
            if (ville.getVilleNid()):
                villeNid = ville.getVille()
            if (ville.getVilleFood()):
                villeFood = ville.getVille()
        
        if(villeNid is not None and villeFood is not None ):
            if (routesGraphiques):
                for route in routesGraphiques:
                    listRoutes.append(route.getRoute())
                    
                nomFichier = asksaveasfilename(
                        parent=self.__master,
                        filetypes=[('Towns files','.towns'),('all files','.*')],
                        title="Sauvegarder fichier Town (\".town\")")
                if (len(nomFichier) > 0):
                    print("Nom du fichier : ", nomFichier)
                    fileManager = FileManager(nomFichier) 
                    fileManager.sauverEnvironementDansFichier(
                            nomFichier, listVilles, listRoutes,
                            villeNid, villeFood)
                    self.__master.chargerEnvironnemment(SetupSimulationPage,nomFichier=nomFichier+'.towns')


class SetupSimulationPage(Frame):
    """Frame page de Simulation

    SimulationPage correspond à page qui contient la description du projet et les crédits. Elle permettre aussi de sortir du programme quand l'utilisateur clique sur le bouton "Quitter".
    """
    def __init__(self, master, civilisation, nomFichier=None):
        Frame.__init__(self, master)
        self.__master = master
        self.__nomFichier = nomFichier
        # self.__civilisation = civilisation

        # Création d'une sous boite
        self.__zoneAffichage = ZoneAffichage(self, 640, 640, 'snow2')
        self.__zoneAffichage.grid(row=0, column=1)


        if (nomFichier is None):
            listVilles, listRoutes, villeNid, villeFood \
                = self.getEnvironementDefault()
        else:
            fileManager = FileManager(nomFichier) 
            listVilles, listRoutes, villeNid, villeFood = \
                fileManager.lireEnvironementDansFichier(nomFichier)

        def updateEntries():
            print("Numéro Max de tours", nMaxTours.get())
            print("Numéro Max de tours type", nMaxTours.get())
            print("Sélection en tours multiples de:",
                  selectionToursMultiplesEntry.get())
            print("Population", populationEntry.get())
            print("Probabilite de Mutation", probabiliteMutationEntry.get())
            print("Taux d'evaporation", tauxEvaporationEntry.get())
            print("Crossover Size", crossoverSize.get())
            pheromoneInitialSurRoutes.set(
                    self.previewPheromoneInitialSurRoutes(
                            listVilles, listRoutes, villeNid, villeFood,
                            population.get()))
            self.setupCanvas(listVilles, listRoutes, villeNid, villeFood, 
                         pheromoneInitialSurRoutes.get())
            # self.__zoneAffichage.delete(ALL)

        def isNumbersInEntry(char):
            return char.isdigit()
        
        # Création d'une sous boite
        leftFrame = Frame(self, height=640, width=240, bg="#eee4da")
        leftFrame.grid(row=0, column=0)#, sticky = W)

        validationNumber = leftFrame.register(isNumbersInEntry)

        # Seulement pour avoir la bonne mise en page avec grid        
        leftSpaceLabelColumn0 = Label(leftFrame, text="", bg="#eee4da")
        leftSpaceLabelColumn0.grid(row=0, column=0, padx = 60, pady=2)
        leftSpaceLabelColumn1 = Label(leftFrame, text="", bg="#eee4da")
        leftSpaceLabelColumn1.grid(row=0, column=1, padx=60, pady=2)
        
        tour = 0
        nouriture  = 0
        # defaultPopulation = 50
        # defaultNMaxTours = 2400
        # defaultSelectionToursMultiples = 1200
        # defaultProbabiliteMutation = 0.01
        # defaultTauxEvaporation = 0.0005

        tourLabel = Label(leftFrame, text="Tours :", bg = "#eee4da")
        tourLabel.grid(row = 1, column = 0)#, padx = 10, pady = 10)
        tourText = Label(leftFrame, text = tour, bg = "#eee4da")
        tourText.grid(row = 1, column = 1)#, padx = 10, pady = 10)

        nouritureLabel = Label(leftFrame, text="Nouriture :", bg = "#eee4da")
        nouritureLabel.grid(row = 2, column = 0)#, padx = 10, pady = 10)
        nouritureText = Label(leftFrame, text = nouriture, bg = "#eee4da")
        nouritureText.grid(row = 2, column = 1)#, padx = 10, pady = 10)

        #Entry box
        nMaxToursLabel = Label(leftFrame, text="Numéro Max de tours :",
                               bg = "#eee4da")
        nMaxToursLabel.grid(row = 3, column = 0)#, padx = 10, pady = 10)
        nMaxTours = IntVar()
        nMaxToursEntry = Entry(leftFrame, text=nMaxTours, validate="key",      
                               validatecommand=(validationNumber, '%S'),
                               bg = "#eee4da")
        nMaxTours.set(DEFAULT_N_MAX_TOURS)
        nMaxToursEntry.grid(row = 3, column = 1)#, padx = 10, pady = 10)

        #Entry box
        selectionToursMultiplesLabel = \
            Label(leftFrame, text="Sélection en tours multiples de :",
                  bg = "#eee4da")
        selectionToursMultiplesLabel.grid(row = 4, column = 0)
        selectionToursMultiples = IntVar()
        selectionToursMultiplesEntry = \
            Entry(leftFrame, text = selectionToursMultiples, 
                  validate="key",      
                  validatecommand=(validationNumber, '%S'),
                  bg = "#eee4da")
        selectionToursMultiples.set(DEFAULT_SELECTION_TOURS_MULTIPLES)
        selectionToursMultiplesEntry.grid(row = 4, column = 1)

        #Entry box
        populationLabel = Label(leftFrame, text="Population :", bg = "#eee4da")
        populationLabel.grid(row = 5, column = 0)#, padx = 10, pady = 10)
        population = IntVar()
        populationEntry = Entry(leftFrame, text = population, bg = "#eee4da")
        population.set(DEFAULT_POPULATION)
        populationEntry.grid(row = 5, column = 1)#, padx = 10, pady = 10)

        #Entry box
        probabiliteMutationLabel = Label(leftFrame, 
                                         text="Probabilite de Mutation :",
                                         bg = "#eee4da")
        probabiliteMutationLabel.grid(row = 6, column = 0)
        probabiliteMutation = DoubleVar()
        probabiliteMutationEntry = Entry(leftFrame,
                                         text =  probabiliteMutation,
                                         bg = "#eee4da")
        probabiliteMutation.set(DEFAULT_PROBABILITE_MUTATION)
        probabiliteMutationEntry.grid(row = 6, column = 1)

        #Entry box
        tauxEvaporationLabel = Label(leftFrame, text="Taux d'evaporation :",
                                     bg = "#eee4da")
        tauxEvaporationLabel.grid(row = 7, column = 0)#, padx = 10, pady = 10)
        tauxEvaporation = DoubleVar()
        tauxEvaporationEntry = Entry(leftFrame,
                                     text =  tauxEvaporation,
                                     bg = "#eee4da")
        tauxEvaporation.set(DEFAULT_TAUX_EVAPORATION)
        tauxEvaporationEntry.grid(row = 7, column = 1)#, padx = 10, pady = 10)

        #Entry box
        crossoverSizeLabel = Label(leftFrame, text="Taille du crossover :",
                                   bg = "#eee4da")
        crossoverSizeLabel.grid(row=8, column=0)#, padx = 10, pady = 10)
        crossoverSize = IntVar()
        crossoverSizeEntry = Entry(leftFrame, text=crossoverSize,
                                   validate="key",      
                                   validatecommand=(validationNumber, '%S'),
                                   bg = "#eee4da")
        crossoverSize.set(DEFAULT_CROSSOVER_SIZE)
        crossoverSizeEntry.grid(row=8, column=1)#, padx = 10, pady = 10)

        #Entry box
        pheromoneInitialSurRoutesLabel = Label(
                leftFrame, text="Pheromone initial sur les routes :",
                bg = "#eee4da")
        pheromoneInitialSurRoutesLabel.grid(row = 9, column = 0)
        pheromoneInitialSurRoutes = DoubleVar()
        pheromoneInitialSurRoutesEntry = Entry(leftFrame,
                                         text =  pheromoneInitialSurRoutes,
                                         bg = "#eee4da")
        pheromoneInitialSurRoutes.set(
                self.previewPheromoneInitialSurRoutes(listVilles, listRoutes,
                                                      villeNid, villeFood,
                                                      population.get()))
        pheromoneInitialSurRoutesEntry.grid(row = 9, column = 1)

        self.setupCanvas(listVilles, listRoutes, villeNid, villeFood, 
                         pheromoneInitialSurRoutes.get())

        myButton =  Button(leftFrame, text="Calcule pheromone",
                           command = updateEntries)
        myButton.grid(row = 10, column = 0)


        startSimulation = Button(leftFrame, text="Start Simulation", 
                                 command=lambda: \
                                 master.startCivilisationSimulation(
                                 SimulationPage, nMaxTours.get(),
                                 listVilles, listRoutes,
                                 "Civil", 
                                 villeNid, villeFood,
                                 population.get(),
                                 selectionToursMultiples.get(),
                                 probabiliteMutation.get(),
                                 tauxEvaporation.get(),
                                 crossoverSize.get(),
                                 self.__nomFichier))
        startSimulation.grid(row = 11, column = 0)
        
        # Création d'une sous boite
        rightFrame = Frame(self, height = 640, width = 240, bg = "#eee4da")
        rightFrame.grid(row = 0, column = 2)#, sticky = W)
        rightSpaceLabel = Label(rightFrame, text="", bg = "#eee4da")
        rightSpaceLabel.grid(row = 0, column = 0, padx = 60, pady = 2)
        rightSpaceLabel1 = Label(rightFrame, text="", bg = "#eee4da")
        rightSpaceLabel1.grid(row = 0, column = 1, padx = 60, pady = 2)

    def getEnvironementDefault(self):
        listVilles = []
        # Creation de cinq villes
        listVilles.append(Ville(600/2,300/2,"Lyon"))
        listVilles.append(Ville(200/2,450/2,"Nantes"))
        listVilles.append(Ville(450/2,600/2,"Paris"))
        listVilles.append(Ville(500/2,800/2,"Lille"))
        listVilles.append(Ville(700/2,100/2,"Marseille"))
        print("Villes en France")
        # print("\t ", listVilles)
        # print(*listVilles, sep='\n')
        listRoutes = []
        # Creation de huit routes
        # routeLyonNantes
        listRoutes.append(Route(100, listVilles[0], listVilles[1]))
        # routeLyonParis 
        listRoutes.append(Route(100, listVilles[0], listVilles[2]))
        # routeLyonLille 
        listRoutes.append(Route(100, listVilles[0], listVilles[3]))
        # routeLyonMarseille 
        listRoutes.append(Route(100, listVilles[0], listVilles[4]))
        # routeNantesParis 
        listRoutes.append(Route(100, listVilles[1], listVilles[2]))
        # routeNantesLille 
        listRoutes.append(Route(100, listVilles[1], listVilles[3]))
        # routeNantesMarseille 
        listRoutes.append(Route(100, listVilles[1], listVilles[4]))
        # routeParisLille
        listRoutes.append(Route(100, listVilles[2], listVilles[3]))

        # Identifie et stock les arêtes conectées
        for ville in listVilles:
            ville.mesAretes(listRoutes)
        print("Routes")

        # print("\t1 ", listRoutes)
        # print(*listRoutes, sep='\n')

        villeNid = listVilles[4]# villeNid Marseille
        villeFood = listVilles[2]  # villeNid Paris
        print("_"*80)

        return listVilles, listRoutes, villeNid, villeFood

    def previewPheromoneInitialSurRoutes(self, listVilles, listRoutes,
                                         villeNid, villeFood, nIndividus):
        # Au départ, on initialise les paramètres de la manière suivante :
        # for all (i, j) arete du graphe, tij = t0 = m / Cnn
        # Où m est le nombre de fourmis et Cnn est la longueur de la tournée 
        # réalisée par  l’heuristique "les plus proches voisins" (va simplement 
        # de proche en proche voisin).
        # + Ou bien par tout autre algorithme qui permet de construire 
        # raisonnablement un tour optimisé, au moins localement.
        print("longueurTournee")
        longueurTournee = Civilisation.longueurTournee(listVilles, villeNid,
                                                       villeFood)
        pheromoneInitialSurRoutes = nIndividus/longueurTournee
        print("pheromoneInitialSurRoutes : ", pheromoneInitialSurRoutes)
        [arete.setPheromone(pheromoneInitialSurRoutes) for arete in listRoutes]

        # Mise à jour pheromone pour les arêtes conectées
        [ville.updatePheromoneAretesConectees(listRoutes)
                for ville in listVilles]
        return pheromoneInitialSurRoutes

    def setupCanvas(self, listVilles, listRoutes, villeNid, villeFood, 
                    pheromoneInitialSurRoutes):
        self.__zoneAffichage.printVilles(listVilles, villeNid, villeFood)
        self.__zoneAffichage.printRoutes(listRoutes, pheromoneInitialSurRoutes)

class SimulationPage(Frame):
    """Frame page de Simulation

    SimulationPage correspond à page qui réalise la simulation
    """
    def __init__(self, master, civilisation, nMaxTours, nomFichier=None):
        Frame.__init__(self, master)
        self.__master = master
        self.__civilisation = civilisation
        self.__nomFichier = nomFichier

        self.__idAlarmCallback = None

        # get pheromoneInitialSurRoutes
        villes = self.__civilisation.getListVilles()
        aretes = villes[0].getAretesConectees()
        self.__pheromoneInitialSurRoutes = aretes[0].getPheromone()
        
        self.__nMaxTours = nMaxTours

        self.__zoneAffichageSimulation = ZoneAffichage(self, 640, 640, 'snow2')
        self.__zoneAffichageSimulation.grid(row = 0, column = 1)      

        print("_" * 80)
        print("Start simulation")
        print("_" * 80)
        self.simulation()  
    
    def simulation(self):
        self.__tours = 0
        lastTurn = False
        self.createInterface(self.__tours, lastTurn)

        self.__civilisation.configTour()

        self.updateInterface()
        # while (self.__tours < self.__nMaxTours+1):
            # if (self.__tours % 1000 == 0):   
            #     print("Tour : ", self.__tours)
            #     # print("*self.__listAnts, size", 
            #             len(self.__listAnts), *self.__listAnts ,sep="\n")
            #     print("*self.__listRoutes, size", 
            #           *(self.__civilisation.getListRoutes()), sep="\n")
            #                
            # self.updateInterface()
            # self.__master.updater()    
            # self.__civilisation.tourSuivant(self.__tours)
            # self.__tours = self.__tours + 1
        
        # self.after_cancel(self.__idAlarmCallback)

        lastTurn = True
        self.updateInterface()#self.__tours, lastTurn)

    def result(self): 
        print("Longueur Tournee")
        longueurTournee = \
            Civilisation.longueurTournee(self.__civilisation.getListVilles(),
                                         self.__civilisation.getVilleNid(),
                                         self.__civilisation.getVilleFood())
        print("longueur Tournee - Algorithme génétique")
        longueurTourOptimise, listVillesTourOptimise, listRoutesTourOptimise = \
            Civilisation.tourOptimise(self.__civilisation.getListVilles(),
                                      self.__civilisation.getVilleNid(),
                                      self.__civilisation.getVilleFood())
        
        if (longueurTourOptimise is not None):
            self.__zoneAffichageSimulation.delete(ALL)
            self.__zoneAffichageSimulation.printVillesResult(
                                listVillesTourOptimise,
                                self.__civilisation.getListVilles(),
                                self.__civilisation.getVilleNid(),
                                self.__civilisation.getVilleFood())
                
            self.__zoneAffichageSimulation.printRoutesResult(
                                listRoutesTourOptimise,
                                self.__civilisation.getListRoutes(),
                                self.__pheromoneInitialSurRoutes)
        else:
            self.__zoneAffichageSimulation.create_rectangle(8, 8, 400, 50,
                fill="snow2")
            self.__zoneAffichageSimulation.create_text(10, 10, fill="black",
                font="Times 12 italic bold", anchor=NW,
                text="L'algorithme génétique n'a pas trouvé une solution \n" \
                     "avec les paramètres de configuration données")
        
        # Création d'une sous boite
        self.__rightFrame = Frame(self, height=640, width=240, bg="#eee4da")
        self.__rightFrame.grid(row=0, column=2)
        # Seulement pour avoir la bonne mise en page avec grid        
        self.__rightSpaceLabelColumn0 = Label(self.__rightFrame,
                                             text="", bg="#eee4da")
        self.__rightSpaceLabelColumn0.grid(row=0, column=0, padx=34, pady=2)
        self.__rightSpaceLabelColumn1 = Label(self.__rightFrame,
                                             text="", bg="#eee4da")
        self.__rightSpaceLabelColumn1.grid(row=0, column=1, padx=40, pady=2)
        self.__rightSpaceLabelColumn2 = Label(self.__rightFrame,
                                             text="", bg="#eee4da")
        self.__rightSpaceLabelColumn2.grid(row=0, column=2, padx=34, pady=2)

        # Création d'un widget Button (bouton Back)
        self.__boutonBack = Button(self.__rightFrame, text='Page Simulation',
                command=lambda: self.__master.chargerEnvironnemment(
                        SetupSimulationPage, self.__nomFichier))
        self.__boutonBack.grid(row=2, column=1, pady=10)

        # Création d'un widget Button (bouton Home)
        self.__boutonStartPage = Button(self.__rightFrame,
                text='Page d\'accueil',
                command=lambda: self.__master.switch_frame(StartPage, None))
        self.__boutonStartPage.grid(row=3, column=1, pady=10)

        # Création d'un widget Button (bouton Quitter)
        self.__boutonQuitter = Button(self.__rightFrame, text='Quitter',
                command=lambda: self.__master.quitter(SimulationPage))
        self.__boutonQuitter.grid(row=4, column=1, pady=10)

    def updateInterface(self):
        if (self.__tours <= self.__nMaxTours):
            self.__civilisation.tourSuivant(self.__tours)
            
            if (self.__tours %550 == 0 or self.__tours > self.__nMaxTours-3):
                self.__tourText.config(text=str(self.__tours))

                self.__nouritureText.config(
                        text=str(self.__civilisation.getNouritureCollectee()))
                
                self.__zoneAffichageSimulation.printVilles(
                        self.__civilisation.getListVilles(),
                        self.__civilisation.getVilleNid(),
                        self.__civilisation.getVilleFood())
                
                self.__zoneAffichageSimulation.printRoutes(
                        self.__civilisation.getListRoutes(),
                        self.__pheromoneInitialSurRoutes)

            elif (self.__tours % (self.__nMaxTours/3) == 0):   
                print("Tour : ", self.__tours)
                # print("*self.__listAnts, size",
                #       len(self.__listAnts), *self.__listAnts ,sep="\n")
                print("*self.__listRoutes, size", 
                      *(self.__civilisation.getListRoutes()),sep="\n")

            self.__tours = self.__tours + 1
            self.__idAlarmCallback = self.after(1, 
                                                lambda: self.updateInterface())
        else:
            self.after_cancel(self.__idAlarmCallback)
            self.result()

    def createInterface(self, tours, lastTurn = False):
        # Création d'une sous boite
        self.__leftFrame = Frame(self, height=640, width=240, bg="#eee4da")
        self.__leftFrame.grid(row=0, column=0)#, sticky = W)

        # Seulement pour avoir la bonne mise en page avec grid        
        self.__leftSpaceLabelColumn0 = Label(self.__leftFrame,
                                             text="", bg="#eee4da")
        self.__leftSpaceLabelColumn0.grid(row=0, column=0, padx=60, pady=2)
        self.__leftSpaceLabelColumn1 = Label(self.__leftFrame,
                                             text="", bg="#eee4da")
        self.__leftSpaceLabelColumn1.grid(row=0, column=1, padx=60, pady=2)

        # entryText = StringVar()
        # entry = tk.Entry( master, textvariable=entryText )

        tourLabel = Label(self.__leftFrame, text="Tours :", bg="#eee4da")
        tourLabel.grid(row=1, column=0)#, padx = 10, pady = 10)
        tour = IntVar()
        self.__tourText = Label(self.__leftFrame, text=tour, bg="#eee4da")
        tour.set(self.__tours)
        self.__tourText.grid(row=1, column=1)#, padx = 10, pady = 10)

        nouritureLabel = Label(self.__leftFrame,
                               text="Nouriture :", bg="#eee4da")
        nouritureLabel.grid(row=2, column=0)#, padx = 10, pady = 10)
        nouriture = IntVar()
        self.__nouritureText = Label(self.__leftFrame,
                                     text=nouriture, bg="#eee4da")
        nouriture.set(self.__civilisation.getNouritureCollectee())
        self.__nouritureText.grid(row=2, column=1)#, padx = 10, pady = 10)

        #Text box
        nMaxToursLabel = Label(self.__leftFrame,
                               text="Numéro Max de tours :", bg = "#eee4da")
        nMaxToursLabel.grid(row=3, column=0)#, padx = 10, pady = 10)
        nMaxToursText = Label(self.__leftFrame, 
                              text=self.__nMaxTours, bg="#eee4da")
        nMaxToursText.grid(row=3, column=1)#, padx = 10, pady = 10)

        #Text box
        selectionToursMultiplesLabel = \
            Label(self.__leftFrame, text="Sélection en tours multiples de :",
                  bg="#eee4da")
        selectionToursMultiplesLabel.grid(row=4, column=0)
        selectionToursMultiples = self.__civilisation.getSelectionNaturelle()#IntVar()
        selectionToursMultiplesText = \
            Label(self.__leftFrame, text=selectionToursMultiples, bg="#eee4da")
        #selectionToursMultiples.set(
        #       self.__civilisation.getSelectionNaturelle())
        selectionToursMultiplesText.grid(row=4, column=1)

        #Text box
        populationLabel = Label(self.__leftFrame, 
                                text="Population :", bg="#eee4da")
        population = self.__civilisation.getNIndividus()#IntVar()
        populationLabel.grid(row=5, column=0)#, padx = 10, pady = 10)
        populationText = Label(self.__leftFrame, text=population, bg="#eee4da")
        # population.set(self.__civilisation.getNIndividus())
        populationText.grid(row=5, column=1)#, padx = 10, pady = 10)

        #Text box
        probabiliteMutationLabel = Label(self.__leftFrame, 
                                         text="Probabilite de Mutation :",
                                         bg="#eee4da")
        probabiliteMutation = self.__civilisation.getProbabiliteMutation()
        #DoubleVar()
        probabiliteMutationLabel.grid(row=6, column=0)#, padx = 10, pady = 10)
        probabiliteMutationText = Label(self.__leftFrame,
                                        text=probabiliteMutation,
                                        bg="#eee4da")
        # probabiliteMutation.set(self.__civilisation.getProbabiliteMutation())
        probabiliteMutationText.grid(row=6, column=1)#, padx = 10, pady = 10)

        #Text box
        tauxEvaporationLabel = Label(self.__leftFrame, 
                                     text="Taux d'evaporation :",
                                     bg="#eee4da")
        tauxEvaporationLabel.grid(row=7, column=0)#, padx = 10, pady = 10)
        tauxEvaporation = self.__civilisation.getTauxEvaporation()#DoubleVar()
        tauxEvaporationText = Label(self.__leftFrame,
                                    text=tauxEvaporation,
                                    bg="#eee4da")
        #tauxEvaporation.set(self.__civilisation.getTauxEvaporation())
        tauxEvaporationText.grid(row=7, column=1)#, padx = 10, pady = 10)

        #Text box
        crossoverSizeLabel = Label(self.__leftFrame,
                               text="Taille du crossover:", bg = "#eee4da")
        crossoverSizeLabel.grid(row=8, column=0)#, padx = 10, pady = 10)
        crossoverSizeText = Label(self.__leftFrame, 
                              text=self.__civilisation.getCrossoverSize(), 
                              bg="#eee4da")
        crossoverSizeText.grid(row=8, column=1)#, padx = 10, pady = 10)

        pheromoneInitialSurRoutesLabel = Label(
                self.__leftFrame, text="pheromone Initial sur routes :",
                bg="#eee4da")
        pheromoneInitialSurRoutesLabel.grid(row=9, column=0)
        pheromoneInitialSurRoutesText = Label(self.__leftFrame, 
                text=self.__pheromoneInitialSurRoutes, bg="#eee4da")
        pheromoneInitialSurRoutesText.grid(row=9, column=1)
 
        # Création d'une sous boite
        self.__rightFrame = Frame(self, height=640, width=240, bg="#eee4da")
        self.__rightFrame.grid(row=0, column=2)
        # Seulement pour avoir la bonne mise en page avec grid        
        self.__rightSpaceLabelColumn0 = Label(self.__rightFrame,
                                             text="", bg="#eee4da")
        self.__rightSpaceLabelColumn0.grid(row=0, column=0, padx=34, pady=2)
        self.__rightSpaceLabelColumn1 = Label(self.__rightFrame,
                                             text="", bg="#eee4da")
        self.__rightSpaceLabelColumn1.grid(row=0, column=1, padx=40, pady=2)
        self.__rightSpaceLabelColumn2 = Label(self.__rightFrame,
                                             text="", bg="#eee4da")
        self.__rightSpaceLabelColumn2.grid(row=0, column=2, padx=34, pady=2)

        self.__zoneAffichageSimulation.printVilles(
                self.__civilisation.getListVilles(),
                self.__civilisation.getVilleNid(),
                self.__civilisation.getVilleFood())
        if (lastTurn == True):
            self.__zoneAffichageSimulation.printRoutes(
                    self.__civilisation.getListRoutes(),
                    self.__pheromoneInitialSurRoutes)

            # self.__zoneAffichage.printRoutes(
            #     self.__civilisation.getListVilles(),
            #     startPheromone =  self.__pheromoneInitialSurRoutes)

class CreditsPage(Frame):
    """Frame page de Crédits

    CreditsPage correspond à page qui contient les crédits du projet.
    """
    def __init__(self, master, civilisation):
        Frame.__init__(self, master)
        Label(self, text="Colonie de \n Fourmie").\
            grid(row = 0, column = 1, sticky = W)
            #pack(side="top", fill="x", pady=10)

        # frame = Frame(self, bg = '#4065A4')

        # Création d'image
        width = 80
        height= 80

        canvas = Canvas(self, width = width, height = height)
        self.__image = PhotoImage(master = canvas, file="img/ant.png")
        image = PhotoImage(master = canvas, file="img/ant.png")
        canvas.create_image((width/4, height/4), image = self.__image, 
                            anchor = NW)
        canvas.grid(row = 1, column = 0, sticky = W)
        # frame.pack(expand=YES)


        # Création d'une sous boite
        rightFrame = Frame(self)#, bg = '#4065A4')
        rightFrame.grid(row = 1, column = 2, sticky = W)
        
        labelInstitution = Label(rightFrame, text="École Centrale de Lyon")
        labelInstitution.pack()

        labelAuthors = Label(rightFrame, text="Achraf Bella\n" \
                             "Bruno Moreira Nabinger")
        labelAuthors.pack()

        # Création d'une sous boite
        bottomFrame = Frame(self, bg = '#4065A4')
        bottomFrame.grid(row = 2, column = 0, sticky = W)
        
        labelCredits = Label(bottomFrame, text="\nIcon made by Freepik \n " \
                             "from www.flaticon.com")
        labelCredits.pack()


if __name__ == "__main__":
    app = FenPrincipale()
    # app.after(500, createInterface)
    app.mainloop()