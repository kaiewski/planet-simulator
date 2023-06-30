import pygame
import random

class TextBox(pygame.sprite.Sprite):
	def __init__(self, x, y, w, h, purpose):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.visibility = False
		self.click = False
		self.state = 0
		self.value = ''
		self.purpose = purpose
		self.fontsize = 17
		self.f1 = pygame.font.SysFont('comicsans', self.fontsize)

		self.tick = 0
		self.tick_state = 0

		self.surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
		self.rect = self.surface.get_rect(center=(self.x + self.fontsize/2 + self.w/2, self.y + self.h * 1.5))

		self.update_parameters()

	def update_parameters(self):
		if self.purpose == 'name':
			self.value = f'Object-{random.randrange(0,10000)}'
		if self.purpose == 'radius':
			self.value = str(random.randrange(1,30))
		if self.purpose == 'mass':
			self.value = str(random.randrange(1,20))
		if self.purpose == 'mass_e':
			self.value = str(random.randrange(1,20))
		if self.purpose == 'sun' or self.purpose == 'atmosphere':
			self.value = 'False'
		
	def draw(self, win, pos, mouse):
		self.rect.w = (self.x + self.fontsize/2 * len(str(self.value)) - self.fontsize * 5.5)
		if self.rect.w <= 25:
			self.rect.w = 25
		if self.visibility:
			self.collide(pos, mouse)
			win.blit((self.f1.render(str(self.value), 1, (255, 255, 255))), (self.x + 5, self.y+self.h))
			if self.tick_state == 1 and self.state == 1 and self.purpose != 'sun' and self.purpose != 'atmosphere':
				win.blit((self.f1.render(f'_', 10, (170,170,170))), (self.x + 5, self.y+self.h))
			if self.state == 1 and (self.purpose == 'sun' or self.purpose == 'atmosphere'):
				self.value = 'True'
			elif self.state == 0 and (self.purpose == 'sun' or self.purpose == 'atmosphere'):
				self.value = 'False'
			self.update_tick_state()
		else:
			self.tick_state = 0
			self.tick = 0

	def update_tick_state(self):
		if self.tick // 20 :
			if self.tick_state == 0:
				self.tick_state = 1
			else:
				self.tick_state = 0
			self.tick = 0
		self.tick += 1

	def update_state(self, textboxes):
		for i in textboxes:
			if i.state == 1 and i.purpose != 'sun' and i.purpose != 'atmosphere':
				i.state = 0

		if self.purpose != 'sun' and self.purpose != 'atmosphere':
			if self.state == 1:
				self.state = 0
			if self.state == 0:
				self.state = 1

		if (self.purpose == 'sun' or self.purpose == 'atmosphere') and self.click:
			if self.state == 1:
				self.state = 0
			if self.state == 0:
				self.state = 1
			self.click = False

	def collide(self, pos, mouse): 
		if self.rect.collidepoint(pos) and mouse[0]:
			self.click = True
		else:
			self.click = False