# knightmare.py - Main CLI Entry Point

import cmd
import importlib
import os
import sys
import yaml
import serial
import serial.tools.list_ports

MODULE_PATH = "modules"

class KnightmareCLI(cmd.Cmd):
    intro = """
╔═╗┬┌─┬┌─┐┌┬┐┬─┐┌─┐┌─┐┬─┐
╠═╣├┴┐││ │ │ ├┬┘│ ││ │├┬┘
╩ ╩┴ ┴┴└─┘ ┴ ┴└─└─┘└─┘┴└─

Knightmare Framework v0.1 (Tengu Edition)
Drones | Robotics | IoT | RF Systems | SDR
ICARUS-Aligned Offensive Toolkit

Type 'help' to begin your hunt.
"""
    prompt = "knightmare> "

    def __init__(self):
        super().__init__()
        self.loaded_module = None
        self.module_config = None
        self.serial_port = None
        self.serial_connections = []
        self.detect_serial_devices()

    def detect_serial_devices(self):
        ports = serial.tools.list_ports.comports()
        print("Detected Serial/USB Devices:")
        for port in ports:
            print(f" - {port.device}: {port.description}")
            self.serial_connections.append(port.device)
        if not ports:
            print(" - No serial devices found.")

    def do_connect(self, line):
        """connect <device_path>: Connect to a serial device (e.g., /dev/ttyUSB0)"""
        try:
            self.serial_port = serial.Serial(line, 115200, timeout=1)
            print(f"Connected to {line}")
        except Exception as e:
            print(f"Failed to connect: {e}")

    def do_use(self, line):
        """use <module_path>: Load a module for exploitation"""
        path = os.path.join(MODULE_PATH, line)
        if not os.path.exists(f"{path}.yaml"):
            print("Module not found.")
            return
        with open(f"{path}.yaml", "r") as f:
            config = yaml.safe_load(f)
            self.loaded_module = line
            self.module_config = config
            print(f"Loaded module: {config['name']}")
            print(f"Description: {config['description']}")
            print(f"ICARUS Pillar: {config.get('icarus', 'N/A')}")
            print("Options:")
            for opt in config['options']:
                print(f"  - {opt}")
            print("Payloads:")
            for p in config['payloads']:
                print(f"  - {p}")

    def do_list(self, line):
        """list [--icarus <pillar>]: Show all available modules, optionally filtered by ICARUS pillar"""
        filter_pillar = None
        if line.startswith("--icarus"):
            parts = line.split()
            if len(parts) == 2:
                filter_pillar = parts[1].upper()

        print("Available modules:")
        for root, dirs, files in os.walk(MODULE_PATH):
            for file in files:
                if file.endswith(".yaml"):
                    rel_path = os.path.relpath(os.path.join(root, file), MODULE_PATH)
                    try:
                        with open(os.path.join(MODULE_PATH, rel_path), 'r') as f:
                            config = yaml.safe_load(f)
                            if not filter_pillar or config.get('icarus', '').upper() == filter_pillar:
                                print(f"  - {rel_path[:-5]} [{config.get('icarus', 'N/A')}]")
                    except Exception:
                        continue

    def do_info(self, line):
        """info: Display information about the currently loaded module"""
        if self.module_config:
            config = self.module_config
            print(f"Module: {config['name']}")
            print(f"Description: {config['description']}")
            print(f"ICARUS Pillar: {config.get('icarus', 'N/A')}")
            print("Options:")
            for opt in config['options']:
                print(f"  - {opt}")
            print("Payloads:")
            for p in config['payloads']:
                print(f"  - {p}")
        else:
            print("No module loaded.")

    def do_set(self, line):
        """set <option> <value>: Set an option for the current module"""
        if not self.module_config:
            print("No module loaded.")
            return
        try:
            option, value = line.split()
            self.module_config['options'][option] = value
            print(f"Set {option} to {value}")
        except ValueError:
            print("Usage: set <option> <value>")
        except KeyError:
            print(f"Invalid option: {option}")

    def do_show(self, line):
        """show options/payloads: Show current module options or payloads"""
        if not self.module_config:
            print("No module loaded.")
            return
        if line == "options":
            for opt, val in self.module_config['options'].items():
                print(f"{opt} = {val}")
        elif line == "payloads":
            for p in self.module_config['payloads']:
                print(p)
        else:
            print("Usage: show options | show payloads")

    def do_run(self, line):
        """run <payload>: Execute the selected payload against connected serial device"""
        if not self.serial_port:
            print("No serial connection. Use 'connect' first.")
            return
        if not self.module_config:
            print("No module loaded. Use 'use <module>' first.")
            return
        payload = line.strip()
        if payload not in self.module_config.get('payloads', []):
            print(f"Invalid payload: {payload}")
            return
        try:
            command = payload.upper() + '\n'
            self.serial_port.write(command.encode())
            print(f"Sent command: {command.strip()}")
            response = self.serial_port.readline().decode().strip()
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error executing payload: {e}")

    def do_icarus(self, line):
        """icarus <pillar>: Display context or guidance for ICARUS pillars (I, C, A, R, U, S)"""
        descriptions = {
            'I': 'Integrated Threat Intelligence: Adversary profiling, CVEs, telemetry, threat feeds.',
            'C': 'Cybersecurity TTPs: ATT&CK tactics adapted for drones/robots/IoT.',
            'A': 'Aerial and Aquatic Defense: GPS spoofing, anti-jamming, telemetry hijack.',
            'R': 'Robotic System Resilience: Hardening firmware/software, recovery protocols.',
            'U': 'Unmanned System Operations: SOP enforcement, comm security, system auth.',
            'S': 'Systems Monitoring & Response: Anomaly detection, alerts, C2 feedback loops.'
        }
        pillar = line.strip().upper()
        if pillar in descriptions:
            print(f"[{pillar}] {descriptions[pillar]}")
        else:
            print("Usage: icarus <I|C|A|R|U|S>")

    def do_exit(self, line):
        """exit: Exit the framework"""
        return True

if __name__ == '__main__':
    if not os.path.exists(MODULE_PATH):
        os.makedirs(MODULE_PATH)
    KnightmareCLI().cmdloop()
