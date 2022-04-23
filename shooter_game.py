# region SETUP
# import modules
from pygame import *
from random import randint
# create the window and the clock
_SCREEN_WIDTH = 1024    
_SCREEN_HEIGHT = 720
window = display.set_mode((_SCREEN_WIDTH, _SCREEN_HEIGHT))
display.set_caption('Alien shooting')
clock = time.Clock()
font.init()

# endregion SETUP

# region CLASSES
class GameSprite(sprite.Sprite):
    def __init__(self, imagefile, x, y, width, height, speed=0):
        sprite.Sprite.__init__(self)
        self.image = image.load(imagefile)
        self.image = transform.scale(self.image, (width, height))
        self.rect = Rect(x, y, width, height)
        self.speed = speed
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > _SCREEN_WIDTH:
            self.rect.right = _SCREEN_WIDTH
    def shoot(self):
        x = self.rect.centerx
        y = self.rect.top
        b = Bullet("bullet.png", x, y, 16, 20, speed = 6)
        b.rect.centerx = x
        bullets.add(b)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > _SCREEN_HEIGHT: 
            self.rect.x = randint(0, _SCREEN_WIDTH - self.rect.width)
            self.rect.bottom = 0
 
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0: 
            self.kill()

class TextSprite(sprite.Sprite):
    def __init__(self, text, size, color_text, position):
        super().__init__()
        self.text = text
        self.position = position
        self.color = color_text
        self.local_font = font.Font(None, size)
        self.image = self.local_font.render(self.text, True, color_text)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
    def update(self, new_text):
        self.text = new_text
        self.image = self.local_font.render(self.text, True, self.color)

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > _SCREEN_HEIGHT: 
            self.rect.x = randint(0, _SCREEN_WIDTH - self.rect.width)
            self.rect.bottom = 0

# endregion CLASSES

background = GameSprite("galaxy.jpg", 0, 0, _SCREEN_WIDTH, _SCREEN_HEIGHT)
game_over = GameSprite("game_over.jpg", 0, 0, _SCREEN_WIDTH, _SCREEN_HEIGHT)
player = Player("rocket.png", _SCREEN_WIDTH/2, _SCREEN_HEIGHT-120, 80, 110, 8)
bullets = sprite.Group()
enemies = sprite.Group()

def create_enemy():
    rand_x = randint(0, _SCREEN_WIDTH-80)
    rand_speed = randint(1, 4)
    en = Enemy("ufo.png", rand_x, 0, 80, 60, speed=rand_speed)
    enemies.add(en)

should_create_enemies = True
score_keep = TextSprite(text="Points: 0", size=50, color_text=(255, 0, 0), position=(100, 30))
points = 0

# region GAME_STATES
def intro():
    global should_create_enemies, game_state, points
    background.draw(window)
    points = 0
    if should_create_enemies:
        enemies.empty()
        bullets.empty()
        for i in range(8):
            create_enemy()
        should_create_enemies = False
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                game_state = "PLAY"
 
def play():
    global game_state, points
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.shoot()
    background.draw(window)
    enemies.update()
    enemies.draw(window)
    bullets.update()
    bullets.draw(window)
    player.update()
    player.draw(window)




    score_keep.update("Points: "+str(points))
    score_keep.draw(window)

    if sprite.spritecollide(player, enemies, False):
        game_state = "END"

    collisions = sprite.groupcollide(enemies, bullets, True, True)
    for c in collisions:
        points += 1
        create_enemy()
 
def end_screen():
    global should_create_enemies, game_state
    game_over.draw(window)
    
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_r:
                game_state = "INTRO"
                should_create_enemies = True
# endregion GAME_STATES

# region GAMELOOP
# create a loop
game_state = "INTRO"
 
while not event.peek(QUIT):
    # game flow
    if game_state == "INTRO":
        intro()
    if game_state == "PLAY":
        play()
    if game_state == "END":
        end_screen()
    # refresh the screen and tick the clock    
    display.update()
    clock.tick(60)
# endregion GAMELOOP