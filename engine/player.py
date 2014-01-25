import pygame as pg
import numpy as np

class Player(object):
    def __init__(self, color, position, width, height, owner, whatILookLike):
        self.mystate = {'color': color,
                        'global_position': position,
                        'local_position': position,
                        'owner' : owner,
                        'visible' : True,
                        'rotation' : 'none',
                        'has_key' : False,
                        'scale' : 'normal'}

        self.width = width
        self.height = height
        self.xoffset = width/8
        self.yoffset = height/8
        self.xscale_multiplier = 1.0
        self.yscale_multiplier = 1.0
        self.mySurface = whatILookLike        
        self.myKeyframe = 0
        self.myAnimationLength = 0

        self.scale_small()
        self.mystate['scale'] = 'small'
        self.scale_normal()
        self.mystate['scale'] = 'normal'
        self.scale_small()
        self.mystate['scale'] = 'small'
        self.scale_normal()
        self.mystate['scale'] = 'normal'


        self.scale_large()
        self.mystate['scale'] = 'large'
        self.scale_normal()
        self.mystate['scale'] = 'normal'
        self.scale_small()
        self.mystate['scale'] = 'small'
        self.scale_normal()
        self.mystate['scale'] = 'normal'







    def move_to_coordinates(self, new_coordinates):
        self.mystate['local_position'] = new_coordinates

    def scale_small(self):
        if self.mystate['scale'] == 'normal':
            self.xoffset += self.width/4
            self.yoffset += self.width/4
            self.xscale_multiplier = .5
            self.yscale_multiplier = .5

        elif self.mystate['scale'] == 'large':
            self.xoffset += self.width*3/4
            self.yoffset += self.width*3/4
            self.xscale_multiplier = .5
            self.yscale_multiplier = .5

        else:
            nothing = 'do'

    def scale_normal(self):
        if self.mystate['scale'] == 'small':
            self.xoffset -= self.width/4
            self.yoffset -= self.width/4
            self.xscale_multiplier = 1.0
            self.yscale_multiplier = 1.0

        elif self.mystate['scale'] == 'large':
            self.xoffset += self.width/2
            self.yoffset += self.width/2
            self.xscale_multiplier = 1.0
            self.yscale_multiplier = 1.0

        else:
            ze_goggles = 'do nothing'

    def scale_large(self):
        if self.mystate['scale'] == 'normal':
            self.xoffset -= self.width/2
            self.yoffset -= self.width/2
            self.xscale_multiplier = 2.0
            self.yscale_multiplier = 2.0

        if self.mystate['scale'] == 'small':
            self.xoffset -= self.width*3/4
            self.yoffset -= self.width*3/4
            self.xscale_multiplier = 2.0
            self.yscale_multiplier = 2.0

        else:
            ze_goggles = 'do nothing'

    def draw(self, myCanvas):
        myCanvas.blit(pg.transform.scale(self.mySurface, (int(self.width*self.xscale_multiplier), int(self.height*self.yscale_multiplier))), (self.xoffset + self.mystate['local_position'][0]*self.width, self.yoffset + self.mystate['local_position'][1]*self.height))

    def map_to_statefunction(self, requested_state):
        goggles = 'do nothing'


