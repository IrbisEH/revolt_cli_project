from revolt_cli.modules.module import Module
from revolt_cli.formatters.formatters import KeyValFormatter
from revolt_cli.managers.network_manager import NetworkManager
from revolt_cli.modules.app_module.config_manager import AppConfigManager


class AppModule(Module, KeyValFormatter):
    CONFIG = AppConfigManager
    ACTIONS = ['get']

    def __init__(self):
        super().__init__()
        self.LAZY_LOADS['network'] = (NetworkManager, (self.config.interface, ))
        self.config_items = {
            'config_file':  ('config file', lambda: self.config.config_file),
        }
        self.network_items = {
            'interface':    ('interface', lambda: getattr(self.network, 'interface', 'undefined')),
            'ip':           ('ip', lambda: getattr(self.network, 'ip', 'undefined')),
            'netmask':      ('netmask', lambda: getattr(self.network, 'netmask', 'undefined')),
            'cidr':         ('cidr', lambda: getattr(self.network, 'cidr', 'undefined'))
        }

    def get(self, args):
        if not args:
            raise AttributeError('Unknown command')

        _type = args.pop(0)

        if _type == 'config':
            return self.get_config(args)
        elif _type == 'config_file':
            return self.config_items['config_file'][1]()
        elif _type == 'network':
            return self.get_network(args)
        elif _type == 'arp':
            return self.get_arp(args)
        elif _type == 'interface':
            return self.network_items['interface'][1]()
        elif _type == 'ip':
            return self.network_items['ip'][1]()
        elif _type == 'netmask':
            return self.network_items['netmask'][1]()
        elif _type == 'cidr':
            return self.network_items['cidr'][1]()
        else:
            raise AttributeError(f'Unknown arg: {_type}')

    def get_config(self, args):
        if args and args[0] in self.config_items:
            return self.config_items[args[0]][1]()
        else:
            output = {v[0]:v[1]() for k, v in self.config_items.items()}
            return self.format(output)

    def get_network(self, args):
        if args and args[0] in self.network_items:
            return self.network_items[args[0]][1]()
        else:
            output = {v[0]:v[1]() for k, v in self.network_items.items()}
            return self.format(output)

    def get_arp(self, args):
        return self.format(getattr(self.network, 'arp', {}))
