#initialization code (to be ran once)
from datetime import datetime
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (1920, 1080)

import time
import RPi.GPIO as GPIO
import numpy as np
GPIO.setmode(GPIO.BCM)

buttonRed = 24
buttonYellow = 25
buttonGreen = 26
buttonBlue = 27

GPIO.setup(buttonRed, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(buttonYellow, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(buttonGreen, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(buttonBlue, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

import pigpio
import math
pi = pigpio.pi(port = 8887)
#sudo pigpiod -p 8887

buzPin=18
TRIG = 20
ECHO = 21

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


def button():
    pinArray = np.array([2,4,3,1])
    userArray = np.array([])
    x = 1
    boolean = True
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
        if i != pinArray[index]:
            boolean = False
            break
        if i == pinArray[index]:
            index += 1
            continue
    return boolean


#def siren(pos):
    #return 440*math.sin(pos)+440

def pulseIn():
    while True:
        GPIO.output(TRIG, False)
        time.sleep(.000005)
        GPIO.output(TRIG, True) # Sending out a trigger pulse for 10 microseconds
        time.sleep(.00001)
        GPIO.output(TRIG, False)
        pulse_start = time.time()
        pulse_end = time.time()
        now = time.time()
        while GPIO.input(ECHO)==0 and time.time()-now<.1: 
            pulse_start = time.time()
            
        now = time.time()  
        while GPIO.input(ECHO)==1 and time.time()-now<.1:
            pulse_end = time.time()
        return pulse_end-pulse_start


try:
    while True:
        SecurityLog = open("IntrusionLog.txt", "a")
        x = 50 #50 cm threshold distance
        y = False
        flag = False
        distance = pulseIn() * 17150
        if (distance <= x):
            flag = True
            dateTime = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            fileString = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S')) + '.jpg'
            camera.capture(fileString)
            dataWrite = str(dateTime)   #+ "  " + fileString + "  " + "\n"
            SecurityLog.write(dataWrite)
        if (flag == True):
            pi.hardware_PWM(buzPin, int(900), int(0.5e6))
            while (y == False):
                if (button() == True):
                    pi.hardware_PWM(buzPin, 0, 0)
                    SecurityLog.write("False Alarm! \n")
                    y = True
                else:
                    pi.hardware_PWM(buzPin, int(1000), int(0.5e6))
        SecurityLog.close()
except(KeyboardInterrupt, SystemExit):
    print("System Disabled")
    
finally:
    pi.hardware_PWM(buzPin, 0, 0)
    SecurityLog.close()
    GPIO.cleanup()
    
                
