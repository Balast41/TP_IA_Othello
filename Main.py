import numpy as np
import time
import copy
import Ini_Aff
import Jeu
import StratClassique

def main():
    p = Ini_Aff.initialisation_plateau()
    joueur = "X"
    passes = 0

    while True:
        Ini_Aff.afficher_plateau(p)
        
        coup, memo_global = StratClassique.choisir_coup(p, joueur, profondeur=1) # Prend le meilleur coups

        if coup is None: # test si coups possibles
            print("Pas de coup pour", joueur)
            passes += 1 # Si pas de coups, le joueur passe son tour
            if passes == 2: # Max de 2 passes
                print("Fin de partie")
                print("Score :", StratClassique.h(p))
                break
        else:
            passes = 0
            Jeu.retournement(p, joueur, coup[0], coup[1]) # Joue le coup

        joueur = "O" if joueur == "X" else "X" # Changement de joueurs
        time.sleep(1)


if __name__ == "__main__":
    main()