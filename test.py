from picozero import RGBLED,pico_led,LED
from time import sleep
import math
import random
rgb = RGBLED(red = 15, green = 2, blue = 17,active_high=False) 
distance = 1.0
angle = 0.0 
direction = 0.0
coord = [distance,angle, direction]
turn_left = 0
turn_right = 0
turn = [turn_left, turn_right] 
count = 0
def forward():
    x = coord[0]*math.cos(coord[1]) + math.cos(coord[2])
    y = coord[0]*math.sin(coord[1]) + math.sin(coord[2])
    coord[0] = math.sqrt(x**2 + y**2)
    coord[1] = math.atan2(y,x)
    rgb.color = (255, 0, 0) #red

    return coord,turn

def left():
    coord[2] += math.pi/2
    coord[2] = (coord[2] + math.pi) % (2 * math.pi) - math.pi  # Keep within [-π, π]

    x = coord[0]*math.cos(coord[1]) + math.cos(coord[2])
    y = coord[0]*math.sin(coord[1]) + math.sin(coord[2])
    coord[0] = math.sqrt(x**2 + y**2)
    coord[1] = math.atan2(y,x)
    turn[0] +=1
    rgb.color = (0, 255, 0) #green
    return coord,turn

def right():
    coord[2] -= math.pi/2
    coord[2] = (coord[2] + math.pi) % (2 * math.pi) - math.pi  # Keep within [-π, π]

    x = coord[0]*math.cos(coord[1]) + math.cos(coord[2])
    y = coord[0]*math.sin(coord[1]) + math.sin(coord[2])
    coord[0] = math.sqrt(x**2 + y**2)
    coord[1] = math.atan2(y,x)
    turn[1] += 1
    rgb.color = (0, 0, 255) #blue
    return coord,turn

def backward():
    x = coord[0]*math.cos(coord[1]) - math.cos(coord[2])
    y = coord[0]*math.sin(coord[1]) - math.sin(coord[2])
    coord[0] = math.sqrt(x**2 + y**2)
    coord[1] = math.atan2(y,x)
    rgb.color = (255, 128, 0) #orange

    return coord,turn

def go_hom():
    """Navigates the robot back to the nest area around (0,0)."""
    countx = 0
    county= 0
    while math.fabs(coord[0]*math.sin(coord[1])) > 1 and county < 50:  # Check distance to origin (coord[0] is distance)
        # If the robot is far from the origin in the Y direction, adjust heading
        if coord[1] > 0:  # Robot needs to move down (towards 0 angle)
            if  not ( -math.pi/2 - 0.2 <coord[2] < -math.pi/2 + 0.2):  # Check if robot is facing down
                right()  # Turn right to face downward
                sleep(0.5)
            else:
                forward()  # Move forward
                sleep(0.5)

        else:  # Robot needs to move up
            if not (math.pi/2 - 0.2 <coord[2] < math.pi/2 + 0.2):
                left()  # Turn left to face upward
                sleep(0.5)
            else:
                forward()  # Move forward
                sleep(0.5)
        county += 1
        print(coord,coord[0]*math.sin(coord[1]))
    print('at around x-axis')   
    while math.fabs(coord[0]*math.cos(coord[1])) > 1 and countx < 50:  # Check the angular position
        if (-math.pi/2 < coord[1] < math.pi/2):  # Need to go towards Negative X direction
            if (-math.pi/2 <= coord[2] <= math.pi/2):  # Check if robot is facing left
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
        countx += 1
        print(coord,coord[0]*math.sin(coord[1]))
    return coord

movement  = [forward,left,right]

def avoid_obstacle():
    '''Stop moving once the robot moves close to an opject'''
    backward()
    random.choice([left,right])()
    return coord

def get_position():
    '''Update the position of the robot from the reference camera '''
    
    return coord

def broadcast():
    '''Broadcasting location of the nest'''
    
    return coord

def find_station():
    count = 0
    while (math.fabs(coord[0]*math.cos(coord[1]) - station[0]*math.cos(station[1])) > 2 or math.fabs(coord[0]*math.sin(coord[1]) - station[0]*math.sin(station[1])) > 2)  and count < 100:
        random.choice(movement)()
        sleep(0.5)
        print(coord,turn)
        count +=1
        rgb.color= (0,0,0)
        sleep(0.5)
        if math.fabs(coord[0] - station[0]) < 1 and math.cos(coord[1]) * math.cos(station[1]) > 0 and math.sin(coord[1]) * math.sin(station[1]) > 0:
            print('Gettng there')
    return coord
    
'''Unconment only what you want it to do '''
station = [8,1] # artificially set station position

find_station()
go_hom()




        
