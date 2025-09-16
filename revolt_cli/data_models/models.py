from dataclasses import dataclass


@dataclass
class RevoltConfig:
    mac: str
    interface: str
    ip: str
    user: str
    password: str
    vmx_roots: list
    dev_items: []
