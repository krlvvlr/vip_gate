import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, ChatJoinRequest
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
VIP_CHAT_ID = int(os.getenv("VIP_CHAT_ID"))
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


def is_vip_status(status: str) -> bool:
    return status in ["member", "administrator", "creator"]


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Бот активен.\n"
        "Подай заявку в канал по ссылке и я проверю доступ."
    )


@dp.chat_join_request(F.chat.id == TARGET_CHAT_ID)
async def join_request_handler(join_request: ChatJoinRequest):
    user_id = join_request.from_user.id

    try:
        vip_member = await bot.get_chat_member(
            VIP_CHAT_ID,
            user_id
        )

        if is_vip_status(vip_member.status):

            await bot.approve_chat_join_request(
                TARGET_CHAT_ID,
                user_id
            )

            logging.info(
                f"APPROVED {user_id}"
            )

        else:

            await bot.decline_chat_join_request(
                TARGET_CHAT_ID,
                user_id
            )

            logging.info(
                f"DECLINED {user_id}"
            )

    except Exception as e:

        logging.error(
            f"ERROR {user_id}: {e}"
        )

        try:
            await bot.decline_chat_join_request(
                TARGET_CHAT_ID,
                user_id
            )
        except:
            pass


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
