import sys
from pathlib import Path

from revolt_cli.managers.network_manager import NetworkManager
from revolt_cli.managers.vm_manager import VmManager
from revolt_cli.managers.config_manager import ConfigManager
from revolt_cli.managers.cmd_manager import CmdManager

APP_DIR = Path(__file__).resolve().parent
CONFIG_FILE = APP_DIR / 'data' / 'config.json'


def main():
    config = ConfigManager(config_file=CONFIG_FILE)
    net_manager = NetworkManager(config)
    vm_manager = VmManager()
    cmd = CmdManager(config, net_manager, vm_manager)

    cmd_args = [i.strip() for i in sys.argv[1:] if i]

    cmd.exec(cmd_args)


if __name__ == '__main__':
    main()