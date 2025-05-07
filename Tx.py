from machine import Pin, PWM
import time

# ======= HARDWARE CONFIG ======= #
IR_TX = PWM(Pin(16))
IR_RX = Pin(15, Pin.IN)
LED = Pin(14, Pin.OUT)

# ======= PROTOCOL CONFIG ======= #
CARRIER_FREQ = 38000
DUTY_CYCLE = 20000  # Increased power
BIT_TIME = 800  # µs (400µs high + 400µs low)
SYNC_TIME = 3000  # µs of continuous carrier for sync
DEBUG = True

# ======= ROBOT STATE ======= #
is_sender = False  # Starts as Receiver (RX) inside nest
message_received = None  # Stores the last message

# ======= INITIALIZATION ======= #
IR_TX.freq(CARRIER_FREQ)
IR_TX.duty_u16(0)  # Start with IR off

def log(msg):
    if DEBUG:
        print(f"[{time.ticks_ms()}] {msg}")

# ======= TRANSMITTER ======= #
def send_bit(bit):
    if bit == 1:
        IR_TX.duty_u16(DUTY_CYCLE)
        time.sleep_us(400)
        IR_TX.duty_u16(0)
        time.sleep_us(400)
    else:
        IR_TX.duty_u16(0)
        time.sleep_us(400)
        IR_TX.duty_u16(DUTY_CYCLE)
        time.sleep_us(400)

def transmit(bits):
    log(f"TX: Sending {bits} with sync pulse")
    
    # Send sync pulse (3ms continuous carrier)
    IR_TX.duty_u16(DUTY_CYCLE)
    time.sleep_us(SYNC_TIME)
    IR_TX.duty_u16(0)
    time.sleep_us(500)  # Sync gap
    
    # Send data bits
    for i, bit in enumerate(bits):
        send_bit(bit)
        log(f"TX: Sent bit {i} = {bit} ({'high-low' if bit else 'low-high'})")
    
    IR_TX.duty_u16(0)
    log("TX: Transmission complete")

# ======= RECEIVER ======= #
def wait_for_signal(timeout_ms=150):
    log("RX: Waiting for sync pulse...")
    start = time.ticks_ms()
    
    # Wait for continuous low signal (receiver active-low)
    while time.ticks_diff(time.ticks_ms(), start) < timeout_ms:
        if IR_RX.value() == 0:  # Signal detected
            sync_start = time.ticks_us()
            while IR_RX.value() == 0:  # Measure sync duration
                pass
            sync_dur = time.ticks_diff(time.ticks_us(), sync_start)
            if sync_dur > SYNC_TIME * 0.7:  # 70% of expected sync
                log(f"RX: Detected sync pulse ({sync_dur}µs)")
                return True
    return False

def capture_bits():
    bits = []
    last_state = IR_RX.value()

    for _ in range(8):  # 8 bits
        # Wait for first edge
        while IR_RX.value() == last_state:
            pass
        first_edge_time = time.ticks_us()
        first_level = last_state
        last_state = IR_RX.value()

        # Wait for second edge (Manchester)
        while IR_RX.value() == last_state:
            pass
        second_edge_time = time.ticks_us()
        second_level = last_state
        last_state = IR_RX.value()

        duration = time.ticks_diff(second_edge_time, first_edge_time)

        # Decode based on transition direction
        if duration < BIT_TIME * 1.5:  # Some margin
            if first_level == 0 and second_level == 1:
                bits.append(0)
            elif first_level == 1 and second_level == 0:
                bits.append(1)
            else:
                log(f"RX: Invalid transition {first_level}->{second_level}")
        else:
            log(f"RX: Pulse too long ({duration}µs), skipping")
    
    return bits


# ======= MAIN LOOP ======= #
def main():
    test_message = [0,1,0,1,0,0,1,0]
    global is_sender, received
    
    while True:
        is_sender = True # Tx Testing 
        if not is_sender:
            # ===== RECEIVER MODE (Inside Nest) ===== #
            print("Waiting for message (RX Mode)...")
            if wait_for_signal():
                LED.on()
                received = capture_bits()
                LED.off()
                
                if len(received) >= len(test_message):
                    received = received[:len(test_message)]
                    log(f"RX: Decoded message: {received}: bits: {received}")
                    
                    if received == test_message:
                        log("SUCCESS: Message matched!: bits: {received}")
                    else:
                        log("ERROR: Message mismatch")
                else:
                    log(f"ERROR: Only received {len(received)}/{len(test_message)} bits: {received}")
        
                time.sleep(1)
                        
                # === ROBOT MOVES OUT (Now becomes Sender) === #
                is_sender = False # change to True when integrating the codes  
                #go_out_and_perform_task()  # Custom navigation logic
                
        else:
        # ===== SENDER MODE (Returned to Nest) ===== #
            print("Transmitting message (TX Mode)...")
            transmit(test_message)
            
            # === ROBOT RESETS TO RECEIVER === #
            is_sender = False  
            time.sleep(2)  # Cooldown before listening again
try:
    main()
except KeyboardInterrupt:
    IR_TX.duty_u16(0)
    print("Program stopped")

