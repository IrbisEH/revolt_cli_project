from revolt_cli.managers.config_manager import ConfigManager


class DevItemsConfigManager(ConfigManager):
    MODULE_KEY = 'dev-items-module'

    def __init__(self):
        super().__init__()

        self.vmx_roots = self.config.get('vmx_roots', [])
        self.dev_items = self.config.get('dev_items', [])

        # self.dev_items = [DevItemModel(**kwargs) for kwargs in self.dev_items]
        #
        # defined_paths = [str(obj.vmx_path) for obj in self.dev_items]
        # for root_path in self.vmx_roots:
        #     for vmx_path in Path(root_path).rglob('*.vmx'):
        #         if str(vmx_path) in defined_paths:
        #             continue
        #         self.dev_items.append(DevItemModel(vmx_path=vmx_path))