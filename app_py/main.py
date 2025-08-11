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


class DevItem:
    def __init__(self, name=None, ip=None, mac=None):
        self.name = name
        self.ip = ip
        self.mac = mac

    def __repr__(self):
        return f'{self.__class__.__name__}: {self.name} {self.ip} {self.mac}'


class VmItem(DevItem):
    def __init__(self, name=None, ip=None, mac=None, vmx_path=None):
        super().__init__(name, ip, mac)
        self.vmx_path = vmx_path

        if not self.mac:
            self.read_vmx()

    def read_vmx(self):
        manual_mac = None   # ethernet0.address — заданный вручную MAC-адрес
        auto_mac = None     # ethernet0.generatedAddress — автоматически сгенерированный VMware

        try:
            with open(self.vmx_path, 'r') as f:
                for line in f.readlines():
                    items = [l.strip() for l in line.split('=')]
                    if len(items) == 2:
                        if items[0] == 'ethernet0.address':
                            manual_mac = items[1]
                        if items[0] == 'ethernet0.generatedAddress':
                            auto_mac = items[1]
        except FileNotFoundError:
            print(f"Error! Can not find '{self.vmx_path}'")

        self.mac = manual_mac if manual_mac else auto_mac
        self.mac = self.mac.lower().strip('"') if self.mac else None



class Storage:
    def __init__(self):
        self.dev_items = {}

        self.init_items()

    def init_items(self):
        try:
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)

            for item in data['items']:
                if item.get('vmx_path'):
                    obj = VmItem(**item)
                else:
                    obj = DevItem(**item)

                if obj.name not in self.dev_items:
                    self.dev_items[obj.name] = obj
                else:
                    print(f"Error! Duplicate item name '{obj.name}'")

        except FileNotFoundError:
            print(f"Error! File '{DATA_FILE}' not found")
            exit(1)

        except json.JSONDecodeError:
            print(f"Error! Invalid JSON format in '{DATA_FILE}'")
            exit(1)

        except Exception as e:
            print(f"Error! {e}")
            exit(1)


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


class Cmd:
    @staticmethod
    def cmd_get_ip(args, storage, network):
        find_name = args.pop(0) if args else None

        dev_items = storage.dev_items.values()

        if find_name:
            dev_items = [i for i in dev_items if find_name in i.name]

        for item in dev_items:
            if item.mac and item.ip is None:
                item.ip = network.get_ip_by_mac(item.mac)
            print(f'{item.name or "Undefined":<20} {item.ip or "Undefined":<15}')


if __name__ == '__main__':
    cmd_args = [i.strip() for i in sys.argv[1:] if i]

    storage = Storage()
    network = Network()

    action = cmd_args.pop(0) if cmd_args else None

    if action == 'get':
        action_type = cmd_args.pop(0) if cmd_args else None

        if action_type == 'ip':
            Cmd.cmd_get_ip(cmd_args, storage, network)