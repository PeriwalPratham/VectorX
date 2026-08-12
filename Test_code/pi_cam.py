import cv2
import time
from picamera2 import Picamera2

print("===================================")
print("Camera Test")
print("===================================")

picam2 = Picamera2()

# Good balance between quality and speed
config = picam2.create_preview_configuration(
    main={"size": (1536, 864)}
)

picam2.configure(config)
picam2.start()

time.sleep(2)

frame_count = 0
start_time = time.time()

while True:

    frame = picam2.capture_array()

    # Convert RGB → BGR for OpenCV
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    frame_count += 1
    elapsed = time.time() - start_time

    fps = frame_count / elapsed

    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow("Camera Test", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

picam2.stop()

cv2.destroyAllWindows()

print()
print("Camera test finished successfully.")
