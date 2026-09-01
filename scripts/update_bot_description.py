"""Synchronize the Telegram bot profile with the active mode."""

import argparse
import asyncio
from pathlib import Path
import sys

from aiogram import Bot
from aiogram.types import FSInputFile, InputProfilePhotoStatic

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

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

PROFILE_PHOTOS = {
    "business": PROJECT_DIR / "images" / "avatar.png",
    "redirect": PROJECT_DIR / "images" / "redirect_avatar.png",
}


async def update_profile(mode: str) -> None:
    photo_path = PROFILE_PHOTOS[mode]
    if not photo_path.is_file():
        raise FileNotFoundError(f"Profile photo not found: {photo_path}")

    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.set_my_profile_photo(
            photo=InputProfilePhotoStatic(photo=FSInputFile(photo_path))
        )
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
    asyncio.run(update_profile(parse_args()))
