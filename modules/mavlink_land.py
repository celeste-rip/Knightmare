# modules/mavlink_land.py

from pymavlink import mavutil

def run(target_ip):
    """Force the drone to land."""
    print(f"Connecting to target drone at {target_ip}...")
    master = mavutil.mavlink_connection(f'udp:{target_ip}:14550')
    
    # Wait for connection confirmation
    master.wait_heartbeat()
    print("Heartbeat received. Connected to the drone.")
    
    # Send LAND command
    master.mav.command_long_send(
        master.target_system,            # target_system
        master.target_component,         # target_component
        mavutil.mavlink.MAV_CMD_NAV_LAND,  # Command: NAV_LAND
        0,                               # Confirmation
        0, 0, 0, 0,                      # Params not used for LAND
        0, 0, 0                          # Params not used for LAND
    )
    print("LAND command sent to the drone.")
