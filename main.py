import pygame
import pygame.gfxdraw
import time
import random
from Ball import Ball
import Brick
pygame.init()

pygame.display.set_caption("break Bricks!")
screen=pygame.display.set_mode((700, 600))
screen.fill((255, 255, 255))
clock=pygame.time.Clock()


MAP_WIDTH=500
MAP_HEIGHT=500
GAME_AREA=(100,50,100+MAP_WIDTH, 50+MAP_HEIGHT)


#게임 데이터들
FPS=50
BAR_WIDTH=90
BAR_HEIGHT=20
BAR_MOVE_SPEED=20
BALL_MOVE_SPEED=4
game=True
barCoord=[0,MAP_HEIGHT-BAR_HEIGHT]
boundary=False  #끝에 닿았는지
ball=Ball((5,5), 10)
RANDOM_VECTOR_SPEED=10
randomVectorCount=0;
vectorDirection=[3,3];

# to create bricks and brickList
brickList={}

for i in range(3):
    brickList[i]=Brick.Brick((100+Brick.Brick.WIDTH*i, 0), 3)
    brickList[i+3]=Brick.Brick((100+Brick.Brick.WIDTH*i, Brick.Brick.HEIGHT), 3)
    brickList[i+6]=Brick.Brick((100+Brick.Brick.WIDTH*i, Brick.Brick.HEIGHT*2), 3)
    brickList[i+9]=Brick.Brick((100+Brick.Brick.WIDTH*i, Brick.Brick.HEIGHT*3), 3)
    brickList[i+12]=Brick.Brick((100+Brick.Brick.WIDTH*i, Brick.Brick.HEIGHT*4), 3)
    brickList[i+15]=Brick.Brick((100+Brick.Brick.WIDTH*i, Brick.Brick.HEIGHT*5), 3)
    brickList[i+18]=Brick.Brick((100+Brick.Brick.WIDTH*i, Brick.Brick.HEIGHT*6), 3)
    brickList[i+21]=Brick.Brick((100+Brick.Brick.WIDTH*i, Brick.Brick.HEIGHT*7), 3)



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

    # check if the ball crashes something
    crashX=False
    crashXSign="negative" # 음수벡터를 가져서 충돌 -> 양수로 바꿔줘야함
    crashY=False
    crashYSign="negative" # 음수벡터를 가져서 충돌 -> 양수로 바꿔줘야함
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
    for i in brickList:

        #일단은 옆에서 박는 걸 좀 더 판정 좋게
        # 왼쪽에서 박기
        if(ball.coord[0]+ball.radius>=brickList[i].coord[0]  and
        ball.coord[0]-ball.radius<=brickList[i].coord[0] and
        ball.coord[1]+ball.radius>=brickList[i].coord[1] and
        ball.coord[1]-ball.radius<=brickList[i].coord[1]+Brick.Brick.HEIGHT):
            # hitBrick이 True를 리턴하면 부셔진 것임
            if(brickList[i].hitBrick()):del brickList[i]
            crashX=True
            crashXSign="positive"
            break
        #오른쪽에서 박기
        elif(ball.coord[0]-ball.radius<=brickList[i].coord[0]+BAR_WIDTH and
        ball.coord[0]+ball.radius>=brickList[i].coord[0]+BAR_WIDTH and
        ball.coord[1]+ball.radius>=brickList[i].coord[1] and
        ball.coord[1]-ball.radius<=brickList[i].coord[1]+Brick.Brick.HEIGHT):
            if(brickList[i].hitBrick()):del brickList[i]
            crashX=True
            crashXSign="negative"
            break

        # 위에서 박기
        elif(ball.coord[0]-ball.radius>=brickList[i].coord[0] and
        ball.coord[0]+ball.radius<=brickList[i].coord[0]+Brick.Brick.WIDTH and
        ball.coord[1]+ball.radius>=brickList[i].coord[1] and
        ball.coord[1]-ball.radius<=brickList[i].coord[1]):
            if(brickList[i].hitBrick()):del brickList[i]
            crashY=True
            crashYSign="positive"
            break

        # 아래서 박기
        elif(ball.coord[0]-ball.radius>=brickList[i].coord[0] and
        ball.coord[0]+ball.radius<=brickList[i].coord[0]+Brick.Brick.WIDTH and
        ball.coord[1]+ball.radius>=brickList[i].coord[1]+Brick.Brick.HEIGHT and
        ball.coord[1]-ball.radius<=brickList[i].coord[1]+Brick.Brick.HEIGHT):
            if(brickList[i].hitBrick()):del brickList[i]
            crashY=True
            crashYSign="negative"
            break

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
