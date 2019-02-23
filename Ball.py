import math

class Ball:


    def __init__(self, coord, SPEED):
        # coord는 ball의 center 좌표
        self.SPEED=SPEED
        self.coord=[coord[0], coord[1]]
        self.radius=15
        print("new Ball")


    # param:vectorDirection example : (1,0) (3,5)
    def move(self, vectorDirection):
        vector=self.adjustVector(vectorDirection)
        # print(vector)
        self.coord[0]+=math.ceil(float(vector[0])*self.SPEED)
        self.coord[1]+=math.ceil(float(vector[1])*self.SPEED)

    #크기가 1인 벡터로 변환하여 리턴해주는 함수
    def adjustVector(self, vectorDirection):
        # vectorSize=math.sqrt((vectorDirection[0])^2+(vectorDirection[1])^2)
        vectorSize=math.sqrt(vectorDirection[0]**2+vectorDirection[1]**2)

        # 크기가 1인 벡터 리턴
        return (format(vectorDirection[0]/vectorSize, ".2f"),format(vectorDirection[1]/vectorSize, ".2f"))
