import math


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