# Mariana's Qubit On A Stick


# ⚠️DO NOT CONFIGURE WIFI BEFORE INSTALLATION. IT WILL MESS UP THE USB CONFIGURATION. DO NOT CONFIG WIFI FROM RASPBERRY PI IMAGER EITHER

# I know its difficult to connect to RPi Zero W, RPi Zero 2 W without Wifi due to the lack of Ethernet support but please use an USB Ethernet adapter instead.

If there is no other way to connect than Wi-Fi, extreme difficulties need extreme measures. Edit the file /boot/firmware/cmdline.txt and remove the `cfg80211.ieee80211_regdom=*` statement from the end. DO NOT REBOOT AFTER THIS CHANGE since it will not connect to WiFi after that. Run the installation after making this change. Not before that. And if you still mess up, well reinstall Raspi OS and try again.

# Use RPi OS Bookwarm. Older versions will not work. Go for Lite version since GUI is not needed.

# USB Setup (Preferred)
## Ephemeral setup
```
curl https://AdityaMitra5102.github.io/Mariana-Stick/setup-ephemeral.sh | sudo bash
```

## Persistent setup
```
curl https://AdityaMitra5102.github.io/Mariana-Stick/setup-persistent.sh | sudo bash
```

# Ethernet Setup
⚠️ Connect only to host. Not to a network swtich directly.
## Ephemeral setup
```
curl https://AdityaMitra5102.github.io/Mariana-Stick/setup-eth-eph.sh | sudo bash
```

## Persistent setup
```
curl https://AdityaMitra5102.github.io/Mariana-Stick/setup-eth-pers.sh | sudo bash
```
