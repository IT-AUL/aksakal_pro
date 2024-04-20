import asyncio
import logging
import sys

from config import *
from aiogram import Bot, Dispatcher, F, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from quest_manager import QuestManager

dp = Dispatcher()
quest_manager = QuestManager('quest.json')

current_choices = []


@dp.message(CommandStart())
async def welcome(message: Message) -> None:
    global current_choices
    await make_choice(message)


async def make_choice(message: Message):
    quest_description, choices = quest_manager.next_quest()
    buttons = []
    builder = InlineKeyboardBuilder()
    for choice in choices:
        print(choice.choice_id)
        builder.button(text=choice.text, callback_data=choice.choice_id)
        # buttons.append([InlineKeyboardButton(text="XXX", callback_data=choice.choice_id)])
        current_choices.append(choice.choice_id)
    # markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer(text=quest_description, reply_markup=builder.as_markup())


@dp.callback_query(F.data.in_(current_choices))
async def execute_choice(callback: types.CallbackQuery):
    print(callback.data, callback.message)
    for choice in quest_manager.current_quest.choices:
        if choice.choice_id == callback.data:
            quest_manager.current_quest_id = choice.to_quest
            await callback.message.edit_reply_markup(reply_markup=None)
            await callback.message.answer(text=choice.text)
            await make_choice(callback.message)
            break


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
