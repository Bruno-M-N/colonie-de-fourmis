# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 16:31:20 2015

@author: Bruno Moreira Nabinger

stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
"""

# from formes import *
from jouer import *
from tkinter import *
from random import randint


class ZoneAffichage(Canvas): # hérite de la classe Tkinter “Canvas”
    """Classe permettant l’affichage des images du pendu

    Zone d’affichage des images utilisées pour représenter les différents états
    du pendu. À chaque étape, l’image correspondant au nombre d’échecs du
    joueur est affichée (images disponibles sur le site pedagogie ont été mises
    dans un dossier "ImagesPendu").
    """
    def __init__(self, parent, w, h, c):
        Canvas.__init__(self, master=parent, width=w, height=h, bg=c)
        self.__photo = PhotoImage(file='ImagesPendu/pendu1.gif')

#        ymax = h
#        self.__dessin = Dessin()
#        f = Rectangle(100,ymax-50,100,5,couleurs[5])
#        self.__dessin.add_forme(f)
#        f = Rectangle(100,ymax-150,5,200,couleurs[5])
#        self.__dessin.add_forme(f)
#        f = Rectangle(148,ymax-250,100,5,couleurs[5])
#        self.__dessin.add_forme(f)
#        f = Rectangle(200, ymax-232,5,40,couleurs[5])
#        self.__dessin.add_forme(f)
#        f = Cercle(200,ymax-200,30,couleurs[5])
#        self.__dessin.add_forme(f)
#        f = Rectangle(200, ymax-170,15,50,couleurs[5])
#        self.__dessin.add_forme(f)
#        f = Rectangle(178, ymax-170,30,5,couleurs[5])
#        self.__dessin.add_forme(f)
#        f = Rectangle(220, ymax-170,30,5,couleurs[5])
#        self.__dessin.add_forme(f)
#        f = Rectangle(195, ymax-130,5,40,couleurs[5])
#        self.__dessin.add_forme(f)
#        f = Rectangle(205, ymax-130,5,40,couleurs[5])
#        self.__dessin.add_forme(f)

    def afficher(self, nb):
        """Affiche l’image correspondant au nombre d’échecs du joueur

        Affiche l’image correspondant au nombre d’échecs du joueur en changent
        l' attribut "photo".

        Parameters:
            nb (int) : nombre d'éhecs du jouer
        Returns:
            None
        """
        print("Nb :", nb)
        self.__photo = PhotoImage(file='ImagesPendu/pendu.gif')
        if nb == 0:
            self.__photo = PhotoImage(file='ImagesPendu/pendu1.gif')
        elif nb == 1:
            self.__photo = PhotoImage(file='ImagesPendu/pendu2.gif')
        elif nb == 2:
            self.__photo = PhotoImage(file='ImagesPendu/pendu3.gif')
        elif nb == 3:
            self.__photo = PhotoImage(file='ImagesPendu/pendu4.gif')
        elif nb == 4:
            self.__photo = PhotoImage(file='ImagesPendu/pendu5.gif')
        elif nb == 5:
            self.__photo = PhotoImage(file='ImagesPendu/pendu6.gif')
        elif nb == 6:
            self.__photo = PhotoImage(file='ImagesPendu/pendu7.gif')
        elif nb == 7:
            self.__photo = PhotoImage(file='ImagesPendu/pendu8.gif')
        else:
            self.__photo = PhotoImage(file='ImagesPendu/pendu.gif')
        self.create_image(0, 0, anchor=NW, image=self.__photo)
        self.config(height=self.__photo.height(), width=self.__photo.width())
#        self.__dessin.affiche_formes(self, nb)

    def getNbCoupsPossibles(self):
        return 8
#        return self.__dessin.size()


class MonBouton(Button): # hérite de la classe Tkinter “Button”
    """Classe de boutons pour le clavier virtuel

    Boutons qui correspondent aux touches du clavier virtuel.
    """
    # Constructeur de la classe MonBouton
    def __init__(self, parent, fen, t, w):
        Button.__init__(self, master=parent, text=t, width=w)
        self.__fenetrePrincipale = fen
        self.__lettre = t

    def cliquer(self):
        self.config(state=DISABLED)
        self.__fenetrePrincipale.traitement(self.__lettre)


class FenPrincipale(Tk):
    """Classe de l'interface principale

    Correspondant à l’interface principale et gérant l’application
    """
    def __init__(self):
        Tk.__init__(self)
        self.title('Jeu du pendu')

        self.__mot = ''
        self.__motAffiche = ''
        self.__mots = []
        self.__nbManques = 0

        self.__jouer = None

        self._frame = None
        self.switch_frame(PageNom, self.__jouer)

    def switch_frame(self, frame_class, jouer):
        """Destroys current frame and replaces it with a new one.

        It works by accepting any Class object that implements Frame. The
        function then creates a new frame to replace the old one.

        Reference:
            Based on the code by Steven M. Vascellaro, in a post called "Switch
            between two frames in tkinter" in Stackoverflow.com, a question and
            answer site for professional and enthusiast programmers.
        Parameters:
            frame_class: Any Class object that implements Frame. For this
                application: PageNom, StartPage, PageHistorique and PageGame
            jouer (Jouer): Jouer
        Returns:
            None
        """
        new_frame = frame_class(self, jouer)
        # Deletes old _frame if it exists, then replaces it with the new frame.
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

#    def historiqueJouer(self):
#        return self.__jouer

    def quitter(self, frame_class):
        """Ferme le programme

        Accept n'importe quel objet d'une classe qui implements Frame.

        Parameters:
            frame_class: n'importe quel objet d'une classe qui implements
                Frame. Pour cette application: PageNom, StartPage,
                PageHistorique and PageGame
        Returns:
            None
        """
        self.destroy()

#    def recupereInfoPartie(mot, result):
#        print("recupereInfoPartie")
#        self.__jouer.miseAJourHistorique(mot, result)
#        print("END recupereInfoPartie")

    def reinitialiserhistoriqueJouer(self, frame_class):
        """Reinitialise l'historique du Jouer

        Reinitialise l'historique du Jouer.

        Parameters:
            frame_class: n'importe quel objet d'une classe qui implements
                Frame. Pour cette application: PageNom, StartPage,
                PageHistorique and PageGame
        Returns:
            None
        """
        self.__jouer.reinitialiserHistorique()
        self.switch_frame(frame_class, self.__jouer)

    def confirm_Nom(self, frame_class, nom):
        """Confirm nom du Jouer

        Lié a une button, ce méthode permettre de confirmer le nom du jouer, si
        le nom n'est pas vide (''). Il permettre aussi de changer le frame

        Parameters:
            frame_class: n'importe quel objet d'une classe qui implements
                Frame. Pour cette application: PageNom, StartPage,
                PageHistorique and PageGame
            nom (StringVar): nom du jouer
        Returns:
            None
        """
        print("Confirm_Nom en FenPrincipale. Nom : ", nom)
        if nom != '':
            self.__jouer = Jouer(nom.get())
            self.switch_frame(frame_class, self.__jouer)
        print("Jouer ", self.__jouer)


class PageNom(Frame): # hérite de la classe Tkinter “Frame”
    """Frame qui permettre de choisir le nom du jouer

    PageNom correspond à page qui est affiché au début du programme et à chaque
    fois qui l'utilisateur clique sur le bouton "Choisir nom".
    Elle renvoi l'utilisateur à la page StartPage.
    """
    def __init__(self, master, jouer):

        Frame.__init__(self, master)
        # Création d'un widget Label (texte 'Choisi votre nom') centralisé en
        # haut du frame
        Label(self, text="Choisi votre nom").\
            pack(side="top", fill="x", pady=10)

        # Création d'un widget Label (texte 'Nom : ')
        label = Label(self, text='Nom : ')
        label.pack(side=LEFT, padx=5, pady=5)

        self.__jouer = jouer
        #  créé un objet de type StringVar qui va stocker une variable de type
        # string
        nom = StringVar(value="")
        if jouer is not None:
            nom = StringVar(value=jouer.getNom())
        print("NOM : ", nom)
        # Création d'un widget Entry (champ de saisie)
        texte = Entry(self, textvariable=nom, bg='bisque', fg='maroon')
        texte.focus_set()
        texte.pack(side=LEFT, padx=5, pady=5)

        Button(self, text="Confirm",
               command=lambda: master.confirm_Nom(StartPage, nom)).pack(
                       side="bottom", padx=5, pady=5)


class StartPage(Frame):
    """Frame Menu

    StartPage correspond à page qui contient un menu pour les autres pages, à
    savoir PageNom, PageHistorique and PageGame. Elle permettre aussi de sortir
    du programme quand l'utilisateur clique sur le bouton "Quitter".
    """
    def __init__(self, master, jouer):
        Frame.__init__(self, master)
        self.__jouer = jouer
#        Label(self, text = nom).pack(side="top", fill="x", pady=10)

        Label(self, text=jouer.getNom()).\
            pack(side="top", fill="x", pady=10)
        Button(self, text="Choisir nom",
               command=lambda: master.switch_frame(PageNom,
                                                   self.__jouer)).pack()
        Button(self, text="Historique",
               command=lambda: master.switch_frame(PageHistorique,
                                                   self.__jouer)).pack()
        Button(self, text="Nouvelle Partie",
               command=lambda: master.switch_frame(PageGame,
                                                   self.__jouer)).pack()
        # Création d'un widget Button (bouton Quitter)
        Button(self, text='Quitter', width=15, command=lambda:
               master.quitter(PageGame)).pack(side=LEFT, padx=5, pady=5)


class PageHistorique(Frame):
    """Frame qui permettre de voir l'historique du jouer

    PageHistorique correspond à page qui est affiché quand l'utilisateur clique
    sur le bouton "Historique" dans StartPage.
    """
    def __init__(self, master, jouer):
        Frame.__init__(self, master)
        self.__jouer = jouer
#        Label(self, text = "Score").pack(side = "top", fill = "x", pady = 10)
#        Label(self, text = "Historique").pack(side = "top", fill= "x", \
#            pady = 10)
        Label(self, text = jouer).pack(side = "top", fill = "x", pady = 10)
        # lambda: master.historiqueJouer()).pack(side="top", fill="x", pady=10)
        Button(self, text="Reinitialiser Historique", command=lambda:
               master.reinitialiserhistoriqueJouer(PageHistorique)).pack()
        Button(self, text="Return to start page",
               command=lambda: master.switch_frame(StartPage,
                                                   self.__jouer)).pack()


class PageGame(Frame):
    def __init__(self, master, jouer):
        Frame.__init__(self, master)
        self.__jouer = jouer

        f1 = Frame(self)
        f1.pack(side=TOP, padx=5, pady=5)

        # Création d'un widget Button (bouton Nouvelle partie)
        Button(f1, text='Nouvelle partie', width=15,
               command=self.nouvellePartie).pack(side=LEFT, padx=5, pady=5)

#        # Création d'un widget Button (bouton Quitter)
#        Button(self, text ='Quitter', width=15,
#           command = lambda: master.quitter(PageGame)).pack(side = LEFT,\
#           padx = 5, pady = 5)
#
        Label(self, text="GAME").pack(side="top", fill="x", pady=10)
        Button(self, text="Return to start page",
               command=lambda: master.switch_frame(StartPage,
                                                   self.__jouer)).pack()

        self.__zoneAffichage = ZoneAffichage(self, 350, 320, 'snow2')
        self.__zoneAffichage.pack(side=TOP, padx=5, pady=5)

        self.__lmot = Label(self, text='Mot :')
        self.__lmot.pack(side=TOP)

        f2 = Frame(self)
        f2.pack(side=TOP, padx=5, pady=5)

        self.__boutons = []
        for i in range(26):
            # Ajoute un bouton disposé dans une Frame “f2”, de largeur “4” et
            # dont le texte est la valeur de “t”) à la liste des boutons de
            # “PageGame” et association du clic sur ce bouton à sa méthode
            # “cliquer” :
            t = chr(ord('A')+i)
            self.__boutons.append(MonBouton(f2, self, t, 4))
            self.__boutons[i].config(command=self.__boutons[i].cliquer)

        for i in range(3):
            for j in range(7):
                self.__boutons[i*7+j].grid(row=i, column=j)

        for j in range(5):
            self.__boutons[21+j].grid(row=3, column=j+1)

        self.chargeMots()
        self.nouvellePartie()

    def nouvellePartie(self):
        """Réinitialise l’application pour commencer une nouvelle partie

        Cette méthode est exécutée lors d’un clic sur le bouton
        “NouvellePartie”
        """

        # Initialisation de l’attribut “mot”
        self.__mot = self.nouveauMot()
        # B4 Création de la zone d’affichage du mot à découvrir
        self.__motAffiche = len(self.__mot)*'*'
        self.__lmot.config(text='Mot : ' + self.__motAffiche)

        # Initialisation de la zone du dessin du pendu (aucune de ses parties
        # ne doit être affichée)
        self.__nbManques = 0
        self.__zoneAffichage.delete(ALL)
        self.__zoneAffichage.afficher(self.__nbManques)

        # Activation de tous les boutons du clavier virtuel (valeur “normal”
        # pour la propriété “state” du bouton, à modifier avec sa méthode
        # “config”)
        for b in self.__boutons:
            b.config(state='normal')

    def traitement(self, lettre):
        """Traitement des touches du clavier virtuel

        Appelée à chaque fois que le joueur clique sur un bouton (ou touche) du
        clavier virtuel. L’argument de cette méthode est donc la lettre
        correspondant au bouton qui a fait cet appel.
        Le traitement consiste à parcourir l’objet “mot” et à vérifier si la
        lettre correspondant à la touche du clavier virtuelle sélectionnée en
        fait partie. Si c’est le cas, le caractère “*“ dans l’objet
        “motAffiche” doit être remplacé par cette lettre.

        Parameters:
            lettre (char) : Nom du jouer
        Returns:
            None
        """
        compteur = 0
        lettres = list(self.__motAffiche)
        for i in range(len(self.__mot)):
            if self.__mot[i] == lettre:
                compteur += 1
                lettres[i] = lettre

        self.__motAffiche = ''.join(lettres)

        if compteur == 0:
            self.__nbManques += 1
            print("self.__nbManques", self.__nbManques, "/",
                  self.__zoneAffichage.getNbCoupsPossibles())
            self.__zoneAffichage.afficher(self.__nbManques)
            if self.__nbManques >= self.__zoneAffichage.getNbCoupsPossibles():
                self.finPartie(False)
        else:
            self.__lmot.config(text='Mot : ' + self.__motAffiche)
            if self.__mot == self.__motAffiche:
                self.finPartie(True)

    def nouveauMot(self):
        """Définition du nouveau mot pour la nouvelle Partie

        Renvoye une chaîne de caractères qui sera stockée dans l’attribut “mot”
        de la classe “FenPrincipale”. Ainsi, “nouveauMot”sera appelée depuis la
        méthode“ nouvelle Partie” décrite précédemment.

        Parameters:
            None
        Returns:
            mot (string) : nouveau mot pour la nouvelle partie
        """
        return self.__mots[randint(0, len(self.__mots)-1)]

    def chargeMots(self):
        """ Lecture des mots contenus dans le fichier "mots.txt"

        Méthode que se charge de remplir le vecteur “__mots” avec les mots
        contenus dans le fichier “mots.txt”.
        """
        f = open('mots.txt', 'r')
        s = f.read()
        self.__mots = s.split('\n')
        f.close()

    def finPartie(self, gagne):
        """ Traitement correspondant à la fin d’une partie

        Méthode que se charge de la désactivation de toutes les touches du
        clavier virtuel et afficher soit un message de félicitation en cas de
        victoire soit le mot complet en cas de défaite. Il fait aussi le mise a
        jour de l'historique du jouer.

        Parameters:
            gagne (bool) : True indique que le jouer a gagné
                           False indique que le jouer a perdu
        Returns:
            None
        """
        for b in self.__boutons:
            b.config(state=DISABLED)

        if gagne:
            self.__lmot.config(text=self.__mot + ' - Bravo, vous avez gagné')
        else:
            self.__lmot.config(text='Vous avez perdu, le mot était : '
                               + self.__mot)
        # Mise a jour de l'historique
        print("finPartie en PageGame", self.__mot, gagne)
        self.__jouer.miseAJourHistorique(self.__mot, gagne)
        # lambda: master.recupereInfoPartie(self.__mot, gagne)
        print("finPartie en PageGame")


if __name__ == "__main__":
    app = FenPrincipale()
    app.mainloop()
