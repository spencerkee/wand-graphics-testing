from __future__ import division
import math
from math import pi
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import collections
import random
import itertools


poss_colors = ['LightCoral','IndianRed1','IndianRed2','brown1','firebrick1','brown2','IndianRed','IndianRed3','firebrick2','brown3','red',
'red1','RosyBrown4','firebrick3','red2','firebrick','brown','red3','brown4','firebrick4','DarkRed','red4','maroon']

poss_colors.sort(reverse=True)

def distance(p0, p1):
	return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def midpoint(p1, p2):
    return ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)


def triangle_point_area(a, b, c):
	def distance(p1, p2):
		return math.hypot(p1[0]-p2[0], p1[1]-p2[1])
	side_a = distance(a, b)
	side_b = distance(b, c)
	side_c = distance(c, a)
	s = 0.5 * ( side_a + side_b + side_c)
	return math.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))

def triangle_side_area(a, b, c):
	s = (a + b + c) / 2
	return (s*(s-a)*(s-b)*(s-c)) ** 0.5

def PointsInCircum(r, center_point, dot_num):
	return [(math.cos(2*pi/dot_num*x)*r+center_point[0],math.sin(2*pi/dot_num*x)*r+center_point[1]) for x in xrange(0,dot_num)]

def check_for_triangles(lines):
	# if lines form a triangle, draw a triangle
	real_triangles = []
	for poss_triangle in itertools.combinations(lines, 3):
		all_points = []
		for edge in poss_triangle:
			all_points.append(edge[0])
			all_points.append(edge[1])
		all_points.sort()
		if all_points[0] == all_points[1] and all_points[2] == all_points[3] and all_points[4] == all_points[5]:
			real_triangles.append([all_points[0],all_points[2],all_points[5]])
	return real_triangles

def main(num_circles,num_frames,radius_range=[10,100], line_length=250, dimensions=[1000,1000],background_color='black',line_color='red',triangle_color=None):

	triangle_divisor = triangle_side_area(line_length,line_length,line_length)/len(poss_colors)

	circle_list = []
	for i in range(num_circles):
		the_center = [random.randint(0,dimensions[0]),random.randint(0,dimensions[1])]
		radius = random.randint(radius_range[0],radius_range[1])
		d = collections.deque(PointsInCircum(r=radius, center_point=the_center,dot_num=num_frames))
		d.rotate(random.randint(0,num_frames))
		circle_list.append(d)

	for frame in range(num_frames):
		print 'frame', frame
		point_list = []
		for circle in range(num_circles):
			point_list.append((circle_list[circle][frame]))
		with Drawing() as draw:
			draw.stroke_color = Color(line_color)
			draw.stroke_width = 2
			#draw every point at it's state around the circle
			# for point in point_list:
			# 	draw.circle((point[0],point[1]),(point[0]+1, point[1]+1))

			#draws line if 2 points are within line_length of each other
			lines = []
			for line in itertools.combinations(point_list,2):
				if distance(line[0],line[1]) <= line_length:
					lines.append(line)
			for line in lines:
				draw.line(line[0],line[1])

			#if lines form a triangle, draw a triangle
			for triangle in check_for_triangles(lines):
				color_number = int(triangle_point_area(triangle[0],triangle[1],triangle[2])/triangle_divisor)
				draw.fill_color = Color(poss_colors[color_number])
				draw.polygon([triangle[0],triangle[1],triangle[2]])

			#draw image onto black background and save it
			with Image(width=dimensions[0], height=dimensions[1], background=Color(background_color)) as image:
				draw(image)
				image.save(filename=('frame'+str(frame)+'.png'))

	with Image(filename='frame0.png') as image:
		for frame_number in range(1,num_frames):
			with Image(filename=('frame'+str(frame_number)+'.png')) as this_frame:
				image.sequence.append(this_frame)
		image.save(filename='testingTriangles.gif')

def doubleImage(first_set,second_set,num_frames=20,line_length=250,dimensions=[1000,1000]):
	triangle_divisor = triangle_side_area(line_length,line_length,line_length)/len(poss_colors)
	circle_list = []
	if len(first_set) < len(second_set):
		lower_length = len(first_set)
		higher_length = len(second_set)
	else:
		lower_length = len(second_set)
		higher_length = len(first_set)
	for i in range(lower_length):
		circle_pair = [first_set[i],second_set[i]]
		this_center = midpoint(circle_pair[0],circle_pair[1])
		radius = distance(this_center,circle_pair[0])
		d = collections.deque(PointsInCircum(r=radius, center_point=this_center,dot_num=num_frames))
		rotate_difference = min(range(len(d)), key=lambda p: distance(d[p],circle_pair[0]))
		#this could be rewritten for distance bewlow a certain threshold
		d.rotate(-rotate_difference)
		circle_list.append(d)
	if higher_length != lower_length:
		for i in range(lower_length,higher_length):
			if higher_length == len(first_set):
				circle_pair = [first_set[i],[random.randint(0,dimensions[0]),random.randint(0,dimensions[1])]]
				radius = distance(circle_pair[0],circle_pair[1])
				d = collections.deque(PointsInCircum(r=radius, center_point=circle_pair[1],dot_num=num_frames))
				rotate_difference = min(range(len(d)), key=lambda p: distance(d[p],circle_pair[0]))
				d.rotate(-rotate_difference)
				circle_list.append(d)
			if higher_length == len(second_set):
				circle_pair = [second_set[i],[random.randint(0,dimensions[0]),random.randint(0,dimensions[1])]]
				radius = distance(circle_pair[0],circle_pair[1])
				d = collections.deque(PointsInCircum(r=radius, center_point=circle_pair[1],dot_num=num_frames))
				rotate_difference = max(range(len(d)), key=lambda p: distance(d[p],circle_pair[0]))
				d.rotate(-rotate_difference)
				circle_list.append(d)

	for i in set1:
		circle_list.append(i)

	for frame in range(num_frames):
		print 'frame_number', frame
		point_list = []
		for circle in range(higher_length):
			point_list.append((circle_list[circle][frame]))
			# point_list.append((circle_list[circle]))
		with Drawing() as draw:
			draw.stroke_color = Color('red')
			draw.stroke_width = 2
			draw.fill_color = Color('red')
			#draw every point at it's state around the circle
			for point in point_list:
				draw.circle((point[0],point[1]),(point[0]+1, point[1]+1))

			# for i in first_set:
			# 	draw.circle((i[0],i[1]),(i[0]+4,i[1]+4))
			# for i in second_set:
			# 	draw.circle((i[0],i[1]),(i[0]+1,i[1]+1))

			# draws line if 2 points are within line_length of each other
			lines = []
			for line in itertools.combinations(point_list,2):
				if distance(line[0],line[1]) <= line_length:
					lines.append(line)
			# for line in lines:
			# 	draw.line(line[0],line[1])

			#if 3 points form a triangle, draw one
			for triangle in check_for_triangles(lines):
				color_number = int(triangle_point_area(triangle[0],triangle[1],triangle[2])/triangle_divisor)
				draw.fill_color = Color(poss_colors[color_number])
				draw.polygon([triangle[0],triangle[1],triangle[2]])

			#draw image onto black background and save it
			with Image(width=dimensions[0], height=dimensions[1], background=Color('black')) as image:
				draw(image)
				image.save(filename=('frame'+str(frame)+'.png'))

	with Image(filename='frame0.png') as image:
		for frame_number in range(1,num_frames):
			with Image(filename=('frame'+str(frame_number)+'.png')) as this_frame:
				image.sequence.append(this_frame)
		image.save(filename='testingTriangles.gif')

main(num_circles=50,num_frames=30)
# [500,100]
set1 = [[100,100],[100,300],[500,300],[500,100]]
# set1 = [(10,5), (12,7), (13,9), (14,9), (6,8), (7,6), (9,5),
# (9,1), (15,0), (16,1), (10,2), (10,5), (11,10), (9,13) , (11,6),
# (12,5), (12,2), (18,2), (17,3), (13,3), (13,9) ,(15,6), (16,6),
# (17,7), (16,11), (16,7), (15,10), (17,12), (17,14), (16,15),
# (19,15), (19,16), (18,17), (17,18), (16,18), (15,20), (14,20), (14,19),
# (15,18), (14,15), (10,15), (8,14), (6,11), (6,4), (5,3), (0,4), (1,3),
# (6,2), (7,3), (9,5) ,(15,12), (14,11), (16,7), (15,6), (14,6),
# (15,7), (13,11), (13,12), (14,14)]
# set1 = [(16,12), (13,13), (16,14) ,(9,13), (6,13) ,(16,13),
# (13,13) ,(10,13), (11,12), (12,13) ,(10,2), (12,2), (13,3),
# (14,5) ,(9,2), (10,1) ,(6,6), (4,4), (3,4), (2,5), (1,8),
# (2,10), (3,11), (4,11), (6,11), (5,12), (3,12), (1,11), (0,9), (0,7),
# (1,4), (3,3), (5,3), (6,4) ,(16,1), (15,2) ,(9,1), (8,2)
# ,(6,12), (9,13), (6,14) ,(12,2), (14,1), (16,1), (16,2),
# (14,3), (15,5), (14,7), (15,9), (17,10), (19,13), (18,14), (17,13),
# (16,11), (14,10), (13,11), (14,13), (14,18), (12,16), (10,16), (8,18),
# (8,13), (9,11), (7,10), (6,9), (6,4), (8,1), (10,1), (10,2), (8,3),
# (10,4), (11,5), (11,6), (10,7) ,(6,5), (7,4), (8,5), (8,8) ,(15,1), (14,2)]
set2 = [[400,400],[400,600],[600,600],[600,400]]
# set2 = [[15,15]]
# for i in range(len(set1)):
# 	set1[i]=[set1[i][0]*28,600-set1[i][1]*28]

random.shuffle(set1)
random.shuffle(set2)
# doubleImage(set1, set2, num_frames=40, line_length=1000, dimensions=[1000,1000])
