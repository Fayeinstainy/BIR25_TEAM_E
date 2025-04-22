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
SEND_BITS = [1,0,1,1,0,1,1,0]

def wall_detection():
    print("Wall detection started")
    IR_transmitter_pin.duty_u16(32768)
    start = time.ticks_ms()
    detected = False
    
    while time.ticks_diff(time.ticks_ms(),start) < WALL_DETECTION_WINDOW_MS:
        if IR_receiver_pin.value()==1:
            #print("IR Signal Detected!")
            detected = True
        #elif IR_receiver_pin.value()==0:
            #print("No Signal")
    
    IR_transmitter_pin.duty_u16(0)
    if detected == True:
        print("Wall detected")
        led_receiver_pin.value(1)

    else:
        print("Wall cleared!")
        led_receiver_pin.value(0)

    
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
        print("Sending bits:", bit)
        manchester_encoding_single_bit(bit)
    ir_off()
    print("Message sent.")
    
# -------- IR Receive -------- #
def listen_for_signal(duration_ms=50):
    print("Listening for IR message...")
    start = time.ticks_us()
    timestamps = []
    prev = IR_receiver_pin.value()

    while time.ticks_diff(time.ticks_us(), start) < duration_ms * 1000:
        curr = IR_receiver_pin.value()
        if curr != prev:
            timestamps.append(time.ticks_us())
            prev = curr

    return [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]

def decode_manchester(pulses):
    bits = []
    for t in pulses:
        if 600 <= t <= 1000:
            bits.append(1)
        elif 200 <= t <= 600:
            bits.append(0)
    return bits

#def receiving_bits(bits):
   
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
        time.sleep(0.1)
        #sending_bits(SEND_BITS)
        pulses = listen_for_signal()
        bits = decode_manchester(pulses)
        
except KeyboardInterrupt:
    IR_transmitter_pin.duty_u16(0)
    print("Transmitter OFF")
    print("Program stopped")




