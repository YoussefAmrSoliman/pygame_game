# A game using pygame
### Video Demo: [Platformer Game](https://youtu.be/TzKGm0lYJ7A?si=3oJHKV0hmR2mmhmA)
### Description: this is game built using python and pygame library.

#### the game code encapsulated in game.py file. at first started by importing libraries that would included in building the game. using `pygame.init()` to initialize the game window, then `pygame.display.set_caption("Platformer")`to display the name of window as platformer, `window = pygame.display.set_mode((WIDTH, HEIGHT))` then use set mode to open window to draw on with this dimentions.

#### created functions to load the assets used before create the classes. `load_sprite_sheets` given the path to load from the directory of the game the characters sprites or images that showed on window. and `get_block(size)` to get the image of the block that construct the platforme to move on.

#### the player class has several attributes and functions that change these attributes and variables to change the status to show a motion"sprite sheet" shwon on screen using `blit` function from pygame. rect value is the rectangle that i put the image on to be drawn on the screen each frame. this image updated in the `update_sprite` function based on the status of the player like idle, run, jump, attack and die. each with a sprite sheet in form of images of the motion in png file. so looping on the sprite sheet to draw it on screen with rate controlled with `ANIMATION_DELAY` value to create motion in the game based on input from user. also to move the player after pressing on key on keyboard with constant speed and `handle_move` function from outside of the class to handle collision and `move_right` `move_left` called with the class given that speed.

#### then  created a parent `class Object` for block class and fire class "enemies and traps" to inherit from it to create surface and rect and draw function.`class Block` used to create platform. `class Fire` with name "enemy" to create character with functions like player to control its status and attributes to get the motion that shown in the window.

#### `get_background` to load the image and append them together to form background shown on window. `draw` call each draw function in each class and draw the background that its locations appended in `tiles` variable to draw the whole frame on the window then with `pygame.display.update()` update it on the screen to the player.

#### created two functions to handle collisions.  `handle_vertical_col` to be able to stand on the platform and the player rect do not overlap with any block using `pygame.sprite.collide_mask` that return if there is any overlap between two objects passed to it. `collide` to handle vertical collisions so the player would be stopped if ran into wall

#### in `handle_move` created list keys to recored the keys pressed each frame using `pygame.key.get_pressed()` then with if statments choose action based on key in keys constrained with collisions.

#### the main game loop created `clock = pygame.time.Clock()` that ticks each 60 FPS "so it loops each second 60 times to show 60 frames in this second". and base condition to quit the game if the event is to quit. in the game loop we create objects from the classes and call loop function on each class that changes over time like enemy and player. also to have scrolling window created offset that increases if player get close to the boarders so in the next frame objects would be drawn in moved position so it would be seen as the player is moving in the map on the screen.