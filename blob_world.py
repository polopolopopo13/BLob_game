### NOTE THIS IS JUST FOR FUN AND KEEP DEVELOPPING SOME CODE

import pygame
import random
from blob_class import PnjBlob, UserBlob
#Flush is imported in blob_class.py
from interface_class import Button
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
STARTING_BLUE_BLOBS = 10
STARTING_RED_BLOBS = 10
STARTING_GREEN_BLOBS = 10

#Standards
size_decrease = 0.04
FPS = 40


def power_flush_contacts(player, blob_units):
	power_units = player.power
	for power_id, power in list(power_units.items()):#usefull when multi types power launched
		for blob_id, blob in list(blob_units.items()):
			if power_hit(power, blob):
				player.size += blob.size/2
				blob.size /= 2
			if blob.size <=1:
				del blob_units[blob_id]


def power_hit(power, unit_collapsed):
	# returning True if collapsed or False
	return np.linalg.norm(np.array([power.x, power.y])-np.array([unit_collapsed.x, unit_collapsed.y])) < (power.size + unit_collapsed.size) 
	#need find something not to multi hit each blob in 1 cast power

def blob_touching(b1, b2):
	# returning True or False
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
		'''elif event.key == pygame.K_ESCAPE:
			game_pause()'''

	elif event.type == pygame.KEYUP:
		if event.key == pygame.K_LEFT:
			user_pressing_left = False
		elif event.key == pygame.K_RIGHT:
			user_pressing_right = False
		elif event.key == pygame.K_UP:
			user_pressing_up = False
		elif event.key == pygame.K_DOWN:
			user_pressing_down = False
		'''elif event.key == pygame.K_ESCAPE:
			pressed_pause = False'''
	#return user_pressing_left, press_right, press_down, press_up

def displaying_units(player, blob_units):
	for blob_id in blob_units:
		blob = blob_units[blob_id]
		pygame.draw.circle(screen, blob.color, [
						   blob.x, blob.y], int(round(blob.size)))	
	for power_id, power in list(player.power.items()):#dict to list cause might be modified during iteration
		power.update()
		pygame.draw.circle(screen, power.color, (power.x, power.y), int(round(power.size)), 1)
		power_flush_contacts(player, blob_units)
		if power.size >= power.initial_size*2 and power.size >= 50:
			del player.power[power_id]
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
	for line in ["To clean level eat each blob.", "If a blob bigger than you is eaten, you loose.", 
	"Arrows keys to move, space to use flush power."]:
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

def menu_gameover():
	gameoverImage = pygame.image.load("images/game_over.jpg").convert()
	gameoverImage = pygame.transform.scale(gameoverImage, (200,200))
	gameoverRect = gameoverImage.get_rect()
	gameoverRect.center = (WIDTH/2,HEIGHT/2)
	draw_text(screen, "YOU LOOSE" , 64, WIDTH/2, HEIGHT/4, color=(135, 178, 204))
	draw_text(screen, "Press a key to try again", 24, WIDTH/2, HEIGHT*3/4, color=WHITE)
	screen.blit(gameoverImage,gameoverRect)
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
player1 =  UserBlob(WHITE, WIDTH, HEIGHT, is_alive=True)

blob_units = dict()
for i in range(STARTING_RED_BLOBS):
	blob_units['red{}'.format(i)] = PnjBlob(RED, WIDTH, HEIGHT)

for i in range(STARTING_BLUE_BLOBS):
	blob_units['blue{}'.format(i)] = PnjBlob(BLUE,WIDTH, HEIGHT)

for i in range(STARTING_GREEN_BLOBS):
	blob_units['green{}'.format(i)] = PnjBlob(GREEN, WIDTH, HEIGHT)

power_units = dict()

user_pressing_left=bool()
user_pressing_right=bool()
user_pressing_up=bool()
user_pressing_down=bool()

## MAIN LOOP
game_over = False
start = True
running = True

while running:
	if start:
		menu_start()
		start=False
	if game_over:
		menu_gameover()
		game_over=False
		#RECREATE Fundamental elements
		player1 =  UserBlob(WHITE, WIDTH, HEIGHT, is_alive=True)

		blob_units = dict()
		for i in range(STARTING_RED_BLOBS):
			blob_units['red{}'.format(i)] = PnjBlob(RED, WIDTH, HEIGHT)

		for i in range(STARTING_BLUE_BLOBS):
			blob_units['blue{}'.format(i)] = PnjBlob(BLUE,WIDTH, HEIGHT)

		for i in range(STARTING_GREEN_BLOBS):
			blob_units['green{}'.format(i)] = PnjBlob(GREEN, WIDTH, HEIGHT)

		power_units = dict()
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
				player1.flush(screen, player1.color, player1.x, player1.y, player1.size)
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

	'''for power_id, power in list(player1.power.items()):#dict
		player1.power[power_id].update()
		pygame.draw.circle(screen, power.color, (power.x, power.y), int(round(power.size)), 1)
		
		if player1.power[power_id].size >= power.initial_size*2 and player1.power[power_id].size >= 100:
			del player1.power[power_id]
		pygame.display.update()'''
	
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
	displaying_units(player1, blob_units)
	
	pygame.display.update()