import turtle
import MazeGame

wn = turtle.Screen() #Create a screen
wn.bgcolor('black')
wn.title('Initial')
wn.setup(700,700) #(pixels)
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
		self.setposition(x_0,y_0)
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
		self.write(title, False, align='center', font=('Arial',12,'normal'))

	def btn_click(self,x,y):
		'''
Function that determines the click on the button
		'''
		if self.xcor() - self.length/2. < x < self.xcor() + self.length/2. \
		and self.ycor() - self.height/3. < y < self.ycor() + 2.*self.height/3.:
#			print('CLICK!', x,y)
			self.click = True

b = Button(0,0, length=300, height=100, title='Game 1')

turtle.listen()
turtle.onscreenclick(b.btn_click, 1)


while True:
	if b.click == True:
		turtle.resetscreen()
		MazeGame
	wn.update()