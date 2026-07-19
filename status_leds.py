#!/usr/bin/env python3
"""
Status LED monitor for Raspberry Pi Zero W (Raspberry Pi OS Trixie).

GPIO4  - Mariana : ON if GET http://localhost:8000/active   returns body text "true"
GPIO17 - Wifi     : ON if GET http://localhost:5000/wifiname returns HTTP 200
GPIO27 - dhcp     : ON if `ip neighbor show dev br0` lists a resolved host in 10.55.0.2-10.55.0.6
GPIO22 - power    : ON as soon as the program starts (stays on)

All LEDs are driven via PWM at reduced brightness since no current-limiting
resistors are in use. Every check re-runs every 3 seconds; any LED whose
condition is no longer satisfied is turned off (except "power").

Requires:
    pip install gpiozero requests rpi-lgpio
    (rpi-lgpio provides the lgpio backend gpiozero needs on Trixie)
"""

import subprocess
import time
import logging

import requests
from gpiozero import PWMLED

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

POLL_INTERVAL_SEC = 1
HTTP_TIMEOUT_SEC = 3

# Brightness (0.0 - 1.0). Kept low since no resistors are used on the LEDs.
BRIGHTNESS = 0.25

MARIANA_URL = "http://localhost:8000/active"
WIFI_URL = "http://localhost:5000/wifiname"

DHCP_RANGE_LAST_OCTET = range(2, 7)  # 10.55.0.2 .. 10.55.0.6 (inclusive)
DHCP_SUBNET_PREFIX = "10.55.0."
NEIGHBOR_INTERFACE = "br0"

GPIO_MARIANA = 4
GPIO_WIFI = 17
GPIO_DHCP = 27
GPIO_POWER = 22

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("status_leds")


# ---------------------------------------------------------------------------
# Condition checks
# ---------------------------------------------------------------------------

def check_mariana() -> bool:
    """GET MARIANA_URL, ON if body text is exactly 'true'."""
    try:
        resp = requests.get(MARIANA_URL, timeout=HTTP_TIMEOUT_SEC)
        return resp.text.strip().lower() == "true"
    except requests.RequestException as exc:
        log.debug("Mariana check failed: %s", exc)
        return False


def check_wifi() -> bool:
    """GET WIFI_URL, ON if HTTP status code is 200."""
    try:
        resp = requests.get(WIFI_URL, timeout=HTTP_TIMEOUT_SEC)
        return resp.status_code == 200
    except requests.RequestException as exc:
        log.debug("Wifi check failed: %s", exc)
        return False


def check_dhcp() -> bool:
    """
    ON if `ip neighbor show dev br0` lists any host in the configured
    range with a resolved (non-FAILED/INCOMPLETE) neighbor entry.
    """
    try:
        result = subprocess.run(
            ["ip", "neighbor", "show", "dev", NEIGHBOR_INTERFACE],
            capture_output=True,
            text=True,
            timeout=HTTP_TIMEOUT_SEC,
        )
    except (subprocess.SubprocessError, OSError) as exc:
        log.debug("ip neighbor command failed: %s", exc)
        return False

    if result.returncode != 0:
        log.debug("ip neighbor returned %d: %s", result.returncode, result.stderr.strip())
        return False

    target_ips = {f"{DHCP_SUBNET_PREFIX}{last}" for last in DHCP_RANGE_LAST_OCTET}

    for line in result.stdout.splitlines():
        parts = line.split()
        if not parts:
            continue
        ip = parts[0]
        if ip not in target_ips:
            continue
        state = parts[-1]  # e.g. REACHABLE, STALE, DELAY, PROBE, FAILED, INCOMPLETE
        if state not in ("FAILED", "INCOMPLETE"):
            return True

    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def set_led(led: PWMLED, on: bool) -> None:
    led.value = BRIGHTNESS if on else 0.0


def main() -> None:
    mariana_led = PWMLED(GPIO_MARIANA)
    wifi_led = PWMLED(GPIO_WIFI)
    dhcp_led = PWMLED(GPIO_DHCP)
    power_led = PWMLED(GPIO_POWER)

    # Power LED: on immediately at startup, stays on for the life of the program.
    power_led.value = BRIGHTNESS
    log.info("Power LED on (GPIO %d)", GPIO_POWER)

    try:
        while True:
            mariana_ok = check_mariana()
            wifi_ok = check_wifi()
            dhcp_ok = check_dhcp()

            set_led(mariana_led, mariana_ok)
            set_led(wifi_led, wifi_ok)
            set_led(dhcp_led, dhcp_ok)

            log.info(
                "Mariana=%s Wifi=%s DHCP=%s",
                mariana_ok, wifi_ok, dhcp_ok,
            )

            time.sleep(POLL_INTERVAL_SEC)

    except KeyboardInterrupt:
        log.info("Stopping, turning off LEDs...")
    finally:
        for led in (mariana_led, wifi_led, dhcp_led, power_led):
            led.value = 0.0
            led.close()


if __name__ == "__main__":
    main()
