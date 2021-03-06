import pygame
import pygame.gfxdraw
import pygame.freetype
import time
import random
import sys
import os
from Ball import Ball
import Brick

# import custom py files
import Bar
import vectorReflecting

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


pygame.init() # pygame 모듈을 사용하기 위해 초기화

pygame.display.set_caption("break Bricks!") # 프로그램 창의 상단바 제목
screen=pygame.display.set_mode((900, 600)) # 프로그램 창의 해상도 900x600으로 설정
clock=pygame.time.Clock() # 화면을 초당 몇 번 출력하는가를 설정하기 위해 선언되는 clock 변수이며 초당 화면 출력이 게임에서는 FPS 혹은 Frame Rate라고도 한다.

LOGO_IMAGE=pygame.image.load(os.path.join("logo.png")) # 로고 이미지 불러오기
MAP_WIDTH=500 #게임 플레이할 공간의 가로 길이
MAP_HEIGHT=500 #게임 플레이할 공간의 세로 길이
GAME_AREA=(30,30,30+MAP_WIDTH, 30+MAP_HEIGHT) # 게임 플레이할 공간과 실행창 사이 간격? (왼쪽 사이 간격, 위쪽 사이 간격, ...?)
#게임 데이터들
FAST_FPS=50 #빠른 FPS
SLOW_FPS=10 #느린 FPS
FPS=FAST_FPS #빠른 FPS로 기본 설정
BAR_WIDTH=100 #바 가로 길이
BAR_HEIGHT=20 #바 세로 길이
BAR_MOVE_WIDTH=20
BALL_MOVE_SPEED=4
game=True
bar=Bar.Bar(((MAP_WIDTH-BAR_WIDTH)/2,MAP_HEIGHT-BAR_HEIGHT)) #게임 초기 실행시 바 기본위치 (가로, 세로)
barCoord=[(MAP_WIDTH-BAR_WIDTH)/2,MAP_HEIGHT-BAR_HEIGHT]
boundary=False  #끝에 닿았는지 확인
currentLife = 10

RANDOM_VECTOR_SPEED=90 #???
randomVectorCount=1; #???

vectorDirection=[-2,1] #공 벡터 방향
ball=Ball((30,30), 10)

drawRainbow=drawRainbow(FPS)

# to create bricks and brickList
brickList={}

#초기 bricks 생성

# def cutAtBoundary() : # 만약 boundary에 닿았을 경우 더 넘어가지 않도록
#     # bar의 x는 0부터 MAP_WIDTH인 셈
#     # MAP이 게임상의 좌표고 전체 게임 창은 신경 안 써도 된다고 보면 됨.
#     barMINX=0
#     barMAXX= MAP_WIDTH - BAR_WIDTH
#     mediumX=barMAXX//2 ## 대충 왼쪽에 bar을 붙일 지 오른쪽에 붙일 지를 판별하는 녀석
#     if(bar.getX()<mediumX):
#         bar.setX(barMINX)
#
#     else:
#         bar.setX(barMAXX)


def initGameDefault():
    for i in range(5):
        brickList[i]=Brick.Brick((120, Brick.Brick.HEIGHT*i), 2)

    for i in range(3):
        brickList[i+5]=Brick.Brick((400, Brick.Brick.HEIGHT*i), 2)

initGameDefault()
while game:

    # FPS를 이용해 진행 속도 설정
    clock.tick(FPS)

    # 눌려있는 key 정보 받음
    keyState=pygame.key.get_pressed()
    boundary=False # 초깃값은 False
    if(keyState[pygame.K_RIGHT]):

        boundary=bar.moveBar("RIGHT")
        # if(bar.getX()>=MAP_WIDTH-BAR_WIDTH-BAR_MOVE_WIDTH):
        #     # 0으로 만들어주거나 MAP_WIDTH-BAR_WIDTH로 만들어 줘야 삐져나오지 않을 수 있음
        #     cutAtBoundary()
        #     boundary=True
        # else :
        #     boundary=False
        #     barCoord[0]+=BAR_MOVE_WIDTH
    elif(keyState[pygame.K_LEFT]):
        boundary=bar.moveBar("LEFT")

        # if(bar.getX()<=0+BAR_MOVE_WIDTH):
        #     cutAtBoundary()
        #     boundary=True
        # else :
        #     boundary=False
        #     barCoord[0]-=BAR_MOVE_WIDTH
    elif(keyState[pygame.K_UP]):
        boundary=bar.moveBar("UP")

    elif(keyState[pygame.K_DOWN]):
        boundary=bar.moveBar("DOWN")

    # pygame의 event를 받아봄
    for event in pygame.event.get():

        if (event.type==pygame.QUIT):
            game=False

        elif event.type == pygame.KEYDOWN:
            #오른쪽키
            if(event.key==pygame.K_RIGHT):
                boundary = bar.moveBar("RIGHT")

                # if(bar.getX()>=MAP_WIDTH-BAR_WIDTH):
                #     boundary=True
                # else :
                #     boundary=False
                #     barCoord[0]+= BAR_MOVE_WIDTH / 3
            # 왼쪽
            elif(event.key==pygame.K_LEFT):
                boundary = bar.moveBar("LEFT")
                # if(bar.getX()<=0):
                #     boundary=True
                # else:
                #     boundary=False
                #     barCoord[0]-= BAR_MOVE_WIDTH / 3
            elif(event.key==pygame.K_UP):
                boundary = bar.moveBar("UP")

            elif(event.key==pygame.K_DOWN):
                boundary = bar.moveBar("DOWN")

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
            elif(event.key==pygame.K_q):
                game=False

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

                    isNeighborBrick=False
                    # 위아래 네이버만 찾을게 일단.....
                    for innerIndex in brickList :
                        if(brick.topLeft==brickList[innerIndex].bottomLeft):
                            isNeighborBrick=True
                            break
                    if(isNeighborBrick and vectorDirection[0]>=0):
                        vectorDirection[0]*=(-1)
                        break
                    else:
                        slope=vectorReflecting.getVerticalVector([ball.coord[0]-brick.topLeft[0], ball.coord[1]-brick.topLeft[1]])
                        vectorDirection=vectorReflecting.getReflectedVector(slope, vectorDirection)
                        break
                # 오른쪽 대각선 위에서 오는 것
                elif(ball.coord[0]>=brick.topRight[0] and
                ball.coord[0]<=brick.topRight[0]+ball.radius and
                ball.coord[1]>=brick.topRight[1]-ball.radius and
                ball.coord[1]<=brick.topRight[1]):
                    # hitBrick이 True를 리턴하면 부셔진 것임
                    if(brickList[i].hitBrick()):del brickList[i]

                    # ball의 adjustVector 메소드를 빌림
                    # tempBallVector=ball.adjustVector(vectorDirection)
                    # tempSlopeVecotr=ball.adjustVector([ball.coord[0]-brick.topRight[0], ball.coord[1]-brick.topRight[1]])
                    # vectorDirection=[float(float(tempBallVector[0])+float(tempSlopeVecotr[0])), float(float(tempBallVector[1])+float(tempSlopeVecotr[1]))]
                    isNeighborBrick=False
                    # 위아래 네이버만 찾을게 일단.....
                    for innerIndex in brickList :
                        if(brick.topRight==brickList[innerIndex].bottomRight):
                            isNeighborBrick=True
                            break
                    if(isNeighborBrick and vectorDirection[0]<=0):
                        vectorDirection[0]*=(-1)
                        break
                    else:
                        slope=vectorReflecting.getVerticalVector([ball.coord[0]-brick.topRight[0], ball.coord[1]-brick.topRight[1]])
                        vectorDirection=vectorReflecting.getReflectedVector(slope, vectorDirection)
                        break

                # 왼쪽 대각선 아래에서 오는 것
                elif(ball.coord[0]>=brick.bottomLeft[0]-ball.radius and
                ball.coord[0]<=brick.bottomLeft[0] and
                ball.coord[1]>=brick.bottomLeft[1]and
                ball.coord[1]<=brick.bottomLeft[1]+ball.radius):
                    # hitBrick이 True를 리턴하면 부셔진 것임
                    if(brickList[i].hitBrick()):del brickList[i]

                    isNeighborBrick=False
                    # 위아래 네이버만 찾을게 일단.....
                    for innerIndex in brickList:
                        if(brick.bottomLeft==brickList[innerIndex].topLeft):
                            isNeighborBrick=True
                            break
                    if(isNeighborBrick):
                        if(vectorDirection[0]>=0):
                            vectorDirection[0]*=(-1)
                            break
                    else:
                        slope=vectorReflecting.getVerticalVector([ball.coord[0]-brick.bottomLeft[0], ball.coord[1]-brick.bottomLeft[1]])
                        vectorDirection=vectorReflecting.getReflectedVector(slope, vectorDirection)
                        break
                # 오른쪽 대각선 아래에서 오는 것
                elif(ball.coord[0]>=brick.bottomRight[0] and
                ball.coord[0]<=brick.bottomRight[0]+ball.radius and
                ball.coord[1]>=brick.bottomRight[1] and
                ball.coord[1]<=brick.bottomRight[1]+ball.radius):
                    # hitBrick이 True를 리턴하면 부셔진 것임
                    if(brickList[i].hitBrick()):del brickList[i]
                    isNeighborBrick=False
                    # 위아래 네이버만 찾을게 일단.....
                    for innerIndex in brickList :
                        if(brick.bottomRight==brickList[innerIndex].topRight):
                            isNeighborBrick=True
                            break
                    if(isNeighborBrick and vectorDirection[0]<=0):
                        vectorDirection[0]*=(-1)
                        break
                    else:
                        slope=vectorReflecting.getVerticalVector([ball.coord[0]-brick.bottomRight[0], ball.coord[1]-brick.bottomRight[1]])
                        vectorDirection=vectorReflecting.getReflectedVector(slope, vectorDirection)
                        break

    # bar과 ball이 충돌했을 때
    if(vectorDirection[1]>0 and (ball.coord[0]+ball.radius>=bar.getX() and
    ball.coord[0]-ball.radius<=bar.getX()+BAR_WIDTH and
    ball.coord[1]>=bar.getY()-ball.radius and
    ball.coord[1]<=bar.getY())):
        ball.coord[1]=bar.getY()-ball.radius
        vectorDirection[1]*=(-1)

    if(ball.coord[1]>MAP_HEIGHT):
        print(currentLife)
        currentLife -= 1;
        ball=Ball((300,300), 10)

    # DRAWING BEGINS
    screen.fill((255, 255, 255))

    # pygame.gfxdraw.filled_polygon(screen, ( (GAME_AREA[0],GAME_AREA[1]), (GAME_AREA[2],GAME_AREA[1]), (GAME_AREA[2], GAME_AREA[3]), (GAME_AREA[0], GAME_AREA[3]) ), (30,30,30))
    #draw game area
    pygame.draw.rect(screen, (30, 30, 30), (GAME_AREA[0], GAME_AREA[1], MAP_WIDTH, MAP_HEIGHT), 3)
    pygame.draw.line(screen, (0, 0, 255), [30,400], [30+MAP_WIDTH,400],3)
    if(currentLife > 0):
        ball.move(vectorDirection)
    for brick in brickList:
        brickList[brick].draw(pygame.draw, screen)
    pygame.draw.circle(screen, (0,150,230),(ball.coord[0]+GAME_AREA[0], ball.coord[1]+GAME_AREA[1]), ball.radius, 3)
    if(boundary=="CRUSH"):
        pygame.draw.rect(screen, (150,0,0), (bar.getX()+GAME_AREA[0], bar.getY()+GAME_AREA[1], BAR_WIDTH, BAR_HEIGHT), 5)
    else:
        # GAME_AREA=(100,50,100+MAP_WIDTH, 50+MAP_HEIGHT)
        pygame.draw.rect(screen, (0,200,200), (bar.getX()++GAME_AREA[0], bar.getY()+GAME_AREA[1], BAR_WIDTH, BAR_HEIGHT), 5)
    screen.blit(LOGO_IMAGE, (550,100))

    #글자쓰기.. 까다로운듯
    lineHeight=30
    lineCount=0
    def writeGuideText(text, x, y):
        guideFont=pygame.freetype.Font("CookieRun Regular.ttf", 20) #쿠키런 폰트, 크기는 20으로 지정
        guidTextSurface=guideFont.render_to(screen, (x,y), text, (100,100,100))

    writeGuideText("key 'A' means", 550, 200+lineHeight*lineCount)
    lineCount+=1
    writeGuideText("to adjust the direction of the ball", 550, 200+lineHeight*lineCount)
    lineCount+=1
    writeGuideText("key 'F' means", 550, 200+lineHeight*lineCount)
    lineCount+=1
    writeGuideText("to change FPS", 550, 200+lineHeight*lineCount)
    lineCount+=2

    if(currentLife > 0):
        currentLifeDescription = "Life: " + str(currentLife)
        writeGuideText(currentLifeDescription, 550, 200+lineHeight*lineCount)
    else:
        writeGuideText("Game Over!", 550, 200+lineHeight*lineCount)

    pygame.display.flip()
