from itertools import combinations
import csv
import time

start_time = time.time()
def lire_donnees_fichier(fichier):
    actions = []
    try:
        with open(fichier, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            headers = reader.fieldnames
            print(f"Noms des colonnes détectées : {headers}")  # Vérification des colonnes

            for row in reader:
                try:
                    action = {
                        'nom': row['name'].strip(),
                        'prix': float(row['price'].strip()),
                        'benefice': float(row['profit'].replace('%', '').strip()),
                        'profit': float(float(row['price'].strip())*(float(row['profit'].replace('%', '').strip())/100)),
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
    return actions

# Chargement des actions depuis le fichier CSV
actions = lire_donnees_fichier('data\dataset2_Python+P7.csv')

def filter_action(actions):
    filter_actions = []
    for action in actions:
        if(action['profit'] > 0):
            filter_actions.append(action)
        else:
            pass
    return filter_actions

def sort_actions_profit(actions):
    # Sorting the actions by 'profit' in descending order
    return sorted(actions, key=lambda x: x['prix']/x['profit'], reverse=False)

sorted_actions = sort_actions_profit(filter_action(actions))


def get_best_combinaison(budget,sorted_actions):
    combinaison = []
    total_profit = 0
    total_cost = 0

    for action in filter_action(sorted_actions):
        if(total_cost + action['prix'] < budget):
            combinaison.append(action)
            total_cost += action['prix']
            total_profit += action['profit']
        else:
            pass
    return total_cost,total_profit,combinaison

# Résoudre avec un budget de 500 euros
budget = 500
total_cost, total_profit, combinaison = get_best_combinaison(budget, sorted_actions)
end_time = time.time()
delay = end_time -start_time
print("Meilleure combinaison :")
for action in combinaison:
    print(f"{action['nom']} {action['prix']}")
print(f"coût: {total_cost}€")
print(f"Meilleur profit : {total_profit}€")
print(delay)