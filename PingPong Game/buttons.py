from graphics2 import *

class Button:
    def __init__(self, win, center, width, height, label):
        self.win = win
        self.width = width
        self.height = height
        self.rectangle = Rectangle(Point(center.getX() - width / 2, center.getY() - height / 2),
                                    Point(center.getX() + width / 2, center.getY() + height / 2))
        self.rectangle.setFill("gray")
        self.rectangle.draw(win)

        self.label = Text(center, label)
        self.label.setFill("black")
        self.label.draw(win)

    def is_clicked(self, point):
        return (self.rectangle.getP1().getX() < point.getX() < self.rectangle.getP2().getX() and
                self.rectangle.getP1().getY() < point.getY() < self.rectangle.getP2().getY())

    def undraw(self):
        self.rectangle.undraw()
        self.label.undraw()

    def draw(self):
        self.rectangle.draw(self.win)
        self.label.draw(self.win)