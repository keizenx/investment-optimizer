from rich.console import Console
from rich.table import Table
from rich import box
from rich.panel import Panel

console = Console()

class ResultatView:
    @staticmethod
    def afficher_resultat(portfolio, temps_execution=None):
        # Création d'une table riche pour les résultats
        table = Table(
            title="Résultats de l'Optimisation",
            box=box.DOUBLE_EDGE,
            border_style="cyan"
        )
        
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
        
        # Ajout du résumé
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
        
        # Affichage de la table détaillée
        console.print("\n")
        console.print(table)
        
        # Affichage du temps d'exécution
        if temps_execution:
            console.print(f"\n[yellow]Temps d'exécution: {temps_execution:.4f} secondes[/yellow]")