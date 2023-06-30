import pygame
import random

class Slider(pygame.sprite.Sprite):
	def __init__(self, x, y, w, visibility):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.w = w

		self.quad_w = 15
		self.quad_h = 30
		self.quad_y = self.saved_quad_y = self.y - self.quad_h/2

		self.saved_value = random.randint(0,255)
		self.value = random.randint(0,255)

		self.quad_x = self.w + self.x - self.quad_w/2 + 0.1 - (self.value * self.w) / 255
		self.saved_quad_x = self.w + self.x - self.quad_w/2 + 0.1 - (self.saved_value * self.w) / 255

		self.num = 0

		self.visibility = visibility
		self.click = False

		self.quad_surface = pygame.Surface((self.w, self.quad_h), pygame.SRCALPHA)
		self.rect = self.quad_surface.get_rect(center=(self.x + self.w/2, self.quad_y + self.quad_h/2))

	def draw(self, win):
		if self.visibility:
			pygame.draw.line(win, (220, 220, 220), (self.x,self.y), (self.x+self.w, self.y))
			if self.num == 1:
				pygame.draw.rect(win, (170, 170, 170), (self.quad_x, self.quad_y, self.quad_w, self.quad_h))
				pygame.draw.rect(win, (220, 220, 220), (self.quad_x+2, self.quad_y+4, self.quad_w-4, self.quad_h-6))
			if self.num == 2:
				pygame.draw.rect(win, (170, 170, 170), (self.saved_quad_x, self.saved_quad_y, self.quad_w, self.quad_h))
				pygame.draw.rect(win, (220, 220, 220), (self.saved_quad_x+2, self.saved_quad_y+4, self.quad_w-4, self.quad_h-6))

	def collide(self, pos, mouse): 
		if self.rect.collidepoint(pos) and mouse[0] and not(self.click):
			self.click = True
		if not(mouse[0]):
			self.click = False

	def update_position(self, pos, mouse, win):
		if self.visibility:
			self.collide(pos, mouse)
			if self.num == 1:
				self.value = int((255/self.w) * (self.w + self.x - self.quad_x - self.quad_w/2 + 0.1))
				if self.click and (self.quad_x <= self.w+self.x-self.quad_w/2 and self.quad_x >= self.x-self.quad_w/2):
					self.quad_x = pos[0] - self	.quad_w/2
				if self.quad_x > self.w+self.x-self.quad_w/2:
					self.quad_x = self.w+self.x-self.quad_w/2
				if self.quad_x < self.x-self.quad_w/2:
					self.quad_x = self.x-self.quad_w/2
			if self.num == 2:
				self.saved_value = int((255/self.w) * (self.w + self.x - self.saved_quad_x - self.quad_w/2 + 0.1))
				if self.click and (self.saved_quad_x <= self.w+self.x-self.quad_w/2 and self.saved_quad_x >= self.x-self.quad_w/2):
					self.saved_quad_x = pos[0] - self.quad_w/2
				if self.saved_quad_x > self.w+self.x-self.quad_w/2:
					self.saved_quad_x = self.w+self.x-self.quad_w/2
				if self.saved_quad_x < self.x-self.quad_w/2:
					self.saved_quad_x = self.x-self.quad_w/2