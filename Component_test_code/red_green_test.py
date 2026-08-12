#Red Object
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

# CROP TOP OF IMAGE: Ignore background above the mat boundary (Top 30%)
CROP_TOP_Y = int(FRAME_HEIGHT * 0.30)  # Ignore Y < 144

MIN_AREA = 800  # Filters out tiny background specs

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

# --- ACCURATE HSV RED BOUNDS ---
# Pure Red wraps around the 0 and 180 boundaries on the HSV color wheel
LOWER_RED1 = np.array([0, 100, 50], dtype=np.uint8)
UPPER_RED1 = np.array([10, 255, 255], dtype=np.uint8)

LOWER_RED2 = np.array([160, 100, 50], dtype=np.uint8)
UPPER_RED2 = np.array([180, 255, 255], dtype=np.uint8)

kernel = np.ones((5, 5), np.uint8)

def send_command(cmd):
    if arduino and arduino.is_open:
        arduino.write((cmd + "\n").encode('utf-8'))

cv2.namedWindow("Red Zone Dodge Test", cv2.WINDOW_AUTOSIZE)

print("Starting Camera... Driving Forward...")
send_command("G") # Default: Go Straight

while True:
    # 1. Capture raw frame & fix channel ordering for OpenCV
    frame_raw = picam2.capture_array()
    frame_bgr = frame_raw[:, :, :3][:, :, ::-1].copy()

    # 2. CONVERT BGR -> HSV (Immune to lighting glare & shadows!)
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # 3. Apply HSV Red Filter (Combines both lower and upper hue wraps)
    mask1 = cv2.inRange(hsv, LOWER_RED1, UPPER_RED1)
    mask2 = cv2.inRange(hsv, LOWER_RED2, UPPER_RED2)
    red_mask = cv2.bitwise_or(mask1, mask2)

    # 4. CROP MASK: Zero out the top 30% so background outside track is NEVER scanned
    red_mask[0:CROP_TOP_Y, :] = 0

    # Clean up noise
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)

    # Find Contours
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    red_detected = False
    center_x = 0

    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > MIN_AREA:
            x, y, w, h = cv2.boundingRect(c)
            center_x = x + (w // 2)
            red_detected = True
            
            # Draw RED bounding box and yellow center point
            cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.circle(frame_bgr, (center_x, y + (h // 2)), 5, (0, 255, 255), -1)

    # --- RED ZONE DECISION LOGIC ---
    if not red_detected or center_x <= LINE_15:
        # Zone 0% - 15% (Clear / Off-screen to the left): Go Straight
        send_command("G")
        status_text = f"ZONE 0-15% (X={center_x}) -> STRAIGHT (85 deg)"
    elif LINE_15 < center_x <= LINE_50:
        # Zone 15% - 50%: Turn 10 degrees Right
        send_command("R10")
        status_text = f"ZONE 15-50% (X={center_x}) -> TURN 10 deg RIGHT (75 deg)"
    elif LINE_50 < center_x <= LINE_85:
        # Zone 50% - 85%: Turn 17 degrees Right
        send_command("R17")
        status_text = f"ZONE 50-85% (X={center_x}) -> TURN 17 deg RIGHT (68 deg)"
    else:
        # Zone 85% - 100%: Turn 20 degrees Right
        send_command("R20")
        status_text = f"ZONE 85-100% (X={center_x}) -> TURN 20 deg RIGHT (65 deg)"

    # Draw 3 vertical zone boundary lines
    cv2.line(frame_bgr, (LINE_15, 0), (LINE_15, FRAME_HEIGHT), (255, 255, 0), 1)  # 15% Line
    cv2.line(frame_bgr, (LINE_50, 0), (LINE_50, FRAME_HEIGHT), (0, 255, 255), 1)  # 50% Line (Center)
    cv2.line(frame_bgr, (LINE_85, 0), (LINE_85, FRAME_HEIGHT), (255, 255, 0), 1)  # 85% Line

    # Draw horizontal crop boundary line (Red line)
    cv2.line(frame_bgr, (0, CROP_TOP_Y), (FRAME_WIDTH, CROP_TOP_Y), (0, 0, 255), 1)

    # Display status
    cv2.putText(frame_bgr, status_text, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

    cv2.imshow("Red Zone Dodge Test", frame_bgr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        send_command("S") # Stop motor on quit
        break

picam2.stop()
if arduino:
    arduino.close()
cv2.destroyAllWindows()

#Green Object
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

# CROP TOP OF IMAGE: Ignore background above the mat boundary
CROP_TOP_Y = int(FRAME_HEIGHT * 0.30)  # Ignore top 30% (Y < 144)

MIN_AREA = 800  # Filters out tiny background specs

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

# --- ACCURATE HSV GREEN BOUNDS ---
# Hue: 35-85 (Pure Green range)
# Saturation: 80-255 (Ensures strong color, ignores dull background/walls)
# Value: 50-255 (Handles light and shadow)
LOWER_GREEN_HSV = np.array([35, 80, 50], dtype=np.uint8)
UPPER_GREEN_HSV = np.array([85, 255, 255], dtype=np.uint8)

kernel = np.ones((5, 5), np.uint8)

def send_command(cmd):
    if arduino and arduino.is_open:
        arduino.write((cmd + "\n").encode('utf-8'))

cv2.namedWindow("Green Zone Dodge Test", cv2.WINDOW_AUTOSIZE)

print("Starting Camera... Driving Forward...")
send_command("G") # Default: Go Straight

while True:
    # 1. Capture raw frame & fix channel ordering for OpenCV
    frame_raw = picam2.capture_array()
    frame_bgr = frame_raw[:, :, :3][:, :, ::-1].copy()

    # 2. CONVERT BGR -> HSV (Immune to lighting glare & shadows!)
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)

    # 3. Apply HSV Green Filter
    green_mask = cv2.inRange(hsv, LOWER_GREEN_HSV, UPPER_GREEN_HSV)

    # 4. CROP MASK: Zero out the top 30% so background outside track is NEVER scanned
    green_mask[0:CROP_TOP_Y, :] = 0

    # Clean up noise
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernel)

    # Find Contours
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    green_detected = False
    center_x = 0

    if contours:
        c = max(contours, key=cv2.contourArea)
        if cv2.contourArea(c) > MIN_AREA:
            x, y, w, h = cv2.boundingRect(c)
            center_x = x + (w // 2)
            green_detected = True
            
            # Draw GREEN bounding box and yellow center point
            cv2.rectangle(frame_bgr, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame_bgr, (center_x, y + (h // 2)), 5, (0, 255, 255), -1)

    # --- MIRRORED GREEN ZONE DECISION LOGIC ---
    if not green_detected or center_x > LINE_85:
        # Zone 85% - 100% (Cleared to far right / Off-screen): Go Straight
        send_command("G")
        status_text = f"ZONE 85-100% (X={center_x}) -> STRAIGHT (85 deg)"
    elif LINE_50 < center_x <= LINE_85:
        # Zone 50% - 85%: Turn 10 degrees Left
        send_command("L10")
        status_text = f"ZONE 50-85% (X={center_x}) -> TURN 10 deg LEFT (95 deg)"
    elif LINE_15 < center_x <= LINE_50:
        # Zone 15% - 50%: Turn 17 degrees Left
        send_command("L17")
        status_text = f"ZONE 15-50% (X={center_x}) -> TURN 17 deg LEFT (102 deg)"
    else:
        # Zone 0% - 15%: Turn 20 degrees Left
        send_command("L20")
        status_text = f"ZONE 0-15% (X={center_x}) -> TURN 20 deg LEFT (105 deg)"

    # Draw 3 vertical zone boundary lines
    cv2.line(frame_bgr, (LINE_15, 0), (LINE_15, FRAME_HEIGHT), (255, 255, 0), 1)  # 15% Line
    cv2.line(frame_bgr, (LINE_50, 0), (LINE_50, FRAME_HEIGHT), (0, 255, 255), 1)  # 50% Line (Center)
    cv2.line(frame_bgr, (LINE_85, 0), (LINE_85, FRAME_HEIGHT), (255, 255, 0), 1)  # 85% Line

    # Draw horizontal crop boundary line (Red line)
    cv2.line(frame_bgr, (0, CROP_TOP_Y), (FRAME_WIDTH, CROP_TOP_Y), (0, 0, 255), 1)

    # Display status
    cv2.putText(frame_bgr, status_text, (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)

    cv2.imshow("Green Zone Dodge Test", frame_bgr)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        send_command("S") # Stop motor on quit
        break

picam2.stop()
if arduino:
    arduino.close()
cv2.destroyAllWindows()
