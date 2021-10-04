#Space Invaders - Part 1
#Set up the screen

import turtle
import os
import random
import numpy as np

#Set up the screen
wn = turtle.Screen()
wn.bgcolor('black')
wn.title('Space Invaders')
wn.bgpic('images/space_background.gif')

#Register the shape
turtle.register_shape('images/space-invader-enemy.gif')
turtle.register_shape('images/space-ship.gif')

#Draw a border
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
score_pen.setposition(-290,280)
scorestring = 'Score: %s' %score
score_pen.write(scorestring, False, align='left', font=('Arial',14, 'normal'))
score_pen.hideturtle()

#Create the player turtle
player = turtle.Turtle()
player.color('blue')
player.shape('images/space-ship.gif')
player.penup()
player.speed(0)
player.setposition(0,-250)
player.setheading(90)

#Space Invaders - Part 2
#Move the player

playerspeed = 15

#Move the player left and right
def move_left():
	x = player.xcor() #Old position
	x -= playerspeed
#the lowest value for x must be -280
	if x < -280:
		x = -280
	player.setx(x) #New position
	
def move_right():
	x = player.xcor() #Old position
	x += playerspeed
#the highest value for x must be 280
	if x > 280:
		x = 280
	player.setx(x)
	
#Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, 'Left') #When left arrow key is pressed, it 
				#calls the function 'move_left'
turtle.onkey(move_right, 'Right') #Same but for right arrow

'''
#Space Invaders - Part 3
#Create the Enemy and move left / right / down

enemy = turtle.Turtle()
enemy.color('red')
enemy.shape('circle')
enemy.penup()
enemy.speed(0)
enemy.setposition(-200,250)
'''

#Space Invaders - Part 6
#Add enemies

#Choose a number of enemies
number_of_enemies = 5

#Create an empty list
enemies = []

#Add enemies to the list
for i in range(number_of_enemies):
#Create an enemy
	enemies.append(turtle.Turtle())
	
for enemy in enemies:

	enemy.shape('images/space-invader-enemy.gif')
	enemy.penup()
	enemy.speed(0)
	x = random.randint(-200,200)
	y = random.randint(100,250)
	enemy.setposition(x,y)

enemyspeed = 2

#Create the big enemy
big_enemy = turtle.Turtle()
big_enemy.color('red')
big_enemy.shape('square')
big_enemy.penup()
big_enemy.speed(0)
big_enemy.setposition(-275,250)
big_enemy.hideturtle()
big_enemy_speed = 10

#Space Invaders - Part 4
#Create the Player Bullet and Fire with the Space Bar

#create the player's bullet

bullet = turtle.Turtle()
bullet.color('yellow')
bullet.shape('triangle')
bullet.penup() #do not draw a line when moving
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5,0.5)
bullet.hideturtle() #bullet hidden at the beginning

bulletspeed = 20

#define bullet state
#ready: ready to fire
#fire: bullet is firing

bulletstate = 'ready'

def fire_bullet():
	#define bulletstate as global if it needs changed
	global bulletstate #any changes in the function are reflected outside the funcion
	if bulletstate == 'ready':
	#move the bullet to the just above the player
		os.system('aplay laser.wav&')
		bulletstate='fire'
		x = player.xcor()
		y = player.ycor()
		bullet.setposition(x,y+10)
		bullet.showturtle()
	
turtle.onkey(fire_bullet, 'space')

#Space Invaders - Part 5
#Collisions

def isCollision(t1, t2):
	distance = np.sqrt((t1.xcor()-t2.xcor())**2+(t1.ycor()-t2.ycor())**2)
	if distance < 15:
		return True #there is a collision
	else:
		return False

#Main game loop
while True:
	rand = random.randint(0,10)
	for enemy in enemies:
		#Move the enemy
		x = enemy.xcor()
		x += enemyspeed
		enemy.setx(x)

		#Move all the enemies back and down
		if enemy.xcor() > 280:
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)
			enemyspeed *= -1 #Inverse the velocity
			
		if enemy.xcor() < -280:
			for e in enemies:
				y = e.ycor()
				y -= 40
				e.sety(y)
			enemyspeed *= -1 #Inverse the velocity
			
		#Check for a collision between bullet and enemy
		if isCollision(bullet, enemy):
			os.system('aplay explosion.wav&')
			#Reset the bullet
			bullet.hideturtle()
			bulletstate = 'ready'
			bullet.setposition(0,-400)
			#Reset the enemy
			x = random.randint(-200,200)
			y = random.randint(100,250)
			enemy.setposition(x,y)
			#Update the score
			score += 10
			scorestring = 'Score: %s' %score
			score_pen.clear()
			score_pen.write(scorestring, False, align='left', font=('Arial',14, 'normal'))
		
		#Collision between player and enemy (Gave Over)
		if isCollision(enemy, player):
			os.system('aplay explosion.wav&')
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
			os.system('aplay explosion.wav&')
			big_enemy.hideturtle()
			big_enemy.setx(-275)
			#Reset the bullet
			bullet.hideturtle()
			bulletstate = 'ready'
			bullet.setposition(0,-400)
			#Update the score
			score += 50
			scorestring = 'Score: %s' %score
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
	

delay = input('Press enter to finish.')
