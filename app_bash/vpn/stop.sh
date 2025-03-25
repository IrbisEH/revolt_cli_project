#!/usr/bin/env bash

# stop.sh

LOG_FILE="$1"

Logging "$LOG_FILE" "info" "Скрипт shop.sh запущен."

ip netns exec $VPN_NAMESPACE ipsec stop > /dev/null 2>&1;
ip netns exec $VPN_NAMESPACE pkill xl2tpd > /dev/null 2>&1
service xl2tpd stop > /dev/null 2>&1

ip netns exec $VPN_NAMESPACE rm -f /var/run/xl2tpd/l2tp-control > /dev/null 2>&1
ip netns exec $VPN_NAMESPACE mkdir -p /var/run/xl2tpd > /dev/null 2>&1
ip netns exec $VPN_NAMESPACE touch /var/run/xl2tpd//l2tp-control > /dev/null 2>&1

Logging "$LOG_FILE" "info" "Скрипт shop.sh завершен."