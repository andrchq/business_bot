import os
from aiogram.types import InputMediaPhoto, FSInputFile

IMAGES_DIR = "images"
DEFAULT_IMAGE = "avatar.png"  # Изображение по умолчанию, если нужного нет

def get_image_path(image_name: str) -> str:
    path = os.path.join(IMAGES_DIR, f"{image_name}.png")
    if os.path.exists(path):
        return path
        
    # Фоллбэк на изображение по умолчанию
    default_path = os.path.join(IMAGES_DIR, DEFAULT_IMAGE)
    if os.path.exists(default_path):
        return default_path
        
    return ""

def get_menu_media(image_name: str, caption: str, parse_mode: str = "HTML") -> InputMediaPhoto:
    image_path = get_image_path(image_name)
    if not image_path:
        # Fallback incase really nothing is found (shouldn't happen since avatar.png exists)
        image_path = os.path.join(IMAGES_DIR, DEFAULT_IMAGE)
        
    return InputMediaPhoto(
        media=FSInputFile(image_path),
        caption=caption,
        parse_mode=parse_mode
    )

async def safe_edit_menu(callback, image_name: str, caption: str, reply_markup):
    """
    Безопасное редактирование меню: если сообщение было текстовым (без медиа), 
    edit_media выдаст ошибку TelegramBadRequest. В таком случае удаляем сообщение и присылаем новое.
    """
    from aiogram.exceptions import TelegramBadRequest
    media_obj = get_menu_media(image_name, caption)
    try:
        await callback.message.edit_media(media=media_obj, reply_markup=reply_markup)
    except TelegramBadRequest as e:
        # Либо "message is not modified", либо "there is no media in the message to edit"
        if "not modified" in str(e).lower():
            pass # Игнорируем, если ничего не изменилось
        else:
            try:
                await callback.message.delete()
            except:
                pass
            await callback.message.answer_photo(
                photo=media_obj.media,
                caption=media_obj.caption,
                parse_mode=media_obj.parse_mode,
                reply_markup=reply_markup
            )
    except Exception:
        # Fallback for any other weird errors
        try:
            await callback.message.delete()
        except:
            pass
        await callback.message.answer_photo(
            photo=media_obj.media,
            caption=media_obj.caption,
            parse_mode=media_obj.parse_mode,
            reply_markup=reply_markup
        )

