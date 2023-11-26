from objects import *
from camera import *
from projection import *
from components import *
import pygame as pg

class SoftwareRender:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900 #Screen resolution
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH //2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, [1.5, 2, -4]) #0.5, 1, -4
        self.camera.camera_pitch(0.2)
        self.camera.camera_yaw(-0.1)
        self.projection = Projection(self)
        self.object = Object3D(self)
        self.object.translate([0.2, 0.4, 0.2])
        self.axes = Axes(self)
        self.axes.translate([0.7, 0.9, 0.7])
        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False
        self.world_axes.scale(2.5)
        self.world_axes.translate([0.0001, 0.0001, 0.0001])
        self.v1Button = InputButton(self, 50, 50, 40, 40, "1")
        self.v2Button = InputButton(self, 50, 100, 40, 40, "1")
        self.v3Button = InputButton(self, 50, 150, 40, 40, "1")
        self.vectorButtons = [self.v1Button, self.v2Button, self.v3Button] #These should be a single function tbh - will integrate into some kind of add vector button.
        self.transformButton = TransformButton(self, 150, 150, 145, 40, "Transform")
        self.mainToTransform = navigationButton(self, 50, 200, 250, 40, "Transformation menu")
        self.transformToMain = navigationButton(self, 50, 200, 250, 40, "Main")
        self.transformToPresets = navigationButton(self, 50, 300, 200, 40, "Presets")
        self.presetsToTransform = navigationButton(self, 50, 200, 250, 40, "Transformation menu")
        self.inputMatrix = InputMatrix(self, 400, 100)
        self.new_vector = CreateVector(self, 200, 500, "V1")
    
    def draw_main(self):
        self.screen.fill(pg.Color("darkslategray"))
        self.world_axes.draw()
        #self.axes.draw()
        #self.object.draw()


        #I will replace this with a new create-vector button which will create new instances of the create-vector class and add them to a list.
        #For each vector in the list, all of the following will be called basically.
        self.new_vector.draw()

        self.vector = Vector(self, self.transformButton.animation_vector)
        self.vector.translate([0.0001, 0.0001, 0.0001]) #Translation how far from z axis
        self.vector.movement_flag = False
        self.vector.draw()
        for button in self.vectorButtons:
            button.draw()
        self.transformButton.draw()


        self.mainToTransform.draw()
        
    
    def main(self):
        while True:
            if self.mainToTransform.switch == True:
                self.transformationScreen()
                self.mainToTransform.switch = False
            self.transformButton.transformAnimation()
            self.draw_main()
            self.camera.controls()
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    exit()
                for button in self.vectorButtons:
                    button.eventHandler(ev)
                self.transformButton.eventHandler(ev, self.vectorButtons)
                self.mainToTransform.eventHandler(ev)
                self.new_vector.eventHandler(ev)
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

    def draw_transform(self):
        self.screen.fill(pg.Color("darkslategray"))
        self.transformToMain.draw()
        self.transformToPresets.draw()
        self.inputMatrix.draw()

    
    def transformationScreen(self):
        self.screen.fill(pg.Color("darkslategray"))
        running = True
        while running:
            if self.transformToMain.switch == True:
                running = False
                self.transformToMain.switch = False
            if self.transformToPresets.switch == True:
                self.presetsScreen()
                self.transformToPresets.switch = False
            self.draw_transform()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                self.transformToMain.eventHandler(event)
                self.transformToPresets.eventHandler(event)
                self.inputMatrix.eventHandler(event)
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(60)

    def draw_presets(self):
        self.screen.fill(pg.Color("darkslategray"))
        self.presetsToTransform.draw()

    
    def presetsScreen(self):
        self.screen.fill(pg.Color("darkslategray"))
        running = True
        while running:
            if self.presetsToTransform.switch == True:
                running = False
                self.presetsToTransform.switch = False
            self.draw_presets()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                self.presetsToTransform.eventHandler(event)
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(60)


if __name__ =="__main__":
    app = SoftwareRender()
    app.main()