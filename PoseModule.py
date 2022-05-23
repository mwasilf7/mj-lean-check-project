"""
Pose Module

"""
import cv2
import mediapipe as mp
import math

class PoseDetector:
    """
    Estimates pose points of a human body using the MediaPipe library.
    """

    def __init__(self, mode=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):
        """
        :param mode: In static mode, detection is done on each image: slower
        :param upBody: Upper body only flag
        :param smooth: Smoothness Flag
        :param detectionCon: Minimum Detection Confidence Threshold
        :param trackCon: Minimum Tracking Confidence Threshold
        """

        self.mode = mode
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode,
                                     smooth_landmarks=self.smooth,
                                     min_detection_confidence=self.detectionCon,
                                     min_tracking_confidence=self.trackCon)

    def findPose(self, img, draw=True):
        """
        Find the pose landmarks in an Image of BGR color space.
        :param img: Image to find the pose in.
        :param draw: Flag to draw the output on the image.
        :return: Image with or without drawings
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    def findPosition(self, img):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy, cz = int(lm.x * w), int(lm.y * h), (lm.z)
                self.lmList.append([id, cx, cy, cz])

        return self.lmList

    def findAngle(self,img,p1,p2,p3,p4, side=None, draw=True):
        ## Get landmarks
        a1, b1 = self.lmList[p1][1:3]
        a2, b2 = self.lmList[p2][1:3]
        a3, b3 = self.lmList[p3][1:3]
        a4, b4 = self.lmList[p4][1:3]
    
        ## Find angles
        if side == "left":
                angle1=math.degrees(math.atan2(b1 - b4, a1 - a4)-math.atan2(0,-100))
                angle2=math.degrees(math.atan2(b1 - b2, a1 - a2)-math.atan2(b3 - b2, a3 - a2))
                angle3=math.degrees(math.atan2(b2 - b3, a2 - a3)-math.atan2(b4 - b3, a4 - a3))

        elif side == "right":
                angle1=math.degrees(-math.atan2(b1 - b4, a1 - a4)+math.atan2(0,100))
                angle2=math.degrees(-math.atan2(b1 - b2, a1 - a2)+math.atan2(b3 - b2, a3 - a2))
                angle3=math.degrees(-math.atan2(b2 - b3, a2 - a3)+math.atan2(b4 - b3, a4 - a3))
        if angle1 < 0:
            angle1 += 360
        if angle2 < 0:
            angle2 += 360
        if angle3 < 0:
            angle3 += 360
        
        ## Draw lines and circles
        if draw:
            cv2.line(img, (a1, b1),(a2, b2) , (255, 255, 0), 3)
            cv2.line(img, (a2, b2),(a3, b3) , (255, 255, 0), 3)
            cv2.line(img, (a3, b3),(a4, b4) , (255, 255, 0), 3) 
            cv2.circle(img, (a1, b1), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (a1, b1), 15, (0, 0, 255), 2)
            cv2.circle(img, (a2, b2), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (a2, b2), 15, (0, 0, 255), 2)
            cv2.circle(img, (a3, b3), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (a3, b3), 15, (0, 0, 255), 2)
            cv2.circle(img, (a4, b4), 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (a4, b4), 15, (0, 0, 255), 2)
            
        return angle1, angle2, angle3