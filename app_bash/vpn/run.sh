#!/usr/bin/env bash

# TODO: реализовать таймауты
# TODO: реализовать относительные пути
# TODO: убрать лог файлы из env забить из в структуру приложения
# TODO: Подвисает тест
# TODO: Добавить парсинг аргуметов, например script.sh --start --stop --test --clean

TIMEOUT_IN_SECONDS=5

COMMON_LOG="/home/irbis-eh/revolt_cli/app_bash/vpn/logs/common.log"
XL2TPD_LOG="/home/irbis-eh/revolt_cli/app_bash/vpn/logs/xl2tpd.log"
IPSEC_LOG="/home/irbis-eh/revolt_cli/app_bash/vpn/logs/ipsec.log"

CONFIGURE_SCRIPT="/home/irbis-eh/revolt_cli/app_bash/vpn/configure.sh"
CLEAN_UP_SCRIPT="/home/irbis-eh/revolt_cli/app_bash/vpn/clean_up.sh"
START_SCRIPT="/home/irbis-eh/revolt_cli/app_bash/vpn/start.sh"
STOP_SCRIPT="/home/irbis-eh/revolt_cli/app_bash/vpn/stop.sh"

DOMAINS_LIST="/home/irbis-eh/revolt_cli/app_bash/vpn/domains.list"

. /home/irbis-eh/revolt_cli/app_bash/vpn/.env
. /home/irbis-eh/revolt_cli/app_bash/library.sh

CleanUp() {
  source "$STOP_SCRIPT" "$COMMON_LOG"
  source "$CLEAN_UP_SCRIPT" "$COMMON_LOG"
}

# Проверяем права пользователя
if [ "$EUID" -ne 0 ]; then
  Logging "$COMMON_LOG" "error" "Ошибка! Скрипт запущен без прав root пользователя."
  exit 1
fi

if [ ! -f "$CLEAN_UP_SCRIPT" ]; then
    Logging "$COMMON_LOG" "error" "Ошибка! Файл очистки $CONFIGURE_SCRIPT не найден."
    exit 1
fi

if [ ! -f "$CONFIGURE_SCRIPT" ]; then
    Logging "$COMMON_LOG" "error" "Ошибка! Файл конфигурации $CONFIGURE_SCRIPT не найден."
    exit 1
fi

trap CleanUp EXIT

source "$CLEAN_UP_SCRIPT" "$COMMON_LOG"
source "$CONFIGURE_SCRIPT" "$COMMON_LOG"
source "$STOP_SCRIPT" "$COMMON_LOG"
source "$START_SCRIPT" "$COMMON_LOG" "$IPSEC_LOG" "$XL2TPD_LOG" "$DOMAINS_LIST"

Logging "$COMMON_LOG" "info" "Запускаю тест."
PingVPN "$COMMON_LOG" "$VPN_NAMESPACE" "$VPN_SERVER_IP" 5