from os import system
from pynput import keyboard as kb
from PFObjects import Wall, Food
import Playfield as pf
import Players as pl


#THIS SCRIPT DEFINES THE KIND OF GAME BEING PLAYED, AND CONTROLS COLLISION.

class Game:

    def __init__(self, multiplayer=False, ai=True, p1Name="Player 1", p2Name="Player 2", hardMode=False, foodSpeed=6, pfSize=10, borderTP=False):
        
        self.won = False
        self.hardMode = hardMode
        """In hard mode, snakes move faster as they eat."""
        self.borderTP = borderTP
        """If True, snakes wrap around to the other side when reaching a border."""
        self.foodSpeed = foodSpeed
        """The speed at which food spawns, in seconds."""
        
        self.pf = pf.PlayField(pfSize)

        self.player1 = pl.Human("bobby")
        self.player2 = None

        self.lstnr = kb.Listener(on_press=self.Controls)
        """This game's keyboard listener."""

        gridChanges = {}

        #Keep this here
        midY = self.pf.gridSizeY//2

        #Create ai or 2nd player if multiplayer was chosen
        if multiplayer:
            if ai:
                self.player2 = pl.Bot(self.pf, p2Name)
            else:
                self.player2 = pl.Human(p2Name)
            
            #Move both snakes to opposite sides, giving them enough space to start with.
            quarter = self.pf.gridSizeX//4
            gridChanges.update(self.player1.snake.Move(pf.Location(quarter, midY)))
            gridChanges.update(self.player2.snake.Move(pf.Location(self.pf.gridSizeX - quarter, midY)))
            del quarter
        else:
            #If there is only one player, move the player's snake to the center of the playfield.
            gridChanges.update(self.player1.snake.Move(self.pf.center))

        #Create playField border
        border = Wall("Border")
        endX = self.pf.gridSizeX-1
        endY = self.pf.gridSizeY-1
        #Draw border wall
        gridChanges.update(border.Draw(pf.Location(endX, midY), pf.Location(endX, midY), [pf.Location(endX, 0), pf.Location(0, 0), pf.Location(0, endY), pf.Location(endX, endY)]))
        del endX, midY, endY

        #Add border nodes to playfield's changedNodes
        if borderTP == False:
            self.pf.changedNodes.extend(border.nodeLocations)

        self.pf.UpdateGrid(gridChanges)
        self.lstnr.start()

    def Controls(self, keyPressed):
        """Controls the snakes. This method is called when a key is pressed."""

        if keyPressed in self.player1.keys.values():
            self.player1.Control(keyPressed)

        if self.player2 != None:
            if keyPressed in self.player2.keys.values():
                self.player2.Control(keyPressed)

    def MoveSnakes(self):

        #Remove old snake locations from changedNodes
        clearAmount = self.player1.snake.length + (self.player2.snake.length if self.player2 != None else 0)
        self.pf.changedNodes = self.pf.changedNodes[:-clearAmount]

        #Move player 1's snake
        gridChanges = self.player1.snake.Move()
        self.pf.changedNodes.extend(self.player1.snake.body.nodeLocations)

        #Move player 2's snake if multiplayer
        if self.player2 != None:
            gridChanges.update(self.player2.snake.Move())
            self.pf.changedNodes.extend(self.player2.snake.body.nodeLocations)

        return gridChanges

    #TODO
    def CheckCollision(self):
        """Searches the playfield for any collisions.

        Returns:
            Bool: True if collision detected.
        """

        for loc in self.pf.changedNodes:
            if self.player1.snake.head.position == loc or (self.player2 != None and self.player2.snake.head.position == loc):
                return True

        pass
        
    def Play(self):
        """The main loop of the game."""

        system("cls")
        gridChanges = {}

        #Move snakes
        gridChanges.update(self.MoveSnakes())
        
        #Check for collision
        if self.CheckCollision():
            print("Collision detected!")
        #If a snake collided, end the game. The other player wins if multiplayer.

        self.pf.UpdateGrid(gridChanges)
        self.pf.PrintGrid()

    def RecordResults(self):
        #This method is intended to be called after the game is finished. Returns the time spent playing the game, and who won (if the game is multiplayer)

        pass

#For food
# def Spawn(self, location: pf.Location=None):
#         """Spawns the food on the Playfield. If the location is not specified, a random location is chosen instead.\n
#         Remember to check if the location is valid before using this!

#         Args:
#             location (pf.Location, optional): The location the food appears at. Defaults to None.

#         Returns:
#             Dict: Playfield grid changes (Location : String)
#         """

#         gridChanges = {}

#         if location == None:
#             self.Node.position = pf.PlayField.RandomLocation()
#         else:
#             self.node.position = location

#         return gridChanges