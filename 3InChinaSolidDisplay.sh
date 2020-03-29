# Install 3.5 tft  
cd /home/
sudo rm -rf LCD-show
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/

#Note this script should only run once....More than once will add extra ":rotate=270" to /boot/config.txt
#sed -i 's/dtoverlay=tft35a:rotate=90/dtoverlay=tft35a:rotate=270/' /boot/config.txt
#echo "dtoverlay=tft35a:rotate=270">>/boot/config.txt
#echo '  Option "InvertY" "true"'
# next command will reboot the display
sudo ./LCD35-show
# sed -i 's/Option  "SwapAxes"      "1"/Option  "SwapAxes"      "0"/' /etc/X11/xorg.conf.d/99-calibration.conf
cd /boot
