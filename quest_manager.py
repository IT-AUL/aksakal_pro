import json

from choice import Choice
from quest import Quest


def load_quests(quests_file):
    with open(quests_file, encoding='utf-8') as file:
        quests = dict()
        for quest_json in json.load(file):
            quest_id = str(quest_json['quest_id'])
            description = str(quest_json['description'])
            choice = []
            for choice_json in quest_json['choices']:
                choice_id = str(choice_json['choice_id'])
                to_quest = str(choice_json['to_quest'])
                text = str(choice_json['text'])
                choice.append(Choice(choice_id, to_quest, text))
            quests[quest_id] = (Quest(quest_id, description, choice))
        return quests


class QuestManager:
    def __init__(self, quests_file):
        self.quests = load_quests(quests_file)
        self.current_quest_id = "welcome_quest"
        self.current_quest = self.quests[self.current_quest_id]

    def next_quest(self):
        self.current_quest = self.quests[self.current_quest_id]
        return self.current_quest.description, self.current_quest.choices