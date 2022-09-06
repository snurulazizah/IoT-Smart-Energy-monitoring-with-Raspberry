import serial
from firebase import firebase
import time

firebase = firebase.FirebaseApplication('https://nurulapp-22175-default-rtdb.firebaseio.com/', None)

def update_firebase():
    arduino= serial.Serial('/dev/ttyACM0', 9600)
    arduino.flush()
    data=arduino.readline()
    time.sleep(2)
    data=arduino.readline()
    pieces = data.decode('utf-8').split("\t")
    Voltage=pieces[2]
    Current=pieces[1]
    Power = pieces[0]
    data={
    "Voltage": Voltage,
    "Current": Current,
    "Power":Power
    }
    firebase.post('/data',data)
while True:
    update_firebase()

        
  