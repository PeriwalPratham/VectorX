# VectorX
## WRO Future Engineers 2026

<div align="center">

<img width="588" height="669" alt="VectorX Logo" src="https://github.com/user-attachments/assets/cdfead13-dfc9-4b0e-b124-f1bc8a1a2785" />


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

#### Key Performance Specs
* **Dimensions -** x mm × y mm × z mm (Fits WRO 300mm x 200mm limit)
* **Steering -** Front Ackermann Steering (REV Smart Servo)
* **Drive System -** Rear Mechanical Differential driven by DC Motor
* **Dual-Brain Compute -** Raspberry Pi 5 + Arduino Uno

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
      +-------------------------+
      | N20 Drive Motor         |
      | (with Encoder Feedback) |
      +-------------------------+
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

### 2.1 Team Members & Roles

#### Pratham Periwal - role
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

#### Inaaya Sood - role
<table>
  <tr>
    <td width="200" align="center">
      <img src="photos/inaaya.jpg" width="180" alt="Inaaya Sood" />
    </td>
    <td>
      I am a 14-year-old Class 9 student at SVKM JV Parekh International School with a strong passion for robotics, programming, and engineering. I enjoy reading, coding, painting, and 3D designing, and I am always eager to explore new technologies and develop innovative solutions.

I love experimenting with new code, building hands-on projects, and transforming ideas into functional designs. Whether I am programming autonomous robots, creating CAD models, or solving engineering challenges, I enjoy combining creativity with logical thinking to design practical and efficient solutions.

I believe that every project is an opportunity to learn something new, and I am constantly looking for ways to improve my technical skills and broaden my understanding of robotics and automation.
    </td>
  </tr>
</table>

#### Swasti Kedia - role
<table>
  <tr>
    <td width="200" align="center">
      <img src="About Team/Swasti Kedia.png" width="180" alt="Swasti Kedia" />
    </td>
    <td>
      I am a 14-year-old, Class 10 student at Podar International School, Powai (CBSE). I enjoy playing the piano, practicing martial arts, reading books, running & exploring new fields. I love building things & doing hands-on work, which led me to robotics.
    </td>
  </tr>
</table>

### 2.2 Team Identity & Story

---

## 3. The Vehicle

### 3.1 Vehicle Overview
### 3.2 Key Specifications & Hardware Summary
### 3.3 Multi-View Photographs
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
### 5.5 Speed & Torque Calculations
### 5.6 Mechanical Design Decisions
### 5.7 Mechanical Iterations

---

## 6. Power & Sensor Architecture

### 6.1 Power System & Isolation
### 6.2 Power Distribution
### 6.3 Power Budget Table
### 6.4 Battery & Regulation
### 6.5 Sensors & Component Selection Rationale
### 6.6 Sensor Placement Geometry
### 6.7 Sensor Calibration
### 6.8 Sensor Failure Modes & Mitigation
### 6.9 Wiring Diagram

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
### 10.8 Problems & Solutions

---

## 11. Reproducing VectorX

### 11.1 Hardware Requirements
### 11.2 Bill of Materials (BOM)
| Component | Description / Spec | Qty | Unit Cost (₹) | Total Cost (₹) | Source / Vendor |
| :--- | :--- | :---: | :---: | :---: | :--- |
| | | | | | |
| **Total Build Cost** | | | | **₹0.00** | |

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
### 12.2 Folder Descriptions
### 12.3 Where to Find What
### 12.4 Version History

---

## 13. Engineering Journal

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
