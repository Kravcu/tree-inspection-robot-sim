import copy
import random
from enum import Enum
from typing import List

import matplotlib.pyplot as plt
import numpy as np


class State(Enum):
    Init = 0
    Work = 1
    Charge = 2
    Service = 3


class Battery:
    def __init__(self):
        self.battery_level = 100  # 0 - 100

    def get_battery_level(self):
        return self.battery_level

    def get_charging_time(self):
        return (100 - self.battery_level) / 2

    def charge(self):
        self.battery_level = 100

    def drain_battery(self, value):
        if self.battery_level - value > 5:
            return True
        else:
            return False


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_left(self):
        self.x += -3
        self.x = -self.x

    def move_right(self):
        self.x += 3

    def move_up(self):
        self.y += 3

    def move_down(self):
        self.y += -3

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class Robot:

    def __init__(self, terrain_viscosity_map, tree_map, x_pos=0, y_pos=0, y_max_pos=886, x_max_pos=1317):
        self.terrain_viscosity_map = terrain_viscosity_map
        self.position = Position(x_pos, y_pos)
        self.pos_history: List[Position] = []
        self.x_max_pos = x_max_pos
        self.y_max_pos = y_max_pos
        self.tree_map = tree_map

    def random_walk(self):
        val = random.randint(1, 4)
        if val == 1:
            self.position.move_up()
        elif val == 2:
            self.position.move_down()
        elif val == 3:
            self.position.move_left()
        else:
            self.position.move_right()
        self.check_position()
        self.pos_history.append(copy.copy(self.position))

    def walk(self, direction):
        if direction == "left":
            self.position.move_left()
        elif direction == "right":
            self.position.move_right()
        elif direction == "up":
            self.position.move_up()
        elif direction == "down":
            self.position.move_down()
        self.check_position()
        self.pos_history.append(copy.copy(self.position))

    def check_position(self):
        if self.position.x < 0:
            self.position.x = -self.position.x
        if self.position.y < 0:
            self.position.y = -self.position.y
        if self.position.x > self.x_max_pos:
            self.position.x = self.x_max_pos
        if self.position.y > self.y_max_pos:
            self.position.y = self.y_max_pos

    def detect_tree(self):
        if self.tree_map[self.position.get_x()][self.position.get_y()] == 1:
            return True
        else:
            return False


class Simulation:
    def __init__(self, tree_map=0):
        self.img = plt.imread('forest.png')
        self.tree_map = tree_map
        img_x, img_y = len(self.img[0]), len(self.img)
        plt.imshow(self.img, origin={0, 0})

        self.workers: List[Robot] = [Robot(np.random.rand(img_x, img_y), self.tree_map, 600, 430)]
        for i in range(10000):
            self.workers[0].random_walk()
        plt.scatter([elem.get_x() for elem in self.workers[0].pos_history],
                    [elem.get_y() for elem in self.workers[0].pos_history], s=5)
        plt.title('Tree inspection robot simulation')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()


sim = Simulation()
