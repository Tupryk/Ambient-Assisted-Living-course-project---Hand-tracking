import numpy as np
import DeskCompanion.HandTracker as ht
from DeskCompanion.ThreeDRendering import Mesh, Renderer

hand = ht.TrackerHand(show=True)

m = Mesh()
r = Renderer()

sliderStartingPos = np.array([])
sliderLatestPos = np.array([])

while hand.step():

    if hand.handPresent():
        
        if hand.isBarSlider():

            sliderLatestPos = hand.nodes[8]
            if not len(sliderStartingPos):
                sliderStartingPos = hand.nodes[8]
            else:
                y_angle = -np.pi*2*(sliderLatestPos[0]-sliderStartingPos[0])/.5
                x_angle = np.pi*2*(sliderLatestPos[1]-sliderStartingPos[1])/.5
                rotated_mesh = m.rotate(np.array([x_angle, y_angle, 0]))
                r.draw(rotated_mesh)
        
        elif len(sliderStartingPos):

            y_angle = -np.pi*2*(sliderLatestPos[0]-sliderStartingPos[0])/.5
            x_angle = np.pi*2*(sliderLatestPos[1]-sliderStartingPos[1])/.5

            m.updateRotation(np.array([x_angle, y_angle, 0]))

            sliderStartingPos = np.array([])
            sliderLatestPos = np.array([])
    
    else:
        print("No hands detected")
