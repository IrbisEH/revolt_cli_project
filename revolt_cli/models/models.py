import threading, queue


class Queues:
    def __init__(self):
        self.to_manager = queue.Queue()
        self.to_terminal = queue.Queue()


class QueueMsg:
    def __init__(self, _input='', _output=''):
        self.input = _input
        self.output = _output

    def  __repr__(self):
        return str(self.__dict__)