import pygame
import random
from sys import exit


class Text:
    def __init__(self, txt, size, color, font):
        font = pygame.font.SysFont(font, size)
        self.surface = font.render(txt, True, color)
        self.rect = self.surface.get_rect()

    def midleft(self, x, y):
        self.rect.midleft = (x, y)
        window.blit(self.surface, self.rect)


class Snake:
    def __init__(self, c1, c2, head):
        self.color1 = c1
        self.color2 = c2
        self.head = head
        self.body = [head]
        self.direction = 'RIGHT'
        self.new_direction = 'RIGHT'
        length = 4
        for i in range(length - 1):
            self.head[0] += unit
            self.body.insert(0, list(self.head))


class Fruit:
    def __init__(self):
        self.pos = [0, 0]
        self.spawn()

    def spawn(self):
        self.pos = [random.randrange(0, canvas_x, unit),
                    random.randrange(0, canvas_y, unit)]
        if self.pos in snake.body:
            self.spawn()


black = (0, 0, 0)
grey = (85, 85, 85)
white = (255, 255, 255)
red = (229, 46, 8)
darkRed = (157, 31, 6)
green = (64, 201, 73)
darkGreen = (36, 127, 42)
blue = (78, 124, 246)
darkBlue = (9, 53, 174)
purple = (182, 72, 242)
darkPurple = (116, 12, 172)

pygame.init()
window = pygame.display.set_mode((780, 780))
pygame.display.set_caption("Pygame貪食蛇")

canvas_x = 720
canvas_y = 630
canvas = pygame.Surface((canvas_x, canvas_y))

background = pygame.image.load("res/background.png").convert()
border = pygame.image.load("res/border.png").convert()
face = pygame.image.load("res/face.png").convert_alpha()
game_over = pygame.image.load("res/game_over.png").convert_alpha()

pygame.mixer.init()
bgm = pygame.mixer.Sound("res/bgm.wav")
fruit_sfx = pygame.mixer.Sound("res/fruit.wav")
game_over_sfx = pygame.mixer.Sound("res/game_over.wav")
bgm.play(-1)

game_speed = 8
unit = 30

while True:

    score = 0
    snake = Snake(green, darkGreen, [0, 0])
    fruit = Fruit()

    while True:

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < 1000 // game_speed:
            pygame.event.pump()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.new_direction = 'RIGHT'
                elif event.key == pygame.K_LEFT:
                    snake.new_direction = 'LEFT'
                elif event.key == pygame.K_DOWN:
                    snake.new_direction = 'DOWN'
                elif event.key == pygame.K_UP:
                    snake.new_direction = 'UP'

        if snake.new_direction == 'RIGHT' and snake.direction != 'LEFT':
            snake.direction = 'RIGHT'
        elif snake.new_direction == 'LEFT' and snake.direction != 'RIGHT':
            snake.direction = 'LEFT'
        elif snake.new_direction == 'DOWN' and snake.direction != 'UP':
            snake.direction = 'DOWN'
        elif snake.new_direction == 'UP' and snake.direction != 'DOWN':
            snake.direction = 'UP'

        if snake.direction == 'RIGHT':
            snake.head[0] += unit
        elif snake.direction == 'LEFT':
            snake.head[0] -= unit
        elif snake.direction == 'DOWN':
            snake.head[1] += unit
        elif snake.direction == 'UP':
            snake.head[1] -= unit

        snake.body.insert(0, list(snake.head))

        if snake.head == fruit.pos:
            fruit_sfx.play()
            fruit.spawn()
            score += 1
        else:
            snake.body.pop()

        if not (0 <= snake.head[0] < canvas_x):
            break
        if not(0 <= snake.head[1] < canvas_y):
            break
        if snake.head in snake.body[1:]:
            break

        canvas.blit(background, (0, 0))

        pygame.draw.rect(canvas, grey, (snake.head[0], snake.head[1], unit + 2, unit + 2))
        for body in snake.body[1:]:
            pygame.draw.rect(canvas, grey, (body[0] + 1, body[1] + 1, unit, unit))

        pygame.draw.rect(canvas, snake.color1, (snake.head[0] - 1, snake.head[1] - 1, unit + 2, unit + 2))
        pygame.draw.rect(canvas, snake.color2, (snake.head[0] - 1, snake.head[1] - 1, unit + 2, unit + 2), 2)

        for body in snake.body[1:]:
            pygame.draw.rect(canvas, snake.color1, (body[0], body[1], unit, unit))
            pygame.draw.rect(canvas, snake.color2, (body[0], body[1], unit, unit), 2)

        canvas.blit(face, snake.head)

        pygame.draw.rect(canvas, grey, (fruit.pos[0] + 3, fruit.pos[1] + 3, unit - 4, unit - 4), 0, 3)
        pygame.draw.rect(canvas, red, (fruit.pos[0] + 2, fruit.pos[1] + 2, unit - 4, unit - 4), 0, 3)
        pygame.draw.rect(canvas, darkRed, (fruit.pos[0] + 2, fruit.pos[1] + 2, unit - 4, unit - 4), 2, 3)

        window.blit(border, (0, 0))
        window.blit(canvas, (30, 120))
        Text(str(score), 45, white, "impact").midleft(90, 45)

        pygame.display.update()

    game_over_sfx.play()
    window.blit(game_over, (0, 0))
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False