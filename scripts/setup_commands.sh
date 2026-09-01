#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${BUSINESS_BOT_PROJECT_DIR:-/root/business_bot}"
SCRIPTS_DIR="$PROJECT_DIR/scripts"
COMMAND_DIR="${BUSINESS_BOT_COMMAND_DIR:-/usr/local/bin}"

install_script() {
  local src="$1" dest="$COMMAND_DIR/$2"
  [ -f "$SCRIPTS_DIR/$src" ] || { echo "Ошибка: $src не найден в $SCRIPTS_DIR" >&2; exit 1; }
  mkdir -p "$COMMAND_DIR"
  tr -d '\r' < "$SCRIPTS_DIR/$src" > "$dest"
  chmod +x "$dest"
}

install_script "bus.sh" "bus"
echo "Готово! Команда bus доступна из любой директории."
