import cv2
import numpy as np
import serial
import time
from picamera2 import Picamera2

# --- CONFIGURATION & FRAME ZONES ---
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

LINE_15 = int(FRAME_WIDTH * 0.15)  # 96 px
LINE_50 = int(FRAME_WIDTH * 0.50)  # 320 px
LINE_85 = int(FRAME_WIDTH * 0.85)  # 544 px

CROP_TOP_Y = int(FRAME_HEIGHT * 0.30)  # Ignore background above mat
MIN_AREA = 800  

# --- TIMING TUNING FOR SINGLE-IMPULSE DODGE ---
DODGE_PULSE_TIME = 0.15   # Seconds to hold turn angle before snapping back to straight
COOLDOWN_TIME    = 0.80   # Seconds to ignore block re-triggers after a dodge

SERIAL_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

try:
    arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=0.01)
    time.sleep(2)
    print("Connected to Arduino on /dev/ttyUSB0")
except Exception as e:
    print(f"Serial Connection Warning: {e}")
    arduino = None

# --- CAMERA SETUP ---
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (FRAME_WIDTH, FRAME_HEIGHT)}))
picam2.start()
time.sleep(1)

# HSV COLOR BOUNDS
LOWER_RED1 = np.array([0, 100, 50], dtype=np.uint8)
UPPER_RED1 = np.array([10, 255, 255], dtype=np.uint8)
LOWER_RED2 = np.array([160, 100, 50], dtype=np.uint8)
UPPER_RED2 = np.array([180, 255, 255], dtype=np.uint8)

LOWER_GREEN = np.array([35, 80, 50], dtype=np.uint8)
UPPER_GREEN = np.array([85, 255, 255], dtype=np.uint8)

kernel = np.ones((5, 5), np.uint8)

def send_command(cmd):
    if arduino and arduino.is_open:
        arduino.write((cmd + "\n").encode('utf-8'))
        arduino.flush()

def find_largest_object(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > MIN_AREA:
            x, y, w, h = cv2.boundingRect(c)
            center_x = x + (w // 2)
            return True, center_x, h, (x, y, w, h)
    return False, 0, 0, None

cv2.namedWindow("Master State-Machine Dodge", cv2.WINDOW_AUTOSIZE)

print("Starting State-Machine Single-Impulse Dodge...")
send_command("G")

# STATE TRACKING VARIABLES
state = "DRIVING_STRAIGHT"  # States: DRIVING_STRAIGHT, DODGING_PULSE, COOLDOWN
pulse_start_time = 0
cooldown_start_time = 0

try:
    while True:
        current_time = time.time()

        frame_raw = picam2.capture_array()
        frame_bgr = frame_raw[:, :, :3][:, :, ::-1].copy()

        hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

        mask_r1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
        mask_r2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
        red_mask = cv2.bitwise_or(mask_r1, mask_r2)
        green_mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

        red_mask[0:CROP_TOP_Y, :] = 0
        green_mask[0:CROP_TOP_Y, :] = 0

        red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
        green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

        red_found, red_x, red_h, red_box = find_largest_object(red_mask)
        green_found, green_x, green_h, green_box = find_largest_object(green_mask)

        target_color = None
        if red_found and green_found:
            target_color = 'RED' if red_h >= green_h else 'GREEN'
        elif red_found:
            target_color = 'RED'
        elif green_found:
            target_color = 'GREEN'

        # --- STATE MACHINE CONTROL ---

        # 1. STATE: DODGING PULSE (Active turn impulse in progress)
        if state == "DODGING_PULSE":
            if current_time - pulse_start_time >= DODGE_PULSE_TIME:
                send_command("G")  # Snap back to STRAIGHT immediately!
                state = "COOLDOWN"
                cooldown_start_time = current_time
                print("Pulse ended! Servo straightened (G). Entering cooldown...")

        # 2. STATE: COOLDOWN (Driving straight, ignoring same block to avoid re-trigger)
        elif state == "COOLDOWN":
            if current_time - cooldown_start_time >= COOLDOWN_TIME:
                state = "DRIVING_STRAIGHT"
                print("Cooldown complete. Ready for next block.")

        # 3. STATE: DRIVING STRAIGHT (Scanning for new threat block)
        elif state == "DRIVING_STRAIGHT":
            cmd_to_trigger = None

            if target_color == 'RED':
                # RED block: Dodge RIGHT if in middle/right zone
                if LINE_15 < red_x <= LINE_50:
                    cmd_to_trigger = "R10"
                elif LINE_50 < red_x <= LINE_85:
                    cmd_to_trigger = "R17"
                elif red_x > LINE_85:
                    cmd_to_trigger = "R20"

            elif target_color == 'GREEN':
                # GREEN block: Dodge LEFT if in middle/left zone
                if LINE_50 < green_x <= LINE_85:
                    cmd_to_trigger = "L10"
                elif LINE_15 < green_x <= LINE_50:
                    cmd_to_trigger = "L17"
                elif green_x <= LINE_15:
                    cmd_to_trigger = "L20"

            # Execute single impulse turn if threat zone hit
            if cmd_to_trigger:
                send_command(cmd_to_trigger)
                state = "DODGING_PULSE"
                pulse_start_time = current_time
                print(f"Triggered Impulse {cmd_to_trigger}! Holding for {DODGE_PULSE_TIME}s...")

        # Visual Overlays
        cv2.line(frame_bgr, (LINE_15, 0), (LINE_15, FRAME_HEIGHT), (255, 255, 0), 1)
        cv2.line(frame_bgr, (LINE_50, 0), (LINE_50, FRAME_HEIGHT), (0, 255, 255), 1)
        cv2.line(frame_bgr, (LINE_85, 0), (LINE_85, FRAME_HEIGHT), (255, 255, 0), 1)
        cv2.line(frame_bgr, (0, CROP_TOP_Y), (FRAME_WIDTH, CROP_TOP_Y), (0, 0, 255), 1)

        status_text = f"STATE: {state} | TARGET: {target_color if target_color else 'NONE'}"
        cv2.putText(frame_bgr, status_text, (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

        cv2.imshow("Master State-Machine Dodge", frame_bgr)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            send_command("S")
            break

except KeyboardInterrupt:
    print("\nStopping run...")

send_command("S")
picam2.stop()
if arduino:
    arduino.close()
cv2.destroyAllWindows()
