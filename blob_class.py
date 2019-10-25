import random
import pygame
import numpy as np
import time
from power_class import Flush

class PnjBlob():
	def __init__(self, color, x_boundary, y_boundary):
		self.size = random.randrange(4, 8)
		self.color = color
		self.x_boundary = x_boundary
		self.y_boundary = y_boundary
		self.x = random.randrange(0, self.x_boundary)
		self.y = random.randrange(0, self.y_boundary)
		self.move_x = random.randrange(-4, 4)
		self.move_y = random.randrange(-4, 4)

	def move(self):
		self.x += self.move_x
		self.y += self.move_y

	def check_boundaries(self):
		if self.x < 0: self.x = self.x_boundary
		elif self.x > self.x_boundary: self.x = 0

		if self.y < 0: self.y = self.y_boundary
		elif self.y > self.y_boundary: self.y = 0

class UserBlob():
	def __init__(self, color, x_boundary, y_boundary, is_alive):
		self.size = 8
		self.alive = is_alive
		self.color = color
		self.x_boundary = x_boundary
		self.y_boundary = y_boundary
		self.x = random.randrange(0, self.x_boundary)
		self.y = random.randrange(0, self.y_boundary)
		self.power = dict()

	def user_move(self, direction):
		if direction == 'move_left':
			self.x -= 5
		if direction == 'move_right':
			self.x += 5
		if direction == 'move_down':
			self.y += 5
		if direction == 'move_up':
			self.y -= 5

	def check_boundaries(self):
		if self.x < 0: self.x = self.x_boundary
		elif self.x > self.x_boundary: self.x = 0

		if self.y < 0: self.y = self.y_boundary
		elif self.y > self.y_boundary: self.y = 0

	def flush(self, screen, color, player_x, player_y, player_size):
	#	self.size *= 0.75
		self.power['{}'.format(time.time())] = Flush(screen, color, player_x, player_y, player_size)

class InBox():
	def __init__(self, x, y , w, h, color, text):
		self.x = None
		self.y = None
		self.w = None
		self.h = None
		self.color = None
		self.text = None
'''
	def handle_mouse(self, event):
		if event.type == pygame.MOUSEBUTTOMLEFT:

'''