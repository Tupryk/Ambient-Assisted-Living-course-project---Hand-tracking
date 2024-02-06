import pygame
import numpy as np
import DeskCompanion.HandTracker as ht

pygame.init()
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Desk Companion Screen")

tracker = ht.TrackerHand(show=True)

screen = [] # A list of three points in 3d space that represent the screen plane

index = tracker.roots["Index"]

pinchLock = False

# SETUP LOOP
while tracker.step():

    if tracker.handsPresent():

        pointing = tracker.fingerUp(index)
        tracker.mainIsLeft()
        pinching = tracker.isPinching()
        tracker.mainIsRight()

        if pointing and pinching and not pinchLock:
            pinchLock = True

            fingerVector = tracker.fingerVector(index)
            handPoint = tracker.nodes[index]

            screen.append(handPoint + fingerVector*10.)

        elif not pinching:
            pinchLock = False
    
    else:
        print("No hands detected")

    window.fill((0, 0, 0))

    if len(screen) == 0:
        pygame.draw.circle(window, (255, 0, 0), [10, 10], 10)

    elif len(screen) == 1:
        pygame.draw.circle(window, (255, 0, 0), [window_width-10, 10], 10)

    elif len(screen) == 2:
        pygame.draw.circle(window, (255, 0, 0), [window_width*.5, window_height-10], 10)

    elif len(screen) >= 3:
        break
    
    pygame.display.update()


screenNormal = np.cross(screen[1]-screen[0], screen[2]-screen[0])
screenPoint = screen[0]
def intersectionToScreen(inter: np.ndarray) -> [float]:
    screenWidth = screen[1][0] - screen[0][0]
    screenHeight = screen[2][1] - screen[0][1]

    x = np.abs(inter[0]/screenWidth * window_width)
    y = inter[1]/screenHeight * window_height
    print(x, y)
    if x > screenWidth: x = screenWidth
    if x < 0: x = 0
    if y > screenHeight: x = screenHeight
    if y < 0: y = 0

    return [x, y]

# MAIN LOOP
while tracker.step():

    if tracker.handPresent():

        if tracker.fingerUp(index):
            fingerVector = tracker.fingerVector(index)
            handPoint = tracker.nodes[index]

            t = np.dot(screenNormal, screenPoint - handPoint) / np.dot(screenNormal, fingerVector)
            intersectionPoint = handPoint + t * fingerVector

            window.fill((0, 0, 0))

            windowPoint = intersectionToScreen(intersectionPoint)
            pygame.draw.circle(window, (255, 0, 0), windowPoint, 10)

            pygame.display.update()
        
    else:
        # print("No hands detected")
        pass

    pygame.display.update()
