import pygame

class Flush():
	def __init__(self, screen, color, player_x, player_y, player_size):
		self.size = 6
		self.color = color
		self.x = player_x
		self.y = player_y
		self.screen = screen
		self.size = player_size
		self.initial_size = player_size

	def update(self):
		self.size += 1
	
	def to_display(self, screen):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, 2)
