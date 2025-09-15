from pathlib import Path
from revolt_cli.managers.config_manager import ConfigManager
from revolt_cli.managers.cli_manager import CliManager


APP_DIR = Path(__file__).resolve().parent
CONFIG_FILE = APP_DIR / 'data' / 'config.json'


def main():
    config = ConfigManager(config_file=CONFIG_FILE)
    cli = CliManager(config=config)
    cli.run()

if __name__ == '__main__':
    main()
