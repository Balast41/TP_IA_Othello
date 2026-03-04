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
        Ini_Aff.afficher_plateau_V2(p)
        
        coup, memo_global = StratClassique.choisir_coup(p, joueur, profondeur=1)

        if coup is None:
            print("Pas de coup pour", joueur)
            passes += 1
            if passes == 2:
                print("Fin de partie")
                print("Score :", StratClassique.h(p))
                break
        else:
            passes = 0
            Jeu.retournement(p, joueur, coup[0], coup[1])

        joueur = "O" if joueur == "X" else "X"
        time.sleep(1)


if __name__ == "__main__":
    main()