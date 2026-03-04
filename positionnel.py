#imports ------------------------------------------------------------------------------------------------------------------------
import Jeu



# Tables de valeur ------------------------------------------------------------------------------------------------------------------------
TableComparaisonA = [
    [ 500,-150,  30,  10,  10,  30,-150, 500],
    [-150,-250,   0,   0,   0,   0,-250,-150],
    [  30,   0,   1,   2,   2,   1,   0,  30],
    [  10,   0,   2,  16,  16,   2,   0,  10],
    [  10,   0,   2,  16,  16,   2,   0,  10],
    [  30,   0,   1,   2,   2,   1,   0,  30],
    [-150,-250,   0,   0,   0,   0,-250,-150],
    [ 500,-150,  30,  10,  10,  30,-150, 500]
    ]

TableComparaisonB = [
    [100, -20,  10,   5,   5,  10, -20, 100],
    [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
    [ 10,  -2,  -1,  -1,  -1,  -1,  -2,  10],
    [  5,  -2,  -1,  -1,  -1,  -1,  -2,  -5],
    [  5,  -2,  -1,  -1,  -1,  -1,  -2,  -5],
    [ 10,  -2,  -1,  -1,  -1,  -1,  -2,  10],
    [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
    [100, -20,  10,   5,   5,  10, -20, 100]
    ]

# On récupère [(valeur, i, j),(valeur, i, j)...] trié par valeur décroissante
elements = [
    (TableComparaisonA[i][j], i, j)
    for i in range(8)
    for j in range(8)
]
elements_sorted = sorted(elements, key=lambda x: x[0], reverse=True)



#fonctions ------------------------------------------------------------------------------------------------------------------------
def CoupPositionnel_0(Plateau, Joueur):
    '''Renvoit le score du meilleur coup positionnel pour le Joueur avec une profondeur de 1/2'''
    for e in range(64):
        J=Jeu.coup_jouable(Plateau, elements[e][1],elements[e][2],Joueur)
        if J :
            print(f"Case de valeur{elements[e][0]}")
            return (elements[e][0])
