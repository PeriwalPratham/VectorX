import cv2
import numpy as np
from picamera2 import Picamera2
import time

# ----------------------------
# Camera
# ----------------------------

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": (1280,720)}
)

picam2.configure(config)
picam2.start()

time.sleep(2)

# ------------------------------------
# HSV VALUES
# Replace after calibration
# ------------------------------------

LOWER_PINK = np.array([140,80,80])
UPPER_PINK = np.array([179,255,255])

FONT = cv2.FONT_HERSHEY_SIMPLEX

while True:

    frame = picam2.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, LOWER_PINK, UPPER_PINK)

    kernel = np.ones((5,5),np.uint8)

    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if contours:

        largest = max(contours, key=cv2.contourArea)

        area = cv2.contourArea(largest)

        if area > 500:

            x,y,w,h = cv2.boundingRect(largest)

            cx = x + w//2
            cy = y + h//2

            cv2.rectangle(
                frame,
                (x,y),
                (x+w,y+h),
                (255,0,255),
                2
            )

            cv2.circle(
                frame,
                (cx,cy),
                5,
                (255,255,255),
                -1
            )

            cv2.putText(
                frame,
                "PARKING",
                (x,y-10),
                FONT,
                0.7,
                (255,0,255),
                2
            )

            cv2.putText(
                frame,
                f"Centre: ({cx},{cy})",
                (x,y+h+20),
                FONT,
                0.5,
                (255,0,255),
                2
            )

            cv2.putText(
                frame,
                f"W:{w} H:{h}",
                (x,y+h+40),
                FONT,
                0.5,
                (255,0,255),
                2
            )

            cv2.putText(
                frame,
                f"Area:{int(area)}",
                (x,y+h+60),
                FONT,
                0.5,
                (255,0,255),
                2
            )

            print("----------------------------------")
            print("Parking Area Found")
            print(f"Centre : ({cx}, {cy})")
            print(f"Width  : {w}")
            print(f"Height : {h}")
            print(f"Area   : {int(area)}")

    cv2.imshow("Parking Detection", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
