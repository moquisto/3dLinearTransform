import pygame as pg
from objects import *

class InputButton:
    def __init__(self, render, x, y, w, h, text = ""):
        self.render = render
        self.FONT = pg.font.Font(None, 32)
        self.COLOR_ACTIVATED, self.COLOR_INACTIVATED, self.COLOR = pg.Color("red"), pg.Color("black"), pg.Color("black")
        self.rectangle = pg.Rect(x, y, w, h)
        self.text = text
        self.displayed_text = self.FONT.render(self.text, True, self.COLOR)
        self.active = False
    
    def eventHandler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rectangle.collidepoint(event.pos) == True:
                self.active = True
            else:
                self.active = False
            self.COLOR = self.COLOR_ACTIVATED if self.active == True else self.COLOR_INACTIVATED
        if event.type == pg.KEYDOWN:
            if self.active == True:
                if event.key == pg.K_RETURN:
                    self.active = False
                    self.COLOR = self.COLOR_INACTIVATED
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.displayed_text = self.FONT.render(self.text, True, pg.Color("black"))


    def draw(self):
        pg.draw.rect(self.render.screen, self.COLOR, self.rectangle, 3)
        self.render.screen.blit(self.displayed_text, (self.rectangle.x + self.rectangle.w / 3, self.rectangle.y + self.rectangle.h / 4))

class TransformButton:
    def __init__(self, render, x, y, w, h, text = ""):
        self.render = render
        self.FONT = pg.font.Font(None, 32)
        self.COLOR = pg.Color("black")
        self.rectangle = pg.Rect(x, y, w, h)
        self.text = text
        self.vector = [1, 1, 1, 1]
        self.goal_vector = [1, 1, 1, 1]
        self.animation_vector = [1, 1, 1, 1]
        self.delta_coord = [0, 0, 0]
        self.change = False
        self.count = 1
    
    def eventHandler(self, event, vectorButtons):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rectangle.collidepoint(event.pos):
                for i in range(3):
                    self.goal_vector[i] = float(vectorButtons[i].text)
                    if self.vector[i] != self.goal_vector[i]:
                        sign = -1 if self.vector[i] > self.goal_vector[i] else 1
                        self.delta_coord[i] = sign*abs(self.vector[i] - (self.goal_vector[i]))
                        self.change = True
                print("current " + str(self.vector))
                print("end " + str(self.goal_vector))
                print("change " + str(self.delta_coord))

    def transformAnimation(self): #Modifies the vector values that are passed to the vector object until reaching goal-vector
        #This isn't the same thing as a matrix that scales something. It is slightly different since this can take something from 0 to 1.
        if self.change == True:
            #Since we are running this at 60 frames per second, if we want the animation to last for approximately 2 second, we should make each increment 120th of total
            for i in range(3):
                self.animation_vector[i] = self.animation_vector[i] + (1/60) * self.delta_coord[i] #after 120 iterations, animation will be equal to goal
            self.count += 1
            if self.count == 60:
                self.animation_vector = self.goal_vector[:]
                self.change = False
                self.count = 1
                self.delta_coord = [0, 0, 0]
                self.vector = self.animation_vector[:]
                print("changed "+ str(self.vector))

    def draw(self):
        pg.draw.rect(self.render.screen, self.COLOR, self.rectangle, 3)
        self.render.screen.blit(self.FONT.render(self.text, True, self.COLOR), (self.rectangle.x + self.rectangle.w / 8, self.rectangle.y + self.rectangle.h / 4))

class navigationButton:
    def __init__(self, render, x, y, w, h, text = ""):
        self.render = render
        self.FONT = pg.font.Font(None, 32)
        self.rectangle = pg.Rect(x, y, w, h)
        self.text = text
        self.COLOR = pg.Color("black")
        self.displayed_text = self.FONT.render(self.text, True, self.COLOR)
        self.switch = False
    
    def eventHandler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rectangle.collidepoint(event.pos) == True:
                self.switch = True
    
    def draw(self):
        pg.draw.rect(self.render.screen, pg.Color("black"), self.rectangle, 3)
        self.render.screen.blit(self.displayed_text, (self.rectangle.x + 10, self.rectangle.y + 10))