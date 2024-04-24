import os
import random 
import math
import pygame
from os import listdir
from os.path import isfile, join

pygame.init()

pygame.display.set_caption("Platformer")

BG_COLOR = (255, 255, 255)
WIDTH, HEIGHT = 1000, 700
FPS = 60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH, HEIGHT))

def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, width, height, direction=False):
    path = join("assets", dir1)
    imgs = [f for f in listdir(path) if isfile(join(path,f))]

    all_sprites = {}

    for img in imgs:
        sprite_sheet = pygame.image.load(join(path, img)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
            
        
        if direction:
            all_sprites[img.replace(".png", "") + "_right"] = sprites
            all_sprites[img.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[img.replace(".png", "")] = sprites

    return all_sprites

def get_block(size):
    path = join("assets", "terrain", "spr_tile_platform.png")
    img = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(80, 0, size, size)
    surface.blit(img, (0, 0), rect)
    return surface

class Player(pygame.sprite.Sprite):
    GRAVITY = 1
    SPRITES = load_sprite_sheets("red_hoded", 50, 36, True)
    ANIMATION_DELAY = 9


    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.attack = False
        self.attack_count = 0
        self.hit = False
        self.hit_count = 0
        self.dead = False
        self.dead_count = 0
        self.sprite_sheet = "idle"
        self.health = 100

    def jump(self):
        self.y_vel = -self.GRAVITY * 8
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def kill(self):
        self.attack = True
        self.attack_count = 0
        self.animation_count = 0
        
    
    def make_hit(self):
        self.hit = True
        self.hit_count = 0
        
    def die(self):
        self.dead = True

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.health -= 1
            self.hit_count += 1
        if self.hit_count > fps * 0.5:
            self.hit = False
            self.hit_count = 0
        
        if self.attack:
            self.attack_count += 1
            self.ANIMATION_DELAY = 3
        if self.attack_count > fps * 0.3:
            self.attack = False
            self.ANIMATION_DELAY = 9
            self.attack_count = 0

        if self.dead:
            self.dead_count +=1
            self.ANIMATION_DELAY = 3

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        if not self.dead:
            self.sprite_sheet = "idle"

        if self.hit and not self.dead:
            self.sprite_sheet = "hit"

        if self.attack and not self.dead:
            self.sprite_sheet = "attack"    

        if self.y_vel < 0 and not self.dead:
            if self.jump_count == 1:
                self.sprite_sheet = "jump"
            elif self.jump_count == 2:
                self.sprite_sheet = "jump"
        elif self.y_vel > self.GRAVITY * 2 and not self.dead: 
            self.sprite_sheet = "fall"
        elif self.x_vel != 0 and not self.dead :
            self.sprite_sheet = "run"
        
        sprite_sheet_name = self.sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        if self.dead:
            self.sprite_sheet = "die"
            sprites = self.SPRITES[sprite_sheet_name]
            
            if self.dead_count // self.ANIMATION_DELAY >= len(sprites):
                self.dead_count -= 1
                sprite_index = (self.dead_count // self.ANIMATION_DELAY) % len(sprites)
                self.sprite = sprites[sprite_index]
            else:
                sprite_index = (self.dead_count // self.ANIMATION_DELAY) % len(sprites)
                self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()
       

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)    

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))

class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name
    
    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Fire(Object):

    ANIMATION_DELAY = 8

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "enemy")
        self.enemy = load_sprite_sheets("enemy", width, height, True)
        
        self.image = self.enemy["idle_right"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "idle_right"
        self.die = False
        self.die_count = 0

    def attack(self):
        if self.die == False:
            self.animation_name = "attack_right"
    
    def idle(self):
        self.animation_name = "idle_right"
    def dead(self):
        
        self.animation_name = "dead_right"
    
    def loop(self, fps):
        sprites = self.enemy[self.animation_name]
        sprites = flip(sprites) 
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        
        self.animation_count += 1

        if self.die:
            sprites = flip(sprites) 
            sprite_index = (self.die_count // self.ANIMATION_DELAY) % len(sprites)
            if fps > 59:    
                self.die_count += 1
            if self.die_count // self.ANIMATION_DELAY >= len(sprites):
                self.die_count -= 1
            
            
            
        self.image = sprites[sprite_index]
        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites) and self.die == False:
            self.animation_count = 0
        


def get_background(name):
    img = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = img.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height +1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, img

def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    pygame.display.update()



def handle_vertical_col(player, objects, dy):
    objects_collided = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0 and obj.name != "enemy" and player.rect.bottom > obj.rect.top:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0 and obj.name != "enemy":
                player.rect.top = obj.rect.bottom
                player.hit_head()
            elif dy > 0 and obj.name == "enemy":
                if obj.animation_name == "idle_right" :
                    player.rect.bottom = obj.rect.top
                    player.landed()

            objects_collided.append(obj)

    return objects_collided

def collide(player, objects, dx):
    player.move(dx, -1)
    player.update()
    collided_obj = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):     
            collided_obj = obj
            break

    player.move(-dx, 1)
    player.update()
    return collided_obj

def handle_move(player, objects, enemy):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    col_left = collide(player, objects, -PLAYER_VEL * 4)
    col_right = collide(player, objects, PLAYER_VEL * 4)
    if keys[pygame.K_a] and not col_left:
        if not player.dead:
            player.move_left(PLAYER_VEL)
        
    if keys[pygame.K_d] and not col_right:
        if not player.dead:
            player.move_right(PLAYER_VEL)

    ver_col = handle_vertical_col(player, objects, player.y_vel)
    to_check = [col_left, col_right, *ver_col]
    for obj in to_check:
        if obj and obj.name == "enemy":
            if obj.animation_name == "attack_right":
                player.make_hit()
            elif player.sprite_sheet == "attack":
                enemy.die = True
            
    

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("bg_00.png")

    block_size = 48

    player = Player(100, 100, 50, 36)
    r3 = random.randint(-400,400)
    enemy = Fire(500 + r3, HEIGHT - block_size -96, 120, 48)
    
    r1 = random.randint(8, 15)
    r2 = random.randint(0, 4)
    floor = [Block(i * block_size, HEIGHT - block_size, block_size) 
             for i in range(-WIDTH // block_size +1, (WIDTH *2) // block_size)]
    platform = [Block(i * block_size , HEIGHT - block_size * 4, block_size)
                for i in range(r1-5,r1 + r2)]
    
    objects = [*floor, *platform, enemy]
    
    offset_x = 0
    scroll_area_width = 100
    
    run = True
    while run:
        clock.tick(FPS)
      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE  and player.jump_count < 2 and not player.dead:
                    player.jump()
                elif event.key == pygame.K_LCTRL:
                    player.kill()
            
        if player.health == 0:
            player.die()
            
        if   (enemy.rect.left - player.rect.right < 45 
              and player.rect.left - enemy.rect.right < enemy.rect.left - player.rect.right
            and player.rect.bottom > enemy.rect.top and not player.dead) :
            enemy.attack()
        elif enemy.die :
            
            enemy.dead()
        else:
            enemy.idle()
        
      
        player.loop(FPS)
        enemy.loop(FPS)
        handle_move(player, objects, enemy)    
        draw(window, background, bg_image, player, objects, offset_x)

        if((player.rect.right - offset_x  >= WIDTH - scroll_area_width and player.x_vel > 0) 
           or (player.rect.left - offset_x <= scroll_area_width and player.x_vel < 0)):
            offset_x += player.x_vel
    
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)