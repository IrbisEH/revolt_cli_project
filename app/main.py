import os
import sys
import json
import ipaddress
import netifaces
from dotenv import load_dotenv
from scapy.all import ARP, Ether, srp

script_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(script_dir, ".env"))

NET_INTERFACE = os.getenv("NET_INTERFACE", None)
DATA_FILE = os.getenv("DATA_FILE", None)


class Vm:
    def __init__(self, name=None, vm_path=None):
        self.name = name
        self.vm_path = vm_path

class Storage:
    def __init__(self):
        self.vm_list = []

        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            for item in data['vm']:
                self.vm_list.append(Vm(**item))

class Network:
    def __init__(self):
        self.intfs = NET_INTERFACE
        self.ip = None
        self.netmask = None
        self.cidr = None

        self.get_network_data()

    def get_network_data(self):
        addrs = netifaces.ifaddresses(self.intfs)
        ip_info = addrs[netifaces.AF_INET][0]

        self.ip = ip_info['addr']
        self.netmask = ip_info['netmask']
        self.cidr = ipaddress.IPv4Network(f'{self.ip}/{self.netmask}', strict=False)

    def arp_scan(self):
        arp = ARP(pdst=self.cidr)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=2, verbose=0)[0]

        devices = []
        for sent, received in result:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})

        return devices

    def find_ip_by_mac(self, target_mac):
        devices = self.arp_scan()

        for device in devices:
            if device['mac'].lower() == target_mac.lower():
                return device['ip']

        return None

    def __str__(self):
        return f'ip: {self.ip}, netmask: {self.netmask}, cidr: {self.cidr}'


def cmd_get_ip(args, store):
    name = args.pop(0) if args else ""
    vm_list = [vm.name == name for vm in store.vm_list]




if __name__ == '__main__':
    cmd_args = [i.strip() for i in sys.argv[1:] if i]

    storage = Storage()
    network = Network()

    network.arp_scan()



    # action = cmd_args.pop(0) if cmd_args else None
    #
    # if action == 'get':
    #     action_type = cmd_args.pop(0) if cmd_args else None
    #
    #     if action_type == 'ip':
    #         cmd_get_ip(cmd_args, storage)