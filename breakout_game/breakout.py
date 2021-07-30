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
NUM_LIVES = 3			# Number of attempts


def main():
    graphics = BreakoutGraphics()

    # Add animation loop here!
   
    _dx = graphics.get_dx()
    _dy = graphics.get_dy()
    
    global NUM_LIVES

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

                if (obj is not graphics.paddle) and (obj is not graphics.score_board):
                    graphics.window.remove(obj)
                    graphics.bricks_num-=1
                    graphics.update_score()
                    _dy *= -1

                    #speed up the ball (has bug)
                    if abs(_dy) <= 15:
                        if _dy < 0:
                            _dy-=0.2
                        else:
                            _dy+=0.2
                    
                  
                elif obj is graphics.paddle:
                    _dy *= -1
                else:
                    pass

            if graphics.ball.y > graphics.window.height:
                NUM_LIVES -= 1
                graphics.started_or_not = 0
                graphics.ball.x = (graphics.window_width-graphics.ball_radius*2)/2
                graphics.ball.y = (graphics.window_height-graphics.ball_radius*2)/2

            if NUM_LIVES == 0:
                result = graphics.message("You Lose!")
                graphics.window.add(result)
                break
            
            if graphics.bricks_num == 0:
                result = graphics.message("You Win!")
                graphics.window.add(result)
                break

            


if __name__ == '__main__':
    main()
