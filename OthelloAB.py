

import numpy as np
import time
import copy

table_transposition={}

def plateau_to_cle(p):
    return tuple(tuple(row) for row in p)


def afficher_plateau(p):
    for l in p:
        print(" ".join([c if c!="" else "." for c in l]))
    print("\n")

def initialisation_plateau():
    plateau=[["" for i in range(8)] for j in range(8)]
    plateau[3][3]="O"
    plateau[4][4]="O"
    plateau[3][4]="X"
    plateau[4][3]="X"
    return plateau

print(initialisation_plateau())


def check_coup(p, joueur, x, y, dx, dy):
    if dx == 0 and dy == 0:
        return False

    adv = "O" if joueur == "X" else "X"
    i, j = x + dx, y + dy

    if not (0 <= i < 8 and 0 <= j < 8) or p[i][j] != adv:
        return False

    # Parcours ligne
    i += dx
    j += dy
    while 0 <= i < 8 and 0 <= j < 8:
        if p[i][j] == "":
            return False
        if p[i][j] == joueur:
            return True
        i += dx
        j += dy

    return False


def coup_jouable(p, x, y, joueur):
    if p[x][y] != "":
        return []

    coups = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if check_coup(p, joueur, x, y, dx, dy):
                coups.append((x, y))
                return coups

    return []


def retournement(p,joueur,x,y):
    p[x][y]=joueur
    for i in range(-1,2):
        for j in range(-1,2):
            if check_coup(p,joueur,x,y,i,j):
                k=1
                while p[x+k*i][y+k*j]==("X" if joueur=="O" else "O"):
                    p[x+k*i][y+k*j]=joueur
                    k+=1



def h(p):
    score = 0
    for i in range(8):
        for j in range(8):
            if p[i][j]=="X":
                score+=1
            elif p[i][j]=="O":
                score-=1

    return score

    

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
                if p[x][y] == "" and coup_jouable(p,x,y, "X"):
                    coups_trouves = True
                    pcopie = copy.deepcopy(p)
                    retournement(pcopie, "X",x,y)
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
                if p[x][y] == "" and coup_jouable(p,x,y, "O"):
                    coups_trouves = True
                    pcopie = copy.deepcopy(p)
                    retournement(pcopie, "O",x,y)
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
            if p[x][y] == "" and coup_jouable(p, x, y, joueur):
                pcopie = copy.deepcopy(p)
                retournement(pcopie, joueur, x, y)

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
    
def main():
    p = initialisation_plateau()
    joueur = "X"
    passes = 0
    memo_global = {}

    while True:
        afficher_plateau(p)
        
        tic= time.time()
        coup, memo_global = choisir_coup_memo(p, joueur, profondeur=1,memo=memo_global)
        tac = time.time() - tic

        print("Temps de calcul : ", tac," s | taille du cache : ", len(memo_global))

        if coup is None:
            print("Pas de coup pour", joueur)
            passes += 1
            if passes == 2:
                print("Fin de partie")
                print("Score :", h(p))
                break
        else:
            passes = 0
            retournement(p, joueur, coup[0], coup[1])

        joueur = "O" if joueur == "X" else "X"
        time.sleep(1)


if __name__ == "__main__":
    main()
