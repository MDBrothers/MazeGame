import pygame as pg
import numpy as np

class Player(object):
    def __init__(self, color, position, width, height, owner, whatILookLike):
        self.mystate = {'color': color,
                        'owner' : owner,
                        'visible' : True,
                        'rotation' : 'none',
                        'has_key' : False,
                        'scale' : 'normal'}

        self.local_position = position

        self.width = width
        self.height = height
        self.xoffset = width/8
        self.yoffset = height/8
        self.xscale_multiplier = 1.0
        self.yscale_multiplier = 1.0
        self.mySurface = whatILookLike        

        self.keyframe = 0
        self.animation_length = 2
        self.framecycler = 0
        
        self.subsurface_one_frame_one_rect = pg.Rect(0, 0, self.height, self.height)
        self.subsurface_one_frame_one = self.mySurface.subsurface(self.subsurface_one_frame_one_rect)
        self.subsurface_one_frame_two_rect = pg.Rect(0, self.height, self.height, self.height)
        self.subsurface_one_frame_two = self.mySurface.subsurface(self.subsurface_one_frame_two_rect)

        self.subsurface_two_frame_one_rect = pg.Rect(2*self.height-1, 0, self.height, self.height)
        self.subsurface_two_frame_one = self.mySurface.subsurface(self.subsurface_two_frame_one_rect)
        self.subsurface_two_frame_two_rect = pg.Rect(2*self.height-1, self.height, self.height, self.height)
        self.subsurface_two_frame_two = self.mySurface.subsurface(self.subsurface_two_frame_two_rect)

        self.subsurface_three_frame_one_rect = pg.Rect(3*self.height-1, 0, self.height, self.height)
        self.subsurface_three_frame_one = self.mySurface.subsurface(self.subsurface_three_frame_one_rect)
        self.subsurface_three_frame_two_rect = pg.Rect(3*self.height-1, self.height, self.height, self.height)
        self.subsurface_three_frame_two = self.mySurface.subsurface(self.subsurface_three_frame_two_rect)

        self.subsurface_four_frame_one_rect = pg.Rect(1*self.height-1, 0, self.height, self.height)
        self.subsurface_four_frame_one = self.mySurface.subsurface(self.subsurface_four_frame_one_rect)
        self.subsurface_four_frame_two_rect = pg.Rect(1*self.height-1, self.height, self.height, self.height)
        self.subsurface_four_frame_two = self.mySurface.subsurface(self.subsurface_four_frame_two_rect)

        self.p_one_animation = [self.subsurface_one_frame_one, self.subsurface_one_frame_two, True] 
        self.p_two_animation = [self.subsurface_two_frame_one, self.subsurface_two_frame_two, True] 
        self.p_three_animation = [self.subsurface_three_frame_one, self.subsurface_three_frame_two, True] 
        self.p_four_animation = [self.subsurface_four_frame_one, self.subsurface_four_frame_two, True] 

        self.myAnimations = [self.p_one_animation, self.p_two_animation, self.p_three_animation, self.p_four_animation]

        self.mySubsurfaces = [self.subsurface_one_frame_one, self.subsurface_two_frame_one, self.subsurface_three_frame_one, self.subsurface_four_frame_one]

        self.color_mapped_subsurface = {'110' : '0',
                                        '120' : '1',
                                        '130' : '2',
                                        '140' : '3'}
        
        self.myKeyframe = 0
        self.myAnimationLength = 0

        #self.scale_small()
        #self.mystate['scale'] = 'small'

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
        if self.keyframe < self.animation_length:
            what_to_draw = pg.transform.scale(self.myAnimations[int(self.color_mapped_subsurface[self.mystate['color']])][self.keyframe],(int(self.width*self.xscale_multiplier),int(self.height*self.yscale_multiplier)))

            myCanvas.blit(what_to_draw,(self.xoffset + self.local_position[0]*self.width,self.yoffset + self.local_position[1]*self.height))

            if self.framecycler % 9 == 0:
                self.keyframe += 1
                self.framecycler = 0

            self.framecycler += 1
        elif True:
            self.keyframe = 0
            self.framecycler += 1
            what_to_draw = pg.transform.scale(self.myAnimations[int(self.color_mapped_subsurface[self.mystate['color']])][self.keyframe],(int(self.width*self.xscale_multiplier),int(self.height*self.yscale_multiplier)))

            myCanvas.blit(what_to_draw,(self.xoffset + self.local_position[0]*self.width,self.yoffset + self.local_position[1]*self.height))


    def map_to_statefunction(self, requested_state):
        goggles = 'do nothing'


