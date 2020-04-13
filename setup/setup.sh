echo "Run all scripts to configure the pi"
if [ $(id -u) -ne 0 ]; then echo "You must use sudo: sudo ./setup.sh"; exit 1; fi
cd /home/pi
git clone https://www.github.com/Paulware/piPair
cd /boot/ 
cp /home/pi/piPair/setup/*.sh .
./all.sh
