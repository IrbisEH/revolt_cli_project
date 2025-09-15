import threading
from revolt_cli.managers.cmd_manager import CmdManager
from revolt_cli.managers.config_manager import ConfigManager
from revolt_cli.managers.terminal_manager import TerminalManager


class CliManager:
    def __init__(self, config: ConfigManager):
        self.config = config
        self.cmd_manager = CmdManager()
        self.terminal = TerminalManager()

    def run(self):
        while True:
            user_input = self.terminal.get_input()

            stop_event = threading.Event()
            th = threading.Thread(
                target=self.terminal.show_loading,
                args=(stop_event, )
            )
            th.start()

            self.cmd_manager.exec(user_input)

            stop_event.set()
            th.join()

            self.terminal.write('some response')
