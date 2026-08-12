#!/usr/bin/env python3

"""
=========================================================
FULL PI DIAGNOSTICS

Checks:
✓ Python
✓ OpenCV
✓ Picamera2
✓ Camera
✓ Serial
✓ FPS

Press Q to quit the camera test.

=========================================================
"""

import sys
import time

print("=" * 45)
print("VECTORX PI DIAGNOSTICS")
print("=" * 45)

# -------------------------------------------------
# Python Version
# -------------------------------------------------

print("\nChecking Python...")

print(f"Version : {sys.version.split()[0]}")
print("Status  : PASS")

# -------------------------------------------------
# OpenCV
# -------------------------------------------------

try:
    import cv2

    print("\nChecking OpenCV...")
    print("Version :", cv2.__version__)
    print("Status  : PASS")

except Exception as e:

    print("\nChecking OpenCV...")
    print("Status : FAIL")
    print(e)
    exit()

# -------------------------------------------------
# Picamera2
# -------------------------------------------------

try:

    from picamera2 import Picamera2

    print("\nChecking Picamera2...")
    print("Status : PASS")

except Exception as e:

    print("\nChecking Picamera2...")
    print("Status : FAIL")
    print(e)
    exit()

# -------------------------------------------------
# Camera
# -------------------------------------------------

print("\nOpening Camera...")

try:

    picam2 = Picamera2()

    config = picam2.create_preview_configuration(
        main={"size": (1280,720)}
    )

    picam2.configure(config)

    picam2.start()

    time.sleep(2)

    print("Camera : PASS")

except Exception as e:

    print("Camera : FAIL")
    print(e)
    exit()

# -------------------------------------------------
# Serial
# -------------------------------------------------

print("\nChecking Serial...")

try:

    import serial

    ser = serial.Serial("/dev/ttyUSB0",115200,timeout=1)

    time.sleep(2)

    print("Serial : PASS")

except Exception as e:

    print("Serial : FAIL")
    print(e)

    ser = None

# -------------------------------------------------
# FPS TEST
# -------------------------------------------------

print("\nRunning FPS Test...")

frames = 0

start = time.time()

while True:

    frame = picam2.capture_array()

    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

    frames += 1

    elapsed = time.time() - start

    fps = frames / elapsed

    cv2.putText(
        frame,
        f"FPS : {fps:.1f}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow("Diagnostics",frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

picam2.stop()

cv2.destroyAllWindows()

if ser:
    ser.close()

# -------------------------------------------------
# SUMMARY
# -------------------------------------------------

print("\n")
print("=" * 45)
print("SUMMARY")
print("=" * 45)

print(f"Average FPS : {fps:.1f}")

if fps > 20:
    print("Camera FPS  : PASS")
else:
    print("Camera FPS  : LOW")

print("\nDiagnostics Complete")

