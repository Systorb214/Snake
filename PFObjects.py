import Playfield as pf

class PlayfieldObject:
    """The base class for Playfield objects. This defines each object's charset dictionary."""
    _charsetkeys = []

    def __init__(self, csValues=[]):
        self.charset = {}

        for key in self._charsetkeys:
            self.charset[key] = ""

        if csValues != []:
            self.ChangeCharacters(csValues)

    def ChangeCharacters(self, values: list):
        """Creates/changes the object's character set values."""
        
        #define values list iterator
        iterator = 0
        #iterate over charset keys
        for key in self.charset.keys():

            #If value length is incorrect, raise exception
            if len(values[iterator]) != 1:
                raise f"Character ({values[iterator]}) must have a length of 1."

            #set each character in charset to a character in values list
            self.charset[key] = values[iterator]

            #increment values list iterator
            iterator += 1

            #break loop if values iterator is greater than values list
            if iterator > len(values):
                break
            
class Food:
    foodCount = 0

    def __init__(self, char="o", power: int=1):
        self.power = power
        self.node = pf.Node(char)
        Food.foodCount += 1

    def __del__(self):
        Food.foodCount -= 1
        print("foodCount: " + str(Food.foodCount))

class Wall(PlayfieldObject):
    _charsetkeys = ["vertical", "horizontal", "diag1", "diag2"]

    def __init__(self, name="wall", csValues=["|", "—", "\\", "/"]):
        super().__init__(csValues)

        self.name = name
        self.nodeLocations = []

        #Walls are a set of wall nodes
        #Walls can change direction, the changing point has a diag character
        #The playfield border is one wall.
        
    def Draw(self, start: pf.Location, end: pf.Location, turnPoints: list=[]):
        """
        Draws a wall from one location to another, with an optional list of turning points.\n
        RETURNS GRID CHANGES
        """

        #Return if there is only one location given
        if start == end and len(turnPoints) < 1:
            return None

        #Dict types: Location : String
        gridChanges = {}

        #Define list of Locations, adding start and end points as well as turning points inbetween
        locations = [start]
        for point in turnPoints:
            locations.append(point)
        locations.append(end)

        #Loop through locations, adding them to gridChanges.
        for i in range(len(locations)-1):

            #Get current, next and previous locations
            cur = locations[i]

            nxt = locations[i+1]

            prev = None if i-1 < 0 else locations[i-1]

            #Get current direction
            up = cur.y > nxt.y
            left = cur.x > nxt.x

            #The changed node's character value
            character = "none"
                
            #"vertical" axis
            if cur.x == nxt.x:
                character = "vertical"
                
                #Check for turns if i-1 exists
                if prev:
                    if up:
                        #Check for up turn
                        if prev.x < cur.x:
                            character = "diag2"
                        elif prev.x > cur.x:
                            character = "diag1"
                    #Down
                    else:
                        #Check for down turn
                        if prev.x < cur.x:
                            character = "diag1"
                        elif prev.x > cur.x:
                            character = "diag2"

                #Draw walls between turn points
                for o in range(cur.y, nxt.y, -1 if up else 1):
                    gridChanges[pf.Location(cur.x, o)] = self.charset["vertical"]

            #"horizontal" axis
            elif cur.y == nxt.y:
                character = "horizontal"

                #Check for turns if i-1 exists
                if prev:
                    if left:
                        #Check for left turn
                        if prev.y < cur.y:
                            character = "diag2"
                        elif prev.y > cur.y:
                            character = "diag1"
                    #right
                    else:
                        #Check for right turn
                        if prev.y < cur.y:
                            character = "diag1"
                        elif prev.y > cur.y:
                            character = "diag2"

                #Draw walls between turn points
                for o in range(cur.x, nxt.x, -1 if left else 1):
                    gridChanges[pf.Location(o, cur.y)] = self.charset["horizontal"]

            else:
                #use pathfinding(Throw error for now) if there are missing turning points.
                raise BaseException(f"Wall {self.name} has no turn points from {cur} to {nxt}.")
                #TODO: insert pathfinding here

            #Set turnpoint to diagonal character
            gridChanges[cur] = self.charset[character]
        
        self.nodeLocations = list(gridChanges.keys())
        return gridChanges

class Snake(PlayfieldObject):
    _charsetkeys = ["up", "down", "left", "right"]

    def __init__(self, csValues=["⮝", "⮟", "⮜", "⮞"]):
        super().__init__(csValues)
        self.faceDirection = ""
        """The direction the snake's head is facing."""

        self.alive = True
        self.head = pf.Node()
        self.body = Wall()
        self.length = 0
        self._growCount = 0
        #A list of locations
        self.bodyLocations = []
        self.turningPoints = []
        
        self.Rotate("up")

    def Eat(self, food: Food):
        self._growCount += food.power

    def Grow(self):
        """Adds +1 length. Snake cannot grow if it has not eaten recently.\n
        This is intended to be called once per frame after Eat has been called.
        """
        if self._growCount > 0:
            self.length += 1
            self._growCount -= 1

    def Die(self):
        """Kills the snake."""

        self.head.ChangeNode("X")

        self.alive = False

    def Rotate(self, direction):
        """Rotates the snake's head.

        Args:
            direction (String): The direction to turn to.

        Returns:
            bool: True if the snake successfully rotated, false otherwise.
        """

        #If the given direction is the opposite of the current faceDirection, return None
        if (self.faceDirection in self._charsetkeys[:2] and direction in self._charsetkeys[:2])\
        or (self.faceDirection in self._charsetkeys[2:] and direction in self._charsetkeys[2:]):
            return False

        for dir in Snake._charsetkeys:
            if direction == dir:
                self.faceDirection = dir
                self.head.ChangeNode(self.charset[dir])

                self.turningPoints.append(self.head.position)
                return True

        return False

    def Move(self, location: pf.Location=None) -> dict:
        """Moves the snake's head to the specified location on the grid.
        Remember to check if the location is valid before using this!

        Args:
            location (pf.Location): The location to move to. If None, the snake will move forward instead.

        Returns:
            dict: Playfield grid changes (Location : String)
        """

        gridChanges = {}

        #Set node at current head location to " "
        gridChanges[self.head.position] = " "

        newLocation = pf.Location(self.head.position.x, self.head.position.y)

        if location == None:
            #movement amount
            magnitude = 1

            #Move head based on faceDirection
            if self.faceDirection == "up":
                newLocation.y -= magnitude
            elif self.faceDirection == "down":
                newLocation.y += magnitude
            elif self.faceDirection == "left":
                newLocation.x -= magnitude
            elif self.faceDirection == "right":
                newLocation.x += magnitude

            self.bodyLocations.append(self.head.position) #use newLocation if this doesn't work
            
            #Remove tail end location if bodyLocations exceeds snake length
            if len(self.bodyLocations) > self.length:

                bodyLoc = self.bodyLocations.pop(0)

                gridChanges[bodyLoc] = " "
                
                if len(self.turningPoints) > 0 and bodyLoc == self.turningPoints[0]:
                    self.turningPoints.pop(0)
        else:
            #Move head to specified location
            newLocation = location

            #Delete snake body so it can regrow itself
            self._growCount = self.length
            self.length = 0
            self.turningPoints = []
            self.bodyLocations = [newLocation]
            

        gridChanges[newLocation] = self.head.nodeType
        self.head.position = newLocation

        #Draw the body

        if self.length > 0:
            gridChanges.update(self.body.Draw(self.bodyLocations[0], self.head.position, self.turningPoints))

        return gridChanges