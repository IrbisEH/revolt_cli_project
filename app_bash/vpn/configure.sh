#!/usr/bin/env bash

#TODO: Allow user to run custom net namespace


. /home/irbis-eh/revolt_cli/app_bash/vpn/.env

sudo ip netns add $VPN_NAMESPACE
sudo ip link add $VETH_INTFS_NAME_DEFAULT_SPACE type veth peer name $VETH_INTFS_NAME_VPN_SPACE
sudo ip addr add 10.0.0.1/24 dev $VETH_INTFS_NAME_DEFAULT_SPACE
sudo ip link set $VETH_INTFS_NAME_DEFAULT_SPACE up
sudo ip netns exec vase_net_space ip addr add 10.0.0.2/24 dev $VETH_INTFS_NAME_VPN_SPACE
sudo ip netns exec vase_net_space ip link set $VETH_INTFS_NAME_VPN_SPACE up
sudo sysctl -w net.ipv4_forward=1
sudo ip netns exec vase_net_space ip route add default via 10.0.0.1
sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o enp4s0 -j MASQUERADE
sudo ufw route allow in on $VETH_INTFS_NAME_DEFAULT_SPACE out on enp4s0
sudo ufw route allow in on enp4s0 out on $VETH_INTFS_NAME_DEFAULT_SPACE

apt-get update
apt-get install strongswan xl2tpd net-tools

cat > /etc/ipsec.conf <<EOF
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
EOF

cat > /etc/ipsec.secrets <<EOF
: PSK $VPN_IPSEC_PSK
EOF

chmod 600 /etc/ipsec.secrets

cat > /etc/xl2tpd/xl2tpd.conf <<EOF
[lac $VPN_NAME]
lns = $VPN_SERVER_IP
ppp debug = yes
pppoptfile = /etc/ppp/options.l2tpd.client
length bit = yes
EOF

cat > /etc/ppp/options.l2tpd.client <<EOF
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
EOF

chmod 600 /etc/ppp/options.l2tpd.client
