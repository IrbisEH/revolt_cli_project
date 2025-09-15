import os
import sys
import threading
import time
import termios

class TerminalManager:
    CMD_PROMPT = 'revolt-cli'
    LOAD_SYMBOLS = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']

    def __init__(self):
        self.user_input = ''
        self.loader = self.load_animation()
        self.fd = sys.stdin.fileno()
        self.settings = termios.tcgetattr(self.fd)

    def get_input(self):
        self.write()
        return sys.stdin.readline()

    def write(self, lines: str = None) -> None:
        _lines = f'\r{self.CMD_PROMPT} > '

        if lines:
            _lines += f'{lines}\n'

        sys.stdout.write(_lines)
        sys.stdout.flush()

    def show_loading(self, stop_event: threading.Event) -> None:
        self.disable_input()
        while not stop_event.is_set():
            next(self.loader)
        self.enable_input()

    def clean(self):
        os.system('clear')

    def load_animation(self):
        idx = 0

        while True:
            if idx >= len(self.LOAD_SYMBOLS):
                idx = 0

            time.sleep(0.1)
            line = f'\r{self.CMD_PROMPT} {self.LOAD_SYMBOLS[idx]} '
            sys.stdout.write(line)
            sys.stdout.flush()
            idx += 1
            yield

    def disable_input(self):
        new_settings = termios.tcgetattr(self.fd)
        new_settings[3] &= ~(termios.ICANON | termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSADRAIN, new_settings)

    def enable_input(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.settings)
