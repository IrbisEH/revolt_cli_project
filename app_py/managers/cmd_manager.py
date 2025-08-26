class CmdManager:
    ACTIONS = [
        'get',
        'refresh'
    ]

    def __init__(self, config, net_manager, vm_manager):
        self.config = config
        self.net_manager = net_manager
        self.vm_manager = vm_manager

        self.dev_items = config.dev_items

    def exec(self, args):
        try:
            action = args.pop(0) if args else None
            a_type = args.pop(0) if args else None

            if action not in self.ACTIONS:
                raise ValueError('Error! Invalid action.')

            self._refresh_dev_items()

            if action == 'get':
                self.get_ip_cmd()

            if action == 'refresh':
                self._refresh_dev_items(True)

        except IndexError:
            print('Error! Wrong number of arguments')
            exit(1)
        except Exception as e:
            print(e)
            exit(1)

    def get_ip_cmd(self):
        for item in self.dev_items:
            print(item)

    def _refresh_dev_items(self, is_hard=False):
        self.net_manager.refresh_dev_items(self.dev_items, is_hard)
        self.vm_manager.refresh_dev_items(self.dev_items)