from dataclasses import dataclass, fields
from datetime import date, datetime
from typing import Optional


class DataItem:
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


@dataclass
class FlowDataItem(DataItem):
    _TABLE = 'dnsflow'
    _TABLE_DIST = 'dnsflow_dist'

    flow_date: date
    flow_time: datetime
    flow_millisecond: int
    login: str
    session_id: int
    source_ipv4: str
    source_ipv6: str
    source_port: int
    destination_ipv4: str
    destination_ipv6: str
    destination_port: int
    host: str
    dns_transport: int
    rclass: int
    rtype: int
    ttl: int
    dns_data: str
    vlan_id: int
    post_vlan_id: int
    mpls_labels: str
    from_subscriber: int
    is_excluded_subscriber: int
    dpi_id: int
    bridge_vchannel_num: int
    host_ip_dns_data: Optional[str] = None

    def get_sql_insert(self, is_dist=False):
        values = {f.name: getattr(self, f.name) for f in fields(self)}
        values['flow_date'] = self.flow_date.strftime(self._DATE_FRMT)
        values['flow_time'] = self.flow_time.strftime(self._DATETIME_FRMT)
        values['host_ip_dns_data'] = self.host_ip_dns_data or ''
        table = self._TABLE_DIST if is_dist else self._TABLE

        names = []
        vals = []

        for key in values:
            names.append(key)
            vals.append(f"'{values[key]}'")

        sql = f'insert into {table} ({",".join(names)}) values ({",".join(vals)})'
        return sql
