import json
from pathlib import Path
from revolt_cli.data_models.models import DevItemModel


class ConfigManager:
    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            data = json.load(f)

        config = data.get('config', {})

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
