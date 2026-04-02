import time
import Ini_Aff
import numpy as np
import Jeu
import copy
import Jeu

table_transposition={}

TableComparaisonA = [
    [ 500,-150,  30,  10,  10,  30,-150, 500],
    [-150,-250,   0,   0,   0,   0,-250,-150],
    [  30,   0,   1,   2,   2,   1,   0,  30],
    [  10,   0,   2,  16,  16,   2,   0,  10],
    [  10,   0,   2,  16,  16,   2,   0,  10],
    [  30,   0,   1,   2,   2,   1,   0,  30],
    [-150,-250,   0,   0,   0,   0,-250,-150],
    [ 500,-150,  30,  10,  10,  30,-150, 500]
    ]

TableComparaisonB = [
    [100, -20,  10,   5,   5,  10, -20, 100],
    [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
    [ 10,  -2,  -1,  -1,  -1,  -1,  -2,  10],
    [  5,  -2,  -1,  -1,  -1,  -1,  -2,  -5],
    [  5,  -2,  -1,  -1,  -1,  -1,  -2,  -5],
    [ 10,  -2,  -1,  -1,  -1,  -1,  -2,  10],
    [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
    [100, -20,  10,   5,   5,  10, -20, 100]
    ]

def h(p):
   score=0
   for x in range(8):
        for y in range(8):
            if p[x][y]=="X":
                score+=TableComparaisonA[x][y] # Ajout du score de la case pour X
            elif p[x][y]=="O":
                score-=TableComparaisonA[x][y] # Soustraction du score de la case pour O
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
                    beta = min(beta, best)
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





