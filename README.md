# GPS-location-finder-for-maps
Using a raspberry pi and a usb gps dongle, this program adds gps data to a txt. take this data and upload to mymaps to get a cool map of where you were on vacation

To make it yourself, i would get a raspberry pi zero 2w, a basic gps/glonass usb dongle, and a small power supply. When you set up the pi, make sure remote SSH is on to allow easy debugging on a different machine

when you first plug in the raspberry pi, run 'ls /dev/tty*' to find the gps device (you might need to enable the serial port with 'sudo raspi-config' and enable serial port hardware.
after listing the terminal devices, find the USB one (maybe labeled "/dev/ttyUSB0"
in current_location_pi.py, change the variable comPort to what ever the device is pathed. 

i would recommend creating a new folder to put all teh files into (py file and txt)

to get the program to run as soon as power is recieved, you can change the rc.local file, find a tutorial online, there are several steps which will differ based on how the pi was setup. 

open up two new files, current_location_pi.py and a text file which i names gps.txt
with python, run python -m pip and install the libraries serial and pynmea2

to run manually, simply run the python file with python current_location_pi.py 
gps data is given in the following format: 

System Date, Time (UTC), latitude, longitude, speedKmh, heading, altitude

After the data is collected, run plot_data.py, and a html file with the plotted points on the map should appear. Make sure to change the home lat and lon to make it center where you would like. 

Here is an image of what it looks like 
![Port Hueneme Plotted Map Segment](https://github.com/Trent24D/GPS-location-finder-for-maps/blob/e81e7b0c52e9e19f2313863af572e9ca608678e5/Port%20Hueneme%20Data.png)
