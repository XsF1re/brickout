MAP_WIDTH=500
MAP_HEIGHT=500
GAME_AREA=(100,50,100+MAP_WIDTH, 50+MAP_HEIGHT)


class Brick:
    WIDTH=80
    HEIGHT=40
    def __init__(self, topLeft, HARDNESS):
        # coord는 wall의 leftUpper coordinate
        # HARDNESS는 몇 대 때려야 깨지는지
        # attack은 맞은 회수
        print("Brick created")

        # to input coordinates

        self.topLeft=[topLeft[0], topLeft[1]]
        self.topRight=[topLeft[0]+Brick.WIDTH, topLeft[1]]
        self.bottomLeft=[topLeft[0], topLeft[1]+Brick.HEIGHT]
        self.bottomRight=[topLeft[0]+Brick.WIDTH, topLeft[1]+Brick.HEIGHT]

#임시
        self.coord=[self.topLeft[0], self.topLeft[1]]
        self.attack=0
        self.HARDNESS=HARDNESS

    def hitBrick(self):
        self.attack+=1
        if(self.HARDNESS==self.attack):
            return True # True면 부셨다는 것
        else: return False # False면 못 부셨다는 것
    def draw(self, drawReference, screen):
        colorStandard= 255/self.HARDNESS # 색깔 비율
        drawReference.rect(screen, ((colorStandard*self.attack), (colorStandard*self.attack), (colorStandard*self.attack)), (self.coord[0]+GAME_AREA[0], self.coord[1]+GAME_AREA[1], Brick.WIDTH, Brick.HEIGHT), 5)
