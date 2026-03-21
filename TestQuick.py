import AIvsAI
import Jeu
import Ini_Aff
from datetime import datetime

# Listes des stratégies à tester (version réduite pour test rapide)
STRATEGIES = ["random", "montecarlo", "poids"]

# Paramètres de test
NUM_GAMES_PER_MATCHUP = 1  # RÉDUIT POUR TESTER
PROFONDEUR = 1  # RÉDUIT POUR TESTER
SIMU_MONTECARLO = 10  # TRÈS RÉDUIT POUR TEST (10 simulations)

# Dictionaries pour stocker les résultats
results = {}
logs = []

def run_single_game(s1, s2):
    """Lance une seule partie et retourne le gagnant"""
    p = Ini_Aff.initialisation_plateau()
    joueur = "X"
    passes = 0
    move_count = 0
    
    # Récupérer les heuristiques appropriées
    h1 = None
    h2 = None
    
    if s1 == "poids":
        import StratPoids
        h1 = StratPoids.h
    elif s1 == "mobilite":
        import StratMobilite
        h1 = StratMobilite.h
    elif s1 == "absolu":
        import StratMemoAB
        h1 = StratMemoAB.h
    
    if s2 == "poids":
        import StratPoids
        h2 = StratPoids.h
    elif s2 == "mobilite":
        import StratMobilite
        h2 = StratMobilite.h
    elif s2 == "absolu":
        import StratMemoAB
        h2 = StratMemoAB.h
    
    while True:
        move_count += 1
        
        # Choix du coup
        if joueur == "X":
            if s1 == "random":
                coup = AIvsAI.choisir_coup_random(p, "X", PROFONDEUR)
            else:
                coup = AIvsAI.choisir_coup_memo(p, "X", PROFONDEUR, PROFONDEUR, 
                                                h1=h1, h2=h2, strategie1=s1, 
                                                strategie2=s2, simu=SIMU_MONTECARLO)
        else:  # joueur == "O"
            if s2 == "random":
                coup = AIvsAI.choisir_coup_random(p, "O", PROFONDEUR)
            else:
                coup = AIvsAI.choisir_coup_memo(p, "O", PROFONDEUR, PROFONDEUR, 
                                                h1=h1, h2=h2, strategie1=s1, 
                                                strategie2=s2, simu=SIMU_MONTECARLO)
        
        if coup is None:
            passes += 1
            if passes == 2:
                gagnant = Jeu.gagnant(p)
                break
        else:
            passes = 0
            Jeu.retournement(p, joueur, coup[0], coup[1])
        
        joueur = "O" if joueur == "X" else "X"
        
        # Limiter le nombre de coups pour éviter boucles infinies en test
        if move_count > 100:
            gagnant = Jeu.gagnant(p)
            break
    
    return gagnant

def test_quick():
    """Test rapide avec peu de parties"""
    print("=" * 80)
    print("TEST RAPIDE - Version Réduite")
    print("=" * 80)
    print(f"Stratégies: {STRATEGIES}")
    print(f"Parties par affrontement: {NUM_GAMES_PER_MATCHUP}")
    print(f"Total d'affrontements: {len(STRATEGIES) * len(STRATEGIES)}")
    print("=" * 80)
    
    # Initialiser les compteurs
    for s1 in STRATEGIES:
        for s2 in STRATEGIES:
            matchup_key = f"{s1}_vs_{s2}"
            results[matchup_key] = {
                "s1_wins": 0,
                "s2_wins": 0,
                "draws": 0,
                "games": []
            }
    
    # Lancer les affrontements
    for s1 in STRATEGIES:
        for s2 in STRATEGIES:
            matchup_key = f"{s1}_vs_{s2}"
            print(f"\n{s1} vs {s2}...", end=" ", flush=True)
            
            for game_num in range(NUM_GAMES_PER_MATCHUP):
                gagnant = run_single_game(s1, s2)
                
                if gagnant == "X":
                    results[matchup_key]["s1_wins"] += 1
                    winner = s1
                elif gagnant == "O":
                    results[matchup_key]["s2_wins"] += 1
                    winner = s2
                else:
                    results[matchup_key]["draws"] += 1
                    winner = "Égalité"
                
                print(f"Gagnant: {winner}", end=" | ")
                
                game_info = {
                    "s1": s1,
                    "s2": s2,
                    "winner": winner,
                    "result": gagnant
                }
                results[matchup_key]["games"].append(game_info)
                logs.append(game_info)
            
            print()
    
    # Afficher le résumé
    print("\n" + "=" * 80)
    print("RÉSUMÉ RAPIDE")
    print("=" * 80)
    
    for matchup_key in sorted(results.keys()):
        s1, s2 = matchup_key.split("_vs_")
        data = results[matchup_key]
        print(f"{s1} vs {s2}: {data['s1_wins']} wins, {data['s2_wins']} losses, {data['draws']} draws")
    
    # Écrire un fichier de résumé simple
    with open("test_rapide_resultats.txt", "w", encoding="utf-8") as f:
        f.write("RÉSULTATS TEST RAPIDE\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        for log in logs:
            f.write(f"{log['s1']} vs {log['s2']}: Gagnant = {log['winner']} ({log['result']})\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("STATISTIQUES\n")
        f.write("=" * 80 + "\n")
        
        for matchup_key in sorted(results.keys()):
            s1, s2 = matchup_key.split("_vs_")
            data = results[matchup_key]
            f.write(f"{s1} vs {s2}: V={data['s1_wins']} D={data['s2_wins']} E={data['draws']}\n")
    
    print("\n✓ Résumé écrit dans: test_rapide_resultats.txt")

if __name__ == "__main__":
    test_quick()
