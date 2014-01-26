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

map_two = {' ' : ' ',
        '\n' : '\n',
        '101' : '101',
        '110' : '120',
        '120' : '130',
        '130' : '140',
        '140' : '110',
        '410' : '420',
        '420' : '430',
        '430' : '440',
        '440' : '410',
        '500' : '500',
        '200' : '200'}

map_three = {' ' : ' ',
        '\n' : '\n',
        '101' : '101',
        '110' : '130',
        '120' : '140',
        '130' : '110',
        '140' : '120',
        '410' : '430',
        '420' : '440',
        '430' : '410',
        '440' : '420',
        '500' : '500',
        '200': '200'}

map_four = {' ' : ' ',
        '\n' : '\n',
        '101' : '101',
        '110' : '140',
        '120' : '110',
        '130' : '120',
        '140' : '130',
        '410' : '440',
        '420' : '410',
        '430' : '420',
        '440' : '430',
        '500' : '500',
        '200' : '200'}

colormap = {'101' : (0,0,0,255),
            '200' : (33,33,33, 0),
            '500' : (255,255,255,0),
            '110' : (255,0,0,0),
            '120' : (0,255,0,0),
            '130' : (0,0,255,0),
            '140' : (125,125,0,0),
            '410' : (255,0,0,0),
            '420' : (0,255,0,0),
            '430' : (0,0,255,0),
            '440' : (125,125,0,0)}


palette_one = open(filename_palette_one, 'w')
palette_two = open(filename_palette_two, 'w')
palette_three = open(filename_palette_three, 'w')
palette_four = open(filename_palette_four, 'w')

paragraph_buffer_in = ""
p_one_line_buffer_out = ""
p_two_line_buffer_out = ""
p_three_line_buffer_out = ""
p_four_line_buffer_out = ""

paragraph_buffer_in = np.loadtxt(filename, dtype=int)
print paragraph_buffer_in

for row in paragraph_buffer_in:
    for col in row:
        print col
        p_one_line_buffer_out += str(col) 
        p_two_line_buffer_out += map_two[str(col)]
        p_three_line_buffer_out += map_three[str(col)]
        p_four_line_buffer_out += map_four[str(col)]
        p_one_line_buffer_out += ' ' 
        p_two_line_buffer_out += ' '
        p_three_line_buffer_out += ' '
        p_four_line_buffer_out += ' '


    p_one_line_buffer_out += '\n' 
    p_two_line_buffer_out += '\n'
    p_three_line_buffer_out += '\n'
    p_four_line_buffer_out += '\n'

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

barriers = pg.image.load("../assets/upbarrier_sheet.png")
red_barrier_rect = pg.Rect(8,0, 8, 24)
red_barrier = barriers.subsurface(red_barrier_rect) 

green_barrier_rect = pg.Rect(16,0, 8, 24)
green_barrier = barriers.subsurface(green_barrier_rect) 

blue_barrier_rect = pg.Rect(24,0, 8, 24)
blue_barrier = barriers.subsurface(blue_barrier_rect) 

yellow_barrier_rect = pg.Rect(0,0, 8, 24)
yellow_barrier = barriers.subsurface(yellow_barrier_rect) 

color_to_barrier = {'110' : red_barrier,
                    '120' : green_barrier,
                    '130' : blue_barrier,
                    '140' : yellow_barrier}

triangles = pg.image.load("../assets/triangle_sheet.png")
red_triangle_rect = pg.Rect(0,0, 36, 31)
red_triangle = triangles.subsurface(red_triangle_rect) 

green_triangle_rect = pg.Rect(36 ,0, 36, 31)
green_triangle = triangles.subsurface(green_triangle_rect) 

blue_triangle_rect = pg.Rect(108, 0, 36, 31)
blue_triangle = triangles.subsurface(blue_triangle_rect) 

yellow_triangle_rect = pg.Rect(72, 0, 36, 31)
yellow_triangle = triangles.subsurface(yellow_triangle_rect) 

color_to_triangle = {'410' : red_triangle,
                    '420' : green_triangle,
                    '430' : blue_triangle,
                    '440' : yellow_triangle}

tiles = pg.image.load("../assets/tile_sheet.png")
color_change_tile_rect = (0, 0,40, 40)
color_change_tile = tiles.subsurface(color_change_tile_rect)

corner_tile_rect = (40, 0,40, 40)
corner_tile = tiles.subsurface(color_change_tile_rect)




row = 0;
column = 0;

def draw_crude(level_map, row, column):
    """
    pg.draw.rect(p_one_level_render, colormap[mycharacter], block.move(block.width*mycolumn, block.height*myrow))
    pg.draw.rect(p_two_level_render, colormap[map_two[mycharacter]], block.move(block.width*mycolumn, block.height*myrow))
    pg.draw.rect(p_three_level_render, colormap[map_three[mycharacter]], block.move(block.width*mycolumn, block.height*myrow))
    pg.draw.rect(p_four_level_render, colormap[map_four[mycharacter]], block.move(block.width*mycolumn, block.height*myrow))
    """
    if str(level_map[row][column])[0] == '5':
        p_one_level_render.blit(pg.transform.scale(color_change_tile, (40,40)), (column*40, row*40))
        p_two_level_render.blit(pg.transform.scale(color_change_tile, (40,40)), (column*40, row*40))
        p_three_level_render.blit(pg.transform.scale(color_change_tile, (40,40)), (column*40, row*40))
        p_four_level_render.blit(pg.transform.scale(color_change_tile, (40,40)), (column*40, row*40))


    elif str(level_map[row][column])[0] == '4':
        p_one_level_render.blit(pg.transform.scale(color_to_triangle[str(level_map[row][column])], (40,40)), (column*40, row*40))
        p_two_level_render.blit(pg.transform.scale(color_to_triangle[map_two[str(level_map[row][column])]], (40,40)), (column*40, row*40))
        p_three_level_render.blit(pg.transform.scale(color_to_triangle[map_three[str(level_map[row][column])]], (40,40)), (column*40, row*40))
        p_four_level_render.blit(pg.transform.scale(color_to_triangle[map_four[str(level_map[row][column])]], (40,40)), (column*40, row*40))

    else: #str(level_map[row][column])[0] != '4':
        pg.draw.rect(p_one_level_render, colormap[str(level_map[row][column])], block.move(block.width*mycolumn, block.height*myrow))
        pg.draw.rect(p_two_level_render, colormap[map_two[str(level_map[row][column])]], block.move(block.width*mycolumn, block.height*myrow))
        pg.draw.rect(p_three_level_render, colormap[map_three[str(level_map[row][column])]], block.move(block.width*mycolumn, block.height*myrow))
        pg.draw.rect(p_four_level_render, colormap[map_four[str(level_map[row][column])]], block.move(block.width*mycolumn, block.height*myrow))




def draw_fancy(level_map, row, column):
    """
    pg.draw.rect(p_one_level_render, colormap[mycharacter], block.move(block.width*mycolumn, block.height*myrow))
    pg.draw.rect(p_two_level_render, colormap[map_two[mycharacter]], block.move(block.width*mycolumn, block.height*myrow))
    pg.draw.rect(p_three_level_render, colormap[map_three[mycharacter]], block.move(block.width*mycolumn, block.height*myrow))
    pg.draw.rect(p_four_level_render, colormap[map_four[mycharacter]], block.move(block.width*mycolumn, block.height*myrow))
    """
    direction = 'none'
    if (row % 2 == 0) and (column % 2 == 0):
        if str(level_map[row][column]) == '110' or str(level_map[row][column]) == '120' or str(level_map[row][column]) == '130' or str(level_map[row][column]) == '140': 
            if row < 2:
                if (column / 2) % 2 ==1:
                    direction = 'horizontal'
                else:
                    direction = 'none'

            elif str(level_map[row][column]) == str(level_map[row - 1][column]):
                if (row / 2) % 2 ==1:
                    direction = 'vertical'
                else:
                    direction = 'none'

            elif str(level_map[row][column]) == str(level_map[row][column +1]):
                if (column / 2) % 2 ==1:
                    direction = 'horizontal'
                else:
                    direction = 'none'
            else:
                direction = 'none'

            if direction == 'horizontal':
                p_one_level_render.blit(pg.transform.scale(pg.transform.rotate(color_to_barrier[str(level_map[row][column])], 90), (120,40)), ((column-1)*40, row*40))
                p_two_level_render.blit(pg.transform.scale(pg.transform.rotate(color_to_barrier[map_two[str(level_map[row][column])]], 90),(120,40)), ((column-1)*40, row*40))
                p_three_level_render.blit(pg.transform.scale(pg.transform.rotate(color_to_barrier[map_three[str(level_map[row][column])]], 90), (120,40)), ((column-1)*40, row*40))
                p_four_level_render.blit(pg.transform.scale(pg.transform.rotate(color_to_barrier[map_four[str(level_map[row][column])]], 90), (120,40)), ((column-1)*40, row*40))
            elif direction == 'vertical': 
                p_one_level_render.blit(pg.transform.scale(color_to_barrier[str(level_map[row][column])], (40,120)), (column*40, (row-1)*40))
                p_two_level_render.blit(pg.transform.scale(color_to_barrier[map_two[str(level_map[row][column])]], (40,120)), (column*40, (row-1)*40))
                p_three_level_render.blit(pg.transform.scale(color_to_barrier[map_three[str(level_map[row][column])]], (40,120)), (column*40, (row-1)*40))
                p_four_level_render.blit(pg.transform.scale(color_to_barrier[map_four[str(level_map[row][column])]], (40,120)), (column*40, (row-1)*40))

for row in range(len(level_map)):
    for column in range(len(level_map[0,:])):
        myrow = row
        mycolumn = column

        draw_crude(level_map, row, column)

for row in range(len(level_map)):
    for column in range(len(level_map[0,:])):
        myrow = row
        mycolumn = column

        draw_fancy(level_map, row, column)


pg.image.save(p_one_level_render, filename + "_palette_one.png")
pg.image.save(p_two_level_render, filename + "_palette_two.png")
pg.image.save(p_three_level_render, filename + "_palette_three.png")
pg.image.save(p_four_level_render, filename + "_palette_four.png")


