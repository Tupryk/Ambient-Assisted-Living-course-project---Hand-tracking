# In this demo we use our HandTacker class to set a value "intensity" by tracking a sliding motion on the fingers.
import pygame
import numpy as np
import DeskCompanion.HandTracker as ht

pygame.init()
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Intensity")

tracker = ht.TrackerHand(show=True)

intensity = .5
sliding = -1.
init_sliding = -1.

while tracker.step():

    tracker.mainIsRight()
    right_present = tracker.handPresent()

    tracker.mainIsLeft()
    left_present = tracker.handPresent()

    if right_present and left_present:

        if tracker.isPeace():

            tracker.mainIsRight()

            if sliding < 0. and tracker.isBarSlider():
                sliding = 0.
                init_sliding = tracker.nodes_r[8]

            elif sliding >= 0. and tracker.isBarSlider():
                intensity = np.linalg.norm(tracker.nodes_r[8] - init_sliding) * 2.

            else:
                sliding = -1.

            if intensity > 1.:
                intensity = 1.
            elif intensity < 0.:
                intensity = 0.
        
        else:
            print("No peace sign")
    
    else:
        print("No hands detected")

    pygame.display.update()
    window.fill((255*intensity, 255*intensity, 255*intensity))