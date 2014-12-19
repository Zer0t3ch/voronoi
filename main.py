#!/usr/bin/python
from algorithms import *
from Tkinter import *
from geo import *
import random


class Application(Frame):
	point_count = 5
	window_size = [300, 150]
	canvas_size = [200, 150]
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
		self.canvas_size[0] = self.window_size[0] - 100
		self.canvas_size[1] = self.window_size[1]
		frame_one = self.frames[0] = Frame(
			self,
			width=self.canvas_size[0],
			height=self.canvas_size[1]
		)
		frame_two = self.frames[1] = Frame(
			self,
			width=100,
			height=self.window_size[1]
		)

		frame_two.pack(side='right', fill='y')
		frame_one.pack(side='left', fill='both')
		self.canvas = Canvas(self.frames[0], width=900, height=900)
		self.canvas.bind('<Configure>', self.on_resize)
		self.canvas.pack()

	def on_resize(self, event):
		self.canvas_size = event.width, event.height
		self.regenerate_points()

	def clear_points(self):
		self.points = []

	def generate_points(self):
		for i in xrange(self.point_count):
			randx = random.randint(0, self.canvas_size[0] / self.canvas_scale)
			randy = random.randint(0, self.canvas_size[1] / self.canvas_scale)
			p = Point(randx, randy)
			self.points.append(p)

	def draw_points(self):
		for p in self.points:
			a, b = self.loc(p)
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
		if self.toggles['c']:
			self.toggle_convex_hull()
		self.toggle_convex_hull()

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
		with open('config.py', 'r') as conf_file:
			conf = {}
			exec(conf_file.read(), conf)
			conf_file.close()
			self.point_count = conf['point_count']
			self.window_size = conf['window_size']
		Frame.__init__(
			self, master,
			width=self.window_size[0],
			height=self.window_size[1]
		)
		self.pack()
		self.create_frames()
		self.create_buttons(self.frames[1])


window = Tk()
app = Application(window)
app.generate_points()
app.draw_points()
window.focus_set()
app.mainloop()
window.destroy()
