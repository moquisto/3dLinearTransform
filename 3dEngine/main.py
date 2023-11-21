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
        self.vectorButtons = [self.v1Button, self.v2Button, self.v3Button]
        self.transformButton = TransformButton(self, 150, 150, 145, 40, "Transform")

    
    def draw(self):
        self.screen.fill(pg.Color("darkslategray"))
        self.world_axes.draw()
        #self.axes.draw()
        #self.object.draw()
        self.vector = Vector(self, self.transformButton.animation_vector)
        self.vector.translate([0.0001, 0.0001, 0.0001]) #Translation how far from z axis
        self.vector.movement_flag = False
        self.vector.draw()
        for button in self.vectorButtons:
            button.draw()
        self.transformButton.draw()
        
    
    def run(self):
        while True:
            self.transformButton.transformAnimation()
            self.draw()
            self.camera.controls()
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    exit()
                for button in self.vectorButtons:
                    button.eventHandler(ev)
                self.transformButton.eventHandler(ev, self.vectorButtons)
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ =="__main__":
    app = SoftwareRender()
    app.run()