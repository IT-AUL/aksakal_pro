import asyncio
import logging
import sys

from config import *
from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from player import Player
from quest_manager import QuestManager

dp = Dispatcher()
player = Player()
quest_manager = QuestManager(player=player)


@dp.message(CommandStart())
async def welcome(message: Message) -> None:
    quest_description, markup = quest_manager.make_choice()
    await message.answer(text=quest_description, reply_markup=markup)


@dp.callback_query(F.data.in_(quest_manager.current_choices))
async def execute_choice(callback: types.CallbackQuery):
    print(callback.data, callback.message)
    for choice in quest_manager.current_quest.choices:
        if choice.choice_id == callback.data:
            quest_manager.current_quest_id = choice.to_quest
            quest_description, markup = quest_manager.make_choice()
            player.apply_changes(**choice.result)
            await callback.message.edit_reply_markup(reply_markup=None)
            await callback.message.answer(text=choice.text)
            await callback.message.answer(text=quest_description, reply_markup=markup)
            print(player.health, player.items)
            break


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
