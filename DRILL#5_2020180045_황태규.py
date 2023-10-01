from pico2d import *
import random

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand_arrow = load_image('hand_arrow.png')

target_x, target_y = random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)
direction = 0  # 0: left, 1: right

move_speed = 20 #여기서 속도를 조절할 수 있음

def set_random_target():
    global target_x, target_y
    target_x, target_y = random.randint(50, TUK_WIDTH - 50), random.randint(50, TUK_HEIGHT - 50) #화면 밖으로 나가지 않도록

def move_towards_target(x, y):
    global direction
    dx, dy = 0, 0
    distance_x = target_x - x
    distance_y = target_y - y
    theta = math.atan2(distance_y, distance_x)
    dx = move_speed * math.cos(theta)
    dy = move_speed * math.sin(theta)

    if dx > 0:
        direction = 1
    else:
        direction = 0

    if math.sqrt((x+dx - target_x)**2 + (y+dy - target_y)**2) < move_speed:
        x, y = target_x, target_y
        set_random_target()
    else:
        x += dx
        y += dy

    return x, y


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
hide_cursor()

while running:
    x, y = move_towards_target(x, y)
    
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    hand_arrow.draw(target_x, target_y)
    
    if direction == 1:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
    else:
        character.clip_draw(frame * 100, 100 * 0, 100, 100, x, y)
    
    update_canvas()
    frame = (frame + 1) % 8
    handle_events()
    delay(0.05)

close_canvas()
