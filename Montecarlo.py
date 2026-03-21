import random
import Jeu

def PartieRandom(Plateau, J1, joueur_depart):
    # Simule une partie complète en appliquant la règle des passes.
    P = [ligne[:] for ligne in Plateau]
    J2 = "O" if J1 == "X" else "X"
    joueur = joueur_depart
    passes = 0

    while passes < 2:
        allCoupJouable = Jeu.liste_coups_jouables(P, joueur)
        if allCoupJouable:
            (i, j) = allCoupJouable[random.randint(0, len(allCoupJouable) - 1)]
            Jeu.retournement(P, joueur, i, j)
            passes = 0
        else:
            passes += 1

        joueur = J2 if joueur == J1 else J1

    # True si J1 a gagné, false sinon
    return sum(ligne.count(J1) for ligne in P) > sum(ligne.count(J2) for ligne in P)



def MonteCarlo(Plateau, J1, N):
    # Le plateau reçu est déjà le résultat du coup candidat de J1.
    # Le prochain joueur à jouer est donc l'adversaire.
    J2 = "O" if J1 == "X" else "X"

    nombreVictoires = 0
    for _ in range(N):
        if PartieRandom(Plateau, J1, J2):
            nombreVictoires += 1

    return nombreVictoires