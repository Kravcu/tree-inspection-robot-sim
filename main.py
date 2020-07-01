import copy
import random
from enum import Enum
from typing import *

import matplotlib.pyplot as plt
import numpy as np


class State(Enum):
    Init = 0
    Walk = 1
    Fire_detected = 2
    Tipped_over = 3
    Out_of_moves = 4


class Forest:
    def __init__(self):
        self.forest_data: np.ndarray = plt.imread("trunks.png")
        self.rows: int = len(self.forest_data)
        self.cols: int = len(self.forest_data[0])

        for y in range(5, self.rows - 5):  # powalanie drzew, dla uproszczenie 8 kierunków
            for x in range(5, self.cols - 5):
                if self.forest_data[y][x] == 1:
                    if np.random.random() > 0.999:
                        direction = np.random.randint(0, 8)
                        if direction == 0:
                            self.forest_data[y - 1][x] = 0.5
                            self.forest_data[y - 2][x] = 0.5
                            self.forest_data[y - 3][x] = 0.5
                            self.forest_data[y - 4][x] = 0.5
                            self.forest_data[y - 5][x] = 0.5
                        elif direction == 1:
                            self.forest_data[y - 1][x + 1] = 0.5
                            self.forest_data[y - 2][x + 2] = 0.5
                            self.forest_data[y - 3][x + 3] = 0.5
                        elif direction == 2:
                            self.forest_data[y][x + 1] = 0.5
                            self.forest_data[y][x + 2] = 0.5
                            self.forest_data[y][x + 3] = 0.5
                            self.forest_data[y][x + 4] = 0.5
                            self.forest_data[y][x + 5] = 0.5
                        elif direction == 3:
                            self.forest_data[y + 1][x + 1] = 0.5
                            self.forest_data[y + 2][x + 2] = 0.5
                            self.forest_data[y + 3][x + 3] = 0.5
                        elif direction == 4:
                            self.forest_data[y + 1][x] = 0.5
                            self.forest_data[y + 2][x] = 0.5
                            self.forest_data[y + 3][x] = 0.5
                            self.forest_data[y + 4][x] = 0.5
                            self.forest_data[y + 5][x] = 0.5
                        elif direction == 5:
                            self.forest_data[y + 1][x - 1] = 0.5
                            self.forest_data[y + 2][x - 2] = 0.5
                            self.forest_data[y + 3][x - 3] = 0.5
                        elif direction == 6:
                            self.forest_data[y][x - 1] = 0.5
                            self.forest_data[y][x - 2] = 0.5
                            self.forest_data[y][x - 3] = 0.5
                            self.forest_data[y][x - 4] = 0.5
                            self.forest_data[y][x - 5] = 0.5
                        else:
                            self.forest_data[y - 1][x - 1] = 0.5
                            self.forest_data[y - 2][x - 2] = 0.5
                            self.forest_data[y - 3][x - 3] = 0.5

        for y in range(self.rows):
            for x in range(self.cols):
                if self.forest_data[y][x] == 0.5:
                    self.forest_data[y][x] = 1

        self.raw_tree_data = copy.deepcopy(self.forest_data)

        for y in range(self.rows):
            for x in range(self.cols):
                if self.forest_data[y][x] != 1:
                    self.forest_data[y][x] = np.random.random() - 0.5  # rozklad gaussa, rodek 0.0, zróżicowanie terenu

    def get_tree_map(self) -> np.ndarray:
        return self.raw_tree_data

    def get_terrain_map(self) -> np.ndarray:
        return self.forest_data


class Position:
    def __init__(self, y, x):
        self.y = y
        self.x = x

    def move_left(self):
        self.y += -1

    def move_right(self):
        self.y += 1

    def move_up(self):
        self.x += 1

    def move_down(self):
        self.x += -1

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

    def reposition(self, y, x):
        self.y = y
        self.x = x

    def get_pos(self):
        return self.y, self.x

    def __cmp__(self, other):
        if self.y == other.y and self.x == other.x:
            return True
        else:
            return False

    def __str__(self):
        return f"y={self.y},x={self.x}"


class Robot:

    def __init__(self, y_pos=0, x_pos=0, x_may_pos=886, y_may_pos=1317):
        self.position: Position = Position(y_pos, x_pos)
        self.pos_historx: List[Tuple(float, float)] = []
        self.y_may_pos: float = y_may_pos
        self.x_may_pos: float = x_may_pos
        self.current_state: State = State.Init
        self.trees_found: List[Tuple(int, int)] = []

    def walk(self, direction):
        if direction == "left":
            self.position.move_left()
        elif direction == "right":
            self.position.move_right()
        elif direction == "up":
            self.position.move_up()
        elif direction == "down":
            self.position.move_down()
        self.pos_historx.append(self.position.get_pos())

    def check_for_fire(self, tree_map_) -> bool:  # to do
        try:
            if tree_map_[self.position.y - 1][self.position.x - 1] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.y][self.position.x - 1] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.y + 1][self.position.x - 1] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.y + 1][self.position.x] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.y + 1][self.position.x + 1] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.y][self.position.x + 1] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.y - 1][self.position.x + 1] == 2:
                self.change_state(State.Fire_detected)

                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.y - 1][self.position.x] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass

        return False

    def reposition(self, y, x):
        self.position = Position(y, x)
        self.change_state(State.Walk)

    ##

    def detect_tree(self, tree_map):  # todo
        if tree_map[self.position.get_y() + 1][self.position.get_x()] == 1:
            self.trees_found.append((self.position.get_y() + 1, self.position.get_x()))
        if tree_map[self.position.get_y() - 1][self.position.get_x()] == 1:
            self.trees_found.append((self.position.get_y() - 1, self.position.get_x()))
        if tree_map[self.position.get_y()][self.position.get_x() + 1] == 1:
            self.trees_found.append((self.position.get_y(), self.position.get_x() + 1))
        if tree_map[self.position.get_y()][self.position.get_x() + 1] == 1:
            self.trees_found.append((self.position.get_y(), self.position.get_x() + 1))
            return True
        else:
            return False

    def change_state(self, state: State):
        self.current_state = state


class Simulation:
    def __init__(self, tree_map: Forest):
        self.img = plt.imread('forest.png')
        self.tree_map: np.ndarray = tree_map.get_tree_map()
        self.terrain_map: np.ndarray = tree_map.get_terrain_map()

        self.img_y, self.img_x = len(self.img[0]), len(self.img)
        self.visited = [[0 for y in range(self.img_y)] for x in range(self.img_x)]
        plt.imshow(self.img, origin={0, 0})

        self.workers: List[Robot] = [Robot(430, 1300),
                                     Robot(800, 430),
                                     Robot(800, 1000),
                                     Robot(0, 100)]

    def simulate(self):
        fire_y_limit = len(self.tree_map) - 1
        fire_x_limit = len(self.tree_map[0]) - 1

        # fire_y = np.random.randint(fire_y_limit)
        # fire_x = np.random.randint(fire_x_limit)
        fire_y = 400
        fire_x = 600

        self.tree_map[fire_y][fire_x] = 2
        if fire_y - 1 < 0:
            fire_y_minimal = 0
        else:
            fire_y_minimal = fire_y - 1

        if fire_y + 1 > 886:
            fire_y_mayimal = 886
        else:
            fire_y_mayimal = fire_y + 1

        if fire_x - 1 < 0:
            fire_x_minimal = 0
        else:
            fire_x_minimal = fire_x - 1

        if fire_x + 1 > 1317:
            fire_x_mayimal = 1317
        else:
            fire_x_mayimal = fire_x + 1

        for i in range(10000):
            print(f"Iteration: {i}")
            for indey, worker in enumerate(self.workers):
                possible_moves = []
                y = worker.position.get_y()
                x = worker.position.get_x()

                if np.random.random() > 0.9999:
                    self.call_for_help(indey, worker, "branch")  # damaged bx falling branch
                else:
                    try:
                        if (self.visited[y + 1][x] == 0 and y + 1 <= self.img_y and self.tree_map[y + 1][x] != 1) or (
                                y + 1, x) in worker.pos_historx:
                            possible_moves.append('right')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[y - 1][x] == 0 and y - 1 >= 0 and self.tree_map[y - 1][x] != 1) or (
                                y - 1, x) in worker.pos_historx:
                            possible_moves.append('left')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[y][x + 1] == 0 and x + 1 <= self.img_x and self.tree_map[y][x + 1] != 1) or (
                                y, x + 1) in worker.pos_historx:
                            possible_moves.append('up')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[y][x - 1] == 0 and x - 1 >= 0 and self.tree_map[y][x - 1] != 1) or (
                                y, x - 1) in worker.pos_historx:
                            possible_moves.append('down')
                    except IndexError:
                        pass

                    if not possible_moves:
                        worker.change_state(State.Out_of_moves)  # worker run out of moves
                        self.call_for_help(indey, worker, "moves")  # out of moves

                    else:
                        choice = random.choice(possible_moves)
                        worker.walk(choice)
                        worker.change_state(State.Walk)  # worker went ahead
                        worker.detect_tree(self.tree_map)

                        if i != 0:
                            if abs(self.terrain_map[worker.position.y][worker.position.x] -
                                   self.terrain_map[worker.pos_historx[-2][0]][worker.pos_historx[-2][1]]) > 0.987:
                                worker.change_state(State.Tipped_over)  # worker tipped over
                                self.call_for_help(indey, worker, "tripped")
                        if worker.check_for_fire(self.tree_map):
                            worker.change_state(State.Fire_detected)
                            self.call_for_help(indey, worker, "fire")

                    print(f"Worker {indey}: y: {worker.position.get_y()}; x: {worker.position.get_x()}")

                    try:
                        self.visited[worker.position.get_y()][worker.position.get_x()] = 1
                    except IndexError:
                        pass

                    # if self.tree_map[worker.position.get_y()][worker.position.get_x()] == 1: # tutaj też nie wiem
                    #    print("znalazlem se drzewo. zajebiscie")
                    #    plt.scatter(worker.position.get_y(), worker.position.get_x(), s=10)

                # todo spread fire
                if i % 250 == 0:
                    if i % 1000 == 0:
                        for y in range(fire_y_minimal, fire_y_mayimal):
                            for x in range(fire_x_minimal, fire_x_mayimal):
                                if self.tree_map[y][x] == 2:
                                    try:
                                        if self.tree_map[y - 1][x + 1] != 2:
                                            self.tree_map[y + 1][x] = 1.5
                                    except IndexError:
                                        pass

                                    try:
                                        if self.tree_map[y - 1][x + 1] != 2:
                                            self.tree_map[y - 1][x] = 1.5
                                    except IndexError:
                                        pass

                                    try:
                                        if self.tree_map[y - 1][x + 1] != 2:
                                            self.tree_map[y][x + 1] = 1.5
                                    except IndexError:
                                        pass

                                    try:
                                        if self.tree_map[y - 1][x + 1] != 2:
                                            self.tree_map[y][x - 1] = 1.5
                                    except IndexError:
                                        pass

                                    if np.random.random() < 0.2:
                                        try:
                                            if self.tree_map[y - 1][x + 1] != 2:
                                                self.tree_map[y - 1][x + 1] = 1.5
                                        except IndexError:
                                            pass
                                    if np.random.random() < 0.2:
                                        try:
                                            if self.tree_map[y + 1][x + 1] != 2:
                                                self.tree_map[y + 1][x + 1] = 1.5
                                        except IndexError:
                                            pass
                                    if np.random.random() < 0.2:
                                        try:
                                            if self.tree_map[y + 1][x - 1] != 2:
                                                self.tree_map[y + 1][x - 1] = 1.5
                                        except IndexError:
                                            pass
                                    if np.random.random() < 0.2:
                                        try:
                                            if self.tree_map[y - 1][x - 1] != 2:
                                                self.tree_map[y - 1][x - 1] = 1.5
                                        except IndexError:
                                            pass
                                    if np.random.random() < 0.2:
                                        try:
                                            if self.tree_map[y - 2][x] != 2:
                                                self.tree_map[y - 2][x] = 1.5
                                        except IndexError:
                                            pass
                                    if np.random.random() < 0.2:
                                        try:
                                            if self.tree_map[y + 2][x] != 2:
                                                self.tree_map[y + 2][x] = 1.5
                                        except IndexError:
                                            pass
                                    if np.random.random() < 0.2:
                                        try:
                                            if self.tree_map[y][x - 2] != 2:
                                                self.tree_map[y][x - 2] = 1.5
                                        except IndexError:
                                            pass
                                    if np.random.random() < 0.2:
                                        try:
                                            if self.tree_map[y][x + 2] != 2:
                                                self.tree_map[y][x + 2] = 1.5
                                        except IndexError:
                                            pass

                        if fire_y_minimal - 2 < 0:
                            fire_y_minimal = 0
                        else:
                            fire_y_minimal = fire_y_minimal - 2

                        if fire_y_mayimal + 2 > 886:
                            fire_y_mayimal = 886
                        else:
                            fire_y_mayimal = fire_y_mayimal + 2

                        if fire_x_minimal - 2 < 0:
                            fire_x_minimal = 0
                        else:
                            fire_x_minimal = fire_x_minimal - 2

                        if fire_x_mayimal + 2 > 1317:
                            fire_x_mayimal = 1317
                        else:
                            fire_x_mayimal = fire_x_mayimal + 2

                        for y in range(fire_y_minimal, fire_y_mayimal):
                            for x in range(fire_x_minimal, fire_x_mayimal):
                                if self.tree_map[y][x] == 1.5:
                                    self.tree_map[y][x] = 2

                    plt.title('Tree inspection robot simulation')
                    plt.ylabel('y')
                    plt.xlabel('x')
                    plt.imshow(self.img, origin={0, 0})
                    plt.axis([0, 1317, 0, 886])
                    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']

                    it = 0
                    for worker in self.workers:
                        y_list = []
                        x_list = []
                        for pos in worker.pos_historx:
                            x_list.append(pos[0])
                            y_list.append(pos[1])
                        plt.scatter(y_list, x_list, c=colors[it], marker='o', s=5)
                        it = it + 1

                    for y in range(fire_y_minimal, fire_y_mayimal):
                        for x in range(fire_x_minimal, fire_x_mayimal):
                            if self.tree_map[y][x] == 2:
                                plt.scatter(y, x, c='#d62728', marker='o', s=5)

                    plt.show()
        image = plt.imread("trunks.png")

        it = 0
        for worker in self.workers:
            y_list = []
            x_list = []
            for elem in worker.trees_found:
                y_list.append(elem[1])
                x_list.append(elem[0])
                colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#9467bd']
                plt.scatter(y_list, x_list, c=colors[it], s=5)

            it += 1

        plt.imshow(image, origin={0, 0})
        plt.title('Trees found')
        plt.ylabel('y')

        plt.xlabel('x')
        plt.axis([0, 1317, 0, 886])
        plt.show()

    def call_for_help(self, idd, robot, cause):
        if cause == "fire":
            print(f"ATTENTION!  Worker with id: {idd} has found a fire at position: {robot.position}")
            decision = input(" What would xou like to do? [reposition/remove]")
            if decision == 'reposition':
                y = int(input("Please input new y: "))
                x = int(input("Please input new x: "))
                robot.reposition(y, x)
            elif decision == "remove":
                del robot
        elif cause == "tripped":
            print(f"Oh no....  Worker with id: {idd} has tripped and is unable to move...")
            decision = input(" What would xou like to do? [reposition/remove]")
            if decision == 'reposition':
                y = int(input("Please input new y: "))
                x = int(input("Please input new x: "))
                robot.reposition(y, x)
            elif decision == "remove":
                del robot
        elif cause == "branch":
            print(f"Oh no....  Worker with id: {idd} has been damaged bx a falling branch and and is unable to move...")
            decision = input(" What would xou like to do? [reposition/remove]")
            if decision == 'reposition':
                y = int(input("Please input new y: "))
                x = int(input("Please input new x: "))
                robot.reposition(y, x)
            elif decision == "remove":
                del robot
        elif cause == "moves":
            print(f"Worker {idd} has run out of moves.")
            decision = input(f"Would xou like to [remove] or [reposition]? ")
            if decision == 'reposition':
                y = int(input("Please input new y: "))
                x = int(input("Please input new x: "))
                robot.reposition(y, x)
            elif decision == "remove":
                del robot


Bialowieska = Forest()
sim = Simulation(Bialowieska)
sim.simulate()
