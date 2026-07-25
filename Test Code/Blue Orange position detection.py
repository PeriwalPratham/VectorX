from picamera2 import Picamera2
import cv2
import numpy as np
import serial

# Adjust the port name if needed:
# Linux/Raspberry Pi: usually '/dev/ttyACM0' or '/dev/ttyUSB0'
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
direction_sent = False   # only send the command once, not every frame

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "BGR888"}
)

picam2.configure(config)
picam2.start()

while True:

    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # -----------------------------------
    # Only look at bottom half
    # -----------------------------------
    roi_y = 220
    roi = frame[roi_y:, :]

    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # -------------------------
    # Orange
    # -------------------------
    lower_orange = np.array([10,100,100])
    upper_orange = np.array([25,255,255])
    orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)

    # -------------------------
    # Blue
    # -------------------------
    lower_blue = np.array([85,50,100])
    upper_blue = np.array([130,255,255])
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((5,5),np.uint8)

    orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_OPEN, kernel)
    orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_CLOSE, kernel)

    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
    blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)

    orange_y = None
    blue_y = None

    # ========================================
    # ORANGE
    # ========================================

    contours, _ = cv2.findContours(
        orange_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        if cv2.contourArea(c) > 300:

            vx, vy, x0, y0 = cv2.fitLine(
                c,
                cv2.DIST_L2,
                0,
                0.01,
                0.01
            )

            vx = float(vx)
            vy = float(vy)
            x0 = float(x0)
            y0 = float(y0)

            left_y = int((-x0 * vy / vx) + y0)
            right_y = int((((roi.shape[1]-1)-x0)*vy/vx)+y0)

            cv2.line(
                roi,
                (0,left_y),
                (roi.shape[1]-1,right_y),
                (0,165,255),
                3
            )

            orange_y = left_y

    # ========================================
    # BLUE
    # ========================================

    contours, _ = cv2.findContours(
        blue_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_NONE
    )

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        if cv2.contourArea(c) > 300:

            vx, vy, x0, y0 = cv2.fitLine(
                c,
                cv2.DIST_L2,
                0,
                0.01,
                0.01
            )

            vx = float(vx)
            vy = float(vy)
            x0 = float(x0)
            y0 = float(y0)

            left_y = int((-x0 * vy / vx) + y0)
            right_y = int((((roi.shape[1]-1)-x0)*vy/vx)+y0)

            cv2.line(
                roi,
                (0,left_y),
                (roi.shape[1]-1,right_y),
                (255,0,0),
                3
            )

            blue_y = left_y

    # ========================================
    # Decide which comes first
    # ========================================

    if orange_y is not None and blue_y is not None and not direction_sent:

        if orange_y > blue_y:
            text = "Orange comes first"
            arduino.write(b'O')
        else:
            text = "Blue comes first"
            arduino.write(b'B')

        direction_sent = True   # stop sending after the first decision

        cv2.putText(
            frame,
            text,
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,0),
            2
        )

    cv2.imshow("Camera", frame)
    cv2.imshow("Orange Mask", orange_mask)
    cv2.imshow("Blue Mask", blue_mask)

    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
arduino.close()
