'''
Name: Duy Luong
CSC 201
Programming Project 4

This program plays a version of Little Spider Solitaire. In this version
the foundation piles starting with two red aces and two black kings
are created when the game begins. The eight tableau piles are in
one horizontal line. At any time, cards can be moved from the
tableau to the foundation piles or to another tableau, as long as
it is a valid move. One point is earned for every valid move to
a foundation pile.

Document Assistance (who and what or declare no assistance):
No assistance and received no assistance.
'''
from board import *
from button import *
from deck import *
import graphics2  # Ensure this is your graphics library
import time

GAME_WINDOW_WIDTH = 750
GAME_WINDOW_HEIGHT = 500
MAX_SCORE = 52  # Set this based on total cards in the game

def displayDirections():
    """Displays the directions for Little Spider Solitaire."""
    win = graphics2.GraphWin("Directions", 700, 600)
    win.setBackground("white")
    string = ("Welcome to Little Spider Solitaire\n\n"
                "The objective is to get all cards moved to the foundation piles.\n"
                "The top card of a tableau can be moved to a foundation pile if it is\n"
                "the same suit as the foundation pile and is one rank above the top\n"
                "foundation card for red suits or one rank below for black suits.\n\n"
                "To move a card, click on the tableau card, then click on the foundation\n"
                "card where you want to move it.\n\n"
                "You can also move tableau cards to other tableau piles if they are one\n"
                "rank apart, including moving a King on an Ace and vice versa.\n\n"
                "Click the stock pile to deal eight cards from the stock.\n\n"
                "Good luck!")
    directions = graphics2.Text(graphics2.Point(win.getWidth()/2, win.getHeight()/2), string)
    directions.setSize(16)
    directions.draw(win)
    startButton = Button(graphics2.Point(350, 525), 120, 40, "Click to Begin")
    startButton.draw(win)
    startButton.activate()
    click = win.getMouse()
    while not startButton.isClicked(click):
        click = win.getMouse()
    win.close()

def setUpGame():
    """Sets up the game window and initializes the game components.

    Returns:
        tuple: A tuple containing the window (GraphWin), game board (LittleSpiderBoard),
               start button (Button), and score label (Text).
    """
    win = graphics2.GraphWin('Little Spider Solitaire', GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT)
    win.setBackground('lightgreen')
    
    gameBoard = LittleSpiderBoard(win)
    
    button = Button(graphics2.Point(675, 50), 80, 40, "Start")
    button.draw(win)
    button.activate()
    
    scoreLabel = graphics2.Text(graphics2.Point(70, 450), "Score: 0")
    scoreLabel.setSize(16)
    scoreLabel.draw(win)

    messageLabel = graphics2.Text(graphics2.Point(375, 475), "")
    messageLabel.setSize(20)
    messageLabel.draw(win)

    click = win.getMouse()
    while not button.isClicked(click):
        click = win.getMouse()
    
    button.setLabel("Quit")
    
    gameBoard.dealFromStock(win)
    return win, gameBoard, button, scoreLabel, messageLabel



def canMoveToFoundation(card, foundationCard):
    """Check if a card can be moved to the foundation pile."""
    if foundationCard is None:
        return False
    if card.getRank() == foundationCard.getRank() + 1 and card.getSuit() in ['h', 'd']:
        return True
    if card.getRank() == foundationCard.getRank() - 1 and card.getSuit() in ['c', 's']:
        return True
    return False

def canMoveToTableau(card, destinationCard):
    """Check if a card can be moved to another tableau based on rank."""
    if destinationCard is None:
        return True
    if (card.getRank() == destinationCard.getRank() + 1 or 
        card.getRank() == destinationCard.getRank() - 1):
        return True 
    return False

def getScoreMessage(score):
    """Return a message based on the player's score."""
    if score < 10:
        return "Were you even trying?"
    elif score < 20:
        return "Not good enough"
    elif score < 30:
        return "Good job"
    elif score >= MAX_SCORE:
        return "You win!"
    else:
        return "Keep going!"
    
def playGame(window, gameBoard, button, scoreLabel, messageLabel):
    """Plays the Little Spider Solitaire game enforcing the rules.

    Params:
        window (GraphWin): The window where the game is played.
        gameBoard (LittleSpiderBoard): The board managing the cards.
        button (Button): The button to click to end the game.
        scoreLabel (Text): The label showing the game score as the game progresses.
        messageLabel (Text): The label to display win/loss messages.

    Returns:
        int: The score earned by the player determined by the number of cards moved to the foundation piles.
    """
    score = 0
    selectedCard = None
    click = window.getMouse()

    while not button.isClicked(click):
        if gameBoard.isPointInStockCard(click) and not gameBoard.isStockEmpty():
            gameBoard.dealFromStock(window)
        
        elif gameBoard.isPointInTableauCard(click):
            selectedCard = gameBoard.getCardAtPoint(click)
            click2 = window.getMouse()
            
            if gameBoard.isPointInFoundationCard(click2):
                foundationCard = gameBoard.getCardAtPoint(click2)
                if canMoveToFoundation(selectedCard, foundationCard):
                    gameBoard.moveCardToFoundationPile(selectedCard, click2, window)
                    score += 1
                    scoreLabel.setText(f'Score: {score}')
                
            elif gameBoard.isPointInTableauCard(click2) or gameBoard.isPointInEmptyTableau(click2):
                destinationCard = None
                if gameBoard.isPointInTableauCard(click2):
                    destinationCard = gameBoard.getCardAtPoint(click2)
                
                if canMoveToTableau(selectedCard, destinationCard):
                    gameBoard.moveCardToAnotherTableauPile(selectedCard, click2, window)
            
            selectedCard = None

        if gameBoard.isWin():
            messageLabel.setText("You win!")
            return score
        
        click = window.getMouse()

    messageLabel.setText(getScoreMessage(score))
    return score

def main():
    """Main function to run the Little Spider Solitaire game."""
    displayDirections()
    
    window, gameBoard, button, scoreLabel, messageLabel = setUpGame()
    
    score = playGame(window, gameBoard, button, scoreLabel, messageLabel)
       
    time.sleep(2)    
    window.close()

if __name__ == '__main__':
    main()