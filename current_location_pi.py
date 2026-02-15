import serial
import pynmea2
from datetime import datetime, timedelta, timezone

comPort = "/dev/ttyACM0"  # Adjust as needed for your GPS device
baudRate = 9600
outputFile = "gps_parsed.txt"
logInterval = timedelta(seconds=60)

lastLat = None
lastLon = None
lastLogTime = None
firstOutputDone = False

ser = serial.Serial(comPort, baudRate, timeout=1)

with open(outputFile, "a") as f:
    if f.tell() == 0:
        f.write("systemTime,gpsTime,latitude,longitude,speedKmh,heading,altitudeM\n")

    while True:
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

        now = datetime.utcnow()
        logThis = False

        # first output always
        if not firstOutputDone:
            logThis = True
            firstOutputDone = True
            lastLogTime = now

        # log if new fix and coordinates changed
        elif hasFix and (latitude != lastLat or longitude != lastLon):
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
