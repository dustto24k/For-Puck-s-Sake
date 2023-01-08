import pygame
import pymunk
import math
import numpy as np
from os import path

WINDOW_WIDTH = 565
WINDOW_HEIGHT = 1000
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

GREEN = (0, 255, 0)
SKYBLUE = (25, 189, 255)

GOLD = (212, 175, 55)
SILVER = (216, 216, 216)
BRONZE = (191, 137, 112)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Air Hockey... but it's pinball")
clock = pygame.time.Clock()

space = pymunk.Space()
static_body = space.static_body

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
table_img = pygame.image.load(path.join(img_dir, "table.png")).convert_alpha()
tableframe_img = pygame.image.load(path.join(img_dir, "table_frame.png")).convert_alpha()
striker_img = pygame.image.load(path.join(img_dir, "striker.png")).convert_alpha()
striker_img = pygame.transform.scale(striker_img, (50, 50))
initial_snd = pygame.mixer.Sound(path.join(snd_dir, 'insertcoin.wav'))
hit_snd = pygame.mixer.Sound(path.join(snd_dir, 'hit.wav'))
jackpot_snd = pygame.mixer.Sound(path.join(snd_dir, 'jackpot.wav'))
hit_snd.set_volume(0.6)
pygame.mixer.music.load(path.join(snd_dir, 'PilaPalaParadise.mp3'))
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(loops=-1)

def puck_striker(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 1500
    shape.elasticity = 1
    space.add(body, shape)
    return shape

def puck(radius, pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = 5
    shape.elasticity = 1.01
    space.add(body, shape)
    return shape
pucks = []
puck_r = 18
rows = 5
for col in range(5):
    for row in range(rows):
        pos = (215 + (row * (puck_r * 2 + 1)) + (col * puck_r), 200 + (col * (puck_r * 2 + 1)))
        new_puck = puck(puck_r, pos)
        pucks.append(new_puck)
    rows -= 1
white_puck = puck(puck_r, (WINDOW_WIDTH / 2, 740))
pucks.append(white_puck)

def cushion(poly_dims):
    body = pymunk.Body(body_type = pymunk.Body.STATIC)
    body.position = ((0, 0))
    shape = pymunk.Poly(body, poly_dims)
    shape.elasticity = 0.99
    space.add(body, shape)

cushions = [
    [ (47, 75), (47, 471), (64, 464), (64, 92) ],
    [ (500, 92), (500, 464), (518, 471), (518, 75) ],
    [ (47, 519), (47, 918), (64, 900), (64, 526) ],
    [ (500, 527), (500, 900), (518, 918), (518, 518) ],
    [ (80, 47), (99, 65), (467, 65), (484, 47) ],
    [ (99, 935), (81, 953), (484, 953), (467, 935)]
]

for c in cushions:
    cushion(c)

pocket_r = 27
pockets = [ (50, 43), (40, 495), (50, 946), (512, 946), (525, 495), (512, 43) ]
respawn = [ (477, 911), (477, 494), (477, 88), (87, 88), (87, 494), (87, 911) ]

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_text2(text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    t = font.render(text, True, color)
    screen.blit(t, (x, y))

def draw_text3(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topright = (x, y)
    surf.blit(text_surface, text_rect)

def show_init_screen():
    screen.blit(table_img, (0, 0))
    draw_text(screen, "FOR PUCK'S SAKE", 64, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4, BLACK)
    if tries == 0:
        draw_text(screen, "Move your mouse to control", 22, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, BLACK)
    else:
        draw_text(screen, "HIGH SCORE", 26, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 65, BLACK)
        draw_text2(f"1st", 22, WINDOW_WIDTH / 2 - 71, WINDOW_HEIGHT / 2 - 30,   GOLD)
        draw_text2(f"2nd", 22, WINDOW_WIDTH / 2 - 71, WINDOW_HEIGHT / 2,      SILVER)
        draw_text2(f"3rd", 22, WINDOW_WIDTH / 2 - 71, WINDOW_HEIGHT / 2 + 30, BRONZE)
        draw_text2(f"4th", 22, WINDOW_WIDTH / 2 - 71, WINDOW_HEIGHT / 2 + 60,  BLACK)
        draw_text2(f"5th", 22, WINDOW_WIDTH / 2 - 71, WINDOW_HEIGHT / 2 + 90,  BLACK)
        draw_text3(screen, f"{sorted(score_list, reverse=True)[0]}", 22, WINDOW_WIDTH / 2 + 67, WINDOW_HEIGHT / 2 - 30,   GOLD)
        draw_text3(screen, f"{sorted(score_list, reverse=True)[1]}", 22, WINDOW_WIDTH / 2 + 67, WINDOW_HEIGHT / 2,      SILVER)
        draw_text3(screen, f"{sorted(score_list, reverse=True)[2]}", 22, WINDOW_WIDTH / 2 + 67, WINDOW_HEIGHT / 2 + 30, BRONZE)
        draw_text3(screen, f"{sorted(score_list, reverse=True)[3]}", 22, WINDOW_WIDTH / 2 + 67, WINDOW_HEIGHT / 2 + 60,  BLACK)
        draw_text3(screen, f"{sorted(score_list, reverse=True)[4]}", 22, WINDOW_WIDTH / 2 + 67, WINDOW_HEIGHT / 2 + 90,  BLACK)
            
    draw_text(screen, "Click to begin", 18, WINDOW_WIDTH / 2, WINDOW_HEIGHT * 3 / 4, BLACK)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONUP:
                waiting = False

def show_go_screen():
    screen.blit(table_img, (0, 0))
    draw_text(screen, "GAME OVER", 64, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4, BLACK)
    draw_text(screen, f"You survived for {round(time, 2)} seconds", 22,
              WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 15, BLACK)
    draw_text(screen, f"Final Score: {score}", 22,
              WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 15, BLACK)
    draw_text(screen, "Click to end game", 18, WINDOW_WIDTH / 2, WINDOW_HEIGHT * 3 / 4, BLACK)
    pygame.display.update()

def dist(p, q):
    lx = abs(p.body.position[0] - q[0])
    ly = abs(p.body.position[1] - q[1])
    return math.sqrt(math.pow(lx, 2) + math.pow(ly, 2))

score_list = [0] * 20
done = False
tries = 0
time = 0
while not done:
    
    score = 0
    multiplier = 1
    initial = True
    gameover = False
    while not gameover:

        clock.tick(120)
        space.step(1 / 120)

        last = 0
        now = pygame.time.get_ticks()
        if now - last >= 10 * 60000:
            last = now
            multiplier *= 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = gameover = True

        for p in pucks[:-1]:
            for i in range(len(pockets)):
                pocket = pockets[i]
                if dist(p, pocket) <= pocket_r:
                    p.body.position = respawn[i]

            if dist(p, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)) > 1149:
                p.body.position = (
                    np.random.randint(low=87, high=477),
                    np.random.randint(low=88, high=911)
                    )
            elif dist(p, pucks[-1].body.position) <= pocket_r * 2 + 1:
                score += 3 * multiplier
                hit_snd.play()

        for i in range(len(pockets)):
            pocket = pockets[i]
            if dist(pucks[-1], (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)) > 1149 or dist(pucks[-1], pocket) <= pocket_r:
                jackpot_snd.play()
                time = temp_time - time
                score_list[tries] = score
                show_go_screen()
                waiting = True
                while waiting:
                    clock.tick(60)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            done = gameover = True
                        elif event.type == pygame.MOUSEBUTTONUP:
                            waiting = False
                            gameover = True

        screen.fill(WHITE)
        screen.blit(table_img, (0, 0))


        for i, puck in enumerate(pucks[:-1]):
            pygame.draw.circle(screen, RED, (puck.body.position[0], puck.body.position[1]), puck_r, 0)
        # portal visualization
        # pygame.draw.circle(screen, SKYBLUE, (pucks[9].body.position[0], pucks[9].body.position[1]), puck_r, 0)
        # pygame.draw.circle(screen, GREEN, (pucks[2].body.position[0], pucks[2].body.position[1]), puck_r, 0)
        pygame.draw.circle(screen, BLACK, (pucks[-1].body.position[0], pucks[-1].body.position[1]), puck_r, 0)
        
        striker_r = 25
        if initial == True:
            show_init_screen()
            striker = puck_striker(striker_r, pygame.mouse.get_pos())
            initial_snd.play()
            pucks[-1].body.apply_impulse_at_local_point((0, 500 * -15), (0, 0))
            initial = False
        else:
            temp_time = pygame.time.get_ticks() / 1000
        
        striker.body.position = pygame.mouse.get_pos()
        screen.blit(striker_img, (striker.body.position[0] - striker_r, striker.body.position[1] - striker_r))
        screen.blit(tableframe_img, (0, 0))
        draw_text(screen, str(score), 18, WINDOW_WIDTH / 2, 10, WHITE)
        pygame.display.update()
    
    pymunk.Space.remove(space, striker)
    tries += 1

    reset = []
    rows = 5
    for col in range(5):
        for row in range(rows):
            pos = (215 + (row * (puck_r * 2 + 1)) + (col * puck_r), 200 + (col * (puck_r * 2 + 1)))
            reset.append(pos)
        rows -= 1
    reset.append((WINDOW_WIDTH / 2, 740))

    for p in range(len(pucks)):
        pucks[p].body.velocity = (0, 0)
        pucks[p].body.position = reset[p]

pygame.quit()