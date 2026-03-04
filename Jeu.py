
def check_coup(p, joueur, x, y, dx, dy):
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
    if p[x][y] != "":
        return []

    coups = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if check_coup(p, joueur, x, y, dx, dy):
                coups.append((x, y))
                return coups

    return []


def retournement(p,joueur,x,y):
    p[x][y]=joueur
    for i in range(-1,2):
        for j in range(-1,2):
            if check_coup(p,joueur,x,y,i,j):
                k=1
                while p[x+k*i][y+k*j]==("X" if joueur=="O" else "O"):
                    p[x+k*i][y+k*j]=joueur
                    k+=1