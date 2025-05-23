sudo apt update

sudo apt install -y apache2
sudo apt install -y dnsmasq
sudo apt install -y git
sudo apt install -y ufw

echo "deb [trusted=yes] https://ppa.launchpadcontent.net/deadsnakes/ppa/ubuntu/ jammy main" | sudo tee /etc/apt/sources.list.d/deadsnakes-ubuntu-ppa-lunar.list
sudo apt update
sudo apt install -y python3.12

sudo ln -sT $(which python3.12) /usr/bin/python3.12
curl https://bootstrap.pypa.io/get-pip.py | python3.12
sudo apt update
sudo apt install -y --fix-broken

sudo mkdir -p /etc/mar
sudo touch /etc/mar/test
chmod -R 777 /etc/mar
cd /etc/mar
sudo apt-get update
rm -rf /etc/mar/Project-Mariana

git clone https://github.com/AdityaMitra5102/Project-Mariana.git


sudo python3.12 -m pip install -r /etc/mar/Project-Mariana/requirements.txt --break-system-package --upgrade

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


sudo nmcli con add type bridge ifname br0
sudo nmcli con add type bridge-slave ifname eth0 master br0
sudo nmcli connection modify bridge-br0 ipv4.method manual ipv4.addresses 10.55.0.1/24
sudo cp -f br0 /etc/dnsmasq.d/br0
sudo touch /etc/mar/stickmode

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

sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow in on eth0
sudo ufw allow in on br0
sudo ufw allow 22
sudo ufw enable --force
sudo ufw status

sudo poweroff
