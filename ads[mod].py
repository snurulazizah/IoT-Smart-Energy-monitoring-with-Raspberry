#!/usr/bin/env python3
import time
import Adafruit_ADS1x15
from Adafruit_IO import *
import math
from firebase import firebase
import time
import pyrebase
import pandas as pd
import csv

# firebase = firebase.FirebaseApplication('https://nurulapp-22175-default-rtdb.firebaseio.com/', None)
# Create an ADS1115 ADC (16-bit) instance..
adc1 = Adafruit_ADS1x15.ADS1115()
GAIN = 1         # see ads1015/1115 documentation for potential values.
samples = 5      # number of samples taken from ads1115
places = int(2)    # set rounding

arus=[]
tegangan=[]
daya=[]
a=1
# create a while loop to monitor the current and voltage and send to Adafruit io.
# def update_firebase()
          
while True:
    # reset variables
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
    for count in range(5):        
        datai.insert(count, (abs(adc1.read_adc(0, gain=GAIN))))
        datav.insert(count, (abs(adc1.read_adc(1, gain=GAIN))))
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
    IrmsA0 = float(maxIValue / float(2047) * 30)
    IrmsA0 = round(IrmsA0, places)
    ampsA0 = IrmsA0 / math.sqrt(2)  # RMS formula to get current reading to match what an ammeter shows.
    ampsA0 = round(ampsA0, places)
    # Calculate voltage
    VrmsA1 = float(maxVValue * 82/ float(2047))
    VrmsA1 = round(VrmsA1, places)
    voltsA1 = VrmsA1 / math.sqrt(2)  # RMS formula to get voltage reading to match what an voltmeter shows.
    voltsA1 = round(voltsA1, places)
    print('Voltage: {0}'.format(voltsA1))
    print('Current: {0}'.format(ampsA0))
    #calculate power
    power = round(ampsA0 * voltsA1,places)
    print('Power: {0}'.format(power))
    time.sleep(5)

    arus.append(ampsA0)
    tegangan.append(voltsA1)
    daya.append(power)

    header=['Voltage','Current','Power']
    data= [voltsA1,ampsA0,power]

    if len(arus) == 240:
        cv_df = pd.DataFrame.from_dict({'Voltage': tegangan, 'Current': arus, 'Power': daya}, orient='index').T
        cv_csv_file = f'/home/raspi/datamagic_{a}.csv'
        with open(cv_csv_file, mode='w') as f:
            cv_df.to_csv(f)
        arus.clear()
        tegangan.clear()
        daya.clear()
        a+=1
            
              


    #post data to adafruit.io
    # Wait before repeating loop
    
    # dataiot={
    # "Voltage": voltsA1,
    # "Current": ampsA0,
    # "Power":power
    # }
    # firebase.post('/dataiot',dataiot)
# while True:
    # update_firebase()