from p5 import *
from boid import Boid
import numpy as np

n = 1000
width = n
height = n

flock = []

def init():
    global flock
    flock = [Boid(*np.random.rand(2)*n, width, height) for _ in range(30)]

def setup():
    init()
    size(width, height)

def draw():
    background(51)
    for boid in flock:
        boid.flock(flock)

    for boid in flock:
        boid.update()
        boid.show()

def key_pressed():
    init()

if __name__ == '__main__':
    run()
