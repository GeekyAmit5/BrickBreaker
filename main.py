import pygame


class Brick:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def show(self):
        pygame.draw.rect(win, self.color, self.rect)
        pygame.draw.rect(win, white, self.rect, 1)


class Player:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def constraint(self):
        if self.rect.x + self.rect.w > win_width:
            self.rect.x = win_width - self.rect.w
        elif self.rect.x < 0:
            self.rect.x = 0

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
        self.speed = 8
        self.xspeed = -1 * self.speed
        self.yspeed = -1*self.speed

    def constraint(self):
        if self.x - self.rad < 0:
            self.xspeed = -1 * self.xspeed
        elif self.x + self.rad > win_width:
            self.xspeed = -1 * self.xspeed

        if self.y - self.rad < 0:
            self.yspeed = -1 * self.yspeed
        elif player.rect.collidepoint((self.x, self.y+self.rad)):
            dir = (self.x - player.rect.x)/player.rect.w
            self.xspeed = int(2*(dir - 0.5) * self.speed)
            if dir > 0.5:
                self.yspeed = -int((1.5-dir) * self.speed)
            else:
                self.yspeed = -int((dir+0.5) * self.speed)

    def show(self):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.rad)
        pygame.draw.circle(win, white, (self.x, self.y), self.rad, 1)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                ball.isMoving = True
        win.fill(black)
        player.show()
        ball.show()
        for brick in bricks:
            brick.show()
            if brick.rect.collidepoint((ball.x, ball.y)):
                sum = 0
                if brick.rect.collidepoint((ball.x+ball.rad, ball.y)):
                    sum += 1
                if brick.rect.collidepoint((ball.x-ball.rad, ball.y)):
                    sum += 1
                if sum != 1:
                    ball.yspeed = -1 * ball.yspeed
                else:
                    ball.xspeed = -1 * ball.xspeed
                bricks.remove(brick)

        mx, my = pygame.mouse.get_pos()
        player.rect = pygame.Rect(mx-player_width//2, win_height -
                                  player_height-player_bottom_margin, player_width, player_height)
        if ball.isMoving:
            ball.x += ball.xspeed
            ball.y += ball.yspeed
        player.constraint()
        ball.constraint()
        # if ball.y - ball.rad > win_height:
        #     font = pygame.font.Font(None, 50)
        #     win.blit(font.render(True, white))
        Clock.tick(fps)
        pygame.display.update()


pygame.init()
win_width = 1000
win_height = 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Brick Breaker")

Clock = pygame.time.Clock()
fps = 60

black = (0, 0, 0)
green = (51, 204, 89)
red = (250, 51, 51)
white = (255, 255, 255)
blue = (0, 0, 255)


# brick settings
brick_row = 9
brick_column = 9
brick_width = 100
brick_height = 20
brick_top_margin = 50
brick_side_margin = 50


bricks = []
for i in range(brick_column):
    for j in range(brick_row):
        if i % 2:
            continue
        rect = pygame.Rect(brick_side_margin+brick_width*i, brick_top_margin +
                           brick_height*j, brick_width, brick_height)
        brick = Brick(rect, green)
        bricks.append(brick)


# player settings
player_height = 20
player_width = 150
player_bottom_margin = 10
player = Player(((win_width-player_width)//2, win_height -
                 player_height-player_bottom_margin, player_width, player_height), red)


# ball settings
ball_rad = 10
ball_x = win_width//2
ball_y = win_height - player_bottom_margin - player_height - ball_rad
ball = Ball(ball_x, ball_y, ball_rad, blue)


main()
