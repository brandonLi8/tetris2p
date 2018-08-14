import pygame, random, sys, copy, math
#Tetris by Brandon Li
###########################################
#          Widely Used Functions 
###########################################
def getCellBounds(row, col):
  #returns (x0, y0, x1, y1) corners/bounding box of given cell if the board 
  #was at (0, 0). We do this because our surfaces start at (0, 0) then we move
  #them into the correct position in our Board class.
  gridWidth  = 200
  gridHeight = 420
  x0 = gridWidth * col / cols
  x1 = gridWidth * (col + 1) / cols
  y0 = gridHeight * row / rows
  y1 = gridHeight * (row + 1) / rows
  return (x0, y0, x1, y1)
def drawCell(data, row, col, color, width, outline, cell, surface):
  #draws a cell at the given row, col on the given surface and type
  #of cell (backround cell, block, etc.)
  (x0, y0, x1, y1) = getCellBounds(row, col)
  if cell == 'backround cell': 
    pygame.draw.rect(surface, outline, (x0, y0, x1 - x0, y1 - y0), width)
    pygame.draw.rect(surface, color, (x0, y0, x1 - x0, y1 - y0))
  elif cell == 'block': 
    pygame.draw.rect(surface, color, (1, 1, x1 - x0 - 0.5, y1 - y0 - .5))
    pygame.draw.rect(surface, outline, (0, 0, x1 - x0 - 1, y1 - y0 - 1), width)
    pygame.draw.rect(surface, outline, (0, 0, x1 - x0, y1 - y0), width)  
    pygame.draw.rect(surface, outline, (4 , 4, x1 - x0 - 9, y1 - y0 - 7.9), 
                     width)
  elif cell == 'next': 
    pygame.draw.rect(surface, color, (0, 0, x1 - x0 - 0.5, y1 - y0 - .5))
    pygame.draw.rect(surface, outline, (0, 0, 15 , 15), width)
    pygame.draw.rect(surface, outline, (0, 0, 16, 16), width)  
    pygame.draw.rect(surface, outline, (3, 3, x1 - x0 - 11, y1 - y0 - 11), 
                     width)   
  elif cell == "ghost": 
    pygame.draw.rect(surface, color, (1, 1, 17,17), width)
def makeboard(data):
  #We create an 2D list filled with the empty color and in Create Board we 
  #then draw the chekerboard backround by checking if row + col is even or odd
  return [([data.emptyColor[0]]*data.cols) for row in range(data.rows)] 
def generatePieces(data): 
  #generate all the pieces for the game. Take the  7 pieces, scramblea them, and
  #returna the list of the pieces scrambled. Everytime a newFallingPiece is 
  #needed we get the first item of this list and delete it. Onces there are 0 
  #pieces, we re call this function to re gather the 7 pieces, rescramble and 
  #use them, then re do this again. 
  result = [] 
  while len(result) != len(data.tetrisPieces): #once result is len(7), stop
    current = random.randrange(len(data.tetrisPieces))
    if data.tetrisPieces[current] not in result:#every piece should be different 
      result.append(data.tetrisPieces[current])
  return result  
def rotateMatrix(m): 
  cols = len(m[0])
  rows =  len(m)
  result = [([0] * cols) for row in range(rows)]
  for col in range(0, cols):   
    for row in range(0, rows):
      result[col][row] = (m[row][col])
  return result
def flipMatrix(m):
  result = [0] * len(m)
  for i in range(len((m))):
    currentReverse = (m[i])[::-1]
    result[i] = copy.deepcopy(currentReverse)
  return result
###########################################
#'Create' fucntions create a new surface and returns them so that we don't 
# have to keep drawing everything every frame (ineffiecient), but instead 'blit' 
# the surface on to canvas (much more effiecient)
###########################################
#create blocks
def createBlocksInTetrisPieces(data, size, type):
  #This will loop throught tetris pieces and make a surface of each block with
  #the specified type and size. Mostly used in init functions to create the 
  #surfaces of, for example, the ghost block
  result = []
  for i in range(len(data.tetrisPieces)):
    piece = data.tetrisPieces[i]
    surface  = pygame.Surface((size , size)) 
    color = data.tetrisPieceColors[i]
    borderColor = data.borderColors[i]
    rows, cols = len(piece), len(piece[0])
    for row in range(rows):
      for col in range(cols):
        if piece[row][col] == True:              
          drawCell(data, row, col, color, 2, borderColor, type, surface)
    result.append(surface)
  return result
def createBlocks(data):
  # returns a list of surfaces of each single block in the order
  # of data.tetrisPieces
  return createBlocksInTetrisPieces(data, cellSize, "block")
def createNextBlocks(data):
  # returns a list of surfaces of each single block in the order
  # of data.tetrisPieces but sized down for the Next Box
  return createBlocksInTetrisPieces(data, 16, "next")
def createDirt():
  #the 'dirt' block is the block for when lines are sent
  return pygame.image.load("block.png")
def createGhost(data):
  #Create and return a single ghost block surface.
  surface = pygame.Surface((19, 19), pygame.SRCALPHA) #we need it to be clear
  surface.fill((0 ,0, 0, 0)) #clear, alpha level 0
  drawCell(data, 0, 0, (150, 150, 150), 2, None, "ghost", surface)
  return surface
#create board 
def createBoard(data, board):
  #returns a board surface that contains the board for us to draw with
  #it first draws every cell in the board then draws the placed blocks on top
  boardSurface = pygame.Surface((gridWidth, gridHeight)) 
  for row in range(data.rows):
    for col in range(data.cols):        
      if (board.board[row][col] == data.emptyColor[0] 
          or board.board[row][col] == data.emptyColor[1]):
        if (row + col)%2 == 0: #evens
          drawCell(data, row, col, data.emptyColor[0],
                   3, (28, 28, 28), "backround cell", boardSurface) 
        else: #odds
          drawCell(data ,row, col, data.emptyColor[1],
                    3, (28 ,28 ,28), "backround cell", boardSurface)
  for row in range(data.rows):
    for col in range(data.cols):  
      if (board.board[row][col] != data.emptyColor[0] 
          and board.board[row][col] != data.emptyColor[1]): 
        if board.board[row][col] == "dirt":
          blockSurface = data.dirtBlock
        else:  
          index = data.tetrisPieceColors.index(board.board[row][col])
          blockSurface = data.createBlocks[index]
        rect = blockSurface.get_rect()         
        rect.move_ip(col*20, (row*20))
        boardSurface.blit(blockSurface, rect)
  return boardSurface
def drawRectAroundBoard(data, surface, x0, y0):
  pygame.draw.rect(
    surface , (80, 80, 80), 
    (x0 + gridWidth, lengthBetweenTopAndStartOfBoard + 9, 21, gridHeight-6), 6)
  pygame.draw.rect(
    surface , (data.emptyColor[0]), 
    (x0 + gridWidth, lengthBetweenTopAndStartOfBoard + 13, 19, gridHeight - 13))
  pygame.draw.rect(
    surface , (80, 80, 80), 
    (x0 - 3, y0 + 12, gridWidth + 6,gridHeight - 9), 10)
def createBackroundSurface(data, type):
  #this function is the backround surface and draws the lines surounding the 
  #boards.
  backroundSurface = pygame.Surface((width, height))
  if type == "marathon":
    backround = pygame.image.load("backround3.png")
  else:
    backround = pygame.image.load("backround.png")
  backroundSurface.blit(backround, (0, 0))
  if type == "multiplayer":
    x0, y0 = margin, lengthBetweenTopAndStartOfBoard
    drawRectAroundBoard(data, backroundSurface,x0, y0)
    x0 += gridWidth + widthBetweenBoards
    drawRectAroundBoard(data, backroundSurface,x0, y0)
    #draw the line that seperates the two sides
    pygame.draw.line(backroundSurface, (100, 100, 100),
                     (width/2, 60), (width/2, height - 60), 7)
    return backroundSurface
  elif type == "marathon":
    x0, y0 = width/2- 0.5* gridWidth, lengthBetweenTopAndStartOfBoard
    drawRectAroundBoard(data, backroundSurface,x0, y0)
    return backroundSurface
def createLinesSurface(data):
  #the second part of the backround surface. We need to create the surface
  #at the top of the board the just gives a little bit of the first row
  #We need this surface to draw on top of the board and falling Piece.
  img = pygame.image.load("backroundTop.png")
  surface = pygame.Surface((gridWidth, 40), pygame.SRCALPHA)
  surface.blit(img, (0, 0))
  pygame.draw.rect(surface , (80, 80, 80), (-10, -10, gridWidth + 15, 48), 10) 
  surface2 = surface.copy()
  return (surface, surface2)
def createNext(data):
  #returns the surface for the box that contains the Next block
  nextSurface = pygame.Surface((70, 70)) 
  nextSurface.fill((46, 46, 46))
  pygame.draw.rect(nextSurface, (5, 5, 5), (6, 6, 62, 62))
  pygame.draw.rect(nextSurface, (90, 90, 90), (1, 1, 66, 66), 6)
  return nextSurface
#create text  
def createGameOverSurfaces(data, text, text2):
  myfont = pygame.font.Font('KOMIKAX_.woff', 47)
  textSurface = myfont.render(text, True, (250, 230, 78))
  text2Surface = myfont.render(text2, True, (105, 186, 239))
  textSurface2 = myfont.render(text, True, (231, 164, 25))
  text2Surface2 = myfont.render(text2, True, (34, 83, 163))
  return (textSurface, textSurface2, text2Surface, text2Surface2)
def createWinnerSurfaces(data):
  # returns (winSurface, winSurface2, loseSurface, loseSurface2). 
  # These are text surfaces to blit when the game is over We have two of
  # each becuase we use two different surfaces next to each other to 
  # create a 3D image
  return createGameOverSurfaces(data, "YOU WIN!", "YOU LOSE!")
def createTiedSurfaces(data):
  # We need to surfaces for "TIE!" becuse the colors are different for each side
  return createGameOverSurfaces(data, "TIE!", "TIE!")
def createPausedSurface(data):
  #surfaces for paused text
  (paused, paused2) = createText("Pause",(255,255,255),(204, 102, 0),47)
  (unpause, unpause2) = createText( "press 'p' to unpause",(255,255,255),(204, 102, 0),18)
  return (paused, paused2, unpause, unpause2)
def createText(msg, color1, color2, size):
  #this returns two surfaces for the 3-D effect
  pygame.font.init()
  myfont = pygame.font.Font('KOMIKAX_.woff', size)
  text = myfont.render(msg, True, color1)
  text2 = myfont.render(msg, True, color2)  
  return (text, text2)
def createText2(msg, color1, color2, size, backround):
  #this returns two surfaces for the 3-D effect
  pygame.font.init()
  myfont = pygame.font.Font('KOMIKAX_.woff', size)
  text = myfont.render(msg, True, color1, backround)
  text2 = myfont.render(msg, True, color2, backround)  
  return (text, text2)
def nextText(data):
  return createText("Next",(255,255,255),((0,255,255)),24)
def holdText(data): 
  return createText("Hold",(255,255,255),(51, 153, 255),24)
#create buttons
def createBlueButton(text):
  #returns 2 surfaces for the blue button at the start. 1 for when the mouse 
  #isnt over it and 1 when the mouse is over it
  buttonSurface = pygame.Surface((235, 73), pygame.SRCALPHA)  
  hoverSurface = pygame.Surface((235, 73), pygame.SRCALPHA)
  buttonImage = pygame.image.load("DarkButton.png")
  hoverImage = pygame.image.load("lightButton.png")
  buttonSurface.fill((255, 255, 255, 0))
  buttonSurface.blit(buttonImage, (-1, -1))
  hoverSurface.fill((255, 255, 255,0))
  hoverSurface.blit(hoverImage, (0, -2))   
  buttonText = createText(str(text), (25, 25, 112), (250, 250, 255), 20)
  buttonSurface.blit(buttonText[0], (10, 8))
  buttonSurface.blit(buttonText[1], (11, 8))
  hoverSurface.blit(buttonText[0], (10, 8))
  hoverSurface.blit(buttonText[1], (11, 8))
  return (buttonSurface, hoverSurface)
def createHomeButton():
  buttonSurface = pygame.Surface((49, 49),pygame.SRCALPHA) 
  hoverSurface = pygame.Surface((49, 49),pygame.SRCALPHA) 
  buttonSurface.fill((2, 3, 5, 0))
  hoverSurface.fill((2, 3, 5, 0))
  buttonImage = pygame.image.load("HomeButton.png")
  hoverImage = pygame.image.load("HomeButton2.png")
  hoverSurface.blit(hoverImage, (-1, -1))  
  buttonSurface.blit(buttonImage, (-1, -1))
  return (buttonSurface, hoverSurface)
#create start screen
def createStart(data):
  surface = pygame.Surface((width, height))
  backround = pygame.image.load("backround2.png")
  surface.blit(backround, (0, 0))
  img = pygame.image.load("tetris.png")
  surface.blit(img, img.get_rect())
  data.startSurface = surface
################################################################################
#                                 Classes
################################################################################
class Board(pygame.sprite.Sprite):
  #This class stores the actual board list and calls createBoard surface to draw 
  #with. Once we place a block we update the board list and check to remove full
  #rows. If there are full rows we then reupdate the list removing the full rows
  #and also send lines to the other board. We then re call createBoard surface 
  #and recreate a brand new surface with the correct blocks.
  def __init__(self, data, state):
    #state is 'left' for the left side, 'right' for the right side
    pygame.sprite.Sprite.__init__(self)
    self.emptyColor = ((36, 36, 36), (41, 41, 41)) #rgb
    self.state = state
    self.board = makeboard(data)
    self.image = createBoard(data, self) #create the surface
    self.rect = self.image.get_rect()
    self.moveBoard()
    self.run = 0 #we keep track of runs
    self.listOfPlaced = [(-1,-1)]
    self.fireSurface = pygame.image.load("fire.png")
  def moveBoard(self):
    #moves the board to the correct posision
    if self.state == 'left':
      self.rect.move_ip(margin ,lengthBetweenTopAndStartOfBoard)
    if self.state == 'right':
      self.rect.move_ip((margin + gridWidth + widthBetweenBoards),
                        lengthBetweenTopAndStartOfBoard)
  def drawBoard(self,data):  
    self.drawPendingSendLines(data)
    canvas.blit(self.image, self.rect)    
  def pieceIsLegal(self, piece, r, c, data):
    #returns if any piece is legal in the board
    rows = len(piece.piece)
    cols = len(piece.piece[0])
    for row in range(rows):
      for col in range(cols):
        if piece.piece[row][col] :
          nR = (r + row) # new row
          nC = (c + col) # new col
          if len(piece.piece) == 4: 
            #the iPiece spawns higher so we give it 1 more row to be legal
            if (nC > 9 or nC < 0 or nR >= 21 or nR < -1): 
              return False  
            if nR > -1 : #we cant index a negative row
              if not((self.board[int(nR)][int(nC)] == data.emptyColor[1] or 
                      self.board[int(nR)][int(nC)] == data.emptyColor[0])): 
                return False      
          else:
            if (nC > 9 or nC < 0 or nR >= 21 or nR < 0): 
              return False        
            if not((self.board[int(nR)][int(nC)] == data.emptyColor[1] or 
                    self.board[int(nR)][int(nC)] == data.emptyColor[0])):   
              return False
    return True 
  def fallingPieceIsLegal(self, data, piece):
    return self.pieceIsLegal(piece, piece.row, piece.col, data)
  def isColoredRow(self, row, data): 
    #this function returns if the row has a block in it that isn't the 
    #empty color, but also returns False if the entire row is filled.
    if "dirt" in row: #the row is all dirk blocks, we do't want to remove it
      return True
    if data.emptyColor[0] not in row and data.emptyColor[1] not in row:
      #entire row filled with blocks because emptyColor not in the row
      #we need to clear this row
      return False
    for block in row:
      if (block != data.emptyColor[0] or block != data.emptyColor[1]): 
        # A block isn't the empty color: there is a block inside the row
        # we don't want to remove
        return True
    return False 
  def removeFullRows(self, data): 
    #this takes an intresting approach: I copy all the rows that have color and 
    #I dont copy all the rows that have nothing or are completly full     
    #then i can add this to a new board
    rowsWithBlocksInside = []
    result =[]
    for i in range(len(self.board)):    
      if self.isColoredRow(self.board[i], data):
        #if we have found a full row
        rowsWithBlocksInside  = copy.deepcopy(self.board[i])
        result.append(rowsWithBlocksInside)    
    self.board = [([self.emptyColor[0]]*data.cols) for row in range(data.rows)] 
    for i in range(len(result)):
      self.board[len(self.board) - i - 1] = result[len(result) - i - 1]
  def howManyLines(self):
    #returns how many lines to send 
    #self.listOfPlaces is a tuple of (how many lines cleared, what run)
    # and is always len(2)
    if self.listOfPlaced[0][0] == 4 and self.listOfPlaced[1][0] == 4:
      #double tetris
      return 6
    if self.listOfPlaced[1][0]==4:
      return 4
    if self.listOfPlaced[len(self.listOfPlaced)-1][0] == 2:
      return 1
    if self.listOfPlaced[len(self.listOfPlaced)-1][0] == 3: 
      return 2
    #1 line cleared
    return 10
  def sendLines(self, data, lines):
    #called when placed. This function first sets its variables to our board
    #and the other board. We make a copy of the other board, so that we can
    #empty the other board, and use copy each row from the copy to the other 
    #board
    if self.state == 'left':
      board = data.board
      other = data.board2
    if self.state == 'right':
      board = data.board2
      other = data.board
    copyOfBoard = copy.deepcopy(other.board)   
    other.board = makeboard(data)
    for i in range(lines):
      other.board[len(self.board) - i - 1] = ["dirt"] * 10
    #we reset the other board and send the correct amount of lines of "dirt"
    for i in range(len(copyOfBoard)):
      #We make a copy of the other board, so that we can
      #empty the other board, and use copy each row from the copy to the other 
      #board
      if i - lines > -1:
        #has to be in bounds
        other.board[i-lines] = copyOfBoard[i]  
    other.image = createBoard(data, other) #re-create the surface
    other.rect = self.image.get_rect()
    if self.state == 'left': #set the other board to other
      data.board2 = other
      data.board2.moveBoard()
    elif self.state == 'right':
      data.board = other
      data.board.moveBoard()
  def resetHoldCount(self, data):
    if self.state == 'left': 
      data.holdCount = 0
    if self.state == 'right':
      data.holdCount2= 0
    if self.state == 'marathon':
      data.marathon.holdCount = 0
  def scorePoints(self,data):
    if self.listOfPlaced[len(self.listOfPlaced)-1][0] > 0:
      if self.listOfPlaced[len(self.listOfPlaced)-1][0] == 1: 
        data.marathon.single = True
        data.marathon.points += (data.marathon.level +1)*4
        return True
      if self.listOfPlaced[len(self.listOfPlaced)-1][0] == 2: 
        data.marathon.double = True
        data.marathon.points += (data.marathon.level +1)*10
        return True
      if self.listOfPlaced[len(self.listOfPlaced)-1][0] == 3: 
        data.marathon.triple = True
        data.marathon.points += (data.marathon.level +1)*30
        return True
      if self.listOfPlaced[0][0] == 4 and  self.listOfPlaced[1][0] == 4: 
        data.marathon.doubleTetris = True
        data.marathon.points += (data.marathon.level +1)*120
        data.marathon.points += (data.marathon.level +1)*50
        return True
      if self.listOfPlaced[1][0] == 4: 
        data.marathon.tetris = True
        data.marathon.points += (data.marathon.level +1)*120
        return True

  def placeFallingPiece(self, data, piece):
    #this function first resets the hold count becuase every time you place,
    #you can hold again. Then this function places piece into self.board and 
    #calulate how many row needed to clear, and asign it to rowsCleared, and
    #use that number to put in self.listOfPlaced to calculate how many rows to
    #send to the other board. Once we have that we set our data.sendLine values
    #to the correct value, so we can make it so when the other person places, we
    #send lines. After this we reset our own board's surface with the correct
    #blocks inside of it
    self.run += 1 #every time you place the run goes up 1. 
    self.resetHoldCount(data) #reset hold count
    for row in range(len(piece.piece)): 
      for col in range(len(piece.piece[0])):#loop throught piece list
        if piece.piece[row][col]:
          #place piece into self.board
          self.board[int(piece.row + row)][int(piece.col + col)] = piece.color
    rowsCleared = 0
    #calculate how many rows cleared and add to listOfPlaced to know how many
    #lines to sent to the other board.
    
    for row in self.board:
      if self.emptyColor[1] not in row and self.emptyColor[0] not in row:
        if row != ["dirt"] *10:   
          rowsCleared += 1
    
    self.listOfPlaced.append((rowsCleared, self.run))
    if len(self.listOfPlaced) > 2:
      self.listOfPlaced.pop(0)
    if self.state == "marathon":
      self.scorePoints(data)
    if self.state != "marathon":
      if self.howManyLines() > 0: #calulate how many lines to send
        if self.state == "left": #send to right
          data.sendLines += self.howManyLines()
          if data.sendLines2 > 0: #cancel
            data.sendLines2, data.sendLines = 0, 0
        elif  self.state == "right":
          data.sendLines2 += self.howManyLines()
          if data.sendLines > 0: #cancel
            data.sendLines2, data.sendLines = 0, 0
    if rowsCleared > 0:
      self.removeFullRows(data)
    self.image = createBoard(data, self) 
    if self.state != "marathon":
      self.rect = self.image.get_rect()
      self.moveBoard()
  def drawPendingSendLines(self, data):
    #draws the red bar
    if data.sendLines2 > 0: #send to left
      for i in range(data.sendLines2):
        canvas.blit(self.fireSurface, (308, 525 - (i*20)))
    if data.sendLines > 0:#send to right
      for i in range(data.sendLines):
        canvas.blit(self.fireSurface, 
                    (308 + gridWidth + widthBetweenBoards, 525 - (i*20)))

class Piece(pygame.sprite.Sprite):
  #the Piece class stores the actual piece list and all the other usefull
  #atributes of a piece (color,borderColor,etc.). It calls createBlocks to 
  #create a surface of the correct block everytime newFallingPiece is called.
  #It can move the piece if needed and rotate the piece. Moving the Piece is 
  #updating the row and the col. Rotating the piece is rotating the 2d list
  #then checking the wallkick algorithm from http://tetris.wikia.com/wiki/SRS
  #and if the wall kick still isnt available then cancel the rotation.
  def __init__(self, state, data):
    pygame.sprite.Sprite.__init__(self)
    self.state = state
    self.row, self.col = 0, 0
    self.color = -1
    self.borderColor = -1
    self.piece = 0
    self.rows, self.cols = 0, 0
    self.fallingOrientation = 0
    self.allBlocksSurfaces = data.createBlocks
    self.surface = 0
  def regenerateGamePiecesList(self, data):
    #regerate data.gamePieces if it is empty
    if len(data.gamePieces) == 0: 
      data.gamePieces = generatePieces(data)
    if len(data.gamePieces2) == 0: 
      data.gamePieces2 = generatePieces(data)
    if len(data.marathon.pieces) == 0:
      data.marathon.pieces = generatePieces(data)
  def updateGamePiecesList(self, data):
    if self.state == 'left':  
      data.gamePieces.pop(0)
    elif self.state == 'right': 
      data.gamePieces2.pop(0)
    elif self.state == "marathon":
      data.marathon.pieces.pop(0)
  def getWinner(self, data):
    if self.state == 'left':
      if not (data.board.pieceIsLegal(self, self.row, self.col, data)):
      #check right away for it the game is over
        data.gameOver = True
        data.player2Win = True
    elif self.state == 'right':
      if not (data.board2.pieceIsLegal(self, self.row, self.col, data)):
        data.gameOver = True
        data.player1Win = True   
    elif self.state == 'marathon':
      if not (data.marathon.board.pieceIsLegal(self, self.row, self.col, data)):
        data.marathon.gameOver = True   
  def newFallingPiece(self, data): 
    #updates all the atributes of the piece (row,col,colors,etc.) and 
    #data.gamePieces, set the correct surface block, and checks if a player
    #has lost 
    if self.state == 'left':  #set the next piece
      self.piece = data.gamePieces[0]
    elif self.state == 'right': 
      self.piece = data.gamePieces2[0]
    elif self.state == 'marathon': 
      self.piece = data.marathon.pieces[0]
    self.regenerateGamePiecesList(data)
    index = data.tetrisPieces.index(self.piece) 
    self.surface = self.allBlocksSurfaces[index]
    self.color = data.tetrisPieceColors[index]
    self.row = 0
    self.col = 3
    self.rows, self.cols = len(self.piece), len(self.piece)
    if self.piece is iPiece : #special case 
      self.row = -1
    if self.piece is oPiece : #special case  
      self.col = 4
    self.fallingOrientation  = 0 #the rotation
    self.getWinner(data)
    self.updateGamePiecesList(data)
    self.regenerateGamePiecesList(data)
    self.fallingOrientation = 0
  def drawFallingPiece(self, data): 
    #draws the piece by iterating through self.piece and placing the surface
    # in the correct spot if neccesary
    for row in range(len(self.piece)):
      for col in range(len(self.piece[0])):     
        if self.piece[row][col]:
          currentSurface = self.surface
          rect = currentSurface.get_rect()     
          x0, y0 = margin, lengthBetweenTopAndStartOfBoard
          if self.state == "marathon":
             x0 += width/2-gridWidth
          if self.state == 'right':
            x0 += gridWidth + widthBetweenBoards  
          rect.move_ip(x0 + ((self.col + col)*20), y0 + ((self.row+row)*20))
          canvas.blit(currentSurface, rect)
  def moveFallingPiece(self, data, drow, dcol): 
    #moves the falling piece in delta row, delta col or change
    #in row, change in col, and if it is illegal to do so, it undos the move
    board = []
    if self.state == 'left':
        board = data.board
    elif self.state == 'right': 
        board = data.board2
    elif self.state == 'marathon': 
        board = data.marathon.board
    self.row += drow
    self.col+= dcol
    if not board.fallingPieceIsLegal(data, self):
        self.row -= drow
        self.col -= dcol 
        return False
    return True
  def wallKickHelper(self, data, listToCheck):
    for tup in listToCheck:
      if self.moveFallingPiece(data,tup[0],tup[1]):
        return True
    return False
  def wallKick(self,data): 
    #full algorithm at http://tetris.wikia.com/wiki/SRS
    count = self.fallingOrientation %4
    if count== 0:
      return self.wallKickHelper(data,[(0,0),(0,-1),(-1,-1),(2,0),(2,-1)])
    if count== 1:
      return self.wallKickHelper(data,[(0,0),(0,1),(1,1),(-2,0),(-2,1)])
    if count== 2:
      return self.wallKickHelper(data,[(0,0),(0,1),(-1,1),(2,0),(2,1)])
    if count== 3:
      return self.wallKickHelper(data,[(0,0),(0,-1),(1,-1),(-2,0),(-2,-1)])
    return False
  def iPieceWallKick(self,data):#iPiece is an exception
    count = self.fallingOrientation %4
    if count== 0:
      return self.wallKickHelper(data,[(0,0),(0,-2),(0,1),(1,-2),(-2,-1)])          
    if count== 1:
      return self.wallKickHelper(data,[(0,0),(0,-1),(0,2),(-2,-1),(1,2)])          
    if count== 2:
      return self.wallKickHelper(data,[(0,0),(0,2),(0,-1),(-1,2),(2,-1)])            
    if count== 3:
      return self.wallKickHelper(data,[(0,0),(0,1),(0,-2),(-2,1),(-1,-2)])        
    return False
  def rotateFallingPiece(self, data):
    self.fallingOrientation += 1
    if self.state == 'left':
      board = data.board
    elif self.state == 'right': 
      board = data.board2
    elif self.state == 'marathon': 
      board = data.marathon.board
    piece = copy.deepcopy(self.piece) 
    #this is to make a copy so that if wall kick doesn't not work, 
    #the piece stays the same   
    if piece is oPiece:#the only piece that is length 2 is the square piece
      self.piece = piece #do nothing
    else: #every other piece
      self.piece = flipMatrix(rotateMatrix(self.piece))
      if len(piece) == 4: # the iPiece
        self.iPieceWallKick(data)
      else:
        self.wallKick(data)  #first rotate it, then wall kick it
      if not board.fallingPieceIsLegal(data, self):
        self.piece = piece  
        #if still illegal than return to original rotates the piece
def intToTime(i):
  minute = str(math.ceil(i/60)-1)
  seconds = str(int(i%60))
  if len(seconds) == 1:
    return minute +":0"+seconds
  else:
    return minute +":"+seconds
class Text(object):
  #this class draws all the text on canvas
  def __init__(self, data):
    pygame.font.init()
    self.gameOverSurfaces = createWinnerSurfaces(data)
    self.gameOver = createText("Game Over!", (255,255,255),(0,255,0), 47)
    self.tiedSurfaces = createTiedSurfaces(data)
    self.paused = createPausedSurface(data)
    self.timeTillOver = 120
    self.sentLinesSurface = createText("Sent Lines:", 
                                       (255, 255, 255), (255, 255, 255), 25)
    self.sentLines = 0
    self.sentLines2 = 0
  def drawMarathonStart(self,data):
    timeRemaining = int((data.marathon.startScreenCount//1)+1)
    if timeRemaining > 0:
      self.drawBeginningAnimationText(canvas, str(timeRemaining), width/2, 
                                      height/2 - 130, 130, 149, (255, 207, 0),
                                      (225, 137, 0))
    if timeRemaining == 0:
      self.drawBeginningAnimationText(canvas, "GO!", width/2, 
                                      height/2 - 130, 90, 93, (106, 246, 1),
                                      (16, 153, 5))
       
    if timeRemaining == -1:
      data.marathon.startScreenDone = True 
  def drawStartScreen(self, data):
    timeRemaining = int(3-(data.timeElapsedInMultiplayer //1))
    if timeRemaining > 0:
      for i in range(2):
        self.drawBeginningAnimationText(canvas, str(timeRemaining), margin +
                                        (1 + (i*2))*gridWidth/2 
                                        + i*widthBetweenBoards, height/2 - 130, 
                                        130, 149, (255, 207, 0), (225, 137, 0))
    if timeRemaining == 0:
      for i in range(2):
        self.drawBeginningAnimationText(canvas, "GO!", margin + 
                                        (1 + (i*2))*gridWidth/2 
                                        + i*widthBetweenBoards + 10, 
                                        height/2 - 130, 100, 105, (106, 246, 1),
                                        (16, 153, 5))
    if timeRemaining == -1:
      data.startScreenDone = True 
  def drawBeginningAnimationText(self, surface, text, x, y, 
                                 fontSize1, fontSize2, color1, color2): 
    myfont = pygame.font.Font('Comic-Panels.woff', 
                              fontSize1)
    myfont2 = pygame.font.Font('Comic-Panels.woff', 
                               fontSize2)
    textsurface = myfont.render(text, True, color1)
    textsurface2 = myfont2.render(text, True, color2)
    rect = textsurface.get_rect()
    rect2 = textsurface2.get_rect()
    rect.midtop = (x, y + 5)
    rect2.midtop = (x, y)
    surface.blit(textsurface2, rect2)
    surface.blit(textsurface, rect)
  def drawGameOver(self, data, state):
    if data.drawTie and state != "marathon":
      (winSurface, winSurface2, loseSurface, loseSurface2) = self.tiedSurfaces
    else:
      (winSurface,winSurface2,loseSurface,loseSurface2) = self.gameOverSurfaces
    winRect = winSurface.get_rect()
    winRect2 = winSurface2.get_rect()
    loseRect = loseSurface.get_rect()
    loseRect2 = loseSurface2.get_rect()
    winRect.midtop = (margin + gridWidth/2, 230)
    loseRect.midtop = (margin + 3*gridWidth/2 + widthBetweenBoards + 7,230)
    winRect2.midtop = (margin + gridWidth/2 + 1,230)
    loseRect2.midtop = (margin + 3*gridWidth/2 + widthBetweenBoards+  8,230)
    if state == "marathon":
      (surface1, surface2) = self.gameOver
      rect1, rect2 = surface1.get_rect(),surface2.get_rect()
      rect1.midtop = (width/2, 230)
      rect2.midtop = (width/2 + 1,230)
      canvas.blit(surface1, rect1)
      canvas.blit(surface2, rect2)
      return True
    if data.drawTie or data.player1Win:
      canvas.blit(winSurface, winRect)
      canvas.blit(loseSurface, loseRect)
      canvas.blit(winSurface2, winRect2)
      canvas.blit(loseSurface2, loseRect2)
    elif data.player2Win: #swap
      canvas.blit(winSurface, loseRect)
      canvas.blit(loseSurface, winRect)
      canvas.blit(winSurface2, loseRect2)
      canvas.blit(loseSurface2, winRect2)
  def drawPaused(self, state):
    (paused, paused2, unpause, unpause2) = self.paused
    rect = paused.get_rect()
    rect2 = paused.get_rect()
    rect.midtop = (margin + gridWidth/2, 250)
    rect2.midtop = (margin + gridWidth/2+2, 251)
    if state == "marathon":
      canvas.blit(paused, (margin + gridWidth/2+140, 250))
      canvas.blit(paused2, (margin + gridWidth/2+142, 251))
    else:
      canvas.blit(paused, rect)
      canvas.blit(paused2, rect2)
      rect.move_ip(widthBetweenBoards + gridWidth, 0)
      rect2.move_ip(widthBetweenBoards + gridWidth, 0)
      canvas.blit(paused, rect)
      canvas.blit(paused2, rect2)
    rect = unpause.get_rect()
    rect2 = unpause2.get_rect()
    rect.midtop = (margin + gridWidth/2, 320)
    rect2.midtop = (margin + gridWidth/2+1, 320)
    if state == "marathon":
      canvas.blit(unpause, (margin + gridWidth/2+115, 320))
      canvas.blit(unpause2, (margin + gridWidth/2+116, 320))
      return True
    canvas.blit(unpause, rect)
    canvas.blit(unpause2, rect2)
    rect.move_ip(widthBetweenBoards + gridWidth, 0)
    rect2.move_ip(widthBetweenBoards + gridWidth, 0)
    canvas.blit(unpause, rect)
    canvas.blit(unpause2, rect2)

  def drawTime(self, data):
    if self.timeTillOver//1 == -1:
      data.gameOver = True
      if self.sentLines2 > self.sentLines:
        data.player2Win = True
      if self.sentLines > self.sentLines2:
        data.player1Win = True
      if self.sentLines == self.sentLines2:
        data.drawTie = True
    if data.startScreenDone and not data.paused and not data.gameOver:
      self.timeTillOver -= data.timeSinceLastFrame
    text = ""
    if not data.startScreenDone or self.timeTillOver//1 + 1 == 120:
      text = "2:00"
    elif self.timeTillOver//1 + 1 == 60:
      text = "1:00"
    elif data.gameOver:
      text = "0:00"
    else:
      text = intToTime(self.timeTillOver//1 + 1)
    myfont = pygame.font.Font('KOMIKAX_.woff', 50)
    surface = myfont.render(text, True, (255,255,255), (4,7,12))  
    canvas.blit(surface, (width/2-60, 0))
  def drawSentLines(self, data):
    canvas.blit(self.sentLinesSurface[0], (0, 600))
    canvas.blit(self.sentLinesSurface[0], (gridWidth + widthBetweenBoards, 600))
    self.sentLines, self.sentLines2 = 0, 0
    for row in data.board.board:
      if "dirt" in row:
        self.sentLines2 += 1
    for row in data.board2.board:
      if "dirt" in row:
        self.sentLines += 1   
    text1 = createText(str(self.sentLines), (255, 255, 255), (255, 255, 255),30)
    canvas.blit(text1[0], (180,595))
    text2 = createText(str(self.sentLines2), (255, 255, 255), (255,255,255), 30)
    canvas.blit(text2[0], (180 + gridWidth + widthBetweenBoards, 595))
   
class Next(object):
  def __init__(self, data,state):
    self.surface = createNext(data)
    self.nextText = nextText(data)
    self.state = state
    self.allBlocksSurfaces = createNextBlocks(data)
  def drawNext(self,data):
    if data.mode == "marathon" and data.marathon.drewBackround == True:
        self.drawBlock(data)
        return True
    currentSurface = self.surface
    rect = currentSurface.get_rect()     
    x0 = margin   
    if self.state == 'right':
      x0 += gridWidth + widthBetweenBoards 
    if self.state == 'marathon':
      x0 += gridWidth + 25  
    rect.move_ip(x0 + gridWidth + 28, 160)
    canvas.blit(currentSurface, rect)

    self.drawBlock(data)
    text, text2 = self.nextText
    rect = text.get_rect()
    rect2 = text2.get_rect()
    rect.midtop = (x0 + gridWidth + 61, 124)
    rect2.midtop = (x0 + gridWidth + 62, 124)
    canvas.blit(text, rect)
    canvas.blit(text2, rect2)
  def drawBlock(self, data):
    if self.state != "marathon":
      condtion = data.startScreenDone
    if self.state == "marathon":
      condtion = data.marathon.startScreenDone
    if condtion:
      if self.state == 'left':
        current = data.gamePieces[0]
      elif self.state == 'right':
        current = data.gamePieces2[0]
      elif self.state == 'marathon':
        current = data.marathon.pieces[0]
      index = data.tetrisPieces.index(current)#needed to set colors
      surface = self.allBlocksSurfaces[index]
      for row in range(len(current)):
        for col in range(len(current)):     
          if current[row][col]:
            currentSurface = surface
            rect = currentSurface.get_rect()     
            x0, y0 = margin + gridWidth + 40, 180  
            if current == iPiece: 
              x0 -= 8
              y0 -= 10
            if current == oPiece: 
              x0 += 8
            if self.state == 'right':
              x0 += gridWidth + widthBetweenBoards  
            elif self.state == 'marathon':
              x0 += gridWidth + 25
            rect.move_ip(x0+((col)*15), y0 + ((row)*15))
            canvas.blit(currentSurface,rect)

class Hold(object):
  def __init__(self, state, data):
    self.state = state
    self.surface = createNext(data)
    self.holdText = holdText(data)
    self.allBlocksSurfaces = createNextBlocks(data)
  def hold(self, data):
    if self.state == 'left':
      if data.holdCount == 0: 
        data.holdCount +=1
        if data.holdPiece == 0:#this is the first move, nothing in the hold
            data.holdPiece = data.fallingPiece.piece
            data.fallingPiece.newFallingPiece(data)
        else:  #swap it out
            copyHoldPiece = data.holdPiece
            copyFallingPiece = data.fallingPiece.piece#make copies to swap
            data.holdPiece = copyFallingPiece
            data.fallingPiece.piece = copyHoldPiece
            for i in range(4): #change the orintation back to original form
                data.fallingPiece.piece = flipMatrix(rotateMatrix(data.fallingPiece.piece)) 
                if data.fallingPiece.piece in data.tetrisPieces: 
                    break
            piece = copyHoldPiece
            for i in range(4): #change the orintation back to original for
                piece = flipMatrix(rotateMatrix(piece))
                if piece in data.tetrisPieces: break
            current = data.tetrisPieces.index(piece)
            data.fallingPiece.surface = data.fallingPiece.allBlocksSurfaces[current]
            data.fallingPiece.color = data.tetrisPieceColors[current]
            data.fallingPiece.row = 0
            if len(data.fallingPiece.piece)==4 :
                data.fallingPiece.row = -1
            data.fallingPiece.col = data.cols // 2 *0.75 -0.75
      else:  # you can't hold the same piece twice
          data.holdDenied = True
    elif self.state == 'right':
      if data.holdCount2 == 0: 
        data.holdCount2 +=1
        if data.holdPiece2 == 0:#this is the first move, nothing in the hold
            data.holdPiece2 = data.fallingPiece2.piece
            data.fallingPiece2.newFallingPiece(data)
        else:  #swap it out
            copyHoldPiece = data.holdPiece2
            copyFallingPiece = data.fallingPiece2.piece#make copies to swap
            data.holdPiece2 = copyFallingPiece
            data.fallingPiece2.piece = copyHoldPiece
            for i in range(4): #change the orintation back to original form
                data.fallingPiece2.piece = flipMatrix(rotateMatrix(data.fallingPiece2.piece)) 
                if data.fallingPiece2.piece in data.tetrisPieces: 
                    break
            piece = copyHoldPiece
            for i in range(4): #change the orintation back to original for
                piece = flipMatrix(rotateMatrix(piece))
                if piece in data.tetrisPieces: break
            current = data.tetrisPieces.index(piece)
            data.fallingPiece2.surface = data.fallingPiece.allBlocksSurfaces[current]
            data.fallingPiece2.color = data.tetrisPieceColors[current]

            data.fallingPiece2.row = 0
            if len(data.fallingPiece2.piece)==4 :
                data.fallingPiece2.row = -1
            data.fallingPiece2.col = data.cols // 2 *0.75 -0.75
      else:  # you can't hold the same piece twice
          data.holdDenied2 = True
    elif self.state == 'marathon':
      if data.marathon.holdCount == 0: 
        data.marathon.holdCount +=1
        if data.marathon.holdPiece == 0:#this is the first move, nothing in the hold
            data.marathon.holdPiece = data.marathon.fallingPiece.piece
            data.marathon.fallingPiece.newFallingPiece(data)
        else:  #swap it out
            copyHoldPiece = data.marathon.holdPiece
            copyFallingPiece = data.marathon.fallingPiece.piece#make copies to swap
            data.marathon.holdPiece = copyFallingPiece
            data.marathon.fallingPiece.piece = copyHoldPiece
            for i in range(4): #change the orintation back to original form
              data.marathon.fallingPiece.piece = flipMatrix(rotateMatrix(data.marathon.fallingPiece.piece)) 
              if data.marathon.fallingPiece.piece in data.tetrisPieces: 
                break
            piece = copyHoldPiece
            for i in range(4): #change the orintation back to original for
                piece = flipMatrix(rotateMatrix(piece))
                if piece in data.tetrisPieces: break
            current = data.tetrisPieces.index(piece)
            data.marathon.fallingPiece.surface = data.fallingPiece.allBlocksSurfaces[current]
            data.marathon.fallingPiece.color = data.tetrisPieceColors[current]

            data.marathon.fallingPiece.row = 0
            if len(data.marathon.fallingPiece.piece)==4 :
                data.marathon.fallingPiece.row = -1
            data.marathon.fallingPiece.col = data.cols // 2 *0.75 -0.75
      else:  # you can't hold the same piece twice
          data.marathon.holdDenied = True
  def drawHold(self, data):
    if data.mode == "marathon" and data.marathon.drewBackround == True:
        self.drawBlock(data)
        return True

    currentSurface = self.surface
    rect = currentSurface.get_rect()     
    x0 = 12  
    if self.state == 'right':
      x0 += gridWidth + widthBetweenBoards  
    if self.state == 'marathon':
      x0 += gridWidth
    rect.move_ip(x0, 178)
    canvas.blit(currentSurface, rect)
    self.drawBlock(data)
    text, text2 = self.holdText
    rect = text.get_rect()
    rect2 = text2.get_rect()
    rect.midtop = (50, 140)
    rect2.midtop = (51, 140)
    if self.state == 'right':
      rect.move_ip(gridWidth + widthBetweenBoards, 0)
      rect2.move_ip(gridWidth + widthBetweenBoards, 0)
    if self.state == 'marathon':
      rect.move_ip(gridWidth, 0)
      rect2.move_ip(gridWidth, 0)
    canvas.blit(text, rect)
    canvas.blit(text2, rect2)
  def drawBlock(self, data):
    if self.state != "marathon":
      condtion = data.startScreenDone
    if self.state == "marathon":
      condtion = data.marathon.startScreenDone
    if condtion:
      if self.state == 'left':
        current = data.holdPiece
        
      elif self.state == 'right':
        current = data.holdPiece2
      elif self.state == 'marathon':
        current = data.marathon.holdPiece
      if type(current) != int:
        for i in range(4): #change the orintation back to original form
          current = flipMatrix(rotateMatrix(current)) 
          if current in data.tetrisPieces: 
              break 
      if current != 0:
        index = data.tetrisPieces.index(current)#needed to set colors
        surface = self.allBlocksSurfaces[index]
        for row in range(len(current)):
          for col in range(len(current)):     
            if current[row][col]:
              currentSurface = surface
              rect = currentSurface.get_rect()     
              x0, y0 = 24, 200  
              if current == iPiece: 
                x0 -= 8
                y0 -= 10
              if current == oPiece: 
                x0 += 8
              if self.state == 'right':
                x0 += gridWidth + widthBetweenBoards  
              if self.state == 'marathon':
                x0 += gridWidth  
              rect.move_ip(x0+((col)*15), 
                                y0 + ((row)*15))
              canvas.blit(currentSurface,rect)

class button(object):
  def __init__(self, type, y, text):
    if type == "blue":
      self.surface, self.surface2 = createBlueButton( text)
      self.rect = self.surface.get_rect()
      self.rect2 = self.surface2.get_rect()
      self.rect.move_ip(width/2 - 115,y)
      self.rect2.move_ip(width/2 - 115,y)
    if type == "home":
      self.surface, self.surface2 = createHomeButton()
      self.rect = self.surface.get_rect()
      self.rect2 = self.surface2.get_rect()
  def draw(self,pos):
    canvas.blit(self.surface, self.rect)
    if self.rect.collidepoint(pygame.mouse.get_pos()):
      canvas.blit(self.surface2, self.rect2)
      return True
    return False
      
class GhostPiece(object):
  def __init__(self, state, data):
    self.state = state
    if state == "left":
      self.piece = data.fallingPiece
    elif state == "right": 
      self.piece = data.fallingPiece2
    elif state == "marathon": 
      self.piece = data.marathon.fallingPiece
    self.row = self.piece.row
    self.col = self.piece.col
    self.surface = createGhost(data)
  def ghostPieceIsLegal(self, data, piece):
    if self.state == "left"  :
      return data.board.pieceIsLegal(self.piece, self.row, self.col,data)
    elif self.state == "right"  :
      return data.board2.pieceIsLegal(self.piece, self.row, self.col,data)
    elif self.state == "marathon"  :
      return data.marathon.board.pieceIsLegal(self.piece, self.row, self.col,data)
  def moveGhostFallingPiece(self, data, drow, dcol):
      self.row += drow
      self.col+= dcol
      if self.ghostPieceIsLegal(data,self) == False:     
          self.row -= drow
          self.col -= dcol
          return False
      return True
  def drawGhost(self, data):
    if self.state == "left":
      self.piece = data.fallingPiece
    elif self.state == "right": 
      self.piece = data.fallingPiece2
    elif self.state == "marathon": 
      self.piece = data.marathon.fallingPiece
    self.row = self.piece.row
    if self.state == "marathon": 
      condition1 = data.marathon.startScreenDone
      condition2 = data.marathon.gameOver
      
    else:
      condition1 = data.startScreenDone
      condition2 = data.gameOver
    if (condition1 and not condition2):
      while self.moveGhostFallingPiece(data,1,0) == True: 
        pass    
      self.col = self.piece.col    
      for row in range(len(self.piece.piece)):
        for col in range(len(self.piece.piece[0])):
          if self.piece.piece[row][col]: 
            currentSurface = self.surface
            rect = currentSurface.get_rect()     
            x0, y0 = margin, lengthBetweenTopAndStartOfBoard   
            if self.state == 'right':
              x0 += gridWidth + widthBetweenBoards 
            if self.state == "marathon":
              x0 += width/2 - gridWidth 
            rect.move_ip(x0 + ((self.col + col)*20), y0 + ((self.row+row)*20))
            canvas.blit(currentSurface, rect)            
###########################################
#           initialize data
###########################################
def init(data):
  #General atriubutes
  data.rows, data.cols = 21, 10
  data.width, data.height = width, height
  #board atriubutes
  data.emptyColor = ((36, 36, 36), (41, 41, 41)) #rgb
  data.backroundColor = (127, 127, 127)
  data.board, data.board2 = Board(data, 'left'), Board(data, 'right')
  data.backroundSurface = createBackroundSurface(data, "multiplayer")
  data.linesSurfaces = createLinesSurface(data)
  # pieces
  data.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
  data.tetrisPieceColors = [(0, 162, 224), (58, 95, 205), (238, 118, 0),
                            (255, 185, 15), (50, 205, 50), 
                            (205, 96, 144), (220, 20, 60) 
                            ] 
  data.borderColors = [(24, 116, 205), (0, 0, 139), (139, 54, 38),
                       (139, 101, 8), (0, 139, 0),(104, 34, 139), (139, 37, 0) 
                       ]
  data.createBlocks = createBlocks(data)
  data.gamePieces, data.gamePieces2 = generatePieces(data), generatePieces(data)
  data.marathon = Marathon(data)
  data.fallingPiece, data.fallingPiece2 = Piece('left',data),Piece('right',data)
  data.fallingPiece.newFallingPiece(data)
  data.fallingPiece2.newFallingPiece(data)
  data.dirtBlock = createDirt()
  #button states
  data.pressedLeft, data.pressedRight, data.pressedDown = False, False, False
  data.pressedA, data.pressedS, data.pressedD = False, False, False
  data.initialMoveRight, data.initialMoveLeft = False, False
  #move block delays
  data.timerCountToMove, data.timerCountToMoveLeft = 0, 0
  data.timerToMoveDownEventLeft, data.timerToMoveDownEvent = 0, 0
  #automatic delays
  data.countToGoDownOneTile, data.countToGoDownOneTile2 = 0, 0
  data.delayToPlace, data.delayToPlace2 = False, False
  data.delayToPlaceCount, data.delayToPlaceCount2 = 0, 0
  #game states
  data.gameOver, data.player1Win, data.player2Win = False, False, False
  data.paused, data.startScreenDone = False, False
  data.startScreenText = Text(data)
  data.drewHelp, data.drawTie = False, False
  data.beforeHelpMode = "home"
  data.linesCleared, data.linesCleared2 = 0, 0
  data.sendLines, data.sendLines2, data.timeElapsedInMultiplayer = 0, 0, 0
  data.drewHome, data.drewMultiplayer, data.drewHelp = False, False, False
  #define next and hold
  data.next, data.next2 = Next(data, 'left'), Next(data, 'right')
  data.holdDenied, data.holdDenied2 = False, False
  data.holdPiece ,  data.holdCount,  data.holdAvailableCount = 0, 0, 0
  data.holdDeniedCount, data.holdDeniedCount2 = 0,  0,
  data.holdPiece2 ,  data.holdCount2,  data.holdAvailableCount2 = 0,  0,  0  
  data.hold1, data.hold2 = Hold('left',data), Hold('right',data)
  # text 
  data.text = Text(data)
  data.holdDeniedText = createText("X", (255,0,0),(255,0,0),20)
  #buttons 
  data.NewBattlebutton = button("blue",190,"Start New battle")
  data.resumeBattlebutton = button("blue", 280, "   resume battle")
  data.homeButton = button("home",0, None)
  data.helpButton = button("blue", 550, "           help")
  data.playMarathon = button("blue", 370, "   Play Marathon")
  data.resumeMarathon =  button("blue", 460, "Resume Marathon")
  #ghostPiece 
  data.ghostPiece = GhostPiece("left", data)
  data.ghostPiece2 = GhostPiece("right", data)
###########################################
#             MULTIPLAYER! 
###########################################
def moveBlockEvent(data, state, button, piece, drow, dcol, cooldown, mod):  
  if state == 'right':
    initialMove = data.initialMoveRight
  elif state == 'left': 
    initialMove = data.initialMoveLeft
  if not initialMove:
    piece.moveFallingPiece(data, drow, dcol)
    if state == 'right':
      data.initialMoveRight = True
    if state == 'left':
      data.initialMoveLeft = True
  if state == 'right':
    if button == "down":
      data.timerToMoveDownEvent += 1
      count = data.timerToMoveDownEvent
    else:
      data.timerCountToMove  += 1
      count = data.timerCountToMove
    if count > cooldown and count  % mod == 0 :

      data.fallingPiece2.moveFallingPiece(data, drow, dcol)
  elif state == 'left':
    if button == "down":
      data.timerToMoveDownEventLeft += 1
      count = data.timerToMoveDownEventLeft
    else:
      data.timerCountToMoveLeft  += 1
      count = data.timerCountToMoveLeft
    if count > cooldown and count  % mod == 0 :
      data.fallingPiece.moveFallingPiece(data, drow, dcol)
def holdDeniedDelay(data):
  if data.holdDenied:
      data.holdDeniedCount += 1
  if data.holdDeniedCount == 50:
      data.holdDenied = False
      data.holdDeniedCount = 0
  if data.holdDenied2:
      data.holdDeniedCount2 += 1
  if data.holdDeniedCount2 == 50:
      data.holdDenied2 = False
      data.holdDeniedCount2 = 0
def delayToPlace(data):
  if data.delayToPlace:
    data.delayToPlaceCount += 1
    if data.delayToPlaceCount == 40:
      if data.fallingPiece.moveFallingPiece(data, 1, 0) == False:
        data.board.placeFallingPiece(data, data.fallingPiece)
        if data.sendLines2 > 0:
            data.board2.sendLines(data, data.sendLines2)
            data.sendLines2 = 0
        data.fallingPiece.newFallingPiece(data) 
        data.countToGoDownOneTile = 0
        data.delayToPlace = False
        if data.board.pieceIsLegal(data.fallingPiece, data.fallingPiece.row, 
                                   data.fallingPiece.col, data ) == False:
          data.gameOver = True
          data.player2Win = True
          data.fallingPiece.piece = [data.fallingPiece.piece[1]]
          data.fallingPiece.row = 0
      data.delayToPlaceCount = 0
      data.countToGoDownOneTile = 0
  if data.delayToPlace2:
    data.delayToPlaceCount2 += 1
    if data.delayToPlaceCount2 == 40:
      if data.fallingPiece2.moveFallingPiece(data, 1, 0) == False:
        data.board2.placeFallingPiece(data, data.fallingPiece2) 
        if data.sendLines > 0:
            data.board.sendLines(data, data.sendLines)
            data.sendLines = 0
        data.fallingPiece2.newFallingPiece(data)
        data.countToGoDownOneTile2 = 0
        data.delayToPlace2 = False
      if data.board2.pieceIsLegal(data.fallingPiece2, data.fallingPiece2.row, 
                                  data.fallingPiece2.col, data) == False:
        data.gameOver = True
        data.player1Win = True
        data.fallingPiece2.piece = [data.fallingPiece2.piece[1]]
        data.fallingPiece2.row = 0
      data.delayToPlaceCount2 = 0
      data.countToGoDownOneTile2 = 0
def moveDownDelay(data):
  #every 100 timerFired calls move the block down 1
  data.countToGoDownOneTile += 1
  data.countToGoDownOneTile2 += 1
  if data.countToGoDownOneTile == 100:
    data.delayToPlace = not data.fallingPiece.moveFallingPiece(data,1,0)  
    data.countToGoDownOneTile = 0
  if data.countToGoDownOneTile2 == 100 :  
    data.delayToPlace2 = not data.fallingPiece2.moveFallingPiece(data,1,0)  
    data.countToGoDownOneTile2 = 0                
  delayToPlace(data)
def multiplayerTimerFired(data):
  holdDeniedDelay(data)
  if not data.gameOver and not data.paused and data.startScreenDone:
    moveDownDelay(data)
    if data.pressedRight and not data.pressedLeft:
      moveBlockEvent(data, 'right', "right", data.fallingPiece2, 0 ,1, 20, 6)
    if data.pressedLeft and not data.pressedRight:
      moveBlockEvent(data, 'right', "left", data.fallingPiece2, 0 ,-1, 20, 6)
    if data.pressedDown :
      moveBlockEvent(data, 'right', "down", data.fallingPiece2, 1, 0, 0, 10)
    if data.pressedD and not data.pressedA:
      moveBlockEvent(data, 'left', "right", data.fallingPiece, 0 ,1, 20, 6)
    if data.pressedA and not data.pressedD:
      moveBlockEvent(data, 'left', "left", data.fallingPiece, 0 ,-1, 20, 6)
    if data.pressedS :
      moveBlockEvent(data, 'left', "down", data.fallingPiece, 1, 0, 0, 10)
def multiplayerMousePressed(data, event): pass
  #event is a tuple (x ,y)
def handleMoveKeyEvents(data, condition, key, state):
  if condition:
    if state == "right":
      if key == "left": data.pressedLeft = True
      if key == "right": data.pressedRight = True
      if key == "down": data.pressedDown = True
      data.initialMoveRight = False
      data.timerCountToMove = 0
    elif state == "left":
      if key == "a": data.pressedA = True
      if key == "s": data.pressedS = True
      if key == "d": data.pressedD = True
      data.initialMoveLeft = False
      data.timerCountToMoveLeft  = 0
def multiplayerKeyPressed(data, event):
  if event.type == pygame.KEYDOWN: 
    if event.key == pygame.K_r:  
      restartMarathon(data)
    if event.key == pygame.K_p and data.startScreenDone:  
      data.paused = not(data.paused)
  if data.startScreenDone and not data.gameOver and not data.paused:
    if event.type == pygame.KEYDOWN:          
      if event.key == pygame.K_TAB:       
        data.hold1.hold(data)
      if event.key == pygame.K_n:       
        data.hold2.hold(data)
      if event.key == pygame.K_UP:        
        data.fallingPiece2.rotateFallingPiece(data)
      if event.key == pygame.K_w:        
        data.fallingPiece.rotateFallingPiece(data)
      handleMoveKeyEvents(data, event.key == pygame.K_RIGHT, "right", "right")
      handleMoveKeyEvents(data, event.key == pygame.K_LEFT, "left", "right")
      handleMoveKeyEvents(data, event.key == pygame.K_DOWN, "down", "right")
      handleMoveKeyEvents(data, event.key == pygame.K_a,"a",  "left")
      handleMoveKeyEvents(data, event.key == pygame.K_s, "s", "left")
      handleMoveKeyEvents(data, event.key == pygame.K_d, "d", "left",)
      if event.key == pygame.K_SPACE:       
        while data.fallingPiece2.moveFallingPiece(data,1,0) == True:
          data.fallingPiece2.moveFallingPiece(data,1,0)  
        data.board2.placeFallingPiece(data,data.fallingPiece2)
        if data.sendLines > 0:
          data.board.sendLines(data, data.sendLines)
          data.sendLines = 0
        data.fallingPiece2.newFallingPiece(data)
        data.countToGoDownOneTile2 = 0
      if event.key == pygame.K_LSHIFT  :       
        while data.fallingPiece.moveFallingPiece(data,1,0) == True:
          data.fallingPiece.moveFallingPiece(data,1,0)  
        data.board.placeFallingPiece(data,data.fallingPiece)
        if data.sendLines2 > 0:
          data.board2.sendLines(data, data.sendLines2)
          data.sendLines2 = 0
        data.fallingPiece.newFallingPiece(data)
        data.countToGoDownOneTile = 0    
    elif event.type == pygame.KEYUP: 
      if event.key == pygame.K_LEFT:        
        data.pressedLeft = False
      if event.key == pygame.K_RIGHT:      
        data.pressedRight = False 
      if event.key == pygame.K_DOWN:     
        data.pressedDown = False
      if event.key == pygame.K_a:        
        data.pressedA = False
      if event.key == pygame.K_d:      
        data.pressedD = False
      if event.key == pygame.K_s:     
        data.pressedS = False
def drawLines(data): 
  rect1 = data.linesSurfaces[0].get_rect()
  rect2= data.linesSurfaces[1].get_rect()
  rect1.move_ip((margin ,lengthBetweenTopAndStartOfBoard - 26))
  rect2.move_ip((margin + gridWidth + widthBetweenBoards, 
                 lengthBetweenTopAndStartOfBoard-26))
  canvas.blit(data.linesSurfaces[0], rect1)
  canvas.blit(data.linesSurfaces[1], rect2)
def multiplayerRedrawAll(data):
  data.timeElapsedInMultiplayer += data.timeSinceLastFrame
  canvas.blit(data.backroundSurface, data.backroundSurface.get_rect())
  data.board.drawBoard(data)
  data.board2.drawBoard(data)
  data.ghostPiece.drawGhost(data)
  data.ghostPiece2.drawGhost(data)
  if data.startScreenDone:
    data.fallingPiece.drawFallingPiece(data)
    data.fallingPiece2.drawFallingPiece(data)
  drawLines(data)
  data.startScreenText.drawStartScreen(data)
  data.next.drawNext(data)
  data.next2.drawNext(data)
  if data.gameOver:
    data.text.drawGameOver(data, None)
  if data.paused:
    data.text.drawPaused(None)
  data.hold1.drawHold(data)
  data.hold2.drawHold(data)
  if data.holdDenied :
    canvas.blit(data.holdDeniedText[0], (82, 172))
  if data.holdDenied2 :
    canvas.blit(data.holdDeniedText[0], (507, 172))
  data.homeButton.draw(pygame.mouse.get_pos())
  data.text.drawTime(data)
  data.text.drawSentLines(data)
  pygame.display.update()
###########################################
#                  Home 
###########################################  
def restartMarathon(data):
  copyOfMarathon = data.marathon 
  copyOfMarathonPiece = data.marathon.fallingPiece
  init(data)
  data.marathon = copyOfMarathon
  data.marathon.fallingPiece = copyOfMarathonPiece  
def homeMousePressed(data, event):
  if data.NewBattlebutton.draw(pygame.mouse.get_pos()):
    restartMarathon(data)
    data.mode = 'multiplayer'
  if data.resumeBattlebutton.draw(pygame.mouse.get_pos()):
    data.mode = 'multiplayer'
    data.drewMultiplayer = False
  if data.helpButton.draw(pygame.mouse.get_pos()):
    data.mode = "help"
    data.beforeHelpMode = "home"
    data.drewHelp = False
  if data.playMarathon.draw(pygame.mouse.get_pos()):
    data.mode = "marathon"
    data.marathon.__init__(data)
    data.marathon.initMarathon(data)
  if data.resumeMarathon.draw(pygame.mouse.get_pos()):
    data.mode = "marathon"
    if data.marathon.fallingPiece.piece == 0:
      data.marathon.initMarathon(data)
    data.marathon.drewBackround = False 
def homeRedrawAll( data):
  if data.drewHome == False:
    canvas.blit(data.startSurface, data.startSurface.get_rect())
    data.drewHome = True
    pygame.display.update()
  else:
    data.NewBattlebutton.draw(pygame.mouse.get_pos())
    data.resumeBattlebutton.draw(pygame.mouse.get_pos())
    data.helpButton.draw(pygame.mouse.get_pos())
    data.playMarathon.draw(pygame.mouse.get_pos())
    data.resumeMarathon.draw(pygame.mouse.get_pos())
    pygame.display.update() 
###########################################
#                 Help Mode!
###########################################
def helpRedrawAll(data):
  if not data.drewHelp:
    canvas.fill((250, 250, 250))
    img = pygame.image.load("Help.png")
    canvas.blit(img,(0, 0))
    data.homeButton.draw(pygame.mouse.get_pos())
    pygame.display.update()
    data.drewHelp = True
  else:
    data.homeButton.draw(pygame.mouse.get_pos())
    pygame.display.update()
###########################################
#              Marathon Class!
###########################################
class Marathon(object):
  def __init__(self, data):
    self.backroundSurface = createBackroundSurface(data, "marathon")
    self.board = Board(data, "marathon")
    self.board.rect.move_ip(width/2 - 0.5*gridWidth,
                            lengthBetweenTopAndStartOfBoard)
    self.gameOver, self.delayToPlace, self.paused = False, False, False
    self.fallingPiece,self.pieces = Piece("marathon", data),generatePieces(data)
    self.pressedLeft, self.pressedRight, self.pressedDown = False, False, False
    self.initialMove, self.timerCountToMove = False, 0
    self.timerToMoveDownEvent, self.countToGoDownOneTile = 0, 0
    self.delayToPlaceCount, self.level, self.points, self.holdCount = 0, 0, 0, 0
    self.moveDownDelayValue, self.countTillLevelUp = 91, 25 
    self.startScreenCount, self.holdCount, self.holdPiece = 3, 0, 0
    self.startScreenDone, self.holdDenied = False, False
    self.single, self.double, self.triple = False, False, False
    self.doubleTetris, self.tetris, self.drewBackround = False, False, False
    self.messageCount = 0
    self.singleText = createText("Single!", (255, 255, 255), (0, 238, 238), 30)
    self.doubleText = createText("Double!", (255, 255, 255), (255, 165, 0), 30)
    self.tripleText = createText("Triple!", (255, 255, 255), (0, 255, 0), 30)
    self.tetrisText = createText("GG Tetris!", (255, 255, 255), (255, 100, 103),
                                 30)
    self.doubleTetrisText = createText("GG Double Tetris!", (255, 255, 255), 
                                       (0, 255, 0), 30)
    self.scoreText = createText("Score: ", (0, 0, 0), (255, 255, 255), 30)
    self.levelText = createText("Level: ", (0, 0, 0), (255, 255, 255), 30)
  def initMarathon(self, data):
    self.fallingPiece.newFallingPiece(data)
    self.ghost = GhostPiece("marathon", data)
    self.next = Next(data, "marathon")
    self.hold = Hold("marathon", data)
  def moveBlockEvent(self, data, button, drow, dcol, cooldown, mod):    
    if not self.initialMove:
      self.fallingPiece.moveFallingPiece(data, drow, dcol)
      self.initialMove = True
    if button == "down":
      self.timerToMoveDownEvent += 1
      count = self.timerToMoveDownEvent
    else:
      self.timerCountToMove  += 1
      count = self.timerCountToMove
    if count > cooldown and count % mod == 0 :
      self.fallingPiece.moveFallingPiece(data, drow, dcol)
  def placeDelay(self, data):
    if self.delayToPlace:
      self.delayToPlaceCount += 1
      if self.delayToPlaceCount == 40:
        if self.fallingPiece.moveFallingPiece(data, 1, 0) == False:
          self.board.placeFallingPiece(data, self.fallingPiece)
          self.drewBackround = False
          self.fallingPiece.newFallingPiece(data)
          self.countToGoDownOneTile = 0
          self.delayToPlace = False
          if not self.board.pieceIsLegal(self.fallingPiece, 
                            self.fallingPiece.row, self.fallingPiece.col, data):
            self.gameOver = True
            self.fallingPiece.piece = [self.fallingPiece.piece[1]]
            self.fallingPiece.row = 0
        self.delayToPlaceCount = 0
        self.countToGoDownOneTile = 0
  def moveDownDelay(self, data, x):
    #every x secnds move the block down 1
    self.countToGoDownOneTile += 1
    if self.countToGoDownOneTile >= x:
      self.delayToPlace = not self.fallingPiece.moveFallingPiece(data, 1, 0)
      self.countToGoDownOneTile = 0               
    self.placeDelay(data)
  def delayForMesage(self, condition):
    #handles the delay for the pop up message to be when scoring points
    if condition:
      self.messageCount += 1
      if self.messageCount >= 60:
        self.single = False
        self.double = False
        self.triple = False
        self.doubleTetris = False
        self.tetris = False
        self.messageCount = 0
        self.drewBackround = False 
  def timerFired(self,data): 
    self.delayForMesage(self.single)
    self.delayForMesage(self.double)
    self.delayForMesage(self.triple)
    self.delayForMesage(self.doubleTetris)
    self.delayForMesage(self.tetris)
    if not self.paused and not self.gameOver and self.startScreenDone:
      if self.countTillLevelUp <= 0:
        self.countTillLevelUp = 25
        if self.level < 14:
          self.moveDownDelayValue -= 6
          self.level += 1
          self.drewBackround = False
    if not self.gameOver and not self.paused and self.startScreenDone:
      self.moveDownDelay(data, self.moveDownDelayValue)
      if self.pressedRight and not self.pressedLeft:
        self.moveBlockEvent(data, "right", 0 ,1, 20, 6)
      if self.pressedLeft and not self.pressedRight:
        self.moveBlockEvent(data, "left", 0 ,-1, 20, 6)
      if self.pressedDown:
        self.moveBlockEvent(data, "down", 1, 0, 0, 10)
  def handleMoveKeyEvents(self, data, condition, key):
    if condition:
      if key == "left": self.pressedLeft = True
      if key == "right": self.pressedRight = True
      if key == "down": self.pressedDown = True
      self.initialMove = False
      self.timerCountToMove  = 0  
  def keyPressed(self, data, event):
    if event.type == pygame.KEYDOWN: 
      if event.key == pygame.K_p and not self.gameOver and self.startScreenDone:  
        self.paused = not(self.paused)
        if self.paused == False:  
          self.drewBackround = False #need to redraw the backround
          pygame.display.update()
      if event.key == pygame.K_r:  
        self.__init__(data)
        self.initMarathon(data)
    if not self.gameOver and not self.paused and self.startScreenDone:
      if event.type == pygame.KEYDOWN:    
        self.handleMoveKeyEvents(data, event.key == pygame.K_RIGHT, "right")
        self.handleMoveKeyEvents(data, event.key == pygame.K_LEFT, "left")
        self.handleMoveKeyEvents(data, event.key == pygame.K_DOWN, "down")
        if event.key == pygame.K_c or event.key == pygame.K_LSHIFT:     
          self.hold.hold(data)
          self.drewBackround = False
        if event.key == pygame.K_UP:        
          self.fallingPiece.rotateFallingPiece(data)
        if event.key == pygame.K_SPACE:        
          while self.fallingPiece.moveFallingPiece(data,1,0) == True:
            self.fallingPiece.moveFallingPiece(data,1,0)  
          self.board.placeFallingPiece(data, self.fallingPiece)
          self.drewBackround = False
          self.fallingPiece.newFallingPiece(data)
          self.countToGoDownOneTile = 0
      elif event.type == pygame.KEYUP: 
        if event.key == pygame.K_LEFT:        
          self.pressedLeft = False
        if event.key == pygame.K_RIGHT:      
          self.pressedRight = False 
        if event.key == pygame.K_DOWN:     
          self.pressedDown = False
  def drawLines(self, data): 
    rect1 = data.linesSurfaces[0].get_rect()
    rect1.move_ip((width/2 - 0.5*gridWidth, lengthBetweenTopAndStartOfBoard-26))
    canvas.blit(data.linesSurfaces[0], rect1)
  def displayText(self, conditionToDisplay, textSurface, rect1, rect2):
    #functions that displays text if the conditionToDiplay is True
    if conditionToDisplay:
      canvas.blit(textSurface[0], rect1)
      canvas.blit(textSurface[1], rect2)
  def drawScore(self, data):
    #display the text if points are scored of how many lines cleared
    self.displayText(self.single, self.singleText, 
                     (width/2 - 280, width - 425), (width/2 - 279, width - 425))
    self.displayText(self.double, self.doubleText, 
                     (width/2 - 280, width -425), (width/2 - 279, width - 425))
    self.displayText(self.triple, self.tripleText, 
                     (width/2 - 280, width - 425), (width/2 - 279, width - 425))
    self.displayText(self.tetris, self.tetrisText, 
                     (width/2 - 280, width - 425), (width/2 - 279, width - 425))
    self.displayText(self.doubleTetris, self.doubleTetrisText, 
                     (width/2 - 360, width - 425), (width/2 - 359,width - 425))
    if not self.drewBackround: 
      self.drewBackround = True
      canvas.blit(self.scoreText[1], (width/2-330, width-350))
      canvas.blit(self.levelText[1], (width/2-310, width-300))
    text = createText2(str(self.points), (0, 0, 0), (255, 255, 255), 
                       30, (23, 49 ,100))
    canvas.blit(text[1], (width/2 - 220, width - 350))
    text2 = createText(str(self.level) + "  ", (0, 0, 0), (255, 255, 255), 30)
    canvas.blit(text2[1], (width/2 - 190, width - 300))
  def redrawAll(self, data):
    if self.paused == False and not self.gameOver and self.startScreenDone:
      self.countTillLevelUp -= data.timeSinceLastFrame
    if self.paused == False and not self.gameOver and not self.startScreenDone:
      self.startScreenCount -= data.timeSinceLastFrame
    if not self.drewBackround:
      canvas.blit(self.backroundSurface, (0,0))
    self.board.drawBoard(data)
    self.ghost.drawGhost(data)
    if self.startScreenDone:
      self.fallingPiece.drawFallingPiece(data)
    self.drawLines(data)
    if self.paused:
      data.text.drawPaused("marathon")
    if self.gameOver:
      data.text.drawGameOver(data, "marathon")
    self.next.drawNext(data)
    self.hold.drawHold(data)
    self.drawScore(data)
    data.homeButton.draw(pygame.mouse.get_pos())
    if not self.startScreenDone:
      data.text.drawMarathonStart(data)
    pygame.display.update()
################################################################################
#                                Main Functions                                #
################################################################################
def changeHelp(data):
  if data.mode != "help":    #turn to help
    data.beforeHelpMode = data.mode
    data.mode = "help"
  elif data.mode == "help":   #turn to before help
    data.mode = data.beforeHelpMode
    data.marathon.drewBackround = False
    data.drewHome = False
    data.drewHelp = False
def timerFired(data): 
  if data.mode == "multiplayer":
    multiplayerTimerFired(data)
  elif data.mode == "marathon": 
    data.marathon.timerFired(data)

def mousePressed(data, event):
  if data.mode != "home" and data.homeButton.draw(pygame.mouse.get_pos()):
    data.mode = 'home'
    data.drewHome = False
  if data.mode == "home":
    homeMousePressed(data, event)
  elif data.mode == "multiplayer":
   multiplayerMousePressed(data,event)

def keyPressed(data,event):
  if data.mode == "multiplayer": 
    multiplayerKeyPressed(data,event)
  elif data.mode == "marathon": 
    data.marathon.keyPressed(data, event)
  if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_h:     
      changeHelp(data)

def redrawAll( data):
  if data.mode == "help" or data.mode == "home":
    data.maxFPS = 5000
  else:
    data.maxFPS = 64
  if data.mode == "home": 
    homeRedrawAll(data)
  elif data.mode == "multiplayer":
    multiplayerRedrawAll(data)
  elif data.mode == "help": 
    helpRedrawAll(data)
  elif data.mode == "marathon": 
    data.marathon.redrawAll(data)
###########################################
#                  run
###########################################
def Quit():
  print("bye")
  pygame.display.quit()
  pygame.quit()
  sys.exit(0) 

def run(width=300, height=300):
  pygame.display.set_caption("Tetris")
  #Set up data and call init
  class Struct(object): pass
  data = Struct()
  init(data)
  data.mode = "home" #defualt mode is the home screen
  pygame.init() #initiate pygame
  #data.sound = pygame.mixer.Sound("/Users/BrandonLi/Desktop/fullsizeoutput_49d.wav")
  data.timeSinceLastFrame = 0
  data.clock = pygame.time.Clock()
  data.timeElapsedInMultiplayer = 0
  pygame.key.set_repeat()
  createStart(data)
  data.maxFPS = 64
  while True: #game loop
    timerFired(data)
    # print(data.clock.get_fps())
    for event in pygame.event.get():
      if event.type == pygame.QUIT: 
        Quit()         
      if event.type == pygame.MOUSEBUTTONDOWN:    
        (x, y) = pygame.mouse.get_pos()
        mousePressed(data, (x, y))      
                   
      keyPressed(data,event) #handle key down or key up in key pressed
    timerFired(data)
    redrawAll(data)
    data.timeSinceLastFrame = (data.clock.tick(data.maxFPS)/1000) #seconds 
###########################################
#             define pieces
###########################################
iPiece = [
  [False, False, False, False],
  [True, True, True, True], 
  [False, False, False, False], 
  [False, False, False, False]
  ]
jPiece = [
  [True, False, False], 
  [True,  True, True],
  [False, False, False]
  ]
lPiece = [
  [False, False, True],
  [True, True, True],
  [False, False, False]
  ]
oPiece = [
  [True, True],
  [True, True]
  ]
sPiece = [
  [False, True, True],
  [True, True, False],
  [False, False, False]
  ]
tPiece = [
  [False, True, False],
  [True, True, True],
  [False, False, False]
  ]
zPiece = [
  [True, True, False],
  [False, True, True], 
  [False, False, False]
  ]
###########################################  
# set up global variables that will not get 
#     modified and can be accessed
###########################################
margin = 100 #margin around grid
lengthBetweenTopAndStartOfBoard = 125
rows = 21
cols = 10
gridWidth  = 200  #length of each board
gridHeight = 420  #height of each board
cellSize = 20
widthBetweenBoards = 225
width = 2*margin + 2*gridWidth + widthBetweenBoards 
height = 2*margin + gridHeight + 100 
canvas = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
  
run(width, height)