echo "**********************************"
echo "*          all.sh                *"
echo "**********************************"
cd /home/pi/piPair
touch /home/pi/piPair/mainConfig.txt
chmod 777 *.*
cp /boot/runPython.sh /home/pi/Desktop/runPython.sh
chmod 777 /home/pi/Desktop/runPython.sh
apt-get update
./ssh.sh
./keyboard.sh
timedatectl set-timezone America/Chicago
./ap.sh
pip install glob3
./runMain.sh
apt-get install bluetooth bluez blueman -y
#ifup wlan0 
echo "Done in setup, Using the wifi icon on desktop:turn wifi on, and set wifi country.  Then reboot"


