import pygame
import time
import numpy as np

pygame.init()
L = 500
x_max = 0.5
x_min = -2
y_max = 1.3
y_min = -1.3
x_range = x_max - x_min
y_range = y_max - y_min
length = L
breadth = int((L * y_range) / x_range)
iters = 100
blue_square = pygame.image.load('blue_square_tr1x1.png')

screen = pygame.display.set_mode((length, breadth))
pygame.display.set_caption("Mandlebrot")
running = True
count = 0
screen_color = (135, 206, 235)
set_color = (0, 0, 0)
mandlebrot_list = []

screen_grid_complex = np.zeros([length, breadth], dtype=complex)
for i in range(length):
    for j in range(breadth):
        z_x = (i / length) * (x_max - x_min) + x_min
        z_y = y_max - (j / breadth) * (y_max - y_min)
        screen_grid_complex[i][j] = z_x + (z_y * 1j)

while running:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
        elif events.type == pygame.KEYDOWN:
            if events.key == pygame.K_r:
                x_max = 0.5
                x_min = -2
                y_max = 1.3
                y_min = -1.3
                x_range = x_max - x_min
                y_range = y_max - y_min
            elif events.key == pygame.K_z:
                # print("B1 pressed!")
                t = pygame.mouse.get_pos()
                centre_x = (t[0] / length) * (x_max - x_min) + x_min
                centre_y = y_max - (t[1] / breadth) * (y_max - y_min)
                x_range /= 2
                y_range /= 2
                x_max = centre_x + (x_range / 2)
                x_min = centre_x - (x_range / 2)
                y_max = centre_y + (y_range / 2)
                y_min = centre_y - (y_range / 2)
            elif events.key == pygame.K_x:
                x_max += x_range/2
                x_min -= x_range/2
                y_max += y_range/2
                y_min -= y_range/2
                x_range *= 2
                y_range *= 2
            elif events.key == pygame.K_a:
                x_min -= x_range/10
                x_max -= x_range/10
            elif events.key == pygame.K_d:
                x_min += x_range/10
                x_max += x_range/10
            elif events.key == pygame.K_s:
                y_min -= y_range/10
                y_max -= y_range/10
            elif events.key == pygame.K_w:
                y_min += y_range/10
                y_max += y_range/10
            elif events.key == pygame.K_q:
                running = False
    screen_grid_complex = np.zeros([length, breadth], dtype=complex)
    for i in range(length):
        for j in range(breadth):
            z_x = (i / length) * (x_max - x_min) + x_min
            z_y = y_max - (j / breadth) * (y_max - y_min)
            screen_grid_complex[i][j] = z_x + (z_y * 1j)

    sgc = np.copy(screen_grid_complex)
    for i in range(iters):
        sgc = np.multiply(sgc, sgc) + screen_grid_complex
        sgc[np.absolute(sgc) > 2] = np.NaN

    screen.fill(screen_color)
    for i in range(length):
        for j in range(breadth):
            if not np.isnan(sgc[i][j]):
                pygame.draw.rect(screen, set_color, pygame.Rect(i, j, 1, 1))
    pygame.display.update()
