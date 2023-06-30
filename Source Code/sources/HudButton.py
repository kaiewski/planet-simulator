import pygame

class Hud_button(pygame.sprite.Sprite):
	def __init__(self, x, y, image, num, visibility, ident='hud_button', scale_x=1, scale_y=1):
		pygame.sprite.Sprite.__init__(self)
		w, h = image.get_width(), image.get_height()
		self.image = pygame.transform.scale(image, (int(w * scale_x), int(h * scale_y)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x,y)
		self.num = num
		self.click = False
		self.ident = ident
		self.visibility = visibility

	def draw(self, pos, mouse, win):
		if self.visibility:
			self.collide(pos, mouse)
			win.blit(self.image, (self.rect.x, self.rect.y))

	def collide(self, pos, mouse):
		if self.rect.collidepoint(pos) and mouse[0] and not(self.click):
			self.click = True
		if not(mouse[0]):
			self.click = False