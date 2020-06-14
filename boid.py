from p5 import Vector, stroke, stroke_weight, point, triangle
import random
import math

class Boid():

    def __init__(self, x, y, width, height):
        self.max_steer = 1
        self.max_speed = 5
        self.sight_radius = 100
        self.width = width
        self.height = height
        self.position = Vector(x, y)
        self.velocity = Vector.random_2D() * self.max_speed
        self.acceleration = Vector(0, 0)

    def show(self):
        stroke(255)
        # stroke_weight(16)
        # point(self.position.x, self.position.y)
        direction = self.velocity.copy()
        direction.magnitude = 7
        head = self.position + direction

        angle = 2 * math.pi / 3

        port = self.velocity.copy()
        port.rotate(angle)
        port.magnitude = 3
        port += self.position

        starboard = self.velocity.copy()
        starboard.rotate(-angle)
        starboard.magnitude = 3
        starboard += self.position

        triangle(head, port, starboard)

    def update(self):
        self.position += self.velocity
        self.edges()
        self.velocity += self.acceleration
        self.velocity.limit(upper_limit=self.max_speed, lower_limit=0.1)
        self.acceleration = Vector(0, 0)

    def flock(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)
        self.acceleration = alignment + cohesion + separation

    def align(self, boids):
        steering = Vector(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance(boid.position)
            if not self is boid and distance < self.sight_radius:
                steering += boid.velocity
                total = total + 1

        if total > 0:
            steering /= total
            steering.magnitude = self.max_speed
            steering -= self.velocity
            steering.limit(upper_limit=self.max_steer)

        return steering

    def cohere(self, boids):
        steering = Vector(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance(boid.position)
            if not self is boid and distance < self.sight_radius:
                steering = steering + boid.position
                total = total + 1

        if total > 0:
            steering /= total
            steering -= self.position
            steering.magnitude = self.max_speed
            steering -= self.velocity
            steering.limit(upper_limit=self.max_steer)

        return steering

    def separate(self, boids):
        steering = Vector(0, 0)
        total = 0
        for boid in boids:
            distance = self.position.distance(boid.position)
            if not self is boid and distance < 66:
                difference = self.position - boid.position
                steering = steering + (difference / distance**2)
                total = total + 1

        if total > 0:
            steering /= total
            steering.magnitude = self.max_speed
            steering -= self.velocity
            steering.limit(upper_limit=self.max_steer)

        return steering

    def edges(self):
        if self.position.x > self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width

        if self.position.y > self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height
