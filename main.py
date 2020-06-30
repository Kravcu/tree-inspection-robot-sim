import random
from enum import Enum
from typing import List

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
        self.forest_data = plt.imread("trunks.png")
        self.rows = len(self.forest_data)
        self.cols = len(self.forest_data[0])
        
        for x in range(5,self.rows-5): # powalanie drzew, dla uproszczenie 8 kierunków
            for y in range(5,self.cols-5):
                if self.forest_data == 1:
                    if np.random.random() > 0.999:
                        direction = np.random.randint(0,8);
                        if direction == 0:
                            self.forest_data[x-1][y] = 0.5
                            self.forest_data[x-2][y] = 0.5
                            self.forest_data[x-3][y] = 0.5
                            self.forest_data[x-4][y] = 0.5
                            self.forest_data[x-5][y] = 0.5
                        elif direction == 1:
                            self.forest_data[x-1][y+1] = 0.5
                            self.forest_data[x-2][y+2] = 0.5
                            self.forest_data[x-3][y+3] = 0.5
                        elif direction == 2:
                            self.forest_data[x][y+1] = 0.5
                            self.forest_data[x][y+2] = 0.5
                            self.forest_data[x][y+3] = 0.5
                            self.forest_data[x][y+4] = 0.5
                            self.forest_data[x][y+5] = 0.5
                        elif direction == 3:
                            self.forest_data[x+1][y+1] = 0.5
                            self.forest_data[x+2][y+2] = 0.5
                            self.forest_data[x+3][y+3] = 0.5
                        elif direction == 4:
                            self.forest_data[x+1][y] = 0.5
                            self.forest_data[x+2][y] = 0.5
                            self.forest_data[x+3][y] = 0.5
                            self.forest_data[x+4][y] = 0.5
                            self.forest_data[x+5][y] = 0.5
                        elif direction == 5:
                            self.forest_data[x+1][y-1] = 0.5
                            self.forest_data[x+2][y-2] = 0.5
                            self.forest_data[x+3][y-3] = 0.5
                        elif direction == 6:
                            self.forest_data[x][y-1] = 0.5
                            self.forest_data[x][y-2] = 0.5
                            self.forest_data[x][y-3] = 0.5
                            self.forest_data[x][y-4] = 0.5
                            self.forest_data[x][y-5] = 0.5
                        else:
                            self.forest_data[x-1][y-1] = 0.5
                            self.forest_data[x-2][y-2] = 0.5
                            self.forest_data[x-3][y-3] = 0.5
                          
        for x in range(self.rows):
            for y in range(self.cols):
                if self.forest_data == 0.5:
                    self.forest_data = 1
                    
        self.raw_tree_data = self.forest_data

        for x in range(self.rows):
            for y in range(self.cols):
                if self.forest_data[x][y]!= 1:
                    self.forest_data[x][y] = np.random.normal(0.0,2) # rozklad gaussa, rodek 0.0, zróżicowanie terenu
    
    def get_tree_map(self):
        return self.raw_tree_data
    
    def get_terrain_map(self):
        return self.forest_data
    
    
    
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

    def __init__(self, tree_map : Forest , x_pos=0, y_pos=0, y_max_pos=886, x_max_pos=1317):
        self.position = Position(x_pos, y_pos)
        self.pos_history: List[Position] = []
        self.x_max_pos = x_max_pos
        self.y_max_pos = y_max_pos
        self.current_state : State = 0; 

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
    
    def check_for_fire(self, tree_map_) -> bool: # to do 
        try:
            if tree_map_[self.Position.x-1][self.Position.y-1] == 2 :
                self.change_state(2)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.Position.x][self.Position.y-1] == 2 :
                self.change_state(2)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.Position.x+1][self.Position.y-1] == 2 :
                self.change_state(2)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.Position.x+1][self.Position.y] == 2 :
                self.change_state(2)
                return True
        except IndexError:
            pass
        try:    
            if tree_map_[self.Position.x+1][self.Position.y+1] == 2 :
                self.change_state(2)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.Position.x][self.Position.y+1] == 2 :
                self.change_state(2)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.Position.x-1][self.Position.y+1] == 2 :
                self.change_state(2)
                return True
        except IndexError:
            pass
        try:
            if tree_map_[self.Position.x-1][self.Position.y] == 2 :
                self.change_state(2)
                return True
        except IndexError:
            pass
        
        return False
    ##

    #def detect_tree(self): ## todo
    #    if self.tree_map[self.position.get_x()][self.position.get_y()] == 1:
    #        return True
    #    else:
    #        return False
    
    
    def change_state(self, state : State):
        self.current_state = State 


class Simulation:
    def __init__(self, tree_map: Forest):
        self.img = plt.imread('forest.png')
        self.tree_map = tree_map.get_tree_map()
        self.terrain_map = tree_map.get_terrain_map()

        img_x, img_y = len(self.img[0]), len(self.img)
        self.visited = [[0 for x in range(img_x)] for y in range(img_y)]
        plt.imshow(self.img, origin={0, 0})

        self.workers: List[Robot] = [Robot(np.random.rand(img_x, img_y), 430, 430),
                                     Robot(np.random.rand(img_x, img_y), 800, 430)]
        
        # todo initiate fire
        fire_x_limit = len(self.tree_map)
        fire_y_limit = len(self.tree_map[0])
        
        fire_x = np.random.randint(fire_x_limit)
        fire_y = np.random.randint(fire_y_limit)
        
        self.tree_map[fire_x][fire_y] = 2
        
        
        for i in range(10000):
            workers_to_remove = []
            for index, worker in enumerate(self.workers):
                possible_moves = []
                x = worker.position.get_x()
                y = worker.position.get_y()
                
                if worker.check_for_fire(self.tree_map):
                        worker.change_state(2)
                        #todo wezwij pomoc ogień 
                
                if random.randint(0, 100) < 2:
                    print(f"Worker {index} został zniszczony przez studia na AGH.")
                    decision = input("would you like to [remove] or [reposition]? ")
                    decision = input(f"Would you like to [remove] or [reposition]? ")
                    if decision == "remove":
                        workers_to_remove.append(index) #nie jestem pewny logiki tutaj, może po prostu zrobimy replace(wstawienie nowego na jego miejsce) albo pickup (remove)
                    elif decision == "reposition":
                        x = int(input("Please put new X pos "))
                        y = int(input("Please put new Y pos "))
                        self.workers[index].position.reposition(x, y)
                else:
                    try:
                        if (self.visited[x + 1][y] == 0 and x + 1 <= img_x and self.tree_map[x+1][y] != 1) or (x + 1, y) in worker.pos_history:
                            possible_moves.append('right')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[x - 1][y] == 0 and x - 1 >= 0 and self.tree_map[x-1][y] != 1) or (x - 1, y) in worker.pos_history:
                            possible_moves.append('left')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[x][y + 1] == 0 and y + 1 <= img_y and self.tree_map[x][y+1] != 1) or (x, y + 1) in worker.pos_history:
                            possible_moves.append('up')
                    except IndexError:
                        pass
                    try:
                        if (self.visited[x][y - 1] == 0 and y - 1 >= 0 and self.tree_map[x][y-1] != 1) or (x, y - 1) in worker.pos_history:
                            possible_moves.append('down')
                    except IndexError:
                        pass

                    if not possible_moves:
                        print(f"Worker {index} has run out of moves.")
                        decision = input(f"Would you like to [remove] or [reposition]? ")                        
                        self.workers[index].change_state(4) # worker run out of moves
                        
                        if decision == "remove":
                            workers_to_remove.append(index)
                        elif decision == "reposition":
                            x = int(input("Please put new X pos "))
                            y = int(input("Please put new Y pos "))
                            self.workers[index].position.reposition(x, y)
                            worker.change_state(1)
                    else:
                        choice = random.choice(possible_moves)
                        self.workers[index].walk(choice)
                        self.workers[index].change_state(1) # worker went ahead
                        if abs(self.terrain_map[worker.position.x][worker.position.y] -  self.terrain_map[worker.pos_history[-2].x][worker.pos_history[-2].y]) >= 0.4:
                            worker.change_state(3) # worker tipped over
                            #todo wezwij pomoc
                    if worker.check_for_fire(self.tree_map):
                        worker.change_state(2)
                        # todo wezwij pomoc - ogień
                        
                    self.visited[worker.position.get_x()][worker.position.get_y()] = 1
                    
                    #if self.tree_map[worker.position.get_x()][worker.position.get_y()] == 1: # tutaj też nie wiem 
                    #    print("znalazlem se drzewo. zajebiscie")
                    #    plt.scatter(worker.position.get_x(), worker.position.get_y(), s=10)
                
                for elem in workers_to_remove:
                    self.workers.remove(elem)
                # todo spread fire
                tree_map_helper = self.tree_map
                
                for x in range(fire_x_limit):
                    for y in range(fire_y_limit):
                        if self.tree_map[x][y] == 2:
                            if np.random.random() > 0.5:
                                try:
                                    self.tree_map_helper[x+1][y] = 2
                                except IndexError:
                                    pass
                                try:
                                    self.tree_map_helper[x-1][y] = 2
                                except IndexError:
                                    pass
                                try:
                                    self.tree_map_helper[x][y+1] = 2
                                except IndexError:
                                    pass
                                try:
                                    self.tree_map_helper[x][y-1] = 2
                                except IndexError:
                                    pass
                                
                for x in range(fire_x_limit):
                    for y in range(fire_y_limit):
                        if self.tree_map_helper[x][y] == 2:
                            self.tree_map[x][y] = 2
                
        # TODO add dynamic plotting of workers position
        plt.scatter(worker.position.get_x(), worker.position.get_y(), s=5)
        plt.title('Tree inspection robot simulation')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()


img = plt.imread('forest.png')
Bialowieska =Forest
img_x, img_y = len(img[0]), len(img)
sim = Simulation(Forest)
