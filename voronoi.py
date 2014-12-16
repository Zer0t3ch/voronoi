from Tkinter import *
import random
import sys
import os


class point:
	def __init__(self, x=0, y=0):
		self.loc = [x, y]
	loc = [0, 0]


def random_points(count, xmax=100, ymax=100, xmin=0, ymin=0):
	pts = []
	for i in xrange(count):
		ptx = random.randint(xmin, xmax)
		pty = random.randint(ymin, ymax)
		pts.append(point(ptx, pty))
	return pts


def draw_point(canvas, x, y):
	a = x * 3
	b = y * 3
	canvas.create_line(
		a - 1, b - 1,
		a - 1, b + 1
	)
	canvas.create_line(
		a - 1, b + 1,
		a + 1, b + 1
	)
	canvas.create_line(
		a + 1, b + 1,
		a + 1, b - 1
	)
	canvas.create_line(
		a + 1, b - 1,
		a - 1, b - 1
	)


def draw_line(canvas, p1, p2):
	x1 = p1.loc[0] * 3
	y1 = p1.loc[1] * 3
	x2 = p2.loc[0] * 3
	y2 = p2.loc[1] * 3
	canvas.create_line(x1, y1, x2, y2)


def paint():
	c.delete(ALL)
	points = random_points(50)
	for p in points:
		draw_point(
			c,
			p.loc[0], p.loc[1]
		)


points = []

w = Tk()
fc = Frame(w, width=300, height=300)
fo = Frame(w, width=200, height=300)
fc.pack({'side': 'left'})
fo.pack({'side': 'right'})
c = Canvas(fc, width=300, height=300)
c.pack()

qb = Button(fo)
qb['text'] = 'QUIT'
qb['command'] = w.quit
qb['fg'] = 'red'
qb.pack({'side': 'bottom'})

paint()

w.mainloop()
w.destroy()
