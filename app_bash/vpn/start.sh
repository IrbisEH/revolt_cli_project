#!/usr/bin/env bash

# start.sh

Logging "info" "Запускаю сервис xl2tpd."
ip netns exec $VPN_NAMESPACE xl2tpd -c /etc/xl2tpd/xl2tpd.conf -D > $XL2TPD_LOG_FILE 2>&1 &
sleep 5

Logging "info" "Перезагружаю ipsec."
ip netns exec $VPN_NAMESPACE ipsec restart
sleep 1

Logging "info" "Включаю ipsec."
ip netns exec $VPN_NAMESPACE ipsec up $VPN_NAME
sleep 1

Logging "info" "Включаю ipsec."
ip netns exec $VPN_NAMESPACE ipsec up $VPN_NAME
sleep 1

Logging "info" "Отправляю сигнал в xl2tpd"
ip netns exec $VPN_NAMESPACE bash -c "echo 'c $VPN_NAME' > /var/run/xl2tpd/l2tp-control"
sleep 3

Logging "info" "Настраиваю маршруты."
ip netns exec $VPN_NAMESPACE ip route del default via $DEFAULT_GATEWAY_VPN_NS || true
ip netns exec $VPN_NAMESPACE ip route add default dev ppp0 || true
ip netns exec $VPN_NAMESPACE ip route add $VPN_SERVER_IP via $DEFAULT_GATEWAY_VPN_NS dev $INTFS_VPN_NS || true

Logging "success" "VPN запущен."