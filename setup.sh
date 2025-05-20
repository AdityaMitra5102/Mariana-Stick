sudo apt update
sudo apt -y upgrade
echo "deb [trusted=yes] https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu/ jammy main" | sudo tee /etc/apt/sources.list.d/deadsnakes-ubuntu-ppa-lunar.list
sudo apt update
sudo apt install -y python3.12
sudo rm -rf $(which python3)
sudo ln -sT $(which python3.12) /usr/bin/python3
curl https://bootstrap.pypa.io/get-pip.py | python3
curl https://AdityaMitra5102.github.io/Project-Mariana/setup.sh | sudo sh
sudo service mariana stop
python3 -m pip install -r /etc/mar/Project-Mariana/requirements.txt --break-system-package --upgrade
sudo python3 -m pip install -r /etc/mar/Project-Mariana/requirements.txt --break-system-package --upgrade
sudo service mariana restart

cd /etc/mar
git clone https://github.com/AdityaMitra5102/Mariana-Stick.git
cd Mariana-Stick
sudo cp -f config.txt /etc/firmware/config.txt
sudo cp -f cmdline.txt /etc/firmware/cmdline.txt
sudo cp -f modules /etc/modules
sudo cp -f usb-gadget.sh /usr/local/sbin/usb-gadget.sh
sudo chmod +x /usr/local/sbin/usb-gadget.sh
sudo cp -f usbgadget.service /lib/systemd/system/usbgadget.service
sudo systemctl daemon-reload
sudo systemctl enable usbgadget.service

sudo nmcli con add type bridge ifname br0
sudo nmcli con add type bridge-slave ifname usb0 master br0
sudo nmcli con add type bridge-slave ifname usb1 master br0
sudo nmcli connection modify bridge-br0 ipv4.method manual ipv4.addresses 10.55.0.1/24
sudo apt install -y dnsmasq
sudo cp -f br0 /etc/dnsmasq.d/br0

sudo apt install -y apache2
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_balancer
sudo a2enmod lbmethod_byrequests
sudo cp -f 000-default.conf /etc/apache2/sites-enabled/000-default.conf

sudo cp -f wifihandler.service /lib/systemd/system/wifihandler.service
sudo systemctl daemon-reload
sudo systemctl enable wifihandler.service
