import cv2
import time
import math
from imutils.video import FPS

vid = cv2.VideoCapture(0)
fps = None
initBB = None
bbox = []
flag = True
while True:
    start_time = time.time()
    ok, frame = vid.read()
    if flag == True:
        H, W = frame.shape[:2]
        cW = int(W / 2)
        cH = int(H / 2)
        flag = False
    if not ok:
        print("video not received")
    if initBB is not None:
        ok, initBB = tracker.update(frame)
        if ok:
            x = int(initBB[0])
            y = int(initBB[1])
            w = x + int(initBB[2])
            h = y + int(initBB[3])
            x0 = int(bbox[0])
            y0 = int(bbox[1])
            elapsed_time = time.time() - start_time
            distance = math.sqrt((x-x0)**2 + (y-y0)**2)
            speed = distance/elapsed_time
            speed = round(speed, 2)
            #print(speed)
            speed = speed/1000
            if x == x0:
                speed1 = 0.00
                print(f"Speed = {speed1} m/s")
            else: 
                print(f"Speed = {round(speed, 2)} m/s")
            fps.update()
            fps.stop()
            cv2.rectangle(frame, (x, y), (w, h), (0, 255, 0), 5)
            cv2.putText(frame, f"FPS: {round(fps.fps(), 2)}", (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            bbox[0] = x
            bbox[1] = y
            bbox[2] = w
            bbox[3] = h
        else:
            cv2.putText(frame, "Tracking failure detected", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
        cv2.putText(frame, "KCF Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)
    cv2.imshow("frame1", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('s'):
        initBB = None
        initBB = cv2.selectROI("frame3", frame, fromCenter=False, showCrosshair=True)
        fps=FPS().start()
        cv2.destroyWindow("frame3")
        flag = True
        tracker = cv2.TrackerKCF_create()
        ok = tracker.init(frame, initBB)
        x = int(initBB[0])
        y = int(initBB[1])
        w = x + int(initBB[2])
        h = y + int(initBB[3])
        bbox = [f"{x}", f"{y}", f"{w}", f"{h}"]
vid.release()
cv2.destroyAllWindows()
