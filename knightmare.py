from core import exploit_loader, payload_manager
from core.logger import Logger

class Knightmare:
    def __init__(self):
        self.exploit_loader = exploit_loader.ExploitLoader()
        self.payload_manager = payload_manager.PayloadManager()
        self.logger = Logger()
        self.loaded_exploit = None

    def start_cli(self):
        print("Knightmare Exploit Toolkit")
        print("Type 'help' for commands.")

        while True:
            command = input("knightmare> ").strip().lower()
            if command == "help":
                self.display_help()
            elif command == "list":
                self.exploit_loader.list_exploits()
            elif command.startswith("load"):
                _, exploit_name = command.split()
                self.loaded_exploit = self.exploit_loader.load_exploit(exploit_name)
            elif command.startswith("run"):
                if not self.loaded_exploit:
                    print("No exploit loaded.")
                    continue
                _, target_ip = command.split()
                self.loaded_exploit.run(target_ip)
            elif command == "exit":
                print("Exiting Knightmare...")
                break
            else:
                print("Unknown command. Type 'help' for a list of commands.")

    def display_help(self):
        print("Commands:")
        print("  list              - List available exploits")
        print("  load [exploit]    - Load an exploit")
        print("  run [target_ip]   - Run loaded exploit on target IP")
        print("  exit              - Exit the framework")

# Run framework if executed directly
if __name__ == "__main__":
    knightmare = Knightmare()
    knightmare.start_cli()
