import pygame
from snake import Point, Region, Snake

region = Region(Point(0,0), Point(100,100))
snake = Snake(region)
# snake.head = region.get_rnd_point()

snake.go("右")
if snake.is_die(): pass