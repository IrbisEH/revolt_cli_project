#!/usr/bin/env bash

Logging "info" "Скрипт конфигурация VPN запущен."

# Создать виртуальное сетевое пространство
Execute "ip netns add $VPN_NAMESPACE" \
        "Сетевое пространство $VPN_NAMESPACE успешно создано." \
        "Ошибка! Произошла ошибка при создании сетевого пространства $VPN_NAMESPACE."

# Создать veth интерфейс
Execute "ip link add "$INTFS_DEFAULT_NS" type veth peer name $INTFS_VPN_NS" \
        "Интерфейс $INTFS_DEFAULT_NS и парный интерфейс $INTFS_VPN_NS успешно созданы." \
        "Ошибка! Произошла ошибка при создании интерфейса $VETH_INTFS_DEFAULT_NS."

# Привязать ip адрес к интерфейсу
Execute "ip addr add $IP_DEFAULT_NS dev $INTFS_DEFAULT_NS" \
        "Ip адрес $IP_DEFAULT_NS привязан к интерфейсу $INTFS_DEFAULT_NS." \
        "Ошибка! Произошла ошибка при привязке ip адреса $IP_DEFAULT_NS к интерфейсу $INTFS_DEFAULT_NS."

# Включить интерфейс
Execute "ip link set $INTFS_DEFAULT_NS up" \
        "Интерфейс $INTFS_DEFAULT_NS успешно запущен." \
        "Ошибка! Произошла ошибка при запуске интерфейса $INTFS_DEFAULT_NS."

# Привязываем парный интерфейс к виртуальному сетевому пространству
Execute "ip link set $INTFS_VPN_NS netns $VPN_NAMESPACE" \
        "Парный интерфейс $INTFS_VPN_NS привязан к сетевому пространству $VPN_NAMESPACE успешно." \
        "Ошибка! Произошла ошибка при парного интерфейса $INTFS_VPN_NS к сетевому пространству $VPN_NAMESPACE."

# Привязать ip адрес к интерфейсу
Execute "ip netns exec $VPN_NAMESPACE ip addr add $IP_VPN_NS dev $INTFS_VPN_NS" \
        "Ip адрес $IP_VPN_NS привязан к интерфейсу $INTFS_VPN_NS." \
        "Ошибка! Произошла ошибка при привязке ip адреса $IP_VPN_NS к интерфейсу $INTFS_VPN_NS."

# Включить парный интерфейс интерфейс
Execute "ip netns exec $VPN_NAMESPACE ip link set $INTFS_VPN_NS up" \
        "Интерфейс $INTFS_VPN_NS успешно запущен." \
        "Ошибка! Произошла ошибка при запуске интерфейса $INTFS_VPN_NS."

# Включить форвардинг IPv4-пакетов
Execute "sysctl -w net.ipv4.ip_forward=1" \
        "Форвардинг IPv4-пакетов включен" \
        "Ошибка! Произошла ошибка при включении форвардинга IPv4-пакетов."

# Назначить шлюз по умолчанию для виртуального сетевого пространства
Execute "ip netns exec $VPN_NAMESPACE ip route add default via $DEFAULT_GATEWAY_VPN_NS" \
        "Шлюз по умолчанию $DEFAULT_GATEWAY_VPN_NS для сетевого пространства $VPN_NAMESPACE успешно настроен." \
        "Ошибка! Произошла ошибка при настройки шлюза по умолчанию $DEFAULT_GATEWAY_VPN_NS для сетевого пространства $VPN_NAMESPACE."

# Добавить правило NAT
Execute "iptables -t nat -A POSTROUTING -s $SOURCE_SUBNET -o $OUT_INTERFACE -j MASQUERADE" \
        "Правило NAT успешно добавлено." \
        "Ошибка! Произошла ошибка при добавлении правила NAT."

# Добавить правило маршрутизации в ufw
Execute "ufw route allow in on $INTFS_DEFAULT_NS out on $OUT_INTERFACE" \
        "Правило форвардинга 1 для UFW настроено" \
        "Ошибка! Произошла ошибка при добавлении правила форвардинга 1 для UFW."

Execute "ufw route allow in on $OUT_INTERFACE out on $INTFS_DEFAULT_NS" \
        "Правило форвардинга 2 для UFW настроено" \
        "Ошибка! Произошла ошибка при добавлении правила форвардинга 2 для UFW."

# Настроить DNS сервер
Execute "sed -i 's/nameserver/nameserver 8.8.8.8/' /etc/resolv.conf" \
        "DNS сервер успешно настроен" \
        "Ошибка! Произошла ошибка при настройке DNS сервера."

# Настройка файлов конфигурации VPN
# TODO: Может быть экзекутить прям сразу файлы
CONFIG_FILE="/etc/ipsec.conf"

Execute "cat > $CONFIG_FILE <<EOF
conn $VPN_NAME
  auto=add
  keyexchange=ikev1
  authby=secret
  type=transport
  left=%defaultroute
  leftprotoport=17/1701
  rightprotoport=17/1701
  right=$VPN_SERVER_IP
  ike=aes128-sha1-modp2048
  esp=aes128-sha1
EOF" \
        "Файл конфигурации $CONFIG_FILE записан." \
        "Ошибка! Произошла ошибка при записи файла конфигурации $CONFIG_FILE"

CONFIG_FILE="/etc/ipsec.secrets"

Execute "cat > $CONFIG_FILE <<EOF
: PSK $VPN_IPSEC_PSK
EOF" \
        "Файл конфигурации $CONFIG_FILE записан." \
        "Ошибка! Произошла ошибка при записи файла конфигурации $CONFIG_FILE"

chmod 600 $CONFIG_FILE

CONFIG_FILE="/etc/xl2tpd/xl2tpd.conf"

Execute "cat > $CONFIG_FILE <<EOF
[lac $VPN_NAME]
lns = $VPN_SERVER_IP
ppp debug = yes
pppoptfile = /etc/ppp/options.l2tpd.client
length bit = yes
EOF" \
        "Файл конфигурации $CONFIG_FILE записан." \
        "Ошибка! Произошла ошибка при записи файла конфигурации $CONFIG_FILE"

CONFIG_FILE="/etc/ppp/options.l2tpd.client"

Execute "cat > $CONFIG_FILE <<EOF
ipcp-accept-local
ipcp-accept-remote
refuse-eap
require-chap
noccp
noauth
mtu 1280
mru 1280
noipdefault
defaultroute
usepeerdns
connect-delay 5000
name $VPN_USER
password $VPN_PASSWORD
EOF" \
        "Файл конфигурации $CONFIG_FILE записан." \
        "Ошибка! Произошла ошибка при записи файла конфигурации $CONFIG_FILE"

chmod 600 $CONFIG_FILE

Logging "info" "Скрипт конфигурация VPN завершен."


#
#cat > /etc/ipsec.conf <<EOF
#conn $VPN_NAME
#  auto=add
#  keyexchange=ikev1
#  authby=secret
#  type=transport
#  left=%defaultroute
#  leftprotoport=17/1701
#  rightprotoport=17/1701
#  right=$VPN_SERVER_IP
#  ike=aes128-sha1-modp2048
#  esp=aes128-sha1
#EOF
#
#cat > /etc/ipsec.secrets <<EOF
#: PSK $VPN_IPSEC_PSK
#EOF
#
#chmod 600 /etc/ipsec.secrets
#
#cat > /etc/xl2tpd/xl2tpd.conf <<EOF
#[lac $VPN_NAME]
#lns = $VPN_SERVER_IP
#ppp debug = yes
#pppoptfile = /etc/ppp/options.l2tpd.client
#length bit = yes
#EOF
#
#cat > /etc/ppp/options.l2tpd.client <<EOF
#ipcp-accept-local
#ipcp-accept-remote
#refuse-eap
#require-chap
#noccp
#noauth
#mtu 1280
#mru 1280
#noipdefault
#defaultroute
#usepeerdns
#connect-delay 5000
#name $VPN_USER
#password $VPN_PASSWORD
#EOF
#
#chmod 600 /etc/ppp/options.l2tpd.client
