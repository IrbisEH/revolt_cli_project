from abc import ABC, abstractmethod


class Module(ABC):
    CONFIG = None
    ACTIONS = []
    LAZY_LOADS = {}

    def __init__(self):
        self.config = self.CONFIG()
        self.actions = {}

        for key in self.ACTIONS:
            if hasattr(self, key) or callable(getattr(self, key)):
                self.actions[key] = getattr(self, key)

    def __getattr__(self, name):
        if name not in self.LAZY_LOADS:
            raise AttributeError(f'Can not find attribute "{name}" for "{self.__class__.__name__}"')

        klass, args = self.LAZY_LOADS.get(name)

        if callable(klass):
            instance = klass(*args)
        else:
            instance = None

        setattr(self, name, instance)
        return instance

    def process(self, args: list):
        if not args:
            raise AttributeError('No arguments provided')

        action = args.pop(0)

        if action not in self.actions:
            raise AttributeError(f'Unknown action: {action}')

        method = self.actions[action]

        return method(args)