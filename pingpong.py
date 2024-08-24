#Ping Pong Game
import pygame as pg
import time
from icecream import ic

pg.init()
pg.font.init()

screen_width = 800
screen_height = 700
window = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Ping Pong')

fps = 60

WHITE = (255,255,255)
BLACK = (0,0,0)

ball_width = 20
ball_height = 20
ball_diameter = 20
screen_middle = (screen_width//2-ball_width//2, screen_height//2 - ball_height//2)

paddle_width = 100
paddle_height = 20
paddle_xpos = screen_width//2 - paddle_width//2
upper_paddle_ypos = 50
lower_paddle_ypos = 650

lower_paddle_img = pg.transform.scale(pg.image.load('./assets/paddle/lower_paddle.png'), (paddle_width, paddle_height*4))
upper_paddle_img = pg.transform.scale(pg.image.load('./assets/paddle/upper_paddle.png'), (paddle_width, paddle_height*4))


upper_player_score = 0
lower_player_score = 0

upper_player_score_font = pg.font.SysFont('comicsans', 30)
lower_player_score_font = pg.font.SysFont('comicsans', 30)
winner_font = pg.font.SysFont('comicsans', 70)

background_img = pg.image.load('./assets/background/Space Background.png')



class Ball(pg.sprite.Sprite):
    
    def __init__(self, x: int, y: int,  velocity_x=5, velocity_y=5):
        pg.sprite.Sprite.__init__(self)
        
        self.velocity = [velocity_x, velocity_y] # x and y velocities are the same
        self.ball_rect = pg.Rect(x, y, ball_diameter, ball_diameter)
        
        
    def update(self, upper_player_score: int, lower_player_score: int):
        #Update the ball's x and y coordinates
        self.ball_rect.x += self.velocity[0]
        self.ball_rect.y += self.velocity[1]

        #ball crosses the right boundary of the window
        if self.ball_rect.top <= 0:
            lower_player_score += 1
            self.ball_rect.x = screen_middle[0]
            self.ball_rect.y = screen_middle[1]
            
        #ball crosses the right boundary of the window
        elif self.ball_rect.bottom >= screen_height:
            upper_player_score += 1
            self.ball_rect.x = screen_middle[0]
            self.ball_rect.y = screen_middle[1]
            
        #ball crosses the upper boundary of the window
        elif self.ball_rect.right >= screen_width:
            self.velocity[0] = -self.velocity[0]

        #ball crosses the lower boundary of the window
        elif self.ball_rect.left <= 0:
            self.velocity[0] = -self.velocity[0]
            
        return upper_player_score, lower_player_score
        
        
        
        
class Paddle(pg.sprite.Sprite):
    
    def __init__(self, x: int, y: int, velocity: int, identity: str):
        pg.sprite.Sprite.__init__(self)
        
        self.velocity = velocity
        self.identity = identity #left paddle or right paddle
        
        if self.identity == 'upper':
            self.paddle_img = upper_paddle_img
        elif self.identity == 'lower':
            self.paddle_img = lower_paddle_img
            
        self.paddle_rect = pg.Rect(x, y, paddle_width, paddle_height)
        
        
    def update(self, key_pressed, ball: Ball):

        #For upper paddle
        if key_pressed[pg.K_a] and self.paddle_rect.left > 0 and self.identity == 'upper':
            self.paddle_rect.x -= self.velocity
            
        elif key_pressed[pg.K_d] and self.paddle_rect.right < screen_width and self.identity == 'upper':
            self.paddle_rect.x += self.velocity

        #For lower paddle
        elif key_pressed[pg.K_LEFT] and self.paddle_rect.left > 0 and self.identity == 'lower':
            self.paddle_rect.x -= self.velocity
            
        
        elif key_pressed[pg.K_RIGHT] and self.paddle_rect.right < screen_width and self.identity == 'lower':
            self.paddle_rect.x += self.velocity
            
            
        #Collision of ball with the paddle
        if self.paddle_rect.colliderect(ball.ball_rect):
            ball.velocity[1] = -ball.velocity[1]
            

            
            

def draw_on_window(window, ball: Ball, lower_paddle: Paddle, upper_paddle: Paddle, upper_player_score: int, lower_player_score: int, winner=None,time_sleep=0):
    
    #To refresh the display each loop
    window.blit(background_img, (0, 0))
    
    #Drawing the ball and paddles
    # window.blit(ball.ball_surface, (ball.ball_rect.x, ball.ball_rect.y))
    pg.draw.circle(window, WHITE, (ball.ball_rect.x+ball.ball_rect.width//2, ball.ball_rect.y+ball.ball_rect.height//2), ball_diameter//2)
    #I subtracted 30 from the y position because that was making the image and the rect perfecty align with each other
    window.blit(lower_paddle.paddle_img, (lower_paddle.paddle_rect.x,lower_paddle.paddle_rect.y-30)) 
    window.blit(upper_paddle.paddle_img, (upper_paddle.paddle_rect.x,upper_paddle.paddle_rect.y-30))

    #Draw the middle line
    pg.draw.line(window, WHITE, (0, screen_height//2), (screen_width, screen_height//2))

    
    player_left_score_text = upper_player_score_font.render(f"{upper_player_score}", 1, WHITE)
    player_right_score_text = lower_player_score_font.render(f"{lower_player_score}", 1, WHITE)
    
    window.blit(player_left_score_text, (20, 20))
    window.blit(player_right_score_text, (20, 680))

    
    winner_text = winner_font.render(f"{winner}", 1, WHITE)
    if winner != None:
        window.blit(winner_text, (screen_width//2 - winner_text.get_width()//2, screen_height//2 - winner_text.get_height()//2))
        
    pg.display.update()
    
    

def reset_game(ball: Ball, lower_paddle: Paddle, upper_paddle: Paddle, upper_player_score: int, lower_player_score: int):
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
    
    return ball.ball_rect.x, ball.ball_rect.y, lower_paddle.paddle_rect.x, lower_paddle.paddle_rect.y, upper_paddle.paddle_rect.x, upper_paddle.paddle_rect.y, upper_player_score, lower_player_score, game_over, winner
    


def main(upper_player_score, lower_player_score):

    #Making ball and paddle instances
    ball = Ball(screen_middle[0], screen_middle[1], 5)
    upper_paddle = Paddle(x=paddle_xpos, y=upper_paddle_ypos, velocity=10, identity='upper')
    lower_paddle = Paddle(x=paddle_xpos, y=lower_paddle_ypos, velocity=10, identity='lower')
    
    #Game's statuses
    is_updating = False
    game_over = False
    run = True
    
    clock = pg.time.Clock()
    
    #Game loop
    while run:
        clock.tick(fps) #Setting the fps

        
        for event in pg.event.get():
            #Quit the game if you press 'X'
            if event.type == pg.QUIT:
                run = False

            #To start the game, you need to press 'ENTER"
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    is_updating = True
     
        
        if is_updating == True and game_over == False:
            
            key_pressed = pg.key.get_pressed()
            
            upper_paddle.update(key_pressed, ball)
            lower_paddle.update(key_pressed, ball)
            
            upper_player_score, lower_player_score = ball.update(upper_player_score, lower_player_score)
            
            #Win conditions
            if upper_player_score == 5:
                winner = "Left Player Wins"
                is_updating = False
                game_over = True
                
            elif lower_player_score == 5:
                winner = 'Right Player Wins'
                is_updating = False
                game_over = True

            #Reset game variables
            if game_over == True:
                ball.ball_rect.x, ball.ball_rect.y, lower_paddle.paddle_rect.x,lower_paddle.paddle_rect.y,upper_paddle.paddle_rect.x, upper_paddle.paddle_rect.y, upper_player_score, lower_player_score, game_over, winner = reset_game(ball, upper_paddle, lower_paddle, upper_player_score,lower_player_score)
            
            
        draw_on_window(window, ball, upper_paddle, lower_paddle, upper_player_score, lower_player_score)
        


if __name__ == '__main__':
    main(upper_player_score, lower_player_score)

pg.quit()
