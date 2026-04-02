
def check_coup(p, joueur, x, y, dx, dy):
    #Test une direction pour un coup
    if dx == 0 and dy == 0:
        return False
    adv = "O" if joueur == "X" else "X"
    i, j = x + dx, y + dy

    if not (0 <= i < 8 and 0 <= j < 8) or p[i][j] != adv:
        return False

    # Parcours ligne
    i += dx
    j += dy
    while 0 <= i < 8 and 0 <= j < 8:
        if p[i][j] == "":
            return False
        if p[i][j] == joueur:
            return True
        i += dx
        j += dy

    return False


def coup_jouable(p, x, y, joueur):
    #test si un coup est jouable en vérifiant si une direction est jouable
    if p[x][y] != "":
        return []

    jouable = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if check_coup(p, joueur, x, y, dx, dy):
                jouable=1
                return jouable

    return jouable

def liste_coups_jouables(p,joueur):
    liste=[]
    for x in range(0,8):
        for y in range(0,8):
            if p[x][y]=="" and coup_jouable(p,x,y,joueur):
                liste.append((x,y))
    return liste



def retournement(p,joueur,x,y):
    #Retourne les pions liés au coup joués
    p[x][y]=joueur
    for i in range(-1,2):
        for j in range(-1,2):
            if check_coup(p,joueur,x,y,i,j):
                k=1
                while p[x+k*i][y+k*j]==("X" if joueur=="O" else "O"):
                    p[x+k*i][y+k*j]=joueur
                    k+=1

def gagnant(p):
    #Retourne le gagnant de la partie
    score = 0
    for i in range(8):
        for j in range(8):
            if p[i][j]=="X":
                score+=1
            elif p[i][j]=="O":
                score-=1
    if score > 0:
        return "X"
    elif score < 0:
        return "O"
    else:
        return "Egalite"