import pygame


class Text:
    def __init__(self, txt):
        font = pygame.font.SysFont(txt, size)
        self.surface = font.render(txt, True, (0, 0, 0))
        self.rect = self.surface.get_rect()

    def topleft(self, pos_x, pos_y):
        self.rect.topleft = (pos_x, pos_y)
        window.blit(self.surface, self.rect)


pygame.init()
window_x = 360
window_y = 480
window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("字型瀏覽器")

size = 30
y = 0
font_list = pygame.font.get_fonts()
min_y = window_y - len(font_list) * (size + 1)
wheel_speed = 48

running = True
while running:
    window.fill((255, 255, 255))
    start = -y // size
    end = start + window_y // size + 1
    t = y + start * size
    for f in font_list[start:end]:
        Text(f).topleft(20, t)
        t += size
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEWHEEL:
            dy = event.y * wheel_speed
            y += dy
            if y > 0:
                y = 0
            elif y < min_y:
                y = min_y
            else:
                window.scroll(0, dy)
    pygame.display.update()
