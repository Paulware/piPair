echo 'Section "InputClass"'>/etc/X11/xorg.conf.d/99-calibration.conf
echo '        Identifier      "calibration"'>>/etc/X11/xorg.conf.d/99-calibration.conf
echo '        MatchProduct    "ADS7846 Touchscreen"'>>/etc/X11/xorg.conf.d/99-calibration.conf
echo '        Option  "Calibration"   "3936 227 268 3880"'>>/etc/X11/xorg.conf.d/99-calibration.conf
echo '        Option  "SwapAxes"      "1"'>>/etc/X11/xorg.conf.d/99-calibration.conf
echo '        Option  "InvertY"       "true"'>>/etc/X11/xorg.conf.d/99-calibration.conf
echo '        Option  "InvertX"       "true"'>>/etc/X11/xorg.conf.d/99-calibration.conf
echo 'EndSection'>>/etc/X11/xorg.conf.d/99-calibration.conf
sed -i 's/dtoverlay=tft35a:rotate=90/dtoverlay=tft35a:rotate=270/' /boot/config.txt
























