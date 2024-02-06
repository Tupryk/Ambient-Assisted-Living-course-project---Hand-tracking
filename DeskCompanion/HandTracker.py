import cv2
import time
import numpy as np
import mediapipe as mp


class TrackerHand:

    def __init__(self, show: bool = False, rightHanded: bool = True):

        self.cap = cv2.VideoCapture(6)
        if not self.cap.isOpened():
            print("Cannot open webcam")
            exit()

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()

        self.mpHandLandmarks = []

        self.right_handed = rightHanded
        self.nodes: [np.ndarray] = []
        self.nodes_r: [np.ndarray] = []
        self.nodes_l: [np.ndarray] = []

        self.roots = {
            "Thumb": 1,
            "Index": 5,
            "Middle": 9,
            "Ring": 13,
            "Pinky": 17
        }

        self.mp_drawing = mp.solutions.drawing_utils
        if show:
            cv2.namedWindow("Tracker visual")
            self.step = self.stepShow
        else:
            self.step = self.justStep

    def fingerTipPosition(self, fingerRootIndex: int=5):
        return self.nodes[fingerRootIndex+3]

    def reloadNodes(self, mediapipe_hand, label):
        # This may be a bit inneficient as we dont always need all finger nodes
        # Should turn coordinates to "real world" coordinates more consistent operations

        new_nodes = []
        for l in mediapipe_hand.landmark:
            new_nodes.append(np.array([l.x, l.y, l.z]))

        if label == "Left":  # Flipped frame
            self.nodes_r = new_nodes
        else:
            self.nodes_l = new_nodes

    def showLastestFrame(self):
        finalFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        for lm in self.mpHandLandmarks:
            self.mp_drawing.draw_landmarks(finalFrame, lm,
                                           connections=self.mp_hands.HAND_CONNECTIONS)
        cv2.imshow("Tracker visual", finalFrame)
        cv2.waitKey(1)

    def reloadMainNodes(self):
        if self.right_handed:
            self.nodes = self.nodes_r
        else:
            self.nodes = self.nodes_l

    # Takes a picture, returns false if there was an error
    def justStep(self, freq: float = .0) -> bool:

        ret, self.frame = self.cap.read()
        if not ret:
            return False

        self.frame = cv2.resize(self.frame, (640, 480))
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

        self.nodes = []
        self.nodes_r = []
        self.nodes_l = []
        self.mpHandLandmarks = []

        results = self.hands.process(self.frame)
        if results.multi_hand_landmarks:

            for i, lm in enumerate(results.multi_hand_landmarks):
                self.mpHandLandmarks.append(lm)
                label = results.multi_handedness[i].classification[0].label
                self.reloadNodes(self.mpHandLandmarks[i], label)

        else:
            self.mpHandLandmarks = []

        self.reloadMainNodes()

        if freq:
            time.sleep(freq)

        return True

    def stepShow(self, freq: float = .0) -> bool:
        status = self.justStep(freq=freq)
        self.showLastestFrame()
        return status

    def handNumber(self) -> int:
        sum_ = 0
        for index in [5, 9, 13, 17]:
            if self.fingerUp(index):
                sum_ += 1
            else:
                break
        return sum_

    def handPresent(self) -> bool:
        return bool(len(self.nodes))
    
    def handsPresent(self) -> bool:
        return bool(len(self.nodes_r) and len(self.nodes_l))

    # Joints is size 4 of joint indices
    def meanOfFingerAngles(self, fingerRoot: int) -> float:
        sum = 0
        vec1 = self.nodes[fingerRoot+1]-self.nodes[fingerRoot]
        vec2 = self.nodes[fingerRoot+2]-self.nodes[fingerRoot+1]
        vec1 /= np.linalg.norm(vec1)
        vec2 /= np.linalg.norm(vec2)

        sum += np.arccos(np.dot(vec1, vec2))

        vec1 = self.nodes[fingerRoot+2]-self.nodes[fingerRoot+1]
        vec2 = self.nodes[fingerRoot+3]-self.nodes[fingerRoot+2]
        vec1 /= np.linalg.norm(vec1)
        vec2 /= np.linalg.norm(vec2)

        sum += np.arccos(np.dot(vec1, vec2))

        return sum*.5

    def isFist(self):

        indices = [5, 9, 13, 17]
        total = 0

        for i in indices:
            total += self.meanOfFingerAngles(i)

        total /= len(indices)

        return total > 1.4

    def fingerUp(self, fingerRoot: int) -> bool:  # Joints is size 4 of joint indices
        hand_dir = self.nodes[9]-self.nodes[0]
        finger_dir = self.nodes[fingerRoot+3]-self.nodes[fingerRoot+2]
        hand_dir /= np.linalg.norm(hand_dir)
        finger_dir /= np.linalg.norm(finger_dir)
        return np.dot(hand_dir, finger_dir) > .2

    def isPinching(self, otherFingersUp: bool = True) -> bool:
        if otherFingersUp and (not self.fingerUp(9) or not self.fingerUp(13) or not self.fingerUp(17)):
            return False
        
        thumbToIndexDist = np.linalg.norm(self.nodes[4] - self.nodes[8])
        indexBoneScale = np.linalg.norm(self.nodes[8] - self.nodes[7]) * 1.5
        return thumbToIndexDist <= indexBoneScale

    def isGrabbing(self) -> bool:
        finger_dist = np.linalg.norm(self.nodes[4] - self.nodes[8])
        rel = np.linalg.norm(self.nodes[8] - self.nodes[7])
        return finger_dist >= rel*1.5 and finger_dist <= rel*6.

    def isPeace(self):
        return (self.fingerUp(5) and self.fingerUp(9)
                and not self.fingerUp(13) and not self.fingerUp(17)
                and np.linalg.norm(self.nodes[8] - self.nodes[12]) > np.linalg.norm(self.nodes[5] - self.nodes[9]))

    def isBarSlider(self) -> bool:
        return (self.fingerUp(5) and self.fingerUp(9)
                and not self.fingerUp(13) and not self.fingerUp(17)
                and np.linalg.norm(self.nodes[8] - self.nodes[12]) < np.linalg.norm(self.nodes[5] - self.nodes[9])*1.5)

    def knobAngle(self, relativeTo: np.ndarray = np.array([0., 0., 1.])) -> float:
        if self.isGrabbing():
            thumbToIndex = self.nodes[4] - self.nodes[8]
            thumbToIndex /= np.linalg.norm(thumbToIndex)
            return np.arccos(np.dot(thumbToIndex, relativeTo))
        return np.nan

    def indexThumbVector(self) -> np.ndarray:
        if self.isGrabbing():
            angles = self.nodes[8] - self.nodes[4]
            angles /= np.linalg.norm(angles)
            angles = np.arccos(angles)
            return angles
        return np.array([])
    
    def fingerVector(self, fingerRoot):
        vector = self.nodes[fingerRoot+2]-self.nodes[fingerRoot]
        vector /= np.linalg.norm(vector)
        return vector
    
    def getRotation(self) -> np.ndarray:
        vec1 = self.nodes[9] - self.nodes[0]
        vec2 = self.nodes[13] - self.nodes[0]
        handNormal = np.cross(vec1, vec2)
        handNormal /= np.linalg.norm(handNormal)
        angles = np.arccos(handNormal)
        return angles

    def detectSigns(self) -> str:
        sign = ""
        if self.isPinching():
            sign = "pinching"
        return sign

    def mainIsLeft(self):
        self.nodes = self.nodes_l

    def mainIsRight(self):
        self.nodes = self.nodes_r

    def palmToFront():
        return False
    
   
    def isPointing(self, threshold_angle: float = 0.8) -> bool:
        if not self.handPresent():
            return False

        index_finger_dir = self.nodes[8] - self.nodes[0] #problem: erkennt nicht nur den Zeigefinger 
        index_finger_dir /= np.linalg.norm(index_finger_dir)
        
        camera_direction = np.array([0., 0., -1.])

        # Calculate the angle between the index finger and the camera direction
        angle = np.arccos(np.dot(index_finger_dir, camera_direction))

        return angle < threshold_angle
