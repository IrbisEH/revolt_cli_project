import os
import sys
import tty
import time
import select
import termios
import threading
import itertools
from revolt_cli.managers.log_manager import LogManager
from revolt_cli.tools.decorators import log_process


class TerminalManager:
    APP_PROMPT = 'revolt-cli'
    INPUT_CHAR = '>'

    def __init__(self, config, queues):
        self.stop_event = threading.Event()
        self.config = config
        self.queues = queues

        self.log = LogManager(
            self.__class__.__name__,
            self.config.log_file,
            log_level=self.config.log_level
        )

        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        self.set_terminal()

        self.cmd_line = ''
        self.print_prompt = True

    def set_terminal(self):
        tty.setcbreak(self.fd)

    def get_terminal_settings(self):
        return termios.tcgetattr(self.fd)

    @log_process
    def loop(self):
        try:
            while not self.stop_event.is_set():

                if not self.cmd_line and self.print_prompt:
                    self.print_prompt = False
                    self.print(f'{self.APP_PROMPT} {self.INPUT_CHAR} ')

                rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                if rlist:
                    ch = sys.stdin.read(1)
                    if ch:
                        self.print(ch)
        finally:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def stop(self):
        self.stop_event.set()

    def print(self, line):
        if line not in ('\n', '\r'):
            sys.stdout.write(line)
            sys.stdout.flush()

    def new_line(self):
        sys.stdout.write('\n')
        sys.stdout.flush()

    def carriage_return(self):
        sys.stdout.write('\r')
        sys.stdout.flush()
