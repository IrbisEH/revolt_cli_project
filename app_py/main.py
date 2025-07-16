import os
import sys
import json
import ipaddress
import netifaces
from pathlib import Path
from dotenv import load_dotenv
from scapy.all import ARP, Ether, srp

APP_DIR = Path(__file__).resolve().parent.parent
ETC_DIR = APP_DIR / 'etc'
DATA_DIR = APP_DIR / 'data'
DATA_FILE = DATA_DIR / 'data.json'

load_dotenv(ETC_DIR / '.env')

NET_INTERFACE = os.getenv("NET_INTERFACE", None)


class Vm:
    def __init__(self, name=None, vm_path=None, ip=None, mac=None):
        self.name = name
        self.vm_path = vm_path
        self.ip = None
        self.mac = None

        if mac is None:
            manual_mac = None   # ethernet0.address — заданный вручную MAC-адрес
            auto_mac = None     # ethernet0.generatedAddress — автоматически сгенерированный VMware

            with open(self.vm_path, 'r') as f:
                for line in f.readlines():
                    items = [l.strip() for l in line.split('=')]
                    if len(items) == 2:
                        if items[0] == 'ethernet0.address':
                            manual_mac = items[1]
                        if items[0] == 'ethernet0.generatedAddress':
                            auto_mac = items[1]

            self.mac = manual_mac if manual_mac else auto_mac
            self.mac = self.mac.lower().strip('"')

    def __str__(self):
        return f"Vm instance: '{self.name}'. IP: {self.ip}. MAC: {self.mac}"

class Storage:
    def __init__(self):
        self.vm_list = []

        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for kwargs in data['vm']:
                self.vm_list.append(Vm(**kwargs))

class Network:
    def __init__(self):
        self.intfs = NET_INTERFACE
        self.ip = None
        self.netmask = None
        self.cidr = None

        self.arp = {}       # key - ip, value - mac

        self.get_network_data()

    def get_network_data(self):
        addrs = netifaces.ifaddresses(self.intfs)
        ip_info = addrs[netifaces.AF_INET][0]

        self.ip = ip_info['addr']
        self.netmask = ip_info['netmask']
        self.cidr = str(ipaddress.IPv4Network(f'{self.ip}/{self.netmask}', strict=False))
        self.arp_scan()

    def arp_scan(self):
        arp = ARP(pdst=self.cidr)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=2, verbose=0)[0]

        for sent, received in result:
            self.arp[received.psrc] = received.hwsrc.lower()

    def get_ip_by_mac(self, target_mac, update_arp=False):
        if update_arp:
            self.arp_scan()
        for ip, mac in self.arp.items():
            if target_mac == mac:
                return ip
        return None

    def __str__(self):
        return f'ip: {self.ip}, netmask: {self.netmask}, cidr: {self.cidr}'


def cmd_get_ip(args, store, network):
    vm_list = store.vm_list

    if args:
        name = args.pop(0) if args else ""
        vm_list = [vm for vm in store.vm_list if name in vm.name]

    for vm in vm_list:
        if vm.ip is None:
            vm.ip = network.get_ip_by_mac(vm.mac)
        print(f'{vm.name:<20} {vm.ip:<15}')


if __name__ == '__main__':
    cmd_args = [i.strip() for i in sys.argv[1:] if i]

    storage = Storage()
    network = Network()

    action = cmd_args.pop(0) if cmd_args else None

    if action == 'get':
        action_type = cmd_args.pop(0) if cmd_args else None

        if action_type == 'ip':
            cmd_get_ip(cmd_args, storage, network)