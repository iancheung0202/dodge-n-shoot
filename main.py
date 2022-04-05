### ------ IMPORT NECESSARY MODULES ------ ###
import pygame, random

### ------ IMPORT KEYS FROM PYGAME ------ ###
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
    K_w,
    K_s,
    K_a,
    K_d,
    K_e
)

### ------ INITIALIZE PYGAME ------ ###
pygame.init()
pygame.mixer.init()

### ------ DISPLAY SCREEN ------ ###
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), 
    pygame.FULLSCREEN
)
pygame.display.set_caption('Dodge n\' Shoot')
pygame.display.set_icon(pygame.image.load('rocket-icon.png'))

### ------ CUSTOM EVENTS FOR NEW ENEMY AND CLOUD ------ ###
ADDENEMY = pygame.USEREVENT + 1
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000) # 1 second
ADDHEAL = pygame.USEREVENT + 3
pygame.time.set_timer(ADDHEAL, random.randint(10000, 20000)) # 10 - 20 seconds
ADDMEGAROCKET = pygame.USEREVENT + 4
pygame.time.set_timer(ADDMEGAROCKET, random.randint(7000, 10000)) # 7 - 10 seconds
ADDPIERCE = pygame.USEREVENT + 5
pygame.time.set_timer(ADDPIERCE, random.randint(13000, 20000)) # 13 - 20 seconds
ADDSHIELD = pygame.USEREVENT + 6
pygame.time.set_timer(ADDSHIELD, random.randint(17000, 27000)) # 17 - 27 seconds
ADDBOSSSPAWN = pygame.USEREVENT + 7
pygame.time.set_timer(ADDBOSSSPAWN, random.randint(2000, 3000)) # Every 2 - 3 seconds

clock = pygame.time.Clock()
text, game = '0'.rjust(3), 0
CLOCKTICK = pygame.USEREVENT + 69
pygame.time.set_timer(CLOCKTICK, 1000)
font = pygame.font.Font('arcadepix.ttf', 40)
reload_speed = 5 # seconds
mega_rocket_player = mega_rocket_player2 = pierce_player = pierce_player2 = False
added_boss = False


### ------ DEFINE PLAYER CLASS ------ ###
class Player(pygame.sprite.Sprite):

    def __init__(self, lives=3):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Player.png") 
        self.rect = self.surf.get_rect()
        self.lives = lives
        self.dt = 0
        self.times = 3
        self.has_shield = False

    def set_dt(self, value):
        self.dt = value

    ### ------ METHOD CALLED WHEN KEY IS PRESSED ------ ###
    def update(self, pressed_keys):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(5, 0)

        ### ------ KEEPING PLAYER IN THE SCREEN ------ ###
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT: 
            self.rect.bottom = SCREEN_HEIGHT

    ### ------ METHOD CALLED WHEN PLAYER COLLIDES WITH MISSILE ------ ###
    def disappear(self):
        if self.has_shield == True:
            self.times = self.times - 1
            if self.times == 0:
                self.has_shield = False
                self.times = 3
                return
            immune_sound.play()
            return
        else:
            collision_sound.play()
            self.lives -= 1
            if self.lives == 0:
                self.kill()

    ### ------ METHOD CALLED WHEN PLAYER COLLIDES WITH HEALER ------ ###
    def heal(self):
        self.lives += 1
        heal_sound.play()


### ------ DEFINE PLAYER 2 CLASS ------ ###
class PlayerTwo(pygame.sprite.Sprite):

    def __init__(self, lives=3):
        super(PlayerTwo, self).__init__()
        self.surf = pygame.image.load("Player2.png") # Draw the jet image
        self.rect = self.surf.get_rect(center=(0, SCREEN_HEIGHT))
        self.lives = lives
        self.dt = 0
        self.times = 3
        self.has_shield = False

    def set_dt(self, value):
        self.dt = value

    ### ------ METHOD CALLED WHEN KEY IS PRESSED ------ ###
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)

        ### ------ KEEPING PLAYER 2 IN THE SCREEN ------ ###
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    ### ------ METHOD CALLED WHEN PLAYER 2 COLLIDES WITH MISSILE ------ ###
    def disappear(self):
        if self.has_shield == True:
            self.times = self.times - 1
            if self.times == 0:
                self.has_shield = False
                self.times = 3
                return
            immune_sound.play()
            return
        else:
            collision_sound.play()
            self.lives -= 1
            if self.lives == 0:
                self.kill()

    ### ------ METHOD CALLED WHEN PLAYER 2 COLLIDES WITH HEALER ------ ###
    def heal(self):
        self.lives += 1
        heal_sound.play()


### ------ DEFINE ENEMY CLASS ------ ###
class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png") # Draw the missiles
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=( # Define random spawn position
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 10) # Random speed 

    def update(self):
        self.rect.move_ip(-self.speed, 0) # Move the enemy based on random speed
        if self.rect.right < 0: # Remove it when it passes the left edge of the screen
            self.kill()


### ------ DEFINE ENEMY CLASS ------ ###
class BossSpawn(pygame.sprite.Sprite):

    def __init__(self, centerx, centery, bosslevel):
        super(BossSpawn, self).__init__()
        boss_spawn_sound.play()
        self.surf = pygame.image.load("BossSpawn.png") # Draw the missiles
        self.rect = self.surf.get_rect(
            center=( # Define spawn position from bass
                centerx,
                centery
            )
        )
        if bosslevel == 0:
            self.fly = 10
        elif bosslevel == 1:
            self.fly = 17
        elif bosslevel == 2:
            self.fly = 25
        elif bosslevel == 3:
            self.fly = 32
        elif bosslevel == 4:
            self.fly = 40
        self.speed = random.randint(self.fly, (self.fly+5)) # Random speed 

    def update(self):
        self.rect.move_ip(-self.speed, 0) # Move the enemy based on random speed
        if self.rect.right < 0: # Remove it when it passes the left edge of the screen
            self.kill()


### ------ DEFINE ENEMY BOSS CLASS ------ ###
class Boss(pygame.sprite.Sprite):

    def __init__(self, centery):
        super(Boss, self).__init__()
        self.surf = pygame.image.load("boss.png") # Draw the boss
        self.lives = 44
        self.rect = self.surf.get_rect(
            center=( # Define spawn position
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                centery,
            )
        )
        self.speed = 5
        self.vertical_speed = 1
        self.died = False
        self.dt = 0
        self.boss_spawn_freq = 2000
        self.level = 0
        self.levels = ["Easy", "Normal", "Hard", "Master", "Insane"]

    def update(self):
        if abs(self.rect.centery - player.rect.centery) < abs(self.rect.centery - player2.rect.centery) and player.lives != 0: # If boss is nearer player
            self.user = player
        elif abs(self.rect.centery - player.rect.centery) > abs(self.rect.centery - player2.rect.centery) and player2.lives != 0: # If boss is nearer player2
            self.user = player2
        elif abs(self.rect.centery - player.rect.centery) == abs(self.rect.centery - player2.rect.centery) and player.lives != player2.lives != 0:
            self.user = random.choice([player, player2])
        elif player.lives == 0:
            self.user = player2
        elif player2.lives == 0:
            self.user = player
        
        if self.rect.centery < self.user.rect.centery: # If missile is above player
            self.rect.move_ip(-self.speed, self.vertical_speed) 
        elif self.rect.centery > self.user.rect.centery: # If missile is below player
            self.rect.move_ip(-self.speed, -self.vertical_speed)
        else:
            self.rect.move_ip(-self.speed, 0) # If missile is at player

        if self.rect.right < (SCREEN_WIDTH - 60): # If placed in the correct position in the right side of the screen, stop moving left
            self.speed = 0

    def get_hit(self):
        self.lives -= 1
        if self.lives % 10 == 0:
            self.boss_spawn_freq = self.boss_spawn_freq - (self.boss_spawn_freq / 2)
            pygame.time.set_timer(ADDBOSSSPAWN, int(self.boss_spawn_freq)) 
            self.dt = pygame.time.get_ticks()
            final_sound = pygame.mixer.Sound("Final.ogg")
            final_sound.set_volume(0.5)
            final_sound.play()
            self.level += 1
            if self.vertical_speed < 5:
                self.vertical_speed += 1


### ------ DEFINE SHOOTER CLASS ------ ###
class Shoot(pygame.sprite.Sprite):

    def __init__(self, coordinate):
        super(Shoot, self).__init__()
        self.surf = pygame.image.load("shoot.png") # Draw the shooters
        self.rect = self.surf.get_rect(
            center=(coordinate) # Define spawn position (The player's current position)
        )
        shoot_sound.play()

    def update(self):
        self.rect.move_ip(15, 0) # Move the shooter on constant speed
        if self.rect.left > SCREEN_WIDTH: # Remove it when it passes the right edge of the screen
            self.kill()


### ------ DEFINE SHOOTER CLASS ------ ###
class MegaShoot(pygame.sprite.Sprite):

    def __init__(self, coordinate):
        super(MegaShoot, self).__init__()
        self.surf = pygame.image.load("mega-rocket.png") # Draw the shooters
        self.rect = self.surf.get_rect(
            center=(coordinate) # Define spawn position (The player's current position)
        )
        shoot_sound.play()

    def update(self):
        self.rect.move_ip(17, 0) # Move the shooter on constant speed
        if self.rect.left > SCREEN_WIDTH: # Remove it when it passes the right edge of the screen
            self.kill()


### ------ DEFINE CLOUD CLASS ------ ###
class Cloud(pygame.sprite.Sprite):

    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=( # Define random spawn position
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0) # Move cloud at a constant speed
        if self.rect.right < 0: # Remove it when it passes the left edge of the screen
            self.kill()


### ------ DEFINE HEALTH RESTORER CLASS ------ ###
class Shield(pygame.sprite.Sprite):

    def __init__(self):
        super(Shield, self).__init__()
        self.surf = pygame.image.load("Shield.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=( # Define random spawn position
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-7.5, 0) # Move cloud at a constant speed
        if self.rect.right < 0: # Remove it when it passes the left edge of the screen
            self.kill()


### ------ DEFINE HEALTH RESTORER CLASS ------ ###
class Heal(pygame.sprite.Sprite):

    def __init__(self):
        super(Heal, self).__init__()
        self.surf = pygame.image.load("Heal.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=( # Define random spawn position
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-7.5, 0) # Move cloud at a constant speed
        if self.rect.right < 0: # Remove it when it passes the left edge of the screen
            self.kill()


### ------ DEFINE MEGA ROCKET CLASS ------ ###
class MegaRocket(pygame.sprite.Sprite):

    def __init__(self):
        super(MegaRocket, self).__init__()
        self.surf = pygame.image.load("MegaRocket.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=( # Define random spawn position
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-7.5, 0) # Move cloud at a constant speed
        if self.rect.right < 0: # Remove it when it passes the left edge of the screen
            self.kill()


### ------ DEFINE PIERCE SHOOTER CLASS ------ ###
class Pierce(pygame.sprite.Sprite):

    def __init__(self):
        super(Pierce, self).__init__()
        self.surf = pygame.image.load("Pierce.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=( # Define random spawn position
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-7.5, 0) # Move cloud at a constant speed
        if self.rect.right < 0: # Remove it when it passes the left edge of the screen
            self.kill()


### ------ DEFINE EXPLODE CLASS ------ ###
class Explode(pygame.sprite.Sprite):

    def __init__(self):
        super(Explode, self).__init__()
        self.surf = pygame.image.load("Explode.png")
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=( # Define random spawn position
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-7.5, 0) # Move cloud at a constant speed
        if self.rect.right < 0: # Remove it when it passes the left edge of the screen
            self.kill()


### ------ DEFINE SPAWN ENEMY FREQ. CLASS ------ ###
class Spawn:

    def __init__(self, freq):
        self.freq = freq
        self.initial = freq
        pygame.time.set_timer(ADDENEMY, self.freq) 
        self.store = self.freq

    def stop_spawning(self):
        self.store = self.freq
        self.freq = 3600000
        pygame.time.set_timer(ADDENEMY, int(self.freq)) 

    def increase_freq(self):
        if int(self.freq) < 150: 
            # Surpassing one missile per 150 millesecond will already result in a relatively huge amount of missiles spawning, and it causes a lot of lag, that basically makes the game unplayable
            return # Stop increasing the spawning frequency
        else:
            self.freq = self.freq * 0.995 # Continue to increase the spawning frequency of incoming missiles         
            pygame.time.set_timer(ADDENEMY, int(self.freq)) 


### ------ DEFINE CLASSES ------ ###
player = Player(100)
player2 = PlayerTwo(100)
spawn = Spawn(500) # The spawning frequency of incoming missiles will be 2 per second at the start of the game, but gradually increases [ see line 389 increase_freq() function ]

### ------ DEFINE SPIRITE GROUPs ------ ###
shooters = pygame.sprite.Group()
megashooters = pygame.sprite.Group()
pierceshooters = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bosses = pygame.sprite.Group()
clouds = pygame.sprite.Group()
healers = pygame.sprite.Group()
pierces = pygame.sprite.Group()
shields = pygame.sprite.Group()
megarockets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(player2)
players = pygame.sprite.Group()
players.add(player)
players.add(player2)

### ------ DEFINE THE MUSIC ------ ###
bg_music = pygame.mixer.music.load("For7ius - Let's Go.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops = -1)
move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")
explosion_sound = pygame.mixer.Sound("Explosion.ogg")
shoot_sound = pygame.mixer.Sound("Shoot.ogg")
reload_sound = pygame.mixer.Sound("Reload.ogg")
heal_sound = pygame.mixer.Sound("Heal.ogg")
mega_rocket_sound = pygame.mixer.Sound("Mega Rocket.ogg")
pierce_sound = pygame.mixer.Sound("Pierce.ogg")
shield_sound = pygame.mixer.Sound("Shield.ogg")
immune_sound = pygame.mixer.Sound("Immune.ogg")
boss1_sound = pygame.mixer.Sound("Boss1.ogg")
boss2_sound = pygame.mixer.Sound("Boss2.ogg")
boss_spawn_sound = pygame.mixer.Sound("BossSpawn.ogg")
move_up_sound.set_volume(0.1)
move_down_sound.set_volume(0.1)
collision_sound.set_volume(0.1)
explosion_sound.set_volume(0.5)
shoot_sound.set_volume(0.5)
reload_sound.set_volume(0.3)
heal_sound.set_volume(0.3)
mega_rocket_sound.set_volume(0.3)
pierce_sound.set_volume(0.2)
shield_sound.set_volume(0.3)
immune_sound.set_volume(0.3)
boss1_sound.set_volume(0.2)
boss2_sound.set_volume(0.5)
boss_spawn_sound.set_volume(0.5)

def intro(intro):
    screen.blit(intro, intro.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))

def ammo(text, color, player):
    screen.blit(pygame.font.Font('arcadepix.ttf', 20).render(str(text), True, color), (player.rect.topright, player.rect.midleft))

### ------ GAME LOOP ------ ###
running = True
while running:
    ### ------ LISTEN TO KEY PRESSES ------ ###
    events = pygame.event.get()
    for event in events:
        if pygame.time.get_ticks() > 7200: # Only execute after the intro is played
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

                ### ------ SPAWN SHOOTER FOR PLAYER (5 seconds reload speed) ------ ###
                if event.key == K_e and player.lives != 0:
                    if (pygame.time.get_ticks() - player.dt) > (reload_speed * 1000) and mega_rocket_player == True and pierce_player == False:
                        shooter = MegaShoot((player.rect.centerx, player.rect.centery))
                        megashooters.add(shooter)
                        shooters.add(shooter)
                        all_sprites.add(shooter)
                        player.set_dt(pygame.time.get_ticks())
                        player.heal()
                        mega_rocket_player = False
                    elif (pygame.time.get_ticks() - player.dt) > (reload_speed * 1000) and pierce_player == True and mega_rocket_player == False:
                        shooter = Shoot((player.rect.centerx, player.rect.centery))
                        pierceshooters.add(shooter)
                        all_sprites.add(shooter)
                        player.set_dt(pygame.time.get_ticks())
                        pierce_player = False
                    elif (pygame.time.get_ticks() - player.dt) > (reload_speed * 1000):
                        shooter = Shoot((player.rect.centerx, player.rect.centery))
                        shooters.add(shooter)
                        all_sprites.add(shooter)
                        player.set_dt(pygame.time.get_ticks())
                    else:
                        reload_sound.play()
                        reload_sound.play() # Playing twice is better than playing once

                ### ------ SPAWN SHOOTER FOR PLAYER 2 (5 seconds reload speed)------ ###
                if event.key == K_SPACE and player2.lives != 0:
                    if (pygame.time.get_ticks() - player2.dt) > (reload_speed * 1000) and mega_rocket_player2 == True and pierce_player2 == False:
                        shooter = MegaShoot((player2.rect.centerx, player2.rect.centery))
                        megashooters.add(shooter)
                        shooters.add(shooter)
                        all_sprites.add(shooter)
                        player2.set_dt(pygame.time.get_ticks())
                        player2.heal()
                        mega_rocket_player2 = False
                    elif (pygame.time.get_ticks() - player2.dt) > (reload_speed * 1000) and pierce_player2 == True and mega_rocket_player2 == False:
                        shooter = Shoot((player2.rect.centerx, player2.rect.centery))
                        pierceshooters.add(shooter)
                        all_sprites.add(shooter)
                        player2.set_dt(pygame.time.get_ticks())
                        pierce_player2 = False
                    elif (pygame.time.get_ticks() - player2.dt) > (reload_speed * 1000):
                        shooter = Shoot((player2.rect.centerx, player2.rect.centery))
                        shooters.add(shooter)
                        all_sprites.add(shooter)
                        player2.set_dt(pygame.time.get_ticks())
                    else:
                        reload_sound.play()
                        reload_sound.play() # Playing twice is better than playing once
            
            elif event.type == ADDENEMY:
                ### ------ CREATE NEW ENEMY ------ ###
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

            elif event.type == ADDCLOUD:
                ### ------ CREATE NEW CLOUD ------ ###
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

            elif event.type == ADDSHIELD:
                ### ------ CREATE NEW SHIELD ------ ###
                new_shield = Shield()
                shields.add(new_shield)
                all_sprites.add(new_shield)

            elif event.type == ADDHEAL:
                ### ------ CREATE NEW HEALER ------ ###
                new_healer = Heal()
                healers.add(new_healer)
                all_sprites.add(new_healer)

            elif event.type == ADDBOSSSPAWN:
                ### ------ CREATE NEW BOSS ENEMY ------ ###
                for boss in bosses:
                    if pygame.time.get_ticks() - boss.dt > random.randint(2000, 3000):
                        new_boss_spawn = BossSpawn(boss.rect.centerx, boss.rect.centery, boss.level)
                        enemies.add(new_boss_spawn)
                        all_sprites.add(new_boss_spawn)
                        boss.dt = pygame.time.get_ticks()

            elif event.type == ADDMEGAROCKET:
                ### ------ CREATE NEW MEGA ROCKET ------ ###
                new_mega_rocket = MegaRocket()
                megarockets.add(new_mega_rocket)
                all_sprites.add(new_mega_rocket)

            elif event.type == ADDPIERCE:
                ### ------ CREATE NEW PIERCE ------ ###
                boss_active = False
                for boss in bosses:
                    if boss.died == False:
                        boss_active = True
                if boss_active is not True:
                    new_pierce = Pierce()
                    pierces.add(new_pierce)
                    all_sprites.add(new_pierce)

            elif event.type == CLOCKTICK: 
                game += 1
                text = str(game)
                spawn.increase_freq()
                
        if event.type == QUIT:
            running = False

    ### ------ GET PRESSED KEYS AND ACTION ------ ###
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    player2.update(pressed_keys)

    ### ------ UPDATE THE SPAWNABLES ------ ###
    enemies.update()
    clouds.update()
    healers.update()
    megarockets.update()
    shooters.update()
    megashooters.update()
    pierces.update()
    pierceshooters.update()
    shields.update()
    bosses.update()
    
    ### ------ FILL THE SCREEN WITH SKY BLUE ------ ###
    screen.fill((135, 206, 250))

    ### ------ DISPLAY EVERYTHING ON THE SCREEN ------ ###
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    ### ------ IF MISSILE AND PLAYER COLLISION ------ ###
    for user in players:
        if pygame.sprite.spritecollide(user, enemies, True):
            user.disappear()
            if player.lives == 0 and player2.lives == 0:
                running = False

    ### ------ IF MISSILE AND PLAYER COLLISION ------ ###
    for user in players:
        for boss in bosses:
            if pygame.sprite.spritecollideany(user, bosses):
                if user == player:
                    while player.lives > 0:
                        player.disappear()
                if user == player2:
                    while player2.lives > 0:
                        player2.disappear()
                if player.lives == 0 and player2.lives == 0:
                    running = False

    ### ------ IF MISSLE AND SHOOTER COLLISION ------ ###
    for enemy in enemies:
        if pygame.sprite.spritecollide(enemy, shooters, True):
            explosion_sound.play()
            ### ------ DESTROY BOTH ------ ###
            enemy.kill()

    ### ------ IF MISSLE AND BOSS COLLISION ------ ###
    for boss in bosses:
        if pygame.sprite.spritecollide(boss, shooters, True):
            explosion_sound.play()
            boss.get_hit()
            if boss.lives == 0:
                running = False

    ### ------ IF MISSLE AND <PIERCE> SHOOTER COLLISION ------ ###
    for enemy in enemies:
        if pygame.sprite.spritecollideany(enemy, pierceshooters):
            explosion_sound.play()
            enemy.kill()

    ### ------ IF PLAYER AND HEALER COLLISION ------ ###
    for user in players:
        if pygame.sprite.spritecollide(user, healers, True):
            user.heal()

    ### ------ IF PLAYER AND MEGA ROCKET COLLISION ------ ###
    for user in players:
        if pygame.sprite.spritecollide(user, megarockets, True):
            if user == player:
                mega_rocket_player = True
                pierce_player = False
                mega_rocket_sound.play()
            if user == player2:
                mega_rocket_player2 = True
                pierce_player2 = False
                mega_rocket_sound.play()

    ### ------ IF PLAYER AND PIERCES COLLISION ------ ###
    for user in players:
        if pygame.sprite.spritecollide(user, pierces, True):
            pierce_sound.play()
            if user == player:
                pierce_player = True
                mega_rocket_player = False
            if user == player2:
                pierce_player2 = True
                mega_rocket_player2 = False

    ### ------ IF PLAYER AND PIERCES COLLISION ------ ###
    for user in players:
        if pygame.sprite.spritecollide(user, shields, True):
            shield_sound.play()
            if user == player:
                player.has_shield = True
                player.times = 3
            if user == player2:
                player2.has_shield = True
                player2.times = 3

    ### ------ DISPLAY EVERYTHING ------ ###
    screen.blit(font.render(text, True, (0, 0, 0)), (SCREEN_WIDTH-100, 10))
    screen.blit(font.render(str(player.lives), True, (255, 0, 0)), (SCREEN_WIDTH-200, SCREEN_HEIGHT-100))
    screen.blit(font.render(str(player2.lives), True, (0, 0, 255)), (SCREEN_WIDTH-100, SCREEN_HEIGHT-100))

    ### ------ DISPLAY MISSLE AVAILABILITY ------ ###
    if (pygame.time.get_ticks() - player.dt) > (reload_speed * 1000) and player.lives != 0:
        if mega_rocket_player == True and pierce_player == False:
            ammo("M", (255, 0, 0), player)
        elif pierce_player == True and mega_rocket_player == False:
            ammo("P", (255, 0, 0), player)
        else:
            ammo("N", (255, 0, 0), player)
    
    if (pygame.time.get_ticks() - player2.dt) > (reload_speed * 1000) and player2.lives != 0:
        if mega_rocket_player2 == True and pierce_player2 == False:
            ammo("M", (0, 0, 255), player2)
        elif pierce_player2 == True and mega_rocket_player2 == False:
            ammo("P", (0, 0, 255), player2)
        else:
            ammo("N", (0, 0, 255), player2)

    if player.has_shield == True:
        screen.blit(pygame.font.Font('arcadepix.ttf', 20).render(str(player.times), True, (0, 128, 0)), (player.rect.topleft, player.rect.midleft))
    if player2.has_shield == True:
        screen.blit(pygame.font.Font('arcadepix.ttf', 20).render(str(player2.times), True, (0, 128, 0)), (player2.rect.topleft, player2.rect.midleft))
    
    ### ------ CREATE FINAL BOSS ------ ###
    if pygame.time.get_ticks() > 451500 and added_boss == False:
        user = random.choice([player, player2])
        new_boss = Boss(user.rect.centery)
        spawn.stop_spawning()
        new_boss.dt = pygame.time.get_ticks()
        bosses.add(new_boss)
        all_sprites.add(new_boss)
        pierce_player = pierce_player2 = False
        boss1_sound.play()
        boss2_sound.play()
        bg_music = pygame.mixer.music.load("Boss.ogg")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops = -1)
        added_boss = True
    
    try:
        if new_boss.died == False:
            ammo(str(new_boss.lives), (250, 0, 0), new_boss)
            screen.blit(pygame.font.Font('arcadepix.ttf', 20).render(new_boss.levels[new_boss.level], True, (255, 0, 0)), (SCREEN_WIDTH/2, SCREEN_HEIGHT-100))
    except Exception:
        pass

    ### ------ INTRO ------ ###
    if pygame.time.get_ticks() < 7500:
        if pygame.time.get_ticks() > 0 and pygame.time.get_ticks() < 3000:
            intro(font.render('Welcome! Two players compete with each other!', True, (255, 0, 0)))
        if pygame.time.get_ticks() > 3000 and pygame.time.get_ticks() < 5000:
            intro(font.render('Use WASD and arrow keys respectively!', True, (255, 0, 0)))
        if pygame.time.get_ticks() > 5000 and pygame.time.get_ticks() < 7200:
            intro(pygame.font.Font("arcadepix.ttf", 80).render('Let\'s go!', True, (255, 245, 14)))

    pygame.display.flip()
    clock.tick(60)