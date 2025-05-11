from machine import ADC, Pin
import time


# ADC channels (GPIO26 = ADC0, GPIO27 = ADC1)
supercap_1 = ADC(0)  # Supercapacitor 1
supercap_2 = ADC(1)  # Supercapacitor 2

# Voltage divider scale based on resistors being 68kOhm and 420kOhm
# Example: If you use a 2:1 divider, then battery voltage = adc_voltage * 2
VOLTAGE_DIVIDER_RATIO = 420/68

# ADC reference voltage and resolution
ADC_REF_VOLTAGE = 3.3
ADC_MAX = 65535  # 16-bit resolution on RP2040's ADC in MicroPython

# Shutdown threshold (in volts)
CUTOFF_VOLTAGE = 2.4

# Output pin to disable the OR controller (active low)
enable_pin = Pin(15, Pin.OUT)  

# === FUNCTIONS ===

def read_voltage(adc):
    raw = adc.read_u16()
    voltage = (raw / ADC_MAX) * ADC_REF_VOLTAGE * VOLTAGE_DIVIDER_RATIO
    return voltage

def check_if_power_off_req(supercap_1, supercap_2):
    v_supercap1 = read_voltage(supercap_1)
    v_supercap2 = read_voltage(supercap_2)
    
    print("Battery 1: {:.2f} V | Battery 2: {:.2f} V".format(v_supercap1, v_supercap2))

    if v_supercap1 <= CUTOFF_VOLTAGE or v_supercap2 <= CUTOFF_VOLTAGE:
        print("Supercapacitor voltages below 2.4V! Shutting down OR controller.")
        enable_pin.value(1)  # Disable OR controller (active-low OFF)
    else:
        enable_pin.value(0)  # Enable OR controller (active-low ON)

    time.sleep(1)  # Delay between checks