import json

from aiogram.utils.keyboard import InlineKeyboardBuilder

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
        self.current_choices = ["0", "1"]

    def next_quest(self):
        self.current_quest = self.quests[self.current_quest_id]
        return self.current_quest.description, self.current_quest.choices

    def make_choice(self):
        quest_description, choices = self.next_quest()
        builder = InlineKeyboardBuilder()
        for choice in choices:
            print(choice.choice_id)
            builder.button(text=choice.text, callback_data=choice.choice_id)
        builder.adjust(len(choices))
        self.current_choices = [choice.choice_id for choice in choices]
        return quest_description, builder.as_markup()
