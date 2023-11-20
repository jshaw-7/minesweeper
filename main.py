from cmu_graphics import *

class Board():
   
   def __init__(self, rows, cols, totalMines):
       self.rows = rows
       self.cols = cols
       self.totalMines = totalMines
       self.tiles = [[Tile() for i in range(rows)] for j in range(cols)]

class Tile():
    
    def __init__(self):
        self.isMine = False
        self.surroundingMines = 0
        self.covered = True

    def __repr__(self):
        return str(self.isMine)
    
    def __hash__(self):
        return hash(str(self))

def onAppStart(app):
    app.rows = 5
    app.cols = 5
    app.boardLeft = 50
    app.boardTop = 75
    app.boardWidth = 300
    app.boardHeight = 300
    app.cellBorderWidth = 2
    app.tiles = []
    for row in range(app.rows):
        app.tiles.append([])
        for col in range(app.cols):
            app.tiles[row].append(Tile())

def redrawAll(app):
    drawBoard(app)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.tiles[row][col])

def drawCell(app, row, col, tile):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=None, border='black',
             borderWidth=app.cellBorderWidth)
    drawLabel(str(tile.surroundingMines), cellLeft + cellWidth/2, cellTop + cellHeight/2)

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def main():
    runApp()

main()
