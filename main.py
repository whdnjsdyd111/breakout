import random

import pygame
from pygame import Rect

WIDTH = 480
HEIGHT = 360
RECT_WIDTH = 40
RECT_HEIGHT = 15
PLAYER_WIDTH = 60
PLAYER_HEIGHT = 10
BALL_X = WIDTH / 2
BALL_Y = HEIGHT / 2 + 50
BALL_RADIUS = 5
PLAYER_X = WIDTH / 2 - PLAYER_WIDTH / 2
PLAYER_Y = HEIGHT - 10
SPEED = 0.125

KEYS = [-0.25, 0.25]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

PLAYING = 1
STARTING = 0
END = -1

COLOR_LIST = [WHITE, BLUE, GREEN, RED]


class Brick(Rect):
    def __init__(self, xPos, yPos):
        Rect.__init__(self, xPos + 1, yPos + 1, RECT_WIDTH - 1, RECT_HEIGHT - 1)
        self.color = COLOR_LIST[random.randint(0, len(COLOR_LIST) - 1)]


class Player(Rect):
    def __init__(self):
        Rect.__init__(self, PLAYER_X, PLAYER_Y, PLAYER_WIDTH, PLAYER_HEIGHT)


def ball_direct(directX, directY):
    nextX = BALL_X + directX
    nextY = BALL_Y + directY
    get_brick = None
    for brick in bricks:
        if brick.left <= nextX <= brick.right:
            if brick.top <= BALL_Y <= brick.bottom:
                directX *= -1
                get_brick = brick
        if brick.top <= nextY <= brick.bottom:
            if brick.left <= BALL_X <= brick.right:
                directY *= -1
                get_brick = brick
    if get_brick is not None:
        bricks.remove(get_brick)
    if player.left <= nextX <= player.right:
        if player.top <= BALL_Y <= player.bottom:
            directX *= -1
    if player.top <= nextY <= player.bottom:
        if player.left <= BALL_X <= player.right:
            directY *= -1
    if 0 >= nextX or nextX >= WIDTH:
        directX *= -1
    if 0 >= nextY or nextY >= HEIGHT:
        directY *= -1
    return directX, directY


bricks = []
player = Player()


for i in range(1, int(HEIGHT / 2 / RECT_HEIGHT) - 1):   # 벽돌 초기화
    for j in range(1, int(WIDTH / RECT_WIDTH) - 1):
        bricks.append(Brick(j * RECT_WIDTH, i * RECT_HEIGHT - 1))


def main():
    global BALL_X, BALL_Y, PLAYER_X, PLAYER_Y
    direct = -1  # -1 은 제자리, 0은 왼쪽, 1은 오른쪽
    is_two_keys = 0  # 키 두개 누른 상태면 1 아니면 0
    game_flag = 0
    game_count = 3
    directX = 1
    directY = 1

    pygame.init()
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("벽돌깨기")
    font = pygame.font.Font(None, 25)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    ball = dict(surface=screen, color=WHITE, center=(BALL_X, BALL_Y), radius=BALL_RADIUS)

    # 메인 루프를 제어할 변수 정의
    running = True

    # 메인 루프
    while running:
        # 이벤트 핸들러, 이벤트 큐로부터 모든 이벤트를 얻는다.
        for event in pygame.event.get():
            # QUIT 타입의 이벤트라면 다음 코딩을 실행
            if event.type == pygame.QUIT:
                # 메인 루프를 탈출하기 위해 변수를 False 로 바꾼다.
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if direct == 0:
                        is_two_keys = 1
                    direct = 1
                if event.key == pygame.K_LEFT:
                    if direct == 1:
                        is_two_keys = 1
                    direct = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    if is_two_keys == 1:
                        is_two_keys = 0
                        direct = 1
                    else:
                        direct = -1
                elif event.key == pygame.K_RIGHT:
                    if is_two_keys == 1:
                        is_two_keys = 0
                        direct = 0
                    else:
                        direct = -1

        screen.fill(BLACK)
        if direct >= 0:
            if player.left + KEYS[direct] > 0 and player.right + KEYS[direct] < WIDTH:
                PLAYER_X += KEYS[direct]
                player.center = (PLAYER_X, PLAYER_Y)
        for r in bricks:
            pygame.draw.rect(screen, r.color, r)
        if game_flag == 0:
            screen.blit(font.render(str(game_count), False, (255, 255, 255)), (WIDTH / 2 - 5, HEIGHT / 2))
            game_count -= 1
            if game_count == -1:
                game_flag = 1
            pygame.time.wait(1000)
        elif game_flag == 1:
            directX, directY = ball_direct(directX, directY)
            BALL_X += SPEED * directX
            BALL_Y += SPEED * directY
            ball['center'] = (BALL_X, BALL_Y)

        pygame.draw.circle(**ball)
        pygame.draw.rect(screen, WHITE, player)
        pygame.display.flip()


if __name__ == "__main__":
    # call the main function
    main()
