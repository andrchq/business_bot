"""Synchronize the Telegram bot profile description with the active mode."""

import argparse
import asyncio

from aiogram import Bot

from config import BOT_TOKEN


DESCRIPTIONS = {
    "business": (
        "Добро пожаловать в Business Tool!\n\n"
        "Этот бот помогает предпринимателям находить точки роста, улучшать продажи, "
        "выстраивать воронки, рекламу и трафик. Выберите нужный раздел, чтобы получить "
        "практические рекомендации, инструменты и шаблоны для развития бизнеса."
    ),
    "redirect": (
        "Добро пожаловать в простовпн\n"
        "С нами можете забыть о всех проблемах с интернетом. Наш бот ускоряет работу "
        "многих сервисов и создает комфорт в интернете.\n\n"
        "У нас есть приятные бонусы для новых пользователей.\n"
        "Для начала нажмите кнопку снизу."
    ),
}


async def update_description(mode: str) -> None:
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.set_my_description(description=DESCRIPTIONS[mode])
    finally:
        await bot.session.close()


def parse_args() -> str:
    parser = argparse.ArgumentParser(
        description="Update the Telegram bot profile description for a bot mode."
    )
    parser.add_argument("mode", choices=DESCRIPTIONS)
    return parser.parse_args().mode


if __name__ == "__main__":
    asyncio.run(update_description(parse_args()))
