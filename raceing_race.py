import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'Racing_Race'

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)


    def on_draw(self):
        arcade.start_render()

def main():
    MyGame()
    arcade.run()


if __name__ == "__main__":
    main()        
 
