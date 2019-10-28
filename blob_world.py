### NOTE THIS IS JUST FOR FUN AND KEEP DEVELOPPING SOME CODE

import pygame
import random
from blob_class import PnjBlob, UserBlob, VoidHole
from power_class import RedFlush, WhiteFlush, GreenFlush, BlueFlush
from interface_class import Menus, Text

import numpy as np
import time

pygame.font.init()

#Screen play
WIDTH = 800
HEIGHT = 600
size = WIDTH, HEIGHT

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Blob World')

#Timers
timer = time.time()
clock = pygame.time.Clock()

#Colors
WHITE = (255, 255, 255)
RED = (0, 0, 255)
BLUE = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = pygame.Color('sienna3')

#Iterators
STARTING_BLUE_BLOBS = 5
STARTING_RED_BLOBS = 5
STARTING_GREEN_BLOBS = 5

#Standards
size_decrease = 0
FPS = 40


def power_flush_contacts(player, blob_units):
	power_units = player.power
	for power_id, power in list(power_units.items()):#usefull when multi types power launched
		for blob_id, blob in list(blob_units.items()):
			if power_hit(power, blob, blob_id):
				#gonna create a new tuple for blob color to handle power effet...
				#if power and blob dominant color are same (Red, Blue or RED): blob is absorbed else, blob is pushed bash
				if power.color in [BLUE, GREEN, RED]:
					p_colormax_idx = max(power.color)#pb, it will return first max index occurence...
					p_idx = [i for i, j in enumerate(power.color) if j == p_colormax_idx]
					bl_colormax_idx = max(blob.color)#IDEM
					bl_idx = [k for k, l in enumerate(blob.color) if l == bl_colormax_idx]
					comon_idx = [m for m in bl_idx and p_idx] 
					if comon_idx:
						new_color = [0,0,0]
						for a in range(2):
							if a in p_idx and a in bl_idx:
								new_color[a]=0
							else:
								new_color[a]=blob.color[a]
						blob.color = tuple(new_color)


def power_hit(power, unit_collapsed, unit_collapsed_id):
	if np.linalg.norm(np.array([power.x, power.y])-np.array([unit_collapsed.x, unit_collapsed.y])) < (power.size + unit_collapsed.size):
		if unit_collapsed_id in power.blob_touched:
			return False
		else:
			power.blob_touched.append(unit_collapsed_id)
			return True

def blob_touching(b1, b2):
	return np.linalg.norm(np.array([b1.x, b1.y])-np.array([b2.x, b2.y])) < (b1.size + b2.size)

def vitesse_transfer(b1,b2):#imaginary
	b1_vvit = np.sqrt(b1.move_x**2+b1.move_y**2)*0.5*b1.size
	b2_vvit = np.sqrt(b2.move_x**2+b2.move_y**2)*0.5*b2.size
	new_move_x = b1.move_x*(b1_vvit/(b1_vvit+b2_vvit)) + b2.move_x*(b2_vvit/(b1_vvit+b2_vvit))
	new_move_y = b1.move_y*(b1_vvit/(b1_vvit+b2_vvit)) + b2.move_y*(b2_vvit/(b1_vvit+b2_vvit))
	return (-1 if -1>new_move_x<0 else int(new_move_x) or 1 -1 if 0<new_move_x<1 else int(new_move_x),
	-1 if -1>new_move_y<0 else int(new_move_y) or 1 -1 if 0<new_move_y<1 else int(new_move_y))

def collision_pnj_blob(blob_id, other_blob_id):
	#size also used as weight
	blob = blob_units[blob_id]
	other_blob = blob_units[other_blob_id]
	new_color = ()
	for c1, c2 in zip(blob.color, other_blob.color):
		coeff_c1 = blob.size/(blob.size + other_blob.size)
		coeff_c2 = other_blob.size/(blob.size + other_blob.size)
		i = np.round((c1*coeff_c1 + c2*coeff_c2), 3)
		new_color = new_color+(i,)
	if blob.size > other_blob.size:
		blob.size += other_blob.size
		blob.color = new_color
		blob.move_x, blob.move_y = vitesse_transfer(blob, other_blob)
		del(blob_units[other_blob_id])
	elif blob.size < other_blob.size:
		other_blob.size += blob.size
		other_blob.color = new_color
		other_blob.move_x, other_blob.move_y = vitesse_transfer(blob, other_blob)
		del(blob_units[blob_id])


def handle_user_collisions(player_blob, blob_units):
	for pnj_blob_id, pnj_blob in list(blob_units.items()):
		if blob_touching(player_blob, pnj_blob):
			if player_blob.size >= pnj_blob.size:
				player_blob.size += pnj_blob.size
				del blob_units[pnj_blob_id]
			elif player_blob.size < pnj_blob.size:
				player_blob.size = 0
				player_blob.alive = False
	return(player_blob, blob_units)


def handle_pnj_collisions(blob_dict):
	for blob_id, blob in list(blob_dict.items()):
		try:
			for other_blob_id, other_blob in list(blob_dict.items()):
				if blob_id == other_blob_id:
					pass
				else:
					if blob.size != other_blob.size: 
						if blob_touching(blob, other_blob):
							collision_pnj_blob(blob_id, other_blob_id)
					else:
						pass
		except:
			pass
	return blob_dict

def handle_keyboard(event):
	global user_pressing_left, user_pressing_right, user_pressing_up, user_pressing_down
	if event.type == pygame.KEYDOWN:
		if event.key == pygame.K_LEFT:
			user_pressing_left = True
		elif event.key == pygame.K_RIGHT:
			user_pressing_right = True
		elif event.key == pygame.K_UP:
			user_pressing_up = True
		elif event.key == pygame.K_DOWN:
			user_pressing_down = True


	elif event.type == pygame.KEYUP:
		if event.key == pygame.K_LEFT:
			user_pressing_left = False
		elif event.key == pygame.K_RIGHT:
			user_pressing_right = False
		elif event.key == pygame.K_UP:
			user_pressing_up = False
		elif event.key == pygame.K_DOWN:
			user_pressing_down = False

	#return user_pressing_left, press_right, press_down, press_up

def displaying_units(player, blob_units, void_units, _whity_units):
	for blob_id in blob_units:
		blob = blob_units[blob_id]
		pygame.draw.circle(screen, blob.color, [
						   blob.x, blob.y], int(round(blob.size)))

	for void_id in void_units:
		void = void_units[void_id]
		pygame.draw.circle(screen, void.color, [
						   void.x, void.y], int(round(void.size)))

	for power_id, power in list(player.power.items()):#dict to list cause might be modified during iteration
		power.update()
		power_flush_contacts(player, blob_units)
		pygame.draw.circle(screen, power.color, (power.x, power.y), int(round(power.size)), 1)
		if power.size >= power.initial_size*2 and power.size >= 50:
			del player.power[power_id]
	
	for _whity_id, _whity in list(_whity_units.items()):
		pygame.draw.circle(screen, _whity.color, (_whity.x, _whity.y), int(round(_whity.size)), 1)

	pygame.draw.circle(screen, player.color, [
					   player.x, player.y], int(round(player.size)))

def draw_text(surface, text, size, x, y, color=WHITE):
    font_name = pygame.font.match_font('linux bolunium')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def menu_start():
	logoImage = pygame.image.load("images/logo_PaPi.xcf").convert()
	logoRect = logoImage.get_rect()
	draw_text(screen, "Welcome in Blobs World" , 64, WIDTH/2, HEIGHT/4, color=ORANGE)
	line_return=0
	for line in ["WORLD CODING STILL IN PROGRESS"]:
		line_return +=25
		draw_text(screen, line, 30, WIDTH/2, (HEIGHT/2)+line_return)
	draw_text(screen, "Press a key to begin", 24, WIDTH/2, HEIGHT*3/4, color=GREEN)
	screen.blit(logoImage,logoRect)
	pygame.display.flip()
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				waiting = False


def menu_win():
	''''''

#CREATE Player and Pnjs

def create_characs():
	player1 =  UserBlob(WHITE, WIDTH, HEIGHT, is_alive=True)
	void_units = dict()
	void_units['void1'] = VoidHole((255,255,0), WIDTH, HEIGHT)

	blob_units = dict()
	for i in range(STARTING_RED_BLOBS):
		blob_units['red{}'.format(i)] = PnjBlob(RED, WIDTH, HEIGHT)

	for i in range(STARTING_BLUE_BLOBS):
		blob_units['blue{}'.format(i)] = PnjBlob(BLUE,WIDTH, HEIGHT)

	for i in range(STARTING_GREEN_BLOBS):
		blob_units['green{}'.format(i)] = PnjBlob(GREEN, WIDTH, HEIGHT)

	power_units = dict()
	_whity_units = dict()
	mainloop_count = 0
	return player1, blob_units, void_units, mainloop_count, power_units, _whity_units


user_pressing_left=bool()
user_pressing_right=bool()
user_pressing_up=bool()
user_pressing_down=bool()

## MAIN LOOP
game_over = False
start = True
running = True

player1, blob_units, void_units, mainloop_count, power_units, _whity_units = create_characs()
while running:
	if start:
		menu_start()
		start=False
	if game_over:
		menu = Menus(screen, WIDTH, HEIGHT)
		menu.gameover(WIDTH, HEIGHT)
		game_over=False
		#RECREATE Fundamental elements
		player1, blob_units, void_units, mainloop_count, power_units, _whity_units = create_characs()
		power_units = dict()
		_whity_units = dict()

		user_pressing_left=bool()
		user_pressing_right=bool()
		user_pressing_up=bool()
		user_pressing_down=bool()
	
	clock.tick(FPS)##keep loop running at 40 FPS
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				player1.power[f'flushwhite_{time.time()}'] = WhiteFlush(screen, player1.x, player1.y, player1.size)
			elif event.key == pygame.K_p:
				player1.power[f'flushred_{time.time()}'] = RedFlush(screen, player1.x, player1.y, player1.size)
			else: handle_keyboard(event)
		elif event.type == pygame.KEYDOWN: handle_keyboard(event)

	if user_pressing_left:
		player1.user_move(direction = 'move_left')
	if user_pressing_right:
		player1.user_move(direction = 'move_right')
	if user_pressing_up:
		player1.user_move(direction = 'move_up')
	if user_pressing_down:
		player1.user_move(direction = 'move_down')
	
	#Player and blob boundaries movement
	player1.check_boundaries()
	for blob_id in blob_units:
		blob_units[blob_id].move()
		blob_units[blob_id].check_boundaries()
	for void_id in void_units:
		void_units[void_id].move()
		void_units[void_id].check_boundaries()

	#whity blobs
	if mainloop_count % 30 == 0 and len(_whity_units)<=10:
		for void_id, void in list(void_units.items()):
			_whity_units['whity_{}_{}'.format(void, mainloop_count)] = void.creating(WIDTH,HEIGHT)
	if _whity_units:
		for _whity_id, _whity in list(_whity_units.items()):
			_whity.move()
			_whity.check_boundaries()

	##collisions
	blob_units = handle_pnj_collisions(blob_units)
	player1, blob_units = handle_user_collisions(player1, blob_units)
	if not blob_units:
		print('win')
		pygame.quit()
		quit()
	
	if player1.size >= size_decrease:
		player1.size -= size_decrease
	elif player1.size < size_decrease:
		player1.alive = False
	if not player1.alive:
		game_over=True

	#power_flush_contacts(player1, blob_units)
	screen.fill(BLACK)
	displaying_units(player1, blob_units, void_units, _whity_units)
	mainloop_count += 1	
	pygame.display.update()