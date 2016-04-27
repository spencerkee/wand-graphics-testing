import math
from math import pi
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import collections
import random
import itertools

def distance(p0, p1):
	return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

import math
def area(a, b, c):
	def distance(p1, p2):
		return math.hypot(p1[0]-p2[0], p1[1]-p2[1])
	side_a = distance(a, b)
	side_b = distance(b, c)
	side_c = distance(c, a)
	s = 0.5 * ( side_a + side_b + side_c)
	return math.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))

def PointsInCircum(r, xmod, ymod, dot_num):
	return [(math.cos(2*pi/dot_num*x)*r+xmod,math.sin(2*pi/dot_num*x)*r+ymod) for x in xrange(0,dot_num)]

def main(num_circles,num_frames,radius_range=[10,100], line_length=250):
	circle_list = []
	for i in range(num_circles):
		starting_x = random.randint(0,1000)
		starting_y = random.randint(0,1000)
		radius = random.randint(radius_range[0],radius_range[1])
		d = collections.deque(PointsInCircum(r=radius, xmod=starting_x, ymod=starting_y,dot_num=num_frames))
		d.rotate(random.randint(0,num_frames))
		circle_list.append(d)

	for frame in range(num_frames):
		point_list = []
		for circle in range(num_circles):
			point_list.append((circle_list[circle][frame]))
		with Drawing() as draw:
			draw.stroke_color = Color('red')
			draw.stroke_width = 2
			draw.fill_color = Color('red')
			#draw every point at it's state around the circle
			for point in point_list:
				draw.circle((point[0],point[1]),(point[0]+1, point[1]+1))

			#draws line if 2 points are within line_length of each other
			lines = []
			for line in itertools.combinations(point_list,2):
				if distance(line[0],line[1]) <= line_length:
					lines.append(line)
			for line in lines:
				draw.line(line[0],line[1])

			#if lines form a triangle, draw a triangle
			for poss_triangle in itertools.combinations(lines, 3):
				all_points = []
				for edge in poss_triangle:
					all_points.append(edge[0])
					all_points.append(edge[1])
				all_points.sort()
				if all_points[0] == all_points[1] and all_points[2] == all_points[3] and all_points[4] == all_points[5]:
					draw.polygon([all_points[0],all_points[2],all_points[4]])

			#draw image onto black background and save it
			with Image(width=1000, height=1000, background=Color('black')) as image:
				draw(image)
				image.save(filename=('frame'+str(frame)+'.png'))

	with Image(filename='frame1.png') as image:
		for frame_number in range(1,num_frames):
			with Image(filename=('frame'+str(frame_number)+'.png')) as this_frame:
				image.sequence.append(this_frame)
		image.save(filename='testingTriangles.gif')

main(num_circles=30,num_frames=30)
#20,30 = 15
#30,30 = 19
