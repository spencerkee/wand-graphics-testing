#!/usr/bin/env python2.7

from __future__ import division
import math
from math import pi
from wand.image import Image
from wand.drawing import Drawing
from wand.color import Color
import collections
import random
import itertools

'''
Note: This program creates the frames locally before saving them into a gif. You should place
it in a directory you don't mind having many image files in.
'''

#wand color names
poss_colors = ['LightCoral','IndianRed1','IndianRed2','brown1','firebrick1','brown2','IndianRed','IndianRed3','firebrick2','brown3','red',
'red1','RosyBrown4','firebrick3','red2','firebrick','brown','red3','brown4','firebrick4','DarkRed','red4','maroon']
poss_colors.sort(reverse=True)

def distance(p0, p1):#distance between 2 coordinates
	return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def midpoint(p1, p2):#midpoint of 2 coordinates
    return ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)

def triangle_point_area(a, b, c):
	'''
	Calculates the area of a triangle given 3 points. 
	This is used for choosing the triangle color. 
	'''
	def distance(p1, p2):
		return math.hypot(p1[0]-p2[0], p1[1]-p2[1])
	side_a = distance(a, b)
	side_b = distance(b, c)
	side_c = distance(c, a)
	s = 0.5 * ( side_a + side_b + side_c)
	return math.sqrt(s * (s - side_a) * (s - side_b) * (s - side_c))

def triangle_side_area(a, b, c):
	'''
	Calculates the area of a triangle given the length of 3 sides.
	'''
	s = (a + b + c) / 2
	return (s*(s-a)*(s-b)*(s-c)) ** 0.5

def PointsInCircum(r, center_point, dot_num): 
	'''
	Takes in the number of points and the centerpoint and radius of a circle and 
	returns the coordinates of evenly spaced points on the circumference.
	'''
	return [(math.cos(2*pi/dot_num*x)*r+center_point[0],math.sin(2*pi/dot_num*x)*r+center_point[1]) for x in xrange(0,dot_num)]

def check_for_triangles(lines):
	'''
	Takes in a list of all lines, then iterates over every triple and checks to see if
	they form a triangle.
	'''
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

def rotate_list(input_list, rotate_difference):
	return_list = []
	for i in range(rotate_difference, len(input_list)):
		return_list.append(input_list[i])
	for i in range(0,rotate_difference):
		return_list.append(input_list[i])
	return return_list

def invert_list(input_list):
	input_length = len(input_list)
	return_list = []
	for i in range(input_length):
		return_list.append(0)
	for i in range(input_length):
		return_list[i] = input_list[input_length-(i+1)]
	return return_list

def makeCircles(num_circles, num_frames, radius_range, dimensions):
	'''
	Finds (num_circles) random points within (dimensions) and chooses a random radius 
	for every point. Then uses PointsInCircum() to create the circles.

	Num_frames corresponds to the number of points on a circle's circumference. 

	(the_center) is the centerpoint of the circle
	(radius) is the radius of the circle
	(circle_points) are the points on the circumference made by PointsInCircum()
	'''
	circle_list = []
	for i in range(num_circles):
		the_center = [random.randint(0,dimensions[0]),random.randint(0,dimensions[1])]
		radius = random.randint(radius_range[0],radius_range[1])
		circle_points = PointsInCircum(r=radius, center_point=the_center,dot_num=num_frames)
		#gives the circle a random starting point
		circle_points = rotate_list(circle_points,random.randint(0, num_frames))
		#50% of the time circles will move counterclockwise
		if random.randint(0,1) == 1:
			circle_points = invert_list(circle_points)
		circle_list.append(circle_points)
	return circle_list

def main(num_circles,num_frames,radius_range=[10,100], line_length=250, dimensions=[1000,1000],background_color='black',line_color='red',triangle_color=None):
	'''
	Creates (num_circles) random orbits in (dimensions), with (num_frames) points on the circumference in.
	Radii are randomly chosen in range (radius_range).
	(line_length) is the threshold below which lines are drawn between points.
	(triangle_color) is currently unfinished.
	'''
	#this is for choosing the intensity of the color based on the area of the triangle
	triangle_divisor = triangle_side_area(line_length,line_length,line_length)/len(poss_colors)
	circle_list = makeCircles(num_circles, num_frames=num_frames, radius_range=radius_range, dimensions=dimensions)

	for frame in range(num_frames):
		print 'frame:', str(frame + 1) + '/' + str(num_frames)
		point_list = []
		for circle in range(num_circles):
			point_list.append((circle_list[circle][frame]))
		with Drawing() as draw:
			draw.stroke_color = Color(line_color)
			draw.stroke_width = 2
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
			for triangle in check_for_triangles(lines):
				color_number = int(triangle_point_area(triangle[0],triangle[1],triangle[2])/triangle_divisor)
				draw.fill_color = Color(poss_colors[color_number])
				draw.polygon([triangle[0],triangle[1],triangle[2]])

			#draw image onto black background and save it
			with Image(width=dimensions[0], height=dimensions[1], background=Color(background_color)) as image:
				draw(image)
				image.save(filename=('frame'+str(frame)+'.png'))

	#create the gif.
	with Image(filename='frame0.png') as image:
		for frame_number in range(1,num_frames):
			with Image(filename=('frame'+str(frame_number)+'.png')) as this_frame:
				image.sequence.append(this_frame)
		image.save(filename='testingTriangles.gif')

def doubleImage(first_set,second_set,num_frames=20,line_length=250,dimensions=[1000,1000]):
	'''
	Unfinished project to switch between 2D wireframes by placing every pair of points between
	the wireframes on opposite ends of an orbiting point.
	'''
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

			for i in first_set:
				draw.circle((i[0],i[1]),(i[0]+4,i[1]+4))
			for i in second_set:
				draw.circle((i[0],i[1]),(i[0]+1,i[1]+1))

			# draws line if 2 points are within line_length of each other
			lines = []
			for line in itertools.combinations(point_list,2):
				if distance(line[0],line[1]) <= line_length:
					lines.append(line)
			for line in lines:
				draw.line(line[0],line[1])

			#if 3 points form a triangle, draw one
			# for triangle in check_for_triangles(lines):
			# 	color_number = int(triangle_point_area(triangle[0],triangle[1],triangle[2])/triangle_divisor)
			# 	draw.fill_color = Color(poss_colors[color_number])
			# 	draw.polygon([triangle[0],triangle[1],triangle[2]])

			#draw image onto black background and save it
			with Image(width=dimensions[0], height=dimensions[1], background=Color('black')) as image:
				draw(image)
				image.save(filename=('frame'+str(frame)+'.png'))

	with Image(filename='frame0.png') as image:
		for frame_number in range(1,num_frames):
			with Image(filename=('frame'+str(frame_number)+'.png')) as this_frame:
				image.sequence.append(this_frame)
		image.save(filename='testingTriangles.gif')



if __name__ == '__main__':
	main(num_circles=30,num_frames=30)

# set1 = [[100,100],[100,300],[500,300],[500,100]]
# set2 = [[400,400],[400,600],[600,600],[600,400]]
# for i in range(len(set1)):
# 	set1[i]=[set1[i][0]*28,600-set1[i][1]*28]
# random.shuffle(set1)
# random.shuffle(set2)
# doubleImage(set1, set2, num_frames=10, line_length=1000, dimensions=[600,600])
