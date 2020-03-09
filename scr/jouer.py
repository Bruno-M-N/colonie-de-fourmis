# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 10:20:32 2019

@author: Usuario
"""


class Jouer:  # Declaration de la classe Jouer
    def __init__(self, nom):  # Constructeur de la classe Jouer
        """Constructeur de la classe Jouer

        Ouvre ou fait la création d'un archive de extension .txt avec le nom
        forni

        Parameters:
            nom (string) : Nom du jouer
        Returns:
            None
        """
        self.__nom = nom
        self.__historique = Historique(nom)
        self.__historique.lireHistoriqueDansFichier(self.__nom)

    def __str__(self):  # Opérateur d’affichage utilisé par print
        return '\n\tNom : {}, Nombre de Parties Jouées: {} Score {}\n {}' \
            .format(self.__nom, self.__historique.getNombrePartieJouees(),
                    self.__historique.score(), self.__historique)

    def getNom(self):
        return self.__nom

    def setNom(self, nom):
        self.__nom = nom

    def miseAJourHistorique(self, mot, resultat):
        self.__historique.lireHistoriqueDansFichier(self.__nom)
        self.__historique.setPartieJouee(mot, resultat)
        self.__historique.getNombrePartieJouees()
        self.__historique.sauverHistoriqueDansFichier(self.__nom)

    def reinitialiserHistorique(self):
        self.__historique = Historique(self.__nom)
        self.__historique.sauverHistoriqueDansFichier(self.__nom)


class Historique:  # Déclaration de la classe Historique
    # Constructeur de la classe Historique
    def __init__(self, nomFichier):
        self.__mots = []
        self.__results = []

#       'a' open for writing, appending to the end of the file if it exists
#       '+' 	open a disk file for updating (reading and writing)
        file = open(nomFichier + ".txt", "a+")
        file.close()

    def getNombrePartieJouees(self):
        return len(self.__mots)

    def setPartieJouee(self, mot, resultat):
        self.__mots.append(mot)
        self.__results.append(resultat)

    def score(self):
        """Retourne la pourcentage de réussites par rapport aux parties jouées

        Parameters:
        Returns:
        float: retourne la pourcentage de réussites par rapport aux parties
        jouées ou 0 dans le cas aucune partie a été jouée.
        """
        if len(self.__results) == 0:
            return 0
        count = 0
        for i in range(0, len(self.__results)):
            if self.__results[i] == True:
                count += 1
        return count/len(self.__results)

    def lireHistoriqueDansFichier(self, nomFichier):
        """Lecture de l'historique du jouer stocké dans fichier de même nom

        Parameters:
            nomFichier (string): nom du Fichier avec le nom du jouer et
                l'extension .txt
        Returns:
            None
        """
        self.__mots = []
        self.__results = []
        with open(nomFichier + '.txt', 'r') as file:
            liste = file.read().splitlines()
#            print("Liste\n",liste)

            for item in liste:
                motListe, resultListe = item.split()
#                print(i, "item = [", item)
#                print("motListe : ", motListe)
#                print("resultListe : ", resultListe)
                if resultListe == "True":
                    self.setPartieJouee(motListe, True)
                else:
                    self.setPartieJouee(motListe, False)

    def sauverHistoriqueDansFichier(self, nomFichier):
        """Sauvagarde l'historique du jouer dans fichier de même nom

        Parameters:
            nomFichier (string): nom du Fichier avec le nom du jouer et
                l'extension .txt
        Returns:
            None
        """
        with open(nomFichier + '.txt', 'w') as file:
            for i in range(len(self.__mots)):
                if self.__results[i] == True:
                    file.write(str(self.__mots[i]) + "\t" + "True\n")
                if self.__results[i] == False:
                    file.write(str(self.__mots[i]) + "\t" + "False\n")

    def __str__(self):  # Opérateur d’affichage utilisé par print
        text = ""
        for i in range(len(self.__mots)):
#     print('i =', i, 'Mots = ',self.__mots[i], 'Results: ',self.__results[i] )
            if self.__results[i] == True:
                text += str(self.__mots[i]) + "\t" + "Succès\n"
            if self.__results[i] == False:
                text += str(self.__mots[i]) + "\t" + "Échec\n"

        return 'Historique \n Mot à trouver \t Succès/échec \n{}' \
            .format(str(text))