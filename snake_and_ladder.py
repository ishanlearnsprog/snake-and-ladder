import random

class Player:

    def __init__(self, name):
        self.name = name
        self.pos = 0
    
class Dice:

    def __init__(self, size):
        self.size = size
    
    def rollDice(self):
        return random.randint(1, self.size)

class Board:

    # instatiate new game board with snake and ladders
    def __init__(self):
        self.board = [0] * 100

        # generate snakes
        snakeCount = 6
        while snakeCount != 0:
            
            # generate snake head
            while True:
                topx = random.randint(0,9)
                topy = random.randint(1,9)
                top = 10 * topy + topx #snake head
                if top != 99 and self.board[top] == 0: break

            # generate snake tail
            while True:                
                botx = random.randint(0,9)
                boty = random.randint(0,9)
                bot = 10 * boty + botx
                if bot != 0 and boty < topy and self.board[bot] == 0: break
            
            # make snake
            self.board[top] = bot
            self.board[bot] = 101 # position lock
            snakeCount -= 1
        
        # generate ladders
        ladderCount = 6
        while ladderCount != 0:
            
            # generate ladder top
            while True:
                topx = random.randint(0,9)
                topy = random.randint(1,9)
                top = 10 * topy + topx #ladder top
                if self.board[top] == 0: break
            
            # generate ladder bottom
            while True:
                botx = random.randint(0,9)
                boty = random.randint(0,9)
                bot = 10 * boty + botx #ladder bottom
                if bot != 0 and boty < topy and self.board[bot] == 0: break

            self.board[bot] = top
            self.board[top] = 101 # position lock
            ladderCount -= 1

    # prints individual charachters
    def displayChars(self, i):
        b = self.board
        if b[i] == 0 or b[i] == 101:
            print(str(i+1), end="\t")
        else:
            if i < b[i]:
                print("L", end="\t")
            elif i > b[i]:
                print("S", end="\t")
    
    # prints the board in correct order
    def displayBoard(self):
        switch = 0
        for y in range(9, -1, -1):
            if switch == 0:
                for x in range(9, -1, -1):
                    # print(b[10*y+x], end="\t")
                    self.displayChars(10*y+x)
            else:
                for x in range(0, 10):
                    # print(b[10*y+x], end="\t")
                    self.displayChars(10*y+x)
            print()
            switch = not switch    

class SnakeAndLadderGame():

    # Initialize Game Session
    def __init__(self):

        print("Welcome to Snake and Ladder\n")
        
        # Input number of players
        while True:

            try:
                numberOfPlayers = input("Enter the number of players (default 2, min 2, max 5): ")
            
                if numberOfPlayers == '': 
                    numberOfPlayers = 2
                elif 2 <= int(numberOfPlayers) <= 5:
                    numberOfPlayers = int(numberOfPlayers)
                else:
                    raise ValueError("Error in numberOfPlayers: Please enter valid number between 2 and 5!")

            except ValueError:
                print("Error in numberOfPlayers: Please enter valid number between 2 and 5!")
                continue
            
            break
    
        # Instantiate players
        self.players = []
        for i in range(numberOfPlayers):
            
            name = input("\nEnter player name (default name: Player {}): ".format(i+1))
            if name == '': name = "Player {}".format(i+1)

            self.players.append(Player(name))

        while True:

            try:
                sizeOfDice = input("\nEnter the size of dice (default 6, min 6, max 10): ")
            
                if sizeOfDice == '': 
                    sizeOfDice = 6
                elif 6 <= int(sizeOfDice) <= 10:
                    sizeOfDice = int(sizeOfDice)
                else:
                    raise ValueError("Error in sizeOfDice: Please enter valid number between 6 and 10!")

            except ValueError:
                print("Please enter valid number between 6 and 10!")
                continue
            
            break
        
        self.dice = Dice(sizeOfDice)

        print()
        self.board = Board()
        self.board.displayBoard()
        print ()

        self.winner = None
    
    def runGame(self):
        
        b = self.board.board

        while True:

            for p in self.players:

                input("\n{}'s Turn \nPlayer is at poistion {} \nPress enter to roll dice".format(p.name, p.pos+1))

                move = self.dice.rollDice()
                print("\nThe dice rolled to {}".format(move))

                pos = p.pos + move
                if pos > 99:
                    print(pos) 
                    print("\nThe player can not move \nRoll a {} to win".format(100 - p.pos))
                    self.gameStatus()
                    continue
                print("\nThe player moves to position {}".format(pos+1))

                if b[pos] != 0 and b[pos] != 101:
                    if b[pos] > pos:
                        print("\nThe palyer found a ladder")
                        print("The player moves to position {}".format(b[pos] + 1))
                    elif b[pos] < pos:
                        print("\nThe palyer was bit by a snake")
                        print("The player moves to position {}".format(b[pos] + 1))
                    pos = b[pos]
                
                p.pos = pos

                if p.pos == 99:
                    self.winner = p
                    print("\n{} has won the game :)".format(p.name))
                    break

                self.gameStatus()
            
            if self.winner != None:
                break
    
    def gameStatus(self):
        print("\nGame Status")
        for pp in self.players:
            print("{}'s Position: {}".format(pp.name, pp.pos+1))
                
if __name__ == "__main__":
    game = SnakeAndLadderGame()
    game.runGame()