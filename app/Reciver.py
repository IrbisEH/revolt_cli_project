from scapy.all import *
import socket

from scapy.layers.inet import UDP


def convert(raw_bytes):
    return int.from_bytes(raw_bytes, byteorder='big')


class FieldProps:
    def __init__(self, *args):
        print(args)
        self.name = args[0]
        self.code = args[1]
        self.bytes = args[2]
        self.handler = args[3] if len(args) > 3 else None

class CliReceiver:
    FIELDS = [
        ('octet_delta_count', 'Q', 8),
        ('packet_delta_count', 'Q', 8),
        ('protocol_identifier', 'B', 1),
        ('ip_class_of_service', 'B', 1),
        ('source_port', 'H', 2),
        ('source_ipv4', '4s', 4, lambda x: socket.inet_ntoa(x)),
        ('source_ipv6', '16s', 16, lambda x: socket.inet_ntop(socket.AF_INET6, x)),
        ('destination_port', 'H', 2),
        ('destination_ipv4', '4s', 4, lambda x: socket.inet_ntoa(x)),
        ('destination_ipv6', '16s', 16, lambda x: socket.inet_ntop(socket.AF_INET6, x)),
        ('bgp_source_as_number', 'I', 4),
        ('bgp_destination_as_number', 'I', 4),
        ('flow_start_millisecond', 'Q', 8),
        ('flow_end_millisecond', 'Q', 8),
        ('input_snmp', 'H', 2),
        ('output_snmp', 'H', 2),
        ('ip_version', 'B', 1),
        ('session_id', 'Q', 8),
        ('host', '65535s', None),
        ('protocol_code', 'H', 2),
        ('login', '65535s', None),
        ('post_nat_source_ipv4', '4s', 4, lambda x: socket.inet_ntoa(x)),
        ('post_nat_source_port', 'H', 2),
        ('frgmt_delta_packs', 'H', 2),
        ('repeat_delta_pack', 'H', 2),
        ('packet_deliver_time', 'I', 4),
        ('bridge_vchannel_num', 'H', 2),
        ('vlan_id', 'H', 2),
        ('post_vlan_id', 'H', 2),
        ('mpls_labels', '65535s', None),
        ('original_tos', 'B', 1),
        ('dropped_bytes', 'Q', 8),
        ('dropped_packets', 'Q', 8)
    ]

    FIELDS_TO_READ = 1

    FMT = '>'
    OFFSET = 0

    def __init__(self, intfs=None, type=None, port=None):
        self.intfs = intfs
        self.type = type
        self.port = port

    def run(self):
        print('--- starting receiver ---')
        sniff(iface=self.intfs, filter=f"{self.type} port {str(self.port)}", prn=self.packet_handler)

    def packet_handler(self, packet):
        checks = [
            UDP in packet,
            IP in packet,
            'NetflowHeader' in packet,
            'NetflowDataflowsetV9' in packet,
        ]

        raw_data = packet['NetflowDataflowsetV9'].records[0].fieldValue if all(checks) else None

        print(packet['NetflowHeader']['NetflowHeaderV10']['NetflowHeaderV10'])

        # if raw_data:
        #     print(raw_data)
        # else:
        #     packet.show()

        # if raw_data:
            # bytes = raw_data[-8:]
            # bytes = raw_data[-11:-3]
            # print(bytes.hex())
            # print(bytes)
            # print(int.from_bytes(bytes, byteorder='big'))

            # last_8_bytes = raw_data[-16:-8]
            # print(last_8_bytes.hex())  # Вывод в hex-формате
            # print(last_8_bytes)  # Вывод как байты
            # print(int.from_bytes(last_8_bytes, byteorder='big'))  # Как число

            # for i in range(0, self.FIELDS_TO_READ):
            #     props = FieldProps(*self.FIELDS[i])





        # exit()