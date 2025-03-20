# RESET
sudo sh /home/irbis-eh/revolt_cli/app_bash/vpn/reset.sh

# FIRST TERMINAL
sudo ip netns exec vase_net_space xl2tpd -c /etc/xl2tpd/xl2tpd.conf -D

# SECOND TERMINAL
sudo ip netns exec vase_net_space ipsec restart
sudo ip netns exec vase_net_space ipsec up vase_vpn

sudo ip netns exec vase_net_space bash -c "echo 'c vase_vpn' > /var/run/xl2tpd/l2tp-control"
# WAIT FOR PPO TUNEL
sudo ip netns exec vase_net_space ip addr

# CONFIGURE ROUTES
sudo ip netns exec vase_net_space ip route del default via 10.0.0.1 || true
sudo ip netns exec vase_net_space ip route add default dev ppp0
sudo ip netns exec vase_net_space ip route add 45.151.108.34 via 10.0.0.1 dev veth1 || true

# CHECK IP ADDRESS
sudo ip netns exec vase_net_space curl ifconfig.co

sudo ip netns exec vase_net_space sudo -u irbis-eh google-chrome --no-sandbox &