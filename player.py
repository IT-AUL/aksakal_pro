class Player:
    def __init__(self):
        self.health = 50
        self.name = "Алмаз"
        self.items = []

    def apply_changes(self, health=0, items=None):
        if items is None:
            items = []
        self.health += health
        self.items.extend(items)
