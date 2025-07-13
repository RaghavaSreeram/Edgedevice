import socket

def scan_ports(ip, port=554, timeout=1):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False
