from time import sleep
from Game import Game
#Snake is a game where you control a snake made of dashes and dividers. The snake eats dots and gets longer. Eat as many dots as you can without crashing into yourself.
#The snake will start in the center, and begin moving once the player presses a movement key.
#The snake will loop to the other side of the play area when going past the edge.

#TODO: Create an intro, and allow the player to set rules in an options menu
print("Welcome to snake!")
sleep(2)



gameSpeed = 1.0
theGame = Game()

theGame.player1.snake.length = 5

while theGame.won == False:
    
    theGame.Play()
    
    sleep(gameSpeed)