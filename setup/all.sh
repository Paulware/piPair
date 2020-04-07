echo "Run all scripts to configure the pi"
echo "Note: .img used for this should already have a wifi access point setup"
if [ $(id -u) -ne 0 ]; then echo "You must use sudo: sudo ./all.sh"; exit 1; fi
cd /home/pi
echo "Still need to make some modes for all.sh to run properly"
git clone https://www.github.com/Paulware/piPair
cd /boot
apt-get update
./ssh.sh
./keyboard.sh
./timezone.sh
# echo "dns-nameservers 8.8.8.8 8.8.4.4" >> /etc/network/interfaces
./ap.sh
pip install glob3


