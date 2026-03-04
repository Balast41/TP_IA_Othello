import numpy as np
import time
import copy
import Ini_Aff
import Jeu
import StratMobilite

def main():
    p = Ini_Aff.initialisation_plateau()
    joueur = "X"
    passes = 0
    memo_global = {}

    while True:
        Ini_Aff.afficher_plateau(p)
        
        tic= time.time()
        coup, memo_global = StratMobilite.choisir_coup_memo(p, joueur, profondeur=1,memo=memo_global) # Joue le meilleur coup
        tac = time.time() - tic

        print("Temps de calcul : ", tac," s | taille du cache : ", len(memo_global))

        if coup is None: # Test si coups possibles
            print("Pas de coup pour", joueur)
            passes += 1 # Si pas de coup, le joueur passe son tour
            if passes == 2: # limite de 2 passes
                print("Fin de partie")
                print("Score :", StratMobilite.h(p))
                break
        else:
            passes = 0
            Jeu.retournement(p, joueur, coup[0], coup[1]) # Joue le coup

        joueur = "O" if joueur == "X" else "X" # Changement de joueur
        time.sleep(1)


if __name__ == "__main__":
    main()
