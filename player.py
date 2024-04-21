class Player:
    def __init__(self):
        self.health = 50
        self.name = "Алмаз"
        self.items = []

    def apply_changes(self, health=0, items=None):
        """
        Apply changes to the player's health and stats
        :param health: How much to increase the health of the player
        :param items: List of items to add to the player's items
        :return: None
        """
        if items is None:
            items = []
        self.health += health
        self.items.extend(items)
