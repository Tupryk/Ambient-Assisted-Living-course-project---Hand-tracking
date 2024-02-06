import time
import pyautogui
import numpy as np
import DeskCompanion.HandTracker as ht

tracker = ht.TrackerHand(show=True)

frames_in_between = 0
frames_to_travel = [5, 10]
distance_to_travel = [.05, .7]
doing_motion = False

while tracker.step():

    if (tracker.handPresent() and tracker.isBarSlider()) or (tracker.handPresent() and doing_motion):
        if not doing_motion:
            start_position = tracker.fingerTipPosition()
            print("Initiated cycle")
        doing_motion = True
        frames_in_between += 1

        if frames_to_travel[0] <= frames_in_between:
            if frames_to_travel[1] >= frames_in_between:
                print("Ended cycle")

                end_position = tracker.fingerTipPosition()
                distance_traveled = np.linalg.norm(end_position - start_position)
                print("Distance traveled: ", distance_traveled)

                if distance_traveled >= distance_to_travel[0] and distance_traveled <= distance_to_travel[1] and tracker.isBarSlider():
                    # Check direction of travel
                    if start_position[0] - end_position[0] < 0:
                        pyautogui.press("left")
                        print("------- Go back -------")
                    else:
                        pyautogui.press("right")
                        print("------- Go forward -------")
                    time.sleep(1.)

            frames_in_between = 0
            doing_motion = False

    else:
        doing_motion = False
        frames_in_between = 0
