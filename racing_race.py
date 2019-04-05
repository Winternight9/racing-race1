import arcade
from models import World, Car, Enemy

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
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

        self.background = arcade.load_texture("Background.png")
        self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT) 
        self.car_sprite = ModelSprite("Car_yellow.png",
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
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.car_sprite.draw()
        self.fpscounter.tick()
        fps = f"fps{self.fpscounter.fps():.2f}"
        arcade.draw_text(fps,750,560,arcade.color.BLACK)
        for enemy in self.enemylist:
            enemy.draw()
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)

    def creteenemy(self):
        for enemy in self.world.enemylist:
            if enemy in (enemy_sprite.model for enemy_sprite in self.enemylist):
                pass
            else:
                self.enemylist.append(ModelSprite("EnemyCar.png", 
                model=enemy))
    
    def update_enemylist(self):
        for enemy_sprite in [_ for _ in self.enemylist]:
            if enemy_sprite.model not in self.world.enemylist:
                self.enemylist.remove(enemy_sprite)





def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()



if __name__ == "__main__":
    main()        
 
