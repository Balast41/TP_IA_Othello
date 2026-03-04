import numpy as np
import Jeu
import copy

def h(p):
    score = 0
    for i in range(8):
        for j in range(8):
            if p[i][j]=="X":
                score+=1
            elif p[i][j]=="O":
                score-=1

    return score

 
def minimax(p, profondeur, joueur):
    if profondeur == 0:
        return h(p)

    coups_trouves = False

    if joueur == "X":  # maximise
        best = -np.inf
        for x in range(8):
            for y in range(8):
                if p[x][y] == "" and Jeu.coup_jouable(p, x, y, "X"):
                    coups_trouves = True
                    pcopie = copy.deepcopy(p)
                    Jeu.retournement(pcopie, "X", x, y)
                    best = max(best, minimax(pcopie, profondeur-1, "O"))
        return best if coups_trouves else h(p)

    else:  # minimise
        best = np.inf
        for x in range(8):
            for y in range(8):
                if p[x][y] == "" and Jeu.coup_jouable(p, x, y, "O"):
                    coups_trouves = True
                    pcopie = copy.deepcopy(p)
                    Jeu.retournement(pcopie, "O", x, y)
                    best = min(best, minimax(pcopie, profondeur-1, "X"))
        return best if coups_trouves else h(p)
    
def choisir_coup(p, joueur, profondeur=2):
    meilleur_score = -np.inf if joueur == "X" else np.inf
    meilleur_coup = None
    for x in range(8):
        for y in range(8):
            if p[x][y] == "" and Jeu.coup_jouable(p, x, y, joueur):
                pcopie = copy.deepcopy(p)
                Jeu.retournement(pcopie, joueur, x, y)

                score = minimax(pcopie,profondeur-1,"O" if joueur == "X" else "X")

                if joueur == "X":
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (x, y)
                else:
                    if score < meilleur_score:
                        meilleur_score = score
                        meilleur_coup = (x, y)

    return meilleur_coup