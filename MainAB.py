import numpy as np
import time
import copy
import Ini_Aff
import Jeu
import StratMemoAB

def main():
    p = Ini_Aff.initialisation_plateau()
    joueur = "X"
    passes = 0
    memo_global = {}

    while True:
        Ini_Aff.afficher_plateau(p)
        
        tic= time.time()
        coup, memo_global = StratMemoAB.choisir_coup_memo(p, joueur, profondeur=1,memo=memo_global)
        tac = time.time() - tic

        print("Temps de calcul : ", tac," s | taille du cache : ", len(memo_global))

        if coup is None:
            print("Pas de coup pour", joueur)
            passes += 1
            if passes == 2:
                print("Fin de partie")
                print("Score :", StratMemoAB.h(p))
                break
        else:
            passes = 0
            Jeu.retournement(p, joueur, coup[0], coup[1])

        joueur = "O" if joueur == "X" else "X"
        time.sleep(1)


if __name__ == "__main__":
    main()
