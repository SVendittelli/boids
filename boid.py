from p5 import Vector, stroke, stroke_weight, point, triangle
import random
import math

class Boid():

    def __init__(self, x, y, width, height):
        self.max_steer = 1
        self.max_speed = 5
        self.sight_radius = 100
        self.personal_space_radius = 50
        self.width = width
        self.height = height
        self.position = Vector(x, y)
        self.bucket = self.determine_bucket()
        self.velocity = Vector.random_2D() * self.max_speed
        self.acceleration = Vector(0, 0)
        self.al_weight, self.co_weight, self.sep_weight = ratio((1, 1, 1.1))

    def show(self):
        stroke(255)
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
        self.bucket = self.determine_bucket()
        self.velocity += self.acceleration
        self.velocity.limit(upper_limit=self.max_speed)
        self.acceleration = Vector(0, 0)

    def determine_bucket(self):
        return (math.floor(self.position.x / self.sight_radius), math.floor(self.position.y / self.sight_radius))

    def flock(self, boids):
        alignment = Vector(0, 0)
        cohesion = Vector(0, 0)
        separation = Vector(0, 0)

        total_in_sight = 0
        total_in_personal_space = 0
        for boid in boids:
            if boid is self:
                continue

            distance = self.position.distance(boid.position)
            if distance < self.sight_radius:
                alignment += boid.velocity
                cohesion += boid.position
                total_in_sight += 1
            if distance < self.personal_space_radius:
                difference = self.position - boid.position
                separation += difference / distance**2
                total_in_personal_space += 1

        alignment = self.align(alignment, total_in_sight)
        cohesion = self.cohere(cohesion, total_in_sight)
        separation = self.separate(separation, total_in_personal_space)

        self.acceleration = self.al_weight * alignment + self.co_weight * cohesion + self.sep_weight * separation

    def align(self, steering, total):
        if total > 0:
            steering /= total
            steering.magnitude = self.max_speed
            steering -= self.velocity
            steering.limit(upper_limit=self.max_steer)

        return steering

    def cohere(self, steering, total):
        if total > 0:
            steering /= total
            steering -= self.position
            steering.magnitude = self.max_speed
            steering -= self.velocity
            steering.limit(upper_limit=self.max_steer)

        return steering

    def separate(self, steering, total):
        if total > 0:
            steering /= total
            steering.magnitude = self.max_speed
            steering -= self.velocity
            steering.limit(upper_limit=self.max_steer)

        return steering

    def edges(self):
        if self.position.x >= self.width:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = self.width - 1

        if self.position.y >= self.height:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = self.height - 1

def ratio(factors):
    total = sum(factors)
    return (f/total for f in factors)
