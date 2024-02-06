import cv2
import pyautogui
from DeskCompanion.HandTracker import TrackerHand  

def map_to_screen(x, y, screen_width, screen_height):
    screen_x = screen_width-int(x * screen_width)
    screen_y = int(y * screen_height)
    return screen_x, screen_y

def move_mouse(hand, screen_width, screen_height):
    if hand.handPresent():
        pointing_finger = hand.nodes[8]  
        screen_x, screen_y = map_to_screen(pointing_finger[0], pointing_finger[1], screen_width, screen_height)
        pyautogui.moveTo(screen_x, screen_y)

def main():
    screen_width, screen_height = pyautogui.size()
 
    hand_tracker = TrackerHand(show=True)

    while hand_tracker.step():
        if hand_tracker.handPresent():

            move_mouse(hand_tracker, screen_width, screen_height)

            hand_tracker.mainIsLeft()
            if hand_tracker.handPresent():
                if hand_tracker.isPinching():
                    pyautogui.mouseDown(button='left')

if __name__ == '__main__':
    main()
