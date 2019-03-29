import arcade
from models import World, Car

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Racing_Race'


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
        self.enemy_car_sprite = ModelSprite("EnemyCar.png",
                                        model=self.world.enemycar)                                

    def update(self, delta):
        self.world.update(delta)    

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.car_sprite.draw()
        self.enemy_car_sprite.draw()
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)

    def on_key_release(self, key, key_modifiers):
        self.world.on_key_release(key, key_modifiers)    


def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.set_window(window)
    arcade.run()


if __name__ == "__main__":
    main()        
 
