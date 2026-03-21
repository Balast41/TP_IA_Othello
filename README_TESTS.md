# Guide de Test des Stratégies

Ce dossier contient des scripts pour tester automatiquement tous les affrontements entre les différentes stratégies d'Othello.

## Scripts disponibles

### 1. `TestQuick.py` - Test rapide (RECOMMANDÉ POUR COMMENCER)
- ✅ **Le plus rapide** - complète en quelques minutes
- Teste 3 stratégies: `random`, `montecarlo`, `poids`
- 1 partie par affrontement
- Paramètres très réduits pour la rapidité

**Utilisation:**
```bash
python TestQuick.py
```

**Résultat:** `test_rapide_resultats.txt`

---

### 2. `TestAll.py` - Test complet de toutes les stratégies
- Teste toutes les stratégies: `montecarlo`, `random`, `poids`, `mobilite`, `mixte`, `absolu`
- Personnalisable via les variables en haut du fichier
- Génère 3 fichiers de résultats

**Paramètres ajustables** (en haut du fichier):
```python
NUM_GAMES_PER_MATCHUP = 2      # Nombre de parties par affrontement
PROFONDEUR = 1                  # Profondeur algorithmes (1=rapide, 3+=lent)
SIMU_MONTECARLO = 50           # Simulations montecarlo (10=rapide, 100+=lent)
```

**Utilisation:**
```bash
python TestAll.py
```

**Résultats générés:**
1. `logs_affrontements_YYYYMMDD_HHMMSS.txt` - Logs détaillés de toutes les parties
2. `resume_affrontements_YYYYMMDD_HHMMSS.txt` - Résumé avec pourcentages et classement
3. `resultats_affrontements_YYYYMMDD_HHMMSS.json` - Données JSON pour analyse

---

## Guide de paramétrage pour TestAll.py

### Vitesse vs Précision

**OPTION 1: Test ultra-rapide (10 minutes)**
```python
NUM_GAMES_PER_MATCHUP = 1      # 1 partie par affrontement
PROFONDEUR = 1                  # Très peu de profondeur
SIMU_MONTECARLO = 10           # Très peu de simulations
```

**OPTION 2: Test rapide (30-60 minutes)**
```python
NUM_GAMES_PER_MATCHUP = 2
PROFONDEUR = 1
SIMU_MONTECARLO = 50
```

**OPTION 3: Test complet (2-4 heures)**
```python
NUM_GAMES_PER_MATCHUP = 3
PROFONDEUR = 2
SIMU_MONTECARLO = 100
```

**OPTION 4: Test très complet (8+ heures)**
```python
NUM_GAMES_PER_MATCHUP = 5
PROFONDEUR = 3
SIMU_MONTECARLO = 100
```

---

## ⚠️  Avertissements de Performance

### Combinaisons très lentes à éviter:
- ❌ `montecarlo` vs `montecarlo` (EXTRÊMEMENT lent)
- ❌ Montecarlo avec `SIMU_MONTECARLO > 100`
- ❌ `PROFONDEUR >= 3` avec montecarlo

### Temps estimés (par partie):
- `random` vs `random`: < 1 seconde
- `random` vs `poids`: 2-5 secondes
- `montecarlo` vs `random`: 30 secondes - 2 minutes (dépend de SIMU)
- Autres combinaisons: 5-30 secondes

---

## Analyse des résultats

### Format de `resume_affrontements_*.txt`:

```
TABLEAU DE RÉSULTATS
────────────────────────────────────────────────────────
Stratégie 1    | Stratégie 2    | Victoires S1  | % Victoire S1
────────────────────────────────────────────────────────
montecarlo     | random         | 3             | 75.00%
random         | montecarlo     | 1             | 25.00%
...
```

**Classement final** - Taux de victoire global par stratégie:
```
1. poids - 65.00% de victoire (39/60 parties)
2. montecarlo - 55.00% de victoire (33/60 parties)
3. mobilite - 48.00% de victoire (29/60 parties)
...
```

### Format de `resultats_affrontements_*.json`:

Fichier structuré pour analyse informatique:
- `results`: Résultats détaillés par affrontement
- `logs`: Historique de toutes les parties
- `parameters`: Paramètres utilisés pour la run

---

## Exemple de workflow complet

```bash
# 1. Commencer par un test rapide pour valider
python TestQuick.py
cat test_rapide_resultats.txt

# 2. Lancer un test complet
python TestAll.py

# 3. Consulter les résultats
notepad resume_affrontements_20260317_120000.txt

# 4. (Optionnel) Analyser les données JSON
# Importez resultats_affrontements_*.json dans votre outil d'analyse
```

---

## Dépannage

### "Le script s'arrête après quelques minutes"
→ Montecarlo est trop lent. Réduisez `SIMU_MONTECARLO` à 10-20 ou exécutez sans montecarlo

### "Certains affrontements sont sautés"
→ C'est normal - montecarlo vs montecarlo est exclu pour éviter les blocages

### "Les fichiers n'apparaissent pas"
→ Vérifiez que vous êtes dans le bon dossier et que Python n'a pas d'erreur (console)

---

## Notes d'implémentation

- Les tests utilisent le même moteur de jeu que `AIvsAI.partie()`
- Les résultats sont sauvegardés avec timestamps pour éviter les écrasements
- Les heuristiques sont sélectionnées automatiquement selon la stratégie
- Les parties qui dépassent 100 coups sont stoppées (évite boucles infinies)

---

**Dernière mise à jour:** Mars 2026
