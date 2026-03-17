import time

import numpy as np
import Jeu
import copy
import Ini_Aff

table_transposition={}

def h(p):
    # Calcul du score du score en fonction de la différence de pions noirs et blancs
    # Stratégie Absolue
    score = 0
    for i in range(8):
        for j in range(8):
            if p[i][j]=="X":
                score+=1
            elif p[i][j]=="O":
                score-=1

    return score

def plateau_to_cle(p):
    return tuple(tuple(row) for row in p)

def minimax_alpha_beta(p, profondeur, joueur, alpha=-np.inf, beta=np.inf, memo=None):
    if memo is None:
        memo={} # Création du dictionnaire de mémoisation

    cle = (plateau_to_cle(p), joueur, profondeur)
    if cle in memo: # recherche si le score du coup a déjà été calculé
        return memo[cle]
    
    if profondeur == 0:
        score = h(p)
        memo[cle] = score
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
                    best = max(best, minimax_alpha_beta(pcopie, profondeur-1, "O",alpha,beta,memo)) # Calcul du meilleur score pour ce coup
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
                    best = min(best, minimax_alpha_beta(pcopie, profondeur-1, "X",alpha,beta,memo))
                    alpha = min(alpha, best)
                    if beta <= alpha: #Coupure beta
                        break
            if beta <= alpha: #Coupure beta
                break
        score= best if coups_trouves else h(p)
    
    memo[cle]=score
    return score


def choisir_coup_memo(p, joueur, profondeur=2,memo=None):
    
    if memo is None:
        memo={}

    meilleur_score = -np.inf if joueur == "X" else np.inf
    meilleur_coup = None
    for x in range(8):
        for y in range(8): #Parcours du plateau pour trouver le meilleur coup
            if p[x][y] == "" and Jeu.coup_jouable(p, x, y, joueur): # Test du coup
                pcopie = copy.deepcopy(p)
                Jeu.retournement(pcopie, joueur, x, y) # Simulation du coup

                score = minimax_alpha_beta(pcopie,profondeur-1,"O" if joueur == "X" else "X",memo=memo) # Calcul du Score

                if joueur == "X":
                    if score > meilleur_score: # Maximiser le score
                        meilleur_score = score
                        meilleur_coup = (x, y)
                else:
                    if score < meilleur_score: # Minimiser le score
                        meilleur_score = score
                        meilleur_coup = (x, y)

    return meilleur_coup, memo # revoie le coup à jouer et le dictionnaire de mémoisation


def partie():
    p = Ini_Aff.initialisation_plateau()
    joueur = "X"
    passes = 0
    memo_global = {}

    while True:
        Ini_Aff.afficher_plateau(p)
        
        tic= time.time()
        coup, memo_global = choisir_coup_memo(p, joueur, profondeur=1,memo=memo_global) # Joue le meilleur coup
        tac = time.time() - tic

        print("Temps de calcul : ", tac," s | taille du cache : ", len(memo_global))

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