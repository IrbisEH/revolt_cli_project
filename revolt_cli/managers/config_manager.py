import json
from pathlib import Path
from revolt_cli.data_models.models import DevItemModel


class ConfigManager:
    CONFIG_FILE_NAME = None

    def __init__(self):
        self.config_file = self.get_config_file_path()
        self.raw_data = self.read_config_file()

    def get_config_file_path(self):
        config_dir = Path.home() / '.config' / self.CONFIG_FILE_NAME
        config_file = config_dir / self.CONFIG_FILE_NAME

        if not config_dir.exists():
            config_dir.mkdir(parents=True, exist_ok=True)

        if not config_file.exists():
            with open(config_file, 'w') as f:
                f.write(json.dumps({}))

        return config_file

    def read_config_file(self):
        with open(self.config_file, 'r') as f:
            return json.load(f)


class AppConfigManager(ConfigManager):
    CONFIG_FILE_NAME = 'config.json'

    def __init__(self):
        super().__init__()

        config = self.raw_data.get('config', {})

        self.mac = config.get('mac')
        self.interface = config.get('interface')
        self.ip = config.get('ip')
        self.user = config.get('user')
        self.password = config.get('password')


class DevItemsConfigManager(ConfigManager):
    CONFIG_FILE_NAME = 'dev-items-config.json'

    def __init__(self):
        super().__init__()

        config = self.raw_data.get('config', {})

        self.vmx_roots = config.get('vmx_roots', [])
        self.dev_items = config.get('dev_items', [])

        self.dev_items = [DevItemModel(**kwargs) for kwargs in self.dev_items]

        defined_paths = [str(obj.vmx_path) for obj in self.dev_items]
        for root_path in self.vmx_roots:
            for vmx_path in Path(root_path).rglob('*.vmx'):
                if str(vmx_path) in defined_paths:
                    continue
                self.dev_items.append(DevItemModel(vmx_path=vmx_path))
