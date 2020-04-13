cd /home/pi/piPair
touch mainConfig.txt
chmod 777 *.*
cp /boot/runPython.sh /home/pi/Desktop/runPython.sh
chmod 777 /home/pi/Desktop/runPython.sh
apt-get update
./ssh.sh
./keyboard.sh
./timezone.sh
./ap.sh
pip install glob3
./runMain.sh
cp runPython.sh /home/pi/Desktop/runPython.sh
apt-get install bluetooth bluez blueman -y
#ifup wlan0
echo "Done in setup, Using the wifi icon on desktop:turn wifi on, and set wifi country.  Then reboot"


