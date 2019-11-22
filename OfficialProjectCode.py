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
# Command for linux console for pigpio daemon
#sudo pigpiod -p 8887

buzPin=18 # Piezoelectric buzzer
TRIG = 20 # Trigger pin on HC-SR04
ECHO = 21 # Echo pin on HC-SR04. This is connected to a voltage divider to reduce 5 volt output to 3.3 v

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

class Button:
    def __init__(self):
        self.pinArray = np.array([2,4,3,1]) # The true passcode
        self.userArray = np.array([]) # The inputted passcode
        self.count = 1 # Represents how many numbers are added to the user array
    def button_press(self):
        if GPIO.input(buttonRed) == True:
            time.sleep(0.5)
            self.userArray = np.append(self.userArray,1)
            self.count+=1
        if GPIO.input(buttonYellow) == True:
            time.sleep(0.5)
            self.userArray = np.append(self.userArray,2)
            self.count+=1
        if GPIO.input(buttonGreen) == True:
            time.sleep(0.5)
            self.userArray = np.append(self.userArray,3)
            self.count+=1
        if GPIO.input(buttonBlue) == True:
            time.sleep(0.5)
            self.userArray = np.append(self.userArray,4)
            self.count+=1    
    def full_length(self): # Checks if the user array is as long as the real passcode
        return self.count > len(self.pinArray)
    def check_pass(self): # Checks if the inputted passcode is correct
        self.index=0
        self.match=True # If the passcodes match
        for i in self.userArray:
            if i != self.pinArray[self.index]:
                self.match = False
                break
            if i == self.pinArray[self.index]:
                self.index += 1
        return self.match

def siren1(pos): # A lower pitched siren for debugging
    return 440*math.sin(pos)+440

def siren2(pos): # A siren
    return 300*math.sin(pos)+740

def pulseIn(): # Returns the length of a pulse from the ultrasonic sensor
    while True:
        GPIO.output(TRIG, False)
        time.sleep(.000005)
        GPIO.output(TRIG, True) # Sending out a trigger pulse for 10 microseconds
        time.sleep(.00001)
        GPIO.output(TRIG, False)
        pulse_start = time.time()
        pulse_end = time.time()
        now = time.time()
        while GPIO.input(ECHO)==0 and time.time()-now<.1: # If we start sending out a pulse or if the command times out
            pulse_start = time.time()
        now = time.time()
        while GPIO.input(ECHO)==1 and time.time()-now<.1: # If we receive the pulse or if the command times out
            pulse_end = time.time()
        return pulse_end-pulse_start


try:
    time.sleep(2) # Waiting for the ultrasonic sensor to warm up
    while True:
        button_obj=Button()
        SecurityLog = open("IntrusionLog.txt", "a") # A text file that saves a log of when the sensor is triggered
        sirenPos=0
        x = 50 #50 cm threshold distance
        flag = False
        distance = pulseIn() * 17150 # 17150 is half the speed of sound in cm/s to account for the return trip
        if (distance <= x): # Someone triggered the sensor
            flag = True
            dateTime = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            fileString = str(datetime.today().strftime('%Y-%m-%d-%H:%M:%S')) + '.jpg'
            camera.capture(fileString) # Takes the photo and stores it
            dataWrite = str(dateTime)   + "  " + fileString + "  " + "\n"
            SecurityLog.write(dataWrite)
        if (flag == True):
            while True:
                pi.hardware_PWM(buzPin,int(siren2(sirenPos)), int(.5e6))
                sirenPos+=.01
                button_obj.button_press()
                time.sleep(.01)
                if (button_obj.full_length()):
                    if(button_obj.check_pass()): # Passcode is correct
                        pi.hardware_PWM(buzPin, 0, 0)
                        SecurityLog.write("False Alarm! \n")
                        time.sleep(5) # So you cannot set it off right after the code is inputted
                        break
                    else: # Passcode is not correct
                        button_obj=Button() # resets button so you can try again
                        continue
                        
        SecurityLog.close()
except(KeyboardInterrupt, SystemExit):
    print("System Disabled")
    
finally:
    pi.hardware_PWM(buzPin, 0, 0)
    SecurityLog.close()
    GPIO.cleanup()
