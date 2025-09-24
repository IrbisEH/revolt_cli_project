import os
import json
from pathlib import Path
from dotenv import load_dotenv


class ConfigManager:
    CONFIG_FILE = '~/.config/revolt-cli/config.json'

    def __init__(self):
        self.config_file = self.get_file_path(self.CONFIG_FILE)

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


class CliConfigManager(ConfigManager):
    LOG_FILE = '~/.log/revolt-cli/cli.log'
    ENV_FILE = '~/.config/revolt-cli/.env'

    def __init__(self):
        super().__init__()
        self.log_file = self.get_file_path(self.LOG_FILE)
        self.env_file = self.get_file_path(self.ENV_FILE)

        load_dotenv(self.env_file)

        self.log_level = os.getenv('CLI_LOG_LEVEL', 'INFO')
        self.app_response_timeout_sec = int(os.getenv('CLI_RESPONSE_TIMEOUT_SEC', 30))
        self.app_module = bool(os.getenv('APP_MODULE', True))
