from machine import Pin, PWM
import time
#-----------setup--------------#
IR_transmitter_pin = PWM(16)
#IR_transmitter_pin.duty_u16(32768)
IR_transmitter_pin.freq(38000)

IR_receiver_pin = Pin(15,Pin.IN)
led_receiver_pin = Pin(14,Pin.OUT, Pin.PULL_DOWN)

#-----------config------------#
CYCLE_TIME_MS = 200
WALL_DETECTION_WINDOW_MS = 20
SEND_BITS = [0,1,0,1,0,0,1,0]

def wall_detection():
    print("Wall detection started")
    IR_transmitter_pin.duty_u16(32768)
    start = time.ticks_ms()
    detected = False
    
    while time.ticks_diff(time.ticks_ms(),start) < WALL_DETECTION_WINDOW_MS:
        if IR_receiver_pin.value()==1:
            print("IR Signal Detected!")
            detected = True
        elif IR_receiver_pin.value()==0:
            print("No Signal")
    
    IR_transmitter_pin.duty_u16(0)
    if detected == True:
        print("Wall detected")
    else:
        print("Wall cleared!")
    
def ir_on():
    IR_transmitter_pin.duty_u16(32768)
def ir_off():
    IR_transmitter_pin.duty_u16(0)
def manchester_encoding_single_bit(bit):
    if bit == 1:
        ir_on()
        time.sleep_us(400)
        ir_off()
        time.sleep_us(400)
        led_receiver_pin.value(1)
    elif bit == 0:
        ir_off()
        time.sleep_us(400)
        ir_on()
        time.sleep_us(400)
        led_receiver_pin.value(0)
def sending_bits(bits):
    for bit in bits:
        print("Sending bits:", bits)
        manchester_encoding_single_bit(bit)
    ir_off()
    print("Message sent.")
    
# def if_ir_detected():
#     if IR_receiver_pin.value()==1:
#         print("IR Signal Detected!")
#         led_receiver_pin.value(1)
# 
#     elif IR_receiver_pin.value()==0:
#         print("No Signal")
#         led_receiver_pin.value(0)

try:
    while True:
        #if_ir_detected()
        wall_detection()
        time.sleep(0.2)
        sending_bits(SEND_BITS)
        
except KeyboardInterrupt:
    IR_transmitter_pin.duty_u16(0)
    print("Transmitter OFF")
    print("Program stopped")

