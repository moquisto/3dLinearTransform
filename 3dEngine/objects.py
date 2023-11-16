import pygame as pg
from matrices import *
#We don't need to import numpy or math since we import that from the matrices.py file

class Object3D:
    def __init__(self, render):
        self.render = render
        self.verteces = np.array([(0, 0 ,0 ,1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1),
                                  (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)])
        
        self.faces = np.array([(0,1,2,3), (4,5,6,7), (0,4,5,1), (2,3,7,6), (1,2,6,5), (0,3,7,4)])

        self.font = pg.font.SysFont("Arial", 30, bold=True)
        self.color_faces = [(pg.Color("orange"), face) for face in self.faces]
        self.movement_flag, self.draw_verteces = True, True
        self.label = ""
    
    def draw(self):
        self.screen_projection()
        self.movement()
    
    def movement(self):
        if self.movement_flag:
            self.rotate_y(pg.time.get_ticks() % 0.005)
    
    def screen_projection(self):
        verteces = self.verteces @ self.render.camera.camera_matrix()
        verteces = verteces @ self.render.projection.projection_matrix
        verteces /= verteces[:, -1].reshape(-1, 1) #Divide by w
        verteces[(verteces > 2) | (verteces < -2)] = 0 #Remove verteces outside screen boundaries. This will however remove lines constructed b/w verteces. Should set them
        #To the edges of the screen or just allow them to exist maybe. I don't really know.
        verteces = verteces @ self.render.projection.to_screen_matrix
        verteces = verteces[:, :2] #x, y, z, w -> x, y

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = verteces[face]
            if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, color, polygon, 3)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color("white"))
                    self.render.screen.blit(text, polygon[-1])
        if self.draw_verteces:
            for vertex in verteces:
                if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)): #Checks if we removed vertex (checks for array rows True, 0 evaluates to False)
                    pg.draw.circle(self.render.screen, pg.Color("white"), vertex, 6)
    
    def translate(self, pos):
        self.verteces = self.verteces @ translate(pos) #matrix multiplication? No, I think the @ sign allows us to use the imported matrix functions with the same name?

    def scale(self, scale_to):
        self.verteces = self.verteces @ scale(scale_to)
    
    def rotate_x(self, angle):
        self.verteces = self.verteces @rotate_x(angle)

    def rotate_y(self, angle):
        self.verteces = self.verteces @rotate_y(angle)

    def rotate_z(self, angle):
        self.verteces = self.verteces @rotate_z(angle)

class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.verteces = np.array([(0,0,0,1), (1,0,0,1), (0,1,0,1), (0,0,1,1)])
        self.faces = np.array([(0,1), (0,2), (0,3)])
        self.colors = [pg.Color("red"), pg.Color("green"), pg.Color("blue")]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_verteces = False
        self.label = "XYZ"