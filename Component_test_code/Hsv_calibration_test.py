import cv2
from picamera2 import Picamera2
import time

# ---------------------------------------
# Camera
# ---------------------------------------

picam2 = Picamera2()

config = picam2.create_preview_configuration(
    main={"size": (1280,720)}
)

picam2.configure(config)
picam2.start()

time.sleep(2)

# ---------------------------------------
# Trackbars
# ---------------------------------------

cv2.namedWindow("Controls")

cv2.createTrackbar("H Min","Controls",0,179,lambda x:None)
cv2.createTrackbar("S Min","Controls",0,255,lambda x:None)
cv2.createTrackbar("V Min","Controls",0,255,lambda x:None)

cv2.createTrackbar("H Max","Controls",179,179,lambda x:None)
cv2.createTrackbar("S Max","Controls",255,255,lambda x:None)
cv2.createTrackbar("V Max","Controls",255,255,lambda x:None)

previous = (-1,-1,-1,-1,-1,-1)

# ---------------------------------------
# Main Loop
# ---------------------------------------

while True:

    frame = picam2.capture_array()

    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    hMin = cv2.getTrackbarPos("H Min","Controls")
    sMin = cv2.getTrackbarPos("S Min","Controls")
    vMin = cv2.getTrackbarPos("V Min","Controls")

    hMax = cv2.getTrackbarPos("H Max","Controls")
    sMax = cv2.getTrackbarPos("S Max","Controls")
    vMax = cv2.getTrackbarPos("V Max","Controls")

    lower = (hMin,sMin,vMin)
    upper = (hMax,sMax,vMax)

    mask = cv2.inRange(hsv,lower,upper)

    result = cv2.bitwise_and(frame,frame,mask=mask)

    cv2.imshow("Original",frame)
    cv2.imshow("Mask",mask)
    cv2.imshow("Detected",result)

    current = (hMin,sMin,vMin,hMax,sMax,vMax)

    if current != previous:

        print()
        print("----------------------------")
        print("Lower HSV =",lower)
        print("Upper HSV =",upper)

        previous = current

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

picam2.stop()

cv2.destroyAllWindows()
