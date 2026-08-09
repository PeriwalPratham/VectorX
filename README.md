# VectorX
## WRO Future Engineers 2026

<div align="center">

<img width="501" height="570" alt="VectorX Logo" src="https://github.com/user-attachments/assets/b47728f1-0384-4bb1-a760-15034163b67b" />

<br />

[![Website](https://img.shields.io/badge/Website-Vector%20X-green?style=for-the-badge&logo=googlechrome&logoColor=white)](https://your-website-url.com)
[![YouTube](https://img.shields.io/badge/YouTube-Vector%20X-red?style=for-the-badge&logo=youtube&logoColor=white)](https://your-youtube-channel-url.com)

</div>

---

## So, what can you find here?

1. [The Project](#1-the-project)
2. [The Team](#2-the-team)
3. [The Vehicle](#3-the-vehicle)
4. [System Architecture](#4-system-architecture)
5. [Mechanical & Mobility System](#5-mechanical--mobility-system)
6. [Power & Sensor Architecture](#6-power--sensor-architecture)
7. [Software Architecture](#7-software-architecture)
8. [Autonomous Navigation & Obstacle Strategy](#8-autonomous-navigation--obstacle-strategy)
9. [Engineering Decisions & Trade-offs](#9-engineering-decisions--trade-offs)
10. [Testing, Calibration & Iteration](#10-testing-calibration--iteration)
11. [Reproducing VectorX](#11-reproducing-vectorx)
12. [Repository Guide](#12-repository-guide)
13. [Engineering Journal](#13-engineering-journal)

---

## 1. The Project

### 1.1 Overview
**VectorX** is our self-driving car built for the **World Robot Olympiad (WRO) Future Engineers (FE) 2026** competition. Our goal was to build a fast, reliable car that can navigate an obstacle-filled track autonomously. We 3D-printed our custom chassis & run everything on it using a "dual brain" method. It combines a **Raspberry Pi 5** for image processing & obstacle detection and an **Arduino Uno** for motor & sensor control.

### 1.2 The Challenge
The competition has two main challenges that the car needs to complete - 

* **Open Challenge -** The car must drive **3 consecutive laps** without hitting the walls in the fastest possible time. The drive direction (clockwise or counter-clockwise) is randomly picked right before the round. The car needs to steer through sharp 90° turns & stop on its own (at its starting position) after finishing the third lap.
* **Obstacle Challenge -** The car still drives 3 laps, but now there are **red and green traffic pillars** randomly placed on the track. Using the camera, the car must steer to the **right of red pillars** and to the **left of green pillars**. Once 3 laps have been completed, the car will look for the **magenta parking plates** and **parallel park** inside them.
  
### 1.3 Our Approach

When building VectorX, we had 3 simple goals - keeping the electronics stable, making the reaction time as fast as possible, and creating a car that runs reliably.

* **Two Brains -** We split up the computing work so nothing gets overloaded. The **Raspberry Pi 5** handles the camera feed and obstacle detection (OpenCV). The **Arduino Uno** reacts to this by moving the steering servo, adjusting motor speed, and reading sensor inputs.
* **Car-Style Steering -** VectorX steers like a real car - the front wheels use **Ackermann steering** to turn smoothly, and the rear axle uses a **mechanical differential** so the back wheels can spin at slightly different speeds during sharp turns. 
* **Smart Power Supply -** Fast DC motors drain the battery power while accelerating, causing the Raspberry Pi to crash (a brownout). To stop this, our 11.1V battery powers the motors directly, while a regulated 5V buck converter powers the Pi, Arduino, and sensors—all linked safely through a common ground.
* **Combining Multiple Sensors -** No single sensor is perfect, and the track is always changing. Instead of relying on just one input, we combine our **wide-angle camera (Pi Camera Module 3), laser distance sensors (ToF), and gyroscope (IMU)** to double-check every movement & increase accuracy.

### 1.4 System Overview
VectorX works using a simple system - **Sense ➔ Decide ➔ Act**
```text
       +-------------------------------------------------+
       |           Pi Camera Module 3 Wide               |
       +-----------------------+-------------------------+
                               |
                               | Captures Live Track Frames (CSI)
                               v
       +-------------------------------------------------+
       |                 Raspberry Pi 5                  |
       |  - Runs OpenCV vision processing                |
       |  - Detects red/green pillars & parking lines    |
       |  - Decides steering direction & speed           |
       +-----------------------+-------------------------+
                               |
                               | Sends Steering & Speed Commands 
                               | (USB Cable)
                               v
       +-------------------------------------------------+
       |                  Arduino Uno                    |
       |  - Reads MPU-6050 Gyro & ToF Distance Sensors   |
       |  - Runs PID motor control loops                 |
       |  - Sends precise physical output signals        |
       +--------------+-------------------+--------------+
                      |                   |
      PWM Speed & DIR |                   | Steering PWM
                      v                   v
      +-----------------------+   +----------------------+
      | DFRobot TB6612FNG     |   | REV Smart Robot      |
      | Motor Driver          |   | Steering Servo       |
      +-----------+-----------+   +----------------------+
                  |
                  v
      +-----------------------+
      | N20 Drive Motor       |
      | (w/ Encoder Feedback) |
      +-----------------------+
```
#### How this Loop Works:

1. **Sense -** The Pi Camera 3 Wide captures live track video, while the ToF distance sensors and MPU-6050 gyro measure wall distances and car orientation.
2. **Decide -** The Raspberry Pi 5 processes the camera feed using OpenCV to detect red/green traffic pillars and track lines. It calculates the necessary steering angle and target speed, then sends these commands to the Arduino over the USB cable.
3. **Act -** The Arduino Uno receives the speed and steering values, adjusts the REV Smart Servo for front-wheel Ackermann steering, and controls power to the drive motor via the TB6612FNG driver.
---

## 2. The Team

<div align="center">

![Team Photo](photos/team_photo.jpg)

### Team VectorX
**Country:** India

</div>

### 2.1 Team Members & Coach

#### Pratham Periwal
<table>
  <tr>
    <td width="200" align="center">
      <img src="photos/pratham.jpg" width="180" alt="Pratham Periwal" />
    </td>
    <td>
      Hi, I'm Pratham! I like xyz.
    </td>
  </tr>
</table>

#### Inaaya Sood
<table>
  <tr>
    <td width="200" align="center">
      <img src="photos/inaaya.jpg" width="180" alt="Inaaya Sood" />
    </td>
    <td>
      Hi, I'm Inaaya! I like xyz.
    </td>
  </tr>
</table>

#### Swasti Kedia
<table>
  <tr>
    <td width="200" align="center">
      <img src="About Team/Swasti Kedia.png" width="180" alt="Swasti Kedia" />
    </td>
    <td>
      Hi, I'm Swasti! I like xyz.
    </td>
  </tr>
</table>

#### Chirag Sir (Coach)
Helped with xyz

### 2.2 Member Roles & Contributions
* **Pratham Periwal:** xyz
* **Inaaya Sood:** xyz
* **Swasti Kedia:** xyz

---

## 3. The Vehicle

### 3.1 Vehicle Overview
### 3.2 Key Specifications & Hardware Summary

#### Vehicle Dimensions & Mass
* **Dimensions:** Width [X] mm × Length [Y] mm × Height [Z] mm (Fits within official 300mm × 200mm × 300mm limit)
* **Total Mass:** [X] g
* **Ground Clearance:** [X] mm
* **Kinematics:** 4-Wheel Drive with Ackermann Front Steering & Rear Differential Gearbox

#### Hardware Component Summary Table
| Category | Component Name | Model / Specification | Interface | Function |
| :--- | :--- | :--- | :--- | :--- |
| **Main Processor (SBC)** | Raspberry Pi 4 Model B | 4GB RAM / 64-bit OS | CSI / USB / UART | Runs high-level state machine, OpenCV vision, and path logic |
| **Microcontroller (MCU)** | Arduino Nano | ATmega328P (5V) | UART / PWM / I2C | Handles low-level motor PWM, sensor reading, and IMU loop |
| **Vision Camera** | Raspberry Pi Camera Module 3 Wide | Sony IMX708 (12MP, 120° FOV) | CSI | Captures track frames for HSV color filtering & obstacle detection |
| **Distance Sensors** | TOF200C | VL53L0X Laser ToF Sensor | I2C | Measures exact wall distances for centering & parking alignment |
| **Inertial Sensor (IMU)** | MPU-6050 | 6-Axis Gyroscope + Accelerometer | I2C | Tracks yaw rate and heading orientation for straight-line stability |
| **Drive Motor Driver** | Cytron 13A Driver | 5V–30V, 13A Continuous | PWM / DIR | Converts MCU logic signals to high-current power for DC motor |
| **Steering Actuator** | REV Smart Servo V2 / MG996R | Digital High-Torque Metal Gear | PWM (`Pin D9`) | Actuates front Ackermann steering rack |

---

### 3.3 Multi-View Photographs

#### Primary Views
| Front View | Back View | Top View | Bottom View |
| :---: | :---: | :---: | :---: |
| ![Front](photos/car_front.jpg) | ![Back](photos/car_back.jpg) | ![Top](photos/car_top.jpg) | ![Bottom](photos/car_bottom.jpg) |

#### Side Views
| Left Side | Right Side |
| :---: | :---: |
| ![Left](photos/car_left.jpg) | ![Right](photos/car_right.jpg) |

---

### 3.4 Demonstration Videos
* **Open Challenge Demonstration Video:** [YouTube Link]
* **Obstacle Challenge Demonstration Video:** [YouTube Link]

---

## 4. System Architecture

### 4.1 Hardware Architecture
### 4.2 Software Architecture
### 4.3 System Communication
### 4.4 Subsystem Integration
---

## 5. Mechanical & Mobility System

### 5.1 Chassis & Kinematics
### 5.2 Drive System & Differential
### 5.3 Steering System
### 5.4 Motors, Drivers & Selection Rationale

#### Drive Motor Driver
<img width="400" alt="Motor Driver Module" src="https://github.com/user-attachments/assets/e974975c-841e-4834-8ada-cf40c2051d88" />

* **Model:** Cytron 13A Single DC Motor Driver
* **Operating Voltage & Current:** 5V–30V, 13A Continuous (30A Peak)
* **Interface:** PWM Speed & DIR Digital Control from Microcontroller
* **Primary Function:** Drives the main rear DC motor based on steering PID outputs.
* **Selection Rationale ("Why We Chose It"):** Unlike standard L298N drivers (which drop ~2V across internal transistors and overheat), the NMOS design of the Cytron delivers near 100% battery power efficiency without overheating during rapid acceleration runs.

---

#### Steering Servo Motor
<img width="400" alt="REV Servo Motor" src="https://github.com/user-attachments/assets/112df6cb-7e90-4af8-a5c2-14de61a694c0" />

* **Model:** REV Smart Robot Servo V2 / MG996R
* **Type:** Digital High-Torque Metal-Gear Servo
* **Interface:** PWM Signal Pin (`D9` on Microcontroller)
* **Primary Function:** Operates the front Ackermann steering rack.
* **Selection Rationale ("Why We Chose It"):** Metal gears prevent stripping during high-speed wall impacts. High stall torque (>10 kg·cm) ensures instantaneous response times when the PID controller requests rapid corrective steering angles in tight corners.

---

### 5.5 Speed & Torque Calculations
* **Vehicle Mass ($m$):** [e.g., 1.2 kg]
* **Target Linear Speed ($v$):** [e.g., 1.5 m/s]
* **Wheel Diameter ($d$) & Radius ($r$):** [e.g., 65mm / 0.0325m]
* **Gear Ratio:** [e.g., 1:10]
* **Torque Reasoning:** Equations proving motor stall/operating torque ($T = F \cdot r$) can accelerate the vehicle without exceeding motor thermal limits.

---

### 5.6 Mechanical Design Decisions
### 5.7 Mechanical Iterations
---

## 6. Power & Sensor Architecture

### 6.1 Power System & Isolation
To prevent computing resets (brownouts) caused by motor current surges, power distribution is split into two isolated domains sharing a common ground:

### 6.2 Power Distribution
### 6.3 Power Budget Table
| Component Domain | Powered Hardware | Power Source / Voltage | Max Current Draw |
| :--- | :--- | :--- | :--- |
| **Logic Domain** | Raspberry Pi 4 / Arduino Nano / Sensors | 5V Regulator / Power Bank | 2.5 A |
| **Drive Domain** | DC Motor & Steering Servo | 2S 7.4V LiPo Battery | 5.0 A Peak |

---

### 6.4 Battery & Regulation
---

### 6.5 Sensors & Component Selection Rationale

#### Vision Camera
<img width="400" alt="Raspberry Pi Camera Module 3 Wide" src="https://github.com/user-attachments/assets/5c6cab85-ed41-4f66-8147-8fbd5683255c" />

* **Model:** Raspberry Pi Camera Module 3 Wide
* **Sensor & Resolution:** Sony IMX708 (12 Megapixel), 1080p @ 50fps
* **Interface:** CSI (Camera Serial Interface) directly to SBC
* **Primary Function:** Captures live track frames for BGR-to-HSV color filtering, identifying red/green pillars, and locating magenta parallel parking bounds.
* **Selection Rationale ("Why We Chose It"):** We selected the 120° wide-angle version over the standard 75° camera. The ultra-wide field of view allows the vision system to detect wall corners and red/green traffic pillars earlier when negotiating sharp 90° turns, eliminating the need for complex pan-tilt mechanisms.

---

#### Inertial Measurement Unit (IMU)
<img width="400" alt="MPU6050 IMU Module" src="https://github.com/user-attachments/assets/43787b9a-8cb0-4fca-b6b4-922ac4cd07ab" />

* **Model:** MPU-6050
* **Sensor Type:** 6-Axis Motion Tracking (3-Axis Gyroscope + 3-Axis Accelerometer)
* **Interface:** I2C (`SDA` / `SCL`)
* **Primary Function:** Measures yaw rate and angular heading velocity to maintain straight-line stability and assist turn verification.
* **Selection Rationale ("Why We Chose It"):** Offers high sample rates (up to 1kHz) with minimal power consumption (~3.9mA). Its built-in Digital Motion Processor (DMP) offloads sensor-fusion calculations from our primary microcontroller.

---

#### Distance Sensors
<img width="400" alt="TOF200C Distance Sensor" src="https://github.com/user-attachments/assets/e5e50b81-aab1-44f8-a4a9-a0db099a9dc4" />

* **Model:** TOF200C (VL53L0X Time-of-Flight Sensor)
* **Type:** Laser Time-of-Flight (ToF) Distance Sensor
* **Interface:** I2C
* **Primary Function:** Measures millimeter-exact distances to track walls for collision avoidance and parallel parking alignment.
* **Selection Rationale ("Why We Chose It"):** Ultrasonic sensors (HC-SR04) suffer from wide 15° beam reflection angles and echo interference when bouncing off smooth track walls at an angle. Time-of-Flight laser sensors use a narrow infrared beam, giving reliable distance readings regardless of wall color or angle.

---

### 6.6 Sensor Placement Geometry
### 6.7 Sensor Calibration
### 6.8 Sensor Failure Modes & Mitigation
### 6.9 Wiring Diagram
![Wiring Diagram](schematics/wiring_diagram.png)

---

## 7. Software Architecture

### 7.1 Software Overview
### 7.2 Software Structure
### 7.3 Code Modules
### 7.4 Control Flow & State Machine
### 7.5 Control Architecture
### 7.6 Communication Protocols
### 7.7 Dependencies & Software Stack
---

## 8. Autonomous Navigation & Obstacle Strategy

### 8.1 Navigation Overview
### 8.2 Direction & Sign Detection
### 8.3 Lane / Wall Following
### 8.4 Obstacle Detection
### 8.5 Obstacle Management Strategy
### 8.6 Parallel Parking Strategy
### 8.7 Control Algorithm
Steering angle $\delta(t)$ is dynamically calculated using a Proportional-Integral-Derivative (PID) loop:
$$\delta(t) = K_p e(t) + K_i \int e(t)dt + K_d \frac{de(t)}{dt}$$

### 8.8 Edge Cases & Safeguards
---

## 9. Engineering Decisions & Trade-offs

### 9.1 Design Constraints
### 9.2 Key Engineering Decisions
### 9.3 Risk Management
---

## 10. Testing, Calibration & Iteration

### 10.1 Testing Methodology
### 10.2 Component Testing
### 10.3 Subsystem Testing
### 10.4 Full-System Testing
### 10.5 Calibration Procedures
### 10.6 Test Results
### 10.7 Design Iterations

#### Evolution of VectorX
| Version | Key Features & Setup | Observations / Limitations Found | Action Taken / Changes Made |
| :--- | :--- | :--- | :--- |
| **Prototype V1** | Off-the-shelf 2WD chassis, single Ultrasonic sensor, direct DC drive without differential. | Suffered from tire slip on corners, erratic distance readings off angled walls, and high CoG. | Shifted to Ackermann steering, 3D printed baseplate, and mechanical differential. |
| **Prototype V2** | 3D-printed Ackermann chassis, single 5V power bank for logic + motors, 75° camera. | Motor current surges caused Raspberry Pi resets; limited camera FOV missed wall turns early. | Separated logic and drive power domains; upgraded to 120° Wide-Angle camera. |
| **Final Build (V3)** | Custom PETG deck, dual isolated power circuits, wide-angle camera + TOF200C laser distance array. | Stable 30+ FPS vision processing, zero controller resets, precise wall centering and parallel parking. | Finalized software tuning and state machine logic. |

---

### 10.8 Problems & Solutions
---

## 11. Reproducing VectorX

### 11.1 Hardware Requirements
### 11.2 Bill of Materials (BOM)
| Component | Description / Spec | Qty | Unit Cost (₹) | Total Cost (₹) | Source / Vendor |
| :--- | :--- | :---: | :---: | :---: | :--- |
| | | | | | |
| **Total Build Cost** | | | | **₹0.00** | |

---

### 11.3 CAD & Manufacturing Files
### 11.4 Wiring Instructions
### 11.5 Software Requirements
### 11.6 Installation
### 11.7 Building / Compiling
### 11.8 Uploading to Controllers
### 11.9 Configuration
### 11.10 Calibration
### 11.11 Running VectorX
---

## 12. Repository Guide

### 12.1 Repository Structure
```text
├── cad/                  # 3D model files (.STL, .STEP)
├── schematics/           # Wiring diagrams and PCB schematics
├── src/                  # Main source code (Vision, Control, Drivers)
├── photos/               # Vehicle views and team photos
├── docs/                 # Journal entries, testing logs, and telemetry
└── README.md             # Main engineering documentation
```

### 12.2 Folder Descriptions
### 12.3 Where to Find What
### 12.4 Version History
---

## 13. Engineering Journal
---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
