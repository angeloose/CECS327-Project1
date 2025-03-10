from scapy import sniff

def packet_callback(packet):
    if packet.haslayer('IP'):
        log = f"{packet.time}, {packet.src}, {packet.dst}, {len(packet)} bytes\n"
        print(log)
        with open("network_log.txt", "a") as file:
            file.write(log)

sniff(filter="ip", prn=packet_callback, store=0)