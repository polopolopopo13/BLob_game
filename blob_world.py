### NOTE THIS IS JUST FOR FUN AND KEEP DEVELOPPING SOME CODE

import pygame
import random
from blob_class import PnjBlob, UserBlob, VoidHole, Collapsing
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
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = pygame.Color('sienna3')

#Iterators
STARTING_BLUE_BLOBS = 5
STARTING_RED_BLOBS = 5
STARTING_GREEN_BLOBS = 5

#Standards
size_decrease = 0
FPS = 30

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

def blob_touching(b1, b2):
	return np.linalg.norm(np.array([b1.x, b1.y])-np.array([b2.x, b2.y])) < (b1.size + b2.size)

def handle_user_collisions(player_blob, blob_units):
	for pnj_blob_id, pnj_blob in list(blob_units.items()):
		if blob_touching(player_blob, pnj_blob):
			if player_blob.size >= pnj_blob.size:
				player_blob.size += pnj_blob.size
				player_blob.mass += pnj_blob.mass
				del blob_units[pnj_blob_id]
			elif player_blob.size < pnj_blob.size:
				player_blob.size = 0
				player_blob.alive = False
	return(player_blob, blob_units)


def handle_pnj_collisions(blob_id, blob_units):
	for other_blob_id in blob_units.copy():
		if blob_id == other_blob_id:
			pass
		else:
			try:
				if blob_touching(blob_units[blob_id], blob_units[other_blob_id]):
					Collapsing(blob_id, other_blob_id,blob_units)
			except: pass
	#return blob_units

def displaying_units(player, blob_units, void_units, _whity_units):
	#Player and blob movement
	for blob_id in list(blob_units.copy()):
		try:
			blob = blob_units[blob_id]
			blob.move()
			handle_pnj_collisions(blob_id, blob_units)
			pygame.draw.circle(screen, blob.color, [
								blob.x, blob.y], int(round(blob.size)))
		except KeyError: pass #cause iterating on a changing size dict
	player, blob_units = handle_user_collisions(player, blob_units)

	#powers
	for power_id, power in list(player.power.items()):#dict to list to handle the length change during iteration
		power.update(blob_units)
		if power.size >= power.initial_size*2 and power.size >= 50:
			del player.power[power_id]

	#whity blobs and void
	for void_id in void_units:
		void = void_units[void_id]
		void.move()
		if blob_units :
			for id in blob_units:
				void.gravity_modif(blob_units[id])
		if player: void.gravity_modif(player)
		pygame.draw.circle(screen, void.color, [
				void.x, void.y], int(round(void.size)))

	if mainloop_count % 100 == 0 and len(_whity_units)<=10:
		for void_id, void in list(void_units.items()):
			_whity_units['whity_{}_{}'.format(void, mainloop_count)] = void.creating(WIDTH,HEIGHT)
	if _whity_units:
		for _whity_id, _whity in list(_whity_units.items()):
			_whity.move()
			pygame.draw.circle(screen, _whity.color, (_whity.x, _whity.y), int(round(_whity.size)), 1)
	
	if player1.size >= size_decrease:
		player1.size -= size_decrease
	elif player1.size < size_decrease:
		player1.alive = False
	if not player1.alive:
		global game_over
		game_over = True

	pygame.draw.circle(screen, player.color, [
					player.x, player.y], int(round(player.size)))


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
		menu = Menus(screen, WIDTH, HEIGHT)
		menu.intro(WIDTH, HEIGHT)
		start = False
	if game_over:
		menu = Menus(screen, WIDTH, HEIGHT)
		menu.gameover(WIDTH, HEIGHT)
		game_over = False
		#RECREATE Fundamental elements
		player1, blob_units, void_units, mainloop_count, power_units, _whity_units = create_characs()
		power_units = dict()
		_whity_units = dict()

		user_pressing_left=bool()
		user_pressing_right=bool()
		user_pressing_up=bool()
		user_pressing_down=bool()
	
	clock.tick(FPS)##keep loop running at 40 FPS
	#KEYBOARD EVENTS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_SPACE:
				player1.power[f'flushwhite_{time.time()}'] = WhiteFlush(screen, player1.x, player1.y, player1.size)
			elif event.key == pygame.K_v:
				player1.power[f'flushred_{time.time()}'] = RedFlush(screen, player1.x, player1.y, player1.size)
			elif event.key == pygame.K_b:
				player1.power[f'flushgreen_{time.time()}'] = GreenFlush(screen, player1.x, player1.y, player1.size)
			elif event.key == pygame.K_n:
				player1.power[f'flushblue_{time.time()}'] = BlueFlush(screen, player1.x, player1.y, player1.size)
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

	screen.fill(BLACK)
	displaying_units(player1, blob_units, void_units, _whity_units)
	mainloop_count += 1	
	pygame.display.update()
