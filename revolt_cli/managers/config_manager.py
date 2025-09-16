import json
from pathlib import Path


class ConfigManager:
    CONFIG_FILE_NAME = 'revolt-cli-config.json'
    MODULE_KEY = None

    def __init__(self):
        self.config_file = self.get_config_file_path()
        raw_data = self.read_config_file()
        self.config = raw_data.get(self.MODULE_KEY, {})

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
    MODULE_KEY = 'app'

    def __init__(self):
        super().__init__()

        self.mac = self.config.get('mac')
        self.interface = self.config.get('interface')
        self.ip = self.config.get('ip')
        self.user = self.config.get('user')
        self.password = self.config.get('password')
