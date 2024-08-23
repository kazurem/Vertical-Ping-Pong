#Ping Pong Game
import pygame as pg
import time

pg.init()
pg.font.init()


screen_width = 800
screen_height = 500
window = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption('Ping Pong')

fps = 60

WHITE = (255,255,255)
BLACK = (0,0,0)

ball_width = 20
ball_height = 20

screen_middle = (screen_width//2-ball_width//2, screen_height//2 - ball_height//2)

paddle_width = 20
paddle_height = 100

player_left_score = 0
player_right_score = 0

player_left_score_font = pg.font.SysFont('comicsans', 50)
player_right_score_font = pg.font.SysFont('comicsans', 50)
winner_font = pg.font.SysFont('comicsans', 70)



class Ball(pg.sprite.Sprite):
    
    def __init__(self, x: int, y: int,  velocity_x=5, velocity_y=5):
        pg.sprite.Sprite.__init__(self)
        
        self.velocity = [velocity_x, velocity_y] # x and y velocities are the same
        
        self.ball_surface = pg.Surface((ball_width, ball_height))
        self.ball_surface.fill(WHITE)
        self.ball_rect = self.ball_surface.get_rect(topleft=(x, y))
        
        
    def update(self, player_left_score: int, player_right_score: int):
        #Update the ball's x and y coordinates
        self.ball_rect.x += self.velocity[0]
        self.ball_rect.y += self.velocity[1]

        #ball crosses the right boundary of the window
        if self.ball_rect.right >= screen_width:
            player_left_score += 1
            self.ball_rect.x = screen_middle[0]
            self.ball_rect.y = screen_middle[1]
            
        #ball crosses the right boundary of the window
        elif self.ball_rect.left <= 0:
            player_right_score += 1
            self.ball_rect.x = screen_middle[0]
            self.ball_rect.y = screen_middle[1]
            
        #ball crosses the upper boundary of the window
        elif self.ball_rect.top <= 0:
            self.velocity[1] = -self.velocity[1]

        #ball crosses the lower boundary of the window
        elif self.ball_rect.bottom >= screen_height:
            self.velocity[1] = -self.velocity[1]
            
        return player_left_score, player_right_score
        
        
        
        
class Paddle(pg.sprite.Sprite):
    
    def __init__(self, x: int, y: int, velocity: int, identity: str):
        pg.sprite.Sprite.__init__(self)
        
        self.velocity = velocity
        self.identity = identity #left paddle or right paddle
        
        self.paddle_surface = pg.Surface((paddle_width, paddle_height))
        self.paddle_surface.fill(WHITE)
        self.paddle_rect = self.paddle_surface.get_rect(topleft=(x, y))
        
        
    def update(self, key_pressed, ball: Ball):

        #For left paddle
        if key_pressed[pg.K_w] and self.paddle_rect.top > 0 and self.identity == 'left':
            self.paddle_rect.y -= self.velocity
            
        elif key_pressed[pg.K_s] and self.paddle_rect.bottom < screen_height and self.identity == 'left':
            self.paddle_rect.y += self.velocity

        #For right paddle
        elif key_pressed[pg.K_UP] and self.paddle_rect.top > 0 and self.identity == 'right':
            self.paddle_rect.y -= self.velocity
            
        
        elif key_pressed[pg.K_DOWN] and self.paddle_rect.bottom < screen_height and self.identity == 'right':
            self.paddle_rect.y += self.velocity
            
            
        #Collision of ball with the paddle
        if self.paddle_rect.colliderect(ball.ball_rect):
            ball.velocity[0] = -ball.velocity[0]
            

            
            

def draw_on_window(window, ball: Ball, paddle_left: Paddle, paddle_right: Paddle, player_left_score: int, player_right_score: int, winner=None,time_sleep=0):
    
    #To refresh the display each loop
    window.fill(BLACK)

    #Drawing the ball and paddles
    window.blit(ball.ball_surface, (ball.ball_rect.x, ball.ball_rect.y))
    window.blit(paddle_left.paddle_surface, (paddle_left.paddle_rect.x,paddle_left.paddle_rect.y))
    window.blit(paddle_right.paddle_surface, (paddle_right.paddle_rect.x,paddle_right.paddle_rect.y))

    #Draw the middle line
    pg.draw.line(window, WHITE, (screen_width//2, 0), (screen_width//2, screen_height))

    
    player_left_score_text = player_left_score_font.render(f"{player_left_score}", 1, WHITE)
    player_right_score_text = player_right_score_font.render(f"{player_right_score}", 1, WHITE)
    
    window.blit(player_left_score_text, (80, 20))
    window.blit(player_right_score_text, (720, 20))

    
    winner_text = winner_font.render(f"{winner}", 1, WHITE)
    if winner != None:
        window.blit(winner_text, (screen_width//2 - winner_text.get_width()//2, screen_height//2 - winner_text.get_height()//2))
        
    pg.display.update()
    
    

def reset_game(ball: Ball, paddle_left: Paddle, paddle_right: Paddle, player_left_score: int, player_right_score: int):
    ball.ball_rect.x = screen_middle[0]
    ball.ball_rect.y = screen_middle[1]
    
    paddle_left.paddle_rect.x = 50
    paddle_left.paddle_rect.y = screen_height//2-paddle_height//2
    paddle_right.paddle_rect.x = 750
    paddle_right.paddle_rect.y = screen_height//2-paddle_height//2
    
    player_left_score = 0
    player_right_score = 0
    
    game_over = False
    winner = None
    
    return ball.ball_rect.x, ball.ball_rect.y, paddle_left.paddle_rect.x, paddle_left.paddle_rect.y, paddle_right.paddle_rect.x, paddle_right.paddle_rect.y, player_left_score, player_right_score, game_over, winner
    


def main(player_left_score, player_right_score):

    #Making ball and paddle instances
    ball = Ball(screen_width//2-ball_width//2, screen_height//2-ball_height//2, 5)
    paddle_left = Paddle(50, screen_height//2-paddle_height//2, 10, 'left')
    paddle_right = Paddle(750, screen_height//2-paddle_height//2, 10, 'right')
    
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
            
            paddle_left.update(key_pressed, ball)
            paddle_right.update(key_pressed, ball)
            
            player_left_score, player_right_score = ball.update(player_left_score, player_right_score)
            
            #Win conditions
            if player_left_score == 5:
                winner = "Left Player Wins"
                is_updating = False
                game_over = True
                
            elif player_right_score == 5:
                winner = 'Right Player Wins'
                is_updating = False
                game_over = True

            #Reset game variables
            if game_over == True:
                ball.ball_rect.x, ball.ball_rect.y, paddle_left.paddle_rect.x,paddle_left.paddle_rect.y,paddle_right.paddle_rect.x, paddle_right.paddle_rect.y, player_left_score, player_right_score, game_over, winner = reset_game(ball, paddle_left, paddle_right, player_left_score,player_right_score)
            
            
        draw_on_window(window, ball, paddle_left, paddle_right, player_left_score, player_right_score)
        



if __name__ == '__main__':
    main(player_left_score, player_right_score)

pg.quit()
