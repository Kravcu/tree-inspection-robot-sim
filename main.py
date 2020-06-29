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
        self.x += -1

    def move_right(self):
        self.x += 1

    def move_up(self):
        self.y += 1

    def move_down(self):
        self.y += -1

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def reposition(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def __cmp__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False


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
        self.pos_history.append(self.position.get_pos())

    def walk(self, direction):
        if direction == "left":
            self.position.move_left()
        elif direction == "right":
            self.position.move_right()
        elif direction == "up":
            self.position.move_up()
        elif direction == "down":
            self.position.move_down()
        # self.check_position()
        self.pos_history.append(self.position.get_pos())

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
    def __init__(self, tree_map: np.ndarray = 0):
        self.img = plt.imread('forest.png')
        self.tree_map = tree_map

        img_x, img_y = len(self.img[0]), len(self.img)
        self.visited = [[0 for x in range(img_x)] for y in range(img_y)]
        plt.imshow(self.img, origin={0, 0})

        self.workers: List[Robot] = [Robot(np.random.rand(img_x, img_y), self.tree_map, 430, 430),
                                     Robot(np.random.rand(img_x, img_y), self.tree_map, 800, 430)]
        for i in range(10000):
            workers_to_remove = []
            for index, worker in enumerate(self.workers):
                possible_moves = []
                x = worker.position.get_x()
                y = worker.position.get_y()
                if random.randint(0, 100) < 2:
                    print(f"Worker {index} został zniszczony przez studia na AGH.")
                    decision = input("would you like to [remove] or [reposition]? ")
                    decision = input(f"Would you like to [remove] or [reposition]? ")
                    if decision == "remove":
                        workers_to_remove.append(index)
                    elif decision == "reposition":
                        x = int(input("Please put new X pos "))
                        y = int(input("Please put new Y pos "))
                        self.workers[index].position.reposition(x, y)
                else:
                    try:
                        if (self.visited[x + 1][y] == 0 and x + 1 <= img_x) or (x + 1, y) in worker.pos_history:
                            possible_moves.append('right')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[x - 1][y] == 0 and x - 1 >= 0) or (x - 1, y) in worker.pos_history:
                            possible_moves.append('left')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[x][y + 1] == 0 and y + 1 <= img_y) or (x, y + 1) in worker.pos_history:
                            possible_moves.append('up')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[x][y - 1] == 0 and y - 1 >= 0) or (x, y - 1) in worker.pos_history:
                            possible_moves.append('down')
                    except IndexError:
                        pass

                    if not possible_moves:
                        print(f"Worker {index} has run out of moves.")
                        decision = input(f"Would you like to [remove] or [reposition]? ")
                        if decision == "remove":
                            workers_to_remove.append(index)
                        elif decision == "reposition":
                            x = int(input("Please put new X pos "))
                            y = int(input("Please put new Y pos "))
                            self.workers[index].position.reposition(x, y)
                    else:
                        choice = random.choice(possible_moves)
                        self.workers[index].walk(choice)
                    self.visited[worker.position.get_x()][worker.position.get_y()] = 1
                    if self.tree_map[worker.position.get_x()][worker.position.get_y()] == 1:
                        print("znalazlem se drzewo. zajebiscie")
                        plt.scatter(worker.position.get_x(), worker.position.get_y(), s=10)
                for elem in workers_to_remove:
                    self.workers.remove(elem)

        # TODO add dynamic plotting of workers position
        plt.scatter(worker.position.get_x(), worker.position.get_y(), s=5)
        plt.title('Tree inspection robot simulation')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()


img = plt.imread('forest.png')
img_x, img_y = len(img[0]), len(img)
sim = Simulation(tree_map=np.random.rand(img_x, img_y))
