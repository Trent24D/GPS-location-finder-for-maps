# GPS-location-finder-for-maps
Using a raspberry pi and a usb gps dongle, this program adds gps data to a txt. take this data and upload to mymaps to get a cool map of where you were on vacation

To make it yourself, i would get a raspberry pi zero 2w, a basic gps/glonass usb dongle, and a small power supply

when you first plug in the raspberry pi, run 'ls /dev/tty*' to find the gps device (you might need to enable the serial port with 'sudo raspi-config' and enable serial port hardware.
after listing the terminal devices, find the USB one (maybe labeled "/dev/ttyUSB0"
in current_location_pi.py, change the variable comPort to what ever the device is pathed. 

with root permissions in terminal, type 'sudo nano /etc/rc.local'
then paste in the line 'sudo python /home/pi/current_location_pi.py &'

make sure you install the packages pyserial and pynmea2
good luck!
