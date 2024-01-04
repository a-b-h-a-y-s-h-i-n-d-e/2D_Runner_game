import pygame
from sys import exit
import time
from random import randint

#initializing pygame

def display_score():
    
    current_time = (pygame.time.get_ticks() // 1000) - start_time
    score_surface = test_font.render(f'Score : {current_time}' , False , (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface , score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 3.5
            
            screen.blit(snail_surface,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player , obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect): 
                game_over.play()
                return False
            
    return True

def player_animation():
    global player_surface , player_index
    
    if player_rect.bottom < 320 :
        player_surface = player_jump
    else:
        player_index += 0.2
        if player_index >= len(player_walk): player_index = 0
        player_surface = player_walk[int(player_index)]
        
    
pygame.init()

jump_sound = pygame.mixer.Sound('sound/mario_jump2.wav')
jump_sound.set_volume(0.7) 
start_sound = pygame.mixer.Sound('sound/shit.mp3')
theme_sound = pygame.mixer.Sound('sound/sa.mp3')
game_over = pygame.mixer.Sound('sound/over.mp3')
theme_sound.play()
start_sound.play()

screen = pygame.display.set_mode((800 , 400))
pygame.display.set_caption('Mad Runner')
clock = pygame.time.Clock()

test_font = pygame.font.Font('font/Blomberg-8MKKZ.ttf',50)
game_active = False
start_time = 0
score = 0



sky_surface = pygame.image.load('graphics/sky.jpg').convert_alpha()
sky_surface = pygame.transform.scale(sky_surface , (800,320))
ground_surface = pygame.image.load('graphics/ground.png').convert_alpha()
ground_surface =pygame.transform.scale(ground_surface , (800,100))



#Obstacles
snail_surface = pygame.image.load('graphics/enemy.png').convert_alpha()
snail_surface =pygame.transform.scale(snail_surface , (40,40))
snail_rect = pygame.Rect(0, 0, 40, 40)                                     


obstacles_rect_list = []

player_walk1 = pygame.image.load('graphics/char_running-removebg-preview.png').convert_alpha()
player_walk1 =pygame.transform.scale(player_walk1 , (120,120))
player_walk2 = pygame.image.load('graphics/char_running2-removebg-preview.png').convert_alpha()
player_walk2 =pygame.transform.scale(player_walk2 , (120,120))
player_walk = [player_walk1 , player_walk2]
player_jump =  pygame.image.load('graphics/cahr_running3-removebg-preview.png').convert_alpha()
player_index = 0

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(topleft = (80,200))
player_rect.width = 50
player_rect.height = 110 
player_gravity = 0

#Intro scene
player_stand = pygame.image.load('graphics/enemy.png').convert_alpha()
player_stand = pygame.transform.scale(player_stand , (170,170))
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render('Mad Runner',False,(11,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render("press space to run",False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,320))

spacebar_surface = pygame.image.load('graphics/spacebar.png')
spacebar_surface = pygame.transform.scale(spacebar_surface , (150,150))
spacebar_rect = spacebar_surface.get_rect(midleft = (50,200))
arrow_surface = pygame.image.load('graphics/arrowkeys.png')
arrow_surface = pygame.transform.scale(arrow_surface,(150,150))
arrow_rect = arrow_surface.get_rect(midright = (700,200))
#TImer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer , 1500)
player_speed = 15
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
            
        keys = pygame.key.get_pressed()
        if game_active:    
            if keys[pygame.K_LEFT]:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_rect.x += player_speed

            if event.type == pygame.KEYDOWN:
                if player_rect.bottom >= 320:
                    if event.key == pygame.K_SPACE:
                        player_gravity =- 14
                        jump_sound.play()
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
             
                    start_time = (pygame.time.get_ticks() // 1000)
                        
        if event.type == obstacle_timer and game_active:
            obstacles_rect_list.append(snail_surface.get_rect(topright = (randint(900,1100),290)))

    if game_active:   
        screen.blit(sky_surface , (0,0))
        screen.blit(ground_surface,(0,300))

        score = display_score()        
        
  
        
        #Player
        player_gravity += 0.5
        player_rect.y += player_gravity
        if player_rect.bottom >= 320:
            player_rect.bottom = 320
            player_animation()
        screen.blit(player_surface , player_rect)

        #obstacle movement
        obstacles_rect_list = obstacle_movement(obstacles_rect_list)
        
        #collision
        game_active = collisions(player_rect , obstacles_rect_list)        
                
    else:
        
        # screen.fill((94,129,162))
        screen.fill((00,00,00))
        screen.blit(player_stand , player_stand_rect)
        obstacles_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        
        score_msg = test_font.render(f'Your score : {score}',False,(111,196,169))
        score_msg_rect = score_msg.get_rect(center = (400,360))
        if score == 0:
            screen.blit(game_message,game_message_rect)
        else:
            screen.blit(score_msg,score_msg_rect)
            
        screen.blit(game_name,game_name_rect)
        screen.blit(game_message,game_message_rect)
        screen.blit(spacebar_surface,spacebar_rect)
        screen.blit(arrow_surface,arrow_rect)
        # start_sound.play()
        
    pygame.display.update()
    clock.tick(60)
    