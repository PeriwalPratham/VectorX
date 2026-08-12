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
### 3.3 Multi-View Photographs
### 3.4 Demonstration Videos
* **Open Challenge Demonstration Video:** [YouTube Link]
* **Obstacle Challenge Demonstration Video:** [YouTube Link]

---

## 4. System Architecture
## 4. System Architecture

<img width="1466" height="855" alt="Screenshot From 2026-08-12 16-22-14" src="https://github.com/user-attachments/assets/6624b7ee-afe4-4e1e-bee9-a3e80e4f38fd" />


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

Each iteration was tested for fit, component clearance, and mechanical stability before moving to the next version, helping us catch design flaws early rather than during final assembly.
---

## 6. Power & Sensor Architecture
### 6.1 Power System & Isolation

We use a split power architecture to prevent motor current draw from affecting the Raspberry Pi.

Our ~12V LiPo battery feeds into a Power Distribution Board (PDB), which splits power into two paths. One path goes directly to the Arduino Uno and the drive motor, since the Arduino's onboard regulator can handle 12V on its Vin pin, and the motor needs the higher voltage for full torque and speed. The other path goes through a 5V buck converter, which steps voltage down and boosts available current specifically for the power hungry Raspberry Pi 5 and camera module.

All other components (steering servo, ToF sensors, MPU6050) are powered off the Arduino's own 5V output rather than pulling directly from the battery or buck converter, since their current draw is low enough for the Arduino to supply safely.

This isolation matters because fast current spikes from the motor can cause voltage sag on a shared rail, which is enough to brown out and crash the Raspberry Pi mid run. Keeping the Pi and camera on their own dedicated buck converter avoids this failure mode entirely.

All grounds (battery negative, PDB, buck converter, Arduino, Raspberry Pi, motor driver, servo, and sensors) are tied to a single common ground, which is required for the I2C bus and PWM signals to work correctly across boards.

### 6.2 Power Distribution

Power originates from a single ~12V LiPo battery and is split at the Power Distribution Board into two paths:

| Path | Voltage | Feeds |
|:---|:---|:---|
| Direct battery path | ~12V | Arduino Uno (via Vin), drive motor |
| Buck converter path | 5V (boosted current) | Raspberry Pi 5, camera module |

From there, the Arduino's own 5V rail powers everything else, the steering servo, ToF sensors, and MPU6050, since these draw comparatively little current.

### 6.3 Power Budget Table

| Component | Voltage | Powered Via | Typical Current | Notes |
|:---|:---|:---|:---|:---|
| Raspberry Pi 5 | 5V | Buck converter (direct from PDB) | up to 3A (peak) | needs boosted current, dedicated rail |
| Pi Camera 3 | 5V | Buck converter (via Pi) | included in Pi draw | CSI connection |
| Arduino Uno | ~12V in, 5V regulated onboard | Direct from PDB (Vin) | ~50mA | low draw |
| N20 motor | ~12V (direct) | Direct from PDB, via motor driver | varies with load | highest draw overall, spikes on acceleration |
| REV Smart Servo | 5V | Arduino 5V rail | varies with load | draws more under steering resistance |
| VL53L0X ToF x3 | 5V | Arduino 5V rail | ~20mA each | I2C |
| MPU6050 | 5V | Arduino 5V rail | ~4mA | I2C |

[Fill in your buck converter's rated headroom and confirm it comfortably covers the Pi 5's peak draw, this is the kind of check judges like to see.]

### 6.4 Battery & Regulation

We use a ~12V LiPo battery as our primary power source, split at the Power Distribution Board before reaching any downstream components. [Confirm exact chemistry and capacity, e.g. 3S LiPo, XXXXmAh.]

We chose this voltage because it comfortably powers the N20 motor directly and feeds the Arduino's Vin pin without needing a separate regulator for the control board. The Raspberry Pi 5, being far more power hungry and voltage sensitive, gets its own dedicated 5V buck converter instead of sharing a rail with the motor, which keeps it isolated from the voltage sag caused by motor current spikes.

<img width="1101" height="786" alt="Screenshot From 2026-08-12 16-22-39" src="https://github.com/user-attachments/assets/4a387e55-7704-426b-a36f-9661cfd1ecd8" />


---

## 7. Software Architecture

## 7. Software Architecture

### 7.1 Software Overview

Our software follows a Sense → Decide → Act pipeline. The Raspberry Pi 5 runs our full computer vision pipeline, converting camera frames into a small set of single-character decisions. The Arduino Uno receives those decisions over serial, combines them with its own real-time sensor readings from the ToF sensors and gyro, and drives the servo and motor accordingly.

We built the Pi-side vision system in nine incremental stages, starting with HSV colour tuning and working up through colour detection, track direction, line detection, distance estimation, obstacle detection, avoidance logic, and finally serial integration. We tested each stage standalone before merging it into the final script.

### 7.2 Software Structure

We kept both codebases single-file, prioritizing reliability and ease of debugging:

- **Raspberry Pi 5 (Python):** one script that runs a continuous camera loop, applies HSV masking for each tracked colour, decides on a track direction or obstacle dodge, and writes single-byte commands to the Arduino over serial.
- **Arduino Uno (C++):** one sketch that reads incoming serial commands from the Pi, polls the ToF sensors and MPU6050, and drives the motor and servo through PID-based control loops.

### 7.3 Code Modules

We organized our Pi-side script functionally around these responsibilities, even though it lives in a single file:

| Module | Responsibility |
|:---|:---|
| HSV masking | Converts each frame to HSV and generates binary masks for orange, blue, red, and green |
| Track direction detection | Compares orange vs blue marker position to decide if the track's inner side is left or right |
| Obstacle detection | Finds red/green contours above an area threshold and estimates distance using the pinhole camera formula |
| Dodge decision | Picks the closest qualifying obstacle and selects a dodge direction (`R` for red, `L` for green) |
| Serial output | Sends single-byte commands to the Arduino, gated by a distance threshold and cooldown timer |

### 7.4 Control Flow & State Machine

Our Pi-side script runs a simple two-phase state machine, controlled by a single flag, `track_direction_set`:

```text
        ┌────────────────────────┐
        │   Phase 1: Direction   │
        │  Detect orange & blue  │
        │  → decide L or R track │
        └───────────┬─────────────┘
                     │ direction found
                     ▼
        ┌────────────────────────┐
        │  Phase 2: Obstacle     │
        │  Detect red/green      │
        │  → estimate distance   │
        │  → dodge if close      │
        │  → cooldown 2s         │
        └────────────────────────┘
```

Once `track_direction_set` becomes `True`, we permanently switch from direction detection into the obstacle-dodging loop for the rest of the run.

[We'll add our Arduino-side state machine here once we finalize the current `.ino` file, our old prototype sketch used a different driver and sensor count so it's not accurate anymore.]

### 7.5 Control Architecture

On the Pi side, our obstacle avoidance is decision-based rather than a continuous feedback loop. Each frame independently evaluates the closest obstacle's estimated distance and triggers a dodge command only if it crosses `DODGE_THRESHOLD_CM`, with a cooldown to prevent repeated commands mid-maneuver.

On the Arduino side, we run PID control loops for motor speed and steering correction, using sensor fusion between the MPU6050 gyro and ToF distance readings to hold heading and maintain wall standoff distance. [We'll fill in our exact gains and loop structure once the current Arduino code is finalized.]

### 7.6 Communication Protocols

We connect the Pi and Arduino over USB serial at **115200 baud**, using single-byte ASCII commands rather than structured messages like JSON, keeping parsing on the Arduino side simple:

| Byte | Meaning |
|:---|:---|
| `]` | Track direction is RIGHT (orange closer) |
| `[` | Track direction is LEFT (blue closer) |
| `R` | Dodge right (red obstacle detected) |
| `L` | Dodge left (green obstacle detected) |

Between the Arduino and our sensors, we run a shared I2C bus (SDA/SCL) across all three ToF sensors and the MPU6050, using XSHUT pins at startup to assign each ToF a unique I2C address.

Between the Arduino and our actuators, we send PWM signals to the TB6612FNG motor driver (speed + direction) and the REV Smart Servo (steering angle).

### 7.7 Dependencies & Software Stack

**Raspberry Pi 5 (Python):**

| Library | Purpose |
|:---|:---|
| `OpenCV` (cv2) | Camera capture, HSV conversion, contour detection |
| `NumPy` | HSV array definitions, numerical operations |
| `PySerial` | Serial communication with the Arduino |
| `time` | Cooldown timing between dodge commands |

**Arduino Uno (C++):**

| Library | Purpose |
|:---|:---|
| `Wire.h` | I2C communication with ToF sensors and MPU6050 |
| `Servo.h` | Steering servo control |
| VL53L0X library | ToF sensor initialization and distance reads |

---

## 8. Autonomous Navigation & Obstacle Strategy

## 8. Autonomous Navigation & Obstacle Strategy

### 8.1 Navigation Overview

We navigate using our Sense → Decide → Act loop. The Raspberry Pi handles all vision based decisions (track direction, obstacle colour, parking marker detection), while the Arduino handles real time physical control (steering angle, motor speed, wall standoff distance) using its own ToF and gyro readings. We treat these as two separate layers, the Pi tells the car what to do at a high level, and the Arduino figures out how to physically execute it safely.

### 8.2 Direction & Sign Detection

At the start of each run, we detect the orange and blue track markers to figure out which direction we're driving. We compare the vertical position of each marker's bounding box in the camera frame, whichever one sits lower (closer to the camera) tells us the inner side of the track:

- Orange closer → inner track is RIGHT
- Blue closer → inner track is LEFT

Once we lock in a direction, we send a single byte (`]` for right, `[` for left) to the Arduino and don't re-check it for the rest of the run, since the track direction doesn't change mid race.

### 8.3 Lane / Wall Following

We handle lane and wall following in two ways depending on what's available:

- **Camera side:** we built a black line detector that converts each frame to HSV, masks out dark pixels, and splits the frame into left, centre, and right sections to count black pixels in each. This tells us roughly where the track line sits in our field of view.
- **Arduino side:** we use the ToF sensors to hold a consistent standoff distance from the wall using a PD control loop, adjusting steering angle proportionally to how far off we are from our target distance, with a derivative term to dampen oscillation.

### 8.4 Obstacle Detection

We detect red and green obstacles using HSV colour masking, similar to our track marker detection. Since red wraps around the HSV hue circle, we combine two separate red ranges (`0-10` and `170-180`) into one mask.

Once we find a valid contour (area above `500` pixels), we estimate its distance using the pinhole camera formula:

```text
Distance = (Real Object Width × Focal Length) / Object Width in Pixels
```

We calibrated our focal length separately for red and green objects to keep the estimate accurate.

### 8.5 Obstacle Management Strategy

Each frame, we track whichever obstacle is currently closest rather than reacting to every obstacle we see:

| Colour | Dodge Direction | Command |
|:---|:---|:---|
| Red | Right | `R` |
| Green | Left | `L` |

We only trigger a dodge once the closest obstacle's estimated distance drops below our `DODGE_THRESHOLD_CM` value, and we enforce a 2 second cooldown between dodge commands so we don't spam the Arduino with repeated instructions while we're already mid maneuver.

### 8.6 Parallel Parking Strategy

[We'll fill this in with our actual parking approach, e.g. how we detect the magenta parking plates, what distance/angle triggers the parking maneuver, and whether we reverse in or pull in forward.]

### 8.7 Control Algorithm

On the Arduino, we use PD (proportional-derivative) control for wall following. We calculate an error term as the difference between our current ToF reading and our target standoff distance, then combine a proportional correction with a derivative term based on how fast that error is changing, and use the result to adjust our servo's steering angle within its mechanical range.

For cornering, we use gyro-based heading tracking rather than relying purely on distance thresholds, since this lets us confirm we've actually completed a turn (roughly matching our expected turn angle) before switching back to wall following.

### 8.8 Edge Cases & Safeguards

- **ToF timeout/out of range:** if a ToF sensor times out or returns an unrealistic reading, we treat it as invalid rather than acting on bad data.
- **Obstacle cooldown:** our 2 second cooldown between dodge commands stops the Arduino from receiving conflicting instructions mid maneuver.
- **Lighting sensitivity:** our HSV thresholds were tuned interactively using our HSV tuner rather than guessed, to reduce false positives/negatives under competition lighting.
- **Distance threshold gating:** we only react to obstacles within `DODGE_THRESHOLD_CM`, ignoring anything further away so we don't dodge prematurely.

*(See Section 8.9 below for the full computer vision code and stage by stage breakdown.)*
# Computer Vision Development

Our computer vision system was developed in multiple stages.

The programs were tested individually before being combined into the final autonomous vision system.

The development process included:

1. HSV colour calibration
2. Basic colour detection
3. Orange and blue track-marker detection
4. Track-direction detection
5. Black line detection
6. Distance estimation
7. Red and green obstacle detection
8. Autonomous obstacle avoidance
9. Raspberry Pi–Arduino communication

---

# 1. HSV Colour Tuner

## Objective

Before detecting colours reliably, the HSV ranges needed to be calibrated for our camera and lighting conditions.

Instead of manually guessing the HSV values, we created an interactive **HSV Tuner**.

The tuner allows us to select a colour and adjust:

- Lower Hue
- Lower Saturation
- Lower Value
- Upper Hue
- Upper Saturation
- Upper Value

The program displays the original camera feed, the binary mask, and the filtered result simultaneously.

## Explanation

### HSV Presets

The program stores starting HSV values for five colours:

| Index | Colour |
|---:|---|
| 0 | Red |
| 1 | Green |
| 2 | Pink |
| 3 | Orange |
| 4 | Blue |

These values are stored inside the `colour_presets` dictionary.

The values can then be adjusted using the sliders.

---

### Interactive Trackbars

The program creates six trackbars:

- `Lower H`
- `Lower S`
- `Lower V`
- `Upper H`
- `Upper S`
- `Upper V`

These sliders allow the HSV range to be changed while the camera is running.

This is useful because lighting conditions can change the appearance of colours.

---

### Colour Mask

The camera image is converted to HSV:

```python
hsv_frame = cv2.cvtColor(
    frame,
    cv2.COLOR_BGR2HSV
)
```

The selected HSV range is then converted into a binary mask:

```python
mask = cv2.inRange(
    hsv_frame,
    lower_bound,
    upper_bound
)
```

Pixels inside the selected range become white, while pixels outside the range become black.

---

### Filtered Result

The mask is applied to the original frame:

```python
masked_result = cv2.bitwise_and(
    frame,
    frame,
    mask=mask
)
```

This allows us to see exactly which parts of the image are being detected.

### Development Benefit

The HSV tuner was used to experimentally determine colour ranges rather than relying only on theoretical HSV values.

This helped create more reliable colour detection for the actual camera and competition environment.

---

# 2. Black Line Detection

## Objective

The next stage was to detect the **black track/line** using the camera.

The image is converted to HSV and a mask is created for dark pixels.

The camera image is also divided into three vertical sections:

- Left
- Centre
- Right

The number of black pixels in each section is counted.

This provides information about where the black line is located in the camera's field of view.

## Explanation

### Black Mask

The program creates an HSV range for dark pixels:

```python
lower_black = np.array([0, 0, 0])
upper_black = np.array([155, 255, 140])
```

The mask is created using:

```python
black_mask = cv2.inRange(
    hsv,
    lower_black,
    upper_black
)
```

The resulting image contains the detected black regions.

---

### Contour Detection

Contours are detected from the black mask:

```python
black_contours, _ = cv2.findContours(...)
```

Contours with an area greater than `500` pixels are considered significant.

A bounding rectangle is then drawn around each detected region.

---

### Dividing the Camera Image

The camera image is divided into three equal vertical sections:

```text
┌────────────┬────────────┬────────────┐
│            │            │            │
│    LEFT    │   CENTRE   │    RIGHT   │
│            │            │            │
└────────────┴────────────┴────────────┘
```

The width of each section is calculated using:

```python
section_width = width // 3
```

Two vertical lines are drawn to show the boundaries.

---

### Counting Black Pixels

The program extracts each section from the black mask.

For example, the left section is:

```python
left_mask = black_mask[
    :,
    :section_width
]
```

The number of white pixels in that mask is then counted:

```python
left_pixels = cv2.countNonZero(
    left_mask
)
```

The same process is repeated for the centre and right sections.

The result tells us how much black area is present in each section.

---

## Decision Concept

The pixel counts can later be used for steering.

For example:

| Highest black pixel count | Possible interpretation |
|---|---|
| Left | Line is predominantly on the left |
| Centre | Line is predominantly centred |
| Right | Line is predominantly on the right |

This program currently **measures and prints the values**. It does not itself make a steering decision.

---

# 3. Orange and Blue Track Marker Detection

## Objective

Orange and blue markers were detected to determine the direction of the track.


## Explanation

The camera image is converted into HSV.

Two masks are created:

- Orange
- Blue

Contours are then found within each mask.

A contour is accepted when its area is greater than `500` pixels.

The bounding rectangle provides the position and dimensions of the detected marker.

The marker's position is printed and displayed on the camera feed.

---

# 4. Orange and Blue Track Direction

## Objective

The positions of the orange and blue markers are compared to determine which side of the track is the inner side.

## Explanation

The system uses the pinhole-camera approximation:

```text
Distance = (Real Object Width × Focal Length)
           ------------------------------------
                 Object Width in Pixels
```

The variables represent:

| Variable | Meaning |
|---|---|
| `REAL_WIDTH` | Known real-world width of the detected object |
| `FOCAL_LENGTH` | Calibrated camera focal length |
| `w` | Width of the detected object in pixels |
| `distance` | Estimated distance from the camera |

As the obstacle gets closer, its width in the image increases.

Therefore, the calculated distance decreases.

The focal length was calibrated for the camera setup before being used in the obstacle-detection system.

---

# 5. Complete Obstacle Detection and Avoidance

## Objective

The final system combines the colour detection and distance estimation systems.

The Raspberry Pi:

1. Detects the track direction.
2. Detects red and green obstacles.
3. Estimates their distance.
4. Determines which obstacle is closest.
5. Selects the required dodge direction.
6. Sends the command to the Arduino.


## Explanation

### Track Direction

The first phase detects the orange and blue markers.

The relative Y-position of the markers determines which side is the inner side of the track.

The result is sent to the Arduino.

---

### Obstacle Detection

Once the track direction has been established, the program switches to obstacle detection.

The robot detects:

- 🔴 **Red obstacles**
- 🟢 **Green obstacles**

The system estimates the distance to each obstacle.

---

### Closest Obstacle

The program starts with:

```python
closest_distance = 999.0
```

Whenever a detected obstacle is closer than the current closest obstacle, it becomes the new target.

This means that if multiple obstacles are visible, the robot prioritises the closest one.

---

### Dodge Direction

The colour of the obstacle determines the dodge command.

| Colour | Dodge Direction | Command |
|---|---|---|
| Red | Right | `R` |
| Green | Left | `L` |

---

### Dodge Threshold

The robot only performs an avoidance manoeuvre when:

```python
closest_distance < 40.0
```

This prevents it from reacting to obstacles that are too far away.

---

### Cooldown

A two-second cooldown is used between dodge commands.

This prevents repeated commands from being sent continuously while the robot is already performing an avoidance manoeuvre.

---

# 7. Overall Computer Vision Pipeline

```text
┌─────────────────────┐
│ Raspberry Pi Camera │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Convert BGR → HSV   │
└──────────┬──────────┘
           ↓
┌──────────────────────────────┐
│       Colour Detection       │
│                              │
│ Orange │ Blue │ Red │ Green  │
└──────────┬───────────────────┘
           ↓
      ┌────┴─────┐
      ↓          ↓
 Track Direction  Obstacles
      ↓          ↓
 Orange/Blue    Red/Green
      ↓          ↓
 Direction     Distance
      └────┬─────┘
           ↓
┌─────────────────────┐
│   Decision Making   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Serial Communication│
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       Arduino       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Robot Movement      │
└─────────────────────┘
```

# 8. Development Progression

| Stage | System Developed | Purpose |
|---:|---|---|
| 1 | HSV Tuner | Calibrate colour ranges |
| 2 | Basic Colour Detection | Detect coloured objects |
| 3 | Orange/Blue Detection | Detect track markers |
| 4 | Track Direction | Determine inner track direction |
| 5 | Black Line Detection | Determine line position in camera |
| 6 | Distance Estimation | Estimate obstacle distance |
| 7 | Red/Green Detection | Identify obstacles |
| 8 | Obstacle Avoidance | Select dodge direction |
| 9 | Serial Communication | Send decisions to Arduino |

# 9. Hardware and Software

## Hardware

- Raspberry Pi
- Raspberry Pi Camera
- Arduino
- Motor Driver
- Motors
- Robot Chassis

## Software

- Python
- OpenCV
- NumPy
- PySerial

## Python Libraries

```python
import cv2
import numpy as np
import serial
import time
```

| Library | Purpose |
|---|---|
| `OpenCV` | Camera capture, colour detection and image processing |
| `NumPy` | HSV arrays and numerical calculations |
| `PySerial` | Raspberry Pi–Arduino communication |
| `time` | Timing and cooldown control |

# 10. Summary

The computer vision system was developed progressively rather than creating the complete autonomous program immediately.

The **HSV tuner** was first used to calibrate the colour ranges for the camera.

The calibrated ranges were then used to detect the **orange and blue track markers**, **red and green obstacles**, and the **black track line**.

Distance estimation was added to determine how close an obstacle was to the robot.

Finally, the individual systems were combined with **serial communication** so that the Raspberry Pi could make decisions and send commands to the Arduino.

The overall system follows:

> **Camera → HSV Processing → Colour Detection → Position/Distance → Decision → Serial Communication → Arduino → Robot Movement**


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
