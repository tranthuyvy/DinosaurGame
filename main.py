from random import randint
from pygame.font import SysFont
from pygame import display as display
from pygame import image as image
from pygame import init
from pygame import mixer as mixer
from pygame import time as time
from pygame.event import get
from pygame.constants import QUIT, K_SPACE, KEYDOWN

def init_game():
    background_x, background_y = 0, 0
    dinosaur_x, dinosaur_y = 100, 360
    obj_x, obj_y = 1000, 320
    x_velocity, y_velocity = 6, 6
    score = 0
    pausing = False
    bool_s2 = True
    return bool_s2, background_x, background_y, dinosaur_x, dinosaur_y, obj_x, obj_y, x_velocity, y_velocity, score, pausing

def write(x, y, text, font):
    a = font.render(text, True, RED)
    screen.blit(a, (x, y))

def velocity_background(background_x):
    screen.blit(background, (background_x, background_y))
    screen.blit(background, (background_x + 1000, background_y))
    background_x -= x_velocity
    if background_x + 1000 <= 0:
        background_x = 0
    return background_x

def velocity_obj(obj_x, i):
    obj_rect = screen.blit(obj[i], (obj_x, obj_y))
    obj_x -= x_velocity
    if obj_x <= -100:
        obj_x = 1100
        return obj_rect, obj_x, True
    return obj_rect, obj_x, False

def velocity_dinosaur(dinosaur_y, jump, up):
    up += 1
    if up <= 10 or jump:
        dinosaur_rect = screen.blit(dinosaur, (dinosaur_x, dinosaur_y))
    else:
        dinosaur_rect = screen.blit(dinosaur, (dinosaur_x, dinosaur_y - 20))
        if up == 20:
            up = 0
    if 360 >= dinosaur_y >= 100 and jump:
        dinosaur_y -= y_velocity
    else:
        jump = False
    if dinosaur_y < 360 and jump == False:
        dinosaur_y += y_velocity
        up = 0
    return dinosaur_rect, dinosaur_y, jump, up

def colliderect_rect():
    if dinosaur_rect[0] + dinosaur_rect[2] < obj_rect[0] or obj_rect[0] + obj_rect[2] < dinosaur_rect[0]:
        return False
    if dinosaur_rect[1] + dinosaur_rect[3] < obj_rect[1] or dinosaur_rect[1] > obj_rect[1] + obj_rect[3]:
        return False
    return True

def gameOver(pausing, x_velocity, y_velocity):
    if colliderect_rect():
        # if dinosaur_rect.colliderect(obj_rect):
        pausing = True
        write(360, 200, "GAME OVER", font1)
        x_velocity = 0
        y_velocity = 0
    return pausing, x_velocity, y_velocity

def random_obj(x_velocity, score):
    rand_obj = randint(0, 5)  # random object
    score += 1
    if score % 3 == 0 and score <= 27:
        x_velocity += 1
    return rand_obj, x_velocity, score

if __name__ == '__main__':
    init()
    screen = display.set_mode((1000, 500))
    display.set_caption('Game Dinosaur')
    bool_s2, background_x, background_y, dinosaur_x, dinosaur_y, obj_x, obj_y, x_velocity, y_velocity, score, pausing = init_game()

    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    step, rand_obj, rand2 = 0, 1, 1

    font = SysFont('Times New Roman', 20)
    font1 = SysFont('Times New Roman', 40)

    background = image.load('asset/images/background.png')
    write(100, 100, str(background), font)
    dinosaur = image.load('asset/images/dinosaur.png')
    obj = [image.load('asset/images/tree1.png'),
           image.load('asset/images/tree2.png'),
           image.load('asset/images/tree3.png'),
           image.load('asset/images/Cloud1.png'),
           image.load('asset/images/Cloud2.png'),
           image.load('asset/images/cloud3.png')]

    sound1 = mixer.Sound('asset/audio/tick.mp3')
    sound2 = mixer.Sound('asset/audio/te.mp3')

    FPS = 60
    clock = time.Clock()

    jump = False
    running = True
    up = 0
    speed = 1

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        background_x = velocity_background(background_x)
        write(5, 5, "Score: " + str(score), font)

        if x_velocity > 0 and score <= 27:
            speed = str(int(score / 3) + 1)
        write(5, 25, "Speed: " + speed, font)

        if step:
            rand_obj, x_velocity, score = random_obj(x_velocity, score)

        if rand_obj < 3:
            obj_y = 320
        else:
            if 1100 >= obj_x >= 1000:
                obj_y = randint(150, 320)

        obj_rect, obj_x, step = velocity_obj(obj_x, rand_obj)
        dinosaur_rect, dinosaur_y, jump, up = velocity_dinosaur(dinosaur_y, jump, up)
        pausing, x_velocity, y_velocity = gameOver(pausing, x_velocity, y_velocity)

        if pausing and bool_s2:
            mixer.Sound.play(sound2)
            bool_s2 = False

        for event in get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if dinosaur_y == 360:
                        mixer.Sound.play(sound1)
                        jump = True
                    if pausing:
                        bool_s2, background_x, background_y, dinosaur_x, dinosaur_y, obj_x, obj_y, x_velocity, y_velocity, score, pausing = init_game()
        display.flip()
    quit()
