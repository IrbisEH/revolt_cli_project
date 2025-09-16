from pip._internal import network

from revolt_cli.modules.module import Module
from revolt_cli.managers.network_manager import NetworkManager
from revolt_cli.managers.command_manager import LinuxCommandManager as cmd
from revolt_cli.modules.app.config_manager import AppConfigManager

LINUX_MAC_ADDRESS_FILE = '/sys/class/net/{}/address'


class AppModule(Module):
    CONFIG = AppConfigManager
    ACTIONS = ['get', 'set', 'delete']

    def __init__(self):
        super().__init__()
        self.LAZY_LOADS['network'] = (NetworkManager, (self.config.interface, ))

    def get(self, args):
        get_lines_dic = {
            'config_file': lambda: f'config file: {self.config.config_file}',
            'interface': lambda: f'interface: {self.network.interface}',
            'ip': lambda: self.network.ip,
            'netmask': lambda: self.network.netmask,
            'cidr': lambda: self.network.cidr,
            # 'arp': lambda: self.get_arp_table
        }

        if not args:
            args = ['all']

        lines = ''
        _type = args.pop(0)

        if _type in get_lines_dic:
            lines = get_lines_dic[_type]()
        elif _type == 'all':
            lines = str(self.network)

        return lines

    def set(self, args):
        pass

    def delete(self, args):
        pass

    def get_arp_table(self):
        pass