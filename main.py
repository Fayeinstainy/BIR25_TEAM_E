from picozero import RGBLED
from time import sleep
import math
import random
import rp2
import sys
import time
#from machine import WDT, reset
from machine import reset, WDT, Pin, PWM, reset_cause, PWRON_RESET
import urequests as requests
import json
###

# Declare links to raw files containing version data and code.
RAW_VERSION_URL = "https://raw.githubusercontent.com/Huw311/pico_ota/refs/heads/main/version.json"
RAW_MAIN_URL    = "https://raw.githubusercontent.com/Fayeinstainy/BIR25_TEAM_E/refs/heads/main/main.py"
# Intterval at which version checks occur
CHECK_INTERVAL = 10  # seconds

##    NECESSARY FUNCTIONS
# Find local version
def get_local_version():
    print("Fetching local version...")
    try:
        with open("local_version.json") as f:
            local_data = json.load(f)
            version = local_data.get("version", "0.0.0")
            print(f"Local version: {version}")
            return version
    except Exception as e:
        print(f"Error reading local_version.json: {e}")
        return "0.0.0"

# Fetch remote version
def get_remote_version():
    print(f"Fetching remote version from: {RAW_VERSION_URL}")
    try:
        res = requests.get(RAW_VERSION_URL)
        print(f"Response Status Code: {res.status_code}")
        if res.status_code == 200:
            data = res.json()  # Parse JSON response
            version = data.get("version", "0.0.0")
            print(f"Remote version: {version}")
            return version
        else:
            print(f"Error: Received non-200 status code {res.status_code}")
    except Exception as e:
        print(f"Error getting remote version: {e}")
    return "0.0.0"

# Updates pico firmware
def update_code():
    print("Attempting to update main.py...")
    try:
        res = requests.get(RAW_MAIN_URL)
        print(f"Response Status Code for main.py: {res.status_code}")
        if res.status_code == 200:
            with open("main.py", "w") as f:
                f.write(res.text)
            print("main.py saved.")
        else:
            print(f"Error: Received non-200 status code {res.status_code} while fetching main.py")

        # Fetch and save the new version info
        res = requests.get(RAW_VERSION_URL)
        print(f"Response Status Code for version.json: {res.status_code}")
        if res.status_code == 200:
            with open("local_version.json", "w") as f:
                f.write(res.text)
            print("Version updated.")
        else:
            print(f"Error: Received non-200 status code {res.status_code} while fetching version.json")

        print("Update successful, rebooting...")
        time.sleep(1)
        machine.reset()
    except Exception as e:
        print(f"Update failed: {e}")
##

## USED FOR TESTING
# setup blink led
led = machine.Pin("LED", machine.Pin.OUT
led.on()


##



def reprogram()

    # Blink LED and check versions periodically

    local = get_local_version()     # local version variable
    remote = get_remote_version()    # Remote version variable
   
    if local != remote:    # if versions do not match, then update code
        print("Version mismatch detected, updating code...")
        update_code()
    else:
        print("Versions are the same, no update required.")
###
# if machine.reset_cause() != machine.PWRON_RESET:  # 如果不是上电复位
#     print("wrong detecting, resetting...")
#     time.sleep(1)       # 等待串口输出完成
#     machine.reset()     # 强制硬件复位

wdt = WDT(timeout=8000) #8 seconds watchdog

# --------- Setup --------- #
IR_transmitter_pin = PWM(Pin(0))
IR_transmitter_pin.freq(38000)  # 38kHz carrier
IR_transmitter_pin2 = PWM(Pin(4))
IR_transmitter_pin2.freq(38000)  # 38kHz carrier
IR_transmitter_pin3 = PWM(Pin(8))
IR_transmitter_pin3.freq(38000)  # 38kHz carrier

IR_receiver_pin1 = Pin(5, Pin.IN)
IR_receiver_pin2 = Pin(9, Pin.IN)
#1 and 9 are not working on Beth.(No Rx 1)
#1 not working on Bella (No Rx 1)
#1 not working on Cursed (No Rx 1)

rgb = RGBLED(red = 16, green = 17, blue = 18,active_high=False)

IR_transmitter_pin.duty_u16(38000)  # Enable IR signal
IR_transmitter_pin2.duty_u16(38000)  # Enable IR signal
IR_transmitter_pin3.duty_u16(38000)  # Enable IR signal

tran1 = Pin(19, Pin.OUT)
tran2 = Pin(20, Pin.OUT)
tran3 = Pin(21, Pin.OUT)

tran1.value(0)
tran2.value(0)
tran3.value(0)
#detected = False
#--------------------walldetection----------#
def wall_detection_notworking():
    print("Wall detection started")
    #IR_transmitter_pin.duty_u16(32768)
    start = time.ticks_ms()
   
   
    while time.ticks_diff(time.ticks_ms(),start) < WALL_DETECTION_WINDOW_MS:
        if IR_receiver_pin.value()==0:
            #print("IR Signal Detected!")
            detected = True
        #elif IR_receiver_pin.value()==0:
            #print("No Signal")
   
    #IR_transmitter_pin.duty_u16(0)
    if detected == True:
        print("Wall detected")
        rgb.color = (255,0,0) #red
        sleep(1)
        #led_receiver_pin.value(1)

    else:
        print("Wall cleared!")
        rgb.color =(100,0,100) #red+green
        sleep(1)
        #led_receiver_pin.value(0)
       
# --------- Wall Detection --------- #
def wall_detection():
     
    #print("Wall detection started")
    #global detected

    time.sleep_ms(1)  # Allow some time for signal to bounce back

    if IR_receiver_pin1.value()==0 or IR_receiver_pin2.value() == 0:
        #detected = True
        print("IR Signal Detected!")
        rgb.color = (255, 0, 0) #red
        return True
    else:
        print("No Signal.")
        rgb.color = (0, 0, 255) #
        return False

#---------------------motor/navigation--------------------
#rgb = RGBLED(red = 16, green = 17, blue = 18,active_high=False)
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

def leftback(duty):
    coord[2] += math.pi/2
    coord[2] = (coord[2] + math.pi) % (2 * math.pi) - math.pi  # Keep within [-π, π]

    x = coord[0]*math.cos(coord[1]) + math.cos(coord[2])
    y = coord[0]*math.sin(coord[1]) + math.sin(coord[2])
    coord[0] = math.sqrt(x**2 + y**2)
    coord[1] = math.atan2(y,x)
    turn[0] +=1
    rgb.color = (0, 255, 0) #blue
    RotateCCW(duty, pwma)
    RotateCW(duty/1.2, pwmb)
    return coord,turn

def rightback(duty):
    coord[2] -= math.pi/2
    coord[2] = (coord[2] + math.pi) % (2 * math.pi) - math.pi  # Keep within [-π, π]

    x = coord[0]*math.cos(coord[1]) + math.cos(coord[2])
    y = coord[0]*math.sin(coord[1]) + math.sin(coord[2])
    coord[0] = math.sqrt(x**2 + y**2)
    coord[1] = math.atan2(y,x)
    turn[1] += 1
    rgb.color = (0, 0, 255) #green
    RotateCW(duty/1.2, pwma)
    RotateCCW(duty, pwmb)
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

def main():
    start_time = time.time()
    duration = 40  # seconds
    try:
       
        while True:
            wdt.feed()
            '''Unconment only what you want it to do '''
            station = [8,1] # artificially set station position
            #movement  = [forward,left,right]
            nest = [0,0] #coordinate of the nest
       
       
       
            if time.time() - start_time > duration:
                print("40 seconds passed, exiting loop.")
                StopMotor()
                break
   
            detected = wall_detection()
            #print("before detected = ",detected)
            time.sleep(0.2)  # Adjust scan interval as needed
    #         forward(72000)
    #         time.sleep(2)
    #         StopMotor()
    #         time.sleep(2)
            if detected == False:
                #backward(24000)  # Move forward
                #time.sleep(2)
                print("detected = ",detected)
               
                #StopMotor()
    #             time.sleep(1)
               
            elif detected == True :#True mean sugbal detected
               
#                 StopMotor()
#                 sleep(1)
#                 leftback(72000)
                print("detected = ",detected)
                time.sleep(.1)
        #forward(72000)  # Move forward
        #time.sleep(2)
        #StopMotor()
        #get_charge([station[0]*math.cos(station[1]),station[0]*math.sin(station[1])])
        #get_charge(nest) #go home


        #rgb.color = (0, 0,100) #red
        # sleep(2)

        # rgb.color = (0, 255, 0) #blue
        #sleep(2)
        #rgb.color = (255,0,0) #green

        #forward(72000)  # Move forward
        #sleep(2)
#         StopMotor()
#         sleep(3)

       
    except KeyboardInterrupt:
        print("KeyboardInterrupt caught. Stopping motor.")
        StopMotor()
       
    finally:
            # 关键清理步骤
            IR_transmitter_pin.duty_u16(0)  # 关闭红外发射
            IR_transmitter_pin2.duty_u16(0)
            IR_transmitter_pin3.duty_u16(0)
            StopMotor()                     # 停止电机
            rgb.color=(0,255,0)                      
            print("turning off...")
            time.sleep(1)
            rgb.off()                      
            time.sleep(2)
            reprogram()
            sys.exit()

       
#if __name__ == "__main__":
 #    main()
