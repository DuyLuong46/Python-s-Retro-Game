from graphics2 import *
import random
import time
from buttons import Button

# Constants
WIDTH = 800
HEIGHT = 600
BALL_RADIUS = 15
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 70
BALL_SPEED_X = 8
BALL_SPEED_Y = 8
WINNING_SCORE = 5

class PingPongGame:
    def __init__(self):
        self.win = GraphWin("Ping Pong Game", WIDTH, HEIGHT)
        self.win.setBackground("black")
        self.is_game_active = True  # Track game state
        self.window_open = True       # Track window open state
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()
        title = Text(Point(WIDTH / 2, HEIGHT / 2 - 150), "PingPong")  # Move title higher
        title.setFill("white")
        title.setSize(36)
        title.draw(self.win)

        # Adjust the button sizes and positions
        button_width = 160
        button_height = 40
        gap = 20  # Increased gap between buttons

        play_button = Button(self.win, Point(WIDTH / 2, HEIGHT / 2 - 30), button_width, button_height, "Play")
        instruction_button = Button(self.win, Point(WIDTH / 2, HEIGHT / 2 + gap + button_height - 30), button_width, button_height, "Instructions")
        exit_button = Button(self.win, Point(WIDTH / 2, HEIGHT / 2 + 2 * (gap + button_height) - 30), button_width, button_height, "Exit")

        while True:
            click_point = self.win.getMouse()
            if play_button.is_clicked(click_point):
                self.start_game()
                break
            elif instruction_button.is_clicked(click_point):
                self.show_instructions()
                break
            elif exit_button.is_clicked(click_point):
                self.confirm_exit()

    def show_instructions(self):
        self.clear_window()
        instructions = Text(Point(WIDTH / 2, HEIGHT / 2), "Use W to move up and S to move down.\n"
                                                           "Try to hit the ball past the NPC paddle!")
        instructions.setFill("white")
        instructions.setSize(24)
        instructions.draw(self.win)

        back_button = Button(self.win, Point(WIDTH / 2, HEIGHT / 2 + 50), 120, 30, "Back")
        while True:
            click_point = self.win.getMouse()
            if back_button.is_clicked(click_point):
                self.show_main_menu()
                break

    def confirm_exit(self):
        self.clear_window()
        message = Text(Point(WIDTH / 2, HEIGHT / 2 - 20), "Are you sure?")
        message.setFill("white")
        message.setSize(24)
        message.draw(self.win)

        yes_button = Button(self.win, Point(WIDTH / 2 - 60, HEIGHT / 2 + 20), 50, 30, "Yes")
        no_button = Button(self.win, Point(WIDTH / 2 + 60, HEIGHT / 2 + 20), 50, 30, "No")

        while self.window_open:  # Check window open state
            click_point = self.win.getMouse()
            if yes_button.is_clicked(click_point):
                self.window_open = False  # Set window state to closed
                self.win.close()           # Close the window
                break
            elif no_button.is_clicked(click_point):
                self.show_main_menu()
                break

    def end_game(self):
        self.is_game_active = False  # Set game state to inactive
        self.ball.undraw()
        self.left_paddle.undraw()
        self.right_paddle.undraw()
        self.score_display.undraw()

        message = "You Win!" if self.left_score >= WINNING_SCORE else "You Lose!"
        result_text = Text(Point(WIDTH / 2, HEIGHT / 2), message)
        result_text.setFill("white")
        result_text.setSize(36)
        result_text.draw(self.win)

        menu_button = Button(self.win, Point(WIDTH / 2, HEIGHT / 2 + 50), 120, 30, "Menu")
        while self.window_open:  # Check window open state
            click_point = self.win.getMouse()
            if menu_button.is_clicked(click_point):
                self.show_main_menu()
                break

    def start_game(self):
        self.left_score = 0
        self.right_score = 0
        self.win.clear()
        self.draw_game_elements()
        self.run_game()

    def draw_game_elements(self):
        self.left_paddle = Rectangle(Point(30, HEIGHT // 2 - PADDLE_HEIGHT // 2),
                                      Point(30 + PADDLE_WIDTH, HEIGHT // 2 + PADDLE_HEIGHT // 2))
        self.left_paddle.setFill("white")
        self.left_paddle.draw(self.win)

        self.right_paddle = Rectangle(Point(WIDTH - 40, HEIGHT // 2 - PADDLE_HEIGHT // 2),
                                       Point(WIDTH - 40 + PADDLE_WIDTH, HEIGHT // 2 + PADDLE_HEIGHT // 2))
        self.right_paddle.setFill("white")
        self.right_paddle.draw(self.win)

        self.ball = Circle(Point(WIDTH // 2, HEIGHT // 2), BALL_RADIUS)
        self.ball.setFill("white")
        self.ball.draw(self.win)

        self.score_display = Text(Point(WIDTH / 2, 30), f"{self.left_score} : {self.right_score}")
        self.score_display.setFill("white")
        self.score_display.setSize(24)
        self.score_display.draw(self.win)

        self.ball_dx = BALL_SPEED_X
        self.ball_dy = BALL_SPEED_Y

    def run_game(self):
        while self.left_score < WINNING_SCORE and self.right_score < WINNING_SCORE:
            self.ball.move(self.ball_dx, self.ball_dy)
            self.check_ball_collision()
            self.check_player_input()
            self.move_npc()  # Move the NPC paddle
            time.sleep(0.03)

        self.end_game()

    def check_ball_collision(self):
        ball_pos = self.ball.getCenter()
        ball_x = ball_pos.getX()
        ball_y = ball_pos.getY()

        if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= HEIGHT:
            self.ball_dy = -self.ball_dy

        if (ball_x - BALL_RADIUS <= 40 and self.left_paddle.getP1().getY() <= ball_y <= self.left_paddle.getP2().getY()):
            self.ball_dx = -self.ball_dx
            self.ball.move(40 - (ball_x - BALL_RADIUS), 0)  # Reposition the ball to avoid getting stuck

        elif (ball_x + BALL_RADIUS >= WIDTH - 40 and self.right_paddle.getP1().getY() <= ball_y <= self.right_paddle.getP2().getY()):
            self.ball_dx = -self.ball_dx
            self.ball.move(-(ball_x + BALL_RADIUS - (WIDTH - 40)), 0)  # Reposition the ball to avoid getting stuck

        if ball_x < 0:
            self.right_score += 1
            self.update_score()
            self.reset_ball()
        elif ball_x > WIDTH:
            self.left_score += 1
            self.update_score()
            self.reset_ball()

    def check_player_input(self):
        key = self.win.checkKey()
        if key == 'w':
            self.move_paddle(self.left_paddle, -20)
        elif key == 's':
            self.move_paddle(self.left_paddle, 20)

    def move_npc(self):
        ball_pos = self.ball.getCenter()
        npc_center_y = (self.right_paddle.getP1().getY() + self.right_paddle.getP2().getY()) / 2

        # Move the NPC paddle based on the ball's position
        if ball_pos.getY() < npc_center_y - 10:
            self.move_paddle(self.right_paddle, -5)  # Move up
        elif ball_pos.getY() > npc_center_y + 10:
            self.move_paddle(self.right_paddle, 5)   # Move down

    def move_paddle(self, paddle, dy):
        paddle.move(0, dy)
        if paddle.getP1().getY() < 0:
            paddle.move(0, -paddle.getP1().getY())
        elif paddle.getP2().getY() > HEIGHT:
            paddle.move(0, HEIGHT - paddle.getP2().getY())

    def update_score(self):
        self.score_display.setText(f"{self.left_score} : {self.right_score}")

    def reset_ball(self):
        self.ball.move(WIDTH // 2 - self.ball.getCenter().getX(), HEIGHT // 2 - self.ball.getCenter().getY())
        self.ball_dx = BALL_SPEED_X * random.choice([-1, 1])
        self.ball_dy = BALL_SPEED_Y * random.choice([-1, 1])

    def clear_window(self):
        for item in self.win.items[:]:
            item.undraw()

# Run the game
if __name__ == "__main__":
    PingPongGame()