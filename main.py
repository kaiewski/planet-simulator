#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame
import math
import time
import random
import sys
sys.path.insert(0, 'sources')

from HudButton import *
from Slider import *
from UserObject import *
from Objects import *
from TextBox import *

pygame.init()

WIDTH, HEIGHT =  1280, 720

size = [WIDTH, HEIGHT]
res_scale = 1
res = [i//res_scale for i in size]

window = pygame.display.set_mode(size)

WIN = pygame.display.set_mode(size)
screen = pygame.transform.scale(window, res)
pygame.display.set_caption("Planet Simulator by kaiewski")

pygame.display.set_icon(pygame.image.load("icon.bmp"))

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

run = True
clock = pygame.time.Clock()

FPS = 60
timestep = 0.0001
cam_x = cam_y = 0
AU = 149.6e6 * 1000

tick = 0
last_fps = 0
max_fps = 0
cent_fps = []
res_fps = 0

hud_cell = pygame.image.load('imgs/hud/hud_cell.png').convert_alpha()
hud_double_cell = pygame.image.load('imgs/hud/hud_double_cell.png').convert_alpha()
hud_big_cell = pygame.image.load('imgs/hud/hud_big_cell.png').convert_alpha()
background = [pygame.image.load('imgs/paralax_stars/sparks_transparent.png').convert_alpha()]

def textbox_check(textbox, symbol):
	pass


def screen_to_world(x, y, scale, camera_x, camera_y):
    world_x = ((x - WIDTH/2) * scale  - -camera_x * -scale)
    world_y = ((HEIGHT/2 - y) * scale - camera_y * -scale)
    return world_x, -world_y

def move_object_number(direction, coords, planets):
	if direction == 0:	
		if coords[1]-1 < 0:
			coords[1] = len(planets)-1
		else:
			coords[1] -= 1

	if direction == 1:	
		if coords[1]+1 >= len(planets):
			coords[1] = 0
		else:
			coords[1] += 1


sun = Planet(0, 0, 30, YELLOW, 3 * 10**34, True, 0, False)
earth = Planet(-200, 0, 16, BLUE, 5.9742, False, 29.783 * 1000, True)
moon = Planet(-240, 0, 16, (255,255,255,0), 7.36, False, 1.023 * 20000, False)
mars = Planet(-1.524 * 200 , 0, 10, RED, 6.39, False, 24.077 * 1000, False)
mercury = Planet(0.387 * 200, 0, 8, DARK_GREY, 3.30, False, -47.4 * 1000, False)
venus = Planet(0.723 * 200, 0, 14, WHITE, 4.8685, False, -35.02 * 1000, False)

userobject = UserObject(100, 100, 30, YELLOW, 3 * 10 ** 34, False)
huduserobjects = [UserObject(100, 100, 30, YELLOW, 3 * 10 ** 34, False), UserObject(100, 100, 30, YELLOW, 3 * 10 ** 34, False)]
textboxes_first = []
textboxes_second = []

for i in huduserobjects:
	i.visibility = False

for i in range(1, 7):
	if i == 1:
		textboxes_first.append(TextBox(100, 100, 100, 25, 'name'))
		textboxes_second.append(TextBox(100, 100, 100, 25, 'name'))
	if i == 2:
		textboxes_first.append(TextBox(100, 200, 100, 25, 'mass'))
		textboxes_second.append(TextBox(100, 200, 100, 25, 'mass'))
	if i == 3:
		textboxes_first.append(TextBox(100, 300, 100, 25, 'mass_e'))
		textboxes_second.append(TextBox(100, 300, 100, 25, 'mass_e'))
	if i == 4:
		textboxes_first.append(TextBox(100, 400, 100, 25, 'radius'))
		textboxes_second.append(TextBox(100, 400, 100, 25, 'radius'))
	if i == 5:
		textboxes_first.append(TextBox(100, 400, 100, 25, 'sun'))
		textboxes_second.append(TextBox(100, 400, 100, 25, 'sun'))
	if i == 6:
		textboxes_first.append(TextBox(100, 400, 100, 25, 'atmosphere'))
		textboxes_second.append(TextBox(100, 400, 100, 25, 'atmosphere'))
	if i == 7:
		textboxes_first.append(TextBox(100, 400, 100, 25, 'temperature'))
		textboxes_second.append(TextBox(100, 400, 100, 25, 'temperature'))		

planets = [earth, mars, mercury, venus, sun]
#planets = []

f1 = pygame.font.SysFont('comicsans', 17)
f2 = pygame.font.Font(None, 50)

hud = []
yc = 80
bg_x = bg_y = 0

dirs = [None, None]
menu_objects = []
coords = None
object_to_delete = None
object_num = 0

for i in range(1,10):
	for y in range(1):
		if i < 3:
			y += yc
			hud.append(Hud_button(20,y,hud_cell, i, True, f'inventory_hud', 2, 2))
		if i == 4:
			hud.append(Hud_button(WIDTH-74*2, 20, hud_double_cell, i, True ,'clear_scene', 2, 2))
		if i == 5:
			hud.append(Hud_button(WIDTH-138*2, 85, hud_big_cell, i, False ,'hud_info', 2, 2))
		if i == 6:
			hud.append(Hud_button(WIDTH-148-5, 320-5, hud_double_cell, i, False ,'delete_object', 2, 2))
		if i == 7:
			hud.append(Hud_button(WIDTH-207-5, 330-5, hud_cell, i, False ,'next_object', 1.7, 1.7))
			dirs[0] = hud[i-2]
		if i == 8:
			hud.append(Hud_button(WIDTH-265-5, 330-5, hud_cell, i, False ,'previous_object', 1.7, 1.7))
			dirs[1] = hud[i-2]
		if i == 9:
			hud.append(Hud_button(32*2+25, 0, hud_big_cell, i, False, 'information_menu', 2, 3.5))
	yc += 20 * 2 + 25

sliders = []
for i in range(3):
	sliders.append(Slider(100, 200, 100, False))

shift = False

if __name__ == "__main__":
	while run:
		while run:
			try:
				start_time = time.time()
				clock.tick(FPS)
				WIN.fill((0,0,0))
				WIN.blit(background[0], (0,0))
				planets_new = []
				btn_clk = False

				for event in pygame.event.get():
					key = pygame.key.get_pressed()
					mouse = pygame.mouse.get_pressed()
					mouse_move = pygame.mouse.get_rel()

					if event.type == pygame.QUIT:
						run = False

					if event.type == pygame.MOUSEWHEEL and event.y == -1 and timestep > 0 and not(mouse[1]):
						if key[pygame.K_LSHIFT]:
							timestep -= 0.01
						if key[pygame.K_LCTRL]:
							timestep -= 0.001
						else:
							timestep -= 0.00001

					if event.type == pygame.MOUSEWHEEL and event.y == 1 and timestep < 1 and not(mouse[1]):
						if key[pygame.K_LSHIFT]:
							timestep += 0.01
						if key[pygame.K_LCTRL]:
							timestep += 0.001
						else:
							timestep += 0.00001

					if key[pygame.K_q] and planets_new != None:
						wx,wy = screen_to_world(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], res_scale, cam_x, cam_y)
						for obj in range(0, len(planets)):
							for cell in hud:
								if planets[obj]!=None and  planets[obj].collide_on_coordinates(wx, wy):
									if cell.ident == 'hud_info':
										coords = [True, obj, cell]
									if cell.ident == 'delete_object':
										object_to_delete = cell

					if key[pygame.K_SPACE] and coords != None:
						coords[0] = False
						if coords[2] != None:
							coords[2].visibility = False
						object_to_delete.visibility = False
						dirs[0].visibility = False
						dirs[1].visibility = False

					if key[pygame.K_LEFT] and coords != None:
						move_object_number(0, coords, planets)

					if key[pygame.K_RIGHT] and coords != None:
						move_object_number(1, coords, planets)

					if event.type == pygame.MOUSEMOTION and mouse[1]:
						cam_x += mouse_move[0]
						cam_y += mouse_move[1]

					if event.type == pygame.KEYDOWN and pygame.key.name(event.key) == "left shift":
						shift = True
					if event.type == pygame.KEYUP and pygame.key.name(event.key) == "left shift":
						shift = False
					for textbox in textboxes_first:
						if textbox.state == 1 and event.type == pygame.KEYDOWN and textbox.purpose != 'name' and textbox.purpose != 'sun' and textbox.purpose != 'atmosphere':
							if '-' in str(textbox.value):
								max_value = 4
							else:
								max_value = 3
							if (pygame.key.name(event.key).isdigit() or pygame.key.name(event.key) == '-') and len(str(textbox.value)) < max_value:
								if pygame.key.name(event.key) == '-' and len(str(textbox.value)) < 2 and textbox.purpose != 'radius':
									 textbox.value = pygame.key.name(event.key)
								if pygame.key.name(event.key) != '-' and str(textbox.value) == '0' and str(textbox.value) != '-':
									textbox.value = int(textbox.value) + int(pygame.key.name(event.key))
								elif pygame.key.name(event.key) != '-' and len(str(textbox.value)) > 0:
									textbox.value = str(textbox.value) + pygame.key.name(event.key)
							if pygame.key.name(event.key) == "backspace" and len(str(textbox.value)) > 0:
								textbox.value = str(textbox.value)[:-1]
							if textbox.purpose == 'radius':
								if len(str(textbox.value)) > 0 and not('-'in str(textbox.value)) and int(textbox.value) > 150:
									textbox.value = '150'

						elif textbox.state == 1 and (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and (textbox.purpose == 'name') and textbox.purpose != 'sun' and textbox.purpose != 'atmosphere':
							if pygame.key.name(event.key) and len(str(textbox.value)) < 18 and len(pygame.key.name(event.key)) < 2 and event.type == pygame.KEYDOWN:
								if shift == False:
									textbox.value += pygame.key.name(event.key)
								if shift == True:
									textbox.value += pygame.key.name(event.key).upper()
							if pygame.key.name(event.key) == "backspace" and len(str(textbox.value)) > 0 and event.type == pygame.KEYDOWN:
								textbox.value = textbox.value[:-1]

						if textbox.state == 1 and event.type == pygame.KEYUP and pygame.key.name(event.key) == 'return' and not(btn_clk) and textbox.purpose != 'sun' and textbox.purpose != 'atmosphere':
							textbox.state = 0
						if textbox.state == 1 and (textbox.purpose == 'sun' or textbox.purpose == 'atmosphere') and textbox.click: 
							textbox.state = 0
							textbox.click = False
						elif textbox.state == 0 and (textbox.purpose == 'sun' or textbox.purpose == 'atmosphere') and textbox.click: 
							textbox.state = 1
							textbox.click = False
						if textbox.value == '' and textbox.purpose != 'sun' and textbox.purpose != 'atmosphere' and textbox.purpose != 'name':
							textbox.value = '0'

					for textbox in textboxes_second:
						if textbox.state == 1 and event.type == pygame.KEYDOWN and textbox.purpose != 'name' and textbox.purpose != 'sun':
							if '-' in str(textbox.value):
								max_value = 4
							else:
								max_value = 3
							if (pygame.key.name(event.key).isdigit() or pygame.key.name(event.key) == '-') and len(str(textbox.value)) < max_value:
								if pygame.key.name(event.key) == '-' and len(str(textbox.value)) < 2 and textbox.purpose != 'radius':
									 textbox.value = pygame.key.name(event.key)
								if pygame.key.name(event.key) != '-' and str(textbox.value) == '0' and str(textbox.value) != '-':
									textbox.value = int(textbox.value) + int(pygame.key.name(event.key))
								elif pygame.key.name(event.key) != '-' and len(str(textbox.value)) > 0:
									textbox.value = str(textbox.value) + pygame.key.name(event.key)
							if pygame.key.name(event.key) == "backspace" and len(str(textbox.value)) > 0:
								textbox.value = str(textbox.value)[:-1]
							if textbox.purpose == 'radius':
								if len(str(textbox.value)) > 0 and not('-'in str(textbox.value)) and int(textbox.value) > 150:
									textbox.value = '150'

						elif textbox.state == 1 and (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP) and (textbox.purpose == 'name') and textbox.purpose != 'sun' and textbox.purpose != 'atmosphere':
							if pygame.key.name(event.key) and len(str(textbox.value)) < 18 and len(pygame.key.name(event.key)) < 2 and event.type == pygame.KEYDOWN:
								if shift == False:
									textbox.value += pygame.key.name(event.key)
								if shift == True:
									textbox.value += pygame.key.name(event.key).upper()
							if pygame.key.name(event.key) == "backspace" and len(str(textbox.value)) > 0 and event.type == pygame.KEYDOWN:
								textbox.value = textbox.value[:-1]

						if textbox.state == 1 and event.type == pygame.KEYUP and pygame.key.name(event.key) == 'return' and not(btn_clk) and textbox.purpose != 'sun' and textbox.purpose != 'atmosphere':
							textbox.state = 0
						if textbox.state == 1 and (textbox.purpose == 'sun' or textbox.purpose == 'atmosphere') and textbox.click: 
							textbox.state = 0
							textbox.click = False
						elif textbox.state == 0 and (textbox.purpose == 'sun' or textbox.purpose == 'atmosphere') and textbox.click: 
							textbox.state = 1
							textbox.click = False
						if textbox.value == '' and textbox.purpose != 'sun' and textbox.purpose != 'atmosphere' and textbox.purpose != 'name':
							textbox.value = '0'

					if timestep < 0:
						timestep = 0
					if event.type == pygame.MOUSEBUTTONUP and (event.button == 1 or event.button == 3):
						for slider in sliders:
							if slider.click:
								btn_clk = True
						for textbox in textboxes_first:
							if textbox.click:
								btn_clk = True
								textbox.update_state(textboxes_first)

						for textbox in textboxes_second:
							if textbox.click:
								btn_clk = True
								textbox.update_state(textboxes_second)

						for cell in hud:
							if cell.click and cell.ident == 'inventory_hud' and (cell.num == 1 or cell.num == 2):
								btn_clk = True
								cs = 0
								if hud[7].visibility:
									hud[7].visibility = False
									userobject.visibility = False
									for textbox in textboxes_first:
										textbox.visibility = False
									for textbox in textboxes_second:
										textbox.visibility = False

									for i in sliders:
										i.visibility = False
								else:
									for i in sliders:
										cs += 0.7
										hud[7].rect.y = cell.rect.y
										hud[7].visibility = True
										userobject.visibility = True
										i.num = cell.num
										i.visibility = True
										if cell.num == 1:
											i.quad_x = hud[7].rect.x + i.quad_w / 2 + 3.5 + (i.quad_x + i.quad_w/2 - i.w) - i.quad_w / 2
											i.rect.y = i.quad_y = hud[7].rect.y + hud[7].rect.h - cs * i.rect.h - (cs * i.quad_h + i.quad_h/2)
											object_num = 1
											for textbox in textboxes_first:
												textbox.visibility = True
											for textbox in textboxes_second:
												textbox.visibility = False
										if cell.num == 2:
											i.saved_quad_x = hud[7].rect.x + i.quad_w / 2 + 3.5 + (i.saved_quad_x + i.quad_w/2 - i.w) - i.quad_w / 2
											i.rect.y = i.saved_quad_y = hud[7].rect.y + hud[7].rect.h - cs * i.rect.h - (cs * i.quad_h + i.quad_h/2)
											object_num = 2
											for textbox in textboxes_second:
												textbox.visibility = True
											for textbox in textboxes_first:
												textbox.visibility = False
										i.x = i.rect.x = hud[7].rect.x + i.quad_w / 2 + 5
										i.y = hud[7].rect.y + hud[7].rect.h - cs * i.rect.h - cs * i.quad_h
										userobject.x = hud[7].rect.x - userobject.radius/2 + hud[7].rect.w/2 + hud[7].rect.w/4 + 10
										userobject.y = hud[7].rect.y - userobject.radius/2 + hud[7].rect.h / 2 + hud[7].rect.h/4 + 70
										
									ty = -30
									if cell.num == 1:
										for textbox in textboxes_first:
											if textbox.purpose != 'name':
												textbox.rect.x = textbox.x = hud[7].rect.x + 70
											if textbox.purpose == 'name':
												textbox.rect.x = textbox.x = hud[7].rect.x - textbox.w/2 + 70
											if textbox.purpose == 'mass_e':
												ty -= 25
												textbox.rect.x = textbox.x = hud[7].rect.x - textbox.w/2 + 200
											if textbox.purpose == 'radius':
												textbox.rect.x = textbox.x = hud[7].rect.x - textbox.w/2 + 133
											if textbox.purpose == 'sun':
												textbox.rect.x = textbox.x = hud[7].rect.x - textbox.w/2 + 113
											if textbox.purpose == 'atmosphere':
												textbox.rect.x = textbox.x = hud[7].rect.x - textbox.w/2 + 177
											textbox.y = hud[7].rect.y + ty + textbox.h
											textbox.rect.y = textbox.y + textbox.h/2 * 1.5 + textbox.fontsize/2
											if ty == -30:
												ty += 20
											ty += 25

									if cell.num == 2:
										for textbox in textboxes_second:
											if textbox.purpose != 'name':
												textbox.rect.x = textbox.x = hud[7].rect.x + 60
											if textbox.purpose == 'name':
												textbox.rect.x = textbox.x = hud[7].rect.x - textbox.w/2 + 70
											if textbox.purpose == 'mass_e':
												ty -= 25
												textbox.rect.x = textbox.x = hud[7].rect.x - textbox.w/2 + 200
											if textbox.purpose == 'radius':
												textbox.rect.x = textbox.x = hud[7].rect.x - textbox.w/2 + 133
											if textbox.purpose == 'sun':
												textbox.rect.x = textbox.x = hud[7].rect.x - textbox.w/2 + 113
											if textbox.purpose == 'atmosphere':
												textbox.rect.x = textbox.x = hud[7].rect.x - textbox.w/2 + 177
											textbox.y = hud[7].rect.y + ty + textbox.h
											textbox.rect.y = textbox.y + textbox.h/2 * 1.5 + textbox.fontsize/2
											if ty == -30:
												ty += 20
											ty += 25

							if cell.click and cell.ident == 'clear_scene':
								planets = []
								planets_new = []
								btn_clk = True
								if coords != None:
									coords[2].visibility = False
									coords[0] = False
									object_to_delete.visibility = False
								coords = None
								object_to_delete = None
								dirs[0].visibility = False
								dirs[1].visibility = False

							if cell.click and cell.ident == 'next_object':
								btn_clk = True
								move_object_number(1, coords, planets)

							if cell.click and cell.ident == 'previous_object':
								btn_clk = True
								move_object_number(0, coords, planets)

							if cell.click and cell.visibility and cell.ident == 'delete_object' and coords != None:
								btn_clk = True
								if len(planets) > 1:
									del planets[coords[1]]
									move_object_number(1, coords, planets)
								else:
									del planets[coords[1]]
									coords[2].visibility = False
									object_to_delete.visibility = False	
									coords[0] = False
									dirs[0].visibility = False
									dirs[1].visibility = False

							if cell.click and cell.ident == 'information_menu':
								btn_clk = True

						for textbox in textboxes_first:
							if not(btn_clk) and textbox.state == 1 and not(textbox.click) and textbox.purpose != 'sun' and textbox.purpose != 'atmosphere':
								textbox.state = 0
							if not(textbox.visibility) and textbox.purpose != 'sun' and textbox.purpose != 'atmosphere':
								textbox.click = False
								textbox.state = 0
						for textbox in textboxes_second:
							if not(btn_clk) and textbox.state == 1 and not(textbox.click) and textbox.purpose != 'sun' and textbox.purpose != 'atmosphere':
								textbox.state = 0
							if not(textbox.visibility) and textbox.purpose != 'sun' and textbox.purpose != 'atmosphere':
								textbox.click = False
								textbox.state = 0

					if (hud[7].visibility):
						if object_num == 1:
							for textbox in textboxes_first:
								userobject.color = ((sliders[0].value, sliders[1].value, sliders[2].value))
								if textbox.purpose == 'atmosphere' and textbox.value == 'True':
									userobject.atmosphere = True
								else:
									userobject.atmosphere = False
						if object_num == 2:
							for textbox in textboxes_second:
								userobject.color = ((sliders[0].saved_value, sliders[1].saved_value, sliders[2].saved_value))
								if textbox.purpose == 'atmosphere' and textbox.value == 'True':
									userobject.atmosphere = True
								else:
									userobject.atmosphere = False

					if btn_clk == False and (key[pygame.K_e] or event.type == pygame.MOUSEBUTTONUP and event.button == 1):
						for par in textboxes_first:
							if par.purpose == 'name':
								_name = par.value
							if par.purpose == 'mass':
								if par.value == '': par.value = '0'
								_mass = int(par.value)
							if par.purpose == 'mass_e':
								if par.value == '': par.value = '0'
								_mass_e = int(par.value)
							if par.purpose == 'radius':
								if par.value == '': par.value = '0'
								_radius = abs(int(par.value))
							if par.purpose == 'sun':
								if par.value == "True":
									_sun = True
								if par.value == "False":
									_sun = False
							if par.purpose == 'atmosphere':
								if _sun == False and par.value == 'True':
									_atmosphere = True
								else:
									_atmosphere = False
						xp, yp = screen_to_world(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], res_scale, cam_x, cam_y)
						new_obj = Planet(xp, yp, _radius, (sliders[0].value, sliders[1].value, sliders[2].value), _mass * 10**_mass_e, _sun, 0, _atmosphere, _name)
						planets.append(new_obj)

					if btn_clk == False and (key[pygame.K_r] or event.type == pygame.MOUSEBUTTONUP and event.button == 3):
						for par in textboxes_second:
							if par.purpose == 'name':
								__name = par.value
							if par.purpose == 'mass':
								if par.value == '': par.value = '0'
								__mass = int(par.value)
							if par.purpose == 'mass_e':
								if par.value == '': par.value = '0'
								__mass_e = int(par.value)
							if par.purpose == 'radius':
								if par.value == '': par.value = '0'
								__radius = abs(int(par.value))
							if par.purpose == 'sun':
								if par.value == "True":
									__sun = True
								if par.value == "False":
									__sun = False
							if par.purpose == 'atmosphere':
								if __sun == False and par.value == 'True':
									__atmosphere = True
								else:
									__atmosphere = False
						xp, yp = screen_to_world(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, cam_x, cam_y)
						new_obj = Planet(xp, yp, __radius, (sliders[0].saved_value, sliders[1].saved_value, sliders[2].saved_value), __mass * 10**__mass_e, __sun, 0, __atmosphere, __name)
						planets.append(new_obj)
				if len(planets) > 0 and planets != None and coords != None and coords[0] and object_to_delete != None:
					try:
						cam_x = -planets[coords[1]].x
						cam_y = -planets[coords[1]].y
						coords[2].visibility = True
						object_to_delete.visibility = True
						dirs[0].visibility = True
						dirs[1].visibility = True
					except:
						if len(planets) > 0:
							move_object_number(1, coords, planets)
						else:
							coords[2].visibility = False
							object_to_delete.visibility = False	
							coords[0] = False
							dirs[0].visibility = False
							dirs[1].visibility = False

				for planet in range(0, len(planets)):
					if planets[planet] != None and (planets[planet].x < 50000 - cam_x and planets[planet].x > -cam_x - 50000) and (planets[planet].y < 50000 - cam_y and planets[planet].y > -cam_y - 50000):
						planets_new.append(planets[planet])
					else:
						planets[planet] = None

				for planet in planets_new:
					if not(planet.sun):
						planet.update_position(planets_new, timestep, cam_x, cam_y, res_scale, tick)
						planet.draw(WIN, cam_x, cam_y, res_scale)

				for planet in planets_new:
					if planet.sun:
						planet.update_position(planets_new, timestep, cam_x, cam_y, res_scale, tick)
						planet.draw(WIN, cam_x, cam_y, res_scale)

				for i in sliders:
					i.update_position(pygame.mouse.get_pos(), mouse, WIN)

				TStext = f1.render(f'Time x{round(timestep*10000,2)}', 1, (255, 255, 255))
				WIN.blit(TStext, (10, 10))
				WIN.blit((f1.render(f'Objects simulated: {len(planets_new)}', 1, (255, 255, 255))), (10, 30))
				for cell in hud:
					cell.draw(pygame.mouse.get_pos(), mouse, WIN)
					if cell.ident == 'clear_scene':
						WIN.blit((f1.render(f'Clear Scene', 1, (255, 255, 255))), (cell.rect.x+17, cell.rect.y+23))
					if cell.ident == 'hud_info' and cell.visibility == True and coords != None and planets != None and len(planets) > 0:
						WIN.blit((f1.render(f'Sun: {planets[coords[1]].sun}', 1, (255, 255, 255))), (cell.rect.x+13, cell.rect.y+13))
						WIN.blit((f1.render(f'Name: {planets[coords[1]].name}', 1, (255, 255, 255))), (cell.rect.x+13, cell.rect.y+30))
						WIN.blit((f1.render(f'Mass: {planets[coords[1]].mass/-1*-1}', 1, (255, 255, 255))), (cell.rect.x+13, cell.rect.y+47))
						WIN.blit((f1.render(f'Radius: {planets[coords[1]].radius}', 1, (255, 255, 255))), (cell.rect.x+13, cell.rect.y+64))
						formatted_num = '{:.3e}'.format(planets[coords[1]].temperature)
						WIN.blit((f1.render(f'Temperature: {formatted_num}', 1, (255, 255, 255))), (cell.rect.x+13, cell.rect.y+81))
						formatted_num = '{:.3e}'.format(planets[coords[1]].gravitation)
						WIN.blit((f1.render(f'Gravitation: {formatted_num}', 1, (255, 255, 255))), (cell.rect.x+13, cell.rect.y+98))
						formatted_num = '{:.3e}'.format(abs(planets[coords[1]].speed_x))
						WIN.blit((f1.render(f'Speed X: {formatted_num}', 1, (255, 255, 255))), (cell.rect.x+13, cell.rect.y+115))
						formatted_num = '{:.3e}'.format(abs(planets[coords[1]].speed_y))
						WIN.blit((f1.render(f'Speed Y: {formatted_num}', 1, (255, 255, 255))), (cell.rect.x+13, cell.rect.y+132))
						if not(planets[coords[1]].sun):
							WIN.blit((f1.render(f'Atmosphere: {planets[coords[1]].atmosphere}', 1, (255, 255, 255))), (cell.rect.x+13, cell.rect.y+149))
							WIN.blit((f1.render(f'Distance to star: {round(planets[coords[1]].distance_to_sun,1)}', 1, (255, 255, 255))), (cell.rect.x+13, cell.rect.y+166))
					if cell.ident == 'delete_object' and cell.visibility == True and coords != None:
						WIN.blit((f1.render(f'Delete Object', 1, (255, 255, 255))), (cell.rect.x + 7, cell.rect.y + 24))
					if cell.ident == 'next_object' and cell.visibility == True and coords != None:
						WIN.blit((f2.render(f'>', 1, (255, 255, 255))), (cell.rect.x + 17, cell.rect.y + 8))
					if cell.ident == 'previous_object' and cell.visibility == True and coords != None:
						WIN.blit((f2.render(f'<', 1, (255, 255, 255))), (cell.rect.x + 17, cell.rect.y + 8))

					if cell.ident == 'information_menu' and cell.visibility:
						if object_num == 1:
							for i in range(1, len(textboxes_first)):
								if i == 1:
									WIN.blit((f1.render(f'Mass:', 1, (255, 255, 255))), (textboxes_first[i].rect.x-45, textboxes_first[i].rect.y - 3))
								if i == 2:
									WIN.blit((f1.render(f' ∙ 10e^', 1, (255, 255, 255))), (textboxes_first[i-1].rect.x + 37, textboxes_first[i-1].rect.y - 3))
								if i == 3:
									WIN.blit((f1.render(f'Radius:', 1, (255, 255, 255))), (textboxes_first[i-2].rect.x - 45, textboxes_first[i].rect.y - 3))
								if i == 4:
									WIN.blit((f1.render(f'Sun:', 1, (255, 255, 255))), (textboxes_first[i-3].rect.x - 45, textboxes_first[i].rect.y - 3))
								if i == 5:
									WIN.blit((f1.render(f'Atmosphere:', 1, (255, 255, 255))), (textboxes_first[i-4].rect.x - 45, textboxes_first[i].rect.y - 3))
						
						if object_num == 2:
							for i in range(1, len(textboxes_second)):
								if i == 1:
									WIN.blit((f1.render(f'Mass:', 1, (255, 255, 255))), (textboxes_second[i].rect.x-45, textboxes_second[i].rect.y - 3))
								if i == 2:
									WIN.blit((f1.render(f'∙ 10e^', 1, (255, 255, 255))), (textboxes_second[i-1].rect.x + 37, textboxes_second[i-1].rect.y - 3))
								if i == 3:
									WIN.blit((f1.render(f'Radius:', 1, (255, 255, 255))), (textboxes_second[i-2].rect.x - 45, textboxes_second[i].rect.y - 3))
								if i == 4:
									WIN.blit((f1.render(f'Sun:', 1, (255, 255, 255))), (textboxes_second[i-3].rect.x - 45, textboxes_second[i].rect.y - 3))
								if i == 5:
									WIN.blit((f1.render(f'Atmosphere:', 1, (255, 255, 255))), (textboxes_second[i-4].rect.x - 45, textboxes_second[i].rect.y - 3))

					if cell.ident == 'inventory_hud' and cell.visibility:
						if cell.num == 1:
							for par in textboxes_first:
								if par.purpose == 'radius':
									huduserobjects[0].radius = int(par.value)
							if huduserobjects[0].radius <= 10:
								huduserobjects[0].radius = 5
							if huduserobjects[0].radius <= 15 and huduserobjects[0].radius > 10:
								huduserobjects[0].radius = 15
							if huduserobjects[0].radius >= 25 and huduserobjects[0].radius > 15:
								huduserobjects[0].radius = 25
							huduserobjects[0].y = cell.rect.y + cell.rect.h/2
							huduserobjects[0].x = cell.rect.x + cell.rect.w/2
							huduserobjects[0].color = (sliders[0].value, sliders[1].value, sliders[2].value)
						if cell.num == 2:
							for par in textboxes_second:
								if par.purpose == 'radius':
									huduserobjects[1].radius = int(par.value)
							if huduserobjects[1].radius <= 10:
								huduserobjects[1].radius = 5
							if huduserobjects[1].radius <= 15 and huduserobjects[1].radius > 10:
								huduserobjects[1].radius = 15
							if huduserobjects[1].radius >= 25 and huduserobjects[1].radius > 15:
								huduserobjects[1].radius = 25
							huduserobjects[1].y = cell.rect.y + cell.rect.h/2
							huduserobjects[1].x = cell.rect.x + cell.rect.w/2
							huduserobjects[1].color = (sliders[0].saved_value, sliders[1].saved_value, sliders[2].saved_value)

				for i in sliders:
					i.draw(WIN)

				if userobject.visibility:
					userobject.draw(WIN)

				for textbox in textboxes_first:
					textbox.draw(WIN, pygame.mouse.get_pos(), mouse)

				for textbox in textboxes_second:
					textbox.draw(WIN, pygame.mouse.get_pos(), mouse)

				for i in huduserobjects:
					i.draw(WIN)
					i.visibility = True

				pygame.display.update()

			except Exception as e:
				print(e)

