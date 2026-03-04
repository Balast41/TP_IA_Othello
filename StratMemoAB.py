import numpy as np
import Jeu
import copy

table_transposition={}

def h(p):
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
        memo={}

    cle = (plateau_to_cle(p), joueur, profondeur)
    if cle in memo:
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
                if p[x][y] == "" and Jeu.coup_jouable(p,x,y, "X"):
                    coups_trouves = True
                    pcopie = copy.deepcopy(p)
                    Jeu.retournement(pcopie, "X",x,y)
                    best = max(best, minimax_alpha_beta(pcopie, profondeur-1, "O",alpha,beta,memo))
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
            if beta <= alpha:
                break
        score= best if coups_trouves else h(p)
    else:
        best= np.inf
        for x in range(8):
            for y in range(8):
                if p[x][y] == "" and Jeu.coup_jouable(p,x,y, "O"):
                    coups_trouves = True
                    pcopie = copy.deepcopy(p)
                    Jeu.retournement(pcopie, "O",x,y)
                    best = min(best, minimax_alpha_beta(pcopie, profondeur-1, "X",alpha,beta,memo))
                    alpha = min(alpha, best)
                    if beta <= alpha:
                        break
            if beta <= alpha:
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
        for y in range(8):
            if p[x][y] == "" and Jeu.coup_jouable(p, x, y, joueur):
                pcopie = copy.deepcopy(p)
                Jeu.retournement(pcopie, joueur, x, y)

                score = minimax_alpha_beta(pcopie,profondeur-1,"O" if joueur == "X" else "X",memo=memo)

                if joueur == "X":
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (x, y)
                else:
                    if score < meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (x, y)

    return meilleur_coup, memo