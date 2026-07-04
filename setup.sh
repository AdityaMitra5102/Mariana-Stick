sudo apt update
#sudo apt -y upgrade
#sudo rpi-update
sudo apt install -y apache2
#sudo apt install -y dnsmasq
sudo apt install -y git

sudo apt install -y python3-pip
sudo apt install -y --fix-broken
sudo apt install -y python3-dev build-essential libffi-dev libssl-dev
sudo mkdir -p /etc/mar
sudo touch /etc/mar/test
chmod -R 777 /etc/mar
cd /etc/mar
sudo apt-get update
rm -rf /etc/mar/Project-Mariana

git clone https://github.com/AdityaMitra5102/Project-Mariana.git


sudo python3 -m pip install -r /etc/mar/Project-Mariana/requirements.txt --break-system-package --upgrade --ignore-installed

sudo mkdir -p /root/Downloads/CargoShip
sudo touch /root/Downloads/CargoShip/CargoShipActive
sudo chmod -R 777 /root/Downloads/CargoShip

cd /etc/mar
sudo rm -rf /etc/mar/Mariana-Stick
git clone https://github.com/AdityaMitra5102/Mariana-Stick.git
cd Mariana-Stick
sudo cp -f mariana.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable mariana

sudo mkdir -p /etc/NetworkManager/dnsmasq-shared.d
sudo apt install -y rpi-usb-gadget
sudo rpi-usb-gadget on
sudo cp -f 92-dns.conf /etc/NetworkManager/dnsmasq-shared.d

sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod proxy_balancer
sudo a2enmod lbmethod_byrequests
sudo a2enmod rewrite
sudo cp -f 000-default.conf /etc/apache2/sites-enabled/000-default.conf
sudo ln -sT /root/Downloads/CargoShip /var/www/cargo

sudo chmod o+rx /root
sudo chmod o+rx /root/Downloads
sudo chmod -R o+rx /root/Downloads/CargoShip
sudo chown -R www-data:www-data /var/www

sudo cp -f wifihandler.service /lib/systemd/system/wifihandler.service
sudo systemctl daemon-reload
sudo systemctl enable wifihandler.service


echo "Installation complete"

#sudo reboot
