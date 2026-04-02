import time
import Ini_Aff
import numpy as np
import Jeu
import copy
import Montecarlo
import StratPoids
import StratMobilite
import StratMemoAB
import StratMixte
from StratRandom import choisir_coup_random
import StratClassique





def minimax_alpha_beta_X(p, profondeur, joueur, alpha=-np.inf, beta=np.inf, h1=None, h2=None):
    if profondeur == 0:
        hfunc = h1 if joueur == "X" else h2
        if not callable(hfunc):
            hfunc = StratClassique.h
        score = hfunc(p)
        return score 
    
    coups_trouves = False
    
    best= -np.inf
    for x in range(8):
        for y in range(8):
            if p[x][y] == "" and Jeu.coup_jouable(p,x,y, "X"): # test si la case est vide et le coup jouable
                coups_trouves = True
                pcopie = copy.deepcopy(p) # Copie du plateau
                Jeu.retournement(pcopie, "X",x,y) # Simulation du coup
                best = max(best, minimax_alpha_beta_O(pcopie, profondeur-1, "O", alpha, beta, h1=h1, h2=h2)) # Calcul du meilleur score pour ce coup
                alpha = max(alpha, best) # Calcul du alpha pour un éventuel élagage
                if beta <= alpha: # Coupure alpha
                    break
        if beta <= alpha: #Coupure alpha
            break
    if coups_trouves:
        score = best
    else:
        hfunc = h1 if joueur == "X" else h2
        if not callable(hfunc):
            hfunc = StratClassique.h
        score = hfunc(p)
    
    return score

def minimax_alpha_beta_O(p, profondeur, joueur, alpha=-np.inf, beta=np.inf, h1=None, h2=None):
    if profondeur == 0:
        hfunc = h1 if joueur == "X" else h2
        if not callable(hfunc):
            hfunc = StratClassique.h
        score = hfunc(p)
        return score 
    
    coups_trouves = False

    best= np.inf
    for x in range(8):
        for y in range(8):
            if p[x][y] == "" and Jeu.coup_jouable(p,x,y, "O"): # test si la case est vide et le coup jouable
                coups_trouves = True
                pcopie = copy.deepcopy(p) # Copie du plateau
                Jeu.retournement(pcopie, "O",x,y) # Simulation du coup
                best = min(best, minimax_alpha_beta_X(pcopie, profondeur-1, "X", alpha, beta, h1=h1, h2=h2))
                beta = min(beta, best)
                if beta <= alpha: #Coupure beta
                    break
        if beta <= alpha: #Coupure beta
            break
    if coups_trouves:
        score = best
    else:
        hfunc = h1 if joueur == "X" else h2
        if not callable(hfunc):
            hfunc = StratClassique.h
        score = hfunc(p)
    
    return score

def choisir_coup_memo(p, joueur, profondeur1, profondeur2, h1=None, h2=None, strategie1=None, strategie2=None, simu=None):

    if joueur == "X" or (joueur == "O" and strategie2 == "montecarlo"):
        meilleur_score = -np.inf
    else:
        meilleur_score = np.inf
    meilleur_coup = None
    for x in range(8):
        for y in range(8): #Parcours du plateau pour trouver le meilleur coup
            if p[x][y] == "" and Jeu.coup_jouable(p, x, y, joueur): # Test du coup
                pcopie = copy.deepcopy(p)
                Jeu.retournement(pcopie, joueur, x, y) # Simulation du coup
                if joueur == "X":
                    if strategie1=="absolu AB" or strategie1=="absolue AB" or strategie1=="mixte AB" or strategie1=="poids AB" or strategie1=="mobilite AB":
                        score = minimax_alpha_beta_X(pcopie, profondeur1-1, "X", h1=h1, h2=h2) # Calcul du Score
                    elif strategie1=="montecarlo":
                        score = Montecarlo.MonteCarlo(pcopie, "X", simu) # Calcul du Score
                    else:
                        score = minimax_X(pcopie, profondeur1-1, "X", h1=h1, h2=h2) # Calcul du Score
                else:
                    if strategie2=="absolu AB" or strategie2=="absolue AB" or strategie2=="mixte AB" or strategie2=="poids AB" or strategie2=="mobilite AB":
                        score = minimax_alpha_beta_O(pcopie, profondeur2-1, "O", h1=h1, h2=h2) # Calcul du Score
                    elif strategie2=="montecarlo":
                        score = Montecarlo.MonteCarlo(pcopie, "O", simu) # Calcul du Score
                    else:
                        score = minimax_O(pcopie, profondeur2-1, "O", h1=h1, h2=h2) # Calcul du Score


                if joueur == "X":
                    if score > meilleur_score: # Maximiser le score
                        meilleur_score = score
                        meilleur_coup = (x, y)
                else:
                    if strategie2 == "montecarlo":
                        if score > meilleur_score: # Monte Carlo retourne des victoires de O, on maximise
                            meilleur_score = score
                            meilleur_coup = (x, y)
                    elif score < meilleur_score: # Minimiser le score
                        meilleur_score = score
                        meilleur_coup = (x, y)

    return meilleur_coup # revoie le coup à jouer

def minimax_X(p, profondeur, joueur, alpha=-np.inf, beta=np.inf, h1=None, h2=None):
    if profondeur == 0:
        hfunc = h1 if joueur == "X" else h2
        if not callable(hfunc):
            hfunc = StratClassique.h
        score = hfunc(p)
        return score 
    
    coups_trouves = False
    
    best= -np.inf
    for x in range(8):
        for y in range(8):
            if p[x][y] == "" and Jeu.coup_jouable(p,x,y, "X"): # test si la case est vide et le coup jouable
                coups_trouves = True
                pcopie = copy.deepcopy(p) # Copie du plateau
                Jeu.retournement(pcopie, "X",x,y) # Simulation du coup
                best = max(best, minimax_O(pcopie, profondeur-1, "O", h1=h1, h2=h2)) # Calcul du meilleur score pour ce coup
    if coups_trouves:
        score = best
    else:
        hfunc = h1 if joueur == "X" else h2
        if not callable(hfunc):
            hfunc = StratClassique.h
        score = hfunc(p)
    
    return score

def minimax_O(p, profondeur, joueur, alpha=-np.inf, beta=np.inf, h1=None, h2=None):
    if profondeur == 0:
        hfunc = h1 if joueur == "X" else h2
        if not callable(hfunc):
            hfunc = StratClassique.h
        score = hfunc(p)
        return score 
    
    coups_trouves = False

    best= np.inf
    for x in range(8):
        for y in range(8):
            if p[x][y] == "" and Jeu.coup_jouable(p,x,y, "O"): # test si la case est vide et le coup jouable
                coups_trouves = True
                pcopie = copy.deepcopy(p) # Copie du plateau
                Jeu.retournement(pcopie, "O",x,y) # Simulation du coup
                best = min(best, minimax_X(pcopie, profondeur-1, "X", h1=h1, h2=h2))

    if coups_trouves:
        score = best
    else:
        hfunc = h1 if joueur == "X" else h2
        if not callable(hfunc):
            hfunc = StratClassique.h
        score = hfunc(p)
    
    return score






def partie(strategie1,strategie2,profondeur1,profondeur2,simu):
    p = Ini_Aff.initialisation_plateau()
    joueur = "X"
    passes = 0

    # Assigner la fonction heuristique (ne pas appeler la fonction ici)
    match strategie1:
        case "poids" | "poids AB":
            h1 = StratPoids.h
        case "mobilite" | "mobilite AB":
            h1 = StratMobilite.h
        case "mixte" | "mixte AB":
            # StratMixte n'a pas de h définie; utiliser une heuristique par défaut
            h1 = StratPoids.h
        case "absolu" | "absolue" | "absolu AB" | "absolue AB":
            h1 = StratMemoAB.h
        case "random":
            h1 = None
        case "montecarlo":
            h1 = None

    match strategie2:
        case "poids" | "poids AB":
            h2 = StratPoids.h
        case "mobilite" | "mobilite AB":
            h2 = StratMobilite.h
        case "mixte" | "mixte AB":
            h2 = StratPoids.h
        case "absolu" | "absolue" | "absolu AB" | "absolue AB":
            h2 = StratMemoAB.h
        case "random":
            h2 = None
        case "montecarlo":
            h2 = None

    while True:
        # Affiche quel joueur utilise quelle stratégie
        print(f"Stratégies — X: {strategie1} | O: {strategie2}")
        Ini_Aff.afficher_plateau(p)
        if strategie1 == "mixte" or strategie1 == "mixte AB":
            if StratMixte.avancee_partie(p) > 40:
                h1 = StratPoids.h
            elif StratMixte.avancee_partie(p) > 20 and StratMixte.avancee_partie(p) <= 40:
                h1 = StratMobilite.h
            else:
                h1 = StratMemoAB.h
        if strategie2 == "mixte" or strategie2 == "mixte AB":
            if StratMixte.avancee_partie(p) > 40:
                h2 = StratPoids.h
            elif StratMixte.avancee_partie(p) > 20 and StratMixte.avancee_partie(p) <= 40:
                h2 = StratMobilite.h
            else:
                h2 = StratMemoAB.h

        tic = time.time()
        # Choix du coup selon le joueur courant
        if joueur == "X":
            if strategie1 == "random":
                coup = choisir_coup_random(p, "X", profondeur1)
            else:
                coup = choisir_coup_memo(p, "X", profondeur1, profondeur2, h1=h1, h2=h2, strategie1=strategie1, strategie2=strategie2, simu=simu)
        else:  # joueur == "O"
            if strategie2 == "random":
                coup = choisir_coup_random(p, "O", profondeur2)
            else:
                coup = choisir_coup_memo(p, "O", profondeur1, profondeur2, h1=h1, h2=h2, strategie1=strategie1, strategie2=strategie2, simu=simu)

        tac = time.time() - tic

        print("Temps de calcul : ", tac," s")
        print(coup)
        if coup is None: # Test si coups possibles
            print("Pas de coup pour", joueur)
            passes += 1 # Si pas de coup, le joueur passe son tour
            if passes == 2: # limite de 2 passes
                print("Fin de partie")
                if strategie1 != "random" and strategie1 != "montecarlo" and callable(h1):
                    print("Score heuristique AI1 :", h1(p))
                if strategie2 != "random" and strategie2 != "montecarlo" and callable(h2):
                    print("Score heuristique AI2 :", h2(p))
                print("Gagnant :", Jeu.gagnant(p))
                break
        else:
            passes = 0
            Jeu.retournement(p, joueur, coup[0], coup[1]) # Joue le coup

        joueur = "O" if joueur == "X" else "X" # Changement de joueur
        time.sleep(1)
    return 0
