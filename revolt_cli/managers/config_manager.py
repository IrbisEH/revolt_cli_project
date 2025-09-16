import json
from pathlib import Path


class ConfigManager:
    CONFIG_FILE_NAME = 'config.json'
    MODULE_KEY = None

    def __init__(self):
        self.config_file = self.get_config_file_path()

    def __repr__(self):
        return str(self.__dict__)

    def get_config_file_path(self):
        config_dir = Path.home() / '.config' / 'revolt-cli'
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

    def set_attributes(self):
        raw_data = self.read_config_file()
        config = raw_data.get(self.MODULE_KEY, raw_data)

        for attr in self.__dict__.keys():
            val = config.get(attr)
            if val:
                setattr(self, attr, val)
