import cv2
import numpy as np


cap = cv2.VideoCapture(0)


while True:

    ret, frame = cap.read()

    if not ret:
        break


    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )


    # Orange

    lower_orange = np.array(
        [10, 100, 100]
    )

    upper_orange = np.array(
        [25, 255, 255]
    )

    orange_mask = cv2.inRange(
        hsv,
        lower_orange,
        upper_orange
    )


    # Blue

    lower_blue = np.array(
        [85, 50, 100]
    )

    upper_blue = np.array(
        [130, 255, 255]
    )

    blue_mask = cv2.inRange(
        hsv,
        lower_blue,
        upper_blue
    )


    # Orange contours

    orange_contours, _ = cv2.findContours(
        orange_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    for contour in orange_contours:

        if cv2.contourArea(contour) > 500:

            x, y, w, h = cv2.boundingRect(
                contour
            )

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 165, 255),
                2
            )

            print(
                f"Orange detected: "
                f"x={x}, y={y}"
            )

            break


    # Blue contours

    blue_contours, _ = cv2.findContours(
        blue_mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    for contour in blue_contours:

        if cv2.contourArea(contour) > 500:

            x, y, w, h = cv2.boundingRect(
                contour
            )

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (255, 0, 0),
                2
            )

            print(
                f"Blue detected: "
                f"x={x}, y={y}"
            )

            break


    cv2.imshow(
        "Webcam",
        frame
    )


    if (
        cv2.waitKey(1) & 0xFF
        == ord('q')
    ):

        break


cap.release()

cv2.destroyAllWindows()
