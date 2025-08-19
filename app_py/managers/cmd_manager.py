class CmdManager:
    def __init__(self, config, network):
        self.config = config
        self.network = network
        self.dev_items = config.dev_items

    def exec(self, args):
        try:
            self.network.refresh_dev_items(self.dev_items)

            action = args.pop(0) if args else None
            a_type = args.pop(0) if args else None

            # get -> make table obj with filter
            # refresh -> refresh arp hard


            self.get_ip_cmd()

        except IndexError:
            print('Error! Wrong number of arguments')
            exit(1)
        except Exception as e:
            print(e)
            exit(1)

    def get_ip_cmd(self):
        for item in self.dev_items:
            print(item)