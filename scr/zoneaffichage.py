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
from tkinter.filedialog import asksaveasfilename
from random import randint

from ville import * # import classe Ville à partir du fichier ville.py
from route import * # import classe Route à partir du fichier route.py
# import classe Civilisation à partir du fichier civilisation.py
from civilisation import *
from file_manager import *

def removeall_replace(liste, elementToRemove):
        t = [y for y in liste if y != elementToRemove]
        del liste[:]
        liste.extend(t)

class ZoneAffichage(Canvas): # hérite de la classe Tkinter “Canvas”
    """Classe permettant l’affichage des villes et routes

    Zone d’affichage des villes (cercles et texte correpondant au nom de la
    ville) et routes (lignes de largeur variable selon la quantité de phéromone 
    sur la route et texte correspondant de la quantité de phéromone).
    """
    def __init__(self, parent, w, h, c):
        Canvas.__init__(self, master=parent, width=w, height=h, bg=c,
                        relief=RAISED)
        self.__listLines = []
        self.__listTextLines = []

    def printVilles(self, listVilles, villeNid, villeFood, rayon=5,
                    couleur='black', fill_color="white"):
        """Dessine les Villes et écrit le nom de la ville

        Dessine un cercle correspondant à la ville, avec le nom respective
         dans la Zone d’affichage.
        """
        for ville in listVilles:
            cx = ville.getX()
            cy = ville.getY()
            if (ville == villeNid):
                self.create_oval(cx - rayon, cy - rayon,
                                 cx + rayon, cy + rayon,
                                 outline=couleur, fill='blue')
            elif (ville == villeFood):
                self.create_oval(cx - rayon, cy - rayon,
                                 cx + rayon, cy + rayon,
                                 outline=couleur, fill='red')
            else:
                self.create_oval(cx - rayon, cy - rayon,
                                 cx + rayon, cy + rayon,
                                 outline=couleur, fill=fill_color)
            self.create_text(cx - 3*rayon, cy - 3*rayon, fill="darkblue",
                             font="Times 12 italic bold", text=ville.getNom())

    def printVillesResult(self, listVillesTourOptimise, listVilles, villeNid, villeFood, rayonTourOptimise=8, rayonNormale=5, couleurTourOptimise='orange', couleurNormale='gray'):
        """Dessine les Villes et écrit le nom de la ville

        Dessine un cercle correspondant à la ville, avec le nom respective
         dans la Zone d’affichage.
        """
        for ville in listVilles:
            for villeEmpruntee in listVillesTourOptimise:
                cx = ville.getX()
                cy = ville.getY()
                if (ville == villeNid):
                    self.create_oval(cx - rayonTourOptimise, cy - rayonTourOptimise,
                                    cx + rayonTourOptimise, cy + rayonTourOptimise,
                                    outline=couleurTourOptimise, fill='blue')
                    self.create_text(cx - 3*rayonTourOptimise, cy - 3*rayonTourOptimise, fill="darkblue",font="Times 12 italic bold", text=ville.getNom())
                elif (ville == villeFood):
                    self.create_oval(cx - rayonTourOptimise, cy - rayonTourOptimise,
                                    cx + rayonTourOptimise, cy + rayonTourOptimise,
                                    outline=couleurTourOptimise, fill='red')
                    self.create_text(cx - 3*rayonTourOptimise, cy - 3*rayonTourOptimise, fill="darkblue",font="Times 12 italic bold", text=ville.getNom())
                elif (ville == villeEmpruntee):
                    self.create_oval(cx - rayonTourOptimise, cy - rayonTourOptimise,
                                    cx + rayonTourOptimise, cy + rayonTourOptimise,
                                    outline=couleurTourOptimise, fill=couleurTourOptimise)
                    self.create_text(cx - 3*rayonTourOptimise, cy - 3*rayonTourOptimise, fill="darkblue",font="Times 12 italic bold", text=ville.getNom())
                else:
                    self.create_oval(cx - rayonTourOptimise, cy - rayonTourOptimise,
                                    cx + rayonTourOptimise, cy + rayonTourOptimise,
                                    outline=couleurNormale, fill="white")
                    self.create_text(cx - 3*rayonNormale, cy - 3*rayonNormale, fill="gray",font="Times 12 italic bold", text=ville.getNom())
    
    def printRoutes(self, listRoutes, startPheromone, couleur='black'):
        """Dessine les Routes et écrit la quantité de phéromone

        Dessine une ligne correspondant à la route, avec la quantité de phéromone respective, dans la Zone d’affichage. Si les lignes et les text ont déjà été dessinés/écrits avant, realise la mise à jour seulement.
        """
        
        if not self.__listLines:
            for route in listRoutes:
                # ville.getAretesConectees().getPheromone()
                # print(*ville.getAretesConectees())
                # listAretes = ville.getAretesConectees()
                #print("ville", ville)
                # for arete in listAretes:
                coordX1 = route.getPremiereVille().getX()
                coordY1 = route.getPremiereVille().getY()
                coordX2 = route.getSecondeVille().getX()
                coordY2 = route.getSecondeVille().getY()
                longueur = route.getLongueur()
                coordTextX = (coordX1 + coordX2)/2 - int(longueur/25)
                coordTextY = (coordY1 + coordY2)/2 - int(longueur/25)
                #print("arete.getPheromone()", arete.getPheromone())
                    
                width = 1.0
                ratioPheromone = route.getPheromone()/startPheromone
                if (ratioPheromone >= 1):
                    width = width + ratioPheromone
                else:
                    width = ratioPheromone
                    
                line = self.create_line(coordX1, coordY1, coordX2, coordY2,
                                width=width,
                                fill=couleur, activefill='white')
                 
                self.__listTextLines.append( 
                    self.create_text(coordTextX, coordTextY,
                                # anchor = NE,         
                                fill="green",
                                font="Times 12 italic bold",
                                text=float("{:.6f}".format(route.getPheromone()))) )

                self.__listLines.append(line)
        else:
            for i in range(len(listRoutes)):
                width = 1.0
                ratioPheromone = listRoutes[i].getPheromone()/startPheromone
                if (ratioPheromone >= 1):
                    width = width + ratioPheromone
                else:
                    width = ratioPheromone
                    
                # for line in self.__listLines:
                self.itemconfig(self.__listLines[i], width=width, fill=couleur)
                self.itemconfig(self.__listTextLines[i], 
                        text=float("{:.5f}".format(listRoutes[i].getPheromone())),
                        fill="darkgreen")
    
    def printRoutesResult(self, listRoutesTourOptimise, listRoutes, startPheromone, couleurTourOptimise='orange', couleurNormale='gray'):
        """Dessine les Routes et écrit la quantité de phéromone

        Dessine une ligne correspondant à la route, avec la quantité de phéromone respective, dans la Zone d’affichage. Si les lignes et les text ont déjà été dessinés/écrits avant, realise la mise à jour seulement.
        """
        for route in listRoutes:
            for routeEmpruntee in listRoutesTourOptimise:
                # ville.getAretesConectees().getPheromone()
                # print(*ville.getAretesConectees())
                # listAretes = ville.getAretesConectees()
                #print("ville", ville)
                # for arete in listAretes:
                coordX1 = route.getPremiereVille().getX()
                coordY1 = route.getPremiereVille().getY()
                coordX2 = route.getSecondeVille().getX()
                coordY2 = route.getSecondeVille().getY()
                longueur = route.getLongueur()
                coordTextX = (coordX1 + coordX2)/2 - int(longueur/25)
                coordTextY = (coordY1 + coordY2)/2 - int(longueur/25)
                #print("arete.getPheromone()", arete.getPheromone())
                    
                width = 1.0
                ratioPheromone = route.getPheromone()/startPheromone
                if (ratioPheromone >= 1):
                    width = width + ratioPheromone
                else:
                    width = ratioPheromone
                
                if (route.memeRoute(routeEmpruntee)):
                    line = self.create_line(coordX1, coordY1, coordX2, coordY2,
                                width=width,
                                fill=couleurTourOptimise, activefill='orange')
                 
                    self.__listTextLines.append( 
                    self.create_text(coordTextX, coordTextY,
                                # anchor = NE,         
                                fill="darkgreen",
                                font="Times 12 italic bold",
                                text=float("{:.6f}".format(route.getPheromone()))) )

                    self.__listLines.append(line)
                else:
                    line = self.create_line(coordX1, coordY1, coordX2, coordY2,
                                width=width,
                                fill=couleurNormale, activefill='white')
                    self.__listTextLines.append( 
                    self.create_text(coordTextX, coordTextY,
                                # anchor = NE,         
                                fill="darkgreen",
                                font="Times 11 italic bold",
                                text=float("{:.6f}".format(route.getPheromone()))) )

                    self.__listLines.append(line)


COULEUR_SELECTED = 'orange'
COULEUR_VILLE_FOOD = 'red'
COULEUR_VILLE_NID = 'blue'


class ZoneAffichageCreation(Canvas): # hérite de la classe Tkinter “Canvas”
    """Classe permettant l’affichage des villes et routes

    Zone d’affichage des villes (cercles et texte correpondant au nom de la
    ville) et routes (lignes et texte correspondant de la longueur de la route).
    Utilisée lors de la création d'un nouveaux environnement
    """
    def __init__(self, parent, w, h, c):
        Canvas.__init__(self, master=parent, width=w, height=h, bg=c,
                        relief=RAISED)
        self.__master = parent
        self.__width = w
        self.__height = h
        # self.__idAlarmCallback = None
        self.__villesGraphiques = []
        self.__routesGraphiques = []
        self.__villesSelected = 0
        self.__villeNid = 0
        self.__villeFood = 0
        self.__villeNidActive = False
        self.__villeFoodActive = False

        self.__CoordText = self.create_text(
            w - 36, h-12, fill="darkgray",
            font="Times 12 italic bold", text="")

        # self.bind("<Button-1>", self.click)
        self.bind("<Button-1>", self.click)
        # self.bind("<B1-Motion>", self.drawCoord)
        self.focus_set()
        self.bind("<Shift_L>", self.drawCoord)
        self.bind("<Delete>", self.deleteSelected)
    
    def toggleVilleNid(self, status):
        self.__villeFoodActive = False
        self.__villeNidActive = status
        if (not self.__villeNidActive):
            self.__villeFoodActive = False
            villeNid = self.getVilleSelected()
            if (villeNid is not None):
                self.setNidAllVilles(False)
                villeNid.setVilleFood(False)
                villeNid.setVilleNid(True)
                self.__villeNid = 1
                            
    def toggleVilleFood(self, status):
        self.__villeNidActive = False
        self.__villeFoodActive = status
        if (not self.__villeFoodActive):
            self.__villeNidActive = False
            villeFood = self.getVilleSelected()
            if (villeFood is not None):
                self.setFoodAllVilles(False)
                villeNid.setVilleNid(False)
                villeFood.setVilleFood(True)
                self.__villeFood = 1

    def deleteSelected(self, event):
        print("DELETE")
        self.delVilleSelected()
        self.delRouteSelected()
        self.setAllVillesSelected(False)
        self.setAllRoutesSelected(False)
        self.__villesSelected = 0
        self.redraw()
        self.update_idletasks()
        self.after(10)

    def click(self, event):
        print("Trace : (x,y) = ", event.x, event.y)

        # print("self.find_withtag(CURRENT)", self.find_withtag(CURRENT))
        currentIdTag = self.find_withtag(CURRENT)
        if (currentIdTag):
            if (self.__villeNidActive):
                ville = self.getVilleCheckCanvasIdCercle(currentIdTag)
                if (ville is not None):
                    self.setAllVillesSelected(False)
                    self.setAllRoutesSelected(False)
                    self.setNidAllVilles(False)
                    ville.setSelected(False)
                    ville.setVilleFood(False)
                    ville.setVilleNid(True)
                    self.__villeNid = 1
                    self.__villesSelected = 0
            elif (self.__villeFoodActive):
                ville = self.getVilleCheckCanvasIdCercle(currentIdTag)
                if (ville is not None):
                    self.setAllVillesSelected(False)
                    self.setAllRoutesSelected(False)
                    self.setFoodAllVilles(False)
                    ville.setSelected(False)
                    ville.setVilleNid(False)
                    ville.setVilleFood(True)
                    self.__villeFood = 1
                    self.__villesSelected = 0
            else:
                route = self.getRouteCheckCanvasIdLine(currentIdTag)
                if (route is not None):
                    self.setAllVillesSelected(False)
                    self.setAllRoutesSelected(False)
                    route.setSelected(True)
                    self.__villesSelected = 0
                else:
                    print("self.__villesSelected = ", self.__villesSelected)
                    if (self.__villesSelected == 0):
                        # set ville to selected
                        ville = self.getVilleCheckCanvasIdCercle(currentIdTag)
                        if (ville is not None):
                            self.setAllVillesSelected(False)
                            self.setAllRoutesSelected(False)
                            ville.setSelected(True)
                            self.__villesSelected = 1
                    elif (self.__villesSelected == 1):
                        # create Route
                        premiereVille = self.getVilleSelected()
                        self.setAllVillesSelected(False)
                        # set ville to selected
                        secondeVille = self.getVilleCheckCanvasIdCercle(currentIdTag)
                        if (secondeVille is not None):
                            newRoute = RouteGraphique(self, premiereVille.getVille(), secondeVille.getVille())
                            self.__routesGraphiques.append(newRoute)
                            # print("New Route", newRoute)
                            self.__villesSelected = 0


                        # self.itemconfig(CURRENT, fill="blue")
                        # self.update_idletasks()
                        # self.after(200)
                        # self.itemconfig(CURRENT, fill="red")
        else:
            # Création d'un nouvelle ville
            self.setAllVillesSelected(False)
            self.setAllRoutesSelected(False)
            self.__villesSelected = 0
            if (self.__villeNidActive):
                self.setNidAllVilles(False)
                newVilleNid = VilleGraphique(self, event.x, event.y, rayon=10, 
                                             couleur='black', fill='white')
                newVilleNid.setVilleNid(True)
                self.__villesGraphiques.append(newVilleNid)
                self.__villeNid = 1
            elif (self.__villeFoodActive):
                self.setFoodAllVilles(False)
                newVilleFood = VilleGraphique(self, event.x, event.y, rayon=10, 
                                              couleur='black', fill='white')
                newVilleFood.setVilleFood(True)
                self.__villesGraphiques.append(newVilleFood)
                self.__villeFood = 1
            else:
                self.__villesGraphiques.append(VilleGraphique(self, event.x, event.y, rayon=10, couleur='black', fill='white'))
                # self.__villesGraphiques.append(newVille)

        self.redraw()
        self.update_idletasks()
        self.after(10)

    def drawCoord(self, event):
        if (0 <= event.x <= self.__width and 0 <= event.y <= self.__height):
            self.itemconfig(self.__CoordText, text="(" + str(event.x) + ","
                                                    + str(event.y) + ")")
        self.update_idletasks()

    def getVillesGraphiques(self):
        return self.__villesGraphiques
    
    def getRoutesGraphiques(self):
        return self.__routesGraphiques

    def getVilleNid(self):
        return villeNid

    def getVilleFood(self):
        return villeFood

    def getVilleCheckCanvasIdCercle(self, currentIdTag):
        for ville in self.__villesGraphiques:
            if (ville.checkCanvasIdCercle(currentIdTag)):
                return ville
        return None

    def getRouteCheckCanvasIdLine(self, currentIdTag):
        for route in self.__routesGraphiques:
            if (route.checkCanvasIdLine(currentIdTag)):
                return route
        return None
    

    def getVilleSelected(self):
        for ville in self.__villesGraphiques:
            if (ville.getSelected()):
                return ville
        return None
    
    def setAllVillesSelected(self, status=False):
        for villes in self.__villesGraphiques:
            villes.setSelected(status)

    def setNidAllVilles(self, status=False):
        for villes in self.__villesGraphiques:
            villes.setVilleNid(status)
    
    def setFoodAllVilles(self, status=False):
        for villes in self.__villesGraphiques:
            villes.setVilleFood(status)

    def getRouteSelected(self):
        for route in self.__routesGraphiques:
            if (route.getSelected()):
                return route
        return None

    def setAllRoutesSelected(self, status=False):
        for routes in self.__routesGraphiques:
            routes.setSelected(status)

    

    def delVilleSelected(self):
        for ville in self.__villesGraphiques:
            if (ville.getSelected()):
                # Tout d'abord, supprime les routes liées à la ville
                for i in range(len(self.__routesGraphiques)):
                    for ville2 in self.__villesGraphiques:
                        if (ville2 is not ville and 
                                self.__routesGraphiques[i] is not None):
                            if (self.__routesGraphiques[i]. \
                                    getRoute().isRoute(ville.getVille(),
                                                       ville2.getVille())):
                                self.delete(self.__routesGraphiques[i]. \
                                    getCanvasIdLine())
                                self.delete(self.__routesGraphiques[i]. \
                                    getCanvasIdText())
                                self.__routesGraphiques[i] = None
                removeall_replace(self.__routesGraphiques, None)
                self.delete(ville.getCanvasIdCercle())
                self.delete(ville.getCanvasIdText())
                self.__villesGraphiques.remove(ville)
                print("\tFinal self.__villesGraphiques:", len(self.__villesGraphiques))
                print("\tFinal self.__routesGraphiques:", len(self.__routesGraphiques))
                break
                
    def delRouteSelected(self):
        for route in self.__routesGraphiques:
            if (route.getSelected()):
                print("self.__routesGraphiques:", len(self.__routesGraphiques))
                self.delete(route.getCanvasIdLine())
                self.delete(route.getCanvasIdText())
                self.__routesGraphiques.remove(route)
                print("After self.__routesGraphiques:", len(self.__routesGraphiques))
                break

    def redraw(self):
        for ville in self.__villesGraphiques:
            ville.redraw()
        for route in self.__routesGraphiques:
            route.redraw()
            

class VilleGraphique(Ville):
    """Représent les noeuds
    
    ***************************************************************************
    
    Attributs:
        x (int): Coordonné x de la ville
        y (int): Coordonné y de la ville
        nom (string): Nom de la ville
    """

    listNames = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    conteurListNames = 0

    def __init__(self, master, cx, cy, rayon=10, couleur='black', fill='white'):
        self.__ville = Ville(cx, cy, self.listNames[VilleGraphique.conteurListNames])
        VilleGraphique.conteurListNames += 1
        self.__rayon = rayon
        self.__color = couleur
        self.__master = master  # Il le faut pour les déplacements
        self.__isSelected = False
        self.__VilleNid = False
        self.__VilleFood = False

        print("self.conteurListNames", self.conteurListNames)

        self.__canvasIdText = self.__master.create_text(
            cx - 3*rayon, cy - 3*rayon, fill="darkblue",
            font="Times 12 italic bold", text=self.__ville.getNom())

        self.__canvasIdCercle = self.__master.create_oval(
            cx - rayon, cy - rayon, cx + rayon, cy + rayon, outline=couleur, fill=fill)

    def checkCanvasIdCercle(self, id):
        if (id[0] == self.__canvasIdCercle):
            return True
        return False 
        # self.__isSelected = True

    def getVille(self):
        return self.__ville
    
    def getCanvasIdCercle(self):
        return self.__canvasIdCercle
    
    def getCanvasIdText(self):
        return self.__canvasIdText

    def getSelected(self):
        return self.__isSelected

    def getVilleNid(self):
        return self.__VilleNid

    def getVilleFood(self):
        return self.__VilleFood

    def setSelected(self, status):
        self.__isSelected = status

    def setVilleNid(self, status):
        self.__VilleNid = status

    def setVilleFood(self, status):
        self.__VilleFood = status

    def redraw(self):
        if (self.__isSelected):
            self.__master.itemconfig(self.__canvasIdCercle,     
                                     outline=COULEUR_SELECTED)
        else:
            self.__master.itemconfig(self.__canvasIdCercle, 
                                     outline='black')

        self.__master.itemconfig(self.__canvasIdCercle,
                                     fill='white')
        
        if (self.__VilleFood):
            self.__master.itemconfig(self.__canvasIdCercle, 
                                     fill=COULEUR_VILLE_FOOD)
        if (self.__VilleNid):
            self.__master.itemconfig(self.__canvasIdCercle,
                                     fill=COULEUR_VILLE_NID)

        # def cercleArea(self, x, y):
        #     if ((self.__ville.getX() - self.__rayon <= x) and
        #             (x <= self.__ville.getX() + self.__rayon) and
        #             (self.__ville.getY() - self.__rayon <= y) and
        #             (y <= self.__ville.getX() + self.__rayon)):
        #         return True
        #     return False
            

class RouteGraphique(Route):
    """Représent les arêtes du graphe
    
    Text***********************************************************************
    
    Attributs:
        longueur (int): Longueur de la route (arête)
        pheromone (float): Intensite de la phéromone sur la route, mésure par
            un nombre réel
        premiere (Ville): Ville connectée à cette route
        seconde (Ville): Ville connectée à cette route
    """

    def __init__(self, master, premiereVille, secondeVille):
        self.__route = Route(0, premiereVille, secondeVille)
        self.__master = master
        self.__isSelected = False

        coordX1 = self.__route.getPremiereVille().getX()
        coordY1 = self.__route.getPremiereVille().getY()
        coordX2 = self.__route.getSecondeVille().getX()
        coordY2 = self.__route.getSecondeVille().getY()
        longueur = self.__route.getLongueur()
        coordTextX = (coordX1 + coordX2)/2 - int(longueur/25)
        coordTextY = (coordY1 + coordY2)/2 - int(longueur/25)

        self.__canvasIdLine = self.__master.create_line(
            premiereVille.getX(), premiereVille.getY(), 
            secondeVille.getX(), secondeVille.getY(),
            width=2.0, fill='black', activefill='white')

        self.__canvasIdText = self.__master.create_text(
            coordTextX, coordTextY, fill="darkgreen",
            font="Times 12 italic bold", text=float("{:.2f}".format(longueur)))

    def checkCanvasIdLine(self, id):
        if (id[0] == self.__canvasIdLine):
            return True
        return False 
        # self.__isSelected = True

    def getRoute(self):
        return self.__route

    def getCanvasIdLine(self):
        return self.__canvasIdLine
    
    def getCanvasIdText(self):
        return self.__canvasIdText

    def getSelected(self):
        return self.__isSelected

    def setSelected(self, status):
        self.__isSelected = status

    def redraw(self):
        if (self.__isSelected):
            self.__master.itemconfig(self.__canvasIdLine,     
                                     fill=COULEUR_SELECTED)
        else:
            self.__master.itemconfig(self.__canvasIdLine, 
                                     fill='black')



        # def action_clique(self, event):
        #         print("Trace : (x,y) = ", event.x, event.y)
        #         if (self.__villesSelected == 0):
        #             for ville in self.__villesGraphiques:
        #                 if (ville.cercleArea(event.x, event.y)):
        #                     for villes in self.__villesGraphiques:
        #                         villes.setSelected(False)
        #                     ville.setSelected(True)
        #                     self.__villesSelected = 1   
        #                     break
        #         elif (self.__villesSelected == 1):
        #             for ville in self.__villesGraphiques:
        #                 if (ville.cercleArea(event.x, event.y)):
        #                     for villes in self.__villesGraphiques:
        #                         villes.setSelected(False)
        #                         RouteGraphique
        #                     self.__villesSelected = 0   
        #                     break

    def __str__(self): # Opérateur d’affichage utilisé par print
        return self.__route.__str__()