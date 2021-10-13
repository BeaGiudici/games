# Tutorial by @TokyoEdTech
#A Simple Maze Game

#Part 1: Setting Up The Maze

import turtle
import numpy as np
import random as rnd

wn = turtle.Screen() #Create a screen
wn.bgcolor('black')
wn.title('Maze Game')
wn.setup(700,700) #(pixels)
wn.tracer(0)

#Register shapes
images = ['images/wizard_right.gif','images/wizard_left.gif', \
          'images/treasure.gif','images/wall.gif',\
          'images/enemy.gif']
for image in images:
    turtle.register_shape(image)

#Create Pen
class Pen(turtle.Turtle): #defines a turtle object
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape('square')
        self.color('white')
        self.penup()
        self.speed(0) #fasest

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape('images/wizard_right.gif')
        #self.color('blue')
        self.penup()
        self.speed(0)
        self.gold = 0 # When the game starts, the player has 0 gold
    '''
    def move(self, where):
        if where == 'up':
            move_to_x = self.xcor()
            move_to_y = self.ycor() + 24

        elif where == 'down':
            move_to_x = self.xcor()
            move_to_y = self.ycor() - 24

        elif where == 'left':
            move_to_x = self.xcor() - 24
            move_to_y = self.ycor()
            self.shape('images/wizard_left.gif')

        elif where == 'right':
            move_to_x = self.xcor()
            move_to_y = self.ycor() + 24
            self.shape('images/wizard_right.gif')

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
    '''
    def up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24
        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)

    def down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def left(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()
        self.shape('images/wizard_left.gif')
        if (move_to_x,move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)

    def right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()
        self.shape('images/wizard_right.gif')
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
    
    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = np.sqrt(a**2 + b**2)

        if distance < 5:
            return True
        else:
            return False

class Treasure(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape('images/treasure.gif')
        #self.color('yellow')
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x,y)

    def destroy(self):
        self.hideturtle()

class Enemy(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape('images/enemy.gif')
        self.penup()
        self.speed(0)
        self.gold = 25
        self.goto(x,y)
        self.direction = rnd.choice(['up','down','left','right'])

    def move(self):
        if self.direction == 'up':
            dx = 0
            dy = 24
        elif self.direction == 'down':
            dx = 0
            dy = -24
        elif self.direction == 'left':
            dx = -24
            dy = 0
        elif self.direction == 'right':
            dx = 24
            dy = 0
        else:
            dx = 0
            dy = 0

        #Check if player is close
        #If so, go in that direction
        if self.is_close(player):
            if player.xcor() < self.xcor():
                self.direction = 'left'
            elif player.xcor() > self.xcor():
                self.direction = 'right'
            elif player.ycor() < self.ycor():
                self.direction = 'down'
            elif player.ycor() > self.ycor():
                self.direction = 'up'

        #Calculate te spot to move to
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        #Check if the space has a wall
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x,move_to_y)
        else:
            #Choose a different direction
            self.direction = rnd.choice(['up','down','left','right'])

        #Set timer to move next time
        turtle.ontimer(self.move, t=rnd.randint(100,300))

    def is_close(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        d = np.sqrt((a**2) + (b**2))

        if d < 75:
            return True
        else:
            return False
        
#Create levels list
levels= ['']

#Define first level
level_1 = [
    'XXXXXXXXXXXXXXXXXXXXXXXXX',
    'XP XXXXXXX         EXXXXX',
    'X  XXXXXXX  XXXXXX  XXXXX',
    'X       XX  XXXXXX  XXXXX',
    'X       XX  XXX        XX',
    'X                  E   XX',
    'XXXXX   XX  XXX      XXXX',
    'XXXXX   XX  XXX  T   XXXX',
    'XXXXX   XX  XXXXXXXXXXXXX',
    'XXXXX   XX       XXXXXXXX',
    'XXXXX   XX       XXXXXXXX',
    'XX      XXXXXXX  XXXXXXXX',
    'XX      XXXXXXX  XXXXXXXX',
    'XX  XXXXXXX      XXXXXXXX',
    'XX  XXXXXXX      XXXXXXXX',
    'XX  XXXXXXXXXXX  XXXXXXXX',
    'XX  XXXXXXXXXXX  XXXXXXXX',
    'XX      XXXX     XXXXXXXX',
    'XX      XXXX     XXXXXXXX',
    'XX      XXXX           XX',
    'XX      XXXX           XX',
    'XX  XXXXXXXX    E      XX',
    'XX                  XXXXX',
    'XX                     XX',
    'XXXXXXXXXXXXXXXXXXXXXXXXX'
] # This permits us to create a level just by changing some text

#Add a treasure list
treasures = []

#Add enemies list
enemies = []

#Add maze to mazes list
levels.append(level_1)

#Create Level Setup Function
def setup_maze(level):
    for y in range(len(level)):
        for x in range (len(level[y])):
            #Get the character at each x,y coordinate
            #NOTE the order of y and x in the next line
            c = level[y][x]
            #Calculate the screen x,y
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            #Check if it is an X (representing a wall)
            if c == 'X':
                pen.goto(screen_x,screen_y)
                pen.shape('images/wall.gif')
                pen.stamp()
                #Add coordinates to wall list
                walls.append((screen_x,screen_y))

            #Check if it is a P (representing the player)
            if c == 'P':
                player.goto(screen_x,screen_y)

            #Check if it is a R (representing a treasure)
            if c == 'T':
                treasures.append(Treasure(screen_x,screen_y))

            if c == 'E':
                enemies.append(Enemy(screen_x,screen_y))

#Create class instances
pen = Pen()
player = Player()

#Draw the gold on screen
gold_pen = turtle.Turtle()
gold_pen.speed(0)
gold_pen.color('gold')
gold_pen.penup()
gold_pen.setposition(-288,298)
gold_pen.write('Gold: %d' % player.gold, False, align='left',font=('Arial',14,'normal'))
gold_pen.hideturtle()

#Create wall coordinates list
walls = []

#Set up the level
setup_maze(levels[1])
#print(walls)

#Keyboard Binding
turtle.listen()
turtle.onkey(player.left,'Left')
turtle.onkey(player.right,'Right')
turtle.onkey(player.up,'Up')
turtle.onkey(player.down,'Down')

#Start moving enemies
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

#wn.tracer(0)

#Main Game Loop
if __name__ == '__main__':
    while True:
        #Check for player collision with treasure
        #Iterate through treasure list
        for treasure in treasures:
            if player.is_collision(treasure):
                #Add the trasure gold to the player gold
                player.gold += treasure.gold
                gold_pen.clear()
                gold_pen.write('Gold: %d' % player.gold,False,align='left', font=('Arial',14,'normal'))
                #Destroy the treasure
                treasure.destroy()
                #Remove the treasure form the list
                treasures.remove(treasure)

        #Iterate through enemy list to see if the player collides
        for enemy in enemies:
            if player.is_collision(enemy):
                enemy_pen = turtle.Turtle()
                enemy_pen.color('red')
                enemy_pen.write('Game Over!',False,align='center', font=('Arial',40,'normal'))

        #Update screen
        wn.update()
