import json
import re

from aiogram.utils.keyboard import InlineKeyboardBuilder

from choice import Choice
from player import Player
from quest import Quest


def load_quests(quests_file):
    """
    Load quests from *quest_file* file and return them as a list
    :param quests_file: Quests file path
    :return: List of quests
    """
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
                conditions = [str(condition) for condition in choice_json['conditions']]
                result = dict(choice_json['result'])
                choice.append(Choice(choice_id, to_quest, text, conditions, result))
            quests[quest_id] = (Quest(quest_id, description, choice))
        return quests


class QuestManager:
    player: Player

    def __init__(self, quests_file='quest.json', player=None):
        self.quests = load_quests(quests_file)
        self.current_quest_id = "q0"
        self.current_quest = self.quests[self.current_quest_id]
        self.current_choices = [choice.choice_id for choice in self.current_quest.choices]
        self.player = player

    def get_current_quest(self):
        self.current_quest = self.quests[self.current_quest_id]
        return self.current_quest.description, self.current_quest.choices

    def make_choice(self):
        quest_description, choices = self.get_current_quest()
        quest_description = self.replace_variables(quest_description)
        builder = InlineKeyboardBuilder()
        for choice in choices:
            if choice.conditions is None or len(choice.conditions) == 0 or any(
                    [self.replace_variables_and_evaluate(condition) for condition in choice.conditions]):
                choice.text = self.replace_variables(choice.text)
                builder.button(text=choice.text, callback_data=choice.choice_id)
        builder.adjust(1, True)
        self.current_choices = [choice.choice_id for choice in choices]
        return quest_description, builder.as_markup()

    def replace_variables(self, string):
        pattern = r'\$(\w+)'
        matches = re.findall(pattern, string)
        for match in matches:
            if hasattr(self.player, match):
                value = str(getattr(self.player, match))
                string = string.replace(f'${match}', value)
        return string

    def replace_variables_and_evaluate(self, expression):
        pattern = r'\$(\w+)'
        matches = re.findall(pattern, expression)
        for match in matches:
            if hasattr(self.player, match):
                value = str(getattr(self.player, match))
                expression = expression.replace(f'${match}', value)
        return eval(expression)
