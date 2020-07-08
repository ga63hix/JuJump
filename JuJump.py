# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 21:23:47 2020

@author: julia
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 20:24:07 2020

@author: julia
"""
import pygame as pg
import random
import numpy as np

import time
# Initialize Process
pg.init()

# Get a screen
screen = pg.display.set_mode((1000, 501)) #  700, 351))
pg.display.set_caption("JuJump")

# Default properties
font = pg.font.SysFont('Courier New', 25)
pg.font.init()

class Game:
    def __init__(self, screen):
        # General initalization
        self.done = False
        self.clock = pg.time.Clock()
        self.screen = screen
        self.screenLength, self.screenHeight = pg.display.get_surface().get_size()
        self.boy = pg.image.load("material/bird.png").convert_alpha()
        self.background = pg.image.load("material/background.png").convert()
        icon = pg.image.load("material/train.png")
        pg.display.set_icon(icon)
        
        # Track time
        self.t0 = time.time()

        # CHARACTER values
        self.boyX = 500
        self.boyY = 70
        self.boyHeight = 80
        x,y, self.boyLength, self.boyHeight = self.boy.get_rect()
        self.boyOnBeam = 1
        
        # BEAMS values   
        self.beam1X = self.boyX-10
        self.beam1Y = self.screenHeight/2
        self.firstBeamLength = 520
        self.heightBeams = 39
        self.floor = self.screenHeight*2
        self.ground = self.beam1Y
        self.beams = [[self.beam1X, self.beam1Y, self.firstBeamLength]] # List containing different lists, each three elements: x,y,length        
        # Game values
        self.velocity = 3
        self.gravity = 5
        self.jump = 0
        self.jumpSpeed = 0
        self.gapSize = random.randint(80,100)
        self.beamY = random.randint(300, 500)
        self.beamLength = random.randint(50, 200)

    def resetRandomValues(self):
        self.gapSize = random.randint(80,100)
        self.beamY = random.randint(300, 400)
        self.beamLength = random.randint(50, 100)
                
    def resetGame(self):
        pg.init()
        self.boyX = 500
        self.boyY = 70
        self.boyOnBeam = 1
        # BEAMS values
        self.beam1X = self.boyX-10
        self.beam1Y = self.screenHeight/2
        self.heightBeams = 39
        self.firstBeamLength = 600
        self.beams = [[self.beam1X, self.beam1Y, self.firstBeamLength]]
        
        self.velocity = 3
        self.gravity = 5
        self.jump = 0
        self.jumpSpeed = 0
        self.ground = self.beam1Y
        
        self.t0 = time.time()
                
    def jumpPossible(self):
        if self.boyOnBeam == 1 and (self.boyY+self.boyHeight <= self.ground+10 and self.boyY+self.boyHeight >= self.ground-10):
            self.gravity = 5 # reset to original
            self.jump = 17
            self.jumpSpeed = 19#13
        
    def quit_game(self):
        """Callback method to quit the game."""
        self.done = True
        
    def update_boy(self):
        if self.jump >= 0: # boy jumps
            self.jumpSpeed -= 1
            self.boyY -= self.jumpSpeed
            self.jump -= 1
            return
        
        ### Test all boxes
        for beam in self.beams:
            if self.boyX >= beam[0]-10 and self.boyX <= beam[0] + beam[2]: # checks if boy is over beam and adjusts self.ground (-10 because beam is not detected fast enough, even if he is quasi already there)
                self.boyOnBeam = 1
                self.ground = beam[1]
                break
            else:
                self.boyOnBeam = 0
                self.ground = self.floor
        
        if self.boyY+self.boyHeight <= self.ground-10: # boy is above beam or already below
            self.boyY += self.gravity
            self.gravity += 0.2       
        elif self.boyY+self.boyHeight > self.ground+10:
            self.boyY += self.gravity
            self.gravity += 0.2 
        else:
            self.boyY = self.ground-self.boyHeight
        
        # if boy is on beam --> too inexact, jumps over value self.ground
        
        if self.boyY+self.boyHeight >= self.floor: # game over
            self.resetGame()
            
        
    def update_beam(self):
        """If x coordinate of a beam is below the current gap value, a new beam 
        is created and added to self.beams.
        """
        for element in self.beams:
            element[0] -= self.velocity
#        self.beam1X -= self.velocity
    
        currentGap = self.screenLength - (self.beams[-1][0] + self.beams[-1][2])
        
        if currentGap > self.gapSize:
            # Create a new beam
            newBeamX = self.screenLength - 1
            newBeamY = self.beamY
            newBeamLength = self.beamLength
            self.beams.append([newBeamX, newBeamY, newBeamLength])
            if len(self.beams) > 7:   
                self.beams.pop(0)
            self.resetRandomValues()
            
    
        
    def run(self):
        while not self.done:
            self.clock.tick(60)
            self.handle_events()
            
            # Time tracking
            t1 = time.time()
            seconds = round(t1 - self.t0, 1)
            if seconds == 10.0:
                self.velocity = 3.5 # make it more difficult
            elif seconds > 20:
                self.velocity = 4
            elif seconds > 30:
                self.velocity = 4.5
            elif seconds > 40:
                self.velocity = 5
            text_surface = font.render(str(seconds), True, (0,0,0))
            
            
            # update values
            self.update_beam()
            self.update_boy()
            
            # background
            self.screen.fill((255,255,255))
            self.screen.blit(self.background, (0, 0))
            
            # Print time
            self.screen.blit(text_surface, (620, 30))
            
            # Show ALL beams
            for beam in self.beams:
                pg.draw.rect(self.screen, (255,255,255), (beam[0], beam[1], beam[2], self.heightBeams))
                
            # Show character
            self.screen.blit(self.boy, (self.boyX-(self.boyLength/2), self.boyY))

            # Show all elements
            pg.display.update()
            
    def getBeamLength(self):
        return random.randint(75, 160)
            
    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.done = True
                else:
                    self.jumpPossible()
                    
            
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                print(f"X Koordinate: {x}")
                print(f"Y Koordinate: {y}")

# Game Run
if __name__ == '__main__':
    pg.init()
    Game(screen).run()
    pg.quit()
    
'''Usefull sites
# KeyNames    
# https://www.pygame.org/docs/ref/key.html
Quelle Zug Icon: Icons erstellt von <a href="https://www.flaticon.com/de/autoren/iconixar" title="iconixar">iconixar</a> from <a href="https://www.flaticon.com/de/" title="Flaticon"> www.flaticon.com</a>
'''