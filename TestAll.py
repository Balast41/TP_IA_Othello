import AIvsAI
import Jeu
from datetime import datetime
import json

# Listes des stratégies à tester
STRATEGIES = [
    "montecarlo",
    "random",
    "poids",
    "mobilite",
    "mixte",
    "absolu"
]

# Paramètres de test
#   AVERTISSEMENT: Certaines combinaisons peuvent être TRÈS lentes
# - montecarlo vs montecarlo: EXTRÊMEMENT lent (éviter)
# - montecarlo avec SIMU_MONTECARLO élevé: très lent
# Recommandation: commencer avec NUM_GAMES = 1 ou 2 et PROFONDEUR = 1
NUM_GAMES_PER_MATCHUP = 4  # Nombre de parties par affrontement
PROFONDEUR = 4  # Profondeur pour les algorithmes 
SIMU_MONTECARLO = 25  # Simulations pour Monte Carlo

# Dictionaries pour stocker les résultats
results = {}
logs = []

def run_game(strategie1, strategie2, game_num):
    """Lance une partie et retourne le gagnant"""
    try:
        # Lancer la partie (retourne 0 si tout va bien)
        winner = AIvsAI.partie(strategie1, strategie2, PROFONDEUR, PROFONDEUR, SIMU_MONTECARLO)
        # AIvsAI.partie affiche directement mais ne retourne rien utile, 
        # donc on doit modifier ou wrapper pour capturer le gagnant
        # Pour l'instant, on va capturer manuellement en modifiant le retour
    except Exception as e:
        print(f"Erreur lors du match {strategie1} vs {strategie2}: {e}")
        return None

def test_all_matchups():
    """Lance tous les affrontements possibles"""
    print("=" * 80)
    print("DÉMARRAGE DES TESTS DE TOUTES LES STRATÉGIES")
    print("=" * 80)
    print(f"Nombre de parties par affrontement: {NUM_GAMES_PER_MATCHUP}")
    print(f"Stratégies testées: {', '.join(STRATEGIES)}")
    # Exclure les affrontements d'une IA contre elle-même
    total_pairings = len(STRATEGIES) * (len(STRATEGIES) - 1)
    print(f"Nombre total d'affrontements: {total_pairings}")
    print(f"Nombre total de parties: {total_pairings * NUM_GAMES_PER_MATCHUP}")
    print("=" * 80)
    
    total_matchups = 0
    
    # Initialiser les compteurs de résultats
    for s1 in STRATEGIES:
        for s2 in STRATEGIES:
            if s1 == s2:
                # Ne pas enregistrer les affrontements d'une IA contre elle-même
                continue
            matchup_key = f"{s1}_vs_{s2}"
            results[matchup_key] = {
                "s1_wins": 0,
                "s2_wins": 0,
                "draws": 0,
                "games": []
            }
    
    # Lancer tous les affrontements
    for s1 in STRATEGIES:
        for s2 in STRATEGIES:
            # Ignorer les affrontements d'une IA contre elle-même
            if s1 == s2:
                print(f"\n[⏭️  SKIPPED] {s1} vs {s2} (même IA)")
                continue
            #   Éviter les combinaisons trop lentes
            if (s1 == "montecarlo" and s2 == "montecarlo"):
                print(f"\n[⏭️  SKIPPED] {s1} vs {s2} (trop lent)")
                continue
            matchup_key = f"{s1}_vs_{s2}"
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Affrontement: {s1} vs {s2}")
            
            for game_num in range(NUM_GAMES_PER_MATCHUP):
                print(f"  Partie {game_num + 1}/{NUM_GAMES_PER_MATCHUP}...", end=" ", flush=True)
                
                # Créer une instance modifiée de partie pour capturer le gagnant
                p = AIvsAI.Ini_Aff.initialisation_plateau()
                joueur = "X"
                passes = 0
                game_moves = 0
                
                while True:
                    game_moves += 1
                    
                    # Choix du coup
                    if joueur == "X":
                        if s1 == "random":
                            coup = AIvsAI.choisir_coup_random(p, "X", PROFONDEUR)
                        else:
                            coup = AIvsAI.choisir_coup_memo(p, "X", PROFONDEUR, PROFONDEUR, 
                                                            h1=None, h2=None, strategie1=s1, 
                                                            strategie2=s2, simu=SIMU_MONTECARLO)
                    else:
                        if s2 == "random":
                            coup = AIvsAI.choisir_coup_random(p, "O", PROFONDEUR)
                        else:
                            coup = AIvsAI.choisir_coup_memo(p, "O", PROFONDEUR, PROFONDEUR, 
                                                            h1=None, h2=None, strategie1=s1, 
                                                            strategie2=s2, simu=SIMU_MONTECARLO)
                    
                    if coup is None:
                        passes += 1
                        if passes == 2:
                            # Fin de partie
                            gagnant = Jeu.gagnant(p)
                            break
                    else:
                        passes = 0
                        Jeu.retournement(p, joueur, coup[0], coup[1])
                    
                    joueur = "O" if joueur == "X" else "X"
                
                # Enregistrer le résultat
                if gagnant == "X":
                    results[matchup_key]["s1_wins"] += 1
                    winner_name = s1
                elif gagnant == "O":
                    results[matchup_key]["s2_wins"] += 1
                    winner_name = s2
                else:
                    results[matchup_key]["draws"] += 1
                    winner_name = "Égalité"
                
                game_info = {
                    "game_num": game_num + 1,
                    "s1": s1,
                    "s2": s2,
                    "winner": winner_name,
                    "result": gagnant,
                    "moves": game_moves,
                    "timestamp": datetime.now().isoformat()
                }
                results[matchup_key]["games"].append(game_info)
                logs.append(game_info)
                
                print(f"Gagnant: {winner_name}")
                total_matchups += 1
    
    print("\n" + "=" * 80)
    print("TESTS TERMINÉS")
    print("=" * 80)

def write_logs():
    """Écrit les logs détaillés dans un fichier"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"logs_affrontements_{timestamp}.txt"
    
    with open(log_filename, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("LOGS DÉTAILLÉS DES AFFRONTEMENTS\n")
        f.write("=" * 80 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Nombre de parties par affrontement: {NUM_GAMES_PER_MATCHUP}\n")
        f.write(f"Nombre total de parties: {len(logs)}\n")
        f.write("=" * 80 + "\n\n")
        
        current_matchup = None
        for log in logs:
            matchup = f"{log['s1']} vs {log['s2']}"
            if matchup != current_matchup:
                current_matchup = matchup
                f.write(f"\n{'─' * 80}\n")
                f.write(f"AFFRONTEMENT: {matchup}\n")
                f.write(f"{'─' * 80}\n")
            
            f.write(f"  Partie {log['game_num']}\n")
            f.write(f"    Gagnant: {log['winner']}\n")
            f.write(f"    Coups joués: {log['moves']}\n")
            f.write(f"    Résultat brut: {log['result']}\n")
            f.write(f"    Heure: {log['timestamp']}\n\n")
    
    print(f"Logs écrits dans: {log_filename}")
    return log_filename

def write_summary():
    """Écrit un résumé avec statistiques"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_filename = f"resume_affrontements_{timestamp}.txt"
    
    with open(summary_filename, "w", encoding="utf-8") as f:
        f.write("=" * 100 + "\n")
        f.write("RÉSUMÉ DES AFFRONTEMENTS - POURCENTAGES DE VICTOIRE\n")
        f.write("=" * 100 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Nombre de parties par affrontement: {NUM_GAMES_PER_MATCHUP}\n\n")
        
        # Tableau principal résumé
        f.write("TABLEAU DE RÉSULTATS\n")
        f.write("─" * 100 + "\n")
        f.write(f"{'Stratégie 1':<15} | {'Stratégie 2':<15} | {'Victoires S1':<15} | {'Victoires S2':<15} | {'Égalités':<10} | {'% Victoire S1':<15}\n")
        f.write("─" * 100 + "\n")
        
        for matchup_key in sorted(results.keys()):
            s1, s2 = matchup_key.split("_vs_")
            data = results[matchup_key]
            total = data["s1_wins"] + data["s2_wins"] + data["draws"]
            pct_s1 = (data["s1_wins"] / total * 100) if total > 0 else 0
            
            f.write(f"{s1:<15} | {s2:<15} | {data['s1_wins']:<15} | {data['s2_wins']:<15} | {data['draws']:<10} | {pct_s1:>6.2f}%\n")
        
        f.write("─" * 100 + "\n\n")
        
        # Récapitulatif global par stratégie
        f.write("STATISTIQUES GLOBALES PAR STRATÉGIE\n")
        f.write("─" * 100 + "\n")
        f.write(f"{'Stratégie':<15} | {'Victoires Totales':<20} | {'Défaites Totales':<20} | {'Égalités':<10} | {'Taux de Victoire':<20}\n")
        f.write("─" * 100 + "\n")
        
        strategy_stats = {}
        for strategy in STRATEGIES:
            strategy_stats[strategy] = {
                "wins": 0,
                "losses": 0,
                "draws": 0,
                "total": 0
            }
        
        for matchup_key, data in results.items():
            s1, s2 = matchup_key.split("_vs_")
            strategy_stats[s1]["wins"] += data["s1_wins"]
            strategy_stats[s1]["losses"] += data["s2_wins"]
            strategy_stats[s1]["draws"] += data["draws"]
            strategy_stats[s1]["total"] += (data["s1_wins"] + data["s2_wins"] + data["draws"])
            
            strategy_stats[s2]["wins"] += data["s2_wins"]
            strategy_stats[s2]["losses"] += data["s1_wins"]
            strategy_stats[s2]["draws"] += data["draws"]
            strategy_stats[s2]["total"] += (data["s1_wins"] + data["s2_wins"] + data["draws"])
        
        for strategy in sorted(STRATEGIES):
            stats = strategy_stats[strategy]
            if stats["total"] > 0:
                win_rate = (stats["wins"] / stats["total"] * 100)
            else:
                win_rate = 0
            
            f.write(f"{strategy:<15} | {stats['wins']:<20} | {stats['losses']:<20} | {stats['draws']:<10} | {win_rate:>6.2f}%\n")
        
        f.write("─" * 100 + "\n\n")
        
        # Classement
        f.write("CLASSEMENT DES STRATÉGIES (par taux de victoire global)\n")
        f.write("─" * 100 + "\n")
        
        sorted_strategies = sorted(STRATEGIES, 
                                   key=lambda s: (strategy_stats[s]["wins"] / strategy_stats[s]["total"] * 100) if strategy_stats[s]["total"] > 0 else 0,
                                   reverse=True)
        
        for rank, strategy in enumerate(sorted_strategies, 1):
            stats = strategy_stats[strategy]
            if stats["total"] > 0:
                win_rate = (stats["wins"] / stats["total"] * 100)
            else:
                win_rate = 0
            f.write(f"{rank}. {strategy:<15} - {win_rate:>6.2f}% de victoire ({stats['wins']}/{stats['total']} parties)\n")
        
        f.write("─" * 100 + "\n")
    
    print(f"Résumé écrit dans: {summary_filename}")
    return summary_filename

def write_json_results():
    """Écrit les résultats en JSON pour analyse ultérieure"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_filename = f"resultats_affrontements_{timestamp}.json"
    
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "parameters": {
                "games_per_matchup": NUM_GAMES_PER_MATCHUP,
                "profondeur": PROFONDEUR,
                "simu_montecarlo": SIMU_MONTECARLO
            },
            "results": results,
            "logs": logs
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Résultats JSON écrits dans: {json_filename}")
    return json_filename

if __name__ == "__main__":
    # Lancer tous les tests
    test_all_matchups()
    
    # Écrire les résultats
    log_file = write_logs()
    summary_file = write_summary()
    json_file = write_json_results()
    
    print("\n" + "=" * 80)
    print("FICHIERS GÉNÉRÉS:")
    print(f"  - {log_file}")
    print(f"  - {summary_file}")
    print(f"  - {json_file}")
    print("=" * 80)
