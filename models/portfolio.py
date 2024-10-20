class Portfolio:
    def __init__(self):
        self.actions = []
        self.cout_total = 0
        self.profit_total = 0

    def ajouter_action(self, action):
        if action and action.est_valide():
            self.actions.append(action)
            self.cout_total += action.prix
            self.profit_total += action.profit

    def est_dans_budget(self, budget):
        return self.cout_total <= budget

    def rendement(self):
        if self.cout_total > 0:
            return (self.profit_total / self.cout_total) * 100
        return 0

    def __str__(self):
        return (f"Nombre d'actions: {len(self.actions)}\n"
                f"Coût total: {self.cout_total:.2f}€\n"
                f"Profit total: {self.profit_total:.2f}€\n"
                f"Rendement: {self.rendement():.2f}%")