import arcade
import sys
from playsound import playsound
from models import World, Car, Enemy
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Racing_Race'

routes = {
    'menu':0,
    'game':1,
    'car':2,
    'exit':3,
}

choices = {
    0: 'game',
    1: 'car',
    2: 'exit'
}

Car = {0: 'images/redcar3.png',
        1: 'images/redcar.png',
        2: 'images/pinkcar.png',
        3: 'images/greencar.png',
        4: 'images/Enemycar2.png',
        5: 'images/Enemycarwhite.png',
        6: 'images/lambo.png'
}

class Fpscounter:
    def __init__(self):
        import time
        import collections
        self.time = time.perf_counter
        self.frametime = collections.deque(maxlen=60)
        self.t = self.time()

    def tick(self):
        t = self.time()
        dt = t-self.t 
        self.frametime.append(dt)
        self.t = t   

    def fps(self):
        try:
            return 60/sum(self.frametime)
        except ZeroDivisionError:
            return 0


class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)

        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
 
    def draw(self):
        self.sync_with_model()
        super().draw()


class MenuChoiceSprite(arcade.AnimatedTimeSprite):
    def __init__(self, *args, **kwargs):
        self.is_select = False

        super().__init__(*args, **kwargs)

    def select(self):
        self.is_select = True

    def unselect(self):
        self.is_select = False


class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        self.current_route = routes['menu']
        self.selecting_choice = 0
        self.car_choice = 1
        self.background = arcade.load_texture("images/Background.png")
        self.cartexture = Car[self.car_choice]
        self.menu_setup()
        self.car_setup()
        self.game_setup(width,height)

    def menu_setup(self):
        self.choice_list = arcade.SpriteList()

        self.start = MenuChoiceSprite()
        self.start.textures.append(arcade.load_texture("images/start.png"))
        self.start.textures.append(arcade.load_texture("images/start1.png"))
        self.start.set_texture(0)
        self.start.texture_change_frames = 10

        self.car = MenuChoiceSprite()
        self.car.textures.append(arcade.load_texture("images/car.png"))
        self.car.textures.append(arcade.load_texture("images/car1.png"))
        self.car.set_texture(1)
        self.car.texture_change_frames = 10

        self.exit = MenuChoiceSprite()
        self.exit.textures.append(arcade.load_texture("images/exit.png"))
        self.exit.textures.append(arcade.load_texture("images/exit1.png"))
        self.exit.set_texture(1)
        self.exit.texture_change_frames = 10

        self.start.center_x,self.start.center_y = self.width//2,self.height//2 +50
        self.car.center_x,self.car.center_y = self.width//2,self.height//2 -20
        self.exit.center_x,self.exit.center_y = self.width//2,self.height//2 -90
        
        self.start.select()
        self.choice_list.append(self.start)
        self.choice_list.append(self.car)
        self.choice_list.append(self.exit)

    def car_setup(self):
        self.car_choice_list = arcade.SpriteList()
        self.car_show = arcade.Sprite(Car[self.car_choice])
        self.car_show.set_position(self.width//2,self.height//2 +50)

    def game_setup(self, width, height):
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background_sprite = ModelSprite("images/Background.png",
                                      model=self.world.background)
        self.background_sprite2 = ModelSprite("images/Background.png",
                                      model=self.world.background2)                              
        self.car_sprite = ModelSprite(self.cartexture,
                                      model=self.world.car)
        self.enemylist = []                              
        self.fpscounter = Fpscounter()
        self.set_update_rate(1/70)
    
    def car_sprite_selected(self):
        self.car_sprite = ModelSprite(self.cartexture,
                                      model=self.world.car)

    def draw_menu(self):
        self.choice_list.draw()

    def draw_car_menu(self):
        self.car_show.draw()                                  
        
    def update(self, delta):
        if self.current_route == routes['menu']:
            for choice in self.choice_list:
                if choice.is_select == True:
                    choice.update()
                    choice.update_animation()
                   
        elif self.current_route == routes['car']:
            self.draw_car_menu()

        elif self.current_route == routes['exit']:
            sys.exit()    

        elif self.current_route == routes['game']:
            self.creteenemy()
            self.update_enemylist()
            self.world.update(delta)
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.width//2 , self.height//2 ,self.width, self.height,self.background)

        if self.current_route == routes['menu']:
            self.draw_menu()  

        elif self.current_route == routes['car']:
            self.car_setup()
            self.draw_car_menu()    
       
        elif self.current_route == routes['game']:
            self.car_sprite_selected()
            self.background_sprite.draw()
            self.background_sprite2.draw()
            self.car_sprite.draw()
            self.fpscounter.tick()
            self.check_state()

            fps = f"fps{self.fpscounter.fps():.2f}"
            score = f"Score {self.world.score}"
            arcade.draw_text(score,670,770,arcade.color.DARK_CANDY_APPLE_RED,24)
            arcade.draw_text(fps,750,560,arcade.color.BLACK)
            for enemy in self.enemylist:
                enemy.draw()
            
    def update_selected_choice(self):
        for choice in self.choice_list:
            choice.unselect()
            choice.set_texture(1)
        self.choice_list[self.selecting_choice].select()    

    def on_key_press(self, key, key_modifiers):
        if self.current_route == routes['menu']:
            if key == arcade.key.DOWN:
                if self.selecting_choice < 2:
                    self.selecting_choice += 1
                else:
                    self.selecting_choice = 0
                self.update_selected_choice()
                press_sound = arcade.load_sound("soundtrack/pressmusic.wav")
                arcade.play_sound(press_sound)
                
            elif key == arcade.key.UP:
                if self.selecting_choice > 0 :  
                    self.selecting_choice -= 1
                else:
                    self.selecting_choice = 2
                self.update_selected_choice()
                press_sound = arcade.load_sound("soundtrack/pressmusic.wav")
                arcade.play_sound(press_sound)        
            elif key == arcade.key.ENTER:
                self.current_route = routes[choices[self.selecting_choice]]

        elif self.current_route == routes['car']:
            if key == arcade.key.RIGHT:
                if self.car_choice < 6:
                    self.car_choice += 1
                else:
                    self.car_choice = 0    
            
            elif key == arcade.key.LEFT:
                if self.car_choice > 0:
                    self.car_choice -= 1
                else:
                    self.car_choice = 4
            elif key == arcade.key.ENTER:
                self.cartexture = Car[self.car_choice]
                self.current_route = routes['menu']
                
        elif self.current_route == routes['game']:
            self.world.on_key_press(key, key_modifiers)
            if not self.world.is_dead():
                self.world.start()       
            elif key == arcade.key.R and self.world.state == World.STATE_DEAD:
                self.game_setup(SCREEN_WIDTH,SCREEN_HEIGHT)

            elif key == arcade.key.M and self.world.state == World.STATE_DEAD:
                self.current_route = routes['menu']
                self.draw_menu()
                self.game_setup(SCREEN_WIDTH,SCREEN_HEIGHT)

    def on_key_release(self, key, key_modifiers):
        if self.current_route == routes['game']:
            self.world.on_key_release(key, key_modifiers)

    def creteenemy(self):
        for enemy in self.world.enemylist:
            if enemy in (enemy_sprite.model for enemy_sprite in self.enemylist):
                pass
            else:
                self.enemylist.append(ModelSprite(self.randomsprite(), 
                model=enemy))
   
    def randomsprite(self):
        enemyspritelist = ['images/EnemyCar2.png','images/Enemycarwhite.png','images/redcar.png','images/pinkcar.png']
        randomnum = randint(0,3)
        return enemyspritelist[randomnum]

    def update_enemylist(self):
        for enemy_sprite in [_ for _ in self.enemylist]:
            if enemy_sprite.model not in self.world.enemylist:
                self.enemylist.remove(enemy_sprite)

    def draw_game_over(self):
        output = f"Score {self.world.score}"
        arcade.draw_text(output, 285, 500, arcade.color.BALL_BLUE, 54)
        
        output = "Game Over"
        arcade.draw_text(output, 225, 400, arcade.color.BALL_BLUE, 54)

        output = "Press R to restart"
        arcade.draw_text(output, 280, 300, arcade.color.BALL_BLUE, 24)

        output = "Press M to mainmenu"
        arcade.draw_text(output,250,230,arcade.color.BALL_BLUE, 24)

    def check_state(self):
        if self.world.state == World.STATE_DEAD:
            self.draw_game_over()        

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()

if __name__ == "__main__":
    main()        
 

