#!/usr/bin/env python3
"""
simple_port_scanner.py
Basic TCP port scanner for educational use.

Usage examples:
  python simple_port_scanner.py              # scans localhost ports 1-1024
  python simple_port_scanner.py 192.168.1.10 # scans host 192.168.1.10 ports 1-1024
  python simple_port_scanner.py example.com 1 65535  # scan full port range (slow)

IMPORTANT: Only scan systems you own or have permission to test.
"""

import socket
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---- Configuration ----
DEFAULT_HOST = "127.0.0.1"
DEFAULT_START_PORT = 1
DEFAULT_END_PORT = 1024
TIMEOUT_SECONDS = 0.5      # socket timeout for each connect
MAX_WORKERS = 100          # concurrency level (thread pool)

def scan_port(host: str, port: int, timeout: float = TIMEOUT_SECONDS) -> bool:
    """Return True if TCP port is open (connect succeeds), False otherwise."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))  # returns 0 on success
            return result == 0
    except Exception:
        return False

def scan_ports(host: str, start_port: int, end_port: int):
    """Scan a range of ports and return a sorted list of open ports."""
    open_ports = []
    # Use a ThreadPoolExecutor to speed up scanning while keeping code simple.
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_port = {
            executor.submit(scan_port, host, port): port
            for port in range(start_port, end_port + 1)
        }
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                if future.result():
                    open_ports.append(port)
                    print(f"[+] Open: {port}")
            except Exception as e:
                # unexpected exception for a port; ignore but print debug optionally
                pass

    open_ports.sort()
    return open_ports

def parse_args(argv):
    """Return (host, start_port, end_port)."""
    if len(argv) == 1:
        return DEFAULT_HOST, DEFAULT_START_PORT, DEFAULT_END_PORT
    elif len(argv) == 2:
        return argv[1], DEFAULT_START_PORT, DEFAULT_END_PORT
    elif len(argv) == 4:
        host = argv[1]
        try:
            p1 = int(argv[2])
            p2 = int(argv[3])
            if not (1 <= p1 <= 65535 and 1 <= p2 <= 65535 and p1 <= p2):
                raise ValueError
            return host, p1, p2
        except ValueError:
            print("Port numbers must be integers between 1 and 65535, with start <= end.")
            sys.exit(1)
    else:
        print("Usage: python simple_port_scanner.py [host] [start_port end_port]")
        sys.exit(1)

def main():
    host, start_port, end_port = parse_args(sys.argv)

    print("=== Basic Port Scanner ===")
    print(f"Target: {host}")
    print(f"Ports: {start_port} - {end_port}")
    print("Only scan systems you own or have permission to test.\n")

    # Try to resolve hostname to IP (optional)
    try:
        ip = socket.gethostbyname(host)
        print(f"Resolved {host} -> {ip}\n")
    except socket.gaierror:
        print(f"Unable to resolve host: {host}")
        sys.exit(1)

    open_ports = scan_ports(ip, start_port, end_port)

    print("\n=== Scan complete ===")
    if open_ports:
        print("Open ports found:", ", ".join(str(p) for p in open_ports))
    else:
        print("No open ports found in the scanned range.")

if __name__ == "__main__":
    main()
