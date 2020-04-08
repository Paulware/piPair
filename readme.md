<h1>Raspberry Pi Pairing project</h1>
This project is based on the 10 in Maker Shack laptop: <img src="images/makerShack.jpg"><br>
But can also be tested on a LAN network with windows pcs.<p>
The idea is to connect 2 (or more) raspberry pi using the pi's wifi chip and then chat or play games.
<br>Recommended bluetooth keyboard (Logitech K380):<br>
<img src="images/k380.jpg">
<p>
Code is written in python in a module fashion so that students can add more games.<br>
Currently the games that are supported are:
<ul>
  <li>Chat (not really a game but the basis of all game communication)</li>
  <li>Tic Tac Toe</li>
  <li>Checkers</li>
  <li>Chess</li>
  <li>Tank (battle)</li>
  <li>Panzer Leader (To be implemented)</li>
</ul>
<h1>Setup</h1>
<ul>
  <li>Download the latest raspbian image from: <a href="https://www.raspberrypi.org/downloads/raspbian">https://www.raspberrypi.org/downloads/raspbian</a></li>
  <li>Copy the .img to an 8gb sd card using <a href="https://www.sourceforge.net/projects/win32diskimager">win32diskimager</a></li>
  <li>Copy the setup directory in this github repo to the sd card (this will be later referred to as /boot area)</li>
  <li>Connect an internet cable to the raspberry pi</li>
  <li>Place the sd card in the raspberry pi and power up</li>
  <li>Open a line terminal and enter the commands</li>
  <ul>
     <li>sudo bash</li>
     <li>cd /boot/setup</li>
     <li>./all.sh</li>
     <li>Turn on wifi (via desktop icon)</li>
     <li>reboot</li>
     <li>A wifi accesspoint with SSID=Walker and password=ABCD1234. Should appear</li>
  </ul>
</ul>

<h1>Keyboard Logitech K380 Setup</h1>
<ul>
   <li>Press and hold yellow key 1 until it blinks</li>
   <li>Using the bluetooth icon on the raspberry pi bt icon</li>
     <ul>
       <li>Turn on bluetooth</li>
       <li>Make Discoverable</li>
       <li>Select K380 Keyboard in list of devices</li>
     </ul>
     <li>Enter the number in the K380 keyboard as directed by the raspberry pi</li>
</ul>

<h1>Test Setup</h1>
<ul>
   <li>Open a line terminal
   <li>Enter the commands:</li>
   <ul>
      <li>sudo bash</li>
      <li>cd /boot</li>
      <li>python main.py</li>
      <li>A python program should open</li>
   </ul>
</ul>