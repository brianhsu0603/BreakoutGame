"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random


BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).
NUM_LIVES = 3          # Number of attempts

INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.

class BreakoutGraphics:

    def __init__(self, ball_radius = BALL_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space
        self.window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        self.window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=self.window_width, height=self.window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height, x=(self.window_width-paddle_width)/2, y=self.window_height-paddle_offset)
        self.paddle.filled = True
        self.window.add(self.paddle)
        self.paddle_offset = paddle_offset
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2, x=(self.window_width-ball_radius*2)/2, y=(self.window_height-ball_radius*2)/2)
        self.ball_radius = ball_radius
        self.ball.filled=True
        self.window.add(self.ball)

        # Default initial velocity for the ball
        self.__dx = random.randint(1, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
   
        if (random.random() > 0.5):
            self.__dx = -self.__dx 


        # Draw bricks
        self.bricks_num = brick_cols*brick_rows
        brick_x = 0 
        brick_y = brick_offset

        if brick_rows < 5:
            num_of_each_color = 1
        else:
            num_of_each_color = int(brick_rows/5)
        
        color_list = ["red","orange","yellow","green","blue"]
        color_index = 0

        for row in range(brick_rows):
            for column in range(brick_cols):
                    brick = GRect(brick_width, brick_height, x=brick_x,y=brick_y)
                    brick.filled=True
                    brick.fill_color=color_list[color_index]
                    self.window.add(brick)
                    brick_x += (brick_width + brick_spacing)
            num_of_each_color -= 1
            if num_of_each_color == 0:
                num_of_each_color = int(brick_rows/5)
                color_index += 1
                if color_index == 5:
                    color_index = 0

            brick_x = 0
            brick_y += (brick_height + brick_spacing)

        self.falling_bricks = []

        #Score Board
        self.score_board = GLabel("Score: 0", 0, 40)
        self.score_board.font_size = "-30"
        self.window.add(self.score_board)
        self.score = 0
        
        #Lives left
        self.num_lives = 3
        self.lives = GLabel("Lives: " + str(self.num_lives), self.window_width - 50, 40)
        self.score_board.font_size = "-30"
        self.window.add(self.lives)

        #Initialize our mouse listeners
        self.started_or_not = 0
        onmouseclicked(self.start)
        onmousemoved(self.paddle_move)


    def get_dx(self):
        return self.__dx
        
    def get_dy(self):
        return self.__dy
        
    def start(self, mouse):
        self.started_or_not = 1

    def paddle_move(self,mouse):
        if self.started_or_not == 1:    
            self.window.add(self.paddle,(mouse.x-self.paddle.width/2),self.window_height-self.paddle_offset)
            if self.paddle.x <= 0:
                self.paddle.x = 0
            if self.paddle.x + self.paddle_width >= self.window_width:
                self.paddle.x= self.window.width - self.paddle_width   

    def detect_object(self):
        upper_left = self.window.get_object_at(self.ball.x, self.ball.y)
        upper_right = self.window.get_object_at(self.ball.x+2*(self.ball_radius), self.ball.y)
        lower_left = self.window.get_object_at(self.ball.x, self.ball.y+2*(self.ball_radius))
        lower_right = self.window.get_object_at(self.ball.x+2*(self.ball_radius), self.ball.y+2*(self.ball_radius))
        if upper_left is not None:
            return upper_left
        elif upper_right is not None:
            return upper_right
        elif lower_left is not None:
            return lower_left
        elif lower_right is not None:
            return lower_right

    def paddle_collision(self):
        upper_left_ = self.window.get_object_at(self.paddle.x + 15, self.paddle.y - 1)
        upper_right_ = self.window.get_object_at(self.paddle.x + self.paddle_width - 15, self.paddle.y - 1)

        if (upper_left_ is None) and (upper_right_ is None):
            return False

        elif (upper_left_ is not None and upper_left_ is not self.ball) and (upper_right_ is not None and upper_right_ is not self.ball):
            self.falling_bricks.remove(upper_left_)
            self.window.remove(upper_left_)
            self.falling_bricks.remove(upper_right_)
            self.window.remove(upper_right_)
            return True
        elif (upper_left_ is not None and upper_left_ is not self.ball) and (upper_right_ is None):
            self.falling_bricks.remove(upper_left_)
            self.window.remove(upper_left_)
            return True
        elif (upper_left_ is None) and (upper_right_ is not None and upper_right_ is not self.ball):
            self.falling_bricks.remove(upper_right_)
            self.window.remove(upper_right_)
            return True

    def message(self, result):
        
        message = GLabel(result, x = self.window_width/2 - 25, y = (self.window_height-self.ball_radius*2)/2 + 100)

        return message

    def update_score(self):
        self.score += 1
        self.window.remove(self.score_board)
        self.score_board = GLabel("Score: " + str(self.score), 0, 40)
        self.score_board.font_size = "-30"
        self.window.add(self.score_board)

    def lost_lives(self):
        self.window.remove(self.lives)
        self.num_lives -= 1
        self.lives = GLabel("Lives: " + str(self.num_lives), self.window_width - 100, 40)
        self.score_board.font_size = "-30"
        self.window.add(self.lives)
    
    def remove_bricks(self,obj):
        self.falling_bricks.append(obj)
        self.bricks_num-=1
        self.update_score()

    def remove_falling_bricks(self,obj):
        self.falling_bricks.remove(obj)
        self.window.remove(obj)

    def reset(self):
         self.started_or_not = 0
         self.ball.x = (self.window_width-self.ball_radius*2)/2
         self.ball.y = (self.window_height-self.ball_radius*2)/2
         self.paddle.x = (self.window_width-self.paddle_width)/2
         self.paddle.y = self.window_height-self.paddle_offset



    
       






