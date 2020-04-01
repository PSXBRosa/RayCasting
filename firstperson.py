import numpy as np
import pygame
from objects import *

WIDTH = 640
HEIGHT = 360
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
	screen.fill((0,0,0))

	pl.enxergar(paredes)

	pygame.display.update()

