class TeamStats:
    def __init__(self):
        self.stats = {}

    def add_stat(self, category, key, value):
        """Adiciona uma estatística à categoria especificada."""
        if category not in self.stats:
            self.stats[category] = {}
        self.stats[category][key] = value

    def get_stats(self, category=None):
        """Retorna as estatísticas de uma categoria específica ou todas as categorias."""
        if category:
            return self.stats.get(category, {})
        return self.stats

    def display_stats(self):
        """Exibe todas as estatísticas armazenadas."""
        for category, data in self.stats.items():
            print(f"Categoria: {category}")
            for key, value in data.items():
                print(f"  {key}: {value}")