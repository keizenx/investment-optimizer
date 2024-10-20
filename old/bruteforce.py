from itertools import combinations
import csv
import time

start_time = time.time()
def lire_donnees_fichier(fichier):
    actions = []
    try:
        with open(fichier, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            headers = reader.fieldnames
            print(f"Noms des colonnes détectées : {headers}")  # Vérification des colonnes

            for row in reader:
                try:
                    action = {
                        'nom': row['Actions'].strip(),
                        'prix': float(row[' Coût par action (en euros)'].strip()),
                        'benefice': float(row[' Bénéfice (après 2 ans)'].replace('%', '').strip()),
                        'profit': float(float(row[' Coût par action (en euros)'].strip())*(float(row[' Bénéfice (après 2 ans)'].replace('%', '').strip())/100))
                    }
                    actions.append(action)
                except KeyError as e:
                    print(f"Erreur de clé : {e} - Vérifie les noms de colonnes dans le CSV.")
                    return []
                except ValueError as e:
                    print(f"Erreur de conversion des valeurs : {e} - Vérifie les données dans le CSV.")
                    return []
    except FileNotFoundError as e:
        print(f"Erreur : fichier non trouvé - {e}")
        return []
    
    # Remove duplicate actions based on 'nom'
    unique_actions = {action['nom']: action for action in actions}.values()
    return list(unique_actions)

# Chargement des actions depuis le fichier CSV
actions = lire_donnees_fichier('data/data_test.csv')

# Fonction pour calculer le profit total d'un ensemble d'actions
def calculate_profit(action_subset):
    total_cost = sum(action["prix"] for action in action_subset)
    total_profit = sum(action["profit"] for action in action_subset)
    return total_cost, total_profit

# Fonction de force brute
def brute_force_solution(actions, budget):
    best_profit = 0
    best_combination = []
    best_cost = 0

    # Générer toutes les combinaisons possibles
    for r in range(1, len(actions) + 1):
        for combination in combinations(actions, r):
            total_cost, total_profit = calculate_profit(combination)

            # Si le coût est dans le budget et le profit est supérieur au meilleur profit trouvé
            if total_cost <= budget and total_profit > best_profit:
                best_profit = total_profit
                best_combination = combination
                best_cost = total_cost

    return best_combination, best_profit, best_cost

# Résoudre avec un budget de 500 euros
budget = 500
best_combination, best_profit, cost = brute_force_solution(actions, budget)
end_time = time.time()
delay = end_time - start_time
# Affichage des résultats
print("Meilleure combinaison :")
for action in best_combination:
    print(f"{action['nom']} {action['prix']}€")

print(f"Coût total: {cost}€")
print(f"Meilleur profit : {best_profit}€")
print(delay)
