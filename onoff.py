import RPi.GPIO as GPIO
import sys
from Adafruit_IO import MQTTClient

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ledPin = [23]
GPIO.setup(ledPin, GPIO.OUT)

ADAFRUIT_IO_KEY = 'aio_ZUBN70Ocjthx557dpnfOzWuJw6d1'
ADAFRUIT_IO_USERNAME = 'nurul_azizah'
FEED_ID = 'saklar'
feed_id='saklar'

def connected(client):
    # Subscribe to changes on a feed named Counter.
    print('Subscribing to Feed {0}'.format(FEED_ID))
    client.subscribe(FEED_ID)
    print('Waiting for feed data...')
def disconnected(client):
    sys.exit(1)
def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if (payload == 'ON'):
        GPIO.output(ledPin,1)
    else:
        GPIO.output(ledPin,0)
       
# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
# Setup the callback functions defined above.
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
# Connect to the Adafruit IO server.
client.connect()
client.loop_blocking()