# Space Invaders Tutorial by @TokyoEdTech

import turtle
import os
import random
import numpy as np
import platform

random.seed(0)

if platform.system() == 'Windows':
	try:
		import winsound
	except:
		print('ERROR: winsound module not available.')

# Set up the screen
wn = turtle.Screen()
wn.bgcolor('black')
wn.title('Space Invaders')
wn.bgpic('images/space_background.gif')
wn.tracer(0) #Shuts off the screen updates

# Register the shape
wn.register_shape('images/space-invader-enemy.gif')
wn.register_shape('images/space-ship.gif')

# Draw a border
border_pen = turtle.Turtle()
border_pen.speed(0) #fastest
border_pen.color('white')
border_pen.penup()
border_pen.setposition(-300,-300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
	border_pen.fd(600)
	border_pen.lt(90)
border_pen.hideturtle()

#Set the score to 0
score = 0

#Draw the score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color('white')
score_pen.penup()
score_pen.setposition(-290,270)
scorestring = 'Score: {}'.format(score)
score_pen.write(scorestring, False, align='left', font=('Arial',12, 'normal'))
score_pen.hideturtle()

#Create the player turtle class
class Player(turtle.Turtle):
	def __init__(self):
		turtle.Turtle.__init__(self)
		self.shape('images/space-ship.gif')
		self.penup()
		self.speed(0)
		self.setposition(0,-250)
		self.setheading(90)
		self.speed = 0

	#Move the player left and right
	def move_left(self):
		player.speed = -0.25
		
	def move_right(self):
		player.speed = 0.25

		
	def move_player(self):
		x = player.xcor() #Old position
		x += player.speed
	#the lowest value for x must be -280
		if x < -280:
			x = -280	
	#the highest value for x must be 280
		if x > 280:
			x = 280
		player.setx(x) #New position
	
	def fire_bullet(self):
		#define bulletstate as global if it needs changed
		global bulletstate #any changes in the function are reflected outside the funcion
		if bulletstate == 'ready':
		#move the bullet to the just above the player
			play_sound('sounds/laser.wav')
			bulletstate='fire'
			x = player.xcor()
			y = player.ycor()
			bullet.setposition(x,y+10)
			bullet.showturtle()

class Enemy(turtle.Turtle):
	def __init__(self,x,y):
		turtle.Turtle.__init__(self)
		self.shape('images/space-invader-enemy.gif')
		self.penup()
		self.speed(0)
		self.speed = 0.02
		self.goto(x,y)
		
player = Player()

#define bullet state
#ready: ready to fire
#fire: bullet is firing
bulletstate = 'ready'


#Choose a number of enemies
Nenemies = 30

enemies = []

enemy_ctr = 0
enemy_xi = -225
enemy_yi = 250
	
for i in range(Nenemies):
	x = enemy_xi + (50*enemy_ctr)
	y = enemy_yi
	enemies.append(Enemy(x,y))
	# Update the enemy number
	enemy_ctr += 1
	if enemy_ctr == 10:
		enemy_yi -= 50
		enemy_ctr = 0

#Create the big enemy
big_enemy = turtle.Turtle()
big_enemy.color('red')
big_enemy.shape('square')
big_enemy.penup()
big_enemy.speed(0)
big_enemy.setposition(-275,250)
big_enemy.hideturtle()
big_enemy_speed = 1.25

#create the player's bullet

bullet = turtle.Turtle()
bullet.color('yellow')
bullet.shape('triangle')
bullet.penup() #do not draw a line when moving
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle() #bullet hidden at the beginning

bulletspeed = 0.5


def isCollision(t1, t2):
	distance = np.sqrt((t1.xcor()-t2.xcor())**2+(t1.ycor()-t2.ycor())**2)
	if distance < 15:
		return True #there is a collision
	else:
		return False

def play_sound(soundfile, time = 0):
	# Windows
	if platform.system() == 'Windows':
		winsound.PlaySound(soundfile, winsound.SND_ASYNC)
	# Linux
	elif platform.system() == 'Linux':
		os.system('aplay -q {}&'.format(soundfile))
	# Mac
	else:
		os.system('afplay {}&'.format(soundfile))
	
	# Repeat sound
	if time > 0:
		turtle.ontimer(lambda: play_sound(soundfile, time), t=int(time*1000))

#Create keyboard bindings
wn.listen()
wn.onkeypress(player.move_left, 'Left') #When left arrow key is pressed, it 
				#calls the function 'move_left'
wn.onkeypress(player.move_right, 'Right') #Same but for right arrow
wn.onkeypress(player.fire_bullet, 'space')

# Play background music
#play_sound('sounds/bgm.mp3', 119)

#Main game loop
while True:
	wn.update()
	rand = random.randint(0,100)
	player.move_player()
	for enemy in enemies:
		#Move the enemy
		x = enemy.xcor()
		x += enemy.speed
		enemy.setx(x)

		#Move all the enemies back and down
		if enemy.xcor() > 280:
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)
				e.speed *= -1 #Inverse the velocity
			
		if enemy.xcor() < -280:
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)
				e.speed *= -1 #Inverse the velocity
			
		#Check for a collision between bullet and enemy
		if isCollision(bullet, enemy):
			play_sound('sounds/explosion.wav')
			#Reset the bullet
			bullet.hideturtle()
			bulletstate = 'ready'
			bullet.setposition(0,-400)
			#Reset the enemy
			enemy.setposition(0,10000)
			#Update the score
			score += 10
			scorestring = 'Score: {}'.format(score)
			score_pen.clear()
			score_pen.write(scorestring, False, align='left', font=('Arial',14, 'normal'))
		
		#Collision between player and enemy (Gave Over)
		if isCollision(enemy, player):
			play_sound('sounds/explosion.wav')
			player.hideturtle()
			enemy.hideturtle()
			print('Game Over!')
			break
	
	#Big enemy shows up
	if rand == 5:
		big_enemy.showturtle()
		X = big_enemy.xcor()
		X += big_enemy_speed
		big_enemy.setx(X)
		if big_enemy.xcor() > 275:
			big_enemy.hideturtle()
			big_enemy.setx(-275)
		if isCollision(bullet, big_enemy):
			play_sound('sounds/explosion.wav')
			big_enemy.hideturtle()
			big_enemy.setx(-275)
			#Reset the bullet
			bullet.hideturtle()
			bulletstate = 'ready'
			bullet.setposition(0,-400)
			#Update the score
			score += 50
			scorestring = 'Score: {}'.format(score)
			score_pen.clear()
			score_pen.write(scorestring, False, align='left', font=('Arial',14, 'normal'))
		
	#move the bullet
	if bulletstate == 'fire':
		y = bullet.ycor()
		y += bulletspeed
		bullet.sety(y)

	#check if the bullet has gone to the top
	if bullet.ycor() > 275:
		bullet.hideturtle()
		bullet.sety(player.ycor()+10) #the bullet returns at the initial position
		bulletstate = 'ready'
	
