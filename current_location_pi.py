import serial
import pynmea2
from datetime import datetime, timedelta, timezone
import threading

comPort = "/dev/ttyACM0"  # Adjust as needed for your GPS device
baudRate = 9600
outputFile = "gps_parsed.txt"
logInterval = timedelta(seconds=180)  # Log every 3 minutes

lastLat = None
lastLon = None
lastLogTime = None
firstOutputDone = False

ser = serial.Serial(comPort, baudRate, timeout=1)

stopEvent = threading.Event()

def waitForExit():
    input()
    stopEvent.set()

threading.Thread(target=waitForExit, daemon=True).start()

with open(outputFile, "a") as f:

    f.write("systemTime,gpsTime,latitude,longitude,speedKmh,heading,altitudeM\n")

    while not stopEvent.is_set():
        line = ser.readline().decode("ascii", errors="replace").strip()

        if not line.startswith("$"):
            continue

        try:
            msg = pynmea2.parse(line)
        except pynmea2.ParseError:
            continue

        systemTime = datetime.now(timezone.utc).isoformat()
        latitude = longitude = speedKmh = heading = altitude = "NA"
        gpsTime = "NO_FIX"
        hasFix = False

        if msg.sentence_type == "RMC":
            latitude = msg.latitude
            longitude = msg.longitude
            if msg.status == "A":
                gpsTime = datetime.combine(msg.datestamp, msg.timestamp).isoformat()
                speedKmh = float(msg.spd_over_grnd) * 1.852 if msg.spd_over_grnd else 0
                heading = msg.true_course if msg.true_course else "NA"
                hasFix = True

        elif msg.sentence_type == "GGA":
            if msg.altitude:
                altitude = msg.altitude
            if msg.gps_qual and int(msg.gps_qual) > 0:
                hasFix = True

        now = datetime.now(timezone.utc)
        logThis = False

        # first output always
        if not firstOutputDone:
            logThis = True
            firstOutputDone = True
            lastLogTime = now

        # log if new fix and coordinates changed
        elif hasFix and (latitude != lastLat or longitude != lastLon) and (lastLogTime is None or now - lastLogTime >= logInterval/2):
            logThis = True
            lastLogTime = now

        # log every interval
        elif lastLogTime is None or now - lastLogTime >= logInterval:
            logThis = True
            lastLogTime = now

        if logThis:
            f.write(
                f"{systemTime},{gpsTime},{latitude},{longitude},{speedKmh},{heading},{altitude}\n"
            )
            f.flush()
            print(
                f"{systemTime} | GPS: {gpsTime} | {latitude},{longitude} | "
                f"{speedKmh} km/h | Heading: {heading} | Altitude: {altitude} m"
            )

            if hasFix:
                lastLat = latitude
                lastLon = longitude