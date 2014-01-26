#!/usr/bin/python

import os
import sys
import pygame as pg
import numpy as np
import audio
import player
import ananab
import intro

pg.font.init()
myFont = pg.font.SysFont('arial', 56, bold=True, italic=True)
mySmallfont = pg.font.SysFont('arial', 26, bold=False, italic=False)


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
        self.enable_player_color_change = False
        self.win = False

        self.palette_transition_map = {'1' : '2',
                                       '2' : '3',
                                       '3' : '4',
                                       '4' : '1'}

        self.background_one =  pg.image.load("../data/levels/level_1/level1_palette_one.png")
        self.background_two =  pg.image.load("../data/levels/level_1/level1_palette_two.png")
        self.background_three =  pg.image.load("../data/levels/level_1/level1_palette_three.png")
        self.background_four =  pg.image.load("../data/levels/level_1/level1_palette_four.png")

        self.surface_palette_map = {'1' : self.background_one,
                            '2' : self.background_two,
                            '3' : self.background_three,
                            '4' : self.background_four}

        self.background = self.background_one
        self.background_position = [0,0]
        self.screen_rect = self.screen.get_rect()

        self.level_one_background_one =  pg.image.load("../data/levels/level_1/level1_palette_one.png")
        self.level_one_background_two =  pg.image.load("../data/levels/level_1/level1_palette_two.png")
        self.level_one_background_three =  pg.image.load("../data/levels/level_1/level1_palette_three.png")
        self.level_one_background_four =  pg.image.load("../data/levels/level_1/level1_palette_four.png")
        self.level_one_map = np.loadtxt("../data/levels/level_1/level1_palette_one.lev", dtype=int)
        self.p_one_level_one_map = np.loadtxt("../data/levels/level_1/level1_palette_one.lev", dtype=int)
        self.p_two_level_one_map = np.loadtxt("../data/levels/level_1/level1_palette_two.lev", dtype=int)
        self.p_three_level_one_map = np.loadtxt("../data/levels/level_1/level1_palette_three.lev", dtype=int)
        self.p_four_level_one_map = np.loadtxt("../data/levels/level_1/level1_palette_four.lev", dtype=int)
        self.level_one_palette_map = {'1' : self.p_one_level_one_map,
                                  '2' : self.p_two_level_one_map,
                                  '3' : self.p_three_level_one_map,
                                  '4' : self.p_four_level_one_map}

        self.level_map = self.level_one_map
        self.level_palette_map = self.level_one_palette_map

        self.level_two_background_one =  pg.image.load("../data/levels/level_2/level2_palette_one.png")
        self.level_two_background_two =  pg.image.load("../data/levels/level_2/level2_palette_two.png")
        self.level_two_background_three =  pg.image.load("../data/levels/level_2/level2_palette_three.png")
        self.level_two_background_four =  pg.image.load("../data/levels/level_2/level2_palette_four.png")
        self.level_two_map = np.loadtxt("../data/levels/level_2/level2_palette_one.lev", dtype=int)
        self.p_one_level_two_map = np.loadtxt("../data/levels/level_2/level2_palette_one.lev", dtype=int)
        self.p_two_level_two_map = np.loadtxt("../data/levels/level_2/level2_palette_two.lev", dtype=int)
        self.p_three_level_two_map = np.loadtxt("../data/levels/level_2/level2_palette_three.lev", dtype=int)
        self.p_four_level_two_map = np.loadtxt("../data/levels/level_2/level2_palette_four.lev", dtype=int)
        self.level_two_palette_map = {'1' : self.p_one_level_two_map,
                                  '2' : self.p_two_level_two_map,
                                  '3' : self.p_three_level_two_map,
                                  '4' : self.p_four_level_two_map}

        self.level_three_background_one =  pg.image.load("../data/levels/level_3/level3_palette_one.png")
        self.level_three_background_two =  pg.image.load("../data/levels/level_3/level3_palette_two.png")
        self.level_three_background_three =  pg.image.load("../data/levels/level_3/level3_palette_three.png")
        self.level_three_background_four =  pg.image.load("../data/levels/level_3/level3_palette_four.png")
        self.level_three_map = np.loadtxt("../data/levels/level_3/level3_palette_one.lev", dtype=int)
        self.p_one_level_three_map = np.loadtxt("../data/levels/level_3/level3_palette_one.lev", dtype=int)
        self.p_two_level_three_map = np.loadtxt("../data/levels/level_3/level3_palette_two.lev", dtype=int)
        self.p_three_level_three_map = np.loadtxt("../data/levels/level_3/level3_palette_three.lev", dtype=int)
        self.p_four_level_three_map = np.loadtxt("../data/levels/level_3/level3_palette_four.lev", dtype=int)
        self.level_three_palette_map = {'1' : self.p_one_level_three_map,
                                  '2' : self.p_two_level_three_map,
                                  '3' : self.p_three_level_three_map,
                                  '4' : self.p_four_level_three_map}

        """The grid spacing depends on the screen resultion, and the number of tiles"""
        self.load_level_one()
        self.playerSurface =  pg.transform.scale(pg.image.load("../data/assets/ball_sheet.png"), (4*self.grid_spacing, 2*self.grid_spacing))
        self.ananabSurface =  pg.transform.scale(pg.image.load("../data/assets/maximum_leader.png"), (4*self.grid_spacing, 10*self.grid_spacing))
        self.introSurface =  pg.transform.scale(pg.image.load("../data/assets/title.png"), (7*self.grid_spacing, 2*self.grid_spacing))

        self.clock = pg.time.Clock()
        self.fps = 35.0
        self.keys = pg.key.get_pressed()
        self.done = False
        self.commence = False
        self.toggle = False
        self.coordinate_multiplier = 4 #This is the number of big tiles per row or column

        self.player_one_global_position = [0, 3]
        self.player_one_local_position = [0, 3]

        self.player_one = player.Player('130', self.player_one_local_position, self.grid_spacing, self.grid_spacing, 'player_one', self.playerSurface)

        self.ananab = ananab.Ananab([0,0], 2*self.grid_spacing, 5*self.grid_spacing, self.ananabSurface)
        self.intro = intro.Intro([0,0], 7*self.grid_spacing, 2*self.grid_spacing, self.introSurface)


        self.special_effect_map = {'500' : self.on_palette_change(),
                                   '410' : self.on_change_player_color(),
                                   '420' : self.on_change_player_color(),
                                   '430' : self.on_change_player_color(),
                                   '440' : self.on_change_player_color(),
                                   '900' : self.toggle_win(),
                                   '101' : self.off_palette_change(),
                                   '200' : self.off_palette_change(),
                                   '110' : self.off_palette_change(),
                                   '120' : self.off_palette_change(),
                                   '130' : self.off_palette_change(),
                                   '140' : self.off_palette_change()}

        self.special_colormap = {'410' : '110',
                                 '420' : '120',
                                 '430' : '130',
                                 '440' : '140'}


    def load_level_one(self):
        self.grid_spacing = self.screen.get_size()[1]/self.level_one_map.shape[0]*4
        self.background = self.level_one_background_one
        self.background_one = self.level_one_background_one
        self.background_two =  self.level_one_background_two
        self.background_three =  self.level_one_background_three
        self.background_four =  self.level_one_background_four
        self.p_one_level_map = self.p_one_level_one_map
        self.p_two_level_map = self.p_two_level_one_map
        self.p_three_level_map = self.p_three_level_one_map
        self.p_four_level_map = self.p_four_level_one_map
        self.level_map = self.level_one_map
        self.level_palette_map = self.level_one_palette_map

    def load_level_two(self):
        self.grid_spacing = self.screen.get_size()[1]/self.level_two_map.shape[0]*4
        self.background = self.level_two_background_one
        self.background_one = self.level_two_background_one
        self.background_two =  self.level_two_background_two
        self.background_three =  self.level_two_background_three
        self.background_four =  self.level_two_background_four
        self.p_one_level_map = self.p_one_level_two_map
        self.p_two_level_map = self.p_two_level_two_map
        self.p_three_level_map = self.p_three_level_two_map
        self.p_four_level_map = self.p_four_level_two_map
        self.level_map = self.level_two_map
        self.level_palette_map = self.level_two_palette_map
        self.player_one.mystate['color'] = '130'



    def load_level_three(self):
        self.grid_spacing = self.screen.get_size()[1]/self.level_two_map.shape[0]*4
        self.background = self.level_three_background_one
        self.background_one = self.level_three_background_one
        self.background_two =  self.level_three_background_two
        self.background_three =  self.level_three_background_three
        self.background_four =  self.level_three_background_four
        self.p_one_level_map = self.p_one_level_three_map
        self.p_two_level_map = self.p_two_level_three_map
        self.p_three_level_map = self.p_three_level_three_map
        self.p_four_level_map = self.p_four_level_three_map
        self.level_map = self.level_three_map
        self.level_palette_map = self.level_three_palette_map
        self.player_one.mystate['color'] = '130'

    def do_nothing(self):
        ze_goggles = 'they do nothing'

    def on_palette_change(self):
        return True

    def off_palette_change(self):
        return False 

    def move_player_to_start(self):
        for row in range(self.level_map.shape[0]):
            for col in range(self.level_map.shape[1]):
                if str(self.level_map[row][col]) == '333':
                    self.player_one_global_position = [col/4, row/4]
                    self.player_one_local_position = [col/4, row/4]
                    self.player_one.local_position = self.player_one_local_position



    def toggle_win(self):
        return True
    
    def map_tile_effect(self):
        #print str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])[0]

        if str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])[0] == '5':
            self.enable_palette_change = self.special_effect_map[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])]

        elif str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])[0] == '4':
            self.enable_player_color_change = self.special_effect_map[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])]

        elif str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])[0] == '9':
            self.win = self.special_effect_map[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])]


        #print self.enable_palette_change

    def movement_refused(self):
        print "OOOFF!"

    def on_change_player_color(self):
        print 'color change enabled'
        return True


    def negotiate_left_movement(self):
        if self.player_one_global_position[0] < 1:
            return self.movement_refused()
        elif COLORMAP[self.player_one.mystate['color']] == COLORMAP[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier])] or str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier]) == '101':

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
        elif COLORMAP[self.player_one.mystate['color']] == COLORMAP[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier])] or str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier +self.coordinate_multiplier]) == '101':

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
        elif COLORMAP[self.player_one.mystate['color']] == COLORMAP[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])] or str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2]) == '101':
           
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

        elif COLORMAP[self.player_one.mystate['color']] == COLORMAP[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])]or str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2]) == '101':
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
        if str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])[0] == '5':
            self.current_palette = self.palette_transition_map[self.current_palette]
        self.enable_palette_change = False

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

    def enforce_player_color_change(self):
        if str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])[0] == '4':
            self.player_one.mystate['color'] = self.special_colormap[str(self.level_map[self.player_one_global_position[1]*self.coordinate_multiplier + self.coordinate_multiplier/2][self.player_one_global_position[0]*self.coordinate_multiplier + self.coordinate_multiplier/2])]
        else:
            self.enable_player_color_change = False

    def update(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, self.background_position)
        
        self.player_one.draw(self.screen)
        self.map_tile_effect()
        self.enforce_palette()
        self.enforce_player_color_change()

        caption = "{} - FPS: {:.2f}".format(CAPTION,self.clock.get_fps())
        pg.display.set_caption(caption)

    def update_intro(self):
        self.screen.fill((0,0,0))

        self.intro.draw(self.screen)
        self.screen.blit(myFont.render('PRESS ENTER TO COMMENCE', True, (0,255,0)), (0,self.screen.get_height()/2)) 

        self.screen.blit(mySmallfont.render('Programmer: Michael Brothers', True, (0,255,0)), (0,self.screen.get_height()*10/16)) 
        self.screen.blit(mySmallfont.render('Art: Adrian Rucker', True, (0,255,0)), (0,self.screen.get_height()*11/16)) 
        self.screen.blit(mySmallfont.render('Music: Howard Timlin', True, (0,255,0)), (0,self.screen.get_height()*12/16)) 
        self.screen.blit(mySmallfont.render('Level Design: Adrian and Howard', True, (0,255,0)), (0,self.screen.get_height()*13/16)) 

        caption = "{} - CAN YOU HANDLE THE POWER? - FPS: {:.2f}".format(CAPTION,self.clock.get_fps())
        pg.display.set_caption(caption)

    def update_win(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.background, self.background_position)

        self.ananab.draw(self.screen)
        
        caption = "{} - MAXIMUM LEADER IS PLEASED - FPS: {:.2f}".format(CAPTION,self.clock.get_fps())
        pg.display.set_caption(caption)

    def main_loop(self):
        """Run around."""
        while not self.commence:
            self.event_loop()
            self.update_intro()
            pg.display.update()
            self.clock.tick(self.fps)

        self.load_level_one()
        self.move_player_to_start()
        while (not self.done and not self.win):
            self.event_loop()
            self.update()
            pg.display.flip()
            self.clock.tick(self.fps)

        self.commence = False
        """

        self.load_level_two()
        self.move_player_to_start()
        while (not self.done and not self.win):
            self.event_loop()
            self.update()
            pg.display.flip()
            self.clock.tick(self.fps)

        self.win = False

        self.load_level_three()
        self.move_player_to_start()
        while (not self.done and not self.win):
            self.event_loop()
            self.update()
            pg.display.flip()
            self.clock.tick(self.fps)

        self.commence = False
        """
        while not self.commence:
            self.event_loop()
            self.update_win()
            pg.display.flip()
            self.clock.tick(self.fps)

        

if __name__ == "__main__":
    resolution = (1200,640)
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_mode(resolution)
    pg.display.toggle_fullscreen()
    music_loaded = audio.load_music('../data/audio/pontiff.ogg')
    if music_loaded:
        pg.mixer.music.play(-1)
    run_it = Control()
    run_it.main_loop()
    pg.font.quit()
    pg.quit()
    sys.exit()

