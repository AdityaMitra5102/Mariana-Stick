import subprocess
import re

def signal_to_bars(dbm):
    """Convert signal strength (dBm) to 1–5 bars."""
    if dbm >= -50:
        return 5
    elif dbm >= -60:
        return 4
    elif dbm >= -70:
        return 3
    elif dbm >= -80:
        return 2
    else:
        return 1

def scan_wifi(interface="wlan0"):
    try:
        output = subprocess.check_output(["sudo", "iwlist", interface, "scan"], text=True)
    except subprocess.CalledProcessError as e:
        print("Failed to scan WiFi:", e)
        return []

    networks = []
    current = {}

    for line in output.splitlines():
        line = line.strip()

        if "Cell" in line:
            if current:
                networks.append(current)
            current = {}

        ssid_match = re.search(r'ESSID:"(.*)"', line)
        signal_match = re.search(r'Signal level=(-?\d+) dBm', line)
        enc_match = re.search(r'Encryption key:(on|off)', line)

        if ssid_match:
            current["SSID"] = ssid_match.group(1)
        if signal_match:
            dbm = int(signal_match.group(1))
            current["Signal Bars"] = signal_to_bars(dbm)
        if enc_match:
            current["Password Required"] = enc_match.group(1) == "on"

    if current:
        networks.append(current)

    return [net for net in networks if net.get("SSID")]
    

def connect_wifi(ssid, password, interface="wlan0"):
    try:
        # Delete any existing connection for this SSID (optional, helps avoid conflicts)
        subprocess.run(["nmcli", "connection", "delete", ssid], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Add and activate new wifi connection
        result = subprocess.run(
            ["nmcli", "device", "wifi", "connect", ssid, "password", password, "ifname", interface],
            check=True, capture_output=True, text=True
        )
        print(f"Connected to {ssid} successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to {ssid}: {e.stderr.strip()}")
        return False

def disconnect_wifi(ssid, interface="wlan0"):
    try:
        # Delete any existing connection for this SSID (optional, helps avoid conflicts)
        subprocess.run(["nmcli", "connection", "delete", ssid], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"Disconnected from {ssid} successfully.")
        return True
    except subprocess.CalledProcessError as e:
        
        return False


def get_connected_ssid(interface="wlan0"):
    try:
        result = subprocess.run(
            ["nmcli", "-t", "-f", "ACTIVE,SSID,DEVICE", "device", "wifi"],
            capture_output=True, text=True, check=True
        )
        for line in result.stdout.strip().split('\n'):
            active, ssid, dev = line.split(':', 1)[0], line.rsplit(':', 1)[0].split(':', 1)[1], line.rsplit(':', 1)[1]
            if active == 'yes' and dev == interface:
                return ssid
        return None
    except Exception:
        return None

def is_ethernet_connected(interface="eth0"):
    try:
        result = subprocess.run(
            ["cat", f"/sys/class/net/{interface}/carrier"],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip() == "1"
    except Exception:
        return False

