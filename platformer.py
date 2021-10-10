# Pygame platformer game tutorial by @TokyoEdTech

import pygame
import sys
import numpy as np
import random as rnd

pygame.init()
pygame.display.set_caption('Platformer Game')
clock = pygame.time.Clock()

WIDTH = 1200
HEIGHT = 800
GRAVITY = 1

BLACK = (0,0,0)
WHITE = (255, 255, 255)
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create classes
class Sprite():
	def __init__(self, x, y, width, height):
		# x,y are top left corner coordinates
		self.x = x
		self.y = y
		self.dx = 0
		self.dy = 0
		self.width = width
		self.height = height
		self.color = WHITE
		self.friction = 0.95 # 1 = no friction, 0 = all friction
		
	def goto(self, x, y):
		self.x = x
		self.y = y
		
	def render(self):
		pygame.draw.rect(screen, self.color, pygame.Rect(int(self.x-self.width/2.0), int(self.y-self.height/2.0), self.width, self.height))
					
	def is_aabb_collision(self, other):
		# Axis Aligned Bounding Box
		x_collision = (np.fabs(self.x - other.x)*2) < (self.width + other.width)
		y_collision = (np.fabs(self.y - other.y) * 2) < (self.height + other.height)
		return (x_collision and y_collision)
		
class Player(Sprite):
	def __init__(self, x, y, width, height):
		Sprite.__init__(self, x, y, width, height)
		self.color = GREEN
		
	def move(self):
		self.x += self.dx
		self.y += self.dy
		self.dy += GRAVITY
		
	def jump(self):
		self.dy -= 24
		
	def left(self):
		self.dx -= 6
		if self.dx < -12: # Limit the speed
			self.dx = -12
		
	def right(self):
		self.dx += 6
		if self.dx > 12:
			self.dx = 12
		
		
# Create game objects
player = Player(600, 0, 20, 40)
blocks = []
blocks.append(Sprite(600, 200, 400, 20))
blocks.append(Sprite(600, 400, 600, 20))
blocks.append(Sprite(1000, 500, 100, 200))
blocks.append(Sprite(600, 600, 1000, 20))
blocks.append(Sprite(200, 500, 100, 200))

# Main game loop	
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
			
		# Keyboards events
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player.left()
			elif event.key == pygame.K_RIGHT:
				player.right()
			elif event.key == pygame.K_SPACE:
				for block in blocks:
					if player.is_aabb_collision(block):
						player.jump()
						break
	
	# Move/Update objects
	player.move()
	
	# Check for collisions
	for block in blocks:
		if player.is_aabb_collision(block):
			if player.x < block.x - block.width/2.0 and player.dx > 0:
			# Player is to the left
				player.dx = 0
				player.x = block.x - block.width/2.0 - player.width/2.0
			
			elif player.x > block.x + block.width/2.0 and player.dx < 0:
			# Player is to the right
				player.dx = 0
				player.x = block.x + block.width/2.0 + player.width/2.0
			
			elif player.y < block.y:
			# Player is above
				player.dy = 0
				player.y = block.y - block.height/2.0 - player.height/2.0 + 1
				player.dx *= block.friction
			
			elif player.y > block.y:
			# Player is below
				player.dy = 0
				player.y = block.y + block.height/2.0 + player.height/2.0
				
	
	# Bordercheck
	if player.y > 600:
		player.goto(600,0)
	
	# Fill the background
	screen.fill(BLACK)
	
	# Render objects
	player.render()
	for block in blocks:
		block.render()
	
	# Flip the display
	pygame.display.flip()
	
	# Set the FPS
	clock.tick(30)
		
