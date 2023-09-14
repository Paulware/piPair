EDITOR=vim
PASSWD=/etc/passwd
RED='\033[0;41;30m'
STD='\033[0;0;39m'
pause(){
  read -p "Press [Enter] key to continue.." fackEnterKey
}

update_file() {
  cat $1 | sed -e "s/$2/$3/" > /f
  mv /f $1
}

menu(){
  echo "one() called"
  cd /boot
  python menuGrid.py
     pause
}

ap(){
  echo "ap() called...use ap.sh for now..."
     pause 
}

ssh() {
  echo "ssh() called"
  # permit ssh login  
  sudo touch /boot/ssh
  # permit root ssh login
  update_file /etc/ssh/sshd_config "#PermitRootLogin prohibit-password" "PermitRootLogin yes"
  sudo echo "root:raspberry" | sudo chpasswd
  sudo echo "pi:goaway" | sudo chpasswd
  echo "ssh.sh completed"  
}

show_menus(){
   clear
   echo "~~~~~~~~~~~~~~~~~~"
   echo " M A I N - M E N U"
   echo "~~~~~~~~~~~~~~~~~~"
   echo "1. mosquitto install"
   echo "2. Set up wifi access point"
   echo "3. Set up ssh"
   echo "q.  exit"
}   

mosquitto () {
   sudo apt-get install mosquitto
   sudo pip install paho-mqtt
   sudo echo "listener 1883" >> /etc/mosquitto/mosquitto.conf
   sudo echo "allow_anonymous true" >> /etc/mosquitto/mosquitto.conf
   sudo systemctl restart mosquitto
}

read_options(){
   local choice
   read -p "Enter choice [1..3]" choice
   case $choice in
      1) mosquitto ;;
      2) ap ;;
      3) ssh ;; 
      4) mosquitto ;; 
      q) exit 0;;
      *) echo -e "${RED}Error...${STD}" && sleep 2
   esac
}
while true
do
   show_menus
   read_options
done