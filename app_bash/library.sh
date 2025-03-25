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
  local logfile="$1"
  local level="$2"
  local message="$3"
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  local msg="[$timestamp] ${level^^}: $message"

  echo "$msg" >> "$logfile"

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
  local logfile="$2"
  local success_msg="$3"
  local error_msg="$4"

  Logging "info" "Выполняет команду: $command"

  local output=$(bash -c "$command" 2>&1)
  local exit_code=$?

  if [ "$exit_code" -eq 0 ]; then
    Logging "$logfile" "success" "$success_msg Вывод: '$output'"
  else
    Logging "$logfile" "error" "$error_msg Вывод: $output"
    exit 1
  fi
}

PingVPN() {
  local logfile="$1"
  local net_space="$2"
  local self_ip="$3"
  local delay="$4"
  local error=0

  while true; do
    res=$(ip netns exec "$net_space" curl -s ifconfig.me)

    if [ "$res" != "$self_ip" ]; then
      local error=1
      Logging "$logfile" "error" "Мой ip: $res"
      break
    fi

    Logging "$logfile" "success" "Мой ip: $res"
    sleep "$delay"
  done

  echo "$error"
}

export -f