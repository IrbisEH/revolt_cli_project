#!/usr/bin/env bash

# start.sh

LOG_FILE="$1"
IPSEC_LOG_FILE="$2"
XL2TPD_LOG_FILE="$3"
DOMAINS_LIST="$4"

Logging "$LOG_FILE" "info" "Запускаю сервис xl2tpd."
ip netns exec $VPN_NAMESPACE xl2tpd -c /etc/xl2tpd/xl2tpd.conf -D > "$XL2TPD_LOG_FILE" 2>&1 &
sleep 5

Logging "$LOG_FILE" "info" "Перезагружаю ipsec."
ip netns exec $VPN_NAMESPACE ipsec restart > "$IPSEC_LOG_FILE" 2>&1
sleep 1

Logging "$LOG_FILE" "info" "Включаю ipsec."
ip netns exec $VPN_NAMESPACE ipsec up $VPN_NAME > "$IPSEC_LOG_FILE" 2>&1
sleep 1

Logging "$LOG_FILE" "info" "Включаю ipsec."
ip netns exec $VPN_NAMESPACE ipsec up $VPN_NAME > "$IPSEC_LOG_FILE" 2>&1
sleep 1

Logging "$LOG_FILE" "info" "Отправляю сигнал в xl2tpd"
ip netns exec $VPN_NAMESPACE bash -c "echo 'c $VPN_NAME' > /var/run/xl2tpd/l2tp-control"
sleep 3

Logging "$LOG_FILE" "info" "Настраиваю маршруты."

ip netns exec $VPN_NAMESPACE ip route del default via $DEFAULT_GATEWAY_VPN_NS || true
ip netns exec $VPN_NAMESPACE ip route add default dev ppp0 || true
ip netns exec $VPN_NAMESPACE ip route add $VPN_SERVER_IP via $DEFAULT_GATEWAY_VPN_NS dev $INTFS_VPN_NS || true

while IFS= read -r domain; do
  [[ -z "$domain" || "$domain" = ~^# ]] && continue
  ip=$(dig +short "$domain")
  ip route add "$ip" via "$DEFAULT_GATEWAY_VPN_NS"
done < "$DOMAINS_LIST"

Logging "$LOG_FILE" "success" "VPN запущен."