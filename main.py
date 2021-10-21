import turtle
import MazeGame

turtle.register_shape('images/main_screen.gif')

wn = turtle.Screen()  # Create a screen
# wn.bgcolor('blue')
wn.bgpic('images/main_screen.gif')
wn.title('Initial')
wn.setup(700, 700)  # (pixels)
wn.tracer(0)


class Button(turtle.Turtle):
    '''
Create a button of dimension length*height pixels
with given title
    '''

    def __init__(self, x_0, y_0, height=100, length=200, title='Lorem Ipsum'):
        turtle.Turtle.__init__(self)
        self.penup()
        self.length = length
        self.height = height
        self.click = False
        # Drawing the contour
        self.setposition(x_0, y_0)
        self.pensize(10)
        self.pencolor('white')
        self.pendown()
        self.fillcolor('red')
        self.begin_fill()
        self.forward(length)
        self.left(90)
        self.forward(height)
        self.left(90)
        self.forward(length)
        self.left(90)
        self.forward(height)
        self.end_fill()
        # Write the title
        self.penup()
        self.goto(x_0 + length/2., y_0 + height/3.)
        self.write(title, False, align='center',
                   font=('Courier', 12, 'bold'))
        self.hideturtle()  # So that does not show the cursor

    def btn_click(self, x, y):
        '''
Function that determines the click on the button
        '''
        if self.xcor() - self.length/2. < x < self.xcor() + self.length/2. \
                and self.ycor() - self.height/3. < y < self.ycor() + 2.*self.height/3.:
            #			print('CLICK!', x,y)
            self.click = True


b = Button(-200, 200, length=300, height=100, title='Maze Game')

turtle.listen()
turtle.onscreenclick(b.btn_click, 1)

while True:
    if b.click == True:
        b.click = False
        wn.clearscreen()
        wn.bgpic('nopic')
        # Set the environment for Maze Game
        MazeGame.create_screen()
        MazeGame.initialise()
        # Start the game
        MazeGame.main_loop()
    wn.update()
