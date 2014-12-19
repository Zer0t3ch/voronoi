#!/usr/bin/python
from Tkinter import *
import random
import math

POINT_COUNT = 50


class Point:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def angle_to(self, target):
		if self.x == target.x:
			return 361
		rad = math.atan(
			(target.y - self.y) / (target.x - self.x)
		)
		deg = math.degrees(rad)
		if deg < 0:
			deg += 360
		return deg

	def same_as(self, target):
		if self.x == target.x:
			if self.y == target.y:
				return True
		return False


class Line:
	def __init__(self, x1, y1, x2, y2):
		self.p1 = Point(x1, y1)
		self.p2 = Point(x2, y2)

	def get_points(self):
		return self.p1, self.p2

	def get_raw(self):
		return self.p1.x, self.p1.y, self.p2.x, self.p2.y


class Application(Frame):
	f_size = [1200, 900]
	canvas_size = [900, 900]
	canvas_scale = 1
	dot_scale = 1
	frames = ['', '']
	buttons = {}
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
	canvas = None

	def loc(self, p):
		a = p.x * self.canvas_scale
		b = p.y * self.canvas_scale
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
		self.canvas = c = Canvas(self.frames[0], width=900, height=900)
		c.pack()

	def clear_points(self):
		self.points = []

	def generate_points(self):
		for i in xrange(POINT_COUNT):
			randx = random.randint(0, self.canvas_size[0] / self.canvas_scale)
			randy = random.randint(0, self.canvas_size[1] / self.canvas_scale)
			p = Point(randx, randy)
			self.points.append(p)

	def draw_points(self):
		for p in self.points:
			a, b = self.loc(p)
			s = self.dot_scale
			self.canvas.create_rectangle(
				a - self.dot_scale, b - self.dot_scale,
				a + self.dot_scale, b + self.dot_scale
			)

	def regenerate_points(self):
		self.clear_points()
		self.clear_lines()
		self.toggles['c'] = False
		self.toggles['d'] = False
		self.toggles['v'] = False
		self.canvas.delete(ALL)
		self.generate_points()
		self.draw_points()

	def clear_lines(self, cat='a'):
		for l in self.lines[cat]:
			self.canvas.delete(l)

	def add_line(self, line, cat='a'):
		self.lines['a'].append(line)
		if cat != 'a':
			self.lines[cat].append(line)

	def toggle_mode(self, mode):
		# print mode, ': ', self.toggles[mode]
		if self.toggles[mode]:
			self.toggles[mode] = False
		else:
			self.toggles[mode] = True

	def toggle_convex_hull(self):
		if self.toggles['c']:
			self.clear_lines(cat='c')
		else:
			for l in convex_lines(self.points):
				# print '[ {0}, {1}, {2}, {3} ]'.format(a, b, x, y)
				a, b, x, y = l.get_raw()
				a *= self.canvas_scale
				b *= self.canvas_scale
				x *= self.canvas_scale
				y *= self.canvas_scale
				temp_line = self.canvas.create_line(a, b, x, y)
				self.add_line(temp_line, cat='c')
		self.toggle_mode('c')

	def create_buttons(self, parent):
		close = self.buttons['close'] = Button(
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
		close.pack(fill='x', side='bottom')
		toggle_convex.pack(fill='x')
		regen_points.pack(fill='x')
		clear_lines.pack(fill='x')

	def __init__(self, master):
		Frame.__init__(
			self, master,
			width=self.f_size[0],
			height=self.f_size[1]
		)
		self.pack()
		self.create_frames()
		self.create_buttons(self.frames[1])


def null():
	return None


def _orientation(a, b, c):
	return ((b.x - a.x) * (c.y - b.y)) - ((b.y - a.y) * (c.x - b.x))


def _rightmost(all_points):
	x_list = []
	for p in all_points:
		x_list.append(p.x)
	index = x_list.index(max(x_list))
	return all_points[index]


def gift_wrapper(point_array):
	points = []
	for p in point_array:
		points.append(p)
	hull = [_rightmost(point_array)]
	while True:
		correct = 0
		for i in range(1, len(points)):
			if _orientation(hull[-1], points[correct], points[i]) < 0:
				correct = i
		if points[correct] is hull[0]:
			break
		else:
			hull.append(points[correct])
			del points[correct]
	return hull


def convex_lines(raw_points):
	hull_points = gift_wrapper(raw_points)
	lines = [Line(
		hull_points[0].x, hull_points[0].y,
		hull_points[-1].x, hull_points[-1].y
	)]
	for i in range(1, len(hull_points)):
		lines.append(Line(
			hull_points[i - 1].x, hull_points[i - 1].y,
			hull_points[i].x, hull_points[i].y
		))
	return lines


window = Tk()
app = Application(window)
app.generate_points()
app.draw_points()
app.mainloop()
window.destroy()
