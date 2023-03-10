# Path: main.py
#gym workout motion tracker

import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

pTime = 0

# check if the person is doin a push-up correctly 
def pushup_check(lankle, rankle, lknee, rknee, lhip, rhip):
    # check if the knees are below the ankles
    if lknee[1] > lankle[1] and rknee[1] > rankle[1]:
        # check if the hips are above the knees
        if lhip[1] < lknee[1] and rhip[1] < rknee[1]:
            return True
    return False


# check if the person is doin a squat correctly
def squat_check(lankle, rankle, lknee, rknee, lhip, rhip):
    # check if the knees are below the ankles
    if lknee[1] > lankle[1] and rknee[1] > rankle[1]:
        # check if the hips are below the knees
        if lhip[1] > lknee[1] and rhip[1] > rknee[1]:
            return True
    return False


nr_of_pushups = 0
prev_state="0"
state_stack=["0"]

while True:

    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        # for id, lm in enumerate(results.pose_landmarks.landmark):
        #     # print(id, lm)
        #     h, w, c = img.shape
        #     cx, cy = int(lm.x * w), int(lm.y * h)
        #     print(id, cx, cy)
        #     cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        # get the coordinates of the landmarks
        lankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].y]
        rankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].y]
        lknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].y]
        rknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].y]
        lhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].y]
        rhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].y]

        # check if the person is doin a squat correctly
        state_stack.append(prev_state)
        if pushup_check(lankle, rankle, lknee, rknee, lhip, rhip):
            print("Squatting correctly")
            if min([0 if x!="Squatting correctly"else 1 for x in state_stack[max(len(state_stack)-5,0):]])==1:
                nr_of_pushups+=1
            prev_state="Squatting correctly"
        else:
            print("Squatting incorrectly")
            prev_state="Squatting incorrectly"
        state_stack.append(prev_state)
        if len(state_stack)>5:
            state_stack.pop(0)
        print("Nr of pushups: ", nr_of_pushups, state_stack)

        # check if
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        # w
