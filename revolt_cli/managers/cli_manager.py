import threading
from revolt_cli.models.models import Queues, QueueMsg
from revolt_cli.managers.log_manager import LogManager
from revolt_cli.managers.config_manager import ConfigManager
from revolt_cli.managers.terminal_manager import TerminalManager
from revolt_cli.tools.decorators import log_process


class CliManager:
    SEP = ' '

    def __init__(self):
        self.config = ConfigManager()

        self.log = LogManager(
            self.__class__.__name__,
            self.config.log_file,
            log_level=self.config.log_level
        )

        self.queues = Queues()
        self.terminal = TerminalManager(self.config, self.queues)

        self.modules = []

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

    def run(self):
        th = threading.Thread(target=self.terminal.loop, daemon=False)

        try:
            th.start()
            self.loop()
        finally:
            self.terminal.stop()

    @log_process
    def loop(self):
        while True:
            try:
                queue_obj = self.queues.to_manager.get()

                if not isinstance(queue_obj, QueueMsg):
                    raise ValueError(f'Error! Get invalid queue object. Can not read terminal msg.')

                cmd = queue_obj.input.split()

                if not cmd:
                    raise ValueError(f'Error! Get invalid user input "{queue_obj.input}"')

                module = cmd[0]
                args = cmd[1:]

                if module not in self.modules:
                    raise ValueError(f'Error! Can not execute cmd "{queue_obj.input}" for module "{module}"')

                queue_obj.output = self.modules[module].execute(args)
                self.queues.to_terminal.put(queue_obj)

            except ValueError as e:
                queue_obj = QueueMsg(_output=str(e))
                self.queues.to_terminal.put(queue_obj.output)
                self.log.error(queue_obj.output)
            except Exception as e:
                queue_obj = QueueMsg(_output=f'Internal error: {str(e)}')
                self.queues.to_terminal.put(queue_obj)
                self.log.error(queue_obj.output)
