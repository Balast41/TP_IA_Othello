def plateau_to_cle(p):
    return tuple(tuple(row) for row in p)


def afficher_plateau(p):
    #Affiche le plateau
    for l in p:
        print(" ".join([c if c!="" else "." for c in l]))
    print("\n")

def initialisation_plateau():
    #Initialise le plateau
    plateau=[["" for i in range(8)] for j in range(8)]
    plateau[3][3]="O"
    plateau[4][4]="O"
    plateau[3][4]="X"
    plateau[4][3]="X"
    return plateau
