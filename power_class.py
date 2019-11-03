import pygame

#Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = pygame.Color('sienna3')

class Flush():
	def __init__(self, screen, player_x, player_y, player_size):
		self.size = 6
		self.color = None
		self.x = player_x
		self.y = player_y
		self.screen = screen
		self.size = player_size
		self.initial_size = player_size
		self.blob_touched = []

	def update(self):
		self.size += 1
		self.to_display(self.screen)
	
	def to_display(self, screen):
		pygame.draw.circle(screen, self.color, (self.x, self.y), self.size, 2)
	
		'''def power_flush_contacts(player, blob_units):
	power_units = player.power
	for power_id, power in list(power_units.items()):#usefull when multi types power launched
		for blob_id, blob in list(blob_units.items()):
			if power_hit(power, blob):
				player.size += blob.size/2
				blob.size /= 2
			if blob.size <=1:
				del blob_units[blob_id]
	'''
class WhiteFlush(Flush):
	def __init__(self, screen, player_x, player_y, player_size):
		super().__init__(screen, player_x, player_y, player_size)
		"""
		player_x = absis of player when he casted the spell
		player_y = ordonate of player when he caster the spell
		"""
		self.color = WHITE

class RedFlush(Flush):
	def __init__(self, screen, player_x, player_y, player_size):
		super().__init__(screen, player_x, player_y, player_size)
		"""
		player_x = absis of player when he casted the spell
		player_y = ordonate of player when he caster the spell
		"""
		self.color = RED

class BlueFlush(Flush):
	def __init__(self, screen, player_x, player_y, player_size):
		super().__init__(screen, player_x, player_y, player_size)
		"""
		player_x = absis of player when he casted the spell
		player_y = ordonate of player when he caster the spell
		"""
		self.color = BLUE

class GreenFlush(Flush):
	def __init__(self, screen, player_x, player_y, player_size):
		super().__init__(screen, player_x, player_y, player_size)
		"""
		player_x = absis of player when he casted the spell
		player_y = ordonate of player when he caster the spell
		"""
		self.color = GREEN