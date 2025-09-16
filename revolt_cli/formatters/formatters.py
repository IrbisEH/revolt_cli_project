from abc import ABC, abstractmethod


class FormatterBase(ABC):
    @abstractmethod
    def format(self, items: dict) -> str:
        pass


class KeyValFormatter(FormatterBase):
    def format(self, items: dict) -> str:
        key_width = max(len(k) for k in items)
        lines = [f'{k.ljust(key_width)} {v}' for k, v in items.items()]
        return '\n'.join(lines)