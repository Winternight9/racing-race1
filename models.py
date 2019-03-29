import arcade
from random import randint
MOVEMENT_SPEED = 4
DIR_STILL = 0
DIR_UP = 1
DIR_RIGHT = 2
DIR_DOWN = 3
DIR_LEFT = 4

KEY_MAP = { arcade.key.UP: DIR_UP,
            arcade.key.DOWN: DIR_DOWN,
            arcade.key.LEFT: DIR_LEFT,
            arcade.key.RIGHT: DIR_RIGHT, }
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_UP: (0,1),
                DIR_RIGHT: (1,0),
                DIR_DOWN: (0,-1),
                DIR_LEFT: (-1,0) }

    
class Car():
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.next_direction = DIR_STILL

    def move(self, direction):
        self.x += MOVEMENT_SPEED * DIR_OFFSETS[direction][0]  

    def update(self, delta): 
        if self.waysideright():
            self.direction = DIR_STILL
            if self.next_direction == DIR_LEFT:
                self.direction = DIR_LEFT
        elif self.waysideleft():
            self.direction = DIR_STILL
            if self.next_direction == DIR_RIGHT:
                self.direction = DIR_RIGHT
        else:
            self.direction = self.next_direction        

        self.move(self.direction)

    def waysideright(self):
        if self.x > (self.world.width-250):
            return True
        else:
            return False   

    def waysideleft(self): 
        if self.x < (self.world.width-550):
            return True
        else:
            return False   
    
            
class Enemy:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_DOWN
    def move(self, direction):
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    def update(self, delta):
        self.move(self.direction)           

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.car = Car(self, 400, 50)
        self.enemycar = Enemy(self,randint(250,550),600)    
        self.press = []
    def on_key_press(self, key, key_modifiers): 
        if key in KEY_MAP:
            self.car.next_direction = KEY_MAP[key]
            self.press.append(KEY_MAP[key])    

    def on_key_release(self, key, key_modifiers):
        if key in KEY_MAP:
            self.press.remove(KEY_MAP[key])
            if self.press == []:
                self.car.next_direction = DIR_STILL
            elif self.checkdirection():
                if self.car.direction == DIR_LEFT:
                    self.car.next_direction = DIR_RIGHT
                else:
                    self.car.next_direction = DIR_LEFT

    def update(self, delta):
        self.car.update(delta)
        self.enemycar.update(delta)    

    def checkdirection(self):
        if self.car.direction in self.press:
            return False
        else:
            return True