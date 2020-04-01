import pygame
import numpy as np
from objects import *

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))

pl = Player(WIDTH/2, HEIGHT/2, 45, screen)
w, h = pygame.display.get_surface().get_size()
paredes = criar_paredes(5, 300, 450)
paredes += [Wall(0,0,0,h),Wall(0,0,w,0),Wall(w,0,w,h),Wall(0,h,w,h)]


running = True
while running:
	raios = pl.relampiar()
	pl.move()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4:
				theta0 += 30
				theta1 += 30
			if event.button == 5:
				theta0 -= 30
				theta1 -= 30
	screen.fill((0,0,0))
	
	for raio in raios:
		raio.show(screen, paredes)
	pygame.draw.circle(screen, (255, 253, 162),
		(int(pl.x), int(pl.y)), 10)
	for parede in paredes:
		parede.show(screen)
	pygame.display.update()