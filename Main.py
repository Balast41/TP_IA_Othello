import numpy as np
import time
import copy
import Ini_Aff
import Jeu
import StratClassique
import StratMixte
import StratPoids
import StratMobilite
import StratMemoAB
import AIvsAI

def main():
    AIvsAI.partie("montecarlo","mixte",profondeur1=1,profondeur2=6,simu=100) # Lancement de la partie entre une IA mixte et une IA random



if __name__ == "__main__":
    main()