#!/usr/bin/python

"""
This is what I was thinking for the path generation itself, paths beginning at paths, no circling back

The next step is to translate paths into a path or barrier maze input file legible by the art generator
and legible by the game engine. Path or barrier colors and locations of special features need to be
somehow indicated.

Michael
"""

import matplotlib.pyplot as plt
import numpy as np

maze_size = 100
numpaths = 50
pathlength_max = 5

iterations = 0
paths = []

for path in range(numpaths):
        paths.append([[0,0]])

def find_all_neighbors(my_point):
        top = [my_point[0], my_point[1] + 1]
        bottom = [my_point[0], my_point[1] - 1]
        left = [my_point[0] - 1, my_point[1]]
        right = [my_point[0] + 1, my_point[1]]
        return [top, bottom, left, right]

def find_available_neighbors(my_point_array, all_point_arrays):
        candidates = find_all_neighbors(my_point_array[-1])
        available = []

	mustremove = False

	for cpoint in candidates:
		mustremove = False
		for point_array in all_point_arrays:
			if cpoint in point_array:
				mustremove = True
				break
					
		if (cpoint[0] > maze_size):
				mustremove = True

		elif  (cpoint[0] < 0):
				mustremove = True

		elif  (cpoint[1] > maze_size): 
				mustremove = True

		elif (cpoint[1] < 0):
				mustremove = True

		if mustremove == False:
			available.append(cpoint)

        return available

def expand_path(my_point_array, available):
        length = len(available)
        if length > 0:
                selection = np.random.randint(0, length)
                my_point_array.append(available[selection])

starting_point = [maze_size/2,maze_size/2]

for pathnumber in range(numpaths):
	paths[pathnumber][0] = starting_point		
        for iteration in range(pathlength_max):
                expand_path(paths[pathnumber], find_available_neighbors(paths[pathnumber], paths))
	
        starting_point = (paths[pathnumber][np.random.randint(0, len(paths[pathnumber]))], paths)[0]
	while not starting_point and iterations < 100:
		iterations += 1
        	starting_point = (paths[pathnumber][np.random.randint(0, len(paths[pathnumber]))], paths)[0]

        path_array = np.array(paths[pathnumber])
        #plt.scatter(path_array[:,0] , path_array[:,1])
        plt.plot(path_array[:,0] , path_array[:,1], linewidth = 2*(pathnumber + 1))

plt.show()

