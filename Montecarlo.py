import random
import Jeu

def PartieRandom(Plateau,J1):
    # Initialisation des variables
    P = [ligne[:] for ligne in Plateau]
    J2 = "O" if J1 == "X" else "X"
    joueur=J1
    
    while True :
        # s'il y a des coups jouables, on joue un coup aléatoire parmi les coups jouables
        allCoupJouable=Jeu.liste_coups_jouables(P,joueur)
        if allCoupJouable :
            (i,j) = allCoupJouable[random.randint(0, len(allCoupJouable)-1)]
            Jeu.retournement(P,joueur,i,j)
            joueur = J1 if joueur == J2 else J2 # on change le joueur
        else :
            break
    
    # True si J1 a gagné, false sinon
    if sum(ligne.count(J1) for ligne in P) > sum(ligne.count(J2) for ligne in P) :
        return True
    else :
        return False



def MonteCarlo(Plateau,J1,N):
    # Initialisation des variables
    allCoupJouable=Jeu.liste_coups_jouables(Plateau,J1)
    if allCoupJouable :
        max = -1
        maxPoint = allCoupJouable[0]
        listeNombreVictoire = []
        
        # On parcourt tous les coups jouables par J1
        for a in allCoupJouable :
            nombreVictoire=0
            
            # On teste N partie aléatoires pour compter le nombre de Victoire
            for k in range(N):
                if PartieRandom(Plateau,J1) :
                    nombreVictoire += 1
            listeNombreVictoire.append(nombreVictoire)

            # On choisit le coup jouable avec le plus grand nombre de victoire
            if nombreVictoire>max :
                max = nombreVictoire
                maxPoint = a
        

        return (maxPoint)