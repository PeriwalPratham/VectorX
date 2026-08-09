# VectorX
## WRO Future Engineers 2026

<div align="center">

<img width="501" height="570" alt="VectorX Logo" src="https://github.com/user-attachments/assets/b47728f1-0384-4bb1-a760-15034163b67b" />

<br />

[![Website](https://img.shields.io/badge/Website-Vector%20X-green?style=for-the-badge&logo=googlechrome&logoColor=white)](https://your-website-url.com)
[![YouTube](https://img.shields.io/badge/YouTube-Vector%20X-red?style=for-the-badge&logo=youtube&logoColor=white)](https://your-youtube-channel-url.com)

</div>

---

## 🧭 So, what can you find here?

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
### 1.2 The Challenge
### 1.3 Our Approach
### 1.4 System Overview
---

## 2. The Team

![Team Photo](photos/team_photo.jpg)

### 2.1 Team Members & Coach
* **Team Name:** Vector X
* **Country:** India
* **Members:** Pratham Periwal, Inaaya Sood, Swasti Kedia
* **Coach:** Chirag Sir
* **Category:** WRO Future Engineers 2026 (Self-Driving Cars Challenge)

### 2.2 Team Photo
### 2.3 Member Roles & Contributions
* **Pratham Periwal:** Lead Software & Computer Vision Engineer
* **Inaaya Sood:** Mechanical Systems & CAD Designer
* **Swasti Kedia:** Electronics & Sensor Integration Engineer

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

```python
import argparse
import sys
import time
from dataclasses import dataclass

import cv2
import numpy as np
import serial

try:
    from picamera2 import Picamera2
    PICAMERA2_AVAILABLE = True
except Exception:
    Picamera2 = None
    PICAMERA2_AVAILABLE = False


@dataclass
class ColorDetection:
    found: bool
    contour: np.ndarray | None = None
    y: int = -1
    x: int = -1
    area: float = 0.0


ORANGE_LOWER = (5, 100, 80)
ORANGE_UPPER = (28, 255, 255)

BLUE_LOWER = (95, 100, 70)
BLUE_UPPER = (130, 255, 255)

MIN_CONTOUR_AREA = 350
STABLE_FRAMES_REQUIRED = 15
SEND_REPEAT_DELAY_SEC = 0.3

PRE_CONNECT_DETECT_TIMEOUT_SEC = 6.0

ARDUINO_READY_TIMEOUT_SEC = 15.0
ACK_WAIT_TIMEOUT_SEC = 1.0
ACK_RETRY_INTERVAL_SEC = 0.3
ACK_MAX_ATTEMPTS = 20


def make_camera(camera_index: int):
    if PICAMERA2_AVAILABLE:
        picam = Picamera2()
        cfg = picam.create_preview_configuration(
            main={"size": (640, 480), "format": "BGR888"}
        )
        picam.configure(cfg)
        picam.start()
        time.sleep(2)
        return ("picamera2", picam)

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera {camera_index}")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    return ("opencv", cap)


def read_frame(camera_kind, cam):
    if camera_kind == "picamera2":
        return cam.capture_array()

    ok, frame = cam.read()
    if not ok:
        return None

    return frame


def preprocess_mask(hsv, lower, upper):
    mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def fit_overlay_line(contour, frame_shape):
    if contour is None or len(contour) < 2:
        return None

    h, w = frame_shape[:2]
    vx, vy, x, y = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
    vx, vy, x, y = float(vx), float(vy), float(x), float(y)

    if abs(vx) < 1e-6:
        vx = 1e-6

    left_y = int((-x * vy / vx) + y)
    right_y = int(((w - x) * vy / vx) + y)

    return ((0, left_y), (w - 1, right_y))


def detect_color(mask, min_area=MIN_CONTOUR_AREA):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return ColorDetection(False)

    best = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(best)

    if area < min_area:
        return ColorDetection(False)

    m = cv2.moments(best)
    if m["m00"] == 0:
        return ColorDetection(False)

    cx = int(m["m10"] / m["m00"])
    cy = int(m["m01"] / m["m00"])

    return ColorDetection(True, best, cy, cx, area)


def send_line(ser, text):
    ser.write((text + "\n").encode())
    ser.flush()


def detect_direction(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    orange = detect_color(preprocess_mask(hsv, ORANGE_LOWER, ORANGE_UPPER))
    blue = detect_color(preprocess_mask(hsv, BLUE_LOWER, BLUE_UPPER))
    debug = frame.copy()

    if orange.found:
        l = fit_overlay_line(orange.contour, frame.shape)
        if l:
            cv2.line(debug, l[0], l[1], (0, 140, 255), 4)
    if blue.found:
        l = fit_overlay_line(blue.contour, frame.shape)
        if l:
            cv2.line(debug, l[0], l[1], (255, 0, 0), 4)

    direction = None
    if orange.found and blue.found:
        direction = "CW" if orange.y < blue.y else "CCW"
        cv2.putText(debug, direction, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    if orange.found or blue.found:
        print(f"[detect] orange.found={orange.found} y={orange.y}  "
              f"blue.found={blue.found} y={blue.y}  -> direction={direction}")

    return direction, debug


def read_arduino_line(ser):
    try:
        if ser.in_waiting == 0:
            return None
        raw = ser.readline()
    except serial.SerialException:
        return None
    if not raw:
        return None
    line = raw.decode(errors="ignore").strip()
    if line:
        print(f"[arduino] {line}")
    return line


def drain_arduino_lines(ser):
    while True:
        if read_arduino_line(ser) is None:
            break


def wait_for_arduino_ready(ser, timeout_sec=ARDUINO_READY_TIMEOUT_SEC):
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        try:
            raw = ser.readline()
        except serial.SerialException:
            return False
        line = raw.decode(errors="ignore").strip()
        if line:
            print(f"[arduino] {line}")
            if line == "READY":
                return True
    return False


def send_command_with_ack(ser, command,
                          ack_timeout=ACK_WAIT_TIMEOUT_SEC,
                          retry_interval=ACK_RETRY_INTERVAL_SEC,
                          max_attempts=ACK_MAX_ATTEMPTS):
    for attempt in range(1, max_attempts + 1):
        send_line(ser, command)
        deadline = time.time() + ack_timeout
        while time.time() < deadline:
            line = read_arduino_line(ser)
            if line is None:
                continue
            if line == "ACK":
                return True
            if line.startswith("ERR="):
                return False
        time.sleep(max(0.0, retry_interval))
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default="/dev/ttyUSB0")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--camera", type=int, default=0)
    args = parser.parse_args()

    print("Opening camera and detecting direction (Arduino not connected yet)...")
    camera_kind, cam = make_camera(args.camera)

    stable_count = 0
    last_direction = None
    confirmed_direction = None

    detect_start = time.time()
    while confirmed_direction is None:
        frame = read_frame(camera_kind, cam)
        if frame is None:
            continue

        direction, debug = detect_direction(frame)

        if direction is not None:
            if direction == last_direction:
                stable_count += 1
            else:
                stable_count = 1
                last_direction = direction

            if stable_count >= STABLE_FRAMES_REQUIRED:
                confirmed_direction = direction
                print(f"Confirmed direction: {confirmed_direction}")
        else:
            stable_count = 0
            last_direction = None

        cv2.imshow("WRO Direction Detection", debug)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        if time.time() - detect_start > PRE_CONNECT_DETECT_TIMEOUT_SEC:
            print("WARNING: could not confirm direction before timeout. "
                  "Proceeding without one - Arduino will use its default.")
            break

    print("Opening serial (this resets the Arduino)...")

    ser = serial.Serial(args.port, args.baud, timeout=0.5)
    print("Serial opened:", ser.port)

    ser.reset_input_buffer()

    print("Waiting for Arduino READY (setup + gyro calibration + ToF init)...")
    arduino_ready = wait_for_arduino_ready(ser)
    if arduino_ready:
        print("Arduino is READY.")
    else:
        print("WARNING: never saw READY from Arduino before timeout. "
              "Proceeding anyway - the command below will still retry for ACK.")

    direction_sent = False

    if confirmed_direction is not None:
        direction_sent = send_command_with_ack(ser, confirmed_direction)
        if direction_sent:
            print(f"Direction {confirmed_direction} ACKed by Arduino.")
        else:
            print(f"WARNING: Arduino never ACKed {confirmed_direction}. "
                  "It will keep being retried from the main loop below.")
    else:
        print("No confirmed direction yet - it will be sent from the main loop below "
              "as soon as the camera confirms one.")

    print("Finished startup handshake.")

    while True:
        drain_arduino_lines(ser)

        frame = read_frame(camera_kind, cam)
        if frame is None:
            continue

        direction, debug = detect_direction(frame)

        if direction is not None:
            if direction == last_direction:
                stable_count += 1
            else:
                stable_count = 1
                last_direction = direction
                direction_sent = False

            if stable_count >= STABLE_FRAMES_REQUIRED and not direction_sent:
                direction_sent = send_command_with_ack(ser, direction)
        else:
            stable_count = 0
            last_direction = None
            direction_sent = False

        cv2.imshow("WRO Direction Detection", debug)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        elif key == ord("p"):
            send_command_with_ack(ser, "PARK")
        elif key == ord("s"):
            send_command_with_ack(ser, "STOP")
        elif key == ord("r"):
            if last_direction is not None:
                send_command_with_ack(ser, last_direction)

    try:
        send_command_with_ack(ser, "STOP", max_attempts=3)
    except Exception:
        pass

    if camera_kind == "picamera2":
        try:
            cam.stop()
        except Exception:
            pass
    else:
        cam.release()

    ser.close()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)

---
## 📌 System Explanation

> The script uses a Raspberry Pi camera to determine the driving direction (**Clockwise** or **Anti-clockwise**) by checking whether the **orange line** or **blue line** is higher in the frame. It confirms the direction first, sends it to the Arduino, and waits for sensor calibration to complete before starting.

---

### 👁️ Computer Vision Breakdown

#### 1. Color Isolation
* **Functions:** `cv2.cvtColor()`, `cv2.inRange()`
* **Role:** Converts video frames to the **HSV** color space to ignore lighting shifts, creating black-and-white masks for orange and blue targets.

#### 2. Noise Filtering
* **Function:** `cv2.morphologyEx()`
* **Role:** Erases random background speckles and fills internal gaps within detected color patches.

#### 3. Position Tracking
* **Functions:** `cv2.findContours()`, `cv2.moments()`
* **Role:** Finds shape outlines and calculates their vertical center coordinates (`cy`) to determine which color sits higher in the frame.

#### 4. Visual Overlay & Interaction
* **Functions:** `cv2.fitLine()`, `cv2.line()`, `cv2.imshow()`
* **Role:** Fits a straight reference line through each color blob, renders status text on-screen, and processes keyboard controls (`q`, `s`, `p`).

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
