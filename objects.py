import pygame
import numpy as np

class Wall:
	def __init__(self, ax ,ay , bx, by):
		self.ax = ax
		self.ay = ay
		self.bx = bx
		self.by = by
		self.vec = (ax-bx, ay-by)/np.sqrt(np.square(ax-bx) + np.square(ay-by)) # A --> B

	def show(self, window):
		pygame.draw.line(window,
						(255,255,255),
						(self.ax,self.ay),
						(self.bx,self.by))


class Ray:
	def __init__(self, x, y, theta):
		self.x = x
		self.y = y
		self.theta = theta
		self.vector = (np.cos(np.radians(theta)), np.sin(np.radians(theta)))

	def collision(self, wall):
		mi_nominador = (wall.ax - self.x)*(self.vector[1]/self.vector[0]) - (wall.ay - self.y)
		mi_denominador = (wall.by - wall.ay) - (self.vector[1]/self.vector[0])*(wall.bx - wall.ax)
		if mi_denominador != 0:
			mi = mi_nominador/mi_denominador
		else: mi = np.inf

		lamb_nominador = (wall.by - wall.ay)*(wall.ax - self.x) - (wall.ay - self.y)*(wall.bx - wall.ax)
		lamb_denominador = self.vector[0]*(wall.by - wall.ay) - self.vector[1]*(wall.bx - wall.ax)
		if lamb_denominador != 0:
			lamb = lamb_nominador/lamb_denominador
		else: lamb = np.inf

		if lamb > 0 and mi >= 0 and mi <= 1:
			return (int(self.x + lamb*self.vector[0]), int(self.y + lamb*self.vector[1]))
		else:
			return None


	def show(self,window, paredes):
		colisao = []
		a = 0
		while a < len(paredes):
			colisao.append(self.collision(paredes[a]))
			a += 1
		if len(colisao) > 0:
			args = list(map(lambda x: np.sqrt((x[0]-self.x)**2 + (x[1]-self.y)**2) if type(x) == tuple else np.inf, colisao))
			i_mais_prox = np.argmin(args)
			mais_prox = colisao[i_mais_prox]
			pygame.draw.line(window,(255,255,255),
									(self.x, self.y),
									(mais_prox[0], mais_prox[1]))
		else:
			pass


class Player:
	def __init__(self, x, y, fov, display):
		self.x = x
		self.y = y
		self.thetac = 0
		self.fov = fov ## Field of view (degrees)
		self.raios = None
		self.display = display

	def relampiar(self):
		angulos = list(np.linspace(self.thetac - int(self.fov//2), self.thetac + int(self.fov//2), 2*self.fov))
		self.raios = [Ray(self.x, self.y, angulo) for angulo in angulos]
		return self.raios

	def move(self):
		w, h = pygame.display.get_surface().get_size()
		vvec = [np.cos(np.radians(self.raios[len(self.raios)//2].theta)),
				np.sin(np.radians(self.raios[len(self.raios)//2].theta))]
		vesq = list(np.cross([0,0,1] , vvec + [0]))[:-1]
		cheat = {pygame.K_a : lambda x: (x[0] + vesq[0],x[1] + vesq[1],x[2]),
				 pygame.K_w : lambda x: (x[0] + vvec[0],x[1] + vvec[1],x[2]),
				 pygame.K_d : lambda x: (x[0] - vesq[0],x[1] - vesq[1],x[2]),
				 pygame.K_s : lambda x: (x[0] - vvec[0],x[1] - vvec[1],x[2]),
				 pygame.K_q : lambda x: (x[0], x[1], x[2] + 0.5),
				 pygame.K_e : lambda x: (x[0], x[1], x[2] - 0.5)}

		pressed = pygame.key.get_pressed()
		for k in cheat.keys():
			if pressed[k]:
				self.x, self.y, self.thetac = cheat[k]((self.x, self.y, self.thetac))

	def enxergar(self, paredes):
		i = 0
		w, h = pygame.display.get_surface().get_size()
		for raio in self.raios:
			colisao = []
			for parede in paredes:
				colisao.append(raio.collision(parede))
			args = list(map(lambda x: np.sqrt((x[0]-self.x)**2 + (x[1]-self.y)**2) if type(x) == tuple else np.inf, colisao))
			i_mais_prox = np.argmin(args)
			ponto = colisao[i_mais_prox]
			if ponto != None:
				correção = 2
				cos = np.cos(np.radians(raio.theta - self.thetac))
				d = np.linalg.norm(np.array(ponto) - np.array((self.x,self.y)))*cos
				largura = round(w/len(self.raios)) + correção
				altura = (-(h-10)*d/w + (h-10))
				cor = [int(255 - (255*(d**2))/np.linalg.norm([w,d])**2)]*3
				posx = -w*(raio.theta - self.thetac - self.fov//2)/(self.fov-1)
				posy = h/2
				pygame.draw.rect(self.display, cor, (posx, posy - altura/2, largura, altura))

def criar_paredes(nparedes, tamanho_min, tamanho_max):
	w, h = pygame.display.get_surface().get_size()
	paredes = []
	for k in range(nparedes):
		ang = np.random.randint(0, 2*np.pi)
		tamanho = np.random.choice([i for i in range(tamanho_min, tamanho_max, 2)])
		vect = (tamanho*np.cos(ang), tamanho*np.sin(ang))
		A = (np.random.randint(0,2), np.random.randint(0,h))
		B = (A[0] + vect[0], A[1] + vect[1])
		paredes.append(
			Wall(A[0],A[1],B[0],B[1]))
	return paredes