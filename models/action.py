class Action:
    def __init__(self, nom, prix, benefice):
        try:
            self.nom = str(nom).strip()
            # Gestion des prix avec virgule ou point
            prix_str = str(prix).strip().replace(',', '.')
            self.prix = float(prix_str)
            # Gestion des pourcentages avec ou sans symbole %
            benefice_str = str(benefice).replace(',', '.').replace('%', '').strip()
            self.benefice = float(benefice_str)
            self.profit = self.prix * (self.benefice / 100)
        except ValueError as e:
            print(f"Erreur lors de la création de l'action {nom}: {e}")
            # Valeurs par défaut en cas d'erreur
            self.nom = str(nom)
            self.prix = 0.0
            self.benefice = 0.0
            self.profit = 0.0

    def __str__(self):
        return f"{self.nom} - Prix: {self.prix:.2f}€ - Bénéfice: {self.benefice:.2f}% - Profit: {self.profit:.2f}€"

    def est_valide(self):
        return self.prix > 0 and self.benefice > 0