from Tkinter import *
import random
import sys
import os


class Point:
	def __init__(self, x=0, y=0):
		self.loc = [x, y]
		self.x = x
		self.y = y
	loc = [0, 0]
	x = 0
	y = 0


class Line:
	def __init__(self, x1, y1, x2, y2):
		self.p1 = Point(x1, y1)
		self.p2 = Point(x2, y2)

	def get_points(self):
		return self.p1, self.p2

	def get_locations(self):
		return self.p1.loc, self.p2.loc

	def get_raw(self):
		return self.p1.loc[0], self.p1.loc[1], self.p2.loc[0], self.p2.loc[1]


class Application(Frame):
	size = [1200, 900]
	csize = [900, 900]
	cscale = 9
	frames = ['', '']
	buttons = {}
	point_count = 50
	points = []
	lines = {
		'a': [],
		'c': [],
		'd': [],
		'v': []
	}
	toggles = {
		'c': False,
		'd': False,
		'v': False
	}

	def loc(self, p):
		x, y = p.loc
		a = x * self.cscale
		b = y * self.cscale
		return a, b

	def create_frames(self):
		self.frames[0] = Frame(
			self,
			width=900,
			height=900
		)
		self.frames[1] = Frame(
			self,
			width=300,
			height=900
		)
		self.frames[0].pack(side='left')
		self.frames[1].pack(side='right', fill='y')
		self.c = c = Canvas(self.frames[0], width=900, height=900)
		c.pack()

	def clear_points(self):
		self.points = []

	def generate_points(self):
		for i in xrange(self.point_count):
			randx = random.randint(0, self.csize[0] / self.cscale)
			randy = random.randint(0, self.csize[1] / self.cscale)
			p = Point(randx, randy)
			self.points.append(p)

	def draw_points(self):
		for p in self.points:
			a, b = self.loc(p)
			self.c.create_line(
				a - 1, b - 1,
				a + 1, b + 1
			)
			self.c.create_line(
				a + 1, b - 1,
				a - 1, b + 1
			)

	def regenerate_points(self):
		self.clear_points()
		self.c.delete(ALL)
		self.generate_points()
		self.draw_points()

	def clear_lines(self, cat='a'):
		for l in self.lines[cat]:
			self.c.delete(l)

	def add_line(self, line, cat='a'):
		lines['a'].append(line)
		if cat != 'a':
			lines[cat].append(line)

	def toggle_mode(self, mode):
		if self.toggles[mode]:
			self.toggles[mode] = False
		else:
			self.toggles[mode] = True

	def toggle_convex_hull(self):
		if self.toggles['c']:
			self.clear_lines(cat='c')
			self.toggle_mode('c')
		else:
			for l in convex_lines(self.points):
				a, b, x, y = l.get_raw()
				tline = self.c.create_line(a, b, x, y)
				self.add_line(tline, cat='c')

	def create_buttons(self, parent):
		quit = self.buttons['quit'] = Button(
			parent,
			text='QUIT',
			command=self.quit,
			fg='red'
		)
		regen_points = self.buttons['regen_points'] = Button(
			parent,
			text='Regenerate Points',
			command=self.regenerate_points
		)
		clear_lines = self.buttons['clear_lines'] = Button(
			parent,
			text='Clear Lines',
			command=self.clear_lines
		)
		toggle_convex = self.buttons['toggle_convex'] = Button(
			parent,
			text='Toggle Convex Hull',
			command=self.toggle_convex_hull
		)
		quit.pack(fill='x', side='bottom')
		toggle_convex.pack(fill='x')
		regen_points.pack(fill='x')
		clear_lines.pack(fill='x')

	def __init__(self, master):
		Frame.__init__(
			self, master,
			width=self.size[0],
			height=self.size[1]
		)
		self.pack()
		self.create_frames()
		self.create_buttons(self.frames[1])


def convex_lines(points):
	lines = []
	pleft = points
	return lines


window = Tk()
app = Application(window)
app.generate_points()
app.draw_points()
app.mainloop()
window.destroy()
