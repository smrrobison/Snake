from random import randint

import pygame
import colors


WINDOW_H = 840
WINDOW_W = 800
WINDOW = WINDOW_H, WINDOW_W
SEGMENT_SIZE = 20
SCORE = 0

pygame.init()
pygame.display.set_caption ("Snake")

clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW)

def draw(snake_location, food_position):
    pygame.draw.rect(screen, colors.FOOD, [food_position, (SEGMENT_SIZE, SEGMENT_SIZE)])

    for x, y in snake_location:
        pygame.draw.rect(screen, colors.SNAKE, [x, y, SEGMENT_SIZE, SEGMENT_SIZE])

def move_food(snake_location):
    while True:
        x_pos = randint(1, 39) * SEGMENT_SIZE
        y_pos = randint(2, 41) * SEGMENT_SIZE
        food_pos = (x_pos, y_pos)

        if food_pos not in snake_location:
            return food_pos
        

def slither (snake_location, direction):
    head_x_pos, head_y_pos = snake_location[0]
    if direction == "l":
        head_pos = (head_x_pos - SEGMENT_SIZE, head_y_pos)
    elif direction == "r":
        head_pos = (head_x_pos + SEGMENT_SIZE, head_y_pos)
    elif direction == "u":
        head_pos = (head_x_pos, head_y_pos - SEGMENT_SIZE )
    elif direction == "d":
        head_pos = (head_x_pos,  head_y_pos + SEGMENT_SIZE)

    snake_location.insert(0, head_pos)
    del snake_location[-1]
    
def on_key_press(event, direction):
    #key = event.__dict__["key"]
    if event.key == pygame.K_LEFT or event.key == ord('a'):
        new_direction = "l"
    if event.key == pygame.K_RIGHT or event.key == ord('d'):
        new_direction = "r"
    if event.key == pygame.K_UP or event.key == ord('w'):
        new_direction = "u"
    if event.key == pygame.K_DOWN or event.key == ord('s'):
        new_direction = "d"
    
    opposites = ({"u", "d"}, {"r", "l"})
    if ({new_direction, direction} not in opposites):
        return new_direction
    
    return direction

def check_bite(snake_location):
    head_x, head_y = snake_location[0]
    return ((head_x, head_y) in snake_location[1:])

def check_food(snake_location, food_position):
    if snake_location[0] == food_position:
        snake_location.append(snake_location[-1])
        return True   
def check_wall(snake_location):
    head_x, head_y = snake_location[0]
    new_head_x = head_x
    new_head_y = head_y

    if head_x <= -20:
     new_head_x = WINDOW_W 
    if head_x >= WINDOW_W:
     new_head_x = -20

    if head_y <= 20:
        new_head_y = WINDOW_H 
    if head_y >= WINDOW_H:
        new_head_y = 20 

    return new_head_x, new_head_y

def play():
    global SCORE
    direction = "r"
    snake_location = [(100, 100), (80, 100), (60, 100)]
    food_position = move_food(snake_location)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                direction = on_key_press(event, direction)
        
        screen.fill(colors.BACKGROUND)
        draw(snake_location, food_position)

        font = pygame.font.Font(None, 28)
        text = font.render(f"Score: {SCORE}", True, colors.TEXT)
        screen.blit(text, (10, 10))

        pygame.display.update()

        slither(snake_location, direction)
        snake_location[0] = check_wall(snake_location)
        if check_bite(snake_location):
            return

        if check_food(snake_location, food_position):
            food_position = move_food(snake_location)
            
            SCORE += 1

        clock.tick(25)

def game_over():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        global SCORE
        font = pygame.font.Font(None, 28)
        screen.fill(colors.BACKGROUND)
        text = font.render(f"Score: {SCORE}", True, colors.TEXT)
        end_message = font.render ("Game Over", True, colors.TEXT)
        screen.blit(text, (10, 10))
        screen.blit(end_message, (WINDOW_W/2, WINDOW_H/2))
        pygame.display.update()

        clock.tick(30)

    
play()
game_over()
