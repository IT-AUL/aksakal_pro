class Choice:
    def __init__(self, choice_id, to_quest, text, result):
        self.choice_id: str = choice_id
        self.to_quest: str = to_quest
        self.text: str = text
        self.result: str = result
