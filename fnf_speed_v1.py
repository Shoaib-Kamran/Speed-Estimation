import cv2
import time
from imutils.video import FPS

vid = cv2.VideoCapture(0)
fps = None
initBB = None
###################################
initialTime = 0  
initialDistance = 0  
changeInTime = 0  
changeInDistance = 0  
listDistance = []  
listSpeed = []  
DECLARED_LEN = 30 # cm  
DECLARED_WID = 14.3 # cm  
GREEN = (0, 255, 0)  
RED = (255, 0, 0)  
WHITE = (255, 255, 255)  
fonts = cv2.FONT_HERSHEY_COMPLEX

def focal_length(determined_distance, actual_width, width_in_rf_image):  
    focal_length_value = (width_in_rf_image * determined_distance) / actual_width  
    return focal_length_value

def speedFinder(coveredDistance, timeTaken):  
    speed = coveredDistance / timeTaken  
    return speed

def averageFinder(completeList, averageOfItems):  
    lengthOfList = len(completeList)  
    selectedItems = lengthOfList - averageOfItems  
    selectedItemsList = completeList[selectedItems:]  
    average = sum(selectedItemsList) / len(selectedItemsList)  
    return average

def distance_finder(focal_length, real_face_width, face_width_in_frame):  
    distance = (real_face_width * focal_length) / face_width_in_frame  
    return distance 
##################################

while True:
    ok, frame = vid.read()
    if not ok:
        print("video not received")
    if initBB is not None:
        ok, initBB = tracker.update(frame)
        if ok:
            x = int(initBB[0])
            y = int(initBB[1])
            w = x + int(initBB[2])
            h = y + int(initBB[3])
            fps.update()
            fps.stop()
            #################################################################
            face_width_in_frame = w  
            if face_width_in_frame != 0:  
                Distance = distance_finder(focal_length_found, DECLARED_WID, face_width_in_frame)  
                listDistance.append(Distance)  
                averageDistance = averageFinder(listDistance, 2)    
                distanceInMeters = averageDistance/100  
                if initialDistance != 0:   
                    changeInDistance = initialDistance - distanceInMeters  
                    changeInTime = time.time() - initialTime   
                    speed = speedFinder(coveredDistance=changeInDistance, timeTaken=changeInTime) 
                    listSpeed.append(speed)     
                    averageSpeed = averageFinder(listSpeed, 10)  
                    if averageSpeed < 0:  
                        averageSpeed = averageSpeed * -1 
                    # filling the progressive line dependent on the speed.  
                    speedFill = int(45+(averageSpeed) * 130)  
                    if speedFill > 235:  
                        speedFill = 235  
                    cv2.line(frame, (45, 165), (235, 165), (0, 255, 0), 35)   
                    cv2.line(frame, (45, 165), (speedFill, 165), (255, 255, 0), 32)  
                    cv2.line(frame, (45, 165), (235, 165), (0, 0, 0), 22)   
                    cv2.putText(frame, f"Speed: {round(averageSpeed, 2)} m/s", (50, 170), fonts, 0.6, (0, 255, 220), 2)  
                initialDistance = distanceInMeters    
                initialTime = time.time()  
                # Writing Text on the displaying screen  
                cv2.line(frame, (45, 115), (255, 115), (255, 0, 255), 30)  
                cv2.line(frame, (45, 115), (255, 115), (0, 0, 0), 22)  
                cv2.putText(frame, f"Distance = {round(distanceInMeters,2)} m", (50, 120), fonts, 0.6, WHITE, 2)  
                #################################################################
                cv2.rectangle(frame, (x,y), (w,h), (0,255,0), 5)
                cv2.line(frame, (45, 65), (200, 65), (255, 0, 255), 30)  
                cv2.line(frame, (45, 65), (200, 65), (0, 0, 0), 22)  
                cv2.putText(frame, f"FPS = {round(fps.fps(), 3)}", (50, 70), fonts, 0.6, WHITE, 2)
        else:
            cv2.line(frame, (45, 65), (325, 65), (255, 0, 255), 30)  
            cv2.line(frame, (45, 65), (325, 65), (0, 0, 0), 22)  
            cv2.putText(frame, "Tracking failure detected", (50, 70), fonts, 0.6, WHITE, 2)
        cv2.line(frame, (45, 15), (175, 15), (0, 255, 0), 35)   
        cv2.line(frame, (45, 15), (175, 15), (255, 255, 0), 32)  
        cv2.line(frame, (45, 15), (175, 15), (0, 0, 0), 22)   
        cv2.putText(frame, "KCF Tracker", (50, 20), fonts, 0.6, WHITE, 2)
    cv2.imshow("frame1",frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('s'):
        initBB = None
        initBB = cv2.selectROI("frame3",frame, fromCenter = False, showCrosshair=True)
        fps=FPS().start()
        cv2.destroyWindow("frame3")
        tracker = cv2.TrackerKCF_create()
        ok = tracker.init(frame, initBB)
        ###############################
        x = int(initBB[0])
        w = x + int(initBB[2])
        focal_length_found = focal_length(DECLARED_LEN, DECLARED_WID, w) 
        ##############################

vid.release()
cv2.destroyAllWindows()