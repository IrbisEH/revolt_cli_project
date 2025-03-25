#!/usr/bin/env bash

. /home/irbis-eh/revolt_cli/app_bash/vpn/.env

ip netns exec $VPN_NAMESPACE ipsec stop
ip netns exec $VPN_NAMESPACE pkill xl2tpd
service xl2tpd stop

ip netns exec $VPN_NAMESPACE rm -f /var/run/xl2tpd/l2tp-control
ip netns exec $VPN_NAMESPACE mkdir -p /var/run/xl2tpd
ip netns exec $VPN_NAMESPACE touch /var/run/xl2tpd//l2tp-control

Logging "info" "Скрипт shop.sh завершен."