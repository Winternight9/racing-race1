import arcade
from models import World, Car, Enemy
from random import randint

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Racing_Race'

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


class MyGame(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)

        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.background_sprite = ModelSprite("Background.png",
                                      model=self.world.background)
        self.background_sprite2 = ModelSprite("Background.png",
                                      model=self.world.background2)                              
        self.car_sprite = ModelSprite("redcar3.png",
                                      model=self.world.car)
        self.enemylist = []                              
        self.fpscounter = Fpscounter()
        self.set_update_rate(1/70)
    def update(self, delta):
        self.creteenemy()
        self.update_enemylist()
        self.world.update(delta)
        

    def on_draw(self):
        arcade.start_render()
        
        self.background_sprite.draw()
        self.background_sprite2.draw()
        self.car_sprite.draw()
        self.fpscounter.tick()
        self.check_state()

        fps = f"fps{self.fpscounter.fps():.2f}"
        score = f"Score {self.world.score}"
        arcade.draw_text(score,710,770,arcade.color.YELLOW)
        arcade.draw_text(fps,750,560,arcade.color.BLACK)
        for enemy in self.enemylist:
            enemy.draw()
            
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
        if not self.world.is_dead():
            self.world.start()

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def creteenemy(self):
        for enemy in self.world.enemylist:
            if enemy in (enemy_sprite.model for enemy_sprite in self.enemylist):
                pass
            else:
                self.enemylist.append(ModelSprite(self.randomsprite(), 
                model=enemy))
    def randomsprite(self):
        namelist = ['EnemyCar2.png','Enemycarwhite.png']
        randomnum = randint(0,1)
        return namelist[randomnum]


    def update_enemylist(self):
        for enemy_sprite in [_ for _ in self.enemylist]:
            if enemy_sprite.model not in self.world.enemylist:
                self.enemylist.remove(enemy_sprite)

    def draw_game_over(self):
        """
        Draw "Game over" across the screen.
        """
        output = "Game Over"
        arcade.draw_text(output, 240, 400, arcade.color.BLACK, 54)

        output = "Click to restart"
        arcade.draw_text(output, 310, 300, arcade.color.BLACK, 24)

    def check_state(self):
        if self.world.state == World.STATE_DEAD:
            self.draw_game_over()        

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()



if __name__ == "__main__":
    main()        
 
