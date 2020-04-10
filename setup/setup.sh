echo "Run all scripts to configure the pi"
if [ $(id -u) -ne 0 ]; then echo "You must use sudo: sudo ./all.sh"; exit 1; fi
cd /home/pi
git clone https://www.github.com/Paulware/piPair
cd /home/pi/piPair
touch mainConfig.txt
chmod 777 *.*
cd /boot/
# Copy setup files to /boot 
cp /home/pi/piPair/setup/*.sh .
cp /boot/runPython.sh /home/pi/Desktop/runPython.sh
chmod 777 /home/pi/Desktop/runPython.sh
apt-get update
./ssh.sh
./keyboard.sh
./timezone.sh
# echo "dns-nameservers 8.8.8.8 8.8.4.4" >> /etc/network/interfaces
./ap.sh
pip install glob3
./runMain.sh
cp runPython.sh /home/pi/Desktop/runPython.sh
apt-get install bluetooth bluez blueman -y
#ifup wlan0
echo "Done in setup, Using the wifi icon on desktop:turn wifi on, and set wifi country.  Then reboot"

