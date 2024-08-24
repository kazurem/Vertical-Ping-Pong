import pygame as pg
from variables import paddle_height, paddle_width
from variables import upper_paddle_img, lower_paddle_img
from variables import screen_height, screen_width
from variables import collision_sound

pg.init()
pg.font.init()


class Paddle(pg.sprite.Sprite):

    def __init__(self, x: int, y: int, velocity: int, identity: str):
        pg.sprite.Sprite.__init__(self)

        self.velocity = velocity
        self.identity = identity  # left paddle or right paddle

        if self.identity == "upper":
            self.paddle_img = upper_paddle_img
        elif self.identity == "lower":
            self.paddle_img = lower_paddle_img

        self.paddle_rect = pg.Rect(x, y, paddle_width, paddle_height)

    def update(self, key_pressed, ball):

        # For upper paddle
        if (
            key_pressed[pg.K_a]
            and self.paddle_rect.left > 0
            and self.identity == "upper"
        ):
            self.paddle_rect.x -= self.velocity

        elif (
            key_pressed[pg.K_d]
            and self.paddle_rect.right < screen_width
            and self.identity == "upper"
        ):
            self.paddle_rect.x += self.velocity

        # For lower paddle
        elif (
            key_pressed[pg.K_LEFT]
            and self.paddle_rect.left > 0
            and self.identity == "lower"
        ):
            self.paddle_rect.x -= self.velocity

        elif (
            key_pressed[pg.K_RIGHT]
            and self.paddle_rect.right < screen_width
            and self.identity == "lower"
        ):
            self.paddle_rect.x += self.velocity

        # Collision of ball with the paddle
        if (
            self.paddle_rect.colliderect(ball.ball_rect)
            and self.identity == "upper"
            and ball.ball_rect.top - ball.velocity[1] >= self.paddle_rect.bottom
        ):
            ball.velocity[1] = -ball.velocity[1]
            collision_sound.play()

        if (
            self.paddle_rect.colliderect(ball.ball_rect)
            and self.identity == "lower"
            and ball.ball_rect.bottom + ball.velocity[1] >= self.paddle_rect.top
        ):
            ball.velocity[1] = -ball.velocity[1]
            collision_sound.play()
