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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Premier graphique : Complexité théorique
    n = np.linspace(1, 20, 100)
    bruteforce = 2**n
    optimized = n * np.log2(n)
    
    ax1.plot(n, bruteforce, 'r-', label='Force Brute O(2ⁿ)', linewidth=2)
    ax1.plot(n, optimized, 'g-', label='Optimisé O(n log n)', linewidth=2)
    
    ax1.set_yscale('log')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.set_title('Complexité Théorique', color='white', pad=20, fontsize=14)
    ax1.set_xlabel('Nombre d\'actions (n)', color='white')
    ax1.set_ylabel('Temps d\'exécution (échelle log)', color='white')
    
    for spine in ax1.spines.values():
        spine.set_color('white')
    ax1.tick_params(colors='white')
    
    legend1 = ax1.legend(facecolor='black', edgecolor='white')
    plt.setp(legend1.get_texts(), color='white')

    # Deuxième graphique : Exemple pratique
    n_practical = np.array([5, 10, 15, 20])
    time_bruteforce = [0.1, 1.0, 15.0, 300.0]  # Temps approximatifs
    time_optimized = [0.05, 0.15, 0.3, 0.5]    # Temps approximatifs

    ax2.bar(n_practical - 0.2, time_bruteforce, 0.4, label='Force Brute',
            color='red', alpha=0.7)
    ax2.bar(n_practical + 0.2, time_optimized, 0.4, label='Optimisé',
            color='green', alpha=0.7)

    ax2.set_title('Exemple de Temps d\'Exécution', color='white', pad=20, fontsize=14)
    ax2.set_xlabel('Nombre d\'actions', color='white')
    ax2.set_ylabel('Temps (secondes)', color='white')
    ax2.grid(True, linestyle='--', alpha=0.3)
    
    for spine in ax2.spines.values():
        spine.set_color('white')
    ax2.tick_params(colors='white')
    
    legend2 = ax2.legend(facecolor='black', edgecolor='white')
    plt.setp(legend2.get_texts(), color='white')

    # Informations supplémentaires
    info_text = (
        "Complexité des Algorithmes:\n"
        "• Force Brute: O(2ⁿ) - Optimal mais lent pour n>20\n"
        "• Optimisé: O(n log n) - Rapide avec résultats optimaux"
    )
    plt.figtext(0.02, 0.02, info_text, color='white', 
                bbox=dict(facecolor='black', alpha=0.8, edgecolor='white'))
    
    plt.tight_layout()
    plt.show(block=False)
    plt.pause(120)
    plt.close()

class ResultatView:
    @staticmethod
    def afficher_resultat(portfolio, temps_execution=None):
        """Afficher les résultats de l'optimisation"""
        # Affichage du tableau des résultats
        table = Table(title="Résultats de l'Optimisation", box=box.DOUBLE_EDGE)
        
        # Configuration des colonnes
        table.add_column("Action", style="green")
        table.add_column("Prix", style="yellow", justify="right")
        table.add_column("Bénéfice", style="blue", justify="right")
        table.add_column("Profit", style="cyan", justify="right")
        
        # Ajout des actions
        for action in portfolio.actions:
            table.add_row(
                action.nom,
                f"{action.prix:.2f}€",
                f"{action.benefice:.2f}%",
                f"{action.profit:.2f}€"
            )
        
        # Ligne de total
        table.add_section()
        table.add_row(
            "TOTAL",
            f"{portfolio.cout_total:.2f}€",
            f"{portfolio.rendement():.2f}%",
            f"{portfolio.profit_total:.2f}€",
            style="bold magenta"
        )
        
        # Affichage du résumé dans un panneau
        console.print("\n")
        summary = Panel(
            f"[cyan]Nombre d'actions: [white]{len(portfolio.actions)}[/white]\n"
            f"[yellow]Coût total: [white]{portfolio.cout_total:.2f}€[/white]\n"
            f"[green]Profit total: [white]{portfolio.profit_total:.2f}€[/white]\n"
            f"[magenta]Rendement: [white]{portfolio.rendement():.2f}%[/white]",
            title="Résumé",
            border_style="blue"
        )
        console.print(summary)
        console.print(table)
        
        if temps_execution:
            console.print(f"\n[yellow]Temps d'exécution: {temps_execution:.4f} secondes[/yellow]")
        
        # Affichage des graphiques
        ResultatView._afficher_graphiques(portfolio, temps_execution)
    
    @staticmethod
    def _afficher_graphiques(portfolio, temps_execution):
        """Afficher les graphiques de résultats"""
        plt.style.use('dark_background')
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        if portfolio.actions:
            # Données pour les graphiques
            noms = [action.nom for action in portfolio.actions]
            couts = [action.prix for action in portfolio.actions]
            profits = [action.profit for action in portfolio.actions]
            
            # Graphique 1: Répartition des investissements
            ax1.pie(couts, labels=noms, autopct='%1.1f%%',
                   colors=plt.cm.viridis(np.linspace(0, 1, len(couts))),
                   textprops={'color': 'white'})
            ax1.set_title('Répartition des Investissements', color='white', pad=20)
            
            # Graphique 2: Profits par action
            bars = ax2.bar(noms, profits,
                          color=plt.cm.viridis(np.linspace(0, 1, len(profits))))
            ax2.set_title('Profits par Action', color='white', pad=20)
            ax2.set_xlabel('Actions', color='white')
            ax2.set_ylabel('Profit (€)', color='white')
            ax2.tick_params(axis='x', rotation=45, colors='white')
            ax2.tick_params(axis='y', colors='white')
            
            # Ajout des valeurs sur les barres
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.2f}€',
                        ha='center', va='bottom', color='white')
            
            ax2.grid(True, linestyle='--', alpha=0.3)
            
            # Configuration des bordures
            for spine in ax2.spines.values():
                spine.set_color('white')
        
        # Informations supplémentaires
        info_text = (
            f"Performance:\n"
            f"Coût Total: {portfolio.cout_total:.2f}€\n"
            f"Profit Total: {portfolio.profit_total:.2f}€\n"
            f"Rendement: {portfolio.rendement():.2f}%\n"
            f"Temps: {temps_execution:.3f}s"
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