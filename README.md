# VectorX
## WRO Future Engineers 2026

<div align="center">

<img width="588" height="669" alt="VectorX Logo" src="https://github.com/user-attachments/assets/cdfead13-dfc9-4b0e-b124-f1bc8a1a2785" />

<br />

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

<img width="5712" height="4284" alt="IMG_3038 (2)" src="https://github.com/user-attachments/assets/29931c7d-84a4-4217-aa9f-cb9609c3a573" />

### Team VectorX
**Country:** India

</div>

### 2.1 Team Members & Roles

#### Pratham Periwal - role
<table>
  <tr>
    <td width="200" align="center">
      <img width="180" height="240" alt="PHOTO-2026-08-12-10-03-59" src="https://github.com/user-attachments/assets/9f91404c-b2d6-4d42-bdbe-d5514d0d7505" />
    </td>
    <td>
      Hi, I'm Pratham! I am a 14-year-old from Podar International School.I love physics and programming which led me into robotics I love building and making projects and learning about new things
    </td>
  </tr>
</table>

#### Inaaya Sood - role
<table>
  <tr>
    <td width="200" align="center">
      <img src="About Team/Inaaya Sood.png" width="180" alt="Inaaya Sood" />
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

#### Why "VectorX"?
In physics, a **vector** has two components - direction and magnitude. That is basically what our car needs to do - figure out where to steer and how fast to drive at any given millisecond. 

The **X** stands for the unknowns. During the competition, we won't know the pillar layouts, driving direction, or track placement in advance. So, **VectorX** is basically a car that can handle any situation, no matter how hard it is.
#### The Logo
<div align="center">

<img width="352" height="401" alt="VectorX Logo" src="https://github.com/user-attachments/assets/3dd50386-06d9-41ec-b475-0aad7c5dafc4" />

</div>

We wanted a clean, modern logo for our team. The design uses a styled 'X' with sharp arrows to mirror our team name and the dynamic steering of our car.

---

## 3. The Vehicle

### 3.1 Vehicle Overview

Our Robot has been made after many iterations, with changes in ideology and thought; each component has been tested multiple times before being added to our build. Many parts have been tested against other components in the same category to see which fit our build ideology better. The main goal of our build has been to be simple,efficient and reliable while keeping up with the latest trends.

### 3.2 Key Specifications & Hardware Summary

**Dimensions & Weight**

| Spec | Value |
|:---|:---|
| Length | ____ mm |
| Width | ____ mm |
| Height | ____ mm |
| Weight | ____ kg |
| Wheel diameter | 56 mm |
| Compute | Raspberry Pi 5 (8GB) + Arduino Uno (dual-brain) |

**Drivetrain & Steering**

| Spec | Value |
|:---|:---|
| Steering | Front Ackermann steering, REV Robotics Smart Robot Servo |
| Drive | Rear mechanical differential, single N20 12V 300RPM motor w/ encoder |
| Motor driver | DFRobot TB6612FNG |
| Top speed (calculated) | ≈0.88 m/s / ≈3.17 km/h (see Section 5.5) |

**Sensing**

| Sensor | Function |
|:---|:---|
| Pi Camera 3 Wide (12MP, 120° FOV) | Lane/line detection, pillar & parking marker detection |
| VL53L0X ToF ×3 | Wall distance for cornering/wall-following |
| MPU-6050 IMU | Yaw tracking for turn/lap counting and orientation |

**Power**

| Spec | Value |
|:---|:---|
| Battery | 11.1V 3S LiPo, 3700 mAh |
| Logic regulation | 5V 5A buck converter → Pi 5 |
| Servo regulation | PDB 5V regulated header → steering servo |

> Fill in the blank dimensions/weight once the final chassis is measured — this table pulls from the same source data as Sections 1.1, 4.1, and the BOM (Section 11.2), so update all four together if any spec changes.

### 3.3 Multi-View Photographs
### 3.4 Demonstration Videos
* **Open Challenge Demonstration Video:** [YouTube Link]
* **Obstacle Challenge Demonstration Video:** [YouTube Link]

---

## 4. System Architecture

### 4.1 Hardware Architecture

We uses a **dual-brain architecture**, splitting compute between two controllers to benefit from their speciallities:

- **Raspberry Pi 5 (8GB)** — Handles camera input and all OpenCV-based image processing (block detection, color line detection, parking  detection).
- **Arduino Uno** — Handles real-time, low-latency tasks: reading the MPU-6050 gyro and ToF distance sensors, running PID motor control loops, and driving the steering servo and drive motor.

**Why we split compute this way:**
- Vision processing (OpenCV) is computationally heavy and non-deterministic in timing — unsuitable for a microcontroller.
- Motor/servo control and sensor polling need **consistent, low-latency timing**, which the Arduino's simpler real-time loop handles more reliably than a full Linux OS on the Pi.
- If the Pi's vision pipeline lags, the Arduino can still keep the car stable using gyro/ToF data independently.

**Core hardware components:**

| Subsystem | Component |
|-----------|-----------|
| Compute (vision) | Raspberry Pi 5 |
| Compute (control) | Arduino Uno |
| Camera | Pi Camera Module 3 Wide |
| Steering actuator | REV Robotics Smart Robot Servo |
| Drive motor | N20 12V 300RPM w/ Encoder |
| Motor driver | DFRobot TB6612FNG |
| Distance sensing | VL53L0X ToF ×3 |
| Orientation sensing | MPU-6050 IMU |
| Power | 11.1V battery → motors directly; 5V 5A buck converter → Pi/Arduino/sensors |

### 4.2 Software Architecture

VectorX runs two separate codebases, one per controller:

**Raspberry Pi 5 — Python**
- Handles camera capture and OpenCV-based image processing (pillar color detection, lane/wall detection, parking line detection)
- Sends steering angle and speed commands to the Arduino over USB serial
- Written as a single script handling capture, detection, and serial communication in sequence

**Arduino Uno — C++ (Arduino framework)**
- Reads sensor data (MPU-6050 gyro, VL53L0X ToF sensors)
- Runs PID control loops for motor speed and steering correction
- Outputs PWM signals to the TB6612FNG motor driver and REV steering servo
- Written as a single `.ino` sketch handling sensor reads, control logic, and actuator output in one file

We have kept both codes for the Arduino and the Raspberry Pi in a single-file respectively, prioritizing reliability and ease of debugging.

### 4.3 System Communication

The Raspberry Pi 5 and Arduino Uno communicate over a **USB serial connection**.

1. The Pi processes each camera frame with OpenCV 
2. These values are sent to the Arduino over USB serial.
3. The Arduino parses the incoming command, cross-checks it against its own sensor readings (ToF, gyro), and outputs the final PWM signals to the servo and motor driver.

This keeps a clear division of responsibility: the Pi give the data, and the Arduino decides *how* to safely execute it in real time.

---

## 5. Mechanical & Mobility System

### 5.1 Chassis & Kinematics

Our chassis uses a **car-like (Ackermann) kinematic model** rather than a differential-drive or holonomic setup. Since only the front wheels steer and the rear wheels drive, the robot is **non-holonomic** — it can only move along smooth curved paths and cannot rotate in place or strafe sideways.

During a turn, all four wheels rotate around a common **Instantaneous Center of Rotation (ICR)**. Because the inner and outer wheels trace circles of different radii, they must be angled differently to roll smoothly without scrubbing the tires against the ground.

**Key Kinematic Formulas**

| # | Formula | Description |
|:---|:---|:---|
| 1 | $R = \dfrac{L}{\tan(\delta)}$ | Bicycle model — turning radius from wheelbase and steering angle |
| 2 | $\tan(\delta_{inner}) = \dfrac{L}{R - \frac{W}{2}}$ | Inner wheel steering angle |
| 3 | $\tan(\delta_{outer}) = \dfrac{L}{R + \frac{W}{2}}$ | Outer wheel steering angle |
| 4 | $\cot(\delta_{outer}) - \cot(\delta_{inner}) = \dfrac{W}{L}$ | Ackermann condition — ensures no wheel scrubbing |
| 5 | $R_{min} = \dfrac{L}{\tan(\delta_{max})}$ | Minimum turning radius from max servo steering angle |

| Symbol | Meaning |
|:---|:---|
| L | Wheelbase (front-rear axle distance) |
| W | Track width (left-right wheel distance) |
| R | Turning radius (to rear axle center) |
| δ | Steering angle |

---

### 5.2 Drive System & Differential

Our rear axle uses a **mechanical differential** driven by a single N20 DC motor, allowing the left and right rear wheels to rotate at different speeds during turns.

**Why a differential instead of a rigid axle or dual independent motors:**

- **Eliminates wheel scrubbing** — during a turn, the outer rear wheel travels a longer arc than the inner wheel. A rigid axle forces both wheels to spin at the same speed, causing skidding; the differential lets them naturally rotate at different rates.
- **Reduces wear** — less scrubbing means less tire wear, less friction heat, and longer component life.
- **Better traction and stability** — both wheels stay in proper rolling contact instead of dragging.
- **Simpler than dual-motor control** — a single motor drives both wheels mechanically, unlike an independent dual-motor setup which would need encoder feedback and software to actively match wheel speeds.
- **Consistent with our Ackermann steering** — since the front steering already follows true Ackermann geometry, the rear differential keeps the whole drivetrain physically consistent with real car-like turning behavior.

> **Trade-off:** as a standard open differential, more torque is sent to whichever wheel has less resistance — meaning if one rear wheel loses traction, it can spin freely while the other gets underpowered.

---

### 5.3 Steering System

<img width="474" height="474" alt="Steering system" src="https://github.com/user-attachments/assets/ea54b908-6f74-498b-b326-aa50131c07f4" />

Our steering system depends on a servo motor. We tried a couple of different servo motors including the MG90S and its plastic version the SG90. However, these did not fit our build and had many problems including calibration drift and jittering.

Hence we settled on the **REV Robotics Smart Servo**. This had many advantages including a higher torque and all-metal gears, which made it resistant to damage. While testing, it also had less jitter, allowing us to control it more precisely.

---

### 5.4 Motors, Drivers & Selection Rationale

<img width="474" height="474" alt="N20 motor" src="https://github.com/user-attachments/assets/1a5511b5-4d45-442c-b605-7e1487fcc4c8" />

For our motor, we tried and tested many variations of the N20 motor at different RPMs. These were fast, produced enough torque, and were cheap to test out. Moreover, we could add an encoder to it, which we tested later on.

<img width="474" height="474" alt="Motor driver" src="https://github.com/user-attachments/assets/95f74a67-df66-483d-a2ee-9175d4e9228c" />

For our motor driver, we tested two options mainly: the L298P and the TB6612FNG. We ended up using the TB6612FNG, as the L298P had many problems including voltage fluctuations that prevented our motors from getting full voltage, and created noise that disrupted the working of other components. It also contains extra parts with no purpose for our build, such as a buzzer, which increased the mass of our robot.

The TB6612FNG had other advantages including its small dimensions, newer technology, and reduced voltage fluctuations.

---

### 5.5 Speed & Torque Calculations

The wheel's linear speed is given by:

```math
v = \frac{\pi \times D \times N}{60}
```

**Solved with our values:**

```math
v = \frac{\pi \times 0.056 \times 300}{60} \approx 0.88 \text{ m/s} \approx 3.17 \text{ km/h}
```

| Variable | Value | Description |
|:---|:---|:---|
| D | 0.056 m (56 mm) | Wheel diameter |
| N | 300 RPM | Motor speed |
| v | ≈ 0.88 m/s | Calculated linear speed |

---

### 5.6 Mechanical Design Decisions

Our chassis is **3D-printed**, chosen over laser-cut alternatives for its ability to create complex, integrated mounting geometry (motor mounts, sensor brackets, servo housings) in a single print rather than assembling multiple flat plates. This also allowed us to iterate quickly — reprinting and testing new versions within a day instead of waiting on external laser-cutting services.

Key design priorities for the chassis:
- **Compact footprint** to stay within the WRO 300mm × 200mm size limit
- **Rigid mounting points** for the Raspberry Pi 5, Arduino Uno, motor driver, and sensors to minimize vibration-induced camera blur and sensor noise
- **Low center of gravity**, keeping heavier components (battery, Pi) mounted low to improve stability during sharp turns
- **Easy access** to wiring and components for debugging without disassembling the whole chassis

---

### 5.7 Mechanical Iterations

We went through **2–3 major chassis iterations** before arriving at our final design.

| Iteration | Key Changes | Reason |
|:---|:---|:---|
| v1 | Initial base layout with mounts for Pi, Arduino, and motor | Establish basic component fit and wiring layout |
| v2 | Added a dedicated 3D-printed stand for the Raspberry Pi, along with custom-printed mounts for the ToF sensors and camera module | Replaced temporary fixes like double-sided tape with proper mechanical mounts, improving reliability and reducing the chance of components shifting during movement |
| v3 (Final) | Added an encoder to the drive motor and switched from the L298P to the TB6612FNG motor driver | The encoder enabled precise speed feedback for closed-loop motor control, while the TB6612FNG resolved voltage fluctuation and noise issues from the L298P (see Section 5.4) |

#### Each iteration was tested for fit, component clearance, and mechanical stability before moving to the next version, helping us catch design flaws early rather than during final assembly.
---

## 6. Power & Sensor Architecture

### 6.1 Power System & Isolation

The electrical system is designed with a hierarchical structure emphasizing stable logic voltages and high-current capability for the actuators. The core strategy is **isolation by regulation**. By using distinct regulators and power paths for logic and high-draw motors, sensitive microcontrollers (Raspberry Pi 5, Arduino Uno) are isolated from inductive noise, back-EMF spikes, and voltage dips caused by the high-torque steering servo and driving motor. A unified ground plane across all power levels guarantees clear signal references for high-speed communication buses (I2C, PWM, and Serial).

### 6.2 Power Distribution

Power flows from a primary high-capacity energy storage unit through a centralized Power Distribution Board (PDB), which splits energy into dedicated voltage domains tailored to component requirements:

```text
[ 11.1V 3S LiPo Battery (3700 mAh) ]
     |
     +---> [ PDB High-Power Rail ] ----> (11.1V Direct) ---> TB6612 Motor Driver (VM)
     |
     +---> [ 5V 5A Buck Converter ] ---> (Regulated 5V) ----> Raspberry Pi 5 (Master)
     |           |
     |     (USB Cable: Power + Serial)
     |           |
     |           v
     |     Arduino Uno (Slave)
     |           |
     |     (5V Logic Rail)
     |           |
     |           v
     |     Sensors (MPU6050, 3x VL53L0X)
     |
     +---> [ PDB 5V Regulated Header ] -> (Regulated 5V) ----> REV Smart Servo
```

### 6.3 Power Budget Table

The total current consumption was calculated under peak and nominal operating conditions to ensure adequate regulator sizing and long operating cycles.

| Component | Qty | Nom. Volt | Nom. Current | Max / Stall Current | Power Rail Source |
|:---|:---:|:---:|:---:|:---:|:---|
| Raspberry Pi 5 | 1 | 5.0V | 1.50 A | 3.00 A | 5V 5A Buck Converter |
| Arduino Uno | 1 | 5.0V | 0.05 A | 0.10 A | Raspberry Pi 5 (USB) |
| REV Smart Servo | 1 | 5.0V | 0.20 A | 2.00 A | PDB 5V Rail |
| N20 DC Motor | 1 | 11.1V | 0.30 A | 1.50 A | PDB 11.1V Rail (via TB6612) |
| VL53L0X ToF Sensors | 3 | 5.0V | 0.06 A (0.02A ×3) | 0.12 A (0.04A ×3) | Arduino 5V Output |
| MPU6050 IMU | 1 | 5.0V | 0.01 A | 0.02 A | Arduino 5V Output |
| **System Total** | **8** | – | **~2.12 A** | **~6.74 A** | 3S LiPo Battery Base |

### 6.4 Battery & Regulation

**Battery Selection Rationale**
An 11.1V 3S LiPo battery (3700 mAh) was chosen as the primary power source. The 11.1V nominal output delivers full voltage to the high-RPM N20 motor, achieving required track speeds without voltage starvation. The 3700 mAh capacity allows continuous testing and competition runs without suffering voltage droop under heavy actuator load.

**Regulation Architecture**
- **Primary Logic Regulation:** An external 5V 5A DC-DC buck converter steps down 11.1V directly to a steady 5V rail dedicated to the Raspberry Pi 5. The 5A headroom prevents low-voltage throttling during vision processing.
- **Actuator Power Domain:** The PDB's onboard 5V regulator independently powers the REV Smart Servo. Isolating servo power protects microcontrollers from high current transients during rapid Ackermann steering adjustments.

### 6.5 Sensors & Component Selection Rationale

| Component | Primary Function | Selection Rationale |
|:---|:---|:---|
| Raspberry Pi 5 (8GB) | Master Vision & Strategy | High CPU/GPU throughput handles real-time visual processing (Pi Camera 3 Wide) for lane detection and high-level path planning. |
| Arduino Uno | Low-Level Hardware Controller | Deterministic microsecond timing ideal for encoder interrupts, software I2C address management for ToF sensors, and hardware PWM generation. |
| Pi Camera 3 Wide | Visual Perception | 12MP resolution with a 120° wide field of view enables simultaneous detection of close-range wall lines and distant track markers. |
| VL53L0X ToF (3x) | Distance Measurement | Time-of-flight laser measurement provides millimeter accuracy (up to 1m) immune to ambient lighting variances, essential for wall-following. |
| MPU6050 IMU | Orientation & Heading | 6-axis accelerometer/gyroscope measures precise angular velocity (yaw) to maintain straight-line driving and confirm accurate 90° turns. |
| REV Smart Servo | Ackermann Steering | High-torque metal gear construction delivers precise steering angle positioning under load. |

### 6.6 Sensor Placement Geometry

Sensors are placed strategically around the vehicle chassis to optimize spatial coverage and minimize rotational movement artifacts:

```text
       [ PI CAMERA 3 WIDE ] (Centered, 120° FOV)
                |
     +----------+----------+
     |          |          |
[ ToF #1 Left ] [ ToF #2 Center ] [ ToF #3 Right ]
 (Angled 45°)     (Facing 0°)     (Angled 45°)
                |
        [ MPU6050 IMU ] (Centered at CG)
```

- **Center ToF (0°):** Monitors forward distance to obstacles, wall limits, and braking boundaries.
- **Left & Right ToFs (45°):** Detect lateral wall clearance for proportional steering adjustments in narrow corridors.
- **Central IMU:** Positioned at the vehicle's Center of Gravity (CG) to eliminate parasitic linear acceleration offsets on rotational gyro readings.

### 6.7 Sensor Calibration

**VL53L0X Distance Calibration**
Each Time-of-Flight sensor undergoes offset calibration against a flat surface at a fixed 200mm distance. The baseline distance difference is saved into Arduino EEPROM to adjust real-time range values during operation.

**MPU6050 Gyroscope Bias Calibration**
During the boot-up sequence, the robot remains stationary for 3 seconds. The Arduino samples 1,000 gyroscope readings across all 3 axes, computing static offsets (`G_off`) which are subtracted from subsequent rate measurements:

```text
Yaw_rate_corrected = Yaw_rate_raw - G_off
```

### 6.8 Sensor Failure Modes & Mitigation

| Sensor | Failure Mode | Detection Method | Automated Mitigation Strategy |
|:---|:---|:---|:---|
| Pi Camera 3 | Image Freeze / Obstruction | Visual frame entropy check drops to near-zero. | System falls back to ToF-only reactive navigation algorithm at reduced drive speed. |
| VL53L0X ToF | I2C Timeout / Out of Range | Return status flag != 0 for 3 consecutive cycles. | Faulty sensor ignored; vehicle extrapolates distance using adjacent ToF and IMU trajectory. |
| MPU6050 | Gyro Drift / Bus Lockup | Unrealistic yaw rate (>180°/s) without encoder motion. | Resets I2C bus via software; switches orientation reference to differential encoder odometry. |
| N20 Encoder | Wire Disconnection | Motor PWM > 50% but encoder delta count = 0. | System switches from distance-based state transitions to timed motion profiling. |

### 6.9 Wiring Diagram

The complete wiring layout below illustrates every pin-to-pin signal and power connection.

<img width="942" height="560" alt="Screenshot 2026-08-12 at 8 41 02 PM" src="https://github.com/user-attachments/assets/dfa898cf-7621-469a-8d6d-ada56d65b1e7" />

**Pre-Power Hardware Safety Checklist:**
1. Verify common ground continuity between Battery (–), PDB GND, Buck Converter GND, Pi 5 GND, Arduino GND, and Motor Driver GND.
2. Ensure Arduino is powered exclusively via the USB cable from Raspberry Pi 5 (no external voltage supplied to 5V or Vin pins).
3. Verify XSHUT lines for ToF sensors are wired to digital pins D10, D11, and D12 to enable sequential I2C initialization.

---

## 7. Software Architecture

> **Status:** The content below documents the current **Open Challenge** codebase (Arduino `.ino` + Python `vision_avoidance.py`). Only the motor driver hardware is being swapped before competition (L298N → TB6612FNG) — the control logic itself (proportional steering, gyro-based turn counting, 2-sensor wall-following) is staying as-is. Obstacle Challenge logic (pillar avoidance, parking) has not been documented yet — Section 8.4–8.6 will be completed once that code is added.

### 7.1 Software Overview

VectorX splits its software across two controllers, matching the dual-brain hardware split:

- **Raspberry Pi 5 (Python):** Detects the mandatory start direction (clockwise/counter-clockwise) from a colored floor line using OpenCV, then hands off full driving control to the Arduino for the remainder of the run.
- **Arduino Uno (C++):** Owns the real-time control loop — reads the IMU and ToF sensors, runs proportional wall-following steering, counts turns/laps via gyro integration, and drives the motor and servo directly.

This is a **handoff architecture** rather than a continuous shared-control loop: the Pi's only job during a run is a one-time direction read at the start line, after which the Arduino runs autonomously using its own sensors until it detects the run is complete.

### 7.2 Software Structure

```text
vectorx/
├── arduino/
│   └── vectorx_open_challenge.ino   # Low-level control: IMU, ToF, servo, motor
└── pi/
    └── vision_avoidance.py          # Direction detection + serial handshake
```

Both files are currently written as single monolithic files (one `.ino`, one `.py`) rather than split into modules — this keeps debugging simple during development, but see Section 9.2 for the reasoning and the trade-off this creates for readability as more logic (obstacle avoidance, parking) gets added.

### 7.3 Code Modules

**Arduino (`vectorx_open_challenge.ino`)**

| Function | Responsibility |
|:---|:---|
| `setup()` | Initializes pins, wakes the MPU6050, runs gyro calibration, sequentially re-addresses the two ToF sensors over I2C, attaches the servo, and stops the motor. |
| `calibrateGyro()` | Averages 150 raw Z-axis gyro samples at startup to compute a static bias offset (`gyroZOffset`), removing drift from later yaw readings. |
| `updateYaw()` | Reads the current Z-axis gyro rate, subtracts the bias, applies a 0.5°/s dead-band (to ignore sensor noise while stationary), and integrates it into a running `turnYaw` value using elapsed time (`dt`). |
| `readSerialFromPi()` | Non-blocking serial parser. Buffers incoming characters until `\n`, then matches `START` (with optional `CCW` flag) or `STOP` commands from the Pi, and echoes a handshake acknowledgment back. |
| `loop()` | Main control loop — see Section 7.4. |
| `moveForward()` / `stopMotor()` | Direct motor driver pin control (direction + PWM speed). |

**Raspberry Pi (`vision_avoidance.py`)**

| Function | Responsibility |
|:---|:---|
| `send_command()` | Writes an ASCII command + newline to the Arduino over serial and flushes the buffer immediately. |
| `detect_start_direction()` | Captures live frames, masks for orange vs. blue floor markings within a cropped scan zone, and returns `"CW"` or `"CCW"` based on which color has more matching pixels (with a 3-second timeout defaulting to `"CW"`). |
| Main block | Runs direction detection once, sends the `START_<direction>` command, then listens for Arduino status messages (printing them) until `ALL_TURNS_DONE_STOPPING` is received or the user interrupts with `Ctrl+C` (which sends `STOP`). |

### 7.4 Control Flow & State Machine

The Arduino's `loop()` implements a simple two-state machine driven by the `isRunning` flag:

```text
        ┌────────────┐   "START_CW" / "START_CCW"   ┌─────────────┐
        │   IDLE      │ ────────────────────────────▶│   RUNNING   │
        │ (servo      │                               │ (wall-      │
        │  centered,  │◀──────────────────────────────│  following, │
        │  motor off) │   "STOP"  OR  turnCount ≥ 13   │  turn count) │
        └────────────┘                               └─────────────┘
```

- **IDLE:** Motor stopped, servo held at `STRAIGHT`. The robot waits here until it receives a `START` command over serial.
- **RUNNING:** On every loop iteration, the robot updates its yaw estimate, checks whether it has completed another 90° turn, reads both ToF sensors, computes a proportional steering correction, and drives forward. The robot returns to IDLE automatically once `turnCount` reaches `MAX_TURNS`, or immediately if a `STOP` command arrives from the Pi.

**Turn/lap counting logic:** Every time the integrated `turnYaw` exceeds ±80° (`SINGLE_TURN_YAW`) *and* at least 1.8 seconds (`MIN_TURN_INTERVAL_MS`) have passed since the last counted turn, the code registers one turn and resets `turnYaw` to 0. This debounce prevents a single physical turn from being double-counted due to gyro noise.

> ⚠️ **Check before competition:** `MAX_TURNS` is set to `13`, but the inline comment says *"Exactly 12 turns (3 laps × 4 corners)"*. Confirm whether the 13th count is an intentional buffer (e.g. to guarantee the robot fully completes the last corner before stopping) or an off-by-one that should be corrected to `12`.

### 7.5 Control Architecture

Steering runs on **proportional control** based on ToF wall distance. This is staying as-is for this competition cycle — the "PID" language elsewhere in this README describes the longer-term target architecture, but the logic below is what's actually implemented and running:

```text
error = measured_distance_mm - TARGET_INNER_DIST   (TARGET_INNER_DIST = 180 mm)
steering_angle = STRAIGHT ± (error × Kp)             (Kp = 0.35)
steering_angle = constrain(steering_angle, MAX_RIGHT, MAX_LEFT)
```

- When driving **clockwise**, the right ToF sensor is treated as the inner-wall reference; when driving **counter-clockwise**, the left sensor is used instead — this keeps the robot hugging the inside of the track through corners.
- If the relevant sensor reads beyond 450 mm (meaning the wall has "opened up," typically at a corner gap), the code skips the proportional term entirely and commands a hard steering angle toward `MAX_RIGHT`/`MAX_LEFT` to actively cut into the turn rather than drift wide.
- Drive speed is currently a fixed PWM value (`DRIVE_SPEED = 210`) rather than a variable target — there's no speed ramp-down for corners or speed-up on straights yet.

### 7.6 Communication Protocols

The Pi and Arduino communicate over **USB serial at 115200 baud**, using a simple ASCII, newline-terminated command protocol:

| Direction | Message | Meaning |
|:---|:---|:---|
| Pi → Arduino | `START_CW` / `START_CCW` | Begin the run in the specified direction. |
| Pi → Arduino | `STOP` | Immediately halt the motor and center the servo. |
| Arduino → Pi | `HANDSHAKE_ACK_MOTORS_STARTED_<dir>` | Confirms the start command was received and parsed. |
| Arduino → Pi | `HANDSHAKE_ACK_MOTORS_STOPPED` | Confirms a stop command was received. |
| Arduino → Pi | `TURN_COMPLETED:<n>/<max>` | Sent each time a corner is counted, for live progress logging. |
| Arduino → Pi | `ALL_TURNS_DONE_STOPPING` | Sent once the lap count target is reached; the Pi uses this to end its own script cleanly. |

The Pi's serial read uses a short timeout (`0.01s`) so it never blocks the main loop while waiting for Arduino messages.

### 7.7 Dependencies & Software Stack

**Raspberry Pi 5:** Python 3, `opencv-python`, `numpy`, `picamera2`, `pyserial`

**Arduino Uno:** `Wire.h`, `VL53L0X.h` (Pololu library, based on sensor addressing calls used), `Servo.h`

---

## 8. Autonomous Navigation & Obstacle Strategy

> **Status:** Sections 8.1–8.3, 8.7, and 8.8 cover the **Open Challenge** behavior, which is implemented and documented below. Sections 8.4–8.6 (obstacle detection, obstacle avoidance, and parallel parking) belong to the **Obstacle Challenge** and are placeholders until that code is added — see the note at the end of each.

### 8.1 Navigation Overview

For the Open Challenge, VectorX uses a two-phase navigation approach: a one-time **vision-based start direction read** on the Raspberry Pi, followed by fully autonomous **IMU + ToF wall-following** on the Arduino for the remainder of the run. The Pi does not participate in steering decisions once the run starts — all reactive driving happens locally on the Arduino, which keeps the control loop fast and independent of camera frame rate or USB latency.

### 8.2 Direction & Sign Detection

Before the run starts, the Pi Camera scans a **colored floor line** to determine which direction (clockwise or counter-clockwise) the robot must drive, as randomly assigned by the competition:

1. The camera captures frames and crops out the top third of the image (`CROP_Y = 480 / 3`), restricting detection to the floor area directly in front of the robot rather than distant track features.
2. The cropped region is converted to HSV and masked against two color ranges — orange (→ clockwise) and blue (→ counter-clockwise).
3. Whichever color exceeds a 400-pixel threshold first is selected as the direction; if neither is detected within a 3-second timeout, the robot **defaults to clockwise**.
4. A live debug overlay (scan-zone boundary, pixel counts, and a mask thumbnail) is shown during this phase to make on-site tuning of the HSV thresholds easier.

Once a direction is chosen, the Pi sends `START_CW` or `START_CCW` to the Arduino and effectively steps back from further decision-making for the rest of the run.

### 8.3 Lane / Wall Following

Wall-following is handled entirely on the Arduino using the left/right ToF pair (see Section 7.5 for the exact control formula). The 3rd (center) ToF sensor in the BOM/target build is not read by the current control code:

- The sensor on the **inside of the current turn direction** (right sensor when driving CW, left sensor when driving CCW) is used as the live distance reference.
- The robot continuously steers to hold that sensor's reading near a fixed 180 mm target, using proportional correction.
- When the inner-wall sensor reads beyond 450 mm — indicating an open corner gap rather than a continuous wall — the robot switches to a fixed hard-steer command toward that side instead of trusting the (now unreliable) proportional error, actively cutting into the turn.

### 8.4 Obstacle Detection *(pending)*

Not yet implemented in the code provided. This section should describe how red/green traffic pillars are detected — most likely HSV color masking on the Pi Camera feed (following the same pattern as the direction-line detection in Section 8.2), including bounding-box extraction, distance/size estimation, and how detections are communicated to the Arduino.

### 8.5 Obstacle Management Strategy *(pending)*

Not yet implemented. Should describe the decision logic for steering right of red pillars / left of green pillars — e.g. whether this is handled by the Pi (sending a lateral offset command) or by extending the Arduino's serial protocol with a pillar-side flag, and how the robot resumes normal wall-following after clearing each pillar.

### 8.6 Parallel Parking Strategy *(pending)*

Not yet implemented. Should describe how the magenta parking plates are detected, how the final parking maneuver is planned (e.g. a scripted reverse-and-turn sequence vs. a closed-loop approach using ToF distances), and how the robot confirms it has stopped fully inside the marked zone.

### 8.7 Control Algorithm

The full per-loop control sequence on the Arduino, once `isRunning` is true:

1. Parse any pending serial command from the Pi (non-blocking).
2. Update the integrated yaw estimate from the gyro (`updateYaw()`).
3. Check whether accumulated yaw has crossed the 80° single-turn threshold with the 1.8 s debounce satisfied; if so, increment `turnCount` and reset `turnYaw`.
4. If `turnCount` has reached the target (13), stop the motor, center is not explicitly re-commanded here, and the state returns to idle.
5. Read both ToF sensors.
6. Compute the proportional steering correction (or hard-steer if the inner wall reading exceeds 450 mm) based on the current direction.
7. Command the servo to the resulting angle.
8. Drive the motor forward at the fixed `DRIVE_SPEED`.

### 8.8 Edge Cases & Safeguards

- **Gyro drift while stationary:** a 0.5°/s dead-band in `updateYaw()` prevents small sensor noise from slowly accumulating into a false turn count while the robot is sitting still.
- **Double-counting a single turn:** the 1.8 s minimum interval between counted turns (`MIN_TURN_INTERVAL_MS`) stops one physical corner from registering as two turns if the gyro output is noisy mid-turn.
- **Open corner gaps:** the >450 mm fallback in the steering logic (Section 8.3) prevents the proportional controller from reacting badly to the sudden jump in distance reading that happens when a wall segment ends at a corner.
- **Direction-detection timeout:** if neither the orange nor blue floor marking is confidently detected within 3 seconds, the robot defaults to clockwise rather than stalling indefinitely at the start line — worth confirming this is the safe default for how the competition assigns direction.
- **Not yet handled:** loss of one ToF sensor mid-run, camera obstruction, or serial disconnection between the Pi and Arduino don't currently have explicit fallback behavior in this codebase (contrast with the failure-mode table documented in Section 6.8, which describes mitigations not yet reflected in the code).

---

## 9. Engineering Decisions & Trade-offs

### 9.1 Design Constraints

While designing our WRO Future Engineers robot, we had to consider the competition rules, the size of the robot, the available space for components, and the need for reliable autonomous driving. These constraints affected almost every part of our design.

**1. Robot Size and Weight**
The robot has to stay within the size limits given by WRO. Our final robot dimensions and weight are:
- **Length:** ____ mm
- **Width:** ____ mm
- **Height:** ____ mm
- **Weight:** ____ kg

Because of the limited size, we had to carefully arrange all the motors, electronics, battery, sensors, and other parts inside the robot.

**2. Four-Wheel Design and Steering**
Our robot uses four wheels, with the rear wheels used for driving and the front wheels used for steering. We used an **Ackermann steering system** so that the front wheels can turn at different angles while taking a corner. This helps the robot turn more smoothly.

**3. Autonomous Driving**
The robot has to drive and make decisions without manual control. We therefore used a **Raspberry Pi 5** with a **Pi Camera 3 Wide** as the main vision system. We also used an **MPU6050** to get information about the robot's movement and orientation.

**4. Limited Space for Electronics**
There were many components that had to fit inside the robot, including the Raspberry Pi 5, Arduino Uno, motor driver, battery, buck converter, MPU6050 and wiring. To solve this problem, we used a multi-level chassis so that the components could be placed on different levels instead of taking up the same space.

**5. Drive Motor Selection**
We used **300 RPM N20 DC motors** to drive the rear wheels. The motors had to provide enough speed while still giving the robot enough control during turns and acceleration. The motors were connected to the rear wheels through the drivetrain.

**6. Steering Motor Selection**
The front Ackermann steering is controlled using a **REV 1097 servo motor**. The servo was chosen because it allows us to control the steering angle more accurately than a normal DC motor.

**7. Power Supply**
The robot is powered by a **3700 mAh LiPo battery**. Since the different components need different voltages, we used an **XL4015 5A buck converter** to reduce and regulate the voltage for the electronics.

**8. Camera Position**
The Pi Camera 3 Wide was placed on a raised structure at the front of the robot. This gives the camera a better view of the track and helps it see the course without the robot's chassis blocking the view. The camera mount was also made rigid so that it does not shake too much while the robot is moving.

**9. Stability**
The robot needs to stay stable while moving and turning. We tried to keep heavier components such as the battery and electronics lower in the chassis. The camera was placed higher only because it needed a better view, while the main body of the robot was kept low.

**10. Easy Maintenance**
Since we had to test the robot many times, we needed to be able to reach the electronics and mechanical parts easily. The different levels of the chassis make it easier for us to access the components, change wiring, and make adjustments when needed.

**11. Reliability**
The robot needs to work consistently during competition runs. We therefore tried to keep the mechanical parts rigid, secure the electronics properly, and avoid unnecessary movement or interference between the different mechanisms. Our main goal was to make the robot reliable rather than only making it as fast as possible.

### 9.2 Key Engineering Decisions

During the design process, we made several important engineering decisions based on the performance we wanted from the robot. We compared different options and selected the ones that gave us a good balance between speed, accuracy, stability, and reliability.

**1. Rear-Wheel Drive**
We decided to use the rear wheels for driving instead of driving all four wheels. This made the drivetrain simpler and gave us more space at the front for the Ackermann steering system. It also made the front steering mechanism easier to control.

**2. Ackermann Steering**
We chose Ackermann steering for the front wheels because it gives the two front wheels different steering angles while turning. This helps the robot follow corners more smoothly and reduces unnecessary tyre slipping. We used a **REV 1097 servo motor** because it allows us to control the steering angle accurately.

**3. N20 300 RPM Drive Motors**
For the rear-wheel drive, we selected **N20 DC motors with 300 RPM**. We wanted a motor that was fast enough for the course but still controllable. Using two motors also keeps the drivetrain relatively simple and reduces the amount of space required.

**4. Raspberry Pi 5 for Main Computing**
We selected the **Raspberry Pi 5** as the main computer because the robot needs to process camera information and make decisions while moving. It gives us enough processing power for our vision-based autonomous system and allows us to run more advanced programs compared to using only a microcontroller.

**5. Pi Camera 3 Wide**
We selected the **Pi Camera 3 Wide** because having a wider field of view helps the robot see more of the track. We mounted it on a raised structure so that the camera has a clearer view and is less affected by the robot's own chassis.

**6. Arduino Uno for Additional Control**
We used an **Arduino Uno** along with the Raspberry Pi. The Raspberry Pi handles the higher-level processing, while the Arduino can handle some of the lower-level control tasks. This division helps reduce the amount of work being done by a single controller and makes the system easier to manage.

**7. MPU6050 for Motion Feedback**
We added an **MPU6050** to get information about the robot's movement and orientation. This gives us additional information apart from the camera and can help us understand how the robot is moving, especially during turns.

**8. TB6612FNG Motor Driver**
We selected the **DFRobot TB6612FNG motor driver** to control the N20 drive motors. It is compact, which was important because space inside the robot was limited. It also allowed us to control the direction and speed of the DC motors from our control system.

**9. Multi-Level Chassis**
One of our main design decisions was to use different levels in the chassis instead of putting everything on one flat plate. The lower section mainly supports the drivetrain and other heavier components, while the upper section holds electronics and other parts. This helped us use the available space more efficiently.

**10. Elevated Camera Mount**
We designed a tall camera mount instead of placing the camera directly on the main chassis. The main reason was to get a better view of the track. We also made the mount rigid because camera movement or vibration could affect the accuracy of image processing.

**11. Centralised Electronics Layout**
We tried to keep the main electronic components close to the centre of the robot. This helped keep the wiring shorter and made the weight distribution more balanced. It also made it easier to access the electronics during testing and troubleshooting.

**12. Focus on Reliability Over Maximum Speed**
We decided that making the robot extremely fast was not our main goal. A robot that moves slightly slower but can consistently detect the track, steer correctly, and complete the course is more useful in a competition. Therefore, we focused on getting stable driving and repeatable performance before increasing the speed.

### 9.3 Risk Management

While building and testing our robot, we identified different problems that could affect its performance during a competition. We tried to reduce these risks by testing each part separately and making the design stronger and easier to maintain.

| Risk | Possible Problem | How We Managed It |
|:---|:---|:---|
| **Motor failure** | One of the N20 motors could stop working or lose performance, causing the robot to move incorrectly. | We tested both drive motors regularly and checked the motor connections before testing and competition runs. |
| **Steering failure** | The steering servo could become loose or give an incorrect steering angle. | We secured the servo and steering mechanism properly and repeatedly tested the steering angles before running the robot. |
| **Wheel slipping** | The wheels could lose grip during acceleration or turning, affecting the robot's path. | We tested the robot at different speeds and adjusted the driving speed and steering to keep the movement stable. |
| **Camera movement** | Vibration or movement of the camera could affect image processing and cause incorrect decisions. | We used a rigid camera mount and checked that the camera stayed in the same position during testing. |
| **Poor lighting** | Changes in lighting could make it harder for the camera to detect track elements correctly. | We tested the vision system under different lighting conditions and adjusted the camera and software settings when needed. |
| **Sensor errors** | Incorrect MPU6050 readings could affect the robot's understanding of its movement or orientation. | We tested and calibrated the sensor before using its readings in the robot's control system. |
| **Loose wiring** | A loose wire could disconnect a motor, sensor, or controller during a run. | We kept the wiring organised and secured important connections so that they would not easily come loose because of vibration. |
| **Power problems** | A low battery or unstable voltage could cause the electronics or motors to behave unexpectedly. | We used the 3700 mAh LiPo battery with the XL4015 buck converter and checked the battery and power connections before testing. |
| **Mechanical damage** | Parts of the chassis, steering system, or camera mount could become loose or damaged after repeated testing. | We regularly checked screws, brackets, gears, and other mechanical connections and repaired or tightened them when required. |
| **Software failure** | A program error could cause the robot to make the wrong movement or stop during a run. | We tested the software in small sections first and then tested the complete autonomous system repeatedly. |
| **Communication between controllers** | Problems between the Raspberry Pi and Arduino could result in incorrect or delayed commands. | We tested the communication separately and checked that commands were being received correctly before full-course testing. |
| **Unexpected robot behaviour** | The robot could behave differently on the actual competition field compared to our practice area. | We performed repeated full-course tests instead of testing only individual sections. This helped us find problems that appeared during complete runs. |

Overall, our main approach to risk management was **testing, checking, and improving the robot repeatedly**. Instead of waiting until the competition to find problems, we tried to identify possible failures during practice and fix them before the final runs. This helped us make the robot more reliable and gave us more confidence during competition.

---

## 10. Testing, Calibration & Iteration

### 10.1 Testing Methodology

Our overall approach followed a **bottom-up progression**: individual components were tested in isolation first (numbered test scripts `01`–`13`, plus standalone vision/diagnostic tests — see Section 10.2), then combined into subsystems (Section 10.3), and finally validated through repeated full-course runs rather than relying on isolated section tests alone (see Section 9.3). The reasoning was that the robot could behave differently on the actual competition field compared to our practice area, so complete runs were prioritized over assuming that passing subsystems would guarantee full-course success.

> This section documents *what* was tested and *how*; **Section 9.3 (Risk Management)** documents *why* each area was considered risky enough to warrant this testing.

### 10.2 Component Testing

Individual hardware components and detection algorithms were each validated with a dedicated standalone test script before being wired into the main control code. Full source for each test lives in [`/tests`](tests/) — linked below.

**Actuators**

| Test | Hardware | What it verifies |
|:---|:---|:---|
| [`01_servo_test.ino`](tests/01_servo_test.ino) | Steering servo (D9) | Automatic sweep across LEFT/CENTRE/RIGHT, plus manual angle entry over serial, to confirm range and check for jitter or calibration drift |
| [`02_motor_test.ino`](tests/02_motor_test.ino) | N20 drive motor (PWM D11, direction D13) | Verifies direction control and speed (PWM) response |
| [`buzzer_test.ino`](tests/buzzer_test.ino) | Buzzer (D4) | Confirms wiring and plays multiple frequency/beep patterns |

**Sensors**

| Test | Hardware | What it verifies |
|:---|:---|:---|
| [`04_single_vl53l0x_test.ino`](tests/04_single_vl53l0x_test.ino) | 1× VL53L0X ToF | Confirms basic range readings from a single sensor before adding the I2C-addressing complexity of running two on the same bus |
| [`03_dual_vl53l0x_test.ino`](tests/03_dual_vl53l0x_test.ino) | 2× VL53L0X ToF | Validates the XSHUT-based sequential re-addressing (`0x30` left / `0x31` right) needed to run both sensors on one I2C bus |
| [`mpu_heading_test.ino`](tests/mpu_heading_test.ino) | MPU6050 | Calibrates Z-axis gyro bias (300-sample average) at startup, then integrates heading over time to check drift-corrected yaw tracking |
| [`07_camera_test.py`](tests/07_camera_test.py) | Pi Camera 3 Wide | Confirms basic frame capture from the Pi |

**Vision / detection algorithms**

| Test | What it verifies |
|:---|:---|
| [`08_hsv_calibrator.py`](tests/08_hsv_calibrator.py) | Interactive tool to find HSV threshold ranges for each color — used to generate the values plugged into the detection scripts below |
| [`09_red_green_test.py`](tests/09_red_green_test.py) | Red/green traffic pillar detection (bounding box, centre, angle) — for Obstacle Challenge pillar avoidance |
| [`10_blue_orange_test.py`](tests/10_blue_orange_test.py) | Orange/blue start-direction line detection — same algorithm used in Section 8.2 |
| [`pink_parking_test.py`](tests/pink_parking_test.py) | Magenta parking-zone detection (bounding box, centre, width/height, area) — for the Obstacle Challenge parking maneuver (Section 8.6, pending) |

**Low-level diagnostics**

| Test | What it verifies |
|:---|:---|
| [`12_output_pin_test.ino`](tests/12_output_pin_test.ino) | Cycles every output pin (buzzer, ToF XSHUT, servo, motor PWM/direction) HIGH→LOW to confirm each is wired and functional, independent of higher-level logic |
| [`i2c_scanner.ino`](tests/i2c_scanner.ino) | Confirms both ToF sensors respond at their expected re-addressed I2C addresses (`0x30`/`0x31`) and the MPU6050 responds at `0x68` — catches wiring/addressing faults before running any control code |

### 10.3 Subsystem Testing

Once individual components passed their standalone tests, they were combined and tested together:

| Test | What it verifies |
|:---|:---|
| [`06_motor_servo_test.ino`](tests/06_motor_servo_test.ino) | Manual keyboard control over serial (F/B/S to drive, L/C/R to steer) — confirms the motor and servo work correctly together before layering autonomous logic on top |
| [`13_full_hardware_test.ino`](tests/13_full_hardware_test.ino) | Single-run diagnostic exercising the servo, motor, buzzer, both ToF sensors, and the MPU6050 in sequence, printing a PASS/FAIL summary for each — used as a quick pre-run health check |
| [`serial_test.ino`](tests/serial_test.ino) / [`serial_test.py`](tests/serial_test.py) | Round-trip test sending fixed messages (`HELLO`, `PING`, `CW`, `CCW`, `START`, `STOP`) from the Pi to the Arduino and measuring reply latency — validates the handshake protocol described in Section 7.6 before relying on it during autonomous runs |
| [`complete_pi_diagnostics.py`](tests/complete_pi_diagnostics.py) | Combined Pi-side script running camera capture, serial communication, and a live FPS counter together — checks the vision pipeline maintains adequate frame rate (flags anything under ~20 FPS) while also talking to the Arduino |

Chassis-level subsystem testing (fit, clearance, mechanical stability across iterations) is covered separately in **Section 5.7**.

> Add specifics here as you generate them — e.g. actual latency numbers from the serial test, or FPS numbers from a Pi diagnostics run.

### 10.4 Problems & Solutions

*(Structure only — fill in with real entries as issues come up. This should capture what actually broke, distinct from Section 9.3's anticipated risks.)*

| Problem | Root Cause | Fix | Date |
|:---|:---|:---|:---|
| | | | |
| | | | |

---

## 11. Reproducing VectorX

### 11.1 Hardware Requirements

Before starting a build, source the following. Full pricing, quantities, and part-level notes are in the BOM (Section 11.2) — this is the condensed "shopping list" version.

**Compute**
- Raspberry Pi 5 (8GB) + official charger + microSD card (32GB+)
- Arduino Uno (ATmega328P) + USB-A to USB-B cable

**Sensing**
- Raspberry Pi Camera 3 Wide
- VL53L0X ToF distance sensor ×3
- MPU-6050 6-axis IMU

**Actuation**
- REV Robotics Smart Robot Servo
- N20 12V 300RPM DC motor with integrated encoder
- DFRobot TB6612FNG motor driver

**Power**
- 11.1V 3S LiPo battery (3700 mAh or larger)
- 5V 5A buck converter
- Power Distribution Board (PDB)

**Mechanical / Structural**
- 3D printer access (or laser cutter, if adapting the chassis design) for the chassis, sensor mounts, and camera tower
- 4× rubber-tyred wheels (56mm diameter)
- Lego differential gear assembly (or equivalent) for the rear axle
- Assorted screws/standoffs/brackets for mounting

**Tools & Misc.**
- Breadboard, jumper wires, soldering equipment
- Development laptop with Arduino IDE 2.x and a Raspberry Pi OS–compatible SD card flasher

For exact wiring, see Section 11.4; for software setup, Section 11.5–11.6.

### 11.2 Bill of Materials (BOM)
## Bill of Materials (BOM)

| Component | Description / Spec | Qty | Unit Cost (₹) | Total Cost (₹) |
|-----------|--------------------|----:|---------------:|----------------:|
| Raspberry Pi 5 | 8GB LPDDR4X RAM | 1 | ₹24,000 | ₹24,000 |
| Raspberry Pi Charger | Charging Cable for Pi 5 | 1 | ₹1,400 | ₹1,400 |
| Raspberry Pi Camera 3 Wide Module | 12MP, 120° wide-angle lens | 1 | ₹4,500 | ₹4,500 |
| Arduino Uno | ATmega328P board | 1 | ₹450 | ₹450 |
| Arduino Uno Cable | USB-A to USB-B cable for programming the Uno | 1 | ₹50 | ₹50 |
| FNG TB6612 Motor Driver | DFRobot, PWM speed control | 1 | ₹350 | ₹350 |
| VL530X ToF Module | Time-of-flight laser distance sensor, I2C, 1m range | 3 | ₹490 | ₹1,470 |
| 5V 5A Buck Converter | DC-DC step-down module | 1 | ₹250 | ₹250 |
| 12V N20 300rpm motor with Encoder | Metal-gear DC motor with integrated quadrature encoder | 1 | ₹450 | ₹450 |
| MPU6050 | 6-axis IMU, I2C interface | 1 | ₹150 | ₹150 |
| Lego Differential Gear | Differential gear assembly for rear-axle power split | 1 | – | ₹0 |
| REV Robotics Smart Robot Servo | High-torque smart servo | 1 | ₹5,000 | ₹5,000 |
| Power Distribution Board | Board for splitting battery power to multiple modules | 1 | ₹250 | ₹250 |
| Breadboard | For splitting pins into multiple points | 1 | ₹100 | ₹100 |
| Chasis Iterations | Estimated material/machining cost per prototype iteration (3D print) | 5 | ₹1,500 | ₹7,500 |
| Final Chasis | Final laser-cut/3D-printed chassis plate with mounts for Pi, Arduino, motors and sensors | 1 | ₹1,500 | ₹1,500 |
| Wheels | Rubber-tyred robot wheels, 56mm diameter | 4 | ₹120 | ₹480 |
| Miscellenaous Cost | Includes testing components, alternatives, wires, etc | 1 | ₹10,000 | ₹10,000 |
| **Total Build Cost** | | | | **₹57,900** |

### 11.3 CAD & Manufacturing Files

> Add links/exports of the chassis CAD (e.g. STEP/STL for the 3D-printed chassis, sensor mounts, camera tower) here, e.g. under a `/cad` folder in the repo.

### 11.4 Wiring Instructions

The full circuit schematic below shows every connection in the build. Power wiring is shown in red (positive) and black (ground); signal wiring is color-coded by bus: blue for I2C and PWM/digital control lines, gold for XSHUT and encoder lines, and gray for the USB link between the Raspberry Pi 5 and Arduino Uno.

> *Figure 11.1: Full wiring schematic — add the exported image here (e.g. `photos/wiring_diagram.png`).*

**Power connections**

| From | To | Wire | Notes |
|:---|:---|:---:|:---|
| Battery (11.1V 3S) | PDB input | Red/Black | Connect positive and negative leads directly to the PDB input terminals. |
| PDB — FULL PWR | 5V 5A buck converter (IN) | Red/Black | Unregulated 11.1V feed. |
| Buck converter (OUT, 5V) | Raspberry Pi 5 (USB-C) | Red/Black | This is the Pi's only power source — do not power it from anywhere else. |
| PDB — FULL PWR | Motor driver VM, GND | Red/Black | Raw 11.1V feeds the TB6612 motor supply pin directly. |
| PDB — 5V header | Steering servo 5V, GND | Red/Black | Regulated 5V for the REV Smart Robot Servo. |
| Arduino 5V, GND | MPU6050 VCC, GND | Red/Black | Logic power shared from the Arduino's own 5V rail. |
| Arduino 5V, GND | VL53L0X ×3 — VCC, GND | Red/Black | All three ToF sensors share this same 5V/GND pair. |

**Signal connections**

| From | To | Wire | Notes |
|:---|:---|:---:|:---|
| Arduino D6 | Motor driver PWMA | Blue | Motor speed (PWM). |
| Arduino D7 | Motor driver AIN1 | Blue | Motor direction. |
| Motor driver M+, M– | N20 drive motor | Red/Black | Motor output terminals. |
| N20 encoder channel A | Arduino D2 | Gold | Interrupt-capable pin. |
| N20 encoder channel B | Arduino D3 | Gold | Interrupt-capable pin. |
| Arduino D9 | Steering servo signal | Blue | PWM steering command. |
| Arduino D10 / D11 / D12 | ToF #1 / #2 / #3 XSHUT | Gold | One dedicated pin per sensor — used to re-address each sensor at boot. |
| Arduino A4 (SDA) | MPU6050 SDA + all 3 ToF SDA | Blue | Shared I2C data line. |
| Arduino A5 (SCL) | MPU6050 SCL + all 3 ToF SCL | Blue | Shared I2C clock line. |
| Raspberry Pi 5 USB | Arduino USB | Gray | Carries both 5V logic power to the Arduino and the serial command link. |
| Raspberry Pi 5 CSI port | Pi Camera 3 Wide | Ribbon cable | Seat the ribbon with contacts facing the board's HDMI ports. |

> *Before first power-on, verify every ground connection is common across the battery, PDB, both controllers, and all sensors — a floating ground on any single component is the most common cause of erratic sensor readings.*

### 11.5 Software Requirements

**Raspberry Pi 5**
- Raspberry Pi OS (64-bit), Bookworm or later
- Python 3.11 or later
- `picamera2` (camera capture)
- `opencv-python` (block detection / vision processing)
- `numpy`
- `pyserial` (serial link to the Arduino)

**Arduino Uno**
- Arduino IDE 2.x (or `arduino-cli`)
- Arduino AVR Boards package
- `Wire.h` — built in, for I2C
- `Servo.h` — built in, or the REV Robotics servo library if using their smart-servo protocol
- `Adafruit_VL53L0X` (or Pololu VL53L0X library) — for the ToF sensors
- `Adafruit_MPU6050` + `Adafruit_Sensor` — for the IMU

### 11.6 Installation

**Raspberry Pi 5 setup**
1. Flash Raspberry Pi OS (64-bit) to the SD card using Raspberry Pi Imager.
2. Boot the Pi, then open a terminal and update the system:
   ```bash
   sudo apt update && sudo apt full-upgrade -y
   ```
3. Enable the camera interface:
   ```
   sudo raspi-config → Interface Options → Camera → Enable
   ```
4. Install the required packages:
   ```bash
   sudo apt install -y python3-opencv python3-picamera2
   pip install pyserial numpy --break-system-packages
   ```
5. Copy the project files onto the Pi (via `git clone` or `scp`), e.g. into `~/vectorx/`.

**Arduino IDE setup**
6. Install Arduino IDE 2.x on a development laptop.
7. Open Tools → Board → Boards Manager, install "Arduino AVR Boards" if not already present.
8. Open Tools → Manage Libraries, and install: Adafruit VL53L0X, Adafruit MPU6050, Adafruit Unified Sensor.
9. Open the project's `.ino` sketch file.

### 11.7 Building / Compiling

**Arduino sketch**
- With the sketch open, click Verify (checkmark icon) to compile and catch errors before uploading.
- Confirm Tools → Board is set to "Arduino Uno".

**Raspberry Pi script**
- Python is interpreted, so no build step is required.
- As a quick syntax check before running on competition day:
  ```bash
  python3 -m py_compile vision_avoidance.py
  ```

### 11.8 Uploading to Controllers

**Arduino Uno**
1. Connect the Arduino to the development laptop via USB.
2. Select the correct port under Tools → Port.
3. Click Upload. The sketch is stored in the Arduino's flash memory and will run automatically every time it is powered on — no laptop connection is needed afterward.

**Raspberry Pi 5**
- There is no "upload" step — code runs directly from the Pi's storage.
- Push updates over SSH or `git pull`, e.g.:
  ```bash
  scp vision_avoidance.py pi@vectorx.local:~/vectorx/
  ```

### 11.9 Configuration

Key tunable constants are grouped near the top of each file so they can be adjusted without touching the control logic.

| Constant | Location | Purpose |
|:---|:---|:---|
| `SERIAL_PORT`, `BAUD_RATE` | `vision_avoidance.py` | Serial link to the Arduino (matches the port Arduino enumerates as, typically `/dev/ttyACM0` or `/dev/ttyUSB0`). |
| Camera resolution / frame rate | `vision_avoidance.py` | Picamera2 capture configuration. |
| `HSV_MIN` / `HSV_MAX` per color | `vision_avoidance.py` | Block/line color-detection thresholds — lighting-dependent, re-tune on site. |
| `TOF_TRIGGER_MM` | Arduino sketch | Distance threshold that triggers the avoidance state machine. |
| `PWM_MIN`, `PWM_MAX` | Arduino sketch | Motor speed floor/ceiling to avoid stall or overspeed. |
| `SERVO_CENTER` (`STRAIGHT`), `SERVO_MIN` (`MAX_RIGHT`), `SERVO_MAX` (`MAX_LEFT`) | Arduino sketch | Steering angle limits for Ackermann geometry. |
| `ENCODER_TICKS_PER_REV` | Arduino sketch | Used to convert encoder pulses into distance traveled. |

### 11.10 Calibration

**Steering servo center**
1. Command the servo to its defined center (`STRAIGHT`) with all wheels off the ground.
2. Adjust the steering linkage until the front wheels point straight ahead.
3. Record any offset needed in `STRAIGHT` so the code's center value corresponds to straight-ahead in hardware.

**ToF sensors**
1. Place a flat target at a known distance (e.g. 200mm) in front of each sensor.
2. Read back the raw sensor value over serial and compare to the known distance.
3. After the XSHUT re-addressing sequence runs at boot, confirm each sensor reports independently and consistently — a stuck or duplicate reading usually means two sensors were re-addressed to the same I2C address.

**Camera color thresholds**
1. Under the actual competition lighting (not a workshop), capture a frame for each color being detected (direction line, pillars, parking markers).
2. Use an HSV color-picker tool on the captured frame to read off the hue/saturation/value range for each color.
3. Update the HSV thresholds in `vision_avoidance.py` and re-test detection reliability at several distances.

**Encoder distance**
1. Mark a known distance on the floor (e.g. 1 meter).
2. Drive the robot that distance and log the raw encoder tick count.
3. Compute `ENCODER_TICKS_PER_REV` / ticks-per-cm from the result and update the constant.

**Motor deadzone**
1. Starting from 0, increase the PWM value sent to the motor driver until the drive motor just begins to turn.
2. Set `PWM_MIN` (or `DRIVE_SPEED` floor) to that value so the state machine never commands a PWM too low to move the robot.

### 11.11 Running VectorX

**Power-on sequence**
1. Double-check all wiring against Section 11.4 before connecting the battery.
2. Connect the battery to the PDB last. The Raspberry Pi 5 will boot automatically; the Arduino powers on automatically once the Pi enumerates its USB port.
3. Wait for the Pi to fully boot (30–45 seconds) before starting the program.

**Starting the program**
- Connect over SSH, or use an attached keyboard/monitor, and navigate to the project directory:
  ```bash
  cd ~/vectorx
  python3 vision_avoidance.py
  ```
- For a competition-ready, no-laptop-needed start, configure the script to run as a systemd service that launches on boot, and use a physical push-button or the Pi's GPIO to arm/start the run.

**What to expect**
- Console output should confirm the camera initialized, the serial connection to the Arduino opened, and the direction-detection routine ran before the Arduino's `START_CW`/`START_CCW` handshake is sent.
- The Arduino will hold the servo at center and the motor at stop until it starts receiving valid commands from the Pi.

**Stopping**
- Press `Ctrl+C` to interrupt the Python script — it sends a `STOP` command so the Arduino returns the motor to stop and the servo to center.
- Disconnect the battery from the PDB when the run is complete.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
