sudo pip install obd
sudo apt-get install bluetooth bluez blueman -y
sed -i -- 's/def __send(self, cmd, delay=None):/def __send(self, cmd, delay=1.0):/g' /usr/local/lib/python2.7/dist-packages/obd/elm327.py
