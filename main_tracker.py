import cv2
from tracker import *

# Create tracker object
tracker = EuclideanDistTracker()

cap = cv2.VideoCapture("video_parking.mp4")

# Object detection from Stable camera
object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=50)

while True:
    ret, frame = cap.read()
    height, width, _ = frame.shape
    x_box_1 = 0
    y_box_1 = 500
    w_box_1 = 500
    h_box_1 = 300
    
    x_box_2 = 700
    y_box_2 = 500
    w_box_2 = 500
    h_box_2 = 300
    # Object detection
    box_1 = frame[x_box_1:x_box_1+w_box_1, y_box_1:y_box_1+h_box_1]

    box_2 = frame[x_box_2: x_box_2+w_box_2, y_box_2: y_box_2+h_box_2]

    mask_box_1 = object_detector.apply(box_2)
    _, mask_box_1 = cv2.threshold(mask_box_1, 254, 255, cv2.THRESH_BINARY)
    contours_box_1, _ = cv2.findContours(mask_box_1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.rectangle(frame, (x_box_1, y_box_1), (x_box_1+w_box_1, y_box_1+h_box_1), (0, 255, 0), 3)
    cv2.rectangle(frame, (x_box_2, y_box_2), (x_box_2+w_box_2, y_box_2+h_box_2), (0, 255, 0), 3)
    detections = []
    for cnt in contours_box_1:
        # Calculate area and remove small elements
        area = cv2.contourArea(cnt)
        if area > 4000:
            #cv2.drawcontours_box_1(box_1, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.putText(box_2, str(area), (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            detections.append([x, y, w, h])
            cv2.rectangle(box_2, (x_box_1, y_box_1), (x_box_1+w_box_1, y_box_1+h_box_1), (0, 255, 0), 3)

    cv2.imshow("box_1", box_1)
    cv2.imshow("Frame", frame)
    # cv2.imshow("mask_box_1", mask_box_1)

    key = cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()