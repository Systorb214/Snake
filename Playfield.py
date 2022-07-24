import random


class Location:
    """
    Contains data representing a point on a grid.
    """
    def __init__(self, xValue, yValue):
        self.intCode = (xValue, yValue)
        self._x = xValue
        self._y = yValue
        """Tuple representation of the location. (X, Y)"""

    def __str__(self):
        return str(self.intCode)
        
    def __getitem__(self, item):
        return self.intCode[item]

    def __eq__(self, other):
        if type(other) == Location:
            return self.intCode == other.intCode

    #This must be used because the __eq__ method removes the default hash method.
    def __hash__(self):
        return hash(self.intCode)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self.intCode = (value, self.y)
        self.__hash__()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.intCode = (self.x, value)
        self.__hash__()

class Node:
    """
    Nodes are the locations on the self.
    """

    def __init__(self, type=" ", position=Location(1, 1)):
        self.nodeType = type
        self.position = position
    
    def __repr__(self):
        return f"{self.nodeType} at {self.position}"
    
    def ChangeNode(self, type=""):
        """
        Changes the Node's character.
        """
        if type in (None, ""):
            raise ValueError(type)

        self.nodeType = type
        
class PlayField:
    """
    A grid of Nodes that make up the playing field.
    """

    def __init__(self, gridSize=10):

        self.gridSizeY = gridSize
        self.gridSizeX = self.gridSizeY * 2

        self.grid = {}
        self.center = Location((self.gridSizeX-1) // 2, (self.gridSizeY-1) // 2)

        #A list of locations
        self.changedNodes = []

        self.CreateGrid()

    def CreateGrid(self):
        """
        Assigns a node to every positional value determined by the gridSize.
        """
        for y in range(self.gridSizeY):
            for x in range(self.gridSizeX):
                location = Location(x, y)
                node = Node(position=location)

                self.grid[location] = node
        
        self.PrintGrid()

    def LocationIsOccupied(self, location):
        return location in self.changedNodes

    def LocationIsOutOfBounds(self, location):
        if location in self.grid:
            return False
        
        return True

    def LocationIsInvalid(self, location):
        return (self.LocationIsOccupied(location) or self.LocationIsOutOfBounds(location))

    def UpdateGrid(self, changes={}):
        """
        Updates the playfield with specified changes.\n
        Dict types: Location : String
        """
        for key, val in changes.items():
            self.grid[key].ChangeNode(val)

    def PrintGrid(self):
        """
        Prints a string in the form of a grid which represents the playfield.
        """
        count = 1
        printedGrid = ""

        #print the grid
        for node in self.grid.values():

            #start the next row
            if count >= self.gridSizeX:
                count = 1
                printedGrid += node.nodeType + "\n"

            else:
                printedGrid += node.nodeType
                count += 1

        print("\r" + printedGrid)

    def RandomLocation(self):
        """Returns a random location on the grid."""
        chosenLocation = self.center

        while self.LocationIsInvalid(chosenLocation):
            chosenLocation = Location(random.randint(1, self.gridSizeX-2), random.randint(1, self.gridSizeY-2))

        return chosenLocation