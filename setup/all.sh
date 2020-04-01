echo "Run all scripts to configure the pi"
echo "Note: .img used for this should already have a wifi access point setup"
if [ $(id -u) -ne 0 ]; then echo "You must use sudo: sudo ./all.sh"; exit 1; fi
apt-get update
./ssh.sh
./keyboard.sh
./timezone.sh
# echo "dns-nameservers 8.8.8.8 8.8.4.4" >> /etc/network/interfaces
#./obd.sh
./ap.sh
# The next command will do a reboot
# ./3InChinaSolidDisplay.sh
#echo 'makeConf.sh needs to be run after ./3InChinaSolidDisplay.sh'
#./makeConf.sh

