import importlib

class PayloadManager:
    def __init__(self):
        self.payload_dir = "payloads"

    def load_payload(self, payload_name):
        """Load a specific payload."""
        try:
            payload = importlib.import_module(f"{self.payload_dir}.{payload_name}")
            print(f"Loaded payload: {payload_name}")
            return payload
        except ModuleNotFoundError:
            print(f"Payload '{payload_name}' not found.")
            return None

    def execute_payload(self, payload, target_ip):
        """Execute a loaded payload on a target IP."""
        payload.run(target_ip)
