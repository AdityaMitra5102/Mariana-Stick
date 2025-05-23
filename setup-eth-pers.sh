sudo nmcli con add type bridge ifname br0
sudo nmcli con add type bridge-slave ifname eth0 master br0
sudo nmcli connection modify bridge-br0 ipv4.method manual ipv4.addresses 10.55.0.1/24
sudo touch /etc/mar/ethmode

curl https://AdityaMitra5102.github.io/Mariana-Stick/setup-persistent.sh | sudo bash
