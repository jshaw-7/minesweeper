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
    app.rows = 10
    app.cols = 10
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.selection = None
    app.tiles = generateTiles(app)
    app.gameStatus = 'homePage'
    app.FPressed = False
        
def generateTiles(app):
    tiles =  [[Tile(i, j) for i in range(app.rows)] for j in range(app.cols)]
    for row in range(app.rows):
        col = random.randint(0, app.cols-1)
        tiles[row][col].isMine = True
        if row - 1 >= 0:
            tiles[row-1][col].surroundingMines += 1
            if col - 1 >= 0:
                tiles[row-1][col-1].surroundingMines += 1
            if col + 1 < app.cols:
                tiles[row-1][col+1].surroundingMines += 1
        if row + 1 < app.rows:
            tiles[row+1][col].surroundingMines += 1
            if col - 1 >= 0:
                tiles[row+1][col-1].surroundingMines += 1
            if col + 1 < app.cols:
                tiles[row+1][col+1].surroundingMines += 1
        if col + 1 < app.cols:
            tiles[row][col+1].surroundingMines += 1
        if col - 1 >= 0:
            tiles[row][col-1].surroundingMines += 1
    return tiles

def redrawAll(app):
    if app.gameStatus == 'homePage':
        drawHomepage(app)
    elif app.gameStatus == 'over':
        drawLabel('GAME OVER', app.width/2, app.height/2, fill = 'red', size=40)
    else:
        drawBoard(app)

def drawHomepage(app):
    drawLabel('MINESWEEPER', 200, 100, size=50)
    drawLabel('CLICK BELOW TO PICK A GAME DIFFICULTY', 200, 150, size=15)
    drawRect(150, 180, 100, 50, fill=None, border='black', borderWidth = 8)
    drawLabel
    drawRect(150, 260, 100, 50, fill=None, border='black', borderWidth = 8)
    drawRect(150, 340, 100, 50, fill=None, border='black', borderWidth = 8)

def drawBoard(app):
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
        if tile.isMine:
            label = 'Mine'
        else:
            label = str(tile.surroundingMines)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)
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
        if mouseX >= 100 and mouseX <= 300 and mouseY >= 200 and mouseY <= 300:
            app.gameStatus = True
    else:
        row, col = getCell(app, mouseX, mouseY)
        if row != None and col != None:
            if app.FPressed:
                app.tiles[row][col].flagged = True
            elif app.tiles[row][col].flagged:
                app.tiles[row][col].flagged = False
            else:
                app.tiles[row][col].covered = False
                if app.tiles[row][col].isMine == True:
                    app.gameOver = True

def onKeyPress(app, key):
    if key == 'f':
        app.FPressed = True

def onKeyRelease(app, key):
    if key == 'f':
        app.FPressed = False

def main():
    runApp()

main()
