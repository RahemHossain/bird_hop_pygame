import pygame
from random import randint
from sys import exit

pygame.init()

# Program Settings
score = 0
previous_score = 0
show = 0
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Bird Hop')
clock = pygame.time.Clock()
start_time = 0
game_active = False

# Fonts
test_font = pygame.font.Font('fonts/font2.ttf', 50)
score_font = pygame.font.Font('fonts/score.otf', 40)
pixel_font = pygame.font.Font('fonts/pixel.ttf', 80)
high_font = pygame.font.Font('fonts/pixel.ttf', 30)

# Sounds
start_sound = pygame.mixer_music.load('audio/Jolly.mp3')
hop_sound = pygame.mixer.Sound('audio/fly.mp3')
coin_sound = pygame.mixer.Sound('audio/coin.mp3')
high_score_sound = pygame.mixer.Sound('audio/high_score.mp3')

# Start Game Settings
sky_surface = pygame.image.load('sprites/sky.png').convert()
ground_surface = pygame.image.load('sprites/ground2.png').convert()

cloud_surface = pygame.image.load('sprites/cloud.png').convert_alpha()
cloud_rect = cloud_surface.get_rect(midbottom=(900, 150))

cloud2_surface = pygame.image.load('sprites/cloud2.png').convert_alpha()
cloud2_rect = cloud2_surface.get_rect(midbottom=(800, 200))
cloud_rect_list = []

text_surface = test_font.render('Flappy Bord', False, 'White')
text_rect = text_surface.get_rect(center=(400, 50))

# False Game Settings
player_stand = pygame.image.load('sprites/bird_standing.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 3)
player_stand_rect = player_stand.get_rect(center=(400, 200))

intro_text = test_font.render('Bird Hop', False, 'White')
intro_text_rect = intro_text.get_rect(midtop=(400, 10))

instruction = pixel_font.render('Click Space To Play!', False, 'Gray')
instruction_rec = instruction.get_rect(center=(400, 350))

# Players Settings
bird_surface = pygame.image.load('sprites/bird_standing.png').convert_alpha()
bird_rect = bird_surface.get_rect(midbottom=(80, 300))
bird_walk_1 = pygame.image.load('sprites/bird_hop.png').convert_alpha()
bird_air = pygame.image.load('sprites/bird_air.png').convert_alpha()
bird_list = [bird_surface, bird_walk_1]
player_index = 0
bird_gravity = 0
bird_surface = bird_list[player_index]

# Enemy Settings
cat_surface = pygame.image.load('sprites/cat.png').convert_alpha()
cat_rect = cat_surface.get_rect(midbottom=(600, 300))
cat_surface2 = pygame.image.load('sprites/cat_run.png').convert_alpha()
cat_index = 0
cat_frames = [cat_surface, cat_surface2]
cat_surface = cat_frames[cat_index]

bee_index = 0
bee_surface = pygame.image.load('sprites/bee.png').convert_alpha()
bee_surface2 = pygame.image.load('sprites/bee_fly.png').convert_alpha()
bee_frames = [bee_surface, bee_surface2]
bee_surface = bee_frames[bee_index]

boss_index = 0
boss_surf = pygame.image.load('sprites/boss.png').convert_alpha()
boss_surf2 = pygame.image.load('sprites/boss2.png').convert_alpha()
boss_surf3 = pygame.image.load('sprites/boss_stand.png').convert_alpha()
boss_frames = [boss_surf,boss_surf3, boss_surf2]
boss_spawn = False

boss_surface = boss_frames[boss_index]

mob_rect_list = []


# coin

coin_surface = pygame.image.load('sprites/bird coin.png').convert_alpha()
coins = 0
coin_rect_list = []



# Functions
def player_animation():
    global player_index
    global bird_surface
    if bird_rect.bottom < 300:
        bird_surface = bird_air
    else:
        player_index += 0.1
        if player_index >= len(bird_list):
            player_index = 0
        bird_surface = bird_list[int(player_index)]




def display_score():
    current_time = int((pygame.time.get_ticks() / 1000) - start_time + coins)
    score_surf = score_font.render(str(current_time), False, 'Red')
    score_rect = score_surf.get_rect(midbottom=(400, 75))

    screen.blit(score_surf, score_rect)
    return current_time

def coin(list):
    coin_list = []
    if len(list) == 0:
        coin_rect_list.append(coin_surface.get_rect(center=(900, randint(50, 250))))
    for rect in list:
        rect.x -= 5
        if rect.x > -100:
            screen.blit(coin_surface, rect)
            coin_list.append(rect)
            return coin_list



def mob_movement(mob_list):
    if mob_list != []:
        for mob_rect in mob_list:
            mob_rect.x -= 5
            if mob_rect.bottom == 300:
                screen.blit(cat_surface, mob_rect)
            elif mob_rect.bottom == 299:
                mob_rect.x -= 1
                screen.blit(boss_surf, mob_rect)
            else:
                screen.blit(bee_surface, mob_rect)
        mob_list = [mob for mob in mob_list if mob.x > -100]

        return mob_list
    else:
        return []


def collisions(player, mobs):
    if mobs:
        for mob_rect in mobs:
            if player.colliderect(mob_rect):
                return False
    return True


def cloud_movement(cloud_rect_list):
    if cloud_rect_list != []:
        for cloud_rect in cloud_rect_list:
            cloud_rect.x -= 5
            if cloud_rect.bottom == 150:
                screen.blit(cloud_surface, cloud_rect)
            else:
                screen.blit(cloud2_surface, cloud_rect)
        cloud_rect_list = [cloud_rect for cloud_rect in cloud_rect_list if cloud_rect.x > -100]
        return cloud_rect_list
    else:
        return []


# Custom Events
mob_timer = pygame.USEREVENT + 1
pygame.time.set_timer(mob_timer, 1500)

cat_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(cat_animation_timer, 500)

bee_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(bee_animation_timer, 200)

background_timer = pygame.USEREVENT + 3
pygame.time.set_timer(background_timer, 2000)

false_game_timer = pygame.USEREVENT + 4
pygame.time.set_timer(false_game_timer, 500)

coin_timer = pygame.USEREVENT + 5
pygame.time.set_timer(coin_timer, 1000)

# gives a chance for human enemy to spawn
hard_timer = pygame.USEREVENT + 6
pygame.time.set_timer(hard_timer, 20000)

boss_animation = pygame.USEREVENT + 7
pygame.time.set_timer(boss_animation, 100)

while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:


            show = 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(hop_sound)
                    if bird_rect.bottom >= 300:
                        bird_gravity = -20

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bird_rect.collidepoint(event.pos):
                    if bird_rect.bottom >= 300:
                        bird_gravity = -20

            # CHECKS FOR CUSTOM EVENTS
            if event.type == mob_timer:
                mob = randint(0, 2)
                if mob == 1:
                    mob_rect_list.append(cat_surface.get_rect(midbottom=(randint(900, 1100), 300)))
                elif mob == 2:
                    mob_rect_list.append(bee_surface.get_rect(midbottom=(randint(900, 1100), randint(100, 250))))
                else:
                    if boss_spawn == True:
                        mob_rect_list.append(boss_surf.get_rect(midbottom=(randint(800, 1000), 299)))
                        boss_spawn = False
                    else:
                        if randint(0, 1) == 1:
                            mob_rect_list.append(cat_surface.get_rect(midbottom=(randint(900, 1100), 300)))

                        else:
                            mob_rect_list.append(bee_surface.get_rect(midbottom=(randint(900, 1100), randint(100, 250))))


            if event.type == cat_animation_timer:
                if cat_index == 0:
                    cat_index = 1
                else:
                    cat_index = 0
                cat_surface = cat_frames[cat_index]
            if event.type == boss_animation:
                if boss_index == 0:
                    boss_index = 1
                elif boss_index == 1:
                    boss_index = 2
                else:
                    boss_index = 0
                boss_surf = boss_frames[boss_index]
            if event.type == bee_animation_timer:
                if bee_index == 0:
                    bee_index = 1
                else:
                    bee_index = 0
                bee_surface = bee_frames[bee_index]
            if event.type == background_timer:
                if randint(0, 2) == 1:
                    cloud_rect_list.append(cloud2_surface.get_rect(midbottom=(randint(800, 1000), 200)))
                else:
                    cloud_rect_list.append(cloud_surface.get_rect(midbottom=(randint(800, 1000), 150)))
            if event.type == coin_timer:
                if randint(0,2) == 1:
                    coin_rect_list.append(coin_surface.get_rect(center=(900, randint(50, 200))))
            if event.type == hard_timer:

                boss_spawn = True




        else:
            screen.fill('Blue')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.set_volume(0.6)
                    pygame.mixer.music.play(-1)
                    game_active = True
                    mob_rect_list = []
                    boss_spawn = False
                    coin_rect_list = []
                    bird_rect.midbottom = (80, 300)
                    bird_gravity = 0
                    start_time = pygame.time.get_ticks() / 1000
            if event.type == false_game_timer:

                if randint(0,2) == 1:
                    show = 1
                else:
                    show = 0
                    continue


    if game_active == True:
        # displays score and background
        score = display_score()
        screen.blit(sky_surface, (0, 0))

        cloud_rect_list = cloud_movement(cloud_rect_list)
        screen.blit(ground_surface, (0, 300))
        pygame.draw.rect(screen, 'Black', text_rect, 1, 14, 14, 14)
        pygame.draw.rect(screen, 'Black', text_rect, 5, 10)

        player_animation()
        screen.blit(bird_surface, bird_rect)

        coin(coin_rect_list)
        point = collisions(bird_rect, coin_rect_list)
        if point == False:
            pygame.mixer.Sound.play(coin_sound)
            coins += 3
            coin_rect_list = []

            # jump boost



        display_score()

        # entity movements

        mob_rect_list = mob_movement(mob_rect_list)


        # players gravity
        bird_gravity += 1
        bird_rect.y += bird_gravity
        if bird_rect.bottom >= 300:
            bird_rect.bottom = 300









        game_active = collisions(bird_rect, mob_rect_list)








    else:

        # Death Screen


        coins = 0
        screen.fill(('black'))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(intro_text, intro_text_rect)
        score_post = pixel_font.render('SCORE: ' + str(score), False, ('White'))
        score_rect = score_post.get_rect(center=(150, 200))
        if show == 1:

            screen.blit(instruction, instruction_rec)
        else:

            show = 1
        if score == 0:
            screen.blit(instruction, instruction_rec)
        else:
            screen.blit(score_post, score_rect)
            if score > previous_score:
                pygame.mixer.Sound.play(high_score_sound)
                previous_score = score


            high_score = high_font.render('HIGH SCORE: ' + str(previous_score), False, ('red'))
            high_score_rec = high_score.get_rect(midtop=(150, 150))

            screen.blit(high_score, high_score_rec)
    pygame.display.update()
    clock.tick(60)
