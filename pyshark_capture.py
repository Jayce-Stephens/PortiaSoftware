import pyshark
import json
from pathlib import Path
from flask import Flask, jsonify

app = Flask(__name__)


def genesis():
    interface = 'en0'
    pcap_file = 'capture011.pcap'
    packetsData = []


    # Start capturing packets
    print("Starting capture...")
    capture = pyshark.LiveCapture(interface=interface, output_file=pcap_file)
    capture.sniff(packet_count=10000)
    capture.close()
    print("Capture finished. Packets saved to", pcap_file)
    return ("Capture complete!")
genesis()

