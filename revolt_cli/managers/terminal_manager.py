import os
import sys
import time
import termios
import threading
import itertools


class TerminalManager:
    APP_PROMPT = 'revolt-cli'
    INPUT_PROMPT = '>'

    def __init__(self):
        self.spinner = Spinner()
        self.fd = sys.stdin.fileno()
        self.settings = None

    def get_user_input(self):
        sys.stdout.write(f'\r{self.APP_PROMPT} {self.INPUT_PROMPT} ')
        sys.stdout.flush()
        lines = sys.stdin.readline().strip()
        return lines

    @staticmethod
    def print(lines: str = None) -> None:
        _lines = '\r{}\n'
        lines = _lines.format(lines or '')
        sys.stdout.write(lines)
        sys.stdout.flush()

    @staticmethod
    def clear():
        os.system('clear')

    def start_load_animation(self) -> None:
        self.disable_input()
        self.spinner.start()

    def stop_load_animation(self):
        self.spinner.stop()
        self.enable_input()

    def disable_input(self):
        self.settings = termios.tcgetattr(self.fd)
        new_settings = termios.tcgetattr(self.fd)
        new_settings[3] &= ~(termios.ICANON | termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSADRAIN, new_settings)

    def enable_input(self):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.settings)


class Spinner:
    def __init__(self, prefix='Loading'):
        self.prefix = prefix
        # TODO: !
        self.spinner = itertools.cycle([
            f'{prefix}.     ',
            f'{prefix}..    ',
            f'{prefix}...   ',
            f'{prefix} ...  ',
            f'{prefix}  ... ',
            f'{prefix}   ...',
            f'{prefix}    ..',
            f'{prefix}     .',
            f'{prefix}      '
        ])
        self.stop_event = threading.Event()
        self.thread = None

    def start(self) -> None:
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        if self.thread:
            self.thread.join()
        sys.stdout.write('\r')
        sys.stdout.flush()

    def _animate(self) -> None:
        time.sleep(0.3)
        while not self.stop_event.is_set():
            sys.stdout.write(f'\r{next(self.spinner)}')
            sys.stdout.flush()
            time.sleep(0.1)
