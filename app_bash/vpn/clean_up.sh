#!/usr/bin/env bash

Logging "info" "Скрипт очистки конфигурация VPN запущен."

# Проверяем форвардинг
if [ $(sysctl -n net.ipv4.ip_forward) -eq 1 ]; then
  Execute "sysctl -w net.ipv4.ip_forward=0" \
          "Форвардинг IPv4-пакетов успешно выключен." \
          "Ошибка! Не удалось выключить форвардинг IPv4-пакетов."
fi

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
            "Ошибка! Не удалось удалить правило NAT для $SOURCE_SUBNET."
fi


Logging "info" "Скрипт очистки конфигурация VPN завершен."



## Проверяем и если нет создаем интерфейс
#if ip link show "$VETH_INTFS_DEFAULT_NS" > /dev/null 2>&1;then
#  ip link delete "$VETH_INTFS_DEFAULT_NS"
#
#
#  # Проверяем тип интерфейса
#  intfs_type=$(ip link show "$VETH_INTFS_DEFAULT_NS" | grep -oP '(?<=link/)\w+')
#
#  if [ "$infs_type" != "veth" ]; then
#    Logging "error" "Ошибка! Интерфейс $VETH_INTFS_DEFAULT_NS уже существует, но его тип не соответствует. Текущий тип - $intfs_type."
#    exit 1
#  fi
#
#  # Проверяем имя парного интерфейса
#  peer_name=$(ip -d link show "$VETH_INTFS_DEFAULT_NS" | grep -oP "(?<=veth peer ifindex \d+ name )\w+)")
#
#  if [ -z "$peer_name" ] || [ "$peer_name" != "$VETH_INTFS_VASE_NS" ]; then
#    Logging "error" "Ошибка! Интерфейс $VETH_INTFS_DEFAULT_NS уже существует, но имя парного интерфейса не соответствует. Текущее имя - $peer_name."
#    exit 1
#  fi
#
#  Logging "info" "Интерфейс $VETH_INTFS_DEFAULT_NS уже существует и соответствует конфигурации."
#
#else
#  ip link add "$VETH_INTFS_DEFAULT_NS" type veth peer name "$VETH_INTFS_VASE_NS."
#
#    if [ $? -eq 0 ];then
#      Logging "success" "Интерфейс $VETH_INTFS_DEFAULT_NS успешно создан."
#    else
#      Logging "error"  "Ошибка при создании интерфейса $VETH_INTFS_DEFAULT_NS!"
#      exit 1
#  fi
#fi