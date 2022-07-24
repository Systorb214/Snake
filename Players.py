import PFObjects as pfo
from pynput import keyboard as kb
#This script will contain a "Player" class as a base, with derived "Human" and "AI" classes.
#The "Human" class will have keyboard controls, while the AI is controlled by the computer.

class Player:
    """The base class for all players."""

    def __init__(self, name: str, charset=[]):
        self.score = 0
        """The player's score. Increases when food is eaten."""
        self.name = name
        """The player's name."""
        self.snake = None
        """The player's snake."""

        #Charset must include up, down, left, and right directions
        if len(charset) == 4:
            self.snake = pfo.Snake(charset)
        else:
            self.snake = pfo.Snake()
        
#example of char key
    #kb.KeyCode.from_char('r')

#example of non-char key
    #kb.Key.left

class Human(Player):
    """A human player that uses keyboard controls."""

    directions = ["up", "down", "left", "right"]

    def __init__(self, name: str, keys=[kb.Key.up, kb.Key.down, kb.Key.left, kb.Key.right], charset=[]):
        super().__init__(name, charset)
        self.keys = {}
        
        #Create dict with "keys" list elements as dict keys
        for i in range(len(Human.directions)):
            self.keys[Human.directions[i]] = keys[i]


    def Control(self, key):
        """Controls the snake. Used with a keyboard listener.

        Args:
            key (keyboard.Key): The key that was pressed.
        """

        for i in Human.directions:
            if key == self.keys[i]:
                self.snake.Rotate(i)

class Bot(Player):
    
    def __init__(self, pField, name: str, chars=[]):
        super().__init__(name, chars)

        self.pField = pField