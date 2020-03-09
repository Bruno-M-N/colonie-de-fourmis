# -*- coding: utf-8 -*-
"""
test_jouer.py
"""

from jouer import *  # import de les classes à partir du fichier jouer.py
# from pendu_interface import *


text = "Test class jouer\n"
print(text)

# Creation d'un Jouer
Jouer1 = Jouer('Jouer1 ECL')
print(Jouer1)

Jouer1.miseAJourHistorique("ANGLE", True)
Jouer1.miseAJourHistorique("BANC", False)
Jouer1.miseAJourHistorique("COIN", False)
print(Jouer1)

Jouer1.reinitialiserHistorique()

Jouer1.miseAJourHistorique("CHAISE", True)
Jouer1.miseAJourHistorique("SERRURE", False)
Jouer1.miseAJourHistorique("PLIAGE", True)
Jouer1.miseAJourHistorique("PLIAGE", True)
print(Jouer1)
