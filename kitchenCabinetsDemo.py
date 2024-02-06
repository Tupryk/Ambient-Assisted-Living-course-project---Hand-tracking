# This demo will track if there are two hands making number signs (1-4)
# There are 4 cabinets in the kitchen, the hand sign will tell which one to open
from DeskCompanion.KitchenApi import activateShelf
import DeskCompanion.HandTracker as ht
import time

tracker = ht.TrackerHand(show=True)

shelvesClosed = [True for _ in range(4)]

while tracker.step():

    tracker.mainIsRight()
    right_present = tracker.handPresent()

    tracker.mainIsLeft()
    left_present = tracker.handPresent()

    if right_present and left_present:
        tracker.mainIsRight()
        number = tracker.handNumber()
        print("Number: ", number)
        tracker.mainIsLeft()
        print("Left hand fist: ", tracker.isFist())
        if tracker.isFist() and number != 0:
            print(activateShelf(number-1))
            time.sleep(1)
    
    else:
        print("No hands detected")
