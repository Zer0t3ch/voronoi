from geo import *


def _orientation(a, b, c):
	return ((b.x - a.x) * (c.y - b.y)) - ((b.y - a.y) * (c.x - b.x))


def _rightmost(all_points):
	x_list = []
	for p in all_points:
		x_list.append(p.x)
	index = x_list.index(max(x_list))
	return all_points[index]


def _gift_wrapper(point_array):
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
	hull_points = _gift_wrapper(raw_points)
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