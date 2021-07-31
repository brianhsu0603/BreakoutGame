"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
import time


FRAME_RATE = 1000 / 120 # 120 frames per second

def main():
    graphics = BreakoutGraphics()

    # Add animation loop here!
   
    _dx = graphics.get_dx()
    _dy = graphics.get_dy()

    while(True):

        pause(FRAME_RATE)

        if graphics.started_or_not == 1:

            graphics.ball.move(_dx, _dy)

            if graphics.ball.x <= 0 or graphics.ball.x+graphics.ball_radius*2 >= graphics.window.width:
                _dx *= -1

            if graphics.ball.y <= 0:
                _dy *= -1

            obj = graphics.detect_object()

            if obj is not None:

                if (obj is not graphics.paddle) and (obj is not graphics.score_board) and (obj is not graphics.lives) and (obj not in graphics.falling_bricks):
                    graphics.remove_bricks(obj)
                    _dy *= -1
                    #speed up the ball
                    if abs(_dy) <= 15:
                        if _dy < 0:
                            _dy-=0.2
                        else:
                            _dy+=0.2
                    
                elif obj is graphics.paddle:
                    _dy *= -1
                else:
                    pass

            if (graphics.ball.y > graphics.window.height) or graphics.paddle_collision() == True:
                graphics.lost_lives()
                graphics.reset()

            for brick in graphics.falling_bricks:
                if brick.y > graphics.window_height:
                    graphics.remove_falling_bricks(brick)
                brick.move(0,graphics.get_dy())

            if graphics.num_lives == 0:
                result = graphics.message("You Lose!")
                graphics.window.add(result)
                break
            
            if graphics.bricks_num == 0:
                result = graphics.message("You Win!")
                graphics.window.add(result)
                break


if __name__ == '__main__':
    main()
