from cmu_graphics import *
import math
import random

class Tile():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.isMine = False
        self.surroundingMines = 0
        self.covered = True
        self.flagged = False

def onAppStart(app):
    app.rows = 0
    app.cols = 0
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.tiles = []
    app.mines = 0
    app.gameStatus = 'homePage'
    app.FPressed = False
    app.flags = 0
    app.timer = 0
    app.stepsPerSecond = 1
    app.testing = []
        
def generateTiles(app):
    app.testing = [[False for i in range(app.rows)] for j in range(app.cols)]
    tiles =  [[Tile(i, j) for i in range(app.rows)] for j in range(app.cols)]
    placedMines = 0
    while placedMines < app.mines:
        col = random.randint(0, app.cols-1)
        row = random.randint(0, app.rows-1)
        if tiles[row][col].isMine == False:
            tiles[row][col].isMine = True
            placedMines += 1
            for i in range(-1,2):
                for j in range(-1,2):
                    if row + i >= 0 and row + i < app.rows and col + j >= 0 and col + j < app.cols:
                        tiles[row+i][col+j].surroundingMines += 1
    return tiles

def redrawAll(app):
    if app.gameStatus == 'homePage':
        drawHomepage(app)
    elif app.gameStatus == 'lost':
        drawLabel('GAME OVER', app.width/2, app.height/2, fill = 'red', size=40)
        minutes =  app.timer // 60
        seconds = app.timer % 60
        if seconds < 10:
            seconds = '0' + str(seconds)
        drawLabel(f'YOU LOST AFTER: {minutes}:{seconds}', 200, 250, size = 15)
        drawRect(150, 280, 100, 50, fill=None, border='black', borderWidth = 8)
        drawLabel('PLAY AGAIN', 200, 305)
    elif app.gameStatus == 'won':
        drawLabel('YOU WON!', app.width/2, app.height/2, fill = 'green', size=40)
        minutes =  app.timer // 60
        seconds = app.timer % 60
        if seconds < 10:
            seconds = '0' + str(seconds)
        drawLabel(f'YOU WON AFTER: {minutes}:{seconds}', 200, 250, size = 15)
        drawRect(150, 280, 100, 50, fill=None, border='black', borderWidth = 8)
        drawLabel('PLAY AGAIN', 200, 305)
    else:
        drawBoard(app)

def drawHomepage(app):
    drawLabel('MINESWEEPER', 200, 100, size=50)
    drawLabel('CLICK BELOW TO PICK A GAME DIFFICULTY', 200, 150, size=15)
    drawRect(150, 180, 100, 50, fill=None, border='black', borderWidth = 8)
    drawLabel('EASY', 200, 205)
    drawRect(150, 260, 100, 50, fill=None, border='black', borderWidth = 8)
    drawLabel('MEDIUM', 200, 285)
    drawRect(150, 340, 100, 50, fill=None, border='black', borderWidth = 8)
    drawLabel('HARD', 200, 365)

def drawBoard(app):
    drawLabel(f'MINES LEFT: {app.mines-app.flags}', 100, 50)
    minutes =  app.timer // 60
    seconds = app.timer % 60
    if seconds < 10:
        seconds = '0' + str(seconds)
    drawLabel(f'TIME ELAPSED: {minutes}:{seconds}', 275, 50)
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.tiles[row][col])

def drawCell(app, row, col, tile):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    label = ""
    if tile.flagged:
        color = 'red'
    elif tile.covered:
        color = 'black'
    else:
        color = None
        label = str(tile.surroundingMines)
        if tile.surroundingMines == 0 or tile.isMine:
            label = ''
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)
    if tile.isMine and not tile.flagged:
        drawCircle(cellLeft + cellWidth/2, cellTop + cellHeight/2, cellWidth/3)
    drawLabel(label, cellLeft + cellWidth/2, cellTop + cellHeight/2)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return (None, None)
    
def onMousePress(app, mouseX, mouseY):
    if app.gameStatus == 'homePage':
        if mouseX >= 150 and mouseX <= 250:
            if mouseY >= 180 and mouseY <= 230:
                app.gameStatus = 'playing'
                app.rows = 9
                app.cols = 9
                app.mines = 10
            elif mouseY >= 260 and mouseY <= 310:
                app.gameStatus = 'playing'
                app.rows = 16
                app.cols = 16
                app.mines = 40
            elif mouseY >= 340 and mouseY <= 390:
                app.gameStatus = 'playing'
                app.rows = 20
                app.cols = 20
                app.mines = 99
        app.tiles = generateTiles(app)
    elif app.gameStatus == 'lost' or app.gameStatus == 'won':
        if mouseX >= 150 and mouseX <= 250 and mouseY >= 280 and mouseY <= 330:
            newGame(app)
    else:
        row, col = getCell(app, mouseX, mouseY)
        if row != None and col != None:
            if app.FPressed:
                app.tiles[row][col].flagged = True
                app.tiles[row][col].covered = False
                app.flags += 1
            elif app.tiles[row][col].flagged:
                app.tiles[row][col].flagged = False
                app.tiles[row][col].covered = True
                app.flags -= 1
            else:
                app.tiles[row][col].covered = False
                for i in range(app.rows):
                    floodfill(app)
                if app.tiles[row][col].isMine == True:
                    app.gameStatus = 'lost'
            if gameIsWon(app):
                app.gameStatus = 'won'
    
def floodfill(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.tiles[row][col].covered == False and app.tiles[row][col].isMine == False and app.tiles[row][col].surroundingMines == 0:
                uncoverSurroundingMines(app, row, col)
                
def uncoverSurroundingMines(app, row, col):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if row + i >= 0 and row + i < app.rows and col + j >= 0 and col + j < app.cols:
                app.tiles[row+i][col+j].covered = False

def gameIsWon(app):
    for row in range(app.rows):
        for col in range(app.cols):
            if app.tiles[row][col].covered:
                return False
            if app.tiles[row][col].isMine and not app.tiles[row][col].flagged:
                return False
    return True

def newGame(app):
    app.tiles = []
    app.gameStatus = 'homePage'
    app.flags = 0
    app.timer = 0

def onKeyPress(app, key):
    if key == 'f':
        app.FPressed = True
    if key == 't':
        for row in range(app.rows):
            for col in range(app.cols):
                app.testing[row][col] = app.tiles[row][col].covered
                app.tiles[row][col].covered = False

def onKeyRelease(app, key):
    if key == 'f':
        app.FPressed = False
    if key == 't':
        for row in range(app.rows):
            for col in range(app.cols):
                app.tiles[row][col].covered = app.testing[row][col]

def onKeyHold(app, keys):
    if 't' in keys:
        for row in range(app.rows):
            for col in range(app.cols):
                app.tiles[row][col].covered = False

def onStep(app):
    if app.gameStatus == 'playing':
        takeStep(app)

def takeStep(app):
    app.timer += 1
    
def main():
    runApp()

main()
