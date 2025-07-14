import socket
def scan_subnet(subnet="192.168.1.", port=554):
    active_hosts = []
    for i in range(1, 255):
        ip = f"{subnet}{i}"
        s = socket.socket()
        s.settimeout(0.5)
        try:
            s.connect((ip, port))
            active_hosts.append(ip)
        except:
            pass
        finally:
            s.close()
    return active_hosts

import socket

def is_port_open(ip, port=554, timeout=2):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False
