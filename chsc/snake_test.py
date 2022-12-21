import pygame
import sys, random

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)

WINDOW_W = 800
WINDOW_H = 600
BLOCK_SIZE = 25

pygame.init()
pygame.mixer.init() # 進階設計：遊戲聲音控制
gameDisplay = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
FPS = 5

font = pygame.font.SysFont(None, 40)
font_title = pygame.font.SysFont(None, 60)
target = pygame.image.load("chsc/assets/target.png")
target = pygame.transform.scale(target, (BLOCK_SIZE, BLOCK_SIZE))


#------------------------------------------------------------------------------------

def draw_snake(snake_loc_list):
    '''將蛇的方塊座標繪製到畫面上'''
    head_x = snake_loc_list[-1][0]
    head_y = snake_loc_list[-1][1]
    pygame.draw.rect(gameDisplay, red, [head_x, head_y, BLOCK_SIZE, BLOCK_SIZE])
    for [body_x, body_y] in snake_loc_list[:-1]:
        pygame.draw.rect(gameDisplay, purple, [body_x, body_y, BLOCK_SIZE, BLOCK_SIZE])

def draw_target(target_x, target_y):
    '''功能：將食物座標繪製到畫面上'''
    gameDisplay.blit(target, [target_x, target_y])


def msg_to_screen(msg, color, x, y, isTitle=False):
    '''功能：將文字訊息顯示在畫面上'''
    text = ""
    if isTitle:
        text = font_title.render(msg, True, color)
    else:
        text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(x, y))
    gameDisplay.blit(text, text_rect)

def generate_rand_target_loc(rand_x, rand_y):
    '''功能：隨機產生目標（食物）位置'''
    rand_x = random.randint(0, WINDOW_W/BLOCK_SIZE-1)*BLOCK_SIZE
    rand_y = random.randint(0, WINDOW_H/BLOCK_SIZE-1)*BLOCK_SIZE
    return rand_x, rand_y

def unpause():
    '''進階設計：遊戲繼續'''
    global pause
    pause = False

def paused():
    '''進階設計：遊戲暫停'''
    while pause:
        msg_to_screen("Pause,Press C to countinue.",white, WINDOW_W / 2, WINDOW_H / 2, True)
        pygame.mixer.music.pause()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                unpause()   # 遊戲繼續
        
        pygame.display.update()
        pygame.mixer.music.unpause()
        
#-----------------------------------------------------------------------------

def game_loop():
    '''功能：遊戲主迴圈'''
    # 遊戲初始化（每一輪都會重新開始）
    game_exit = False
    game_over = False
    global pause
    pause = False
    
    head_x = WINDOW_W / 4 ; head_y = WINDOW_H / 2
    head_x_change = 0 ; head_y_change = 0 
    rand_x = 0 ; rand_y = 0
    snake_loc_list = []
    snake_len = 1
    score = 0

    pygame.mixer.music.load("chsc/assets/main_theme.ogg") #背景音樂
    pygame.mixer.music.play(-1)
    death = pygame.mixer.Sound("chsc/assets/death.wav") #遊戲結束音效
    got = pygame.mixer.Sound("chsc/assets/coin.ogg") #吃到食物音效
    #功能：隨機產生目標（食物）位置
    target_x, target_y = generate_rand_target_loc(rand_x, rand_y)
    
    while not game_exit:
        
        # 遊戲結束（重新開始）畫面
        while game_over == True:
            death.play()
            pygame.mixer.music.stop()
            gameDisplay.fill(red)
            msg_to_screen("Died! Press R to restart or Q to quit.",white, WINDOW_W / 2, WINDOW_H / 2, True)
            msg_to_screen(f"Score: {score}", white, WINDOW_W / 2, WINDOW_H / 3)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_loop()
                    if event.key == pygame.K_q:
                        game_exit = True
                        game_over = False
                elif event.type == pygame.QUIT:
                    game_exit = True
                    game_over = False
            pygame.display.update()
        
        # 遊戲暫停
        while pause:
            paused()

        # 遊戲進行畫面—
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            #偵測到按鍵按下事件
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    head_x_change = -BLOCK_SIZE
                    head_y_change = 0
                if event.key == pygame.K_RIGHT:
                    head_x_change = BLOCK_SIZE
                    head_y_change = 0
                if event.key == pygame.K_UP:
                    head_x_change = 0
                    head_y_change = -BLOCK_SIZE
                if event.key == pygame.K_DOWN:
                    head_x_change = 0
                    head_y_change = BLOCK_SIZE
                if event.key == pygame.K_p:
                    pause = True

        #head_x_change = BLOCK_SIZE # 測試蛇是可以正確移動的，開始製作專案時請將本行刪除
        head_x += head_x_change
        head_y += head_y_change
        # 更新蛇各節點位置               
        snake_loc_list.append((head_x, head_y))
        while len(snake_loc_list) > snake_len:
            snake_loc_list.remove(snake_loc_list[0])
        #print("snake_len:", snake_len, "\nsnake_loc_list:", snake_loc_list) #偵錯用
        
        # 食物偵測
        if head_x == target_x and head_y == target_y:
            got.play()
            target_x, target_y = generate_rand_target_loc(rand_x, rand_y)
            snake_len += 1
            score += 1

        # 邊界碰撞偵測
        if not (0 <= head_x < WINDOW_W and 
                0 <= head_y < WINDOW_H):
            game_over = True

        # 進階設計:穿牆
        # if head_x >= WINDOW_W:
        #     head_x = -BLOCK_SIZE
        # elif head_x < 0:
        #     head_x = WINDOW_W
        # if head_y >= WINDOW_H:
        #     head_y = -BLOCK_SIZE
        # elif head_y < 0:
        #     head_y = WINDOW_H
        
        # 身體重疊偵測        
        for i in range(snake_len-2):
            if snake_loc_list[i] == snake_loc_list[-1]:
                game_over = True
                death.play()

        gameDisplay.fill(black)
        msg_to_screen(f"Score: {score}", white, 60, 20)
        draw_snake(snake_loc_list)
        draw_target(target_x, target_y)
        pygame.display.update()# 畫面更新



        clock.tick(FPS)

    pygame.quit()

game_loop()
