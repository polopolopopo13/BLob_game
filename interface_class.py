import pygame

FPS = 5
#Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
ORANGE = pygame.Color('sienna3')
clock = pygame.time.Clock()
class Menus():
	def __init__(self, screen, screen_width, screen_height):
		'''
		screen : screen to display on # will pbly be updated to handle mutlticreen?
		'''
		self.screen = screen
		self.screen_width = screen_width
		self.screen_height = screen_height

	def gameover(self, screen_width, screen_height):
		waiting = True
		gameoverImage = pygame.image.load("images/game_over.jpg").convert()
		gameoverImage = pygame.transform.scale(gameoverImage, (200,200))
		gameoverRect = gameoverImage.get_rect()
		gameoverRect.center = (screen_width/2,screen_height/2)
		text1, text2 = Text(self.screen),Text(self.screen)
		text1.draw_text(self.screen, "YOU LOOSE" , 64, self.screen_width/2, self.screen_height/4, color=(135, 178, 204))
		text2.draw_text(self.screen, "Press a key to try again", 24, self.screen_width/2, self.screen_height*3/4, color=WHITE)
		self.screen.blit(gameoverImage,gameoverRect)
		pygame.display.flip()
		while waiting:
			clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					waiting = False

	def win_menu(self, screen_width, screen_height):
		waiting = True
		winImage = pygame.image.load("images/level_completed.jpg").convert()
		winImage = pygame.transform.scale(winImage, (200,200))
		winRect = winImage.get_rect()
		winRect.center = (screen_width/2,screen_height/2)
		text1, text2 = Text(self.screen),Text(self.screen)
		text1.draw_text(self.screen, "CONGRATULATIONS" , 64, self.screen_width/2, self.screen_height/4, color=(135, 178, 204))
		text2.draw_text(self.screen, "Press a key to ...will see", 24, self.screen_width/2, self.screen_height*3/4, color=WHITE)
		self.screen.blit(winImage,winRect)
		pygame.display.flip()
		while waiting:
			clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
				if event.type == pygame.KEYDOWN:
					waiting = False

	def intro(self, screen_width, screen_height ):
		logoImage = pygame.image.load("images/logo_PaPi.xcf").convert()
		logoRect = logoImage.get_rect()
		text1, text2, text3 = Text(self.screen), Text(self.screen), Text(self.screen)
		text1.draw_text(self.screen, "Welcome in Blobs World" , 50, self.screen_width/2, self.screen_height/4, color=(135, 178, 204))
		text2.draw_text(self.screen, "WORLD CODING STILL IN PROGRESS", 40, self.screen_width/2, self.screen_height*0.50, color=WHITE)
		text3.draw_text(self.screen, "Press a key to begin", 30, self.screen_width/2, self.screen_height*0.75, color=WHITE)
		self.screen.blit(logoImage,logoRect)
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

class Text():
	def __init__(self, screen):
		self.screen = screen
	
	def draw_text(self, screen, text, size, x, y, color=WHITE):
		font_name = pygame.font.match_font('linux bolunium')
		font = pygame.font.Font(font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x, y)
		self.screen.blit(text_surface, text_rect)


class Button():
	def __init__(self, pos, image, clickedImage = "" ):
		if clickedImage != "":
			self.baseImage =  pygame.image.load(image)
			self.clickedImage =  pygame.image.load(clickedImage)
		else:
			self.baseImage =  pygame.image.load(image)
			self.clickedImage =  pygame.image.load(image)
		self.image = self.baseImage
		self.rect = self.image.get_rect()
		self.place(pos)
		self.clicked = False
		
	def place(self, pos):
		self.rect.center = pos
		
	def collidePoint(self, pt):
		if self.rect.right > pt[0] and self.rect.left < pt[0]:
			if self.rect.bottom > pt[1] and self.rect.top < pt[1]:		
				return True
		return False
	
	def click(self, pt):
		if self.collidePoint(pt):
			self.clicked = True
			self.image = self.clickedImage
		else:
			self.clicked = False
			self.image = self.baseImage
			
	def release(self, pt):
		if self.clicked and self.collidePoint(pt):
			return True
		else:
			self.clicked = False
			self.image = self.baseImage
			return False
	
	def update(self, width, height):
		pass