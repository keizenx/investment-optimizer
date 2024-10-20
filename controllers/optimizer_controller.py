from itertools import combinations
from models.portfolio import Portfolio
from rich.console import Console
import time

console = Console()

class OptimizerController:
    @staticmethod
    def filtrer_actions_valides(actions):
        """Filtre les actions avec des prix valides (non nuls)"""
        actions_valides = [action for action in actions if action.est_valide()]
        if len(actions_valides) < len(actions):
            console.print(f"[yellow]Attention: {len(actions) - len(actions_valides)} action(s) ignorée(s) car invalide(s)[/yellow]")
        return actions_valides

    @staticmethod
    def optimiser_bruteforce(actions, budget):
        """Algorithme force brute pour trouver la meilleure combinaison"""
        actions_valides = OptimizerController.filtrer_actions_valides(actions)
        if not actions_valides:
            console.print("[red]Aucune action valide trouvée![/red]")
            return Portfolio()

        meilleur_portfolio = Portfolio()
        total_combinations = sum(1 for r in range(1, len(actions_valides) + 1)
                               for _ in combinations(actions_valides, r))
        combinations_tested = 0
        
        try:
            start_time = time.time()
            for r in range(1, len(actions_valides) + 1):
                for combinaison in combinations(actions_valides, r):
                    combinations_tested += 1
                    if combinations_tested % 1000 == 0:
                        elapsed_time = time.time() - start_time
                        progress = (combinations_tested / total_combinations) * 100
                        console.print(f"[cyan]Progression: {progress:.1f}% - Temps écoulé: {elapsed_time:.1f}s[/cyan]")
                    
                    portfolio_test = Portfolio()
                    for action in combinaison:
                        portfolio_test.ajouter_action(action)
                    
                    if (portfolio_test.est_dans_budget(budget) and 
                        portfolio_test.profit_total > meilleur_portfolio.profit_total):
                        meilleur_portfolio = Portfolio()
                        for action in combinaison:
                            meilleur_portfolio.ajouter_action(action)
            
            return meilleur_portfolio
        except Exception as e:
            console.print(f"[red]Erreur lors de l'optimisation: {e}[/red]")
            return Portfolio()

    @staticmethod
    def optimiser_greedy(actions, budget):
        """Algorithme optimisé pour trouver une bonne combinaison rapidement"""
        actions_valides = OptimizerController.filtrer_actions_valides(actions)
        if not actions_valides:
            console.print("[red]Aucune action valide trouvée![/red]")
            return Portfolio()

        portfolio = Portfolio()
        try:
            # Tri des actions par ratio profit/prix décroissant
            actions_triees = sorted(
                actions_valides,
                key=lambda x: (x.profit/x.prix if x.prix > 0 else 0),
                reverse=True
            )

            for action in actions_triees:
                if portfolio.cout_total + action.prix <= budget:
                    portfolio.ajouter_action(action)
                    console.print(f"[green]Action ajoutée: {action.nom} - Profit: {action.profit:.2f}€[/green]")
            
            return portfolio
        except Exception as e:
            console.print(f"[red]Erreur lors de l'optimisation: {e}[/red]")
            return Portfolio()