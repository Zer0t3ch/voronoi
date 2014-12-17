#!/usr/bin/python
from operator import attrgetter
from Tkinter import *
import random
import time
import math
import sys
import os


class Point:
	def __init__(self, x=0, y=0):
		self.loc = (x, y)
		self.x = x
		self.y = y
	x = 0
	y = 0

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

	def get_locations(self):
		return self.p1.loc, self.p2.loc

	def get_raw(self):
		return self.p1.loc[0], self.p1.loc[1], self.p2.loc[0], self.p2.loc[1]


class Application(Frame):
	f_size = [1200, 900]
	c_size = [900, 900]
	c_scale = 9
	frames = ['', '']
	buttons = {}
	point_count = 15
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
		a = x * self.c_scale
		b = y * self.c_scale
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
			randx = random.randint(0, self.c_size[0] / self.c_scale)
			randy = random.randint(0, self.c_size[1] / self.c_scale)
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
		self.lines['a'].append(line)
		if cat != 'a':
			self.lines[cat].append(line)

	def toggle_mode(self, mode):
		print mode, ': ', self.toggles[mode]
		if self.toggles[mode]:
			self.toggles[mode] = False
		else:
			self.toggles[mode] = True

	def toggle_convex_hull(self):
		self.toggle_mode('c')
		if self.toggles['c']:
			self.clear_lines(cat='c')
		else:
			for l in convex_lines(self.points):
				# print '[ {0}, {1}, {2}, {3} ]'.format(a, b, x, y)
				a, b, x, y = l.get_raw()
				a *= 9
				b *= 9
				x *= 9
				y *= 9
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
			width=self.f_size[0],
			height=self.f_size[1]
		)
		self.pack()
		self.create_frames()
		self.create_buttons(self.frames[1])


def null():
	return None


def convex_lines(point_array):
	points = point_array
	lines = []
	pts = []
	shit_point = Point(-1, -1)
	pts.append(shit_point)
	lowest = min(points, key=attrgetter('x'))		# Find the bottom-most point
	pts.append(lowest)								# Add the lowest to the hull
	count = 0
	while not pts[0].same_as(pts[-1]):				# Loop until the last point on the hull is the same as the first
		try:										# Attempt to
			angle = 0
			pts.append(points[0])
			for x in xrange(len(points)):
				if pts[-2].angle_to(points[x]) < angle:
					pts.pop(-1)
					pts.append(points[x])
					if pts[0].same_as(points[x]):
						print 'Same on both ends'
					# time.sleep(0.1)
					# print 'Adding Point: ', points[x], ' at index ', len(pts) - 1
					# print len(pts)
					print pts[0].x, ',', pts[0].y
					print pts[-1].x, ',', pts[-1].y
		except Exception, why:						# Catch exceptions
			print(str(why))							# And print the cause
		if count == 0:
			pts.pop(0)
		count += 1
		if count > 99999:
			break
	for x in xrange(len(pts)):						# Cycle every point in the hull
		if x != 0:									# If not the first in the list
			lines.append(Line(						# Add a line between pts[x] and pts[x-1]
				pts[x].x,
				pts[x].y,
				pts[x - 1].x,
				pts[x - 1].y
			))
	# print(pts.x)
	return lines


window = Tk()
app = Application(window)
app.generate_points()
app.draw_points()
print len(convex_lines(app.points))
app.mainloop()
window.destroy()
