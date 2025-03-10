import subprocess

def capture_packets(interface="eth0", count=10, filter_expr=""):
    cmd = ["tcpdump", "-i", interface, "-c", str(count), "-nn"]
    
    if filter_expr:
        cmd.append(filter_expr)

    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in iter(process.stdout.readline, ''):
            print(line.strip())

    except KeyboardInterrupt:
        print("\nCapture stopped.")

# Example usage: Capture 5 TCP packets on eth0
capture_packets(interface="eth0", count=5, filter_expr="tcp")