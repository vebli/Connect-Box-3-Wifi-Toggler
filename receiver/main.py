from scapy.all import *

ESP32_MAC = ""

def packet_handler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.addr2 == ESP32_MAC:
            print("ESP32 Button Press Detected! Executing code...")
            execute_code()

sniff(iface="", prn=packet_handler, store=0) 

