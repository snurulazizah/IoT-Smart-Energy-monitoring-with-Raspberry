import time
import digitalio
import board

from Adafruit_IO import Client, Feed, RequestError
ADAFRUIT_IO_KEY = 'Your API Key'
# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)

ADAFRUIT_IO_USERNAME = 'Your user name'
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

try: # if we have a 'digital' feed
    digital = aio.feeds('digital')
except RequestError: # create a digital feed
    feed = Feed(name="digital")
    digital = aio.create_feed(feed)
# lamp set up
lamp = digitalio.DigitalInOut(board.D5)
lamp.direction = digitalio.Direction.OUTPUT

while True:
    data = aio.receive(digital.key)
    if int(data.value) == 1:
        print('received <- ON\n')
    elif int(data.value) == 0:
        print('received <- OFF\n')

 # set the lamp to the feed value
    led.value = int(data.value)
    time.sleep(0.5)
