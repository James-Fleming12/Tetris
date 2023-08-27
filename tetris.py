import pygame 
import random
import numpy as np
import copy

pygame.init()
screen = pygame.display.set_mode((400, 440))
clock = pygame.time.Clock()
running = True
timer_is_on, timer = False, 0
grid = [[0 for x in range(22)] for y in range(20)] # 1's are grey/bkgrnd
myFont = pygame.font.SysFont("monofetti", 20)
myFont2 = pygame.font.SysFont("monofetti", 90)
myFont3 = pygame.font.SysFont("monofetti", 40)
score, level = 0,  1
rows, cols, blockSize = 20, 10, 20
playGrid = [[0 for x in range(cols)] for y in range(rows)] # 1's are currentPieces, 2's are placedPieces
nextPlayGrid = [[0 for x in range(cols)] for y in range(rows)]
colorsGrid = [[0 for x in range(cols)] for y in range(rows)]
colorsGridCopy = [[0 for x in range(cols)] for y in range(rows)]
rows, cols = 2, 3
nextPieceColor, currentPieceColor = "", ""
movedDown, extraPlaced, notAtBorder, currentPieceGen, rotateCollision = False, False, True, False, False
nextGrid = [[0 for x in range(3)] for y in range(2)]
nextGridLine = [0]*4
pieces = ["l", "j", "s", "z", "line", "t", "square"]
heldPiece = ""
heldGrid = [[0 for x in range(3)] for y in range(2)]
heldGridLine = [0]*4
heldPieceColor = ""
currentPiece = random.choice(pieces)
nextPiece = random.choice(pieces)
pieceLoc = pygame.Vector2(0, 3)
blockCollide, fastDrop, fullRow, heldPieceGen, usedHold, turnPassed, rowDeletedLast = False, False, False, False, False, False, False
tempStorage = []
pieceRotate, timerSet = 1, 20 
fullRowsSaved = []
rowsCleared, deletedRow, lines, rowsDeleted = 0, 0, 0, 0
gameOver = False
def drawGrid():
    for x in range(0, screen.get_width(), blockSize):
        for y in range(0, screen.get_height(),blockSize):
            if(260 <= x < 360 and (y==20 or y==60 or y==80 or 110 <= y < 200 or 220<= y <300)):
                pass
            else: 
                rect = pygame.Rect(x, y, blockSize, blockSize)
                pygame.draw.rect(screen, "dark gray", rect, 1)
def clearNextPlayGrid():
    global nextPlayGrid
    for index, x in enumerate(nextPlayGrid):
        for index2, y in enumerate(x):
            if(y==1):
                nextPlayGrid[index][index2] = 0 
def clearNextGridAll():
    global nextPlayGrid
    for index, x in enumerate(nextPlayGrid):
        for index2, y in enumerate(x):
            nextPlayGrid[index][index2] = 0 
            colorsGridCopy[index][index2] = 0 

for index, x in enumerate(grid): 
    for index2 ,y in enumerate(x): 
        if(index==1 or index==18 or index2==0 or index2 ==21 or index == 19 or index==12 or index==0):
            grid[index][index2] = 1
        if(index == 16 or index==13 or index==14 or index==15 or index==17):
            if(index2==2 or index2==5 or index2==10 or index2>=15):
                grid[index][index2] = 1

while running:
    clearNextGridAll()
    for index, x in enumerate(playGrid):
        for index2, y in enumerate(x):
            if(y==2 and index==0):
                gameOver = True
    if(lines/20 >= 1):
        lines = lines%20 
        timerSet-=1
        level+=1
    for index, x in enumerate(playGrid):
        fullRow = True
        for index2, y in enumerate(x): 
            if(y!=2):
                fullRow = False
        if(fullRow):
            currentPieceGen = False
            rowDeleted = index
            rowsCleared+=1
            if(rowDeletedLast):
                rowsDeleted+=1
            for index3, z in enumerate(playGrid[index]):
                playGrid[index][index3] = 0
                rowDeletedLast = True
            for index4, m in enumerate(playGrid):
                for index5, n in enumerate(m):
                    if(n==2 and index4<=index):
                        nextPlayGrid[index4+1][index5] = 2
                    elif(n==2):
                        nextPlayGrid[index4][index5] = 2
            playGrid = copy.deepcopy(nextPlayGrid)
        else: 
            rowDeletedLast = False
    if(rowDeletedLast == False and rowsDeleted>0):
        score += (100 + (200*rowsDeleted))
        lines += (rowsDeleted+1)
        rowsDeleted=0 
    elif(rowsCleared==1):
        score+= 100
        lines+= 1
    if(rowsCleared!=0):
        for index, x in enumerate(playGrid):
            for index2, y in enumerate(x):
                if(y==2 and index<=rowDeleted):
                    colorsGridCopy[index][index2] = colorsGrid[index-1][index2]
                elif(y==2): 
                    colorsGridCopy[index][index2] = colorsGrid[index][index2]
        rowsCleared = 0
        colorsGrid = copy.deepcopy(colorsGridCopy)

    nextPlayGrid = copy.deepcopy(playGrid)
    keys = pygame.key.get_pressed()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
        if(ev.type == pygame.KEYDOWN):
            if(ev.key == pygame.K_SPACE):
                fastDrop = True
            if(ev.key == pygame.K_c and usedHold == False):
                usedHold = True
                if(heldPiece == ""):
                    heldPiece = currentPiece 
                    heldPieceColor = currentPieceColor
                    currentPieceGen = False
                else:
                    currentPieceGen = False
                    heldPieceGen = True
                for index, x in enumerate(playGrid):
                    for index2, y in enumerate(x):
                        if(y==1): 
                            playGrid[index][index2] = 0 
            if(ev.key == pygame.K_RIGHT):
                clearNextPlayGrid()
                for index, x in enumerate(playGrid):
                    for index2, y in enumerate(x):
                        if(index2 == 9 and y==1):
                            notAtBorder = False
                        elif(y == 1 and nextPlayGrid[index][index2+1] == 2):
                            notAtBorder = False
                        elif(y==1):
                            nextPlayGrid[index][index2+1] = 1
                if(notAtBorder == True):
                    playGrid = copy.deepcopy(nextPlayGrid)
                    pieceLoc.y += 1
                else: 
                    notAtBorder = True
            if(ev.key == pygame.K_r and gameOver):
                for index, x in enumerate(playGrid):
                    for index2, y in enumerate(x):
                        playGrid[index][index2], nextPlayGrid[index][index2], colorsGrid[index][index2], colorsGridCopy[index][index2] = 0, 0, 0, 0
                gameOver = False
                blockCollide, fastDrop, fullRow, heldPieceGen, usedHold, turnPassed, rowDeletedLast = False, False, False, False, False, False, False
                currentPiece = random.choice(pieces)
                nextPiece = random.choice(pieces)
                lines, score, level = 0, 0, 1
                heldPiece = ""
            if(ev.key == pygame.K_LEFT):
                clearNextPlayGrid()
                for index, x in enumerate(playGrid):
                    for index2, y in enumerate(x):
                        if(index2 == 0 and y==1):
                            notAtBorder = False
                        elif(y == 1 and nextPlayGrid[index][index2-1] == 2):
                            notAtBorder = False
                        elif(y==1):
                            nextPlayGrid[index][index2-1] = 1
                if(notAtBorder == True):
                    playGrid = copy.deepcopy(nextPlayGrid)
                    pieceLoc.y -= 1
                else: 
                    notAtBorder = True
            if(ev.key == pygame.K_UP):
                if(pieceRotate < 4):
                    pieceRotate+=1 
                else: 
                    pieceRotate = 1
                for index, x in enumerate(playGrid):
                    for index2, y in enumerate(x):
                        if(y==1 and movedDown):
                            tx = int(pieceLoc.x)
                            ty = int(pieceLoc.y)
                            clearNextPlayGrid()
                            if(ty+1 == 19 or ty == 0 or tx==9 or tx == 0):
                                rotateCollision = True
                            elif(ty>=8  and currentPiece == "line"):
                                rotateCollision = True
                            else:
                                for x in range(0,2):
                                    for y in range(0,2):
                                        if(playGrid[x][y] == 2):
                                            rotateCollision = True
                            if(rotateCollision == False):
                                if(currentPiece == "square"):
                                    pass
                                if(currentPiece == "s"):
                                    nextPlayGrid[tx][ty] = 1
                                    if(pieceRotate == 2 or pieceRotate == 4): nextPlayGrid[tx-1][ty], nextPlayGrid[tx][ty+1], nextPlayGrid[tx+1][ty+1] = 1, 1, 1
                                    if(pieceRotate == 3 or pieceRotate == 1): nextPlayGrid[tx][ty+1], nextPlayGrid[tx+1][ty], nextPlayGrid[tx+1][ty-1] = 1, 1, 1
                                if(currentPiece == "z"):
                                    nextPlayGrid[tx][ty] = 1
                                    if(pieceRotate == 2 or pieceRotate == 4): nextPlayGrid[tx][ty+1], nextPlayGrid[tx-1][ty+1], nextPlayGrid[tx+1][ty] = 1, 1, 1
                                    if(pieceRotate == 3 or pieceRotate == 1): nextPlayGrid[tx-1][ty-1], nextPlayGrid[tx-1][ty], nextPlayGrid[tx][ty+1] = 1, 1, 1
                                if(currentPiece == "line"):
                                    nextPlayGrid[tx][ty] = 1
                                    if(pieceRotate == 2 or pieceRotate == 4): nextPlayGrid[tx-1][ty], nextPlayGrid[tx+1][ty], nextPlayGrid[tx+2][ty] = 1, 1, 1
                                    if(pieceRotate == 1 or pieceRotate == 3): nextPlayGrid[tx][ty-1], nextPlayGrid[tx][ty+1], nextPlayGrid[tx][ty+2] = 1, 1, 1
                                if(currentPiece == "t"):
                                    nextPlayGrid[tx][ty] = 1
                                    if(pieceRotate == 1): nextPlayGrid[tx-1][ty], nextPlayGrid[tx][ty+1], nextPlayGrid[tx][ty-1] = 1, 1, 1
                                    if(pieceRotate == 2): nextPlayGrid[tx+1][ty], nextPlayGrid[tx-1][ty], nextPlayGrid[tx][ty+1] = 1, 1, 1
                                    if(pieceRotate == 3): nextPlayGrid[tx][ty+1], nextPlayGrid[tx+1][ty], nextPlayGrid[tx][ty-1] = 1, 1, 1
                                    if(pieceRotate == 4): nextPlayGrid[tx-1][ty], nextPlayGrid[tx+1][ty], nextPlayGrid[tx][ty-1] = 1, 1, 1
                                if(currentPiece == "l"):
                                    nextPlayGrid[tx][ty] = 1
                                    if(pieceRotate == 1): nextPlayGrid[tx-1][ty+1], nextPlayGrid[tx][ty+1], nextPlayGrid[tx][ty-1] = 1, 1, 1
                                    if(pieceRotate == 2): nextPlayGrid[tx-1][ty], nextPlayGrid[tx+1][ty], nextPlayGrid[tx+1][ty+1] = 1, 1, 1
                                    if(pieceRotate == 3): nextPlayGrid[tx+1][ty-1], nextPlayGrid[tx][ty-1], nextPlayGrid[tx][ty+1] = 1, 1, 1
                                    if(pieceRotate == 4): nextPlayGrid[tx-1][ty-1], nextPlayGrid[tx-1][ty], nextPlayGrid[tx+1][ty] = 1, 1, 1
                                if(currentPiece == "j"):
                                    nextPlayGrid[tx][ty] = 1
                                    if(pieceRotate == 1): nextPlayGrid[tx-1][ty-1], nextPlayGrid[tx][ty-1], nextPlayGrid[tx][ty+1] = 1, 1, 1
                                    if(pieceRotate == 2): nextPlayGrid[tx+1][ty], nextPlayGrid[tx-1][ty], nextPlayGrid[tx-1][ty+1] = 1, 1, 1
                                    if(pieceRotate == 3): nextPlayGrid[tx][ty-1], nextPlayGrid[tx][ty+1], nextPlayGrid[tx+1][ty+1] = 1, 1, 1
                                    if(pieceRotate == 4): nextPlayGrid[tx+1][ty], nextPlayGrid[tx-1][ty], nextPlayGrid[tx+1][ty-1] = 1, 1, 1
                if(currentPiece != "square" and rotateCollision == False): 
                    playGrid = copy.deepcopy(nextPlayGrid)
                else:
                    rotateCollision = False
    for index, x in enumerate(nextGrid):
        for index2, y in enumerate(x):
            nextGrid[index][index2] = 0
    if(nextPiece == "line"):
        for x in range(0,3):
            nextGridLine[x] = 1
        nextPieceColor = "cyan2"
    if(nextPiece == "j"):
        nextGrid[0][0], nextGrid[1][0], nextGrid[1][1], nextGrid[1][2] = 1, 1, 1, 1
        nextPieceColor = "orange"
    if(nextPiece == "l"):
        nextGrid[0][2], nextGrid[1][0], nextGrid[1][1], nextGrid[1][2] = 1, 1, 1, 1
        nextPieceColor = "dark blue"
    if(nextPiece == "s"):
        nextGrid[1][0], nextGrid[1][1], nextGrid[0][1], nextGrid[0][2] = 1, 1, 1, 1
        nextPieceColor = "green1"
    if(nextPiece == "z"):
        nextGrid[0][0], nextGrid[0][1], nextGrid[1][1], nextGrid[1][2] = 1, 1, 1, 1
        nextPieceColor = "red"
    if(nextPiece == "t"):
        nextGrid[0][1], nextGrid[1][0], nextGrid[1][1], nextGrid[1][2] = 1, 1, 1, 1
        nextPieceColor = "purple"
    if(nextPiece == "square"):
        nextGrid[0][0], nextGrid[0][1], nextGrid[1][0], nextGrid[1][1] = 1, 1, 1, 1
        nextPieceColor = "yellow"
    for index, x in enumerate(nextGrid):
        for index2, y in enumerate(x):
            heldGrid[index][index2] = 0
    if(heldPiece == "line"):
        for x in range(0,3):
            heldGridLine[x] = 1
        heldPieceColor = "cyan2"
    if(heldPiece == "j"):
        heldGrid[0][0], heldGrid[1][0], heldGrid[1][1], heldGrid[1][2] = 1, 1, 1, 1
        heldPieceColor = "orange"
    if(heldPiece == "l"):
        heldGrid[0][2], heldGrid[1][0], heldGrid[1][1], heldGrid[1][2] = 1, 1, 1, 1
        heldPieceColor = "dark blue"
    if(heldPiece == "s"):
        heldGrid[1][0], heldGrid[1][1], heldGrid[0][1], heldGrid[0][2] = 1, 1, 1, 1
        heldPieceColor = "green1"
    if(heldPiece == "z"):
        heldGrid[0][0], heldGrid[0][1], heldGrid[1][1], heldGrid[1][2] = 1, 1, 1, 1
        heldPieceColor = "red"
    if(heldPiece == "t"):
        heldGrid[0][1], heldGrid[1][0], heldGrid[1][1], heldGrid[1][2] = 1, 1, 1, 1
        heldPieceColor = "purple"
    if(heldPiece == "square"):
        heldGrid[0][0], heldGrid[0][1], heldGrid[1][0], heldGrid[1][1] = 1, 1, 1, 1
        heldPieceColor = "yellow"
    screen.fill("white")
    if(currentPieceGen == False and gameOver == False):
        fastDrop, pieceRotate = False, 1
        if(usedHold):
            if(turnPassed):
                usedHold, turnPassed = False, False
            else: 
                turnPassed = True
        movedDown, extraPlaced = False, False
        if(heldPieceGen == False):
            currentPiece = nextPiece
            currentPieceColor = nextPieceColor
            nextPiece = random.choice(pieces)
        else: 
            temp = copy.copy(heldPiece)
            tempColor = heldPieceColor
            heldPieceColor = currentPieceColor
            currentPieceColor = tempColor
            heldPiece = copy.copy(currentPiece)
            currentPiece = temp
            heldPieceGen = False
        currentPieceGen, blockCollide = True, False
        if(currentPiece == "line"):
            playGrid[0][3], playGrid[0][4], playGrid[0][5], playGrid[0][6]= 1, 1, 1, 1
        if(currentPiece == "z" or currentPiece == "square"):
            playGrid[0][4], playGrid[0][5] = 1, 1
        if(currentPiece == "s"):
            playGrid[0][4], playGrid[0][3] = 1, 1
        if(currentPiece == "l" or currentPiece == "j" or currentPiece == "t"):
            playGrid[0][4], playGrid[0][3], playGrid[0][5] = 1, 1, 1
        timer = timerSet
        timer_is_on = True
        pieceLoc.x, pieceLoc.y = 0, 4

    if(timer_is_on and gameOver == False):  
        if(fastDrop):
            timer-=timerSet
        else: 
            timer-=1
        if(timer <= 0):
            timer_is_on = False
            timer = 0 

    clearNextPlayGrid()
    for index, x in enumerate(nextPlayGrid):
        for index2, y in enumerate(x):
            if(colorsGrid[index][index2] != 0): 
                tempRect = pygame.Rect(20+((index2+1)*20), ((index+1)*20), blockSize, blockSize)
                pygame.draw.rect(screen, colorsGrid[index][index2], tempRect)
            else:
                tempRect = pygame.Rect(20+((index2+1)*20), ((index+1)*20), blockSize, blockSize)
                pygame.draw.rect(screen, "ivory1", tempRect)
            if(playGrid[index][index2]==1):
                if(index==19):
                    blockCollide = True
                elif(playGrid[index+1][index2]==2):
                    blockCollide = True

        for index, x in enumerate(playGrid):
            for index2, y in enumerate(x):
                if(y==1):
                    if(blockCollide):
                        playGrid[index][index2] = 2
                        nextPlayGrid[index][index2] = 2
                        colorsGrid[index][index2] = currentPieceColor
                        currentPieceGen = False
                    else: 
                        if(timer_is_on):
                            tempRect = pygame.Rect(20+((index2+1)*20), ((index+1)*20), blockSize, blockSize)
                            pygame.draw.rect(screen, currentPieceColor, tempRect)
                        elif(timer_is_on == False and index<19):
                            playGrid[index][index2] = 0
                            temp = index+1
                            nextPlayGrid[temp][index2] = 1
        if(blockCollide == False and currentPieceGen == True): 
            if(timer_is_on == False):
                playGrid = copy.deepcopy(nextPlayGrid)
                movedDown = True
                pieceLoc.x += 1
                timer = timerSet
                timer_is_on = True
        blockCollide = False
    if(movedDown and extraPlaced == False):
        if(currentPiece == "z"):
            playGrid[int(pieceLoc.x)-1][int(pieceLoc.y)], playGrid[int(pieceLoc.x)-1][int(pieceLoc.y)-1] = 1, 1
        if(currentPiece == "s" or currentPiece == "square"):
            playGrid[int(pieceLoc.x)-1][int(pieceLoc.y)], playGrid[int(pieceLoc.x)-1][int(pieceLoc.y)+1] = 1, 1
        if(currentPiece == "t"):
            playGrid[int(pieceLoc.x)-1][int(pieceLoc.y)] = 1
        if(currentPiece == "l"):
            playGrid[int(pieceLoc.x-1)][int(pieceLoc.y)+1] = 1
        if(currentPiece == "j"):
            playGrid[int(pieceLoc.x-1)][int(pieceLoc.y)-1] = 1
        extraPlaced = True
    
    for index, x in enumerate(grid):
        for index2, y in enumerate(x): 
            if(y == 1):
                tempRect = pygame.Rect(index*20 , index2*20 ,blockSize, blockSize)
                pygame.draw.rect(screen, "gray30", tempRect)
    drawGrid()
    textLevel = myFont.render("Level: %d" % level, False, "purple")
    screen.blit(textLevel, (263, 25))
    textScore = myFont.render("Score: ", False, "purple")
    screen.blit(textScore, (263, 65))
    textScoreNum = myFont.render("%d" % score, False, "purple")
    screen.blit(textScoreNum, (263, 85))
    textNext = myFont.render("Next", False, "purple")
    screen.blit(textNext, (263, 125))
    textHold = myFont.render("Hold", False, "purple")
    screen.blit(textHold, (263, 225))
    if(nextPiece == "line"):
        tempRect = pygame.Rect(270, 150, 80, 20)
        pygame.draw.rect(screen, nextPieceColor, tempRect)
        for x in range(270, 350, 20):
            tempOL = pygame.Rect(x, 150, blockSize, blockSize)
            pygame.draw.rect(screen, "dark gray", tempOL, 1)
    elif(nextPiece == "square"):
        for index, x in enumerate(nextGrid):
            for index2, y in enumerate(x):
                if(y == 1):
                    tempRect = pygame.Rect(270+(20*(index2+1)), 120+(20*(index+1)), 20, 20)
                    pygame.draw.rect(screen, nextPieceColor, tempRect)
                    tempOL = pygame.Rect(270+(20*(index2+1)), 120+(20*(index+1)), blockSize, blockSize)
                    pygame.draw.rect(screen, "dark gray", tempOL, 1)
    else:
        for index, x in enumerate(nextGrid):
            for index2, y in enumerate(x):
                if(y == 1):
                    tempRect = pygame.Rect(260+(20*(index2+1)), 120+(20*(index+1)), 20, 20)
                    pygame.draw.rect(screen, nextPieceColor, tempRect)
                    tempOL = pygame.Rect(260+(20*(index2+1)), 120+(20*(index+1)), blockSize, blockSize)
                    pygame.draw.rect(screen, "dark gray", tempOL, 1)
    if(heldPiece == "line"):
        tempRect = pygame.Rect(270, 250, 80, 20)
        pygame.draw.rect(screen, heldPieceColor, tempRect)
        for x in range(270, 350, 20):
            tempOL = pygame.Rect(x, 250, blockSize, blockSize)
            pygame.draw.rect(screen, "dark gray", tempOL, 1)
    elif(heldPiece == "square"):
        for index, x in enumerate(heldGrid):
            for index2, y in enumerate(x):
                if(y == 1):
                    tempRect = pygame.Rect(270+(20*(index2+1)), 220+(20*(index+1)), 20, 20)
                    pygame.draw.rect(screen, heldPieceColor, tempRect)
                    tempOL = pygame.Rect(270+(20*(index2+1)), 220+(20*(index+1)), blockSize, blockSize)
                    pygame.draw.rect(screen, "dark gray", tempOL, 1)
    else:
        for index, x in enumerate(heldGrid):
            for index2, y in enumerate(x):
                if(y == 1):
                    tempRect = pygame.Rect(260+(20*(index2+1)), 220+(20*(index+1)), 20, 20)
                    pygame.draw.rect(screen, heldPieceColor, tempRect)
                    tempOL = pygame.Rect(260+(20*(index2+1)), 220+(20*(index+1)), blockSize, blockSize)
                    pygame.draw.rect(screen, "dark gray", tempOL, 1)
    if(gameOver):
        tempRect = pygame.Rect(0, 0, 400, 440)
        pygame.draw.rect(screen, "black", tempRect)
        textGameOver = myFont2.render("GAME OVER", False, "red")
        screen.blit(textGameOver, (10, 120))
        textGameOverInst = myFont3.render("Press R to Restart", False, "white")
        screen.blit(textGameOverInst, (80, 200))
        tempString = "Score: %s | Level: %s" % (score, level)
        textGameOverStats = myFont.render(tempString, False, "white")
        tempNum = (440 - len(tempString)*8)/2
        screen.blit(textGameOverStats, (tempNum, 250))
    pygame.display.flip() 
    dt = clock.tick(60)

pygame.quit()