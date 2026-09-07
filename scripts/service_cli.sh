#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${BUSINESS_BOT_PROJECT_DIR:-/root/business_bot}"
COMPOSE_FILE="${BUSINESS_BOT_COMPOSE_FILE:-docker-compose.yml}"
SCOPE="${1:-bus}"
ACTION="${2:-help}"
shift 2 2>/dev/null || true

RESET='\033[0m'; DIM='\033[2m'; GREEN='\033[1;32m'; RED='\033[1;31m'; YELLOW='\033[1;33m'
case "$SCOPE" in
  bus) COLOR='\033[1;35m'; TITLE='BUSINESS TOOL'; SERVICES=(bot) ;;
  *) printf "Неизвестная область: %s\n" "$SCOPE" >&2; exit 1 ;;
esac

clear_screen() { printf '\033[2J\033[H'; }
line() { printf "${COLOR}%-10s${RESET} ${DIM}%s${RESET}\n" "$SCOPE" "$1"; }
ok() { printf "${GREEN}✓${RESET} %s\n" "$*"; }
info() { printf "${COLOR}›${RESET} %s\n" "$*"; }
warn() { printf "${YELLOW}!${RESET} %s\n" "$*" >&2; }
fail() { printf "${RED}×${RESET} %s\n" "$*" >&2; exit 1; }
has() { command -v "$1" >/dev/null 2>&1; }

compose() {
  if has docker && docker compose version >/dev/null 2>&1; then
    docker compose -f "$COMPOSE_FILE" "$@"
  elif has docker-compose; then
    docker-compose -f "$COMPOSE_FILE" "$@"
  else
    fail "Docker Compose не установлен"
  fi
}

run_hidden() {
  local label="$1" output status pid frame=0 started_at elapsed
  local frames=('⠋' '⠙' '⠹' '⠸' '⠼' '⠴' '⠦' '⠧' '⠇' '⠏')
  shift
  output="$(mktemp)"
  started_at=$SECONDS
  "$@" >"$output" 2>&1 &
  pid=$!
  if [ -t 1 ]; then
    while kill -0 "$pid" 2>/dev/null; do
      printf "\r${COLOR}%s${RESET} %s ${DIM}[%02d:%02d]${RESET}" \
        "${frames[$((frame % ${#frames[@]}))]}" "$label" "$(((SECONDS - started_at) / 60))" "$(((SECONDS - started_at) % 60))"
      frame=$((frame + 1))
      sleep 0.12
    done
    printf '\r\033[K'
  else
    info "$label"
  fi
  if wait "$pid"; then
    elapsed=$((SECONDS - started_at))
    rm -f "$output"
    ok "$label [$((elapsed / 60)) мин $((elapsed % 60)) сек]"
    return 0
  else
    status=$?
  fi
  printf "${RED}× %s${RESET}\n" "$label" >&2
  printf '\n%s\n' "──────── полный текст ошибки ────────" >&2
  cat "$output" >&2
  printf '%s\n\n' "────────────────────────────────────" >&2
  rm -f "$output"
  return "$status"
}

show_changed_files() {
  local before="$1" after="$2" changes count status file target_file label
  changes="$(git diff --name-status "$before" "$after")"
  if [ -z "$changes" ]; then
    ok "Изменённых файлов нет"
    return
  fi
  count="$(printf '%s\n' "$changes" | wc -l | tr -d ' ')"
  printf "\n${COLOR}ИЗМЕНЁННЫЕ ФАЙЛЫ: %s${RESET}\n" "$count"
  while IFS=$'\t' read -r status file target_file; do
    case "${status:0:1}" in
      A) label="добавлен" ;;
      M) label="изменён" ;;
      D) label="удалён" ;;
      R) label="переименован"; file="$file → $target_file" ;;
      *) label="$status" ;;
    esac
    printf "  ${DIM}%-12s${RESET} %s\n" "$label" "$file"
  done <<< "$changes"
  printf '\n'
}

usage() {
  printf "${COLOR}%s${RESET} — %s\n\n" "$SCOPE" "$TITLE"
  cat <<EOF
Использование: ${SCOPE} <команда>

  запуск       Запустить сервисы
  остановка    Остановить сервисы
  перезапуск   Перезапустить сервисы
  статус       Показать состояние
  логи         Показать живые логи
  обновить     Скачать код, собрать и запустить
  пересобрать  Пересобрать и перезапустить
  редирект     Включить версию бота-переходника
  основной     Включить основную версию бота
  очистка      Удалить неиспользуемые данные Docker
  помощь       Показать эту справку

Допустимы также: start, stop, restart, status, logs, update, rebuild, redirect, main, clean, help
EOF
}

checklist() {
  local expected="${1:-running}" failed=0 service state running_services
  printf "\n${COLOR}ЧЕК-ЛИСТ${RESET}\n"
  if ! run_hidden "Проверка конфигурации Docker Compose" compose config; then
    failed=1
  fi

  running_services="$(compose ps --status running --services 2>/dev/null || true)"
  for service in "${SERVICES[@]}"; do
    state="$(printf '%s\n' "$running_services" | grep -Fx "$service" || true)"
    if { [ "$expected" = running ] && [ "$state" = "$service" ]; } || { [ "$expected" = stopped ] && [ -z "$state" ]; }; then
      ok "Бот: $([ "$expected" = running ] && echo 'запущен' || echo 'остановлен')"
    else
      printf "${RED}×${RESET} Бот: неверное состояние\n"
      failed=1
    fi
  done

  if [ "$failed" -ne 0 ]; then
    if [ "$expected" = running ]; then
      printf "\n${RED}──── последние логи бота ────${RESET}\n" >&2
      compose logs --tail 40 "${SERVICES[@]}" >&2 || true
      printf "${RED}──────────────────────────────${RESET}\n" >&2
    fi
    fail "Чек-лист завершён с ошибками"
  fi
  printf '\n'; ok "Команда выполнена полностью"
}

update_code() {
  has git || fail "Git не установлен"
  if git status --porcelain --untracked-files=no | grep -q .; then
    fail "Есть локальные изменения. Сохраните их через commit или stash"
  fi
  run_hidden "Получение информации об обновлениях" git fetch --prune origin
  local current target updated
  current="$(git rev-parse HEAD)"
  target="$(git rev-parse '@{u}' 2>/dev/null || git rev-parse origin/main)"
  if [ "$current" = "$target" ]; then
    ok "Код уже обновлён"
  else
    run_hidden "Скачивание обновления" git pull --ff-only
  fi
  updated="$(git rev-parse HEAD)"
  show_changed_files "$current" "$updated"
}

set_bot_mode() {
  local mode="$1" temp_file
  [ -f .env ] || fail "Файл .env не найден"
  temp_file="$(mktemp)"
  awk -v mode="$mode" '
    BEGIN { found = 0 }
    /^[[:space:]]*BOT_MODE[[:space:]]*=/ {
      if (!found) {
        print "BOT_MODE=" mode
        found = 1
      }
      next
    }
    { print }
    END {
      if (!found) print "BOT_MODE=" mode
    }
  ' .env > "$temp_file"
  mv "$temp_file" .env
}

show_mode_description() {
  local mode="$1"
  printf "\n${COLOR}ОПИСАНИЕ БОТА${RESET}\n\n"
  case "$mode" in
    business)
      cat <<'EOF'
Добро пожаловать в Business Tool!

Этот бот помогает предпринимателям находить точки роста, улучшать продажи,
выстраивать воронки, рекламу и трафик. Выберите нужный раздел, чтобы получить
практические рекомендации, инструменты и шаблоны для развития бизнеса.
EOF
      ;;
    redirect)
      cat <<'EOF'
Добро пожаловать в простовпн
С нами можете забыть о всех проблемах с интернетом. Наш бот ускоряет работу
многих сервисов и создает комфорт в интернете.

У нас есть приятные бонусы для новых пользователей.
Для начала нажмите кнопку снизу.
EOF
      ;;
  esac
  printf '\n'
}

switch_mode() {
  local mode="$1" label="$2"
  set_bot_mode "$mode"
  ok "Выбран режим: $label"
  show_mode_description "$mode"
  run_hidden "Переключение версии бота" compose up -d --force-recreate "${SERVICES[@]}"
  checklist running
}

clear_screen
cd "$PROJECT_DIR" 2>/dev/null || fail "Каталог проекта не найден: $PROJECT_DIR"
[ -f "$COMPOSE_FILE" ] || fail "Compose-файл не найден: $COMPOSE_FILE"
line "$TITLE · $ACTION"

case "$ACTION" in
  запуск|start) run_hidden "Запуск сервисов" compose up -d "${SERVICES[@]}"; checklist running ;;
  остановка|stop) run_hidden "Остановка сервисов" compose stop "${SERVICES[@]}"; checklist stopped ;;
  перезапуск|restart) run_hidden "Перезапуск сервисов" compose restart "${SERVICES[@]}"; checklist running ;;
  статус|status) checklist running ;;
  логи|logs) compose logs -f --tail "${1:-120}" "${SERVICES[@]}" ;;
  обновить|update)
    update_code
    run_hidden "Обновление серверной команды" bash "$PROJECT_DIR/scripts/setup_commands.sh"
    run_hidden "Сборка сервисов" compose build "${SERVICES[@]}"
    run_hidden "Запуск обновлённого сервиса" compose up -d --remove-orphans "${SERVICES[@]}"
    checklist running
    ;;
  пересобрать|rebuild)
    run_hidden "Сборка сервисов" compose build "${SERVICES[@]}"
    run_hidden "Пересоздание сервиса" compose up -d --force-recreate "${SERVICES[@]}"
    checklist running
    ;;
  редирект|redirect) switch_mode redirect "редирект" ;;
  основной|main) switch_mode business "основной" ;;
  очистка|clean)
    run_hidden "Очистка остановленных контейнеров" docker container prune -f
    run_hidden "Очистка неиспользуемых образов" docker image prune -f
    run_hidden "Очистка кэша сборки старше 7 дней" docker builder prune -f --filter until=168h
    checklist running
    ;;
  помощь|help|--help|-h) usage ;;
  *) usage; fail "Неизвестная команда: $ACTION" ;;
esac
