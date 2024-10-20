import csv
import os
from models.action import Action
from rich.console import Console

console = Console()

class DataController:
    @staticmethod
    def lire_donnees_fichier(fichier, delimiteur=';'):
        actions = []
        try:
            if not os.path.exists(fichier):
                console.print(f"[red]Erreur: Le fichier {fichier} n'existe pas[/red]")
                return actions

            with open(fichier, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=delimiteur)
                headers = reader.fieldnames
                console.print(f"[green]Colonnes détectées : {headers}[/green]")

                for row in reader:
                    try:
                        if delimiteur == ';':
                            # Format pour data_test.csv
                            action = Action(
                                row['Actions'],
                                row[' Coût par action (en euros)'],
                                row[' Bénéfice (après 2 ans)']
                            )
                        else:
                            # Format pour dataset1 et dataset2
                            action = Action(
                                row['name'],
                                row['price'],
                                row['profit']
                            )

                        if action.est_valide():
                            actions.append(action)
                        else:
                            console.print(f"[yellow]Action ignorée car invalide: {action.nom}[/yellow]")

                    except KeyError as e:
                        console.print(f"[red]Erreur de format dans le fichier. Colonne manquante: {e}[/red]")
                        return []
                    except Exception as e:
                        console.print(f"[red]Erreur lors de la lecture d'une ligne: {e}[/red]")
                        continue

        except Exception as e:
            console.print(f"[red]Erreur lors de la lecture du fichier : {e}[/red]")
        
        console.print(f"[green]Nombre d'actions chargées: {len(actions)}[/green]")
        return actions