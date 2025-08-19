import sys
from pathlib import Path

from app_py.managers.network_manager import NetworkManager
from app_py.managers.vm_manager import VmManager
from app_py.managers.config_manager import ConfigManager
from app_py.managers.cmd_manager import CmdManager

APP_DIR = Path(__file__).resolve().parent
ETC_DIR = APP_DIR / 'etc'
CONFIG_FILE = ETC_DIR / 'config.json'


if __name__ == '__main__':
    config = ConfigManager(config_file=CONFIG_FILE)
    net_manager = NetworkManager(config)
    vm_manager = VmManager()
    cmd = CmdManager(config, net_manager, vm_manager)

    cmd_args = [i.strip() for i in sys.argv[1:] if i]

    cmd.exec(cmd_args)
