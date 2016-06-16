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

def orbit_maker(first_set, second_set, i, num_frames, dimensions=None):
	if dimensions != None:
		binary_orbit_pair = [second_set[i],[random.randint(0,dimensions[0]),random.randint(0,dimensions[1])]]
	else:
		binary_orbit_pair = [first_set[i],second_set[i]]

	barycenter_point = midpoint(binary_orbit_pair[0],binary_orbit_pair[1])
	radius = distance(binary_orbit_pair[0],binary_orbit_pair[1])/2
	orbit_phases = PointsInCircum(r=radius, center_point=barycenter_point,dot_num=num_frames)
	rotate_difference = min(range(len(orbit_phases)), key=lambda p: distance(orbit_phases[p],second_set[i]))
	orbit_phases = rotate_list(orbit_phases, rotate_difference)
	if random.randint(0,1) == 1:
		orbit_phases = invert_list(orbit_phases)
	return orbit_phases

def wireframe_orbit(first_set,second_set,num_frames=20,line_length=0,dimensions=[1000,1000]):

	lower_length = len(first_set)
	higher_length = len(second_set)
	if len(first_set) > len(second_set):
		lower_length = len(second_set)
		higher_length = len(first_set)

	#Create binary orbits for n pairs of points where n is the length of the smaller set
	orbit_list = []
	for i in range(lower_length):
		orbit_phases = orbit_maker(first_set,second_set, i, num_frames)
		orbit_list.append(orbit_phases)

	if higher_length != lower_length:
		#forces second_set to be longer
		if len(first_set) == higher_length:
			first_set, second_set = second_set, first_set
		for i in range(lower_length,higher_length):
			orbit_phases = orbit_maker(first_set,second_set, i, num_frames, dimensions)
			orbit_list.append(orbit_phases)

	for frame in range(num_frames):
		print 'frame_number', frame
		point_list = []
		for circle in range(higher_length):
			point_list.append((orbit_list[circle][frame]))
			# point_list.append((circle_list[circle]))
		with Drawing() as draw:
			draw.stroke_color = Color('red')
			draw.stroke_width = 2
			draw.fill_color = Color('red')
			#draw every point at it's state around the circle
			for point in point_list:
				draw.circle((point[0],point[1]),(point[0]+1, point[1]+1))

			#if the switch occurs here then the second set could be drawn twice for instance
			# if frame == 0:
			# 	print ('zero')
			# 	for i in second_set:
			# 		draw.circle((i[0],i[1]),(i[0]+2,i[1]+2))
			# if frame == (num_frames/2):
			# 	print ('half')
			# 	for i in first_set:
			# 		draw.circle((i[0],i[1]),(i[0]+2,i[1]+2))

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
	# main(num_circles=30,num_frames=30)

	set1 = [[100,100],[100,300],[500,300],[500,100]]
	set2 = [[400,400],[400,600],[600,600],[600,400]]

	strawberry = [[7.0, 105.0], [7.0, 119.0], [7.0, 133.0], [7.0, 147.0], [7.0, 161.0], [7.0, 175.0], [7.0, 189.0], [7.0, 203.0], [21.0, 91.0], [21.0, 105.0], [21.0, 119.0], [21.0, 133.0], [21.0, 147.0], [21.0, 189.0], [21.0, 203.0], [21.0, 217.0], [35.0, 63.0], [35.0, 77.0], [35.0, 91.0], [35.0, 105.0], [35.0, 147.0], [35.0, 161.0], [35.0, 203.0], [35.0, 217.0], [35.0, 231.0], [49.0, 49.0], [49.0, 63.0], [49.0, 77.0], [49.0, 91.0], [49.0, 105.0], [49.0, 119.0], [49.0, 161.0], [49.0, 175.0], [49.0, 189.0], [49.0, 217.0], [49.0, 231.0], [63.0, 49.0], [63.0, 63.0], [63.0, 77.0], [63.0, 91.0], [63.0, 105.0], [63.0, 119.0], [63.0, 161.0], [63.0, 175.0], [63.0, 189.0], [63.0, 203.0], [63.0, 231.0], [63.0, 245.0], [77.0, 49.0], [77.0, 63.0], [77.0, 77.0], [77.0, 91.0], [77.0, 105.0], [77.0, 161.0], [77.0, 231.0], [77.0, 245.0], [77.0, 259.0], [77.0, 273.0], [91.0, 35.0], [91.0, 49.0], [91.0, 91.0], [91.0, 119.0], [91.0, 133.0], [91.0, 161.0], [91.0, 203.0], [91.0, 217.0], [91.0, 245.0], [91.0, 259.0], [91.0, 273.0], [91.0, 287.0], [105.0, 35.0], [105.0, 49.0], [105.0, 91.0], [105.0, 105.0], [105.0, 119.0], [105.0, 133.0], [105.0, 161.0], [105.0, 203.0], [105.0, 217.0], [105.0, 273.0], [105.0, 287.0], [105.0, 301.0], [105.0, 315.0], [119.0, 35.0], [119.0, 49.0], [119.0, 91.0], [119.0, 105.0], [119.0, 119.0], [119.0, 133.0], [119.0, 161.0], [119.0, 175.0], [119.0, 245.0], [119.0, 259.0], [119.0, 287.0], [119.0, 301.0], [119.0, 315.0], [133.0, 7.0], [133.0, 21.0], [133.0, 35.0], [133.0, 49.0], [133.0, 63.0], [133.0, 91.0], [133.0, 105.0], [133.0, 119.0], [133.0, 133.0], [133.0, 161.0], [133.0, 175.0], [133.0, 245.0], [133.0, 259.0], [133.0, 287.0], [133.0, 315.0], [147.0, 7.0], [147.0, 21.0], [147.0, 35.0], [147.0, 49.0], [147.0, 91.0], [147.0, 105.0], [147.0, 119.0], [147.0, 133.0], [147.0, 161.0], [147.0, 203.0], [147.0, 217.0], [147.0, 273.0], [147.0, 287.0], [147.0, 315.0], [161.0, 7.0], [161.0, 21.0], [161.0, 35.0], [161.0, 49.0], [161.0, 63.0], [161.0, 77.0], [161.0, 91.0], [161.0, 105.0], [161.0, 119.0], [161.0, 133.0], [161.0, 147.0], [161.0, 161.0], [161.0, 203.0], [161.0, 217.0], [161.0, 315.0], [175.0, 49.0], [175.0, 63.0], [175.0, 77.0], [175.0, 91.0], [175.0, 105.0], [175.0, 119.0], [175.0, 133.0], [175.0, 147.0], [175.0, 161.0], [175.0, 231.0], [175.0, 245.0], [175.0, 273.0], [175.0, 287.0], [175.0, 315.0], [189.0, 49.0], [189.0, 63.0], [189.0, 77.0], [189.0, 91.0], [189.0, 161.0], [189.0, 231.0], [189.0, 245.0], [189.0, 259.0], [189.0, 273.0], [189.0, 287.0], [189.0, 301.0], [189.0, 315.0], [203.0, 49.0], [203.0, 63.0], [203.0, 77.0], [203.0, 91.0], [203.0, 105.0], [203.0, 161.0], [203.0, 175.0], [203.0, 189.0], [203.0, 273.0], [203.0, 287.0], [203.0, 301.0], [203.0, 315.0], [217.0, 49.0], [217.0, 63.0], [217.0, 161.0], [217.0, 175.0], [217.0, 189.0], [217.0, 217.0], [217.0, 231.0], [217.0, 245.0], [217.0, 259.0], [217.0, 273.0], [217.0, 287.0], [217.0, 301.0], [231.0, 49.0], [231.0, 63.0], [231.0, 77.0], [231.0, 119.0], [231.0, 133.0], [231.0, 147.0], [231.0, 161.0], [231.0, 203.0], [231.0, 217.0], [231.0, 231.0], [231.0, 245.0], [231.0, 259.0], [245.0, 63.0], [245.0, 77.0], [245.0, 91.0], [245.0, 105.0], [245.0, 161.0], [245.0, 175.0], [245.0, 189.0], [245.0, 203.0], [245.0, 217.0], [259.0, 77.0], [259.0, 91.0], [259.0, 105.0], [259.0, 119.0], [259.0, 133.0], [259.0, 147.0], [259.0, 161.0], [259.0, 175.0], [259.0, 189.0]]
	flower = [[7.0, 77.0], [7.0, 91.0], [7.0, 105.0], [7.0, 119.0], [7.0, 133.0], [7.0, 147.0], [7.0, 161.0], [7.0, 175.0], [7.0, 189.0], [7.0, 203.0], [7.0, 217.0], [7.0, 231.0], [21.0, 63.0], [21.0, 77.0], [21.0, 91.0], [21.0, 105.0], [21.0, 119.0], [21.0, 133.0], [21.0, 147.0], [21.0, 161.0], [21.0, 175.0], [21.0, 189.0], [21.0, 203.0], [21.0, 217.0], [21.0, 231.0], [21.0, 245.0], [35.0, 63.0], [35.0, 77.0], [35.0, 105.0], [35.0, 119.0], [35.0, 133.0], [35.0, 175.0], [35.0, 189.0], [35.0, 203.0], [35.0, 217.0], [35.0, 231.0], [35.0, 245.0], [49.0, 35.0], [49.0, 49.0], [49.0, 63.0], [49.0, 77.0], [49.0, 91.0], [49.0, 105.0], [49.0, 119.0], [49.0, 147.0], [49.0, 161.0], [49.0, 175.0], [49.0, 189.0], [49.0, 203.0], [49.0, 231.0], [49.0, 245.0], [49.0, 259.0], [63.0, 21.0], [63.0, 35.0], [63.0, 49.0], [63.0, 63.0], [63.0, 77.0], [63.0, 91.0], [63.0, 105.0], [63.0, 119.0], [63.0, 133.0], [63.0, 147.0], [63.0, 161.0], [63.0, 175.0], [63.0, 189.0], [63.0, 203.0], [63.0, 217.0], [63.0, 231.0], [63.0, 245.0], [63.0, 259.0], [63.0, 273.0], [77.0, 21.0], [77.0, 35.0], [77.0, 49.0], [77.0, 77.0], [77.0, 91.0], [77.0, 105.0], [77.0, 119.0], [77.0, 133.0], [77.0, 147.0], [77.0, 161.0], [77.0, 175.0], [77.0, 189.0], [77.0, 203.0], [77.0, 217.0], [77.0, 231.0], [77.0, 245.0], [77.0, 259.0], [77.0, 273.0], [77.0, 287.0], [91.0, 21.0], [91.0, 35.0], [91.0, 49.0], [91.0, 77.0], [91.0, 91.0], [91.0, 105.0], [91.0, 119.0], [91.0, 133.0], [91.0, 147.0], [91.0, 161.0], [91.0, 175.0], [91.0, 189.0], [91.0, 203.0], [91.0, 217.0], [91.0, 259.0], [91.0, 273.0], [91.0, 287.0], [105.0, 7.0], [105.0, 21.0], [105.0, 35.0], [105.0, 49.0], [105.0, 77.0], [105.0, 91.0], [105.0, 105.0], [105.0, 119.0], [105.0, 133.0], [105.0, 147.0], [105.0, 161.0], [105.0, 175.0], [105.0, 189.0], [105.0, 203.0], [105.0, 217.0], [105.0, 231.0], [105.0, 259.0], [105.0, 273.0], [105.0, 287.0], [119.0, 7.0], [119.0, 21.0], [119.0, 35.0], [119.0, 49.0], [119.0, 63.0], [119.0, 77.0], [119.0, 91.0], [119.0, 105.0], [119.0, 119.0], [119.0, 175.0], [119.0, 189.0], [119.0, 203.0], [119.0, 217.0], [119.0, 231.0], [119.0, 259.0], [119.0, 273.0], [119.0, 287.0], [133.0, 7.0], [133.0, 21.0], [133.0, 35.0], [133.0, 49.0], [133.0, 63.0], [133.0, 77.0], [133.0, 91.0], [133.0, 105.0], [133.0, 119.0], [133.0, 189.0], [133.0, 203.0], [133.0, 217.0], [133.0, 231.0], [133.0, 245.0], [133.0, 259.0], [133.0, 273.0], [133.0, 287.0], [147.0, 7.0], [147.0, 21.0], [147.0, 49.0], [147.0, 63.0], [147.0, 77.0], [147.0, 91.0], [147.0, 105.0], [147.0, 189.0], [147.0, 203.0], [147.0, 217.0], [147.0, 231.0], [147.0, 245.0], [147.0, 259.0], [147.0, 273.0], [147.0, 287.0], [161.0, 7.0], [161.0, 21.0], [161.0, 35.0], [161.0, 49.0], [161.0, 63.0], [161.0, 77.0], [161.0, 91.0], [161.0, 105.0], [161.0, 119.0], [161.0, 189.0], [161.0, 203.0], [161.0, 217.0], [161.0, 231.0], [161.0, 245.0], [161.0, 259.0], [161.0, 273.0], [161.0, 287.0], [175.0, 7.0], [175.0, 21.0], [175.0, 35.0], [175.0, 49.0], [175.0, 63.0], [175.0, 77.0], [175.0, 91.0], [175.0, 105.0], [175.0, 119.0], [175.0, 133.0], [175.0, 175.0], [175.0, 189.0], [175.0, 203.0], [175.0, 217.0], [175.0, 231.0], [175.0, 245.0], [175.0, 259.0], [175.0, 273.0], [175.0, 287.0], [189.0, 21.0], [189.0, 35.0], [189.0, 77.0], [189.0, 91.0], [189.0, 105.0], [189.0, 119.0], [189.0, 133.0], [189.0, 147.0], [189.0, 161.0], [189.0, 175.0], [189.0, 189.0], [189.0, 203.0], [189.0, 217.0], [189.0, 245.0], [189.0, 259.0], [189.0, 273.0], [189.0, 287.0], [203.0, 21.0], [203.0, 35.0], [203.0, 77.0], [203.0, 91.0], [203.0, 105.0], [203.0, 119.0], [203.0, 133.0], [203.0, 147.0], [203.0, 161.0], [203.0, 175.0], [203.0, 189.0], [203.0, 203.0], [203.0, 217.0], [203.0, 259.0], [203.0, 273.0], [217.0, 21.0], [217.0, 35.0], [217.0, 49.0], [217.0, 77.0], [217.0, 91.0], [217.0, 105.0], [217.0, 119.0], [217.0, 133.0], [217.0, 147.0], [217.0, 161.0], [217.0, 175.0], [217.0, 189.0], [217.0, 203.0], [217.0, 217.0], [217.0, 259.0], [217.0, 273.0], [231.0, 21.0], [231.0, 35.0], [231.0, 49.0], [231.0, 63.0], [231.0, 77.0], [231.0, 91.0], [231.0, 105.0], [231.0, 119.0], [231.0, 133.0], [231.0, 147.0], [231.0, 161.0], [231.0, 175.0], [231.0, 189.0], [231.0, 203.0], [231.0, 217.0], [231.0, 231.0], [231.0, 245.0], [231.0, 259.0], [231.0, 273.0], [245.0, 49.0], [245.0, 63.0], [245.0, 77.0], [245.0, 105.0], [245.0, 119.0], [245.0, 147.0], [245.0, 161.0], [245.0, 175.0], [245.0, 189.0], [245.0, 203.0], [245.0, 217.0], [245.0, 231.0], [245.0, 245.0], [245.0, 259.0], [245.0, 273.0], [259.0, 49.0], [259.0, 63.0], [259.0, 77.0], [259.0, 105.0], [259.0, 119.0], [259.0, 175.0], [259.0, 189.0], [259.0, 217.0], [259.0, 231.0], [273.0, 49.0], [273.0, 63.0], [273.0, 77.0], [273.0, 91.0], [273.0, 105.0], [273.0, 119.0], [273.0, 133.0], [273.0, 161.0], [273.0, 175.0], [273.0, 189.0], [273.0, 203.0], [273.0, 217.0], [273.0, 231.0], [287.0, 63.0], [287.0, 77.0], [287.0, 91.0], [287.0, 105.0], [287.0, 119.0], [287.0, 133.0], [287.0, 147.0], [287.0, 161.0], [287.0, 175.0], [287.0, 189.0], [287.0, 203.0], [287.0, 217.0], [287.0, 231.0]]
	strawberry = []
	wireframe_orbit(flower,strawberry, num_frames=40, line_length=0, dimensions=[400,400])
	# wireframe_orbit(set1, set2, num_frames=40, line_length=0, dimensions=[1000,1000])
	# wireframe_orbit(set1,set2,num_frames=20,line_length=1000,dimensions=[1000,1000])
