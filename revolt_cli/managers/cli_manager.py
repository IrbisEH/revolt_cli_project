from revolt_cli.managers.config_manager import ConfigManager
from revolt_cli.managers.terminal_manager import TerminalManager


class CliManager:
    SEP = ' '

    def __init__(self):
        self.config = ConfigManager()
        self.terminal = TerminalManager()
        self.modules = self.define_modules()

    def __getattr__(self, name):
        if name not in self.modules:
            raise AttributeError(name)

        klass = self.modules.get(name)

        if callable(klass):
            instance = klass()
        else:
            instance = None

        setattr(self, name, instance)
        return instance

    def define_modules(self):
        modules = {}
        all_config = self.config.read_config_file()
        for key in all_config.keys():
            if key == 'app-module':
                from revolt_cli.modules.app.module import AppModule
                modules['AppModule'] = AppModule

            if key == 'dev-items-module':
                from revolt_cli.modules.dev_items_module.module import DevItemsModule
                modules['DevItemsModule'] = DevItemsModule

        return modules

    def run(self):
        while True:
            user_input = self.terminal.get_user_input()
            response = ''

            self.terminal.disable_input()
            self.terminal.spinner.start()

            try:
                args = self._parse_arguments(user_input)

                if not len(args):
                    raise AttributeError('No arguments provided.')

                action = args.pop(0)

                if 'AppModule' in self.modules and action in self.modules['AppModule'].ACTIONS:
                    args.insert(0, action)
                    action = 'app'

                if not hasattr(self, action) or not callable(getattr(self, action)):
                    raise AttributeError(f'Unknown command: {action}')

                method = getattr(self, action)
                response = method(args)

            except RuntimeError as e:
                response = f'Error! {e}'
            except AttributeError as e:
                response = f'Error! {e}'
            except Exception as e:
                response = f'Error! Failed to execute command "{user_input}" Exception: "{e}"'
            finally:
                self.terminal.spinner.stop()
                self.terminal.enable_input()
                if response:
                    self.terminal.print(response)
                self.terminal.print()

    def _parse_arguments(self, line):
        line = line.strip()
        if line == '':
            return []
        return line.split(self.SEP)

    def app(self, args):
        return self.AppModule.process(args)

    def devitems(self, args):
        return self.DevItemsModule.process(args)

    def exit(self, args):
        exit()
