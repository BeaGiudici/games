# Space Invaders Tutorial by @TokyoEdTech

import turtle
import os
import sys
import random
import numpy as np
import platform

random.seed(0)

if platform.system() == 'Windows':
    try:
        import winsound
    except:
        print('ERROR: winsound module not available.')


# Register the shape
turtle.register_shape('images/space-invader-enemy.gif')
turtle.register_shape('images/space-ship.gif')

# Create the player turtle class


class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape('images/space-ship.gif')
        self.penup()
        self.speed(0)
        self.setposition(0, -250)
        self.setheading(90)
        self.speed = 0

# Move the player left and right
    def move_left(self):
        self.speed = -0.25

    def move_right(self):
        self.speed = 0.25

    def move_player(self):
        x = self.xcor()  # Old position
        x += self.speed
# the lowest value for x must be -280
        if x < -280:
            x = -280
# the highest value for x must be 280
        if x > 280:
            x = 280
        self.setx(x)  # New position

    def fire_bullet(self):
        if bullet.bulletstate == 'ready':
            # move the bullet to the just above the player
            play_sound('sounds/laser.wav', time=0)
            bullet.bulletstate = 'fire'
            x = self.xcor()
            y = self.ycor()
            bullet.setposition(x, y+10)
            bullet.showturtle()


class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape('images/space-invader-enemy.gif')
        self.penup()
        self.speed(0)
        self.speed = 0.02
        self.goto(x, y)

    def isCollision(self, other):
        distance = np.sqrt((self.xcor()-other.xcor())**2 +
                           (self.ycor()-other.ycor())**2)
        if distance < 15:
            return True  # there is a collision
        else:
            return False


class Bullet(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape('triangle')
        self.color('gold')
        self.penup()  # do not draw a line when moving
        self.speed(0)
        self.setheading(90)
        self.shapesize(0.5, 0.5)
        self.hideturtle()  # bullet hidden at the beginning
        self.bulletspeed = 0.5
        # Define bullet state
        # ready: ready to fire
        # fire: bullet is firing
        self.bulletstate = 'ready'


def play_sound(soundfile, time=0):
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
        turtle.ontimer(lambda: play_sound(
            soundfile, time), t=int(time*1000))


def create_sreen():
    '''
Set up the screen
    '''
    global wn
    wn = turtle.Screen()
    wn.bgcolor('black')
    wn.title('Space Invaders')
    wn.bgpic('images/space_background.gif')
    wn.tracer(0)  # Shuts off the screen updates
    # Draw a border
    border_pen = turtle.Turtle()
    border_pen.speed(0)  # fastest
    border_pen.color('white')
    border_pen.penup()
    border_pen.setposition(-300, -300)
    border_pen.pendown()
    border_pen.pensize(3)
    for side in range(4):
        border_pen.fd(600)
        border_pen.lt(90)
    border_pen.hideturtle()


def initialize():
    global player
    global enemies
    global big_enemy
    global bullet

    player = Player()


# Choose a number of enemies
    Nenemies = 30

    enemies = []

    enemy_ctr = 0
    enemy_xi = -225
    enemy_yi = 250

    for i in range(Nenemies):
        x = enemy_xi + (50*enemy_ctr)
        y = enemy_yi
        enemies.append(Enemy(x, y))
        # Update the enemy number
        enemy_ctr += 1
        if enemy_ctr == 10:
            enemy_yi -= 50
            enemy_ctr = 0

    # Create the big enemy
    big_enemy = Enemy(-275, 250)
    # big_enemy.shape('images/space-big-ship.png')
    big_enemy.shape('square')
    big_enemy.color('red')
    big_enemy.penup()
    # big_enemy.speed(0)
    big_enemy.hideturtle()
    big_enemy.speed = 1.25

    # create the player's bullet
    bullet = Bullet()

    # Create keyboard bindings
    wn.listen()
    # When left arrow key is pressed, it
    # calls the function 'move_left'
    wn.onkeypress(player.move_left, 'Left')
    wn.onkeypress(player.move_right, 'Right')  # Same but for right arrow
    wn.onkeypress(player.fire_bullet, 'space')
    wn.onkeypress(wn.bye, 'Escape')

# Play background music
# play_sound('sounds/bgm.mp3', 119)

# Main game loop


def main_loop():

    # Set the score to 0
    score = 0

    # Draw the score
    score_pen = turtle.Turtle()
    score_pen.speed(0)
    score_pen.color('white')
    score_pen.penup()
    score_pen.setposition(-290, 270)
    scorestring = 'Score: {}'.format(score)
    score_pen.write(scorestring, False, align='left',
                    font=('Arial', 12, 'normal'))
    score_pen.hideturtle()

    while True:
        player.move_player()
        for enemy in enemies:
            # Move the enemy
            x = enemy.xcor()
            x += enemy.speed
            enemy.setx(x)

            # Move all the enemies back and down
            if enemy.xcor() > 280:
                for e in enemies:
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
                    e.speed *= -1  # Inverse the velocity

            if enemy.xcor() < -280:
                for e in enemies:
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
                    e.speed *= -1  # Inverse the velocity

            # Check for a collision between bullet and enemy
            if enemy.isCollision(bullet):
                play_sound('sounds/explosion.wav')
                # Reset the bullet
                bullet.hideturtle()
                bullet.bulletstate = 'ready'
                bullet.setposition(0, -400)
                # Reset the enemy
                enemy.setposition(0, 10000)
                # Update the score
                score += 10
                scorestring = 'Score: {}'.format(score)
                score_pen.clear()
                score_pen.write(scorestring, False, align='left',
                                font=('Arial', 14, 'normal'))

            # Collision between player and enemy (Gave Over)
            if enemy.isCollision(player):
                play_sound('~Codici/retroGames/sounds/explosion.wav')
                player.hideturtle()
                enemy.hideturtle()
                print('Game Over!')
                break

        # move the bullet
        if bullet.bulletstate == 'fire':
            y = bullet.ycor()
            y += bullet.bulletspeed
            bullet.sety(y)

        # check if the bullet has gone to the top
        if bullet.ycor() > 275:
            bullet.hideturtle()
            # the bullet returns at the initial position
            bullet.sety(player.ycor()+10)
            bullet.bulletstate = 'ready'

        wn.update()


if __name__ == '__main__':
    create_sreen()
    initialize()
    main_loop()
