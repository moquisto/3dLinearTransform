import pygame as pg
from objects import *

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

class InputButton:
    def __init__(self, render, x, y, w, h, text = ""):
        self.render = render
        self.FONT = pg.font.Font(None, 32)
        self.COLOR_ACTIVATED, self.COLOR_INACTIVATED, self.COLOR = pg.Color("red"), pg.Color("white"), pg.Color("white")
        self.TEXT_COLOR = pg.Color("white")
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
                    self.displayed_text = self.FONT.render(self.text, True, self.TEXT_COLOR)
                else:
                    try:
                        int(event.unicode)
                        self.text += event.unicode
                        self.displayed_text = self.FONT.render(self.text, True, self.TEXT_COLOR)
                    except:
                        if event.unicode == "." or "-":
                            self.text += event.unicode
                            self.displayed_text = self.FONT.render(self.text, True, self.TEXT_COLOR)

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
        pg.draw.rect(self.render.screen, pg.Color("white"), self.container, 3)
        self.render.screen.blit(self.FONT.render(self.text, True, pg.Color("white")), (self.container.x + 10, self.container.y + 10))
        if len(self.vectorList) != 0:
            for vectorPack in self.vectorList:
                if vectorPack.remove == True:
                    self.vectorList.remove(vectorPack)
                else:
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
        self.exitBox = pg.Rect(x+self.container.w - 20, y-10, 10, 10)
        self.FONT = pg.font.Font(None, 32)
        self.COLOR = pg.Color("white")
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
        self.remove = False

    def draw(self):
        pg.draw.rect(self.render.screen, self.COLOR, self.container, 3)
        for button in self.inputButtons:
            button.draw()
        pg.draw.rect(self.render.screen, pg.Color("red"), self.exitBox)
        pg.draw.rect(self.render.screen, self.COLOR, self.confirmationButton, 3)
        self.render.screen.blit(self.FONT.render("Change", True, self.COLOR), (self.confirmationButton.x + self.confirmationButton.w / 8, self.confirmationButton.y + self.confirmationButton.h / 4))
        self.render.screen.blit(self.FONT.render(self.text, True, pg.Color("red")), (self.container.x + 80, self.container.y + 15))
        self.vector = Vector(self.render, self.animation_vector)
        self.vector.translate([0.0001, 0.0001, 0.0001])
        self.vector.movement_flag = False
        self.vector.draw()
    
    def transformationHandler(self, matrix):
        tempVector = []
        for i in range(3):
            tempVector.append(self.og_vector[i])
        transformedVector = matrix@tempVector
        for i in range(3):
            self.goal_vector[i] = transformedVector[i]
            if self.og_vector[i] != self.goal_vector[i]:
                sign = -1 if self.og_vector[i] > self.goal_vector[i] else 1
                self.delta_coord[i] = sign*abs(self.og_vector[i] - (self.goal_vector[i]))
                self.change = True
        self.animate()
        for i in range(3):
            self.inputButtons[i].text = str(self.goal_vector[i])
            self.inputButtons[i].displayed_text = self.inputButtons[i].FONT.render(str(self.goal_vector[i]), True, pg.Color("white"))
        

    def eventHandler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.exitBox.collidepoint(event.pos):
                    self.remove = True
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
                self.exitBox.move_ip(event.rel)
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
This was part of the foundation for the VectorPackage class - name was slightly misleading
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
        self.COLOR = pg.Color("white")
        self.displayed_text = self.FONT.render(self.text, True, self.COLOR)
        self.switch = False
    
    def eventHandler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rectangle.collidepoint(event.pos) == True:
                self.switch = True
    
    def draw(self):
        pg.draw.rect(self.render.screen, self.COLOR, self.rectangle, 3)
        self.render.screen.blit(self.displayed_text, (self.rectangle.x + 10, self.rectangle.y + 10))

class InputMatrix:
    #Will render a rectangle with 9 inputbuttons inside. I will then add a drag effect on the big rectangle.
    #This will only be the matrix, I won't have any transformation buttons attached since I want to be able to chain transformations.
    #How will I do the transformation? I still need to have a choose vector button. It can basically be current transformation button but I reduce the animation time
    #To maybe 1 second or 1/2 second. The actual transformation button should be a modificed version of the current transformation button. Still I think I need to change
    #the transformation button a bit.
    def __init__(self, render, x, y, text = ""):
        self.container = pg.Rect(x-20, y-40, 180, 200)
        self.exitBox = pg.Rect(x+self.container.w - 30, y-40, 10, 10)
        self.remove = False
        self.buttonList = []
        self.render = render
        self.text = text
        self.FONT = pg.font.Font(None, 32)
        self.active = False
        for i in range(3):
            for j in range(3):
                self.buttonList.append(InputButton(render, x+(j*50), y+(i*50), 40, 40, "1"))
    
    def draw(self):
        pg.draw.rect(self.render.screen, pg.Color("red"), self.exitBox)
        pg.draw.rect(self.render.screen, pg.Color("white"), self.container, 3)
        for button in self.buttonList:
            button.draw()
        self.render.screen.blit(self.FONT.render(self.text, True, pg.Color("red")), (self.container.x + 75, self.container.y + 10))
    
    def eventHandler(self, event):
        #Move matrix
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.exitBox.collidepoint(event.pos):
                    self.remove = True
                if self.container.collidepoint(event.pos):
                    self.active = True
        if self.active == True:
            if event.type == pg.MOUSEMOTION:
                for button in self.buttonList:
                    button.rectangle.move_ip(event.rel)
                self.container.move_ip(event.rel)
                self.exitBox.move_ip(event.rel)
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.active = False
        for button in self.buttonList: #Activate inputbuttons
            button.eventHandler(event)

class CreateMatrix:
    def __init__(self, render, x, y):
        self.render = render
        self.text = "Spawn matrix"
        self.FONT = pg.font.Font(None, 32)
        self.container = pg.Rect(x, y, 170, 40)
        self.matrixList = []
    
    def eventHandler(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.container.collidepoint(event.pos):
                    self.matrixList.append(InputMatrix(self.render, 400, 100, f"M{len(self.matrixList)+1}"))
        if len(self.matrixList) != 0:
            for matrix in self.matrixList:
                matrix.eventHandler(event)

    def draw(self):
        pg.draw.rect(self.render.screen, pg.Color("white"), self.container, 3)
        self.render.screen.blit(self.FONT.render(self.text, True, pg.Color("white")), (self.container.x + 10, self.container.y + 10))
        if len(self.matrixList) != 0:
            for matrix in self.matrixList:
                if matrix.remove == True:
                    self.matrixList.remove(matrix)
                else:
                    matrix.draw()
        

class TransformButton:
    def __init__(self, render, x, y):
        self.render = render
        self.container = pg.Rect(x, y, 200, 40)
        self.text = "Transform"
        self.FONT = pg.font.Font(None, 32)
        self.COLOR = pg.Color("white")
        self.matrices = []

    def eventHandler(self, event, objectLists = []):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.container.collidepoint(event.pos):
                    #Get the objects to be transformed
                    objects = []
                    for oList in objectLists:
                        for o in oList:
                            objects.append(o)
                    if objects != []:
                        """Check whether objectList is empty, if that's the case, pass, else, check the order of the matrices on the transformationscreen
                        and perform a few matrixmultiplications to obtain the resulting transformation. Then apply that on the objects in objectList.
                        How Should I design objectList? Later on, I will have more than just vectors, and I could also have both a grid and a few vectors
                        active at the same time. Since I allow the user to change the vector manually and not just using transformations there has to be communication
                        b/w classes as well. This is going to be a bit tricky actually. Lets start step by step. Create some kind of object-list, pass it to transform button,
                        if you press the transform-button, just print the list of objects in objectList."""
                        #This part sorts the matrices according to their x-position on the transformation-screen.
                        mSorted = []
                        mReady = []
                        if self.matrices != []:
                            for matrix in self.matrices:
                                if len(mSorted) == 0:
                                    mSorted.append(matrix)
                                else:
                                    for each in mSorted:
                                        inserted = False
                                        if matrix.container.x < each.container.x:
                                            mSorted.insert(mSorted.index(each), matrix)
                                            inserted = True
                                            break
                                    if inserted == False:
                                        mSorted.append(matrix)
                            mSorted.reverse()
                            #This part formats the matrices into the correct format for multiplication.
                            for matrix in mSorted:
                                formatted = []
                                for i in range(3):
                                    row = []
                                    for j in range(3):
                                        row.append(float(matrix.buttonList[i*3 + j].text))
                                    formatted.append(row)
                                formatted = np.array(formatted)
                                mReady.append(formatted)
                            #This part multiplies into a singular matrix
                            for i in range(len(mReady)):
                                if i != len(mReady) - 1:
                                    mReady[i+1] = mReady[i+1]@mReady[i]
                                else:
                                    result = mReady[i]
                            for o in objects:
                                o.transformationHandler(result)
                            #Now its time to create the new "goal vectors". This part will animate every change. I basically need to write the logic for animation
                            #and all of that but for all kinds of objects and not just vectors. At the moment I only have vectors though. I can modify it later to 
                            #accomodate for other types of 3d objects.
                            #Vector object is basically just a a vertex and a line drawn b/w. Since that is the case, other transformations will be done in
                            #practically the same way, since the verteces shift positions and straight lines are drawn b/w.
                            #In other words, for each object that is in the objectList, the transformation has to be applied to every vertex's first 3 position since
                            #the fourth is kept at a constant 1.
                            #For the vector, what I need to do as well is to change each vectorPackage to reflect the changes caused by the transformation as well.

                        else:
                            print("No matrices")
                    else:
                        print("No objects to transform")

    def draw(self):
        pg.draw.rect(self.render.screen, self.COLOR, self.container, 3)
        self.render.screen.blit(self.FONT.render(self.text, True, self.COLOR), (self.container.x + 10, self.container.y + 10))



    """class VectorPackage:
    def __init__(self, render, x, y, text = ""):
        self.render = render
        self.container = pg.Rect(x-10, y-10, 190, 160)
        self.FONT = pg.font.Font(None, 32)
        self.COLOR = pg.Color("white")
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
                self.og_vector = self.animation_vector[:]"""