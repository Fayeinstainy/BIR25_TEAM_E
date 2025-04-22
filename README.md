# Smart Swarmica - A Swarm Ant Robots Project
## Overview
This project is part of a biologically-inspired swarm robot system, where multiple robots cooperate to perform tasks such as locating a wireless charger and coordinating actions using IR signals.
All circuities were **initially developed and tested on a Raspberry Pi Pico**, and later **finalized on a custom PCB using the same RP2040 microcontroller chip** for integration into the final robot design.

## Hardware Component 

- **IR LED**: IR333
- **IR Receiver**: TSOP38238
- **Microcontroller**: RP2040
- **IMU**:
- **Other**: Resistors, Transistors (for LED driving), 38kHz signal source (via PWM)
## System Power Architecture
![new_robot_power_architecture](https://github.com/user-attachments/assets/9395186a-cf4d-4508-8e1b-a4c97f948f56)

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
## Obstacle Avoidance
- Based on detecting reflection of IR signal from nearby obstacles.
- If TSOP382 receives the robot’s own IR pulses reflected from a wall, it triggers a "wall detected" event.
## Infrared Code Flashing
