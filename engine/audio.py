#!/usr/bin/python
import pygame as pg

class Dummysound:
    def play(self, times): 
        pass
    def play(self):
        pass

def load_sound(file):
    if not pg.mixer: 
        return Dummysound()
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print 'Warning, unable to load,', file
    return Dummysound()

def load_music(file):
    if not pg.mixer: 
        return False 
    try:
        pg.mixer.music.load(file)
        return True
    except pg.error:
        print 'Warning, unable to load,', file
    return False

