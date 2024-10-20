# Imports nécessaires
import time
import os
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

from colorama import init, Fore, Style
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.panel import Panel
from rich.table import Table
from rich import box
from controllers.data_controller import DataController
from controllers.optimizer_controller import OptimizerController
from models.action import Action
from models.portfolio import Portfolio
from views.resultat_view import ResultatView

# Initialisation de colorama et console
init()
console = Console()

def effacer_ecran():
    """Effacer l'écran"""
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_titre():
    """Afficher le titre du programme"""
    effacer_ecran()
    console.print("\n")
    console.print(Panel("AlgoOpti++", border_style="blue"))
    console.print("=" * 60, style="yellow")
    console.print("Optimisation d'investissements en actions", style="green bold", justify="center")
    console.print("=" * 60, style="yellow")
    console.print("\n")

def show_complexity_chart():
    """Générer et afficher un graphique de complexité"""
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Génération des points de données
    n = np.linspace(1, 20, 100)
    bruteforce = 2**n
    optimized = n * np.log2(n)
    
    # Tracer avec un style personnalisé
    ax.plot(n, bruteforce, 'r-', label='Force Brute O(2ⁿ)', linewidth=2)
    ax.plot(n, optimized, 'g-', label='Optimisé O(n log n)', linewidth=2)
    
    ax.set_yscale('log')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title('Comparaison des Complexités Algorithmiques', color='white', pad=20, fontsize=14)
    ax.set_xlabel('Nombre d\'actions (n)', color='white')
    ax.set_ylabel('Temps d\'exécution (échelle log)', color='white')
    
    for spine in ax.spines.values():
        spine.set_color('white')
    ax.tick_params(colors='white')
    
    legend = ax.legend(facecolor='black', edgecolor='white')
    plt.setp(legend.get_texts(), color='white')
    
    info_text = (
        "Complexité des Algorithmes:\n"
        "• Force Brute: O(2ⁿ) - Optimal mais lent pour n>20\n"
        "• Optimisé: O(n log n) - Rapide avec résultats optimaux"
    )
    plt.figtext(0.02, 0.02, info_text, color='white', 
                bbox=dict(facecolor='black', alpha=0.8, edgecolor='white'))
    
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(60)
    plt.close()

def progress_animation(description, duration=1):
    """Afficher une animation de progression"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(complete_style="green"),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        expand=True
    ) as progress:
        task = progress.add_task(f"[cyan]{description}[/cyan]", total=100)
        while not progress.finished:
            progress.update(task, advance=1)
            time.sleep(duration / 100)

def afficher_menu_principal():
    """Afficher le menu principal"""
    menu = Table(show_header=False, box=box.ROUNDED)
    menu.add_column("Option", style="cyan")
    menu.add_column("Description", style="white")
    
    menu.add_row("1", "[green]Choisir le fichier de données[/green]")
    menu.add_row("2", "[green]Choisir l'algorithme[/green]")
    menu.add_row("3", "[green]Modifier le budget[/green]")
    menu.add_row("4", "[yellow]Exécuter l'optimisation[/yellow]")
    menu.add_row("5", "[green]Visualiser les complexités[/green]")
    menu.add_row("6", "[red]Quitter[/red]")
    
    console.print(Panel(menu, title="[cyan]Menu Principal[/cyan]", border_style="blue"))
    return console.input("[cyan]Votre choix (1-6): [/cyan]")

# Fonction principale
def main():
    budget = 500  # Budget par défaut
    fichier_choisi = "data/data_test.csv"  # Fichier par défaut
    delimiteur = ';'  # Délimiteur par défaut
    algorithme = "bruteforce"  # Algorithme par défaut
    
    while True:
        afficher_titre()
        choix = afficher_menu_principal()
        
        if choix == "1":
            table = Table(title="Fichiers Disponibles", box=box.ROUNDED)
            table.add_column("Option", style="cyan")
            table.add_column("Fichier", style="green")
            table.add_column("Description", style="yellow")
            
            table.add_row("1", "data_test.csv", "Petit dataset (test)")
            table.add_row("2", "dataset1_Python+P7.csv", "Dataset moyen")
            table.add_row("3", "dataset2_Python+P7.csv", "Grand dataset")
            
            console.print(Panel(table, border_style="blue"))
            choix_fichier = console.input("[cyan]Choisir un fichier (1-3): [/cyan]")
            
            if choix_fichier == "1":
                fichier_choisi = "data/data_test.csv"
                delimiteur = ';'
            elif choix_fichier == "2":
                fichier_choisi = "data/dataset1_Python+P7.csv"
                delimiteur = ','
            elif choix_fichier == "3":
                fichier_choisi = "data/dataset2_Python+P7.csv"
                delimiteur = ','
        
        elif choix == "2":
            console.print(Panel("Choisir l'algorithme:", border_style="blue"))
            console.print("[1] Force brute (optimal mais lent)")
            console.print("[2] Optimisé (rapide)")
            choix_algo = console.input("[cyan]Votre choix (1-2): [/cyan]")
            algorithme = "bruteforce" if choix_algo == "1" else "optimized"
        
        elif choix == "3":
            nouveau_budget = console.input("[cyan]Entrer le nouveau budget en euros: [/cyan]")
            try:
                budget = float(nouveau_budget)
                console.print(f"[green]Budget mis à jour: {budget}€[/green]")
            except ValueError:
                console.print("[red]Budget invalide![/red]")
        
        elif choix == "4":
            progress_animation("Chargement des données...")
            actions = DataController.lire_donnees_fichier(fichier_choisi, delimiteur)
            
            if not actions:
                console.print("[red]Erreur: Aucune action chargée![/red]")
                continue
            
            progress_animation("Optimisation en cours...")
            debut = time.time()
            
            if algorithme == "bruteforce":
                portfolio = OptimizerController.optimiser_bruteforce(actions, budget)
            else:
                portfolio = OptimizerController.optimiser_greedy(actions, budget)
            
            temps_execution = time.time() - debut
            
            ResultatView.afficher_resultat(portfolio, temps_execution)
            input("\nAppuyez sur Entrée pour continuer...")

        elif choix == "5":
            show_complexity_chart()
            input("\nAppuyez sur Entrée pour continuer...")

        elif choix == "6":
            effacer_ecran()
            sys.exit(0)

if __name__ == "__main__":
    main()