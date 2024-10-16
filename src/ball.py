import pygame as pg
from variables import ball_diameter
from variables import screen_middle, screen_height, screen_width
from variables import upper_player_score, lower_player_score

pg.init()


class Ball(pg.sprite.Sprite):

    def __init__(self, x: int, y: int, velocity_x=5, velocity_y=5):
        pg.sprite.Sprite.__init__(self)

        self.velocity = [velocity_x, velocity_y]  # x and y velocities are the same
        self.ball_rect = pg.Rect(x, y, ball_diameter, ball_diameter)

    def update(self, upper_player_score: int, lower_player_score: int):
        # Update the ball's x and y coordinates
        self.ball_rect.x += self.velocity[0]
        self.ball_rect.y += self.velocity[1]

        # ball crosses the right boundary of the window
        if self.ball_rect.top <= 0:
            lower_player_score += 1
            self.ball_rect.x = screen_middle[0]
            self.ball_rect.y = screen_middle[1]

        # ball crosses the right boundary of the window
        elif self.ball_rect.bottom >= screen_height:
            upper_player_score += 1
            self.ball_rect.x = screen_middle[0]
            self.ball_rect.y = screen_middle[1]

        # ball crosses the upper boundary of the window
        elif self.ball_rect.right >= screen_width:
            self.velocity[0] = -self.velocity[0]

        # ball crosses the lower boundary of the window
        elif self.ball_rect.left <= 0:
            self.velocity[0] = -self.velocity[0]

        return upper_player_score, lower_player_score
