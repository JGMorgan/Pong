import pygame
import math
import ssl
import json
import random
from websocket import create_connection

class Ball():
    def __init__(self, x, y, x_0, y_0):
        self.x = x
        self.y = y
        self.xMove = x_0
        self.yMove = y_0

    def update(self, paddle1, paddle2):
        self.x += self.xMove
        self.y += self.yMove
        if self.y < 0 or self.y > 720:
            self.yMove *= -1
        if self.x >= 10 and self.x <= 20 and self.y <= (paddle1[1] + 180) and self.y >= paddle1[1]:
            self.xMove = int(self.xMove * 1.2)
            self.yMove = int(self.yMove * 1.2)
            self.xMove *= -1
        elif self.x >= 1250 and self.x <= 1260 and self.y <= (paddle2[1] + 180) and self.y >= paddle2[1]:
            self.xMove = int(self.xMove * 1.2)
            self.yMove = int(self.yMove * 1.2)
            self.xMove *= -1

        return (self.x, self.y)

    def reset(self, score1, score2):
        if self.x < 0 or self.x > 1280:
            if (self.x < 0):
                score2 += 1
            if (self.x > 1280):
                score1 += 1
            self.x = 640
            self.y = 360
            self.xMove = 8
            self.yMove = 8
            return (score1, score2)
        return (score1, score2)

class Paddle():
    x = 10
    y = 10
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            pressed = pygame.key.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            self.y = mouse_pos[1] - 90
        return (self.x, self.y)

    def updateRemote(self, x, y):
        self.x = x
        self.y = y
        return (self.x, self.y)


def main():
    pygame.init()
    #ws = create_connection("ws://localhost:5000/", sslopt={"cert_reqs": ssl.CERT_NONE})
    ws = create_connection("ws://54.200.200.83:5000/", sslopt={"cert_reqs": ssl.CERT_NONE})
    screen = pygame.display.set_mode((1280, 720))
    myfont = pygame.font.Font(None, 72)
    done = False
    x = 10
    y = 10
    score1 = 0;
    score2 = 0;
    balls = []
    balls.append(Ball(640, 360, 8, 8))
    balls.append(Ball(640, 360, -8, -8))
    balls.append(Ball(640, 360, 23, -8))
    balls.append(Ball(640, 360, 18, 3))
    balls.append(Ball(640, 360, -76, 7))
    balls.append(Ball(640, 360, -1, -1))
    balls.append(Ball(640, 360, -2, 8))
    balls.append(Ball(640, 360, -98, 8))

    ball1 = balls[0]
    paddle = Paddle(x, y)
    paddle2 = Paddle(1250, 10)
    clock = pygame.time.Clock()
    paddle_coords2 = (1250, 10)
    value = random.random()
    tick = 0
    while not done:
        tick += 1
        screen.fill((0x27, 0x2B, 0x33))
        paddle_coords = paddle.update()

        temp = json.dumps({"paddleX": paddle_coords[0],
                            "paddleY": paddle_coords[1],
                            "value": value})

        newscores = ball1.reset(score1, score2)
        score1 = newscores[0]
        score2 = newscores[1]

        for i in xrange(1, len(balls)):
            ball = balls[i]
            if((score1 > i*2) or (score2 > i*2)):
                newscores = ball.reset(score1, score2)
                score1 = newscores[0]
                score2 = newscores[1]


        ws.send(temp)
        tick = 0

        result = ws.recv()
        coords = json.loads(result)
        if value != coords['value']:
            coords = json.loads(result)
            print coords['paddleY']
            paddle_coords2 = paddle2.updateRemote(1250, coords['paddleY'])

        ball1_coords = ball1.update(paddle_coords, paddle_coords2)

        balls_coords = []
        balls_coords.append(ball1_coords)
        for i in xrange(1, len(balls)):
            ball = balls[i]
            if((score1 > i*2) or (score2 > i*2)):
                balls_coords.append(ball.update(paddle_coords, paddle_coords2))

        # ball_coords = ball2.update(paddle_coords, paddle_coords2)
        pygame.draw.rect(screen, (0x87, 0xC0, 0x78), pygame.Rect(paddle_coords[0], paddle_coords[1] , 20, 180))
        pygame.draw.rect(screen, (0x87, 0xC0, 0x78), pygame.Rect(paddle_coords2[0], paddle_coords2[1] , 20, 180))

        pygame.draw.rect(screen, (0xF4, 0x43, 0x36), pygame.Rect(ball1_coords[0], ball1_coords[1], 20, 20))

        # if(score1 > 4 or score2 > 4):
        #     pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(ball2_coords[0], ball2_coords[1], 20, 20))
        for i in xrange(1, len(balls)):
            ball = balls[i]
            if((score1 > i*2) or (score2 > i*2)):
                balls_coords[i] = ball.update(paddle_coords, paddle_coords2)
                pygame.draw.rect(screen, (0xF4, 0x43, 0x36), pygame.Rect(balls_coords[i][0], balls_coords[i][1], 20, 20))

        scoretext = myfont.render("{0}   {1}".format(score1, score2), 1, (0xE5, 0xC1, 0x7C))
        screen.blit(scoretext, (1280/2 - 50, 25))

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
