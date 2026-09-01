#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$PROJECT_DIR/.env"

fail() { printf 'Ошибка: %s\n' "$*" >&2; exit 1; }
command -v docker >/dev/null 2>&1 || fail "Docker не установлен. Установите Docker Engine и Docker Compose."
docker compose version >/dev/null 2>&1 || fail "Docker Compose v2 не установлен."
[ -f "$ENV_FILE" ] || fail "Не найден $ENV_FILE. Создайте его и задайте BOT_TOKEN."
grep -Eq '^BOT_TOKEN=.+$' "$ENV_FILE" || fail "В $ENV_FILE не задан BOT_TOKEN."

export BUSINESS_BOT_PROJECT_DIR="$PROJECT_DIR"
printf 'Развёртывание Business Tool из %s\n' "$PROJECT_DIR"
docker compose -f "$PROJECT_DIR/docker-compose.yml" up -d --build --remove-orphans
bash "$PROJECT_DIR/scripts/setup_commands.sh"
docker compose -f "$PROJECT_DIR/docker-compose.yml" ps
printf '\nГотово. Управление: bus статус, bus логи, bus обновить\n'
