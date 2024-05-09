import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from dialogue import Translate
from npc_manager import ask_question
from player import Player
from quest_manager import QuestManager
from config import *

dp = Dispatcher()
players = {}
quest_managers = {}
asked_questions = {}
translate = Translate()


@dp.message(CommandStart())
async def start_quest(message: Message) -> None:
    if message.from_user.id not in players.keys():
        players[message.from_user.id] = Player()
        quest_managers[message.from_user.id] = QuestManager(player=players[message.from_user.id])
    asked_questions[message.from_user.id] = False
    quest_description, markup = quest_managers[message.from_user.id].make_choice()

    await message.answer(text=quest_description, reply_markup=markup)


@dp.message()
async def answer_question(message: Message):
    global asked_questions
    if asked_questions[message.from_user.id]:
        translation = translate.tat2rus(message.text)
        print(translation)
        answer = ask_question(translation)
        await message.answer(text=answer)


@dp.callback_query(F.data != "ask_question")
async def apply_choice(callback: types.CallbackQuery):
    global asked_questions
    if callback.data == 'ask':
        asked_questions[callback.from_user.id] = True
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(text="Ну, спрашивай")
    else:
        for choice in quest_managers[callback.from_user.id].current_quest.choices:
            asked_questions[callback.from_user.id] = False
            if choice.choice_id == callback.data:
                quest_managers[callback.from_user.id].current_quest_id = choice.to_quest
                quest_description, markup = quest_managers[callback.from_user.id].make_choice()
                players[callback.from_user.id].apply_changes(**choice.result)
                await callback.message.edit_reply_markup(reply_markup=None)
                await callback.message.answer(text=choice.text)
                await callback.message.answer(text=quest_description, reply_markup=markup)
                break


# @dp.callback_query()
# async def go_to(callback: types.CallbackQuery):
#     quest_description, markup = quest_managers[callback.from_user.id].make_choice()
#     await callback.message.edit_reply_markup(reply_markup=None)
#     await callback.message.answer(text=quest_description, reply_markup=markup)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
