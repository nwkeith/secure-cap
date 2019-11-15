# secure-cap
A security system with a Raspberry Pi at its core
***
#Code that I found from: https://stackoverflow.com/questions/32490629/getting-todays-date-in-yyyy-mm-dd-in-python , that will return the current date and time in Python
  from datetime import datetime
  datetime.today().strftime('%Y-%m-%d') <-just for displaying year, month, and day
  datetime.today().strftime('%Y-%m-%d-%H:%M:%S') <-will return the year, month, day, hour, minute, and seconds values (we will want           to use this one)
  ***
  more documentation on setting up the HC-SRO4 sensor on the raspberry pi: http://www.piddlerintheroot.com/hc-sr04/
  ***
  others are also facing difficulty with the while loop that we keep getting stuck in: https://stackoverflow.com/questions/36474735/raspberry-pi-python-loop-stop-to-work
 ***
 https://raspberrypi.stackexchange.com/questions/41159/ultrasonic-sensor-stops-after-giving-some-reading-when-running-in-thread-on-torn

Code for Button Pin
import time
import RPi.GPIO as GPIO
import numpy as np
GPIO.setmode(GPIO.BCM)
buttonRed = 24
buttonYellow = 25
buttonGreen = 26
buttonBlue = 27

pinArray = np.array([2,4,3,1])
userArray = np.array([])
x = 1

while x <= len(pinArray):
    while True:
        if GPIO.input(buttonRed) == True:
            time.sleep(0.5)
            userArray = np.append(userArray,1)
            x+=1
            break
        if GPIO.input(buttonYellow) == True:
            time.sleep(0.5)
            userArray = np.append(userArray,2)
            x+=1
            break
        if GPIO.input(buttonGreen) == True:
            time.sleep(0.5)
            userArray = np.append(userArray,3)
            x+=1
            break
        if GPIO.input(buttonBlue) == True:
            time.sleep(0.5)
            userArray = np.append(userArray,4)
            x+=1
            break
        continue

index = 0
for i in userArray:
    if i =! pinArray[index]:
        print("Incorrect Pin")
        break
    if i = pinArray[index]:
        index += 1
        continue
