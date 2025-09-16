from revolt_cli.managers.config_manager import ConfigManager


class AppConfigManager(ConfigManager):
    MODULE_KEY = 'app-module'

    def __init__(self):
        super().__init__()

        self.user = None
        self.password = None
        self.interface = None

        self.set_attributes()
