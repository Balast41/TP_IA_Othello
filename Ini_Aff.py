def plateau_to_cle(p):
    return tuple(tuple(row) for row in p)


def afficher_plateau(p):
    for l in p:
        print(" ".join([c if c!="" else "." for c in l]))
    print("\n")

def afficher_plateau_V2(Plateau):
    print("  0 1 2 3 4 5 6 7")
    for i in range(8):
        print(i, end="")
        for j in range(8):
            if Plateau[i][j] == "O":
                print('⚪', end="")
            elif Plateau[i][j] == "X":
                print('⚫', end="")
            else :
                print('🟫', end="")
        print("")

def initialisation_plateau():
    plateau=[["" for i in range(8)] for j in range(8)]
    plateau[3][3]="O"
    plateau[4][4]="O"
    plateau[3][4]="X"
    plateau[4][3]="X"
    return plateau
