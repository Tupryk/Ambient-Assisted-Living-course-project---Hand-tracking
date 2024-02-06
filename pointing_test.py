import cv2
import unittest
from DeskCompanion.HandTracker import TrackerHand  

class LiveTestTrackerHand(unittest.TestCase):

    def setUp(self):
        self.tracker = TrackerHand(show=True)

    def test_live_isPointing(self):
        while True:
            # Capture a frame and update hand information
            if not self.tracker.stepShow(freq=0.03):
                break

            result = self.tracker.isPointing()

            # Display live result
            frame = cv2.cvtColor(self.tracker.frame, cv2.COLOR_RGB2BGR)
            if result:
                cv2.putText(frame, "Pointing towards camera", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Not pointing towards camera", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            cv2.imshow("Live Test", frame)

        cv2.destroyAllWindows()

if __name__ == '__main__':
    unittest.main()
