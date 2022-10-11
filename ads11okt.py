#!/usr/bin/env python3
import Adafruit_ADS1x15
from Adafruit_IO import *
import math
import time
import RPi.GPIO as GPIO
from datetime import datetime
from firebase import firebase
import pyrebase
import pandas as pd
import csv


# Create an ADS1115 ADC (16-bit) instance..
adc1 = Adafruit_ADS1x15.ADS1115()
username = 'nurul_azizah'
AIO_KEY = 'aio_IsAq50rsjA85x3OxyLbHulFDEVwC' 
aio = Client(username, AIO_KEY)
GAIN = 1         # see ads1015/1115 documentation for potential values.
samples = 200     # number of samples taken from ads1115
places = int(2)    # set rounding
arus=[]
tegangan=[]
daya=[]
waktu=[]
waktustamp=[]
a=1
# create a while loop to monitor the current and voltage and send to Adafruit io.
# def update_firebase()
relay= [23] #16

GPIO.setmode(GPIO.BCM)       
GPIO.setup(relay, GPIO.OUT)
    
try:
    # firebase = firebase.FirebaseApplication('https://nurulapp-22175-default-rtdb.firebaseio.com/', None)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay, GPIO.OUT)
    while True:
        GPIO.output(relay, GPIO.HIGH) 
        count = int(0)
        datai = []
        datav = []
        maxIValue = 0
        maxVValue = 0
        IrmsA0 = 0
        VrmsA1 = 0
        ampsA0 = 0
        voltsA1 =0
        kilowatts = float(0)
            
            
            # since we are measuring an AC circuit the output of SCT-013 wand the voltage sensor will be a sinewave.
            # in order to calculate amps from sinewave we will need to get the peak voltage
            # from each input and use root mean square formula (RMS)
            # this loop will take 200 samples from each input and give you the highest (peak)
        for count in range(200):        
            datai.insert(count, (abs(adc1.read_adc(0, gain=1))))
            datav.insert(count, (abs(adc1.read_adc(1, gain=1))))
                # see if you have a new maxValue
                #print (datai[count])
            if datai[count] > maxIValue:
                maxIValue = datai[count]           
            if datav[count] > maxVValue:
                maxVValue = datav[count]
                    #print("new maxv value:")
                    #print(maxVValue)               
            #calculate current using the sampled data
            # I used a sct-013 that is calibrated for 1000mV output @ 30A. Usually has 30A/1V printed on it.
            #print("proceeding")
        IrmsA0 = float(maxIValue / float(4095) * 37)
        IrmsA0 = round(IrmsA0, places)
        ampsA0 = IrmsA0 / math.sqrt(2)  # RMS formula to get current reading to match what an ammeter shows.
        ampsA0 = round(ampsA0, places)
            # Calculate voltage
        VrmsA1 = float(maxVValue * 1180/ float(65535))
        VrmsA1 = round(VrmsA1, places)
        voltsA1 = VrmsA1 / math.sqrt(2)  # RMS formula to get voltage reading to match what an voltmeter shows.
        voltsA1 = round(voltsA1, places)
        power = round(ampsA0 * voltsA1,places)
        dt=datetime.now()
        ts= datetime.timestamp(dt)

        print('Voltage: {0}'.format(voltsA1))
        print('Current: {0}'.format(ampsA0))
        print('Power: {0}'.format(power))#
        print  ("time :{0}".format(dt))#
        print ("Timestamp:{0}".format(ts))
        Voltage = aio.feeds('voltage')
        aio.send_data(Voltage.key, voltsA1)
        Current= aio.feeds('current')
        aio.send_data(Current.key, ampsA0)
        EnergyUsage = aio.feeds('energyusage')
        aio.send_data(EnergyUsage.key, power)
        
        arus.append(ampsA0)
        tegangan.append(voltsA1)
        daya.append(power)
        waktu.append(dt)
        waktustamp.append(ts)

        header=['Voltage','Current','Power','Time','Timestamp']
        data= [voltsA1,ampsA0,power,dt,ts]

        if len(arus) == 20:
            cv_df = pd.DataFrame.from_dict({'Voltage': tegangan, 'Current': arus, 'Power': daya,'Time':waktu,'Timestamp':waktustamp}, orient='index').T
            cv_csv_file = f'/home/raspi/data11okt_{a}.csv'
            with open(cv_csv_file, mode='w') as f:
                cv_df.to_csv(f)
            arus.clear()
            tegangan.clear()
            daya.clear()
            a+=1
        if voltsA1 > float(235):
            print('terjadi masalah')
            GPIO.output(relay,GPIO.LOW)
            GPIO.cleanup()
                                                        
        
except KeyboardInterrupt: 
    GPIO.cleanup()
    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            