#!/usr/bin/env bash

CONFIGURE_SCRIPT="/home/irbis-eh/revolt_cli/app_bash/vpn/configure.sh"
CLEAN_UP_SCRIPT="/home/irbis-eh/revolt_cli/app_bash/vpn/clean_up.sh"

. /home/irbis-eh/revolt_cli/app_bash/vpn/.env
. /home/irbis-eh/revolt_cli/app_bash/library.sh

# Проверяем права пользователя
if [ "$EUID" -ne 0 ]; then
  Logging "error" "Ошибка! Скрипт запущен без прав root пользователя."
  exit 1
fi

if [ ! -f "$CLEAN_UP_SCRIPT" ]; then
    Logging "error" "Ошибка! Файл очистки $CONFIGURE_SCRIPT не найден."
    exit 1
fi

if [ ! -f "$CONFIGURE_SCRIPT" ]; then
    Logging "error" "Ошибка! Файл конфигурации $CONFIGURE_SCRIPT не найден."
    exit 1
fi

source "$CLEAN_UP_SCRIPT"
source "$CONFIGURE_SCRIPT"