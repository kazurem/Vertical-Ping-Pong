import pygame as pg

pg.init()
pg.font.init()
pg.mixer.init()

# screen variables
screen_width = 800
screen_height = 700
window = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Ping Pong")

fps = 60

# colors
WHITE = (255, 255, 255)

# ball variables
ball_diameter = 20
screen_middle = (
    screen_width // 2 - ball_diameter // 2,
    screen_height // 2 - ball_diameter // 2,
)
ball_img = pg.transform.scale(
    pg.image.load("./assets/sprite-assets/ball/ball.png"),
    (ball_diameter, ball_diameter),
)


# paddle variables
paddle_width = 100
paddle_height = 20
paddle_xpos = screen_width // 2 - paddle_width // 2
upper_paddle_ypos = 50
lower_paddle_ypos = 650

# Importing paddle assets
lower_paddle_img = pg.transform.scale(
    pg.image.load("./assets/sprite-assets/paddle/lower_paddle.png"),
    (paddle_width, paddle_height * 4),
)
upper_paddle_img = pg.transform.scale(
    pg.image.load("./assets/sprite-assets/paddle/upper_paddle.png"),
    (paddle_width, paddle_height * 4),
)


# Scores
upper_player_score = 0
lower_player_score = 0

# initialzing fonts for scores,winner and instructions
upper_player_score_font = pg.font.SysFont("comicsans", 30)
lower_player_score_font = pg.font.SysFont("comicsans", 30)
winner_font = pg.font.SysFont("comicsans", 70)
instructions_font = pg.font.SysFont("comicsans", 50)

background_img = pg.image.load("./assets/background/Space Background.png")

collision_sound = pg.mixer.Sound("./assets/sound-assets/collision.mp3")
