import pygame
import sys
import time


class Player:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def constraint(self):
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x + self.rect.w > win_width:
            self.rect.x = win_width - self.rect.w

    def show(self):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, white, self.rect, 1)


class Brick:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color
        self.health = 100

    def show(self):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, white, self.rect, 1)


class Ball:
    def __init__(self, x, y, rad, color):
        self.x = x
        self.y = y
        self.rad = rad
        self.color = color
        self.isMoving = False
        self.speed = 10
        self.xspeed = -1 * self.speed
        self.yspeed = -1 * self.speed
        self.damage = 10

    def constraint(self):
        if self.x - self.rad < 0 or self.x + self.rad > win_width:
            self.xspeed = -1 * self.xspeed
        if self.y - self.rad < 0:
            self.yspeed = -1 * self.yspeed

    def show(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.rad)
        pygame.draw.circle(win, white, (self.x, self.y), self.rad, 1)


black = (0, 0, 0)
green = (51, 204, 89)
red = (250, 51, 51)
white = (255, 255, 255)
blue = (0, 0, 255)


def text(msg, coords, size=200, color=white):
    win.blit(pygame.font.SysFont(
        None, size).render(msg, True, color), coords)
    pygame.display.update()


def main():
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                ball.isMoving = True
                balls.append(Ball(player.rect.x + player.rect.w //
                                  3, ball_y, ball_rad, blue))
        win.fill(black)
        player.show()
        for ball in balls:
            if ball.y - ball.rad > win_height + 50:
                balls.remove(ball)
            else:
                if player.rect.collidepoint((ball.x, ball.y+ball.rad)):
                    dir = (ball.x - player.rect.x)/player.rect.w
                    ball.xspeed = int(2*(dir - 0.5) * ball.speed)
                    ball.yspeed = -int(2*min(1-dir, dir) * ball.speed)
                    if not ball.yspeed:
                        ball.yspeed = -1
                ball.constraint()
                ball.show()
                if ball.isMoving:
                    ball.x += ball.xspeed
                    ball.y += ball.yspeed
                else:
                    ball.x = player.rect.x + player.rect.w//3
        for brick in bricks:
            if brick.health <= 0:
                bricks.remove(brick)
            else:
                brick.show()
                for ball in balls:
                    if brick.rect.collidepoint((ball.x, ball.y+ball.rad)) or brick.rect.collidepoint((ball.x, ball.y-ball.rad)):
                        ball.yspeed = -1 * ball.yspeed
                        brick.health -= ball.damage
                        score += ball.damage
                    if brick.rect.collidepoint((ball.x+ball.rad, ball.y)) or brick.rect.collidepoint((ball.x-ball.rad, ball.y)):
                        ball.xspeed = -1 * ball.xspeed
                        brick.health -= ball.damage
                        score += ball.damage
        mx, my = pygame.mouse.get_pos()
        player.rect = pygame.Rect(mx-player_width//2, win_height -
                                  player_height-player_bottom_margin, player_width, player_height)
        player.constraint()
        if not balls:
            text("YOU LOST!", [100, 200])
            time.sleep(3)
            pygame.quit()
            sys.exit()
        elif not bricks:
            text("YOU WON!", [100, 200])
            time.sleep(3)
            pygame.quit()
            sys.exit()
        text("Score: "+str(score), (10, 10), 30)
        Clock.tick(fps)
        pygame.display.update()


pygame.init()
win_width = 1000
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Brick Breaker")

Clock = pygame.time.Clock()
fps = 60


# player settings
player_height = 20
player_width = 150
player_bottom_margin = 10
player_rect = pygame.Rect((win_width-player_width)//2, win_height -
                          player_height-player_bottom_margin, player_width, player_height)
player = Player(player_rect, red)


# brick settings
brick_row = 9
brick_column = 18
brick_width = 50
brick_height = 50
brick_top_margin = 50
brick_side_margin = 50


bricks = []
for i in range(brick_column):
    for j in range(brick_row):
        rect = pygame.Rect(brick_side_margin+brick_width*i, brick_top_margin +
                           brick_height*j, brick_width, brick_height)
        brick = Brick(rect, green)
        bricks.append(brick)


# ball settings
ball_rad = 10
ball_x = win_width//2
ball_y = win_height - player_bottom_margin - player_height - ball_rad
balls = [Ball(ball_x, ball_y, ball_rad, blue)]


main()
