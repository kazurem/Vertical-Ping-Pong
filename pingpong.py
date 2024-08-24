# Ping Pong Game
import pygame as pg

from variables import (
    upper_player_score_font,
    lower_player_score_font,
    instructions_font,
    winner_font,
)
from variables import background_img, ball_img
from variables import upper_player_score, lower_player_score
from variables import screen_height, screen_width, screen_middle
from variables import paddle_xpos, lower_paddle_ypos, upper_paddle_ypos
from variables import window
from variables import fps
from variables import WHITE
from paddle import Paddle
from ball import Ball


pg.init()
pg.font.init()


def draw_on_window(
    window,
    ball: Ball,
    lower_paddle: Paddle,
    upper_paddle: Paddle,
    upper_player_score: int,
    lower_player_score: int,
    is_updating: bool,
    game_over: bool,
    winner: str,
):

    # To refresh the display each loop
    window.blit(background_img, (0, 0))

    # Drawing the ball and paddles
    window.blit(ball_img, (ball.ball_rect.x, ball.ball_rect.y))

    # I subtracted 30 from the y position because that was making the image and the rect perfecty align with each other
    window.blit(
        lower_paddle.paddle_img,
        (lower_paddle.paddle_rect.x, lower_paddle.paddle_rect.y - 30),
    )
    window.blit(
        upper_paddle.paddle_img,
        (upper_paddle.paddle_rect.x, upper_paddle.paddle_rect.y - 30),
    )

    # Draw the middle line
    pg.draw.line(
        window, WHITE, (0, screen_height // 2), (screen_width, screen_height // 2)
    )

    # Displaying the player scores on the window
    player_left_score_text = upper_player_score_font.render(
        f"{upper_player_score}", 1, WHITE
    )
    player_right_score_text = lower_player_score_font.render(
        f"{lower_player_score}", 1, WHITE
    )

    window.blit(player_left_score_text, (20, 20))
    window.blit(player_right_score_text, (20, 680))

    # displaying instructions
    if is_updating == False:
        instructions_text = instructions_font.render(
            "Press 'Enter' to start the game.", 1, WHITE
        )
        window.blit(
            instructions_text,
            (
                screen_width // 2 - instructions_text.get_width() // 2,
                screen_height // 2 - instructions_text.get_width() // 2,
            ),
        )

    # displaying winner
    if is_updating == False and game_over == True:
        winner_text = winner_font.render(f"{winner} Wins!", 1, WHITE)
        window.blit(
            winner_text,
            (
                screen_width // 2 - winner_text.get_width() // 2,
                screen_height // 2 - winner_text.get_height() // 2,
            ),
        )

    pg.display.update()


def reset_game(
    ball: Ball,
    lower_paddle: Paddle,
    upper_paddle: Paddle,
    upper_player_score: int,
    lower_player_score: int,
    winner: str,
    time_to_display_winner,
):
    ball.ball_rect.x = screen_middle[0]
    ball.ball_rect.y = screen_middle[1]

    lower_paddle.paddle_rect.x = paddle_xpos
    lower_paddle.paddle_rect.y = lower_paddle_ypos
    upper_paddle.paddle_rect.x = paddle_xpos
    upper_paddle.paddle_rect.y = upper_paddle_ypos

    upper_player_score = 0
    lower_player_score = 0

    game_over = False
    winner = None

    time_to_display_winner = 120

    return (
        ball.ball_rect.x,
        ball.ball_rect.y,
        lower_paddle.paddle_rect.x,
        lower_paddle.paddle_rect.y,
        upper_paddle.paddle_rect.x,
        upper_paddle.paddle_rect.y,
        upper_player_score,
        lower_player_score,
        game_over,
        winner,
        time_to_display_winner,
    )


def display_winner(winner):
    winner_text = winner_font.render(f"{winner} Wins!", 1, WHITE)
    window.blit(
        winner_text,
        (
            screen_width // 2 - winner_text.get_width() // 2,
            screen_height // 2 - winner_text.get_height() // 2,
        ),
    )
    pg.display.update()


def main(upper_player_score, lower_player_score):

    # Making ball and paddle instances
    ball = Ball(screen_middle[0], screen_middle[1], velocity_x=-5, velocity_y=-5)
    upper_paddle = Paddle(
        x=paddle_xpos, y=upper_paddle_ypos, velocity=10, identity="upper"
    )
    lower_paddle = Paddle(
        x=paddle_xpos, y=lower_paddle_ypos, velocity=10, identity="lower"
    )
    time_to_display_winner = 120

    # Game's statuses
    is_updating = False
    game_over = False
    run = True
    winner = None

    clock = pg.time.Clock()

    # Game loop
    while run:
        clock.tick(fps)  # Setting the fps

        for event in pg.event.get():
            # Quit the game if you press 'X'
            if event.type == pg.QUIT:
                run = False

            # To start the game, you need to press 'ENTER"
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    is_updating = True

        if is_updating == True and game_over == False:

            key_pressed = pg.key.get_pressed()

            upper_paddle.update(key_pressed, ball)
            lower_paddle.update(key_pressed, ball)

            upper_player_score, lower_player_score = ball.update(
                upper_player_score, lower_player_score
            )

            # Win conditions
            if upper_player_score == 5:
                winner = "Upper Player Wins"
                is_updating = False
                game_over = True

            elif lower_player_score == 5:
                winner = "Lower Player Wins"
                is_updating = False
                game_over = True

        # Reset game variables
        if game_over == True and is_updating == True:
            (
                ball.ball_rect.x,
                ball.ball_rect.y,
                lower_paddle.paddle_rect.x,
                lower_paddle.paddle_rect.y,
                upper_paddle.paddle_rect.x,
                upper_paddle.paddle_rect.y,
                upper_player_score,
                lower_player_score,
                game_over,
                winner,
                time_to_display_winner,
            ) = reset_game(
                ball,
                upper_paddle,
                lower_paddle,
                upper_player_score,
                lower_player_score,
                winner,
                time_to_display_winner,
            )

        draw_on_window(
            window,
            ball,
            upper_paddle,
            lower_paddle,
            upper_player_score,
            lower_player_score,
            is_updating,
            game_over,
            winner,
        )


if __name__ == "__main__":
    main(upper_player_score, lower_player_score)

pg.quit()
