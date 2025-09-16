from datetime import date, datetime
from dataclasses import dataclass, fields


@dataclass
class RevoltConfig:
    mac: str
    interface: str
    ip: str
    user: str
    password: str
    vmx_roots: list
    dev_items: []


class DbItemModel:
    _SEP = '\t'
    _TABLE = None
    _TABLE_DIST = None
    _DATE_FRMT = '%Y-%m-%d'
    _DATETIME_FRMT = '%Y-%m-%d %H:%M:%S'

    @classmethod
    def init_by_line(cls, line):
        values = line.split(cls._SEP)
        return cls(*values)

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)

            if isinstance(value, str):
                if field.type == date:
                    setattr(self, field.name, date.fromisoformat(value))

                if field.type == datetime:
                    setattr(self, field.name, datetime.fromisoformat(value))

                if field.type == int:
                    setattr(self, field.name, round(float(value)))
