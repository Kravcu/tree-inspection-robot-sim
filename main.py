import random
from enum import Enum
from typing import *

import matplotlib.pyplot as plt
import numpy as np
import copy


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

        for x in range(5, self.rows - 5):  # powalanie drzew, dla uproszczenie 8 kierunków
            for y in range(5, self.cols - 5):
                if self.forest_data[x][y] == 1:
                    if np.random.random() > 0.999:
                        direction = np.random.randint(0, 8)
                        if direction == 0:
                            self.forest_data[x - 1][y] = 0.5
                            self.forest_data[x - 2][y] = 0.5
                            self.forest_data[x - 3][y] = 0.5
                            self.forest_data[x - 4][y] = 0.5
                            self.forest_data[x - 5][y] = 0.5
                        elif direction == 1:
                            self.forest_data[x - 1][y + 1] = 0.5
                            self.forest_data[x - 2][y + 2] = 0.5
                            self.forest_data[x - 3][y + 3] = 0.5
                        elif direction == 2:
                            self.forest_data[x][y + 1] = 0.5
                            self.forest_data[x][y + 2] = 0.5
                            self.forest_data[x][y + 3] = 0.5
                            self.forest_data[x][y + 4] = 0.5
                            self.forest_data[x][y + 5] = 0.5
                        elif direction == 3:
                            self.forest_data[x + 1][y + 1] = 0.5
                            self.forest_data[x + 2][y + 2] = 0.5
                            self.forest_data[x + 3][y + 3] = 0.5
                        elif direction == 4:
                            self.forest_data[x + 1][y] = 0.5
                            self.forest_data[x + 2][y] = 0.5
                            self.forest_data[x + 3][y] = 0.5
                            self.forest_data[x + 4][y] = 0.5
                            self.forest_data[x + 5][y] = 0.5
                        elif direction == 5:
                            self.forest_data[x + 1][y - 1] = 0.5
                            self.forest_data[x + 2][y - 2] = 0.5
                            self.forest_data[x + 3][y - 3] = 0.5
                        elif direction == 6:
                            self.forest_data[x][y - 1] = 0.5
                            self.forest_data[x][y - 2] = 0.5
                            self.forest_data[x][y - 3] = 0.5
                            self.forest_data[x][y - 4] = 0.5
                            self.forest_data[x][y - 5] = 0.5
                        else:
                            self.forest_data[x - 1][y - 1] = 0.5
                            self.forest_data[x - 2][y - 2] = 0.5
                            self.forest_data[x - 3][y - 3] = 0.5

        for x in range(self.rows):
            for y in range(self.cols):
                if self.forest_data[x][y] == 0.5:
                    self.forest_data[x][y] = 1

        self.raw_tree_data = copy.deepcopy(self.forest_data)

        for x in range(self.rows):
            for y in range(self.cols):
                if self.forest_data[x][y] != 1:
                    self.forest_data[x][y] = np.random.random()-0.5 # rozklad gaussa, rodek 0.0, zróżicowanie terenu

    def get_tree_map(self) -> np.ndarray:
        return self.raw_tree_data

    def get_terrain_map(self) -> np.ndarray:
        return self.forest_data


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

    def __str__(self):
        return f"x={self.x},y={self.y}"


class Robot:

    def __init__(self, x_pos=0, y_pos=0, y_max_pos=886, x_max_pos=1317):
        self.position: Position = Position(x_pos, y_pos)
        self.pos_history: List[Tuple(float, float)] = []
        self.x_max_pos: float = x_max_pos
        self.y_max_pos: float = y_max_pos
        self.current_state: State = State.Init
        self.trees_found = np.empty((y_max_pos, x_max_pos))

    def walk(self, direction):
        if direction == "left":
            self.position.move_left()
        elif direction == "right":
            self.position.move_right()
        elif direction == "up":
            self.position.move_up()
        elif direction == "down":
            self.position.move_down()
        self.pos_history.append(self.position.get_pos())

    def check_for_fire(self, tree_map_) -> bool:  # to do
        try:
            if tree_map_[self.position.x - 1][self.position.y - 1] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.x][self.position.y - 1] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.x + 1][self.position.y - 1] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.x + 1][self.position.y] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.x + 1][self.position.y + 1] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.x][self.position.y + 1] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.x - 1][self.position.y + 1] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.position.x - 1][self.position.y] == 2:
                self.change_state(State.Fire_detected)
                return True
        except IndexError:
            pass

        return False

    def reposition(self, x, y):
        self.position = Position(x, y)
        self.change_state(State.Walk)

    ##

    def detect_tree(self, tree_map):  # todo
        if tree_map[self.position.get_x()][self.position.get_y()] == 1:
            self.trees_found[self.position.get_x()][self.position.get_y()] = 1
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

        self.img_x, self.img_y = len(self.img[0]), len(self.img)
        self.visited = [[0 for x in range(self.img_x)] for y in range(self.img_y)]
        plt.imshow(self.img, origin={0, 0})

        self.workers: List[Robot] = [Robot(430, 1300),
                                     Robot(800, 430),
                                     Robot(800, 1000),
                                     Robot(0, 100)]
        
    def simulate(self):
        fire_x_limit = len(self.tree_map) - 1
        fire_y_limit = len(self.tree_map[0]) - 1

        #fire_x = np.random.randint(fire_x_limit)
        #fire_y = np.random.randint(fire_y_limit)
        fire_x = 500
        fire_y = 500

        self.tree_map[fire_x][fire_y] = 2
        if fire_x - 1 < 0:
            fire_x_minimal = 0
        else:
            fire_x_minimal = fire_x - 1

        if fire_x + 1 > 886:
            fire_x_maximal = 886
        else:
            fire_x_maximal = fire_x + 1

        if fire_y - 1 < 0:
            fire_y_minimal = 0
        else:
            fire_y_minimal = fire_y - 1

        if fire_y + 1 > 1317:
            fire_y_maximal = 1317
        else:
            fire_y_maximal = fire_y + 1
        
        
        for i in range(30):
            print(f"Iteration: {i}")
            for index, worker in enumerate(self.workers):
                possible_moves = []
                x = worker.position.get_x()
                y = worker.position.get_y()

                if np.random.random() > 0.9999:
                    self.call_for_help(index, worker, "branch")  # damaged by falling branch
                else:
                    try:
                        if (self.visited[x + 1][y] == 0 and x + 1 <= self.img_x and self.tree_map[x + 1][y] != 1) or (
                                x + 1, y) in worker.pos_history:
                            possible_moves.append('right')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[x - 1][y] == 0 and x - 1 >= 0 and self.tree_map[x - 1][y] != 1) or (
                                x - 1, y) in worker.pos_history:
                            possible_moves.append('left')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[x][y + 1] == 0 and y + 1 <= self.img_y and self.tree_map[x][y + 1] != 1) or (
                                x, y + 1) in worker.pos_history:
                            possible_moves.append('up')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[x][y - 1] == 0 and y - 1 >= 0 and self.tree_map[x][y - 1] != 1) or (
                                x, y - 1) in worker.pos_history:
                            possible_moves.append('down')
                    except IndexError:
                        pass

                    if not possible_moves:
                        worker.change_state(State.Out_of_moves)  # worker run out of moves
                        self.call_for_help(index, worker, "moves")  # out of moves

                    else:
                        choice = random.choice(possible_moves)
                        worker.walk(choice)
                        worker.change_state(State.Walk)  # worker went ahead
                        
                        if i!=0:
                            if abs(self.terrain_map[worker.position.x][worker.position.y] -
                                   self.terrain_map[worker.pos_history[-2][0]][worker.pos_history[-2][1]]) > 0.987:
                                worker.change_state(State.Tipped_over)  # worker tipped over
                                self.call_for_help(index, worker, "tripped")
                        if worker.check_for_fire(self.tree_map):
                            worker.change_state(State.Fire_detected)
                            self.call_for_help(index, worker, "fire")
                            
                    print(f"Worker {index}: X: {worker.position.get_x()}; Y: {worker.position.get_y()}")
                    
                    try:
                        self.visited[worker.position.get_x()][worker.position.get_y()] = 1
                    except IndexError:
                        pass

                    # if self.tree_map[worker.position.get_x()][worker.position.get_y()] == 1: # tutaj też nie wiem
                    #    print("znalazlem se drzewo. zajebiscie")
                    #    plt.scatter(worker.position.get_x(), worker.position.get_y(), s=10)

                # todo spread fire
                tree_map_helper = self.tree_map
                if i%50 == 0:
                    for x in range(fire_x_minimal,fire_x_maximal):
                        for y in range(fire_y_minimal,fire_y_maximal):
                            if self.tree_map[x][y] == 2:
                                try:
                                    if self.tree_map[x-1][y+1] != 2:
                                        self.tree_map[x + 1][y] = 1.5
                                except IndexError:
                                    pass
                                
                                try:
                                    if self.tree_map[x-1][y+1] != 2:
                                        self.tree_map[x - 1][y] = 1.5
                                except IndexError:
                                    pass
                                    
                                try:
                                    if self.tree_map[x-1][y+1] != 2:
                                        self.tree_map[x][y + 1] = 1.5
                                except IndexError:
                                    pass
                                    
                                try:
                                    if self.tree_map[x-1][y+1] != 2:
                                        self.tree_map[x][y - 1] = 1.5
                                except IndexError:
                                    pass
                                
                                if np.random.random <0.2:
                                    try:
                                        if self.tree_map[x-1][y+1] != 2:
                                            self.tree_map[x-1][y+1] = 1.5
                                    except IndexError:
                                        pass
                                if np.random.random <0.2:
                                    try:
                                        if self.tree_map[x+1][y+1] != 2:
                                            self.tree_map[x+1][y+1] = 1.5
                                    except IndexError:
                                        pass
                                if np.random.random <0.2:
                                    try:
                                        if self.tree_map[x+1][y-1] != 2:
                                            self.tree_map[x+1][y-1] = 1.5
                                    except IndexError:
                                        pass
                                if np.random.random <0.2:
                                    try:
                                        if self.tree_map[x-1][y-1] != 2:
                                            self.tree_map[x-1][y-1] = 1.5
                                    except IndexError:
                                        pass
                                if np.random.random <0.2:
                                    try:
                                        if self.tree_map[x-2][y] != 2:
                                            self.tree_map[x-2][y] = 1.5
                                    except IndexError:
                                        pass
                                if np.random.random <0.2:
                                    try:
                                        if self.tree_map[x+2][y] != 2:
                                            self.tree_map[x+2][y] = 1.5
                                    except IndexError:
                                        pass
                                if np.random.random <0.2:
                                    try:
                                        if self.tree_map[x][y-2] != 2:
                                            self.tree_map[x][y-2] = 1.5
                                    except IndexError:
                                        pass
                                if np.random.random <0.2:
                                    try:
                                        if self.tree_map[x][y+2] != 2:
                                            self.tree_map[x][y+2] = 1.5
                                    except IndexError:
                                        pass
                                    
 
                    if fire_x_minimal - 2 < 0:
                        fire_x_minimal = 0
                    else:
                        fire_x_minimal = fire_x_minimal - 1

                    if fire_x_maximal + 2 > 886:
                        fire_x_maximal = 886
                    else:
                        fire_x_maximal = fire_x_maximal + 1
                    
                    if fire_y_minimal - 2 < 0:
                        fire_y_minimal = 0
                    else:
                        fire_y_minimal = fire_y_minimal - 1
                    
                    if fire_y_maximal + 2 > 1317:
                        fire_y_maximal = 1317
                    else:
                        fire_y_maximal = fire_y_maximal + 1               

                    for x in range(fire_x_minimal,fire_x_maximal):
                        for y in range(fire_y_minimal,fire_y_maximal):
                            if self.tree_map[x][y] == 1.5:
                                self.tree_map[x][y] = 2
                                
            # TODO add dynamic plotting of workers position
            # TODO add dynamic plotting of workers position
            # plt.title('Tree inspection robot simulation')
            # plt.xlabel('x')
            # plt.ylabel('y')
            # plt.imshow(self.img, origin={0, 0})
            # for worker in self.workers:
            #     plt.axis([0, 1317, 0, 886])
            #     plt.scatter(worker.position.get_x(), worker.position.get_y())
            # plt.show()
        
        plt.imshow(self.img, origin={0, 0})
        colors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728']
        it = 0
        for worker in self.workers:
            for pos in worker.pos_history:
                plt.scatter(pos[1],pos[0],c=colors[it])
            it = it+1
                
        plt.title("Inspected")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()

    def call_for_help(self, idd, robot, cause):
        if cause == "fire":
            print(f"ATTENTION!  Worker with id: {idd} has found a fire at position: {robot.position}")
            decision = input(" What would you like to do? [reposition/remove]")
            if decision == 'reposition':
                x = int(input("Please input new X: "))
                y = int(input("Please input new Y: "))
                robot.reposition(x, y)
            elif decision == "remove":
                del robot
        elif cause == "tripped":
            print(f"Oh no....  Worker with id: {idd} has tripped and is unable to move...")
            decision = input(" What would you like to do? [reposition/remove]")
            if decision == 'reposition':
                x = int(input("Please input new X: "))
                y = int(input("Please input new Y: "))
                robot.reposition(x, y)
            elif decision == "remove":
                del robot
        elif cause == "branch":
            print(f"Oh no....  Worker with id: {idd} has been damaged by a falling branch and and is unable to move...")
            decision = input(" What would you like to do? [reposition/remove]")
            if decision == 'reposition':
                x = int(input("Please input new X: "))
                y = int(input("Please input new Y: "))
                robot.reposition(x, y)
            elif decision == "remove":
                del robot
        elif cause == "moves":
            print(f"Worker {idd} has run out of moves.")
            decision = input(f"Would you like to [remove] or [reposition]? ")
            if decision == 'reposition':
                x = int(input("Please input new X: "))
                y = int(input("Please input new Y: "))
                robot.reposition(x, y)
            elif decision == "remove":
                del robot


Bialowieska = Forest()
sim = Simulation(Bialowieska)
sim.simulate()


