import pygame
import pygame.gfxdraw
import pygame.freetype
import time
import random
import sys
import os
from Ball import Ball
import Brick

class drawRainbow:
    ROUGH_MAX=245 # 대략적인 최대값
    def __init__(self, FPS):
        self.rgbUnit=int(255/FPS) # 한 번의 FPS마다 증가될 컬러값의 기본값
        self.rgb=[0,0,0]
    def adjustRGB(self):
        if(self.rgb[0]<=drawRainbow.ROUGH_MAX):
            self.rgb[0]+=self.rgbUnit
            # self.rgb[0]/=255 # 나머지 값으로 저장
        elif(self.rgb[1]<=drawRainbow.ROUGH_MAX):
            self.rgb[1]+=self.rgbUnit
            # self.rgb[1]/=255
        elif(self.rgb[2]<=drawRainbow.ROUGH_MAX):
            self.rgb[2]+=self.rgbUnit
            # self.rgb[2]/=255
        else:
            self.rgb=[0,0,0]


pygame.init()

pygame.display.set_caption("break Bricks!")
screen=pygame.display.set_mode((900, 600))
clock=pygame.time.Clock()

LOGO_IMAGE=pygame.image.load(os.path.join("logo.png"))
MAP_WIDTH=500
MAP_HEIGHT=500
GAME_AREA=(30,30,30+MAP_WIDTH, 30+MAP_HEIGHT)
#게임 데이터들
FPS=40
FAST_FPS=40
SLOW_FPS=20
BAR_WIDTH=200
BAR_HEIGHT=20
BAR_MOVE_SPEED=20
BALL_MOVE_SPEED=4
game=True
barCoord=[0,MAP_HEIGHT-BAR_HEIGHT]
boundary=False  #끝에 닿았는지
ball=Ball((90,300), 10)
RANDOM_VECTOR_SPEED=90
randomVectorCount=1;
vectorDirection=[1,-3]
drawRainbow=drawRainbow(FPS)

# to create bricks and brickList
brickList={}

#초기 bricks 생성
for i in range(6):
    brickList[i]=Brick.Brick((120, Brick.Brick.HEIGHT*i), 3)
    brickList[i+6]=Brick.Brick((300, Brick.Brick.HEIGHT*i), 3)

while game:

    # FPS를 이용해 진행 속도 설정
    clock.tick(FPS)

    # 눌려있는 key 정보 받음
    keyState=pygame.key.get_pressed()

    if(keyState[pygame.K_RIGHT]):
        if(barCoord[0]>=MAP_WIDTH-BAR_WIDTH):
            # 0으로 만들어주거나 MAP_WIDTH-BAR_WIDTH로 만들어 줘야 삐져나오지 않을 수 있음
            barCoord[0]=MAP_WIDTH-BAR_WIDTH
            boundary=True
        else :
            boundary=False
            barCoord[0]+=BAR_MOVE_SPEED
    elif(keyState[pygame.K_LEFT]):
        if(barCoord[0]<=0):
            barCoord[0]=0
            boundary=True
        else :
            boundary=False
            barCoord[0]-=BAR_MOVE_SPEED

    # pygame의 event를 받아봄
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
            elif(event.key==pygame.K_f):
                # FAST와 SLOW FPS로 교대
                if(FPS==FAST_FPS):
                    FPS=SLOW_FPS
                else:
                    FPS=FAST_FPS

            # vectorDirection이 (0,1) or (1,0) 등으로 인해
            # 게임이 진행 안 되는 걸 막기 위함
            elif(event.key==pygame.K_a):
                c=0
                while(c<=10):   #일단 10번만
                    vectorDirection[0]=random.randint(-10,10)
                    vectorDirection[1]=random.randint(-3,3)
                    if(vectorDirection[0]==0 or vectorDirection[1]==0):c-=1
                    c+=1

    if(ball.coord[0]<=0+ball.radius):
        if(vectorDirection[0]<0):
            vectorDirection[0]*=(-1)

    elif(ball.coord[0]>=MAP_WIDTH-ball.radius):
        ball.coord[0]=MAP_WIDTH-ball.radius
        if(vectorDirection[0]>0):
            vectorDirection[0]*=(-1)
    if(ball.coord[1]<=0+ball.radius):
        if(vectorDirection[1]<0):
            vectorDirection[1]*=(-1)
    else:
        for i in brickList:
            brick=brickList[i]
            # IMPORTANT!
            # 이 if 문은 순수한 방향 (대각선 제외)
            # 완전 왼쪽에서오는 것
            if(ball.coord[0]>=brick.topLeft[0]-ball.radius and
            ball.coord[0]<=brick.topLeft[0] and
            ball.coord[1]>=brick.topLeft[1] and
            ball.coord[1]<=brick.bottomLeft[1] and
            vectorDirection[0]>0):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(1)
                vectorDirection[0]*=(-1)
                break

            # 완전 오른쪽에서 오는 것
            elif(ball.coord[0]>=brick.topRight[0] and
            ball.coord[0]<=brick.topRight[0]+ball.radius and
            ball.coord[1]>=brick.topRight[1] and
            ball.coord[1]<=brick.bottomRight[1] and
            vectorDirection[0]<0):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(2)
                vectorDirection[0]*=(-1)
                break
            # 아래에서 오는 것
            elif(ball.coord[0]>=brick.bottomLeft[0]and
            ball.coord[0]<=brick.bottomRight[0] and
            ball.coord[1]>=brick.bottomLeft[1] and
            ball.coord[1]<=brick.bottomLeft[1]+ball.radius and
            vectorDirection[1]<0):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(3)
                vectorDirection[1]*=(-1)
                break
            # 위에서 오는 것
            elif(ball.coord[0]>=brick.topLeft[0]and
            ball.coord[0]<=brick.topRight[0] and
            ball.coord[1]>=brick.topLeft[1]-ball.radius and
            ball.coord[1]<=brick.topLeft[1] and
            vectorDirection[1]>0):
                # hitBrick이 True를 리턴하면 부셔진 것임
                if(brickList[i].hitBrick()):del brickList[i]
                print(4)
                vectorDirection[1]*=(-1)
                break

            # IMPORTANT
            # 이 else문은 순수하지 않은 방향( 즉 대각선 )이나 그 밖에 있을 때
            else:
                #벡터로 튕김각 계산하는 부분 시작not  중요함 진짜 ㅜㅜ

                # 왼쪽 대각선 위에서 오는 것not  중요
                # 우선은 적당한 범위 안에 있는 지 확인
                # 드디어 구현했당.... ㅜㅅㅜ
                if(ball.coord[0]>=brick.topLeft[0]-ball.radius and
                ball.coord[0]<=brick.topLeft[0] and
                ball.coord[1]>=brick.topLeft[1]-ball.radius and
                ball.coord[1]<=brick.topLeft[1]):
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
                ball.coord[1]<=brick.topRight[1]):
                    # hitBrick이 True를 리턴하면 부셔진 것임
                    if(brickList[i].hitBrick()):del brickList[i]
                    print(6)

                    # ball의 adjustVector 메소드를 빌림
                    tempBallVector=ball.adjustVector(vectorDirection)
                    tempSlopeVecotr=ball.adjustVector([ball.coord[0]-brick.topRight[0], ball.coord[1]-brick.topRight[1]])
                    vectorDirection=[float(float(tempBallVector[0])+float(tempSlopeVecotr[0])), float(float(tempBallVector[1])+float(tempSlopeVecotr[1]))]
                    break

                # 왼쪽 대각선 아래에서 오는 것
                elif(ball.coord[0]>=brick.bottomLeft[0]-ball.radius and
                ball.coord[0]<=brick.bottomLeft[0] and
                ball.coord[1]>=brick.bottomLeft[1]and
                ball.coord[1]<=brick.bottomLeft[1]+ball.radius):
                    # hitBrick이 True를 리턴하면 부셔진 것임
                    if(brickList[i].hitBrick()):del brickList[i]
                    print(7)

                    # ball의 adjustVector 메소드를 빌림
                    tempBallVector=ball.adjustVector(vectorDirection)
                    tempSlopeVecotr=ball.adjustVector([ball.coord[0]-brick.bottomLeft[0], ball.coord[1]-brick.bottomLeft[1]])
                    vectorDirection=[float(float(tempBallVector[0])+float(tempSlopeVecotr[0])), float(float(tempBallVector[1])+float(tempSlopeVecotr[1]))]
                    break
                # 오른쪽 대각선 아래에서 오는 것
                elif(ball.coord[0]>=brick.bottomRight[0] and
                ball.coord[0]<=brick.bottomRight[0]+ball.radius and
                ball.coord[1]>=brick.bottomRight[1] and
                ball.coord[1]<=brick.bottomRight[1]+ball.radius):
                    # hitBrick이 True를 리턴하면 부셔진 것임
                    if(brickList[i].hitBrick()):del brickList[i]
                    print(8)

                    # ball의 adjustVector 메소드를 빌림
                    tempBallVector=ball.adjustVector(vectorDirection)
                    tempSlopeVecotr=ball.adjustVector([ball.coord[0]-brick.bottomRight[0], ball.coord[1]-brick.bottomRight[1]])
                    vectorDirection=[float(float(tempBallVector[0])+float(tempSlopeVecotr[0])), float(float(tempBallVector[1])+float(tempSlopeVecotr[1]))]
                    break

    # bar과 ball이 충돌했을 때
    if(vectorDirection[1]>0 and (ball.coord[0]+ball.radius>=barCoord[0] and
    ball.coord[0]-ball.radius<=barCoord[0]+BAR_WIDTH and
    ball.coord[1]>=barCoord[1]-ball.radius and
    ball.coord[1]<=barCoord[1])):
        ball.coord[1]=barCoord[1]-ball.radius
        vectorDirection[1]*=(-1)

    if(ball.coord[1]>MAP_HEIGHT): ball=Ball((300,300), 10)

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
    screen.blit(LOGO_IMAGE, (550,100))

    #글자쓰기.. 까다로운듯
    lineHeight=30
    lineCount=0
    def writeGuideText(text, x, y):
        guideFont=pygame.freetype.Font("nanum.ttf", 20)
        guidTextSurface=guideFont.render_to(screen, (x,y), text, (100,100,100))

    writeGuideText("key 'A' means", 550, 200+lineHeight*lineCount)
    lineCount+=1
    writeGuideText("to adjust the direction of the ball", 550, 200+lineHeight*lineCount)
    lineCount+=1
    writeGuideText("key 'F' means", 550, 200+lineHeight*lineCount)
    lineCount+=1
    writeGuideText("to change FPS", 550, 200+lineHeight*lineCount)
    
    pygame.display.flip()
