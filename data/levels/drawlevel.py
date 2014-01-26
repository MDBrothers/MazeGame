#!/usr/bin/python

import pygame as pg
import numpy as np
import sys
import os

filename = sys.argv[-1] 

myrow = 0
mycolumn = 0

filename_palette_one = filename + "_palette_one.lev"
filename_palette_two = filename + "_palette_two.lev"
filename_palette_three = filename + "_palette_three.lev"
filename_palette_four = filename + "_palette_four.lev"

map_two = {'1' : '2',
        '2' : '3',
        '3' : '4',
        '4' : '1',
        ' ' : ' ',
        '\n' : '\n',
        '0' : '0',
        '11' : '11'}

map_three = {'1' : '3',
        '2' : '4',
        '3' : '1',
        '4' : '2',
        ' ' : ' ',
        '\n' : '\n',
        '0' : '0',
        '11' : '11'}

map_four = {'1' : '4',
        '2' : '1',
        '3' : '2',
        '4' : '3',
        ' ' : ' ',
        '\n' : '\n',
        '0' : '0',
        '11' : '11'}

colormap = {'0' : (0,0,0,255),
            '1' : (255,0,0,0),
            '2' : (0,255,0,0),
            '3' : (0,0,255,0),
            '4' : (125,125,0,0),
            '11' : (255,255,255,0),
            '22' : (255,255,255,0),
            '33' : (255,255,255,0),
            '44' : (255,255,255,0)}

palette_one = open(filename_palette_one, 'w')
palette_two = open(filename_palette_two, 'w')
palette_three = open(filename_palette_three, 'w')
palette_four = open(filename_palette_four, 'w')

paragraph_buffer_in = ""
p_one_line_buffer_out = ""
p_two_line_buffer_out = ""
p_three_line_buffer_out = ""
p_four_line_buffer_out = ""

template_file = open(filename)
paragraph_buffer_in = template_file.readlines()

for line in paragraph_buffer_in:
    for character in line:
        p_one_line_buffer_out += character
        p_two_line_buffer_out += map_two[character]
        p_three_line_buffer_out += map_three[character]
        p_four_line_buffer_out += map_four[character]

    palette_one.write(p_one_line_buffer_out)
    palette_two.write(p_two_line_buffer_out)
    palette_three.write(p_three_line_buffer_out)
    palette_four.write(p_four_line_buffer_out)

    p_one_line_buffer_out = ""
    p_two_line_buffer_out = ""
    p_three_line_buffer_out = ""
    p_four_line_buffer_out = ""

palette_one.close()
palette_two.close()
palette_three.close()
palette_four.close()

level_map = np.loadtxt(filename, dtype=int)

p_one_level_render = pg.Surface((level_map.shape[1]*40, level_map.shape[0]*40))
p_two_level_render = pg.Surface((level_map.shape[1]*40, level_map.shape[0]*40))
p_three_level_render = pg.Surface((level_map.shape[1]*40, level_map.shape[0]*40))
p_four_level_render = pg.Surface((level_map.shape[1]*40, level_map.shape[0]*40))

block = pg.Rect(0,0, p_one_level_render.get_width()/level_map.shape[1], p_two_level_render.get_height()/level_map.shape[0])

row = 0;
column = 0;

def draw(mycharacter):
    pg.draw.rect(p_one_level_render, colormap[mycharacter], block.move(block.width*mycolumn, block.height*myrow))
    pg.draw.rect(p_two_level_render, colormap[map_two[mycharacter]], block.move(block.width*mycolumn, block.height*myrow))
    pg.draw.rect(p_three_level_render, colormap[map_three[mycharacter]], block.move(block.width*mycolumn, block.height*myrow))
    pg.draw.rect(p_four_level_render, colormap[map_four[mycharacter]], block.move(block.width*mycolumn, block.height*myrow))


for row in range(len(level_map)):
    for column in range(len(level_map[0,:])):
        myrow = row
        mycolumn = column

        draw(str(level_map[row][column]))

        column += 1
            
    column = 0
    row += 1

pg.image.save(p_one_level_render, filename + "_palette_one.png")
pg.image.save(p_two_level_render, filename + "_palette_two.png")
pg.image.save(p_three_level_render, filename + "_palette_three.png")
pg.image.save(p_four_level_render, filename + "_palette_four.png")


