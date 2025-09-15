import os
import json
from pathlib import Path
from revolt_cli.data_models.models import DevItemModel


class ConfigManager:
    FILE_NAME = 'config.json'

    def __init__(self):
        self.config_file = self.get_config_path()
        print(self.config_file)
        self.raw_data = dict()

        if not os.path.isfile(self.config_file):
            with open(self.config_file, 'w') as f:
                f.write(json.dumps(self.raw_data))
        else:
            with open(self.config_file, 'r') as f:
                self.raw_data = json.load(f)

        config = self.raw_data.get('config', {})

        self.mac = config.get('mac')
        self.interface = config.get('interface')
        self.ip = config.get('ip')
        self.user = config.get('user')
        self.password = config.get('password')
        self.vmx_roots = config.get('vmx_roots', [])
        self.dev_items = config.get('dev_items', [])

        self.dev_items = [DevItemModel(**kwargs) for kwargs in self.dev_items]

        defined_paths = [str(obj.vmx_path) for obj in self.dev_items]
        for root_path in self.vmx_roots:
            for vmx_path in Path(root_path).rglob('*.vmx'):
                if str(vmx_path) in defined_paths:
                    continue
                self.dev_items.append(DevItemModel(vmx_path=vmx_path))

    def get_config_path(self):
        user_config = Path.home() / '.config' / 'revolt-cli' / self.FILE_NAME
        system_config = Path('/etc/revolt-cli') / self.FILE_NAME

        if user_config.exists():
            return user_config
        elif system_config.exists():
            return system_config
        else:
            raise FileNotFoundError('Error! Can not find config file!')
