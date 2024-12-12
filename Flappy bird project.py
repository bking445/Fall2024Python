import pygame
from sys import exit

import os
import random
import time
pygame.init()
clock = pygame.time.Clock()


gone_sound = pygame.mixer.Sound("flapiamge/Mario Death - Sound Effect (HD).mp3")
pygame.mixer.music.load("flapiamge/John Williams  Superman (The Best Theme For 'The Man Of Steel').mp3")
jump_sound = pygame.mixer.Sound("flapiamge/Mario Jump Sound Effect.mp3")
yeet_sound = pygame.mixer.Sound("flapiamge/[Sound Effect] YEET.mp3")
sup_height = 20
sup_width = 20
row = pygame.display.set_mode((sup_height, sup_width))

supa_height = 20
supa_width = 20
row = pygame.display.set_mode((supa_height, supa_width))

supb_height = 20
supb_width = 20
row = pygame.display.set_mode((supb_height, supb_width))

win_height = 750
win_width = 750
window = pygame.display.set_mode((win_width, win_height))

superman_image = [pygame.image.load("flapiamge/Right_up-remove.png"),
                 pygame.image.load("flapiamge/Right_up-remove.png"),
                 pygame.image.load("flapiamge/Right_up-remove.png"),]

superman_image[0] = pygame.transform.scale(superman_image[0],(50, 50))
superman_image[1] = pygame.transform.scale(superman_image[1],(50, 50))
superman_image[2] = pygame.transform.scale(superman_image[2],(50, 50))

superwoman_image = [pygame.image.load("flapiamge/Real_superwoman_up-removebg-preview.png"),
                    pygame.image.load("flapiamge/superwoman-straight-removebg-preview.png"),
                    pygame.image.load("flapiamge/Real_superwoman_down-removebg-preview.png")]

superwoman_image[0] = pygame.transform.scale(superwoman_image[0],(75, 75))
superwoman_image[1] = pygame.transform.scale(superwoman_image[1],(75, 75))
superwoman_image[2] = pygame.transform.scale(superwoman_image[2],(75, 75))

#superman_image = supermann_image and supermana_image and supermanb_image
#top_enemy_image = pygame.transform.scale(200,200)

city_image = pygame.image.load("flapiamge/360_F_554533035_Qh3qctqPzAiAefyAesYOx0RmxvPZofbd.jpg")
city_image = pygame.transform.scale(city_image,(win_width, win_height))

game_over_image = pygame.image.load("flapiamge/real-game-over.png")
ground_image = pygame.image.load("flapiamge/Road.jpg")
# image_to_resize = pygame.transform.scale(image_to_resize, (width, height))
top_enemy_image = pygame.image.load("flapiamge/smallKryptonite.png")
bottom_enemy_image = pygame.image.load("flapiamge/smallKryptonite.png")

start_image = pygame.image.load("flapiamge/realStart-Game-removebg-preview.png")

top_enemy_image = pygame.transform.scale(top_enemy_image,(75,75))
bottom_enemy_image = pygame.transform.scale(bottom_enemy_image,(75,75))
game_over_image = pygame.transform.scale(game_over_image,(150,150))
ground_image = pygame.transform.scale(ground_image,(200,200))

#game
scroll_speed = 1
superman_start_position = (100,250)
superwoman_start_position = (80,250)
score = 0
font = pygame.font.SysFont("Arial", 20)
game_stopped = True

class Superman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = superman_image[0]
        self.rect = self.image.get_rect()
        self.rect.center = superman_start_position
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True


    def update(self, user_input):
        #Animate superman
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = superman_image[self.image_index // 10]     
        #Gravity and Flap
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500 or self.vel < 0:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        #Rotate Bird
        self.image = pygame.transform.rotate(self.image,self.vel * -7)
        #user input

        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            pygame.mixer.Sound.play(jump_sound)
            self.flap = True
            self.vel = -7


class Superwoman(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = superwoman_image[0]
        self.rect = self.image.get_rect()
        self.rect.center = superwoman_start_position
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True


    def update(self, user_input):
        #Animate superman
        if self.alive:
            self.image_index += 1
        if self.image_index >= 30:
            self.image_index = 0
        self.image = superwoman_image[self.image_index // 10]
        #Gravity and Flap
        self.vel += 0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500 or self.vel < 0:
            self.rect.y += int(self.vel)
        if self.vel == 0:
            self.flap = False

        #Rotate Bird
        self.image = pygame.transform.rotate(self.image,self.vel * -7)
        #user input

        if user_input[pygame.K_b] and not self.flap and self.rect.y > 0 and self.alive:
            pygame.mixer.Sound.play(yeet_sound)
            self.flap = True
            self.vel = -7
 








class Pipe(pygame.sprite.Sprite):


    def __init__(self,x,y,image, pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.enter, self.exit, self.passed = False, False, False
        self.pipe_type = pipe_type
    def update(self):
        #Move Villian
        self.rect.x -= scroll_speed
        if self.rect.x <= -win_width:
            self.kill()


    #score
        global score
        if self.pipe_type == 'bottom':
            if superman_start_position[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if superman_start_position[0]> self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1
        
class Ground(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y

    def update(self):
        #move ground
        self.rect.x -=scroll_speed
        if self.rect.x <= -win_width:
            self.kill()

        
        

def quit_game():
    # exit game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
#Game Main Method
def main():
    pygame.mixer.music.play(-1)
    os.getcwd()
    global score

    #Instantiate Superman
    superman = pygame.sprite.GroupSingle()
    superman.add(Superman())

    #Instantiate Superman
    superwoman = pygame.sprite.GroupSingle()
    superwoman.add(Superwoman())

    #setup villians
    pipe_timer = 0
    pipes = pygame.sprite.Group()

    # Instantiate Initial Ground
    x_pos_ground, y_pos_ground = 620, 620
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground, y_pos_ground))
    
    run = True
    i = 0
    while run:

        quit_game()
        # Reset Frame
        window.fill((0,0,0))

        #user Input
        user_input = pygame.key.get_pressed()
        #Draw Background
        window.blit(city_image,(0,-70))

        #spawn Ground
        if i % 2:#len(ground) <= 2   :
            ground.add(Ground(win_width, y_pos_ground))
        i += 1
        """
        ground.draw(window)
        pipes.draw(window)
        superman.draw(window)
        """
        #show score
        score_text = font.render("Score: " + str(score), True, (255,255,255))
        window.blit(score_text,(20,20))
        """
        if superman.sprite.alive:
            ground.update()
            pipes.update()
        superman.update(user_input)
        """
        #collison pipes
        collision_pipes = pygame.sprite.spritecollide(superman.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(superman.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            superman.sprite.alive = False
            game_over()



        collision_pipes = pygame.sprite.spritecollide(superwoman.sprites()[0], pipes, False)
        collision_ground = pygame.sprite.spritecollide(superwoman.sprites()[0], ground, False)
        if collision_pipes or collision_ground:
            superwoman.sprite.alive = False
            game_over()





        if pipe_timer <= 0 and superman.sprite.alive and superwoman.sprite.alive:
            x_top, x_bottom = 550, 550
            y_top = random.randint(-100, 300)
                # x_bottom = x_top - random.randint(0,130) + top_enemy_image.get_height()
            y_bottom = y_top + random.randint(100, 300) + bottom_enemy_image.get_height()
            pipes.add(Pipe(x_top, y_top, top_enemy_image, 'top'))
            pipes.add(Pipe(x_bottom, y_bottom, bottom_enemy_image, 'bottom' ))
            pipe_timer = random.randint(180, 250)
        pipe_timer -= 1

        #Draw - Pipes, Ground, and Bird
        #if superman.sprite.alive:

        ground.draw(window)
        pipes.draw(window)
        superman.draw(window)
        superwoman.draw(window)
        # Update - Pipes, Ground, and Bird

        if superman.sprite.alive:
            ground.update()
            pipes.update()
            superman.update(user_input)
            superwoman.update(user_input)
        clock.tick(60)
        pygame.display.update()




def game_over():
    #window.blit(start_image, (win_width // 2 - start_image.get_width() // 2,
                              #win_height // 2 - start_image.get_height() // 2))
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(gone_sound)
    window.blit(game_over_image, (win_width // 2 - game_over_image.get_width() // 2,
                                  win_height // 2 - game_over_image.get_height() // 2))
    user_input = pygame.key.get_pressed()

    if user_input[pygame.K_r]:
        main()

#if __name__ == '__main__':
    #main()
def menu():
    global game_stopped

    while game_stopped:
        quit_game()

        #Draw menu
        window.fill((0,0,0))
        window.blit(city_image, (0,0))
        window.blit(ground_image, Ground(0,520))
        window.blit(superman_image[0],(100,250))
        window.blit(start_image, (win_width // 2 - start_image.get_width() // 2,
                                        win_height // 2 - start_image.get_height() // 2))
        #user Input
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()

        pygame.display.update()


menu()
