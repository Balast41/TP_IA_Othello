import time
import Ini_Aff
import numpy as np
import Jeu
import copy
import Jeu
import StratPoids
import StratMobilite
import StratMemoAB

table_transposition={}

def avancee_partie(p):
    coups_restants = 0
    for x in range(8):
        for y in range(8):
            if p[x][y]=="":
                coups_restants += 1

    return coups_restants



def partie():
    p = Ini_Aff.initialisation_plateau()
    joueur = "X"
    passes = 0

    while True:
        Ini_Aff.afficher_plateau(p)
        avancee = avancee_partie(p)
        tic= time.time()
        if avancee > 40:
            coup = StratPoids.choisir_coup_memo(p, joueur, profondeur=1) # Joue le meilleur coup
        elif avancee > 20 and avancee <= 40:
            coup = StratMobilite.choisir_coup_memo(p, joueur, profondeur=1) # Joue le meilleur coup
        else:
            coup = StratMemoAB.choisir_coup_memo(p, joueur, profondeur=1) # Joue le meilleur coup
        tac = time.time() - tic

        print("Temps de calcul : ", tac," s")
        if coup is None: # Test si coups possibles
            print("Pas de coup pour", joueur)
            passes += 1 # Si pas de coup, le joueur passe son tour
            if passes == 2: # limite de 2 passes
                print("Fin de partie")
                print("Gagnant :", Jeu.gagnant(p))
                break
        else:
            passes = 0
            Jeu.retournement(p, joueur, coup[0], coup[1]) # Joue le coup

        joueur = "O" if joueur == "X" else "X" # Changement de joueur
        time.sleep(1)
    return 0