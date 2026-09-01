#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="${BUSINESS_BOT_PROJECT_DIR:-/root/business_bot}"
if [ "$#" -eq 0 ]; then set -- статус; fi
exec bash "$PROJECT_DIR/scripts/service_cli.sh" bus "$@"
