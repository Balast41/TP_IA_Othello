import time

import numpy as np
import Jeu
import copy
import Jeu
import Ini_Aff

table_transposition={}

def h(p):
    coins = [(0,0),(0,7),(7,0),(7,7)]
    score_mobilite_X=len(Jeu.liste_coups_jouables(p,"X")) # Nombre de coups jouables pour X
    score_mobilite_O=len(Jeu.liste_coups_jouables(p,"O")) # Nombre de coups jouables pour O
    score_mobilite= score_mobilite_X - score_mobilite_O

    # Gestion des coins
    score_coins = 0
    for x, y in coins:
        if p[x][y] == "X":
            score_coins += 25  # Bonus si coin pour X
        elif p[x][y] == "O":
            score_coins -= 25  # Malus si coin pour O
    
    # Score final = mobilité + valeur des coins
    score = score_mobilite + score_coins
    return score

def minimax_alpha_beta(p, profondeur, joueur, alpha=-np.inf, beta=np.inf):
    
    if profondeur == 0:
        score = h(p)
        return score 
    
    coups_trouves = False
    
    if joueur == "X":
        best= -np.inf
        for x in range(8):
            for y in range(8):
                if p[x][y] == "" and Jeu.coup_jouable(p,x,y, "X"): # test si la case est vide et le coup jouable
                    coups_trouves = True
                    pcopie = copy.deepcopy(p) # Copie du plateau
                    Jeu.retournement(pcopie, "X",x,y) # Simulation du coup
                    best = max(best, minimax_alpha_beta(pcopie, profondeur-1, "O",alpha,beta)) # Calcul du meilleur score pour ce coup
                    alpha = max(alpha, best) # Calcul du alpha pour un éventuel élagage
                    if beta <= alpha: # Coupure alpha
                        break
            if beta <= alpha: #Coupure alpha
                break
        score= best if coups_trouves else h(p)
    else:
        best= np.inf
        for x in range(8):
            for y in range(8):
                if p[x][y] == "" and Jeu.coup_jouable(p,x,y, "O"): # test si la case est vide et le coup jouable
                    coups_trouves = True
                    pcopie = copy.deepcopy(p) # Copie du plateau
                    Jeu.retournement(pcopie, "O",x,y) # Simulation du coup
                    best = min(best, minimax_alpha_beta(pcopie, profondeur-1, "X",alpha,beta))
                    alpha = min(alpha, best)
                    if beta <= alpha: #Coupure beta
                        break
            if beta <= alpha: #Coupure beta
                break
        score= best if coups_trouves else h(p)
    
    return score


def choisir_coup_memo(p, joueur, profondeur=2):
    meilleur_score = -np.inf if joueur == "X" else np.inf
    meilleur_coup = None
    for x in range(8):
        for y in range(8): #Parcours du plateau pour trouver le meilleur coup
            if p[x][y] == "" and Jeu.coup_jouable(p, x, y, joueur): # Test du coup
                pcopie = copy.deepcopy(p)
                Jeu.retournement(pcopie, joueur, x, y) # Simulation du coup

                score = minimax_alpha_beta(pcopie,profondeur-1,"O" if joueur == "X" else "X") # Calcul du Score

                if joueur == "X":
                    if score > meilleur_score: # Maximiser le score
                        meilleur_score = score
                        meilleur_coup = (x, y)
                else:
                    if score < meilleur_score: # Minimiser le score
                        meilleur_score = score
                        meilleur_coup = (x, y)

    return meilleur_coup

def partie():
    p = Ini_Aff.initialisation_plateau()
    joueur = "X"
    passes = 0
    while True:
        Ini_Aff.afficher_plateau(p)
        
        tic= time.time()
        coup = choisir_coup_memo(p, joueur, profondeur=1) # Joue le meilleur coup
        tac = time.time() - tic

        print("Temps de calcul : ", tac," s")

        if coup is None: # Test si coups possibles
            print("Pas de coup pour", joueur)
            passes += 1 # Si pas de coup, le joueur passe son tour
            if passes == 2: # limite de 2 passes
                print("Fin de partie")
                print("Score heuristique :", h(p))
                print("Gagnant :", Jeu.gagnant(p))
                break
        else:
            passes = 0
            Jeu.retournement(p, joueur, coup[0], coup[1]) # Joue le coup

        joueur = "O" if joueur == "X" else "X" # Changement de joueur
        time.sleep(1)
    return 0