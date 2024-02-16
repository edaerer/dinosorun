import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # import surfaces
        self.jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        walk1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        walk2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.walk_surfaces = [walk1, walk2]
        self.surf_index = 0
        self.image = self.walk_surfaces[self.surf_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        # add gravity
        self.gravity = 0
        # import music
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.5)
        
    def get_input(self): 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump_sound.play()
            self.gravity = -20
            
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            
    def animate(self):
        if self.rect.bottom < 300:
            self.image = self.jump
        else:
            self.surf_index += 0.1
            if self.surf_index >= len(self.walk_surfaces):
                self.surf_index = 0
            self.image = self.walk_surfaces[int(self.surf_index)]
        
    def update(self):
        self.get_input()
        self.apply_gravity()
        self.animate()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            fly1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.surfaces = [fly1, fly2]
            y = 210
        elif type == "snail":
            snail1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.surfaces = [snail1, snail2]
            y = 300
        
        self.type = type
        self.surf_index = 0
        self.image = self.surfaces[self.surf_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y))
        
    def animate(self):
        if self.type == "fly": self.surf_index += 0.15
        if self.type == "snail": self.surf_index += 0.07
        if self.surf_index >= len(self.surfaces): self.surf_index = 0
        self.image = self.surfaces[int(self.surf_index)]
        
    def update(self):
        self.animate()
        self.rect.x -= 6
        self.destroy()
        
    def destroy(self):
        # if an obstacle is too far to the left, remove it
        if self.rect.x <= -100:
            self.kill()
        
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f"Score: {current_time}", False, "red")
    score_rect = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collisions():
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        # whenever a collision is detected, clear all the obstacles
        obstacles.empty()
        return False
    else:
        return True

# start the engine
pygame.init()
# create the window - takes a tuple
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Dinosorun")
# create a clock object to control the frame rate
clock = pygame.time.Clock()
# variable to check if the game is running
game_active = False
# time since the game started (in miliseconds)
start_time = 0
# background
music = pygame.mixer.Sound("audio/music.wav")
music.play(loops = -1)  # play it forever
font = pygame.font.Font("font/Pixeltype.ttf", 50)
sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()
# current game score and highest score
highest_score, score = 0, 0
# player
player = pygame.sprite.GroupSingle()
player.add(Player())
# obstacles
obstacles = pygame.sprite.Group()
# intro screen
player_stand_surf = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand_surf = pygame.transform.scale(player_stand_surf, (100, 125))
player_stand_rect = player_stand_surf.get_rect(center = (400, 200))
game_title_surf = font.render("Welcome to Dinosorun", False, "pink")
game_title_rect = game_title_surf.get_rect(center = (400, 50))
game_message_surf = font.render("Press space to run", False, "pink")
game_message_rect = game_message_surf.get_rect(center = (400, 330))
# create your own events
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

# main game loop
while True:
    # check for all possible user input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                # choose either fly or snail (mostly snail)
                obstacles.add(Obstacle(choice(["snail","fly","snail", "snail"])))
        else:
            # restart the game if space key is pressed
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
         
    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        # player
        player.draw(screen)
        player.update()
        # obstacle movement
        obstacles.draw(screen)
        obstacles.update()
        # keep track of score
        score = display_score()
        if score > highest_score: highest_score = score
        # check for collisions
        game_active = collisions()
    else:
        screen.fill((95, 130, 160))
        screen.blit(player_stand_surf, player_stand_rect)
        screen.blit(game_title_surf, game_title_rect)
        # display the highest score
        highest_score_surf = pygame.font.Font("font/Pixeltype.ttf", 30).render(f"Highest Score: {highest_score}", False, "pink")
        highest_score_rect = highest_score_surf.get_rect(topright = (760, 20))
        screen.blit(highest_score_surf, highest_score_rect)
        # display game message
        if score:
            game_message_surf = font.render(f"Your Score: {score}", False, "pink")
            game_message_rect = game_message_surf.get_rect(center = (400, 330))
        screen.blit(game_message_surf, game_message_rect)
    
    # update the window
    pygame.display.update()
    # 60 fps
    clock.tick(60)