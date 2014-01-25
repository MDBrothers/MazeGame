#!/usr/bin/python

import pygame as pg
import numpy as np
import sys
import os

filename = sys.argv[-1] 

level_map = np.loadtxt(filename, dtype=int)

level_render = pg.Surface((640, 640))
print len(level_map)
barrier = pg.Rect(0,0, level_render.get_width()/len(level_map), level_render.get_width()/len(level_map[0]))
background = pg.Rect(0,0, level_render.get_width()/len(level_map), level_render.get_width()/len(level_map[0]))
print barrier.width

row = 0;
column = 0;

print level_map

for row in range(len(level_map)):
    for column in range(len(level_map[0,:])):
        if level_map[row, column] == 2:
            print str(row) + ", " + str(column)
            pg.draw.rect(level_render, (255,0,0), barrier.move(barrier.width*column, barrier.height*row))

        else:
            pg.draw.rect(level_render, (0,255,0), background.move(background.width*column, background.height*row))

        column += 1
            
    column = 0
    row += 1

pg.image.save(level_render, filename + ".png")
