import serial

ser = serial.Serial("COM5", 9600, timeout=1)

while True:
    line = ser.readline().decode("ascii", errors="replace").strip()
    if line:
        print(line)
