import arcade
from crashdetect import check_crash
from random import randint
MOVEMENT_SPEED = 8
BACKGROUND_SPEED = 4
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
        if self.x > (self.world.width-270):
            return True
        else:
            return False   

    def waysideleft(self): 
        if self.x < (self.world.width-530):
            return True
        else:
            return False   
    
            
class Enemy:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_DOWN
        self.enemylist = []
    def move(self, direction):
        self.y += MOVEMENT_SPEED * DIR_OFFSETS[direction][1]

    def hit(self, player):
        return check_crash(player.x,player.y,self.x,self.y)    

    def update(self, delta):
        self.move(self.direction)


class World:
    STATE_FROZEN = 1
    STATE_STARTED = 2
    STATE_DEAD = 3

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.state = World.STATE_FROZEN
        self.car = Car(self, 400, 60)
        self.background = Background(400,400)
        self.background2 = Background(400,1200)
        self.enemylist = []
        self.press = []
        self.score = 0
        self.millisecond = 0    

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
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return
        self.background.update(delta)
        self.background2.update(delta)
        self.car.update(delta)
        self.reuse_bg()
        self.check_enemy_car()
        self.crete_many_enemy()
        self.plusscore()
        for car in self.enemylist:  
            car.update(delta)
            if car.hit(self.car):
                self.die()
            
    def checkdirection(self):
        if self.car.direction in self.press:
            return False
        else:
            return True

    def crete_enemy(self):
        x = randint(270,530)
        y = 800
        self.enemylist.append(Enemy(self, x, y))


    def check_enemy_car(self):
        copylist = [_ for _ in self.enemylist]
        for car in copylist:
            if car.y < -30:
                self.enemylist.remove(car) 

    def crete_many_enemy(self):
        if len(self.enemylist) ==0:
            self.crete_enemy()
        elif self.enemylist[-1].y <300:
            self.crete_enemy()
       
    def reuse_bg(self):
        if self.background.y == -400:
            self.background.y = 1200
        if self.background2.y == -400:
            self.background2.y = 1200  

    def plusscore(self):
        self.millisecond += 1
        if self.millisecond == 60:
            self.score += 1
            self.millisecond = 0
                         
    
    def start(self):
        self.state = World.STATE_STARTED

    def freeze(self):
        self.state = World.STATE_FROZEN     

    def is_started(self):
        return self.state == World.STATE_STARTED 

    def die(self):
        self.state = World.STATE_DEAD
 
    def is_dead(self):
        return self.state == World.STATE_DEAD    

class Background:
    def __init__(self,x,y):
        self.x = x 
        self.y = y
    
    def update(self,delta):
        self.y = self.y - BACKGROUND_SPEED

        
                



    

   