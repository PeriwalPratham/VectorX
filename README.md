# VectorX
## WRO Future Engineers 2026

<img width="501" height="570" alt="VectorX Logo" src="https://github.com/user-attachments/assets/5b4f19d7-6c34-4ac3-b680-ea389b7f9f41" />

VectorX is our autonomous vehicle developed for the WRO Future Engineers 2026 competition.
This repository documents our engineering process, mechanical and electrical systems, software architecture, autonomous navigation, testing, and design iterations.

[![Website](https://img.shields.io/badge/Website-Visit-blue?style=for-the-badge&logo=googlechrome&logoColor=white)](https://yourwebsite.com)
![Future Engineers](https://img.shields.io/badge/Future%20Engineers-0057B7?style=for-the-badge)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-A22846?style=for-the-badge&logo=raspberrypi&logoColor=white)
![Arduino Uno](https://img.shields.io/badge/Arduino%20Uno-00979D?style=for-the-badge&logo=arduino&logoColor=white)

## Table of Contents

- [Introduction](#introduction)
- [The Team](#the-team)
- [The Challenge](#the-challenge)
- [The Vehicle](#the-vehicle)
- [Performance Videos](#performance-videos)

- [Mobility and Mechanical Design](#mobility-and-mechanical-design)
  - [Chassis](#chassis)
  - [Drivetrain](#drivetrain)
    - [Drive Motor](#drive-motor)
    - [Motor Driver](#motor-driver)
  - [Steering](#steering)
    - [Servo Motor](#servo-motor)

- [Power and Sensor Architecture](#power-and-sensor-architecture)
  - [Power System](#power-system)
    - [Battery](#battery)
    - [Voltage Regulator](#voltage-regulator)
  - [Controllers](#controllers)
  - [Sensors](#sensors)
    - [Camera](#camera)
    - [IMU](#imu)
    - [Distance Sensors](#distance-sensors)
  - [Wiring Diagram](#wiring-diagram)
  - [PCB Design](#pcb-design)

- [Software Architecture](#software-architecture)
  - [Overall Program Flow](#overall-program-flow)
  - [Lane Following](#lane-following)
  - [Obstacle Detection and Avoidance](#obstacle-detection-and-avoidance)
  - [Parking Strategy](#parking-strategy)
  - [Code by Component](#code-by-component)

- [Systems Thinking and Engineering Decisions](#systems-thinking-and-engineering-decisions)
  - [Design Constraints](#design-constraints)
  - [Key Tradeoffs](#key-tradeoffs)
  - [Testing and Iteration Log](#testing-and-iteration-log)
  - [Risks and Failure Modes](#risks-and-failure-modes)

- [Build Guide](#build-guide)
  - [Step 1: Print the Parts](#step-1-print-the-parts)
  - [Step 2: Assemble the Chassis](#step-2-assemble-the-chassis)
  - [Step 3: Assemble the Powertrain](#step-3-assemble-the-powertrain)
  - [Step 4: Wire the Electronics](#step-4-wire-the-electronics)
  - [Step 5: Final Assembly](#step-5-final-assembly)
  - [Step 6: Upload the Code](#step-6-upload-the-code)

- [Cost Report](#cost-report)
- [Resources](#resources)
  - [3D Models](#3d-models)
  - [Images](#images)
- [License](#license)



## Introduction

## The Team

## The Challenge

## The Vehicle

## Performance Videos

---

## Mobility and Mechanical Design

### Chassis

### Drivetrain

#### Drive Motor

#### Motor Driver

### Steering

#### Servo Motor

---

## Power and Sensor Architecture

### Power System

#### Battery

#### Voltage Regulator

### Controllers

### Sensors

#### Camera

#### IMU

<img width="1024" height="694" alt="mpu6050" src="https://github.com/user-attachments/assets/43787b9a-8cb0-4fca-b6b4-922ac4cd07ab" />

- **Model:** MPU-6050
- **Type:** 6-axis IMU (3-axis accelerometer + 3-axis gyroscope)
- **Function:** Measures orientation and angular velocity to track turns and detect collisions
- **Interface:** I2C (SDA/SCL)

#### Distance Sensors

<img width="800" height="800" alt="TOFxxxC-4-1816875055" src="https://github.com/user-attachments/assets/e5e50b81-aab1-44f8-a4a9-a0db099a9dc4" />

- **Model:** TOF200C (VL53L0X sensor)
- **Type:** Time-of-Flight (ToF) laser distance sensor
- **Function** Measures distance between the robot and the inner and outer wall
- **Interface** 

### Wiring Diagram

### PCB Design

---

## Software Architecture

### Overall Program Flow

### Lane Following

### Obstacle Detection and Avoidance

### Parking Strategy

### Code by Component

---

## Systems Thinking and Engineering Decisions

### Design Constraints

### Key Tradeoffs

### Testing and Iteration Log

### Risks and Failure Modes

---

## Build Guide

### Step 1: Print the Parts

### Step 2: Assemble the Chassis

### Step 3: Assemble the Powertrain

### Step 4: Wire the Electronics

### Step 5: Final Assembly

### Step 6: Upload the Code

---

## Cost Report

## Resources

### 3D Models

### Images

## License
