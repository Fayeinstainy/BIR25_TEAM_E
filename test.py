from picozero import RGBLED
from time import sleep
import math
import random
from machine import Pin , PWM
import machine
import rp2
import sys
rgb = RGBLED(red = 16, green = 17, blue = 18,active_high=False) 
distance = 1.0 #polar distancce of the current location
angle = 0.0 #polar angle of the current location
direction = 0.0 #where the robot is facing
coord = [distance,angle, direction] 
turn_left = 0
turn_right = 0
turn = [turn_left, turn_right] 
count = 0
led = Pin('LED', Pin.OUT)

ain1 = Pin(12,Pin.OUT)
ain2 = Pin(11, Pin.OUT)
bin1 = Pin(13,Pin.OUT)
bin2 = Pin(14,Pin.OUT)
pwma = PWM(Pin(10))
pwmb = PWM(Pin(15))
pwma.freq(24000)
pwmb.freq(24000)

def RotateCW(duty, pwm):
    ain1.value(1)
    ain2.value(0)
    bin1.value(1)
    bin2.value(0)
    duty_16 = int(duty)
    pwm.duty_u16(duty_16)

def RotateCCW(duty, pwm):
    ain1.value(0)
    ain2.value(1)
    bin1.value(0)
    bin2.value(1)
    duty_16 = int(duty)
    pwm.duty_u16(duty_16)
    led.toggle()
    
def StopMotor():
    ain1.value(0)
    ain2.value(0)
    bin1.value(0)
    bin2.value(0)
    pwma.duty_u16(0)
    pwmb.duty_u16(0)
    led.toggle()
    
def forward(duty):
    x = coord[0]*math.cos(coord[1]) + math.cos(coord[2])
    y = coord[0]*math.sin(coord[1]) + math.sin(coord[2])
    coord[0] = math.sqrt(x**2 + y**2)
    coord[1] = math.atan2(y,x)
    RotateCW(duty, pwma)
    RotateCW(duty, pwmb)
    rgb.color = (255, 0, 0) #red

    return coord,turn

def left(duty):
    coord[2] += math.pi/2
    coord[2] = (coord[2] + math.pi) % (2 * math.pi) - math.pi  # Keep within [-π, π]

    x = coord[0]*math.cos(coord[1]) + math.cos(coord[2])
    y = coord[0]*math.sin(coord[1]) + math.sin(coord[2])
    coord[0] = math.sqrt(x**2 + y**2)
    coord[1] = math.atan2(y,x)
    turn[0] +=1
    rgb.color = (0, 255, 0) #green
    RotateCW(duty, pwma)
    RotateCCW(duty, pwmb)
    return coord,turn

def right(duty):
    coord[2] -= math.pi/2
    coord[2] = (coord[2] + math.pi) % (2 * math.pi) - math.pi  # Keep within [-π, π]

    x = coord[0]*math.cos(coord[1]) + math.cos(coord[2])
    y = coord[0]*math.sin(coord[1]) + math.sin(coord[2])
    coord[0] = math.sqrt(x**2 + y**2)
    coord[1] = math.atan2(y,x)
    turn[1] += 1
    rgb.color = (0, 0, 255) #blue
    RotateCCW(duty, pwma)
    RotateCW(duty, pwmb)
    return coord,turn

def backward(duty):
    x = coord[0]*math.cos(coord[1]) - math.cos(coord[2])
    y = coord[0]*math.sin(coord[1]) - math.sin(coord[2])
    coord[0] = math.sqrt(x**2 + y**2)
    coord[1] = math.atan2(y,x)
    rgb.color = (255, 128, 0) #orange
    RotateCCW(duty, pwma)
    RotateCCW(duty, pwmb)

    return coord,turn

def foraging():
    '''Randomly move to find a charger'''
    count = 0
    while (math.fabs(coord[0]*math.cos(coord[1]) - station[0]*math.cos(station[1])) > 2 or math.fabs(coord[0]*math.sin(coord[1]) - station[0]*math.sin(station[1])) > 2)  and count < 30:
        random.choice(movement)(48000)
        sleep(3)
        print(coord,turn)
        count +=1
        rgb.color= (0,0,0)
        sleep(1)
        #if math.fabs(coord[0] - station[0]) < 1 and math.cos(coord[1]) * math.cos(station[1]) > 0 and math.sin(coord[1]) * math.sin(station[1]) > 0:
           # print('Gettng there')   these are for debugging purpose 
    return coord
#stop and talk to each other
def get_charge(destination):
    """Navigates the robot to the charger"""
    count = 0
    while math.fabs(coord[0]*math.sin(coord[1]) - destination[1]) > 0.9 and count < 100 :
        if  coord[0]*math.sin(coord[1]) <= destination[1] : # Robot needs to move up
            if not (math.pi/2 -0.2 < coord[2] < math.pi/2 +0.2):
                left()
                sleep(0.5)
            else:
                forward()
                sleep(0.5)
        else: #robot needs to move down
            if not ( -math.pi/2 - 0.2 <coord[2] < -math.pi/2 + 0.2):  # Check if robot is facing down
                right()  # Turn right to face downward
                sleep(0.5)
            else:
                forward()  # Move forward
                sleep(0.5)
        print(coord[0]*math.sin(coord[1]))
        count +=1
    while math.fabs(coord[0]*math.cos(coord[1]) - destination[0]) > 0.9 and count < 100 :
        if  coord[0]*math.cos(coord[1]) > destination[0]: # Move to the left
            if (-math.pi/2-0.000001 <= coord[2] <= math.pi/2):  # Check if robot is facing left
                left()  # Turn left to face right
                sleep(0.5)
            else:
                forward()  # Move forward
                sleep(0.5)
        else:  # Need to go towards positive X direction
            if not (-0.2 <coord[2] < 0.2) :  # Check if robot is facing right
                right()  # Turn right to face left
                sleep(0.5)
            else:
                forward()  # Move forward
                sleep(0.5)
        print(coord[0]*math.cos(coord[1]))
        count +=1
    print(coord)
    return coord
    
'''Unconment only what you want it to do '''
station = [8,1] # artificially set station position
movement  = [forward,left,right]
nest = [0,0] #coordinate of the nest


#foraging()
#get_charge([station[0]*math.cos(station[1]),station[0]*math.sin(station[1])])
#get_charge(nest) #go home


        
#rgb.color = (0, 0,255 ) #red
# sleep(2)
# rgb.color = (0, 255, 0) #green
# sleep(2)
# rgb.color = (0,0,255) #blue

left(24000)  # Move forward
sleep(5)
StopMotor()

