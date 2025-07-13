import subprocess

def discover_rtsp_streams(subnet="192.168.1.0/24"):
    try:
        result = subprocess.check_output(f"nmap -p 554 --open {subnet}", shell=True).decode()
        return [line.split()[-1] for line in result.splitlines() if "Nmap scan report for" in line]
    except Exception as e:
        print(f"Camera discovery error: {e}")
        return []
