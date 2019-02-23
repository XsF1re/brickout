# test 코드를 작성해보겠다.
# 위로 쭉 올라가는 방향의 공에게 어떻게 될지

import pygame
import pygame.gfxdraw
import time
import random
from Ball import Ball
import Brick
pygame.init()

pygame.display.set_caption("break Bricksnot ")
screen=pygame.display.set_mode((700, 600))
screen.fill((255, 255, 255))
clock=pygame.time.Clock()


MAP_WIDTH=500
MAP_HEIGHT=500
GAME_AREA=(100,50,100+MAP_WIDTH, 50+MAP_HEIGHT)


#게임 데이터들
FPS=30
BAR_WIDTH=90
BAR_HEIGHT=20
BAR_MOVE_SPEED=20
BALL_MOVE_SPEED=4
game=True
barCoord=[0,MAP_HEIGHT-BAR_HEIGHT]
boundary=False  #끝에 닿았는지
ball=Ball((310,50), 10)
RANDOM_VECTOR_SPEED=10
randomVectorCount=0
vectorDirection=[3,3]

# 우선 main.py의 설정 내용을 다 가져옴
# 그중 바꿔야하는 요소들만 바꿔줌
vectorDirection=[3,3]
randomVectorCount=1
RANDOM_VECTOR_SPEED=60


# to create bricks and brickList
brickList={}
#Ball을 세로로 생성해봄
for i in range(3):
    brickList[i]=Brick.Brick((100, 255+Brick.Brick.HEIGHT*i), 3)
    brickList[i+3]=Brick.Brick((200, 255+Brick.Brick.HEIGHT*i), 3)
    brickList[i+6]=Brick.Brick((300, 255+Brick.Brick.HEIGHT*i), 3)
    brickList[i+9]=Brick.Brick((400, 255+Brick.Brick.HEIGHT*i), 3)


# 여기부터는 main과 비슷

    # check if the ball crashes something
    crashX=False
    crashXSign="negative" # 음수벡터를 가져서 충돌 -> 양수로 바꿔줘야함
    crashY=False
    crashYSign="negative" # 음수벡터를 가져서 충돌 -> 양수로 바꿔줘야함
while game:
    clock.tick(FPS)
    keyState=pygame.key.get_pressed()

    if(keyState[pygame.K_RIGHT]):
        if(barCoord[0]>=MAP_WIDTH-BAR_WIDTH):
            boundary=True
        else :
            boundary=False
            barCoord[0]+=BAR_MOVE_SPEED
    elif(keyState[pygame.K_LEFT]):
        if(barCoord[0]<=0):
            boundary=True
        else :
            boundary=False
            barCoord[0]-=BAR_MOVE_SPEED
    for event in pygame.event.get():

        if (event.type==pygame.QUIT):
            game=False

        elif event.type == pygame.KEYDOWN:
            if(event.key==pygame.K_RIGHT):
                if(barCoord[0]>=MAP_WIDTH-BAR_WIDTH):
                    boundary=True
                else :
                    boundary=False
                    barCoord[0]+=BAR_MOVE_SPEED/2
            elif(event.key==pygame.K_LEFT):
                if(barCoord[0]<=0):
                    boundary=True
                else:
                    boundary=False
                    barCoord[0]-=BAR_MOVE_SPEED/2
    #SPEED만큼 count가 차면 랜덤벡터생성
    if(randomVectorCount%RANDOM_VECTOR_SPEED==0):
        vectorDirection=[vectorDirection[0]+random.random()*4-2, vectorDirection[1]+random.random()*4-2]
        randomVectorCount=0
    randomVectorCount+=1

    # check out if the ball crashes map

    if(ball.coord[0]<=0+ball.radius):
        crashX=True
        crashXSign="negative"
    elif(ball.coord[0]>=MAP_WIDTH-ball.radius):
        crashX=True
        crashXSign="positive"
    elif(ball.coord[1]<=0+ball.radius):
        crashY=True
        crashYSign="negative"

    #check out if the ball crashes the bar
    elif((ball.coord[0]+ball.radius>=barCoord[0] and ball.coord[0]-ball.radius<=barCoord[0]+BAR_WIDTH) and (ball.coord[1]+ball.radius>=barCoord[1])):
        crashY=True
        crashYSign="positive"

    #check out if the ball crashes any brick
    else:
        for i in brickList:
            brick=brickList[i]

            # 완전 왼쪽에서오는 것
            if(ball.coord[0]>=brick.topLeft[0]-ball.radius and
            ball.coord[0]<=brick.topLeft[0] and
            ball.coord[1]>=brick.topLeft[1] and
            ball.coord[1]<=brick.bottomLeft[1] and not crashX):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(1)
                crashX=True
                crashXSign="positive"
                break

            # 완전 오른쪽에서 오는 것
            elif(ball.coord[0]>=brick.topRight[0] and
            ball.coord[0]<=brick.topRight[0]+ball.radius and
            ball.coord[1]>=brick.topRight[1] and
            ball.coord[1]<=brick.bottomRight[1] and not crashX):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(2)
                crashX=True
                crashXSign="negative"
                break
            # 아래에서 오는 것
            elif(ball.coord[0]>=brick.bottomLeft[0]and
            ball.coord[0]<=brick.bottomRight[0] and
            ball.coord[1]>=brick.bottomLeft[1] and
            ball.coord[1]<=brick.bottomLeft[1]+Brick.Brick.HEIGHT and not crashY):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(3)
                crashY=True
                crashYSign="negative"
                break
            # 위에서 오는 것
            elif(ball.coord[0]>=brick.topLeft[0]and
            ball.coord[0]<=brick.topRight[0] and
            ball.coord[1]>=brick.topLeft[1]-ball.radius and
            ball.coord[1]<=brick.topLeft[1] and not crashY):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(4)
                crashY=True
                crashYSign="positive"
                break

            #벡터로 튕김각 계산하는 부분 시작not  중요함 진짜 ㅜㅜ

            # 왼쪽 대각선 위에서 오는 것not  중요
            # 우선은 적당한 범위 안에 있는 지 확인
            # 드디어 구현했당.... ㅜㅅㅜ
            elif(ball.coord[0]>=brick.topLeft[0]-ball.radius and
            ball.coord[0]<=brick.topLeft[0] and
            ball.coord[1]>=brick.topLeft[1]-ball.radius and
            ball.coord[1]<=brick.topLeft[1] and not crashX and not crashY):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(5)

                # ball의 adjustVector 메소드를 빌림
                tempBallVector=ball.adjustVector(vectorDirection)
                tempSlopeVecotr=ball.adjustVector([ball.coord[0]-brick.topLeft[0], ball.coord[1]-brick.topLeft[1]])
                vectorDirection=[float(float(tempBallVector[0])+float(tempSlopeVecotr[0])), float(float(tempBallVector[1])+float(tempSlopeVecotr[1]))]
                break
            # 오른쪽 대각선 위에서 오는 것
            elif(ball.coord[0]>=brick.topRight[0] and
            ball.coord[0]<=brick.topRight[0]+ball.radius and
            ball.coord[1]>=brick.topRight[1]-ball.radius and
            ball.coord[1]<=brick.topRight[1] and not crashX and not crashY):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(6)

                # ball의 adjustVector 메소드를 빌림
                tempBallVector=ball.adjustVector(vectorDirection)
                tempSlopeVecotr=ball.adjustVector([ball.coord[0]-brick.topLeft[0], ball.coord[1]-brick.topLeft[1]])
                vectorDirection=[float(float(tempBallVector[0])+float(tempSlopeVecotr[0])), float(float(tempBallVector[1])+float(tempSlopeVecotr[1]))]
                break

            # 왼쪽 대각선 아래에서 오는 것
            elif(ball.coord[0]>=brick.bottomLeft[0]-ball.radius and
            ball.coord[0]<=brick.bottomLeft[0] and
            ball.coord[1]>=brick.bottomLeft[1]and
            ball.coord[1]<=brick.bottomLeft[1]+ball.radius and not crashX and not crashY ):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(7)

                # ball의 adjustVector 메소드를 빌림
                tempBallVector=ball.adjustVector(vectorDirection)
                tempSlopeVecotr=ball.adjustVector([ball.coord[0]-brick.topLeft[0], ball.coord[1]-brick.topLeft[1]])
                vectorDirection=[float(float(tempBallVector[0])+float(tempSlopeVecotr[0])), float(float(tempBallVector[1])+float(tempSlopeVecotr[1]))]
                break
            # 오른쪽 대각선 아래에서 오는 것
            elif(ball.coord[0]>=brick.bottomLeft[0] and
            ball.coord[0]<=brick.bottomLeft[0]+ball.radius and
            ball.coord[1]>=brick.bottomLeft[1] and
            ball.coord[1]<=brick.bottomLeft[1]+ball.radius and not crashX and not crashY):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(8)

                # ball의 adjustVector 메소드를 빌림
                tempBallVector=ball.adjustVector(vectorDirection)
                tempSlopeVecotr=ball.adjustVector([ball.coord[0]-brick.topLeft[0], ball.coord[1]-brick.topLeft[1]])
                vectorDirection=[float(float(tempBallVector[0])+float(tempSlopeVecotr[0])), float(float(tempBallVector[1])+float(tempSlopeVecotr[1]))]
                break
            else:
                crashX=False
                crashY=False

    # X좌표가 무엇인가와 충돌했는데
    if(crashX):
        if(crashXSign=="negative"):
            if(vectorDirection[0]<0):
                vectorDirection[0]*=(-1)
                randomVectorCount=1 #시간 초기화
        if(crashXSign=="positive"):
            if(vectorDirection[0]>0):
                vectorDirection[0]*=(-1)
                randomVectorCount=1
            vectorDirection

    # y좌표가 무엇인가와 충돌했는데
    if(crashY):
        if(crashYSign=="negative"):
            if(vectorDirection[1]<0):
                vectorDirection[1]*=(-1)
                randomVectorCount=1
        if(crashYSign=="positive"):
            if(vectorDirection[1]>0):
                vectorDirection[1]*=(-1)
                randomVectorCount=1

            # 벽과 충돌했을 때
            if(vectorDirection[1]>0 and (ball.coord[0]+ball.radius>=barCoord[0] and ball.coord[0]-ball.radius<=barCoord[0]+BAR_WIDTH)):
                print("crash bar")
                vectorDirection[1]*=(-1)
                randomVectorCount=1

    if(ball.coord[1]>MAP_HEIGHT): ball=Ball((100,100), 10)
    # DRAWING BEGINS
    screen.fill((255, 255, 255))
    # pygame.gfxdraw.filled_polygon(screen, ( (GAME_AREA[0],GAME_AREA[1]), (GAME_AREA[2],GAME_AREA[1]), (GAME_AREA[2], GAME_AREA[3]), (GAME_AREA[0], GAME_AREA[3]) ), (30,30,30))
    #draw game area
    pygame.draw.rect(screen, (30, 30, 30), (GAME_AREA[0], GAME_AREA[1], MAP_WIDTH, MAP_HEIGHT), 3)

    ball.move(vectorDirection)
    for brick in brickList:
        brickList[brick].draw(pygame.draw, screen)
    pygame.draw.circle(screen, (0,150,230),(ball.coord[0]+GAME_AREA[0], ball.coord[1]+GAME_AREA[1]), ball.radius, 3)
    if(boundary):
        pygame.draw.rect(screen, (150,0,0), (barCoord[0]+GAME_AREA[0], barCoord[1]+GAME_AREA[1], BAR_WIDTH, BAR_HEIGHT), 5)
    else:
        # GAME_AREA=(100,50,100+MAP_WIDTH, 50+MAP_HEIGHT)
        pygame.draw.rect(screen, (0,200,200), (barCoord[0]++GAME_AREA[0], barCoord[1]++GAME_AREA[1], BAR_WIDTH, BAR_HEIGHT), 5)
    pygame.display.flip()
