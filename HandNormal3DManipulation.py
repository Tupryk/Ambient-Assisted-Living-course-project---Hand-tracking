# This method of 3d manipulation didn't prove to be very effective

import DeskCompanion.HandTracker as ht
from DeskCompanion.ThreeDRendering import Mesh, Renderer

hand = ht.TrackerHand(show=True)

m = Mesh()
r = Renderer()

while hand.step():

    hand.mainIsRight()

    if hand.handPresent():
        angles = hand.getRotation()
        r.draw(m.rotate(angles))
    
    else:
        print("No hands detected")
