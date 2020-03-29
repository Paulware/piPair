import obd

print ("nano /etc/systemd/system/dbus-org.bluez.service" )
print ("ExecStart=/usr/lib/bluetooth/bluetoothd -C" )
print ("ExecStartPost=/usr/bin/sdptool add SP" )

print ("Before calling this python execute the commands:" )
#print ("rfcomm bind rfcomm1 00:1d:A5:01:C8:10" )
#print ("You can try rfcomm release all before if you like" )

#ports = obd.scan_serial()
#print ("serial ports:" )
#print ports 

connection = obd.OBD("/dev/rfcomm0", protocol="3") # , fast=False, timeout=10) # auto-connects to USB or RF port

cmd = obd.commands.RPM # select an OBD command (sensor)

response = connection.query(cmd, force=True) # send the command, and parse the response

print(response.value) # returns unit-bearing values thanks to Pint
#print(response.value.to("mph")) # user-friendly unit conversions

#print ("Current status: " ) 
#print (obd.status()) 
