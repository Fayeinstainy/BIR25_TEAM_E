# Smart Swarmica - A Swarm Ant Robots Project
## Overview
This project is part of a biologically-inspired swarm robot system, where multiple robots cooperate to perform tasks such as locating a wireless charger and coordinating actions using IR signals.
All circuities were **initially developed and tested on a Raspberry Pi Pico**, and later **finalized on a custom PCB using the same RP2040 microcontroller chip** for integration into the final robot design.

## Hardware Component 

- **IR LED**: IR333
- **IR Receiver**: TSOP38238
- **Microcontroller**: RP2350-based Raspberry Pi Pico 2W
  
- **Other**: Resistors, Transistors (for LED driving), 38kHz signal source (via PWM)

## System Architecture
![final_robot_sys_architecture](https://github.com/user-attachments/assets/d5efba0b-72d6-4d2d-bf08-09f5cb9b66ce)

## Power System Architecture (Normal Operation Mode)
![new_robot_power_architecture](https://github.com/user-attachments/assets/9395186a-cf4d-4508-8e1b-a4c97f948f56)

## Software Architecture
![Software_algorithm drawio-2](https://github.com/user-attachments/assets/e782ca1f-5753-40df-9293-42e803d6a72f)
## Motor Control
## Navigation
## Infrared Communication
- Uses **modulated IR signals** at 38kHz for one-way signaling between robots.
- Encodes simple messages (e.g. "Relative location is (4, 12)", "Stop Moving").
- Receiver uses TSOP382 to detect incoming signals reliably even in ambient light.

### How it works:
1. IR LED emits 38kHz modulated pulses.
2. TSOP382 detects signal and triggers logic in firmware.
3. Signal interpreted as communication or wall proximity.

## PCB Design
Designed using kiCAD 9.0, project files, schematic and PCB pdfs under bio_robots/ folder, featuring the following features:
- Populated: Common anode RGB LED, 3-pairs of IR transmitters and receivers, full bridge rectifier, parallel chargers for the supercapacitors, OR controller.
- Unpopulated: ICM-20948, 1.8V regulator, level shifters, bypass strategy (U12, D10-D13)

## Obstacle Avoidance
- Based on detecting reflection of IR signal from nearby obstacles.
- If TSOP382 receives the robot’s own IR pulses reflected from a wall, it triggers a "wall detected" event.
##  WI-FI Programming Mode
