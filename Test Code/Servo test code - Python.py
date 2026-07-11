import cv2
import numpy as np
import serial
import time

arduino = serial.Serial(
    '/dev/cu.usbserial-A5069RR4',
    9600
)

time.sleep(2)

cap = cv2.VideoCapture(0)

RED = [
    (np.array([0,170,80]), np.array([8,255,255])),
    (np.array([172,170,80]), np.array([180,255,255]))
]

GREEN = [
    (np.array([40,100,70]), np.array([85,255,255]))
]

MIN_AREA = 3000

servo_angle = 90

def move_servo(target):
    global servo_angle
    step = 1
    if servo_angle < target:
        servo_angle += step
    elif servo_angle > target:
        servo_angle -= step
    servo_angle = max(0,min(180,servo_angle))
    arduino.write(
        f"{servo_angle}\n".encode()
    )

def detect_color(frame,ranges):
    hsv=cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )
    mask=None
    for low,high in ranges:
        temp=cv2.inRange(
            hsv,
            low,
            high
        )
        if mask is None:
            mask=temp
        else:
            mask=cv2.bitwise_or(mask,temp)
    kernel=np.ones((7,7),np.uint8)
    mask=cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )
    contours,_=cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    biggest=None
    for c in contours:
        area=cv2.contourArea(c)
        if area < MIN_AREA:
            continue
        x,y,w,h=cv2.boundingRect(c)
        M=cv2.moments(c)
        if M["m00"] == 0:
            continue
        obj={
            "area":area,
            "x":int(M["m10"]/M["m00"]),
            "y":int(M["m01"]/M["m00"]),
            "box":(x,y,w,h)
        }

        if biggest is None or area > biggest["area"]:
            biggest=obj
    return biggest

while True:
    ret,frame=cap.read()
    if not ret:
        break
    frame_width=frame.shape[1]
    red=detect_color(
        frame,
        RED
    )

    green=detect_color(
        frame,
        GREEN
    )

    objects=[]
  
  if red:
        objects.append(
            ("RED",red)
        )
    if green:
        objects.append(
            ("GREEN",green)
        )
      
 if len(objects)>0:
        closest=max(
            objects,
            key=lambda x:x[1]["area"]
        )
        color,data=closest
        print(
            "Closest:",
            color,
            "Area:",
            int(data["area"])
        )
        cv2.putText(
            frame,
            f"Closest: {color}",
            (20,50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,255,255),
            3
        )
        cx=data["x"]
   
        # RED -> right side (90 to 0)
        if color=="RED":
            target=int(
                np.interp(
                    cx,
                    [0,frame_width],
                    [0,90]
                )
            )

        # GREEN -> left side (90 to 180)
        else:
            target=int(
                np.interp(
                    cx,
                    [0,frame_width],
                    [90,180]
                )
            )
        move_servo(target)
    else:
        move_servo(90)
    # draw ALL detected objects
    for name,obj in objects:
        x,y,w,h=obj["box"]
        if name=="RED":
            colour=(0,0,255)
        else:
            colour=(0,255,0)
        cv2.rectangle(
            frame,
            (x,y),
            (x+w,y+h),
            colour,
            3
        )
        cv2.putText(
            frame,
            f"{name} x={obj['x']} y={obj['y']} area={int(obj['area'])}",
            (x,y-15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            colour,
            2
        )
    cv2.putText(
        frame,
        f"Servo={servo_angle}",
        (20,90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,255),
        2
    )
    cv2.imshow(
        "WRO Tracking",
        frame
    )
    if cv2.waitKey(1)==ord('q'):
        break
cap.release()
arduino.close()
cv2.destroyAllWindows()
