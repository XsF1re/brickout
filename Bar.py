class Bar:
    BAR_WIDTH = 200
    BAR_HEIGHT = 20
    BAR_MOVE_WIDTH = 20
    MAP_WIDTH = 500
    def __init__(self, *args):
        print("constructed a bar")
        self.setCoord(args[0])

    def setCoord(self, coord):
        self.coord=[coord[0], coord[1]]

    def getX(self):
        return self.coord[0]
    def setX(self, value):
        print(str(value) + "로 bar의 X가 설정됨")

    def getY(self):
        return self.coord[1]

    def setY(self, value):
        print(str(value) + "로 bar의 Y가 설정됨")

    def moveBar(self, direction):
        if(direction == "RIGHT"):
            # print("go to right")

            # 만약 끝 부분에 있다면 끝부분으로 좌표 설정
            if self.coord[0]>=Bar.MAP_WIDTH-Bar.BAR_WIDTH:
                self.coord[0]=Bar.MAP_WIDTH-Bar.BAR_WIDTH
                return "CRASH"

            else :
                self.coord[0]+=Bar.BAR_MOVE_WIDTH

        if(direction == "LEFT"):
            # print("go to left")
            # 만약 시작 부분 근처에 있다면 시작 부분으로 좌표 설정
            # print(self.coord[0])
            if self.coord[0] <= Bar.BAR_MOVE_WIDTH:
                self.coord[0] = 0
                return "CRUSH"
            else:
                self.coord[0] -= Bar.BAR_MOVE_WIDTH




