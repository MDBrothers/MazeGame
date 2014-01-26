#!/usr/bin/python

import os
import sys
import pygame as pg
import numpy as np
import audio
import player
import furniture

CAPTION = "Perspectrum"

COLORMAP = {'101' : (0,0,0,255),
            '200' : (33,33,33, 0),
            '110' : (255,0,0,0),
            '120' : (0,255,0,0),
            '130' : (0,0,255,0),
            '140' : (125,125,0,0)}

class Control(object): 
    def __init__(self):
        """Initialize the display and create a player and level."""
        self.screen = pg.display.get_surface()

        self.current_palette = '1'
        self.enable_palette_change = False
        self.palette_transition_map = {'1' : '2',
                                       '2' : '3',
                                       '3' : '4',
                                       '4' : '1'}

        self.background =  pg.image.load("../data/levels/level1.lev.png")
        self.background_one =  pg.image.load("../data/levels/level1_palette_one.png")
        self.background_two =  pg.image.load("../data/levels/level1_palette_two.png")
        self.background_three =  pg.image.load("../data/levels/level1_palette_three.png")
        self.background_four =  pg.image.load("../data/levels/level1_palette_four.png")

        self.surface_palette_map = {'1' : self.background_one,
                            '2' : self.background_two,
                            '3' : self.background_three,
                            '4' : self.background_four}

        self.background_position = [0,0]
        self.screen_rect = self.screen.get_rect()

        self.level_map = np.loadtxt("../data/levels/level1_palette_one.lev", dtype=int)

        self.p_one_level_map = np.loadtxt("../data/levels/level1_palette_one.lev", dtype=int)
        self.p_two_level_map = np.loadtxt("../data/levels/level1_palette_two.lev", dtype=int)
        self.p_three_level_map = np.loadtxt("../data/levels/level1_palette_three.lev", dtype=int)
        self.p_four_level_map = np.loadtxt("../data/levels/level1_palette_four.lev", dtype=int)

        self.level_palette_map = {'1' : self.p_one_level_map,
                                  '2' : self.p_two_level_map,
                                  '3' : self.p_three_level_map,
                                  '4' : self.p_four_level_map}


        """The grid spacing depends on the screen resultion, and the number of tiles"""
        self.grid_spacing = self.screen.get_size()[0]/self.level_map.shape[1]*8

        self.playerSurface =  pg.transform.scale(pg.image.load("../data/assets/ball_sheet.png"), (4*self.grid_spacing, 2*self.grid_spacing))
        #self.furnitureSurface =  pg.transform.scale(pg.image.load("../data/assets/triangle_sheet.png"), (4*self.grid_spacing, self.grid_spacing))

        self.clock = pg.time.Clock()
        self.fps = 35.0
        self.keys = pg.key.get_pressed()
        self.done = False
        self.commence = False
        self.toggle = False
        self.coordinate_multiplier = 4 #This is the number of big tiles per row or column

        self.player_one_global_position = [0, 0]
        self.player_one_local_position = [0, 0]

        self.player_one = player.Player('140', self.player_one_local_position, self.grid_spacing, self.grid_spacing, 'player_one', self.playerSurface)
        #self.triangle_one = furniture.Furniture('140', '140', [3,3], self.grid_spacing, self.grid_spacing, 'dark_forces', self.furnitureSurface)
        #self.triangle_two = furniture.Furniture('140', '140', [2,2], self.grid_spacing, self.grid_spacing, 'dark_forces', self.furnitureSurface)

        #self.furniture = [self.triangle_one, self.triangle_two]
        self.special_effect_map = {'500' : self.on_palette_change(),
                                   '410' : self.change_player_color('110'),
                                   '420' : self.change_player_color('120'),
                                   '430' : self.change_player_color('130'),
                                   '440' : self.change_player_color('140'),
                                   '101' : self.off_palette_change(),
                                   '200' : self.off_palette_change(),
                                   '110' : self.off_palette_change(),
                                   '120' : self.off_palette_change(),
                                   '130' : self.off_palette_change(),
                                   '140' : self.off_palette_change()}


    def do_nothing(self):
        ze_goggles = 'they do nothing'

    def on_palette_change(self):
        return True

    def off_palette_change(self):
        return False 

    
    def map_tile_effect(self):
        #print str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])

        self.enable_palette_change = self.special_effect_map[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])]

        #print self.enable_palette_change

    def movement_refused(self):
        print "OOOFF!"

    def change_player_color(self, color):
        print "Happens!"
        self.player_one.mystate['color'] = color
        return False


    def negotiate_left_movement(self):
        if self.player_one_global_position[0] < 1:
            return self.movement_refused()
        elif COLORMAP[self.player_one.mystate['color']] == COLORMAP[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier])]:

            if self.player_one_local_position[0] == 1 and self.player_one_global_position[0] > 1:
                #self.background.scroll(0, +int(self.grid_spacing))
                self.background_position[0] += self.grid_spacing
                self.player_one_global_position[0] -= 1
                #print "I am scrolling"
            else:
                self.player_one_global_position[0] -= 1
                self.player_one_local_position[0] -= 1 

            #print self.player_one_local_position
            self.player_one.move_to_coordinates(self.player_one_local_position)

        else:
            return self.movement_refused()
     
    def negotiate_right_movement(self):
        if self.player_one_global_position[0] > (self.level_map.shape[1]/self.coordinate_multiplier - 2):
            return self.movement_refused()
        elif COLORMAP[self.player_one.mystate['color']] == COLORMAP[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier])]:

            if self.player_one_local_position[0] == 2 and self.player_one_global_position[0] < (self.level_map.shape[1]/self.coordinate_multiplier-2):
                self.background_position[0] -= self.grid_spacing
                self.player_one_global_position[0] += 1
                #print "I am scrolling"
            else:
                self.player_one_global_position[0] += 1
                self.player_one_local_position[0] += 1 

            #print self.player_one_local_position
            self.player_one.move_to_coordinates(self.player_one_local_position)

        else:
            return self.movement_refused()

    def negotiate_up_movement(self):
        if self.player_one_local_position[1] < 1:
            return self.movement_refused()
        elif COLORMAP[self.player_one.mystate['color']] == COLORMAP[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])]:
           
            if self.player_one_local_position[1] == 1 and self.player_one_global_position[1] > 1:
                #self.background.scroll(0, +int(self.grid_spacing))
                self.background_position[1] += self.grid_spacing
                self.player_one_global_position[1] -= 1
                #print "I am scrolling"
            else:
                self.player_one_global_position[1] -= 1
                self.player_one_local_position[1] -= 1 

            #print self.player_one_local_position
            self.player_one.move_to_coordinates(self.player_one_local_position)

        else:
            return self.movement_refused()

    def negotiate_down_movement(self):
        if self.player_one_global_position[1] > (self.level_map.shape[0]/self.coordinate_multiplier - 2):
            return self.movement_refused()

        elif COLORMAP[self.player_one.mystate['color']] == COLORMAP[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])]:
            self.player_one_global_position = self.player_one_global_position
            self.player_one_local_position = self.player_one_local_position

            if self.player_one_local_position[1] == 2 and self.player_one_global_position[1] < (self.level_map.shape[0]/self.coordinate_multiplier-2):
               # self.background.scroll(0, -int(self.grid_spacing))
                self.background_position[1] -= self.grid_spacing

                self.player_one_global_position[1] += 1
                #print "I am scrolling"
            else:
                self.player_one_global_position[1] += 1
                self.player_one_local_position[1] += 1 

            #print self.player_one_local_position
            self.player_one.move_to_coordinates(self.player_one_local_position)
        else:
            return self.movement_refused()

    def increment_palette(self):
        self.current_palette = self.palette_transition_map[self.current_palette]

    def event_loop(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.commence = True
                elif event.key == pg.K_LEFT:
                    self.negotiate_left_movement()

                elif event.key == pg.K_RIGHT:
                    self.negotiate_right_movement()

                elif event.key == pg.K_UP:
                    self.negotiate_up_movement()

                elif event.key == pg.K_DOWN:
                    self.negotiate_down_movement()

                elif event.key == pg.K_SPACE:
                    self.map_tile_effect()
                    if self.enable_palette_change:
                        self.increment_palette()

                elif event.key == pg.K_q:
                    self.increment_palette()

                elif event.key == pg.K_1:
                    self.player_one.mystate['color'] = '110'

                elif event.key == pg.K_2:
                    self.player_one.mystate['color'] = '120'

                elif event.key == pg.K_3:
                    self.player_one.mystate['color'] = '130'

                elif event.key == pg.K_4:
                    self.player_one.mystate['color'] = '140'




    def enforce_palette(self):
        self.background = self.surface_palette_map[self.current_palette]
        self.level_map = self.level_palette_map[self.current_palette]

    def update(self):
        self.screen.fill((0,0,0))
        self.background.set_colorkey((0,0,0))
        self.screen.blit(self.background, self.background_position)
        
        #self.triangle_one.draw(self.screen)
        #self.triangle_two.draw(self.screen)

        self.player_one.draw(self.screen)
        
        self.enforce_palette()

        caption = "{} - FPS: {:.2f}".format(CAPTION,self.clock.get_fps())
        pg.display.set_caption(caption)

    def main_loop(self):
        """Run around."""
        while not self.commence:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)

        while not self.done:
            self.event_loop()
            self.update()
            pg.display.flip()
            self.clock.tick(self.fps)

if __name__ == "__main__":
    resolution = (640,640)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_mode(resolution)
    music_loaded = audio.load_music('../data/audio/pontiff.ogg')
    if music_loaded:
        pg.mixer.music.play(-1)
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    sys.exit()
