# raspi-lf
Line Follower Project for Raspberry Pi

## Hardware
* [Elegoo Smart Robot Kit v2.0](https://www.elegoo.com/product/elegoo-uno-project-upgraded-smart-robot-car-kit-v2-0/)
  * V5.0 Extension Board V2.0
  * L298N Motor Driver Board V2.0
  * Ultrasonic Sensor
  * Servo Motor
  * IR Receiver
  * Line Tracking Module
* [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
* MP1584EN DC-DC Buck Converter
* 0.96" Inch IIC 128x64 Oled LCD

## Raspberry Pi Zero W Pinouts

| Component      | Raspberry Pi Pin | BCM    | Extension Board |
|:---------------|:----------------:|:------:|:---------------:|
| All            | 2                |        | VIN             |
| OLED LCD (SDA) | 3                | GPIO 2 |                 |
| OLED LCD (SCL) | 5                | GPIO 3 |                 |
| All            | 6                |        | GND             |
| Bluetooth (TX) | 8                | GPIO 14| IO1             |
| Bluetooth (RX) | 10               | GPIO 15| IO0             |
| Tracking Mod 1 | 11               | GPIO 17| IO10            |
| Tracking Mod 2 | 13               | GPIO 27| IO4             |
| Tracking Mod 3 | 15               | GPIO 22| IO2             |
| IR Receiver    | 16               | GPIO 23| IO12            |
| Servo Motor    | 18               | GPIO 24| IO3             |
| L298N (M1)     | 31               | GPIO 6 | IO7             |
| L298N (M2)     | 29               | GPIO 5 | IO6             |
| L298N (M4)     | 32               | GPIO 12| IO9             |
| L298N (M3)     | 33               | GPIO 13| IO8             |
| L298N (ENA)    | 36               | GPIO 16| IO5             |
| L298N (ENB)    | 37               | GPIO 26| IO11            |
| UltraS (Trig)  | 38               | GPIO 20| A5              |
| UltraS (Echo)  | 40               | GPIO 21| A4              |

## Line Tracking Module Test
The line tracker module test program is setup to use the following pins on the Raspberry Pi

Connections to Raspberry Pi:

| Component      | Raspberry Pi Pin | BCM    | Extension Board |
|:---------------|:----------------:|:------:|:---------------:|
| Tracking Mod 1 | 11               | GPIO 17| IO10            |
| Tracking Mod 2 | 13               | GPIO 27| IO4             |
| Tracking Mod 3 | 15               | GPIO 22| IO2             |

## Motor Driver Test
The motor driver test program is setup to use the following pins on the Raspberry Pi

Connections to Raspberry Pi:

| Component      | Raspberry Pi Pin | BCM    | Extension Board |
|:---------------|:----------------:|:------:|:---------------:|
| L298N (M1)     | 31               | GPIO 6 | IO7             |
| L298N (M2)     | 29               | GPIO 5 | IO6             |
| L298N (M4)     | 32               | GPIO 12| IO9             |
| L298N (M3)     | 33               | GPIO 13| IO8             |
| L298N (ENA)    | 36               | GPIO 16| IO5             |

### L298N Control
Pins IN1 and IN2 control forward and reverse of the right motor.
ENA turns the right motors on and off.

Pins IN3 and IN4 control forward and reverse of the left motor.
ENB turns the left motors on and off.

| ENA | IN1 | IN2 | IN3 | IN4 | ENB | DC Motor Status |
|:---:|:---:|:---:|:---:|:---:|:---:|-----------------|
| 0   | X   | X   | X   | X   | 0   | Stop            |
| 1   | 1   | 1   | 1   | 1   | 1   | Braking         |
| 1   | 0   | 1   | 0   | 1   | 1   | Forward         |
| 1   | 1   | 0   | 1   | 0   | 1   | Backward        |
