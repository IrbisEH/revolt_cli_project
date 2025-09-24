import json
from pathlib import Path


class ConfigManager:
    CONFIG_FILE = '~/.config/revolt-cli/config.json'
    LOG_FILE = '~/.log/revolt-cli/cli.log'
    TIMEOUT_SEC_DEFAULT = 30

    def __init__(self):
        self.config_file = self.get_file_path(self.CONFIG_FILE)
        self.log_file = self.get_file_path(self.LOG_FILE)
        # self.log_level = 'INFO'
        self.log_level = 'DEBUG'
        self.timeout_sec = self.TIMEOUT_SEC_DEFAULT

        if not self.config_file.exists():
            with open(self.config_file, 'w') as f:
                f.write(json.dumps({}))

    @staticmethod
    def get_file_path(file_path):
        file = Path(file_path).expanduser()
        file.parent.mkdir(parents=True, exist_ok=True)
        return file

    def read_config_file(self):
        with open(self.config_file, 'r') as f:
            return json.load(f)
