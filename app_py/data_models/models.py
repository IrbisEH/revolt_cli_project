from pathlib import Path
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


@dataclass
class DevItemModel:
    type: str = 'unknown'
    vmx_path: Path = None
    is_running: bool = False
    name: str = None
    mac: str = None
    ip: str = None
    ssh_port: int = None
    user: str = None
    password: str = None

    def __post_init__(self):
        if self.vmx_path:
            self.type = 'vmx'

            if not isinstance(self.vmx_path, Path):
                self.vmx_path = Path(self.vmx_path)

            if not self.name:
                self.name = self.vmx_path.name

            if not self.mac:
                kwargs = {}
                with open(self.vmx_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith('#') or '=' not in line:
                            continue
                        k, v = (i.strip() for i in line.split('=', 1))
                        kwargs[k] = v
                manual_mac = kwargs.get('ethernet0.address')        # ethernet0.address — заданный вручную MAC-адрес
                auto_mac = kwargs.get('ethernet0.mac')              # ethernet0.generatedAddress — автоматически сгенерированный VMware
                self.mac = manual_mac if manual_mac else auto_mac

        if self.mac:
            self.mac = self.mac.strip('"').strip("'").lower()

        if isinstance(self.ssh_port, str):
            self.ssh_port = int(self.ssh_port)

    def __str__(self):
        return f'{self.name or "Undefined":<35} {str(self.is_running):<10} {self.mac or "Undefined":<20} {self.ip or "Undefined":<15}'
