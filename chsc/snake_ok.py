from random import randrange
import pygame, sys
import pygame.display as display
import pygame.event as event

# 定義頻色變數
redColour = pygame.Color(255, 0, 0)
greenColour = pygame.Color(0, 255, 0)
blackColour = pygame.Color(0, 0, 0)
whiteColour = pygame.Color(255, 255, 255)
greyColour = pygame.Color(150, 150, 150)

def theEnd():
    '''結束程式'''
    pygame.quit()
    sys.exit()

def gameOver(dispSurface, score):
    '''死了，顯示分數，遊戲結束'''
    txtFont = pygame.font.SysFont('arial.ttf', 54)  # 建立字型物件供顯示文字訊息時用
    
    # 顯示「Game Over!」文字
    # 1.產生文字圖形物件
    txtSurf = txtFont.render('Game Over!', True, greyColour)
    # 2.取得圖形的距形物件，用來設定要顯示的位置及範圍
    txtRect = txtSurf.get_rect()    
    txtRect.midbottom = (dispSurface.get_rect().centerx, txtFont.get_height())
    # 3.將文字圖形顯示於矩形的位置範圍
    dispSurface.blit(txtSurf, txtRect)  

    # 同上，顯示分數
    txtSurf = txtFont.render('Score:' + str(score), True, greyColour)
    txtRect = txtSurf.get_rect()
    txtRect.midtop = (dispSurface.get_rect().centerx, txtFont.get_height())
    dispSurface.blit(txtSurf, txtRect)
    
    display.update()     # 更新畫面
    
    time.sleep(2)   # 程式暫停2秒
    theEnd()        # 結束程式

# 主程式
def main():

    # 初始化pygame
    pygame.init()

    # 建立clock時鐘物件，遊戲速度控制用
    fpsClock = pygame.time.Clock()
    
    # 創建遊戲顯示畫布(pygame顯示層)
    dispSurface = display.set_mode((600, 460))
    display.set_caption('Snake Game')    # 設定視窗抬頭
    
    # 初始化變數
    snakePosition = (100, 100)          # 貪吃蛇 蛇頭的位置
    snakeSegments = [snakePosition]     # 貪吃蛇 蛇的身體，初始為一個單位
    raspberryPosition = (300, 300)      # 樹莓的初始位置
    direction = '右'                    # 初始方向為右
    score = 0                           # 初始得分
    
    while True:
        fpsClock.tick(7)    # 控制遊戲速度

        # 逐一檢測pygame的事件佇列(Queue)，看看發生了哪些事件
        for e in event.get():
            
            # 若按「X」關閉視窗
            if e.type == pygame.QUIT:   
                theEnd()    # 不顯示數分，直接結束程式

            # 若有按鍵被按下
            elif e.type == pygame.KEYDOWN:
                
                # 看看是按下什麼鍵 及 蛇目前的移動方向 來決定再來移動方向
                if e.key == pygame.K_RIGHT and direction in '上下':
                    direction = '右'
                if e.key == pygame.K_LEFT and direction in '上下':
                    direction = '左'
                if e.key == pygame.K_UP and direction in '左右':
                    direction = '上'
                if e.key == pygame.K_DOWN and direction in '左右':
                    direction = '下'
                if e.key == pygame.K_ESCAPE:
                    event.post(event.Event(pygame.QUIT))
                
        # 根據移動方向來決定(移動)新蛇頭的座標
        (x, y) = snakePosition
        if direction == '右':
            snakePosition = (x+20, y)
        elif direction == '左':
            snakePosition = (x-20, y)
        elif direction == '下':
            snakePosition = (x, y+20)
        else:  # direction == '上':
            snakePosition = (x, y-20)
        
        # 先在蛇身上加入新蛇頭(長度增加)
        snakeSegments.insert(0, snakePosition)
        
        # 判斷是否吃掉了樹莓，再決定是否刪掉蛇尾
        if snakePosition != raspberryPosition:  # 如果沒有吃到樹莓
            snakeSegments.pop()                 # 就把身體的最後一節(尾巴)刪掉
        
        # 如果吃掉樹莓，則重新生成樹莓
        else:   
            raspberryPosition = (               
                randrange(0, 600, 20),   # 隨機產生[0,600)之間間隔20的亂數
                randrange(0, 460, 20)    # (0,20,40, ... 580)
            )                                   # 註：randrange半開區間[)，randint閉區間[]
            score += 1
        
        # 清空、重繪pygame顯示層
        dispSurface.fill(blackColour)   # 塗黑全部背景
        
        # 繪出蛇身體
        for (x, y) in snakeSegments[1:]:
            pygame.draw.rect(dispSurface, whiteColour, pygame.Rect(x, y, 20, 20))

        # 繪出蛇頭(先畫身體再畫頭方能使頭吃到身體時畫面能表現出來)
        (x, y) = snakeSegments[0]
        pygame.draw.rect(dispSurface, greenColour, pygame.Rect(x, y, 20, 20))
        
        # 繪出樹莓
        (x, y) = raspberryPosition
        pygame.draw.rect(dispSurface, redColour, pygame.Rect(x, y, 20, 20))
        
        # 刷新pygame顯示層
        display.update()
        
        # 判斷是否死亡
        (x, y) = snakePosition
        if not (0 <= x < 600 and 0 <= y < 460):  # 如果蛇頭在X、Y軸方向沒有在視窗範圍內
            gameOver(dispSurface, score)

        # 是否吃到自己身體
        elif snakePosition in snakeSegments[1:]:
            gameOver(dispSurface, score)


if __name__ == "__main__":
    main()
