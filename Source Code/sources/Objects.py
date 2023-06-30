import pygame
import random
import math

prefix_names = ['Miden','Ena','Di','Trio','Tesera','Pende','Exi','Eta','Okto','Enea']
names = ['Andromeda', 'Gemini', 'Ursa Major', 'Canis Major', 'Libra', 'Aquarius', 'Auriga', 'Lupus', 'Bootes', 'Corvus', 'Hercules', 'Hydra', 'Columba', 'Virgo', 'Delphinus', 'Draco', 'Monoceros', 'Ara', 'Pictor', 'Pyxis', 'Carinae', 'Lepus']

WIDTH, HEIGHT =  1280, 720

class Planet(pygame.sprite.Sprite):
	G = 6.67428e-11
	def __init__(self, x, y, radius, color, mass, sun, y_vel, atmosphere, name=None):
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass
		self.name = name

		self.atmosphere = atmosphere
		self.temperature = 0
		self.gravitation = 0
		self.speed_x = self.speed_y = 0

		self.circle_surface = pygame.Surface((self.radius, self.radius), pygame.SRCALPHA)
		self.rect = self.circle_surface.get_rect(center=(self.x+self.radius/2, self.y+self.radius/2))
		self.atmosphere_image = pygame.image.load('imgs/other/atmosphere.png').convert_alpha()
		self.atmosphere_image = pygame.transform.scale(self.atmosphere_image, (self.radius*3 - self.radius + 7, self.radius*3 - self.radius + 7))
		self.light_image = pygame.image.load('imgs/other/sunlight.png').convert_alpha()
		self.light_image = pygame.transform.scale(self.light_image, (self.radius*self.radius - self.radius + self.radius*2, self.radius*self.radius - self.radius + self.radius*2))

		self.resup = False
		self.show_hit_boxes = False

		self.orbit = []
		self.sun = sun
		self.distance_to_sun = 0

		self.x_vel = 0
		self.y_vel = y_vel
		self.fc = 0
		
		self.update_parameters()

	def update_parameters(self):
		if self.radius != 0:
			self.gravitation = (self.G * self.mass)/self.radius**2
			self.temperature = (self.G * self.mass * 28.966e-10)/(3 * 1.380649 * 10e-23 * self.radius) -273.15
		if self.name == None:
			self.name = f'{prefix_names[random.randint(0,len(prefix_names)-1)]}-{names[random.randint(0,len(names)-1)]}'

	def draw(self, win, cam_x, cam_y, resolution):
		x = self.x + WIDTH / 2 * resolution
		y = self.y  + HEIGHT / 2 * resolution
		if len(self.orbit) > 2 and self.sun == False:
			updated_points = []
			for point in self.orbit:
				x, y = point
				x = x + WIDTH / 2
				y = y + HEIGHT / 2
				updated_points.append((x + cam_x, y + cam_y))
			pygame.draw.lines(win, self.color, False, updated_points, 2)
		if self.atmosphere:
			win.blit(self.atmosphere_image, (x + cam_x - self.radius-3.5, y + cam_y - self.radius-3.5))

		if self.sun:
			win.blit(self.light_image, (x + cam_x - (self.radius * self.radius) + (self.radius * self.radius/2)- 10, y + cam_y - (self.radius * self.radius) + (self.radius * self.radius/2) - 10))

		pygame.draw.circle(win, self.color, (x + cam_x, y + cam_y), self.radius)
		if self.show_hit_boxes:
			pygame.draw.rect(win, (0,0,255), ((WIDTH/2 + self.rect.x + cam_x - self.radius, HEIGHT/2 + self.rect.y + cam_y - self.radius, self.radius*2, self.radius*2)))

	def collide_on_coordinates(self, mouse_x, mouse_y):
		if self.rect.collidepoint((mouse_x, mouse_y)):
			return True
		return False
		
	def attraction(self, other, tick):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y

		if distance_x == 0:
			distance_x += 1
		if distance_y == 0:
			distance_y += 1
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2)
		if other.sun:
			self.distance_to_sun = distance

		force = self.G * self.mass * other.mass / distance**2
		if not(self.sun):
			if force > 10*10e33 + self.mass:
				force = 10*10e33 + self.mass
			if force < -(10*10e33) -self.mass:
				force = -(10*10e33) -self.mass

		elif self.sun:
			if force > 10*10e54 + self.mass:
				force = 10*10e54 + self.mass
			if force < -(10*10e54) - self.mass:
				force = -(10*10e54) - self.mass

		theta = math.atan2(distance_y, distance_x)
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		self.speed_x = force_x
		self.speed_y = force_y

		return force_x, force_y
		
	def update_position(self, planets, TIMESTEP, cam_x, cam_y, res, tick):
		total_fx = total_fy = 0
		suns = []
		for planet in planets:
			if self == planet:
				continue
			fx, fy = self.attraction(planet, tick)
			total_fx += fx*10**-13
			total_fy += fy*10**-13

		if self.mass == 0:
			self.mass = 10 * 10e-120

		self.x_vel += total_fx / self.mass * TIMESTEP
		self.y_vel += total_fy / self.mass * TIMESTEP

		self.x += self.x_vel * TIMESTEP
		self.y += self.y_vel * TIMESTEP

		self.rect.x = self.x
		self.rect.y = self.y

		self.orbit.append((self.x, self.y))
		if len(self.orbit) > 500:
			del self.orbit[0]

	def __del__(self):
		pass