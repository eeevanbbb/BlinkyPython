from BlinkyTape import BlinkyTape
import time
from random import randint

import GlobalSettings as G

def dynamicColor():
    # Copy pasta from flash_example.rainbow
    r = G.color[0]
    g = G.color[1]
    b = G.color[2]
    while True:
        if G.dynaColor is True:
            rNew = randint(0,255)
            gNew = randint(0,255)
            bNew = randint(0,255)

            transitionTime = 3.0
            numberOfSteps = float(G.speed) * transitionTime

            rDelta = (rNew - r) / numberOfSteps
            gDelta = (gNew - g) / numberOfSteps
            bDelta = (bNew - b) / numberOfSteps

            while transitionTime > 0:
                if G.dynaColor is True:
                    transitionTime -= 1/float(G.speed)

                    r += rDelta
                    g += gDelta
                    b += bDelta

                    # Setting global colors
                    G.color[0] = int(r)
                    G.color[1] = int(g)
                    G.color[2] = int(b)

                    # sleepy
                    time.sleep(1/float(G.speed))
                else:
                    return
        else:
            return
