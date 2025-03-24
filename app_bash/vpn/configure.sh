#!/usr/bin/env bash

Execute() {
  local command="$1"
  local success_msg="$2"
  local error_msg="$3"

  Logging "info" "Выполняет команда: $command"

  local output=$(bash -c "$command")
  local exit_code=$?

  if [ "$exit_code" -eq 0 ]; then
    Logging "success" "$success_msg Вывод: $output"
  else
    Logging "error" "$error_msg Вывод: $output"
    exit 1
  fi
}

Execute "ip netns add $VPN_NAMESPACE" \
        "Сетевое пространство $VPN_NAMESPACE успешно создано." \
        "Ошибка! Произошла ошибка при создании сетевого пространства $VPN_NAMESPACE."

Execute "ip link add "$VETH_INTFS_DEFAULT_NS" type veth peer name $VETH_INTFS_VASE_NS" \
        "Интерфейс $VETH_INTFS_DEFAULT_NS успешно создан." \
        "Ошибка! Произошла ошибка при создании интерфейса $VETH_INTFS_DEFAULT_NS."

Execute "ip addr add $IP_DEFAULT_NS dev $VETH_INTFS_DEFAULT_NS" \
        "Ip адрес $VPN_NAMESPACE привязан к интерфейсу $VETH_INTFS_DEFAULT_NS." \
        "Ошибка! Произошла ошибка при привязке ip адреса $VPN_NAMESPACE к интерфейсу $VETH_INTFS_DEFAULT_NS."

Execute "ip link set $VETH_INTFS_DEFAULT_NS up" \
        "Интерфейс $VETH_INTFS_DEFAULT_NS успешно запущен." \
        "Ошибка! Произошла ошибка при запуске интерфейса $VETH_INTFS_DEFAULT_NS."

Execute "ip netns exec $VPN_NAMESPACE ip addr add $VETH_INTFS_VASE_NS dev $VETH_INTFS_NAME_VPN_SPACE" \
        "Интерфейс $VETH_INTFS_DEFAULT_NS успешно запущен." \
        "Ошибка! Произошла ошибка при запуске интерфейса $VETH_INTFS_DEFAULT_NS."





#sudo ip netns exec vase_net_space ip addr add 10.0.0.2/24 dev $VETH_INTFS_NAME_VPN_SPACE
#sudo ip netns exec vase_net_space ip link set $VETH_INTFS_NAME_VPN_SPACE up
#sudo sysctl -w net.ipv4_forward=1
#sudo ip netns exec vase_net_space ip route add default via 10.0.0.1
#sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o enp4s0 -j MASQUERADE
#sudo ufw route allow in on $VETH_INTFS_NAME_DEFAULT_SPACE out on enp4s0
#sudo ufw route allow in on enp4s0 out on $VETH_INTFS_NAME_DEFAULT_SPACE
#
#apt-get update
#apt-get install strongswan xl2tpd net-tools
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
