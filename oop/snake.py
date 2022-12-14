from typing import List, Union
import random


class Point:
    def __init__(self, x: int, y: int) -> None:
        """
        給定 x 和 y 然後產生一個點
        """
        self.x = x
        self.y = y


class Region:
    def __init__(self, p1:Point, p2:Point) -> None:
        """
        給兩個點，定義一個矩形範圍
        """
        self.p1 = p1
        self.p2 = p2

    def rnd_point(self, except_points: List[Point] = []) -> Point:
        """
        產生範圍內的隨機一個「點」
        除了except_points(list of Point)之外
        """
        while True:
            pt = Point( 
                random.randrange(self.p1.x, self.p2.x), 
                random.randrange(self.p1.y, self.p2.y) 
            )
            if not (pt in except_points): break

    def is_in(self, pt: Point) -> bool:
        """
        傳入一個點pt，判斷該點是不是超出本Region範圍
        """
        if self.p1.x <= pt.x <= self.p2.x and \
            self.p1.y <= pt.y <= self.p2.y:
            return True
        else:
            return False

class Snake:
    def __init__(self, region: Region) -> None:
        """
        傳入一個蛇活動的「範圍」及蛇頭的「點」\n
        建立一隻貪食蛇
        """
        self.region = region
        self.head = Point(
            (region.p1.x + region.p2.x) // 2,
            (region.p1.y + region.p2.y) // 2                
        )
        self.body = [self.head]
        self.food = self.new_food()
        self.score = 0

    def new_food(self) -> Point:
        """
        在原先給定的Region內，新增一個食物\n
        而且避免新增的食物出現在蛇的身體上
        """
        self.food = self.region.rnd_point(self.body)
        return self.food

    def is_eaten(self) -> bool:
        """
        判斷是否有吃到食物
        """
        return self.head == self.food

    def is_died(self) -> bool:
        """
        判斷是否死掉：\n
        1.碰到四周牆壁
        2.吃到自己身體
        """
        
        if self.head in self.body[1:] and self.region.is_in(self.head):
            return True
        else:
            return False
        
    def go(self, dir_: str = '右') -> None:
        """
        往目前方向(dir=左、右、上、下)走一步
        """
        if dir_ == '左':
            self.head.x +=1
        elif dir_ == '左':
            self.head.x -=1
        elif dir_ == '上':
            self.head.y -=1
        else:
            self.head.y -=1

class Food:
    def __init__(self, region: Region, snake:Snake) -> None:
        """
        給定範圍內的食物
        """
        self.region = region
        (self.x, self.y) = self.region.rnd_point(except_points=snake.body) 
        
    def new_food(self):
        (self.x, self.y) = self.region.rnd_point(except_points=snake.body) 
