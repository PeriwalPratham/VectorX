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

<img width="474" height="474" alt="OIP-3428776098" src="https://github.com/user-attachments/assets/e974975c-841e-4834-8ada-cf40c2051d88" />

### Steering

#### Servo Motor

<img width="1200" height="1200" alt="REV-41-3334-Smart_Robot_Servo_V2-Balanced_INSIDE__28225 1753214770-3286525541" src="https://github.com/user-attachments/assets/112df6cb-7e90-4af8-a5c2-14de61a694c0" />


---

## Power and Sensor Architecture

### Power System

#### Battery

#### Voltage Regulator

### Controllers

<img width="1600" height="1052" alt="ArduinoUno_R3_Front-3654177212" src="https://github.com/user-attachments/assets/e9da40f3-1fdb-42d2-8113-28963e8ecdc3" />

-
-
-
-
-

<img width="474" height="473" alt="OIP-1711219644" src="https://github.com/user-attachments/assets/414433e6-4477-445a-ad29-f6cabc85f16f" />



### Sensors

#### Camera

<img width="1400" height="1050" alt="2-114993030-raspberry-pi-camera-3-wide-font-534121739" src="https://github.com/user-attachments/assets/5c6cab85-ed41-4f66-8147-8fbd5683255c" />

- **Model:** Raspberry Pi Camera Module 3 Wide
- **Sensor:** Sony IMX708, 12MP
  #!/usr/bin/env python3

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


# ---------------- HSV RANGES ----------------
ORANGE_LOWER = (5, 100, 80)
ORANGE_UPPER = (28, 255, 255)

BLUE_LOWER = (95, 100, 70)
BLUE_UPPER = (130, 255, 255)

MIN_CONTOUR_AREA = 350
STABLE_FRAMES_REQUIRED = 15
SEND_REPEAT_DELAY_SEC = 0.3

PRE_CONNECT_DETECT_TIMEOUT_SEC = 6.0

# ---------------- COMMUNICATION LAYER SETTINGS ----------------
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
        time.sleep(2)  # Sensor warm-up before serial connection
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


# ---------------- COMMUNICATION HELPERS ----------------

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
    parser.add_argument("--port", default="/dev/ttyUSB0", help="Serial port for Arduino")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    args = parser.parse_args()

    # PHASE 1: Vision before Serial Connection
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

        cv2.imshow("Direction Detection", debug)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        if time.time() - detect_start > PRE_CONNECT_DETECT_TIMEOUT_SEC:
            print("WARNING: Timeout reached before confirming direction. Proceeding with default.")
            break

    # PHASE 2: Open Serial & Wait for Arduino
    print("Opening serial connection...")
    ser = serial.Serial(args.port, args.baud, timeout=0.5)
    ser.reset_input_buffer()

    print("Waiting for Arduino READY signal...")
    if wait_for_arduino_ready(ser):
        print("Arduino is READY.")
    else:
        print("WARNING: READY timeout. Proceeding with send retries.")

    direction_sent = False
    if confirmed_direction is not None:
        direction_sent = send_command_with_ack(ser, confirmed_direction)
        if direction_sent:
            print(f"Direction {confirmed_direction} ACKed by Arduino.")

    # PHASE 3: Main Execution Loop
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

        cv2.imshow("Direction Detection", debug)
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

    # Clean Exit
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
