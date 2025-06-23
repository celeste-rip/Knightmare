# core/knightmare_controller.py
import os
import yaml
import serial
import serial.tools.list_ports
from datetime import datetime

MODULE_PATH = "modules"
LOG_PATH = "logs/knightmare.log"

class KnightmareController:
    def __init__(self):
        self.module_config = None
        self.serial_port = None
        self.serial_connections = []
        self.logging_enabled = True
        self.detect_serial_devices()
        if not os.path.exists("logs"):
            os.makedirs("logs")

    def detect_serial_devices(self):
        ports = serial.tools.list_ports.comports()
        self.serial_connections = [port.device for port in ports]
        return self.serial_connections

    def connect(self, device_path):
        try:
            self.serial_port = serial.Serial(device_path, 115200, timeout=1)
            return f"Connected to {device_path}"
        except Exception as e:
            return f"Failed to connect: {e}"

    def list_modules(self):
        modules = []
        for root, _, files in os.walk(MODULE_PATH):
            for file in files:
                if file.endswith(".yaml"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, MODULE_PATH)
                    with open(full_path, 'r') as f:
                        config = yaml.safe_load(f)
                        modules.append({
                            "path": rel_path[:-5],
                            "name": config['name'],
                            "description": config['description'],
                            "icarus": config.get('icarus', 'N/A')
                        })
        return modules

    def load_module(self, module_path):
        full_path = os.path.join(MODULE_PATH, f"{module_path}.yaml")
        if not os.path.exists(full_path):
            return "Module not found."
        with open(full_path, "r") as f:
            self.module_config = yaml.safe_load(f)
            self.module_config["path"] = module_path
        return f"Loaded module: {self.module_config['name']}"

    def get_module_info(self):
        return self.module_config if self.module_config else "No module loaded."

    def set_option(self, key, value):
        if self.module_config and key in self.module_config['options']:
            self.module_config['options'][key] = value
            return f"Set {key} to {value}"
        return "Invalid option or no module loaded."

    def run_payload(self, payload_name):
        if not self.serial_port:
            return "Serial not connected."
        if not self.module_config:
            return "No module loaded."
        if payload_name not in self.module_config['payloads']:
            return "Invalid payload."
        try:
            self.serial_port.write((payload_name.upper() + '\n').encode())
            response = self.serial_port.readline().decode().strip()
            if self.logging_enabled:
                with open(LOG_PATH, "a") as log_file:
                    log_file.write(f"[{datetime.now()}] {payload_name}: {response}\n")
            return response
        except Exception as e:
            return f"Error running payload: {e}"