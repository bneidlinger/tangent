# geiger_logger.py
import RPi.GPIO as GPIO, time, datetime, collections

PIN = 17          # change if you used another pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.IN)

window = collections.deque(maxlen=60)   # 1-min window of timestamps

def pulse(channel):
    window.append(time.time())

GPIO.add_event_detect(PIN, GPIO.RISING, callback=pulse, bouncetime=1)

print("Logging... Ctrl-C to stop")
try:
    while True:
        time.sleep(1)
        cpm = len([t for t in window if time.time()-t < 60])
        print(f"{datetime.datetime.now():%H:%M:%S}  CPM: {cpm:3}")
except KeyboardInterrupt:
    GPIO.cleanup()