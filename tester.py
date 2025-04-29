import subprocess
import pyshark_capture
import model_test
import ip_blocker

def testcommand(command):
    try:
        print(f"Executing command: {command}")
        result = subprocess.check_output(command, shell=True, text=True)
        print("Output:\n", result)
    except Exception as e:
        print("Error executing command: {e}")
        raise

# Test the commands
print("Running pyshark_capture.genesis()...")
pyshark_capture.genesis()

fileP = '/Volumes/HUNTER/PortiaSoftware/capture011.pcap'
command = "tshark -r " + fileP + " -T fields -e frame.number -e ipv6.src -e ipv6.dst -e frame.len -e tcp.srcport -e tcp.dstport -E header=y -E separator=, -E quote=d -E occurrence=f > capturedData001.csv"
print("Running tshark command...")
testcommand(command)

print("Running model_test.main()...")
model_test.main("/Volumes/HUNTER/PortiaSoftware/database/TFTP.csv")

print("Running ip_blocker.blockip()...")
ip_blocker.blockip('dc84b8dc-96a0-4cf3-8a43-908a9361f6d6', '/Volumes/HUNTER/PortiaSoftware/anomalous_ip.txt')

