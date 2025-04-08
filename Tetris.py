import pygame
import time
import numpy as np


class Tetromino:

    def __init__(self, shape):
        self.shape = shape
        if shape == 1:  # straight piece
            self.stretch = [(3, 0), (4, 0), (5, 0), (6, 0)]
            self.pivot = (4.5, 0.5)
        if shape == 2:  # square piece
            self.stretch = [(4, 0), (5, 0), (4, 1), (5, 1)]
            self.pivot = (4.5, 0.5)
        if shape == 3:  # Z piece
            self.stretch = [(4, 0), (5, 0), (5, 1), (6, 1)]
            self.pivot = (5, 0)
        if shape == 4:  # S piece
            self.stretch = [(4, 1), (5, 0), (5, 1), (6, 0)]
            self.pivot = (5, 0)
        if shape == 5:  # J piece
            self.stretch = [(4, 0), (5, 0), (6, 0), (6, 1)]
            self.pivot = (5, 0)
        if shape == 6:  # L piece
            self.stretch = [(4, 0), (5, 0), (6, 0), (4, 1)]
            self.pivot = (5, 0)
        if shape == 7:  # T piece
            self.stretch = [(4, 0), (5, 0), (6, 0), (5, 1)]
            self.pivot = (5, 0)

    def goDown(self):
        i = 0
        for (x, y) in self.stretch:
            self.stretch[i] = (x, y + 1)
            i += 1
        (x, y) = self.pivot
        self.pivot = (x, y + 1)

    def goUp(self):
        i = 0
        for (x, y) in self.stretch:
            self.stretch[i] = (x, y - 1)
            i += 1
        (x, y) = self.pivot
        self.pivot = (x, y - 1)

    def goLeft(self):
        i = 0
        for (x, y) in self.stretch:
            self.stretch[i] = (x - 1, y)
            i += 1
        (x, y) = self.pivot
        self.pivot = (x - 1, y)

    def goRight(self):
        i = 0
        for (x, y) in self.stretch:
            self.stretch[i] = (x + 1, y)
            i += 1
        (x, y) = self.pivot
        self.pivot = (x + 1, y)

    def rotate(self):
        for i in range(len(self.stretch)):
            (x, y) = self.stretch[i]
            p = self.pivot[0] + self.pivot[1] - y
            q = x + self.pivot[1] - self.pivot[0]
            self.stretch[i] = (p, q)

    def antiRotate(self):
        for i in range(len(self.stretch)):
            (x, y) = self.stretch[i]
            p = self.pivot[0] + y - self.pivot[1]
            q = self.pivot[1] - x + self.pivot[0]
            self.stretch[i] = (p, q)

    def checkBounds(self, boundary):
        for (x, y) in self.stretch:
            if (x, y) in boundary:
                return True
        return False


m = 1


def moveTupleDown(w):
    return w[0], w[1] + 1


def last(n):
    return n[m]

blockSize = 23
hor_d = 10
ver_d = 22
next_block = np.random.randint(7) + 1
length = blockSize * ver_d
breadth = blockSize * (hor_d + 9)
pygame.init()
screen = pygame.display.set_mode((breadth, length))
screen_color = (220, 220, 200)
pygame.display.set_caption("Tetris")
font = pygame.font.Font('8-bit-hud.ttf', 17)
title = font.render("TETRIS", True, (0, 0, 0))
screen.blit(title, (11 * blockSize, 1 * blockSize))
font = pygame.font.Font('8-bit-hud.ttf', 13)
controls = font.render("Controls:", True, (0, 0, 0))

font = pygame.font.Font('8-bit-hud.ttf', 10)
line1 = font.render(">MOVEMENT", True, (0, 0, 0))
line2 = font.render("  -arrow keys", True, (0, 0, 0))
line3 = font.render(">ROTATE", True, (0, 0, 0))
line4 = font.render("  -r/t", True, (0, 0, 0))
line5 = font.render(">PAUSE GAME", True, (0, 0, 0))
line6 = font.render("  -p", True, (0, 0, 0))
line7 = font.render(">RESTART GAME", True, (0, 0, 0))
line8 = font.render("  -spacebar", True, (0, 0, 0))
line9 = font.render(">QUIT GAME", True, (0, 0, 0))
line10 = font.render("  -q", True, (0, 0, 0))

font = pygame.font.Font('8-bit-hud.ttf', 17)

line_end1 = font.render("GAME OVER.", True, (0, 0, 0))

font = pygame.font.Font('8-bit-hud.ttf', 13)

line_end2 = font.render("Press spacebar to continue", True, (0, 0, 0))

running = True
m_index = 0
new_block_flag = True
bounds_lower = []
bounds_left = []
bounds_right = []

time_count = 0
down_count = 100
input_count = 140
pause_flag = False
game_over_flag = False

color_dict = {1: [(0, 255, 255), (100, 255, 255)],
              2: [(255, 255, 0), (255, 255, 100)],
              3: [(255, 0, 0), (255, 100, 100)],
              4: [(0, 255, 0), (100, 255, 100)],
              5: [(0, 0, 255), (100, 100, 255)],
              6: [(255, 255, 0), (255, 255, 100)],
              7: [(255, 0, 255), (255, 100, 255)]}

right_flag = False
left_flag = False

for j in range(hor_d + 2):
    bounds_lower.append((j - 1, ver_d))

for j in range(ver_d):
    bounds_left.append((-1, j))
    bounds_right.append((hor_d, j))

bounds_orig = bounds_lower.copy()

while running:
    screen.fill(screen_color)
    pygame.draw.rect(screen, (0, 0, 0),
                     pygame.Rect(blockSize * (hor_d + 1), blockSize * 3, 6 * blockSize, 4 * blockSize))

    for x_pos in range(hor_d):
        for y_pos in range(ver_d):
            if (x_pos, y_pos) in bounds_lower:
                pygame.draw.rect(screen, (0, 0, 0),
                                 pygame.Rect(blockSize * x_pos, blockSize * y_pos, blockSize, blockSize))
                pygame.draw.rect(screen, (135, 206, 235),
                                 pygame.Rect(blockSize * x_pos + 2, blockSize * y_pos + 2, blockSize - 4,
                                             blockSize - 4))
                pygame.draw.rect(screen, (0, 0, 0),
                                 pygame.Rect(blockSize * x_pos + 4, blockSize * y_pos + 4, blockSize - 8,
                                             blockSize - 8))
                pygame.draw.rect(screen, (135, 206, 235),
                                 pygame.Rect(blockSize * x_pos + 6, blockSize * y_pos + 6, blockSize - 12,
                                             blockSize - 12))
                pygame.draw.rect(screen, (0, 0, 0),
                                 pygame.Rect(blockSize * x_pos + 8, blockSize * y_pos + 8, blockSize - 16,
                                             blockSize - 16))
            else:
                pygame.draw.rect(screen, (50, 50, 50),
                                 pygame.Rect(blockSize * x_pos, blockSize * y_pos, blockSize, blockSize))
                pygame.draw.rect(screen, (0, 0, 0),
                                 pygame.Rect(blockSize * x_pos + 3, blockSize * y_pos + 3, blockSize - 6,
                                             blockSize - 6))
    if new_block_flag:
        current_block = next_block
        a = Tetromino(current_block)
        next_block = np.random.randint(7) + 1
        b = Tetromino(next_block)
        # a = Tetromino(np.random.randint(7) + 1)
        # a = Tetromino(1)
        new_block_flag = False

    elif time_count % down_count == 10:
        a.goDown()
        if a.checkBounds(bounds_lower):
            a.goUp()
            for k in range(4):
                bounds_lower.append(a.stretch[k])
            if not game_over_flag:
                new_block_flag = True

    for k in range(4):
        (x_pos, y_pos) = b.stretch[k]
        if b.shape == 1:
            pygame.draw.rect(screen, color_dict[b.shape][0],
                             pygame.Rect(blockSize * (x_pos + hor_d - 1), blockSize * (y_pos + 4), blockSize,
                                         blockSize))
        if b.shape == 2:
            pygame.draw.rect(screen, color_dict[b.shape][0],
                             pygame.Rect(blockSize * (x_pos + hor_d - 1), blockSize * (y_pos + 4), blockSize,
                                         blockSize))
        if b.shape == 3:
            pygame.draw.rect(screen, color_dict[b.shape][0],
                             pygame.Rect(blockSize * (x_pos + hor_d - 1.5), blockSize * (y_pos + 4), blockSize,
                                         blockSize))
        if b.shape == 4:
            pygame.draw.rect(screen, color_dict[b.shape][0],
                             pygame.Rect(blockSize * (x_pos + hor_d - 1.5), blockSize * (y_pos + 4), blockSize,
                                         blockSize))
        if b.shape == 5:
            pygame.draw.rect(screen, color_dict[b.shape][0],
                             pygame.Rect(blockSize * (x_pos + hor_d - 1.5), blockSize * (y_pos + 4), blockSize,
                                         blockSize))
        if b.shape == 6:
            pygame.draw.rect(screen, color_dict[b.shape][0],
                             pygame.Rect(blockSize * (x_pos + hor_d - 1.5), blockSize * (y_pos + 4), blockSize,
                                         blockSize))
        if b.shape == 7:
            pygame.draw.rect(screen, color_dict[b.shape][0],
                             pygame.Rect(blockSize * (x_pos + hor_d - 1.5), blockSize * (y_pos + 4), blockSize,
                                         blockSize))

    k = 0
    while k < ver_d:
        row_filled_flag = True
        for l in range(hor_d):
            if (l, k) not in bounds_lower:
                row_filled_flag = False
                break
        if row_filled_flag:
            for l in range(hor_d):
                bounds_lower.remove((l, k))
            for l in range(len(bounds_lower)):
                if bounds_lower[l][1] < k:
                    bounds_lower[l] = moveTupleDown(bounds_lower[l])
        k += 1 - row_filled_flag

    bounds_lower.sort(key=last)
    tallness = bounds_lower[0][1]
    if tallness == 0:
        game_over_flag = True

    for k in range(4):
        (x_pos, y_pos) = a.stretch[k]
        pygame.draw.rect(screen, color_dict[a.shape][0],
                         pygame.Rect(blockSize * x_pos, blockSize * y_pos, blockSize, blockSize))
        pygame.draw.rect(screen, color_dict[a.shape][1],
                         pygame.Rect(blockSize * x_pos + 4, blockSize * y_pos + 4, blockSize - 8, blockSize - 8))
        # pygame.draw.rect(screen, (135, 206, 235),
        #                  pygame.Rect(blockSize * x_pos + 2, blockSize * y_pos + 2, blockSize - 4, blockSize - 4))
        # pygame.draw.rect(screen, (0, 0, 0),
        #                  pygame.Rect(blockSize * x_pos + 4, blockSize * y_pos + 4, blockSize - 8, blockSize - 8))
        # pygame.draw.rect(screen, (135, 206, 235),
        #                  pygame.Rect(blockSize * x_pos + 6, blockSize * y_pos + 6, blockSize - 12, blockSize - 12))
        # pygame.draw.rect(screen, (0, 0, 0),
        #                  pygame.Rect(blockSize * x_pos + 8, blockSize * y_pos + 8, blockSize - 16, blockSize - 16))

    if right_flag and time_count % input_count == 10:
        a.goRight()
        if a.checkBounds(bounds_right) or a.checkBounds(bounds_lower):
            a.goLeft()
    if left_flag and time_count % input_count == 10:
        a.goLeft()
        if a.checkBounds(bounds_left) or a.checkBounds(bounds_lower):
            a.goRight()

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_q:
                running = False
            if events.key == pygame.K_r:
                a.rotate()
                while a.checkBounds(bounds_left):
                    a.goRight()
                while a.checkBounds(bounds_right):
                    a.goLeft()
                if a.checkBounds(bounds_lower):
                    a.antiRotate()
            if events.key == pygame.K_t:
                a.antiRotate()
                while a.checkBounds(bounds_left):
                    a.goRight()
                while a.checkBounds(bounds_right):
                    a.goLeft()
                if a.checkBounds(bounds_lower):
                    a.rotate()
            if events.key == pygame.K_RIGHT:
                right_flag = True
                a.goRight()
                if a.checkBounds(bounds_right) or a.checkBounds(bounds_lower):
                    a.goLeft()
            if events.key == pygame.K_LEFT:
                left_flag = True
                a.goLeft()
                if a.checkBounds(bounds_left) or a.checkBounds(bounds_lower):
                    a.goRight()
            if events.key == pygame.K_DOWN:
                down_count -= 80
            if events.key == pygame.K_SPACE:
                bounds_lower = bounds_orig.copy()
                game_over_flag = False
                new_block_flag = True
                time.sleep(0.3)
            if events.key == pygame.K_p:
                pause_flag = not pause_flag
        if events.type == pygame.KEYUP:
            if events.key == pygame.K_RIGHT:
                right_flag = False
            if events.key == pygame.K_LEFT:
                left_flag = False
            if events.key == pygame.K_DOWN:
                down_count += 80
    if not pause_flag:
        time_count += 1
    if game_over_flag:
        time.sleep(0.5)
        screen.fill((255, 255, 255))
        screen.blit(line_end1, (breadth / 2 - 100, length / 2 - 50))
        screen.blit(line_end2, (breadth / 2 - 185, length / 2 - 10))
    else:
        screen.blit(title, (11 * blockSize, 1 * blockSize))
        screen.blit(controls, (11 * blockSize, 8 * blockSize))
        screen.blit(line1, (10.5 * blockSize, 9.5 * blockSize))
        screen.blit(line2, (10.5 * blockSize, 10.5 * blockSize))
        screen.blit(line3, (10.5 * blockSize, 12 * blockSize))
        screen.blit(line4, (10.5 * blockSize, 13 * blockSize))
        screen.blit(line5, (10.5 * blockSize, 14.5 * blockSize))
        screen.blit(line6, (10.5 * blockSize, 15.5 * blockSize))
        screen.blit(line7, (10.5 * blockSize, 17 * blockSize))
        screen.blit(line8, (10.5 * blockSize, 18 * blockSize))
        screen.blit(line9, (10.5 * blockSize, 19.5 * blockSize))
        screen.blit(line10, (10.5 * blockSize, 20.5 * blockSize))
    pygame.display.update()
    time_count = time_count % 100
