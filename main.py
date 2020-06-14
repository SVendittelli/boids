from p5 import *
from boid import Boid
import numpy as np

width = 750
height = 750

flock = [Boid(*np.random.rand(2)*750, width, height) for _ in range(25)]

def setup():
    size(width, height)

def draw():
    background(51)
    for boid in flock:
        boid.flock(flock)

    for boid in flock:
        boid.update()
        boid.show()

if __name__ == '__main__':
    run()
