from p5 import *
from boid import Boid
import numpy as np
import math

n = 800
width = n
height = n

flock = []
bucket_size = 100
max_x_bucket = math.ceil(width / bucket_size)
max_y_bucket = math.ceil(height / bucket_size)

def init():
    global flock
    flock = [Boid(*np.random.rand(2)*n, width, height) for _ in range(30)]

def setup():
    init()
    size(width, height)

def draw():
    background(51)
    stroke(128)
    for x in range(max_x_bucket):
        line(Vector(x*bucket_size, 0), Vector(x*bucket_size, height))
    for y in range(max_y_bucket):
        line(Vector(0, y*bucket_size), Vector(width, y*bucket_size))

    buckets = { (x, y): [] for x in range(max_x_bucket) for y in range(max_y_bucket) }
    for boid in flock:
        buckets[boid.bucket].append(boid)

    for boid in flock:
        x_neighbours = set([max(0, (boid.bucket[0] - 1)), boid.bucket[0], min(boid.bucket[0] + 1, max_x_bucket - 1)])
        y_neighbours = set([max(0, (boid.bucket[1] - 1)), boid.bucket[1], min(boid.bucket[1] + 1, max_y_bucket - 1)])
        local_buckets = [ buckets[(x, y)] for x in x_neighbours for y in y_neighbours ]
        local_boids = [ b for bucket in local_buckets for b in bucket ]
        boid.flock(local_boids)
        boid.update()
        boid.show()

def key_pressed():
    init()

if __name__ == '__main__':
    run()
