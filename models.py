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
            arcade.key.RIGHT: DIR_RIGHT,
            }
 
DIR_OFFSETS = { DIR_STILL: (0,0),
                DIR_UP: (0,1),
                DIR_RIGHT: (1,0),
                DIR_DOWN: (0,-1),
                DIR_LEFT: (-1,0) }

class Background:
    def __init__(self,x,y):
        self.x = x 
        self.y = y
    
    def update(self,speed,delta):
        self.y = self.y - (BACKGROUND_SPEED)
            
class Car():
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_STILL
        self.next_direction = DIR_STILL

    def move(self, direction,speed):
        self.x += (MOVEMENT_SPEED+speed) * DIR_OFFSETS[direction][0]  

    def update(self, delta): 
        self.wayside()

    def wayside(self):
        # if self.x > (self.world.width-270):
        #     if len(self.world.press) != 0 and self.world.press[-1] == DIR_RIGHT:
        #         self.direction = DIR_STILL
        #     elif len(self.world.press) != 0  and self.world.press[-1] == DIR_LEFT: 
        #         self.next_direction = DIR_LEFT
        #         self.direction = DIR_LEFT

        # elif self.x < (self.world.width-530):
        #     if len(self.world.press) != 0 and self.world.press[-1] == DIR_LEFT:
        #         self.direction = DIR_STILL
        #     elif len(self.world.press) != 0  and self.world.press[-1] == DIR_RIGHT: 
        #         self.next_direction = DIR_RIGHT
        #             self.direction = DIR_RIGHT
        #     else:
        #                 
        #     self.move(self.direction,self.world.morespeed)       
        if self.world.width-530 < self.x < self.world.width-270:
            self.direction = self.next_direction
            self.move(self.direction,self.world.morespeed)
        else:
            self.direction = self.next_direction
            if self.x > self.world.width//2 and self.direction == DIR_LEFT:
                self.move(self.direction,self.world.morespeed)
            elif self.x < self.world.width//2 and self.direction == DIR_RIGHT:
                self.move(self.direction,self.world.morespeed)
          

            
class Enemy:
    def __init__(self, world, x, y):
        self.world = world
        self.x = x
        self.y = y
        self.direction = DIR_DOWN
        self.enemylist = []
    def move(self, direction,speed):
        self.y += (MOVEMENT_SPEED+speed) * DIR_OFFSETS[direction][1]

    def hit(self, player):
        return check_crash(player.x,player.y,self.x,self.y)    

    def update(self, delta):
        self.move(self.direction,self.world.morespeed)


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
        self.morespeed = 0


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
                elif self.car.direction == DIR_RIGHT:
                    self.car.next_direction = DIR_LEFT
        # if key == arcade.key.LEFT:
        #     self.next_direction = DIR_LEFT
        # elif key == arcade.key.RIGHT:
        #     self.next_direction = DIR_RIGHT
        # else:
        #     self.next_direction = DIR_STILL
    

    def update(self, delta):
        if self.state in [World.STATE_FROZEN, World.STATE_DEAD]:
            return
        self.background.update(self.morespeed,delta)
        self.background2.update(self.morespeed,delta)
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
        if self.background.y <= -400:
            self.background.y = 1200
        if self.background2.y <= -400:
            self.background2.y = 1200  

    def plusscore(self):
        self.millisecond += 1
        if self.millisecond == 60:
            self.score += 1
            self.millisecond = 0
            self.plusspeed()

    def plusspeed(self):
        self.morespeed += 0.2       
                         
    
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


                



    

   