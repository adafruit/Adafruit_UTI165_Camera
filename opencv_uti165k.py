import numpy as np
import time
import cv2

camera_num = 0

for camera_num in range(6):
    cam = cv2.VideoCapture(camera_num)
    if not cam.isOpened():
        print("Was not able to open camera", camera_num)
        cam.release()
        continue
    if not cam.set(3, 240) or cam.get(3) != 240:
        print("Was not able to set camera", camera_num, "width to 240 pixels")
        cam.release()
        continue
    if not cam.set(4, 321) or cam.get(4) != 321:
        print("Was not able to set camera", camera_num, "height to 321 pixels")
        cam.release()
        continue
    break

print("Camera %d open at size: (%d x %d)" % (camera_num, cam.get(3), cam.get(4)))

while(True):
    # Capture frame-by-frame
    ret, frame = cam.read()

    if not ret:
        print("Failed to fetch frame")
        continue
    print("Frame OK!")
    time.sleep(0.1)
    # Our operations on the frame come here
    #colorframe = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    # Display the resulting frame
    #cv2.imshow('frame', colorframe)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

cam.release()
cv2.destroyAllWindows()
