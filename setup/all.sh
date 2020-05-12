echo "**********************************"
echo "*          all.sh                *"
echo "**********************************"
cd /home/pi/piPair
touch /home/pi/piPair/mainConfig.txt
chmod 777 *.*
cp /boot/runPython.sh /home/pi/Desktop/runPython.sh
chmod 777 /home/pi/Desktop/runPython.sh
apt-get update
apt-get install bluetooth bluez blueman -y
timedatectl set-timezone America/Chicago
cd /boot
./ssh.sh
./keyboard.sh
./ap.sh
# python3 already has glob3 # pip install glob3
#./runMain.sh
#ifup wlan0 
echo "Done in setup, Using the wifi icon on desktop:turn wifi on, and set wifi country.  Then reboot"


