import subprocess
import pyshark_capture
import iso_forest
import model_test
import ip_blocker

def testcommand(command):
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        print("Output:\n", result)
    except Exception as e:
        print("Error executing command: {e}")

# Test the commands
pyshark_capture.genesis()
fileP = '/Volumes/HUNTER/PortiaSoftware/database/capture011.pcap'
command = "tshark -r " + fileP + " -T fields -e frame.number -e ipv6.src -e ipv6.dst -e frame.len -e tcp.dstport -E header=y -E separator=, -E quote=d -E occurrence=f > capturedData001.csv"
testcommand(command)
model_test.main("capturedData001.csv")
ip_blocker.blockip('dc84b8dc-96a0-4cf3-8a43-908a9361f6d6', '/Volumes/HUNTER/PortiaSoftware/database/anomalous_IPs.txt')

