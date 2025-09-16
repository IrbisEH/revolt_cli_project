import re
import ipaddress
import netifaces
import subprocess
from scapy.all import ARP, Ether, srp


class NetworkManager:
    def __init__(self, config):
        self.interface = config.interface

        addrs = netifaces.ifaddresses(self.interface)
        ip_info = addrs[netifaces.AF_INET][0]

        self.ip = ip_info['addr']
        self.netmask = ip_info['netmask']
        self.cidr = str(ipaddress.IPv4Network(f'{self.ip}/{self.netmask}', strict=False))

        self.arp = self._get_arp_table()

    def _get_arp_table(self):
        arp_table = {}
        result = subprocess.run(['arp', '-a'], capture_output=True, text=True)
        pattern = re.compile(r'\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-fA-F:]{17})')

        for ip, mac in pattern.findall(result.stdout):
            arp_table[mac.lower()] = ip  # MAC в нижний регистр

        return arp_table

    def arp_scan(self):
        arp = ARP(pdst=self.cidr)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=2, verbose=0)[0]

        for sent, received in result:
            mac = received.hwsrc.lower()
            ip = received.psrc
            self.arp[mac] = ip
