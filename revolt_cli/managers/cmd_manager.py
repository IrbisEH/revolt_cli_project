import time


class CmdManager:
    def __init__(self):
        pass

    def parse_cmd(self, line):
        return line.split()

    def exec(self, line):
        cmd = self.parse_cmd(line)
        time.sleep(3)
