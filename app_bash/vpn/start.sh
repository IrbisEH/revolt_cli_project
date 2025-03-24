#!/usr/bin/env bash

CONFIGURE_SCRIPT="/home/irbis-eh/revolt_cli/app_bash/vpn/configure.sh"


. /home/irbis-eh/revolt_cli/app_bash/vpn/.env
. /home/irbis-eh/revolt_cli/app_bash/logging.sh

# Проверяем права пользователя
if [ "$EUID" -ne 0 ]; then
  Logging "error" "Ошибка! Скрипт запущен без прав root пользователя."
  exit 1
fi

.CONFIGURE_SCRIPT