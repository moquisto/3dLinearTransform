import pygame as pg
from objects import *

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

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
                    self.displayed_text = self.FONT.render(self.text, True, pg.Color("black"))
                else:
                    try:
                        int(event.unicode)
                        self.text += event.unicode
                        self.displayed_text = self.FONT.render(self.text, True, pg.Color("black"))
                    except:
                        if event.unicode == ".":
                            self.text += event.unicode
                            self.displayed_text = self.FONT.render(self.text, True, pg.Color("black"))

    def draw(self):
        pg.draw.rect(self.render.screen, self.COLOR, self.rectangle, 3)
        self.render.screen.blit(self.displayed_text, (self.rectangle.x + self.rectangle.w / 3, self.rectangle.y + self.rectangle.h / 4))

class CreateVector:
    def __init__(self, render, x, y):
        self.render = render
        self.text = "Spawn vector"
        self.FONT = pg.font.Font(None,32)
        self.container = pg.Rect(x, y, 170, 40)
        self.vectorList = []
    
    def eventHandler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.container.collidepoint(event.pos):
                    self.vectorList.append(VectorPackage(self.render, 50, 500, f"V{len(self.vectorList)+1}"))
        if len(self.vectorList) != 0:
            for vectorPack in self.vectorList:
                vectorPack.eventHandler(event)

    def draw(self):
        pg.draw.rect(self.render.screen, pg.Color("black"), self.container, 3)
        self.render.screen.blit(self.FONT.render(self.text, True, pg.Color("black")), (self.container.x + 10, self.container.y + 10))
        if len(self.vectorList) != 0:
            for vectorPack in self.vectorList:
                vectorPack.draw()


class VectorPackage:
    """This class will create a 3d vector object as well as 3 input buttons for xyz coordinates and 1 confirm button.
    With this class I will be able to repeatedly create new vectors to experiment with. Is this necessary? Perhaps not, but it will likely make
    things a bit easier when linking matrices to vectors. I should later on add some kind of "for active_object in 3dobjects: apply transformation" thing.
    Should I add the possibility to drag and drop these too? Tbh could be nice.
    Another reason to construct this class is to freely be able to remove vectors if I want to exchange it for a grid for example. This will
    also lay the groundwork for similar classes.
    I should label new vectors according to numbers"""
    def __init__(self, render, x, y, text = ""):
        self.render = render
        self.container = pg.Rect(x-10, y-10, 190, 160)
        self.FONT = pg.font.Font(None, 32)
        self.COLOR = pg.Color("black")
        self.inputButtons = []
        self.active = False
        for i in range(3):
            self.inputButtons.append(InputButton(render, x, y+(i*50), 40, 40, "1"))
        self.confirmationButton = pg.Rect(x+60, y+50, 110, 40)
        self.text = text
        self.og_vector = [1, 1, 1, 1]
        self.goal_vector = [1, 1, 1, 1]
        self.animation_vector = [1, 1, 1, 1]
        self.delta_coord = [0, 0, 0]
        self.change = False
        self.count = 1

    def draw(self):
        pg.draw.rect(self.render.screen, self.COLOR, self.container, 3)
        for button in self.inputButtons:
            button.draw()
        pg.draw.rect(self.render.screen, self.COLOR, self.confirmationButton, 3)
        self.render.screen.blit(self.FONT.render("Change", True, self.COLOR), (self.confirmationButton.x + self.confirmationButton.w / 8, self.confirmationButton.y + self.confirmationButton.h / 4))
        self.render.screen.blit(self.FONT.render(self.text, True, pg.Color("red")), (self.container.x + 80, self.container.y + 15))
        self.vector = Vector(self.render, self.animation_vector)
        self.vector.translate([0.0001, 0.0001, 0.0001])
        self.vector.movement_flag = False
        self.vector.draw()

    def eventHandler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.container.collidepoint(event.pos):
                    self.active = True
                if self.confirmationButton.collidepoint(event.pos):
                    for i in range(3):
                        self.goal_vector[i] = float(self.inputButtons[i].text)
                        if self.og_vector[i] != self.goal_vector[i]:
                            sign = -1 if self.og_vector[i] > self.goal_vector[i] else 1
                            self.delta_coord[i] = sign*abs(self.og_vector[i] - (self.goal_vector[i]))
                            self.change = True
                    print("current " + str(self.og_vector))
                    print("change " + str(self.delta_coord))
                    print("end " + str(self.goal_vector))
        if self.active == True:
            if event.type == pg.MOUSEMOTION:
                for button in self.inputButtons:
                    button.rectangle.move_ip(event.rel)
                self.container.move_ip(event.rel)
                self.confirmationButton.move_ip(event.rel)
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.active = False
        for button in self.inputButtons:
            button.eventHandler(event)
    
    def animate(self):
        if self.change == True:
            for i in range(3):
                self.animation_vector[i] = self.animation_vector[i] + (1/60) * self.delta_coord[i]
            self.count += 1
            if self.count == 60:
                self.animation_vector = self.goal_vector[:]
                self.change = False
                self.count = 1
                self.delta_coord = [0, 0, 0]
                self.og_vector = self.animation_vector[:]


"""
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
"""
        
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

class InputMatrix:
    #Will render a rectangle with 9 inputbuttons inside. I will then add a drag effect on the big rectangle.
    #This will only be the matrix, I won't have any transformation buttons attached since I want to be able to chain transformations.
    #How will I do the transformation? I still need to have a choose vector button. It can basically be current transformation button but I reduce the animation time
    #To maybe 1 second or 1/2 second. The actual transformation button should be a modificed version of the current transformation button. Still I think I need to change
    #the transformation button a bit.
    def __init__(self, render, x, y):
        self.container = pg.Rect(x-20, y-20, 180, 180)
        self.buttonList = []
        self.render = render
        self.active = False
        for i in range(3):
            for j in range(3):
                self.buttonList.append(InputButton(render, x+(j*50), y+(i*50), 40, 40, "1"))
    
    def draw(self):
        pg.draw.rect(self.render.screen, pg.Color("grey"), self.container)
        for button in self.buttonList:
            button.draw()
    
    def eventHandler(self, event):
        #Move matrix
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.container.collidepoint(event.pos):
                    self.active = True
        if self.active == True:
            if event.type == pg.MOUSEMOTION:
                for button in self.buttonList:
                    button.rectangle.move_ip(event.rel)
                self.container.move_ip(event.rel)
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.active = False
        for button in self.buttonList: #Activate inputbuttons
            button.eventHandler(event)
