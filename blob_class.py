import random
import pygame
import numpy as np
import time
import math
WIDTH = 800
HEIGHT = 600
size = WIDTH, HEIGHT

screen = pygame.display.set_mode(size)
G = 6.674#*10e-11


class Collapsing():
	def __init__(self, id1, id2, dict_unit):
		self.u1 = dict_unit[id1]
		self.u2 = dict_unit[id2]
		self.update(id1, id2, dict_unit)

	def update(self, id1, id2, dict_unit):
		new_color = ()
		if self.u1.size == self.u2.size: return
		for c1, c2 in zip(self.u1.color, self.u2.color):
			coeff_c1 = self.u1.size/(self.u1.size + self.u2.size)
			coeff_c2 = self.u2.size/(self.u1.size + self.u2.size)
			i = np.round((c1*coeff_c1 + c2*coeff_c2), 3)
			new_color = new_color+(i,)
		if self.u1.size *self.u1.mass  > self.u2.size*self.u2.mass:
			self.u1.color = new_color
			self.u1.speed_x, self.u1.speed_y, self.u1.angle_x, self.u1.angle_y = self.transfer(self.u1, self.u2)
			self.u1.size += self.u2.size
			self.u1.mass += self.u2.mass
			del dict_unit[id2]
		elif self.u1.size*self.u1.mass < self.u2.sizeother_blob.mass:
			self.u2.color = new_color
			self.u2.speed_x, self.u2.speed_y, self.u2.angle_x, self.u2.angle_y = self.transfer(self.u1, self.u2)
			self.u2.size += self.u1.size
			self.u2.mass += self.u1.mass
			del dict_unit[id1]

	def transfer(self, b1,b2):#imaginary
		b1_cinetik_x = 0.5*b1.size*b1.speed_x**2
		b2_cinetik_x = 0.5*b2.size*b2.speed_x**2
		enrj_b1b2_x = b1_cinetik_x + b2_cinetik_x

		b1_cinetik_y = 0.5*b1.size*b1.speed_y**2
		b2_cinetik_y = 0.5*b2.size*b2.speed_y**2
		enrj_b1b2_y = b1_cinetik_y + b2_cinetik_y

		#speed (size seen as weight to make it simple for now)
		new_speed_x = b1.speed_x*b1_cinetik_x/enrj_b1b2_x + b2.speed_x*b2_cinetik_x/enrj_b1b2_x
		new_speed_y= b1.speed_y*b1_cinetik_y/enrj_b1b2_y + b2.speed_y*b2_cinetik_y/enrj_b1b2_y
		#angle
		new_angle_x = b1.angle_x*b1_cinetik_x/enrj_b1b2_x + b2.angle_x*b2_cinetik_x/enrj_b1b2_x
		new_angle_y = b1.angle_y*b1_cinetik_y/enrj_b1b2_y + b2.angle_y*b2_cinetik_y/enrj_b1b2_y
		return new_speed_x, new_speed_y, new_angle_x, new_angle_y


class PnjBlob():
	def __init__(self, color, x_boundary, y_boundary):
		self.size = random.randrange(4, 8)
		self.color = color
		self.x_boundary = x_boundary
		self.y_boundary = y_boundary
		self.x = random.randrange(0, self.x_boundary)
		self.y = random.randrange(0, self.y_boundary)
		self.speed_x = 4#random.randrange(-4, 4)
		self.speed_y = 4#random.randrange(-4, 4)
		self.angle_x = random.uniform(0, math.pi*2)#create a random angle between 0 and 2 * pi
		self.angle_y = random.uniform(0, math.pi*2)#IDEM
		self.move_x = math.sin(self.angle_x)*self.speed_x
		self.move_y = math.cos(self.angle_y)*self.speed_y
		self.mass = 100

	def move(self):
		self.x += int(self.move_x)
		self.y += int(self.move_y)
		self.check_boundaries()

	def check_boundaries(self):
		if self.x < 0: self.x = self.x_boundary
		elif self.x > self.x_boundary: self.x = 0

		if self.y < 0: self.y = self.y_boundary
		elif self.y > self.y_boundary: self.y = 0


#class VoidHole():
class VoidHole(PnjBlob):
	def __init__(self, color, x_boundary, y_boundary):
		self.size = 11
		self.color = color
		self.x_boundary = x_boundary
		self.y_boundary = y_boundary
		self.x = int(x_boundary/2) #random.randrange(0, self.x_boundary)
		self.y = int(y_boundary/2) #random.randrange(0, self.y_boundary)
		self.speed_x = 4
		self.speed_y = 4
		self.angle_x = math.pi
		self.angle_y = math.pi/2
		self.attractiv = True
		self.mass = 300
		self.move_x = math.sin(self.angle_x)*self.speed_x
		self.move_y = math.cos(self.angle_y)*self.speed_y

	def creating(self, x_boundary, y_boundary):
		#self.size *= 0.95
		_whithy = PnjBlob((255,255,255), x_boundary, y_boundary)
		_whithy.size = 3
		_whithy.x = self.x
		_whithy.y = self.y
		return _whithy

	def gravity_modif(self, other):
		dx = other.x - self.x
		dy = other.y - self.y
		dist = math.hypot(dx, dy)
		if dist == 0:
			return
		else:
			gravit_area = G*self.mass*other.mass/dist**2
			if 0<dist<=gravit_area and gravit_area>2:
				#pygame.draw.circle(screen, self.color, (self.x, self.y), int(gravit_area), 1)
				other.x -= int(dx*4/dist)
				other.y -= int(dy*4/dist)
			else: pass


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
		self.be_attracted = True
		self.speed_x = 5
		if self.speed_x > 5 :
			self.speed_x *= 0.9
		elif self.speed_x < 5:
			self.speed_x = 5
		self.speed_y = 5
		if self.speed_y > 5 :
			self.speed_y *= 0.9
		elif self.speed_y < 5:
			self.speed_y = 5
		self.angle_x = math.pi/2
		self.angle_y = 0
		self.mass = 150

	def user_move(self, direction):
		if direction == 'move_left':
			self.x -= int(math.sin(self.angle_x)*self.speed_x)
		if direction == 'move_right':
			self.x += int(math.sin(self.angle_x)*self.speed_x)
		if direction == 'move_down':
			self.y += int(math.cos(self.angle_y)*self.speed_y)
		if direction == 'move_up':
			self.y -= int(math.cos(self.angle_y)*self.speed_y)
		self.check_boundaries()

	def check_boundaries(self):
		if self.x < 0: self.x = self.x_boundary
		elif self.x > self.x_boundary: self.x = 0

		if self.y < 0: self.y = self.y_boundary
		elif self.y > self.y_boundary: self.y = 0


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