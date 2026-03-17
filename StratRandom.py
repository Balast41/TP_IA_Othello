import random
import copy
import Jeu
import AIvsAI


def choisir_coup_random(p, joueur, profondeur=2, memo=None):
    if memo is None:
        memo = {}

    # Récupère la liste des coups jouables et en choisit un au hasard
    try:
        coups = Jeu.liste_coups_jouables(p, joueur)
    except Exception:
        coups = []

    if not coups:
        return None, memo
    
    if joueur == "X":
        AIvsAI.joueur="O"
    else:
        AIvsAI.joueur="X"

    return random.choice(coups), memo