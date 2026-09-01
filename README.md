# Business Tool bot

Telegram-бот с навигацией по бизнес-диагностике, точкам роста, продажам, рекламе и практическим шаблонам.

## Быстрый деплой на сервер

На сервере с Docker Engine и Docker Compose v2:

```bash
git clone https://github.com/andrchq/business_bot.git /root/business_bot
cd /root/business_bot
cp .env.example .env
# укажите настоящий BOT_TOKEN в .env
sudo bash scripts/deploy.sh
```

Скрипт соберёт образ, запустит контейнер и установит команду `bus` в `/usr/local/bin`.

## Управление на сервере

Команда доступна из любой директории:

```bash
bus статус
bus запуск
bus остановка
bus перезапуск
bus логи
bus обновить
bus пересобрать
bus редирект
bus основной
bus очистка
bus помощь
```

Поддерживаются и английские варианты: `start`, `stop`, `restart`, `status`, `logs`, `update`, `rebuild`, `clean`, `help`.

## Режимы бота

По умолчанию в `.env` задан `BOT_MODE=business`: работает полное меню Business Tool.

Для включения бота-переходника на сервере выполните:

```bash
bus редирект
```

После этого `/start` отправляет изображение и одну красную кнопку `ОТКРЫТЬ`, ведущую в [@prstabot](https://t.me/prstabot). Текст подписи хранится в `handlers/start.py` в переменной `redirect_text` и поддерживает Telegram HTML, например `<b>` и `<code>`.

Для возврата к текущему бизнес-боту:

```bash
bus основной
```
