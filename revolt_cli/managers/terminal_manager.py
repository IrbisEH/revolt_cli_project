import os
import sys
import tty
import time
import queue
import select
import termios
import threading
import itertools
from revolt_cli.tools.decorators import log_process
from revolt_cli.managers.log_manager import LogManager
from revolt_cli.models.models import QueueMsg


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

    def set_terminal(self):
        tty.setcbreak(self.fd)
        settings = termios.tcgetattr(self.fd)
        settings[3] &= ~termios.ECHO
        termios.tcsetattr(self.fd, termios.TCSADRAIN, settings)

    def get_terminal_settings(self):
        return termios.tcgetattr(self.fd)

    @log_process
    def loop(self):
        try:
            self.clear_line()

            while not self.stop_event.is_set():
                rlist, _, _ = select.select([sys.stdin], [], [], 0.01)

                if not rlist:
                    continue

                ch = sys.stdin.read(1)

                if ch == '\n':
                    resp = self.get_response(self.cmd_line, timeout=self.config.timeout_sec)
                    self.cmd_line = ''
                    self.new_line()
                    self.print(resp)
                    self.new_line()
                    self.print_prompt()
                    continue

                self.cmd_line += ch
                self.print(ch)

        finally:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

    def stop(self):
        self.stop_event.set()

    def print(self, line=''):
        sys.stdout.write(line)
        sys.stdout.flush()

    def print_prompt(self):
        self.print(f'{self.APP_PROMPT} {self.INPUT_CHAR} ')

    def new_line(self):
        sys.stdout.write('\n')
        sys.stdout.flush()

    def clear_line(self, prompt=True):
        sys.stdout.write('\r\x1b[2K')
        sys.stdout.flush()
        if prompt:
            self.print_prompt()

    def get_response(self, cmd_line, timeout=None):
        queue_obj = QueueMsg(_input=cmd_line)
        self.queues.to_manager.put(queue_obj)

        try:
            queue_obj = self.queues.to_terminal.get(timeout=timeout)

            if not isinstance(queue_obj, QueueMsg):
                raise ValueError(f'Error! Get invalid queue object. Can not read app msg.')

            return queue_obj.output

        except queue.Empty:
            return 'Error! App response timed out.'
        except ValueError as e:
            return str(e)
