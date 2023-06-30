import pygame

class UserObject:
	def __init__(self, x, y, radius, color, mass, sun):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass
		self.sun = sun
		self.visibility = False
		self.atmosphere = False

		self.circle_surface = pygame.Surface((self.radius, self.radius), pygame.SRCALPHA)
		self.rect = self.circle_surface.get_rect(center=(self.x+self.radius/2, self.y+self.radius/2))
		self.atmosphere_image = pygame.image.load('imgs/other/atmosphere.png').convert_alpha()
		self.atmosphere_image = pygame.transform.scale(self.atmosphere_image, (self.radius*3 - self.radius + 7, self.radius*3 - self.radius + 7))

	def draw(self, win):
		if self.visibility:
			if self.atmosphere:
				win.blit(self.atmosphere_image, (self.x - self.radius - 4, self.y - self.radius - 4))
			pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
