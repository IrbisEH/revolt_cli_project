#!/usr/bin/env bash

Logging "info" "Скрипт очистки конфигурация VPN запущен."

# Проверяем форвардинг
if [ $(sysctl -n net.ipv4.ip_forward) -eq 1 ]; then
  Execute "sysctl -w net.ipv4.ip_forward=0" \
          "Форвардинг IPv4-пакетов успешно выключен." \
          "Ошибка! Не удалось выключить форвардинг IPv4-пакетов."
fi

# Проверяем правило маршрутизации в ufw, удаляем
while true; do
  FIRST=$(ufw status numbered | grep "ALLOW FWD" | grep "$INTFS_DEFAULT_NS" | head -n 1)

  if [ -z "$FIRST" ]; then
    break
  fi

  RULE_NUMBER=$(echo "$FIRST" | cut -d ']' -f1 | tr -d '[] ')

  Execute "ufw --force delete $RULE_NUMBER" \
          "Правило маршрутизации $RULE_NUMBER успешно удалено." \
          "Ошибка! Произошла ошибка при удалении правило маршрутизации $RULE_NUMBER."
done

# Проверяем интерфейс, удаляем
if ip netns list | grep -q "^$VPN_NAMESPACE"; then
  Execute "ip netns delete $VPN_NAMESPACE" \
          "Сетевое пространство $VPN_NAMESPACE успешно удаленно." \
          "Ошибка! Произошла ошибка при удалении сетевого пространства $VPN_NAMESPACE."
fi

# Проверяем интерфейс, удаляем
if ip link show "$INTFS_DEFAULT_NS" > /dev/null 2>&1; then
  Execute "ip link delete $INTFS_DEFAULT_NS" \
          "Интерфейс $INTFS_DEFAULT_NS успешно удален." \
          "Ошибка! Произошла ошибка при удалении интерфейса $INTFS_DEFAULT_NS."
fi

# Проверяем правило NAT, удаляем
if iptables -t nat -C POSTROUTING -s "$SOURCE_SUBNET" -o "$OUT_INTERFACE" -j MASQUERADE 2>/dev/null; then
    Execute "iptables -t nat -D POSTROUTING -s $SOURCE_SUBNET -o $OUT_INTERFACE -j MASQUERADE" \
            "Существующее правило NAT для $SOURCE_SUBNET успешно удалено." \
            "Ошибка! Произошла ошибка при удалении правила NAT для $SOURCE_SUBNET."
fi

# TODO: Надо ли чистить файлы?

Logging "info" "Скрипт очистки конфигурация VPN завершен."