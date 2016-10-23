import pygame
import math
import ssl
import json
import random
from websocket import create_connection

class Ball():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xMove = 8
        self.yMove = 8

    def update(self, paddle1, paddle2):
        self.x += self.xMove
        self.y += self.yMove
        if self.y < 0 or self.y > 720:
            self.yMove *= -1
        if self.x >= 10 and self.x <= 20 and self.y <= (paddle1[1] + 180) and self.y >= paddle1[1]:
            self.xMove *= 2
            self.yMove *= 2
            self.xMove *= -1
        elif self.x >= 1250 and self.x <= 1260 and self.y <= (paddle2[1] + 180) and self.y >= paddle2[1]:
            self.xMove *= 2
            self.yMove *= 2
            self.xMove *= -1

        return (self.x, self.y)

    def reset():
        if self.x < 0 or self.x > 1280:
            self.x = 640
            self.y = 360
            self.xMove = 8
            self.yMove = 8
            return True
        return False

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
    ws = create_connection("ws://localhost:5000/", sslopt={"cert_reqs": ssl.CERT_NONE})
    screen = pygame.display.set_mode((1280, 720))
    done = False
    x = 10
    y = 10
    ball = Ball(640, 360)
    paddle = Paddle(x, y)
    paddle2 = Paddle(1250, 10)
    clock = pygame.time.Clock()
    paddle_coords2 = (1250, 10)

    while not done:
        screen.fill((0, 0, 0))
        paddle_coords = paddle.update()


        temp = json.dumps({"paddleX": paddle_coords[0],
                            "paddleY": paddle_coords[1],
                            "value": random.random()})
        ws.send(temp)
        result = ws.recv()
        if temp == result:
            coords = json.loads(result)
            paddle_coords2 = paddle2.updateRemote(1250, coords['paddleY'])
        ball_coords = ball.update(paddle_coords, paddle_coords2)
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(paddle_coords[0], paddle_coords[1] , 20, 180))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(paddle_coords2[0], paddle_coords2[1] , 20, 180))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(ball_coords[0], ball_coords[1], 20, 20))
        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
