#!/usr/bin/env bash

# library.sh

# Цветовые коды
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'          # Сброс цвета

# Функция для вывода сообщений
# $1 - уровень сообщения (info, success, error)
# $2 - текст сообщения
# $3 - путь к лог файлу

Logging() {
  local level="$1"
  local message="$2"
  local logfile="$3"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  local msg="[$timestamp] ${level^^}: $message"

  if [ -z "$logfile" ]; then
    local logfile=$LOG_FILE
  fi

  echo "$msg" >> "$LOG_FILE"

  case "$level" in
    "info")
      echo -e "${YELLOW} $msg${NC}"
      ;;
    "success")
      echo -e "${GREEN} $msg${NC}"
      ;;
    "error")
      echo -e "${RED} $msg${NC}"
      ;;
    *)
      echo -e "${YELLOW} $msg${NC}"
      ;;
  esac
}

Execute() {
  local command="$1"
  local success_msg="$2"
  local error_msg="$3"

  Logging "info" "Выполняет команду: $command"

  local output=$(bash -c "$command" 2>&1)
  local exit_code=$?

  if [ "$exit_code" -eq 0 ]; then
    Logging "success" "$success_msg Вывод: '$output'"
  else
    Logging "error" "$error_msg Вывод: $output"
    exit 1
  fi
}

export -f