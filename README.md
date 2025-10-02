# simple-port-scanner

Beginner-friendly Python TCP port scanner — simple, fast, and for educational use only.

**Warning:** Only scan machines you own or have explicit permission to test.

## Features
- Simple, easy-to-read implementation (great for learning).
- Concurrent scanning using a thread pool.
- Configurable port range, timeout, and concurrency.

## Requirements
- Python 3.7+

No external packages required.

## Usage
```bash
# default: scan localhost ports 1-1024
python simple_port_scanner.py

# scan a remote host
python simple_port_scanner.py 192.168.1.10

# scan a full range (slow)
python simple_port_scanner.py example.com 1 65535

# change timeout and concurrency
python simple_port_scanner.py example.com 1 1024 --timeout 0.2 --workers 200
